#!/usr/bin/env python3
# =============================================================================
#   AC RUNE 0.1  (2026)  [C] AC HOLDING  --  a Team Flames / Samsoft joint
#   -------------------------------------------------------------------------
#   An ORIGINAAL dark-world AU RPG in one file. files = off. 60 fps. meow.
#   Original story, original cast, original procedural chiptune OST.
#   (No copyrighted game assets, music, or characters are reproduced.)
#
#   CAST
#     AC      - a quiet blue cat. the vessel. (hero)
#     RYEN    - a time traveller with cracked goggles. (rude one)
#     LASSE   - a soft-spoken fox. joins in CH3. (healer)
#     PLOMBO  - a laid-back mustachioed plumber OC. judges you in CH5.
#     WRENCHARD - the Pipe Knight. plumber-armor OC. opens the fountains.
#     BECCA   - runs the house. worries. (mom energy)
#     JOSEPH  - classmate. grows sunflowers. (big warm guy)
#
#   CHAPTERS
#     CH1 SCHOOL OF STATIC   CH2 NEON HARBOR   CH3 BOARDWALK VHS
#     CH4 THE HOLLOW CHOIR   CH5 PIPEWORKS
#
#   OST (all original, rendered live by the built-in synth):
#     startup_ver. / field_of_static / neon_harbor / boardwalk_vhs
#     hollow_choir / pipeworks / rude_rumble / PREFECT! / CIRCUIT CROWN
#     JESTER STATIC / WARDEN'S HYMN / KNIGHT OF PIPES / plombo's_theme
#     a_cat's_tomorrow
#
#   CONTROLS:  Arrows move - Z confirm - X cancel - M mute - ESC quit
#   RUN:       python3 ac_rune.py          (python 3.10+ incl. 3.14)
# =============================================================================
import os, sys, math, random, array

SMOKE = "--smoke" in sys.argv
if SMOKE:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

# ---------------------------------------------------------------- constants
W, H   = 640, 480
FPS    = 60
SR     = 22050
BLUE   = (51, 204, 255)          # electric flames-blue
WHITE  = (240, 240, 240)
BLACK  = (6, 6, 10)
YELLOW = (255, 230, 90)
RED    = (255, 70, 90)
GREEN  = (90, 230, 130)
ORANGE = (255, 170, 60)
PURPLE = (200, 120, 255)
GRAY   = (120, 120, 140)
BOX    = pygame.Rect(170, 238, 300, 162)

CH_TITLES = ["CH1: SCHOOL OF STATIC", "CH2: NEON HARBOR", "CH3: BOARDWALK VHS",
             "CH4: THE HOLLOW CHOIR", "CH5: PIPEWORKS"]
CH_PAL = [((18,18,30),(40,40,70)), ((6,20,34),(10,60,90)), ((26,10,30),(70,20,80)),
          ((14,14,14),(60,50,30)), ((8,24,16),(20,80,50))]

# ---------------------------------------------------------------- audio synth
NAMES = {'C':-9,'C#':-8,'Db':-8,'D':-7,'D#':-6,'Eb':-6,'E':-5,'F':-4,'F#':-3,
         'Gb':-3,'G':-2,'G#':-1,'Ab':-1,'A':0,'A#':1,'Bb':1,'B':2}
def nfreq(name):
    octv = int(name[-1]); key = name[:-1]
    return 440.0 * (2 ** ((NAMES[key] + (octv - 4) * 12) / 12))

def osc(w, f, t):
    p = (t * f) % 1.0
    if w == 'sq':  return 1.0 if p < 0.5 else -1.0
    if w == 'saw': return 2.0 * p - 1.0
    if w == 'tri': return 4.0 * abs(p - 0.5) - 1.0
    return random.uniform(-1.0, 1.0)

# ------- original melodies (note, beats). 'R' = rest --------------------------
MEL_T = [('A3',1),('C4',1),('E4',1),('A4',1),('G4',2),('E4',2),
         ('F4',1),('E4',1),('D4',1),('C4',1),('D4',2),('E4',2),
         ('A3',1),('C4',1),('E4',1),('A4',1),('B4',2),('C5',2),
         ('B4',1),('A4',1),('G4',1),('E4',1),('A4',4)]
BAS_T = [('A2',2),('A2',2),('F2',2),('G2',2)]

MEL_W = [('C4',.5),('E4',.5),('G4',.5),('E4',.5),('A4',.5),('G4',.5),('E4',1),
         ('F4',.5),('A4',.5),('C5',.5),('A4',.5),('G4',1.5),('R',.5),
         ('E4',.5),('G4',.5),('C5',.5),('G4',.5),('B4',.5),('A4',.5),('G4',1),
         ('F4',.5),('E4',.5),('D4',.5),('E4',.5),('C4',2)]
BAS_W = [('C3',1),('G2',1),('A2',1),('F2',1)]

MEL_B = [('E4',.5),('E4',.5),('G4',.5),('E4',.5),('D4',.5),('E4',.5),('B3',1),
         ('C4',.5),('C4',.5),('E4',.5),('C4',.5),('B3',.5),('C4',.5),('A3',1),
         ('E4',.5),('G4',.5),('A4',.5),('B4',.5),('A4',.5),('G4',.5),('E4',1),
         ('D4',.5),('E4',.5),('G4',.5),('E4',.5),('D4',1.5),('R',.5)]
BAS_B = [('E2',1),('E2',1),('C3',1),('D3',1)]

MEL_X = [('A3',.5),('A3',.5),('C4',.5),('A3',.5),('D#4',.5),('D4',.5),('C4',.5),('A3',.5),
         ('E4',.5),('E4',.5),('F4',.5),('E4',.5),('D4',.5),('C4',.5),('B3',.5),('C4',.5),
         ('A4',.5),('G4',.5),('F4',.5),('E4',.5),('F4',.5),('E4',.5),('D4',.5),('C4',.5),
         ('B3',1),('E4',1),('A3',2)]
BAS_X = [('A2',.5),('A2',.5),('A2',.5),('G2',.5),('F2',.5),('F2',.5),('G2',.5),('G2',.5)]

MEL_F = [('D4',2),('F4',2),('A4',2),('G4',1),('F4',1),('E4',2),('C#4',2),
         ('D4',2),('A3',2),('D4',1),('E4',1),('F4',1),('G4',1),
         ('A4',2),('C5',2),('A4',1),('G4',1),('F4',1),('E4',1),('D4',4)]
BAS_F = [('D2',2),('D2',2),('A2',2),('A2',2)]

SONGS = {  # key: (melody, bass, bpm, wave, transpose, display name)
 'title':  (MEL_T,BAS_T, 92,'sq',  0,"startup_ver."),
 'world0': (MEL_W,BAS_W,118,'sq',  0,"field_of_static"),
 'world1': (MEL_W,BAS_W,124,'saw', 2,"neon_harbor"),
 'world2': (MEL_W,BAS_W,112,'tri',-3,"boardwalk_vhs"),
 'world3': (MEL_W,BAS_W,100,'tri',-5,"hollow_choir"),
 'world4': (MEL_W,BAS_W,128,'saw', 5,"pipeworks"),
 'battle': (MEL_B,BAS_B,142,'sq',  0,"rude_rumble"),
 'boss0':  (MEL_X,BAS_X,148,'sq',  0,"PREFECT!"),
 'boss1':  (MEL_X,BAS_X,152,'saw', 3,"CIRCUIT CROWN"),
 'boss2':  (MEL_X,BAS_X,156,'sq', -2,"JESTER STATIC"),
 'boss3':  (MEL_X,BAS_X,146,'tri',-4,"WARDEN'S HYMN"),
 'final':  (MEL_F,BAS_F,106,'saw', 0,"KNIGHT OF PIPES"),
 'plombo': (MEL_T,BAS_T,148,'tri',-5,"plombo's_theme"),
 'end':    (MEL_W,BAS_W, 92,'tri', 0,"a_cat's_tomorrow"),
}

class Music:
    def __init__(self, ok):
        self.ok = ok; self.cache = {}; self.cur = None; self.snd = None
        self.mute = False; self.now = ""
    def build(self, key):
        mel, bas, bpm, wave, tr, name = SONGS[key]
        spb = 60.0 / bpm
        total = sum(b for _, b in mel)
        n = int(total * spb * SR)
        buf = [0.0] * n
        # lead
        pos = 0
        for nt, b in mel:
            ns = int(b * spb * SR)
            if nt != 'R':
                f = nfreq(nt) * (2 ** (tr / 12))
                for i in range(ns):
                    env = 1.0 if i < ns - 800 else (ns - i) / 800.0
                    buf[pos + i] += osc(wave, f, i / SR) * 0.20 * env
            pos += ns
        # bass (looped triangle)
        pos = 0; bi = 0
        while pos < n:
            nt, b = bas[bi % len(bas)]; bi += 1
            ns = min(int(b * spb * SR), n - pos)
            f = nfreq(nt) * (2 ** (tr / 12))
            for i in range(ns):
                env = 1.0 if i < ns - 600 else (ns - i) / 600.0
                buf[pos + i] += osc('tri', f, i / SR) * 0.16 * env
            pos += ns
        # hat tick each beat
        step = int(spb * SR); i = 0
        while i < n:
            for j in range(min(500, n - i)):
                buf[i + j] += random.uniform(-1, 1) * 0.05 * (1 - j / 500)
            i += step
        a = array.array('h', (int(max(-1.0, min(1.0, s)) * 26000) for s in buf))
        return pygame.mixer.Sound(buffer=a.tobytes()), name
    def play(self, key):
        if not self.ok or key == self.cur: return
        if self.snd: self.snd.stop()
        if key not in self.cache:
            try: self.cache[key] = self.build(key)
            except Exception: self.ok = False; return
        self.snd, self.now = self.cache[key]
        self.cur = key
        if not self.mute: self.snd.play(-1)
    def toggle(self):
        self.mute = not self.mute
        if self.snd: self.snd.stop() if self.mute else self.snd.play(-1)

def tone(freq, dur, wave='sq', vol=0.3, slide=0.0):
    n = int(dur * SR); a = array.array('h')
    for i in range(n):
        f = freq + slide * (i / n)
        env = 1 - i / n
        a.append(int(max(-1, min(1, osc(wave, f, i / SR) * vol * env)) * 26000))
    return pygame.mixer.Sound(buffer=a.tobytes())

# ---------------------------------------------------------------- helpers
def txt(surf, s, x, y, size=18, col=WHITE, center=False, font=[None]*80):
    if font[size] is None: font[size] = pygame.font.Font(None, size + 6)
    img = font[size].render(s, False, col)
    r = img.get_rect()
    if center: r.center = (x, y)
    else: r.topleft = (x, y)
    surf.blit(img, r); return r

def draw_actor(s, x, y, who, f=0, scale=1.0):
    bob = int(math.sin(f * 0.15) * 2)
    x, y = int(x), int(y + bob)
    sz = int(22 * scale)
    if who == 'AC':      # blue cat
        pygame.draw.rect(s, BLUE, (x - sz//2, y - sz, sz, sz), border_radius=4)
        pygame.draw.polygon(s, BLUE, [(x - sz//2, y - sz), (x - sz//2 + 6, y - sz - 9), (x - sz//2 + 10, y - sz)])
        pygame.draw.polygon(s, BLUE, [(x + sz//2, y - sz), (x + sz//2 - 6, y - sz - 9), (x + sz//2 - 10, y - sz)])
        pygame.draw.line(s, BLUE, (x + sz//2, y - 6), (x + sz//2 + 9, y - 14), 3)
        pygame.draw.rect(s, BLACK, (x - 6, y - sz + 7, 3, 3)); pygame.draw.rect(s, BLACK, (x + 3, y - sz + 7, 3, 3))
    elif who == 'RYEN':  # time traveller
        pygame.draw.rect(s, PURPLE, (x - sz//2, y - sz, sz, sz), border_radius=3)
        pygame.draw.rect(s, (255,255,180), (x - sz//2 + 2, y - sz + 4, sz - 4, 6))  # goggles
        pygame.draw.line(s, (255,255,180), (x, y - 2), (x, y - sz//2), 2)           # clock hand
    elif who == 'LASSE': # fox
        pygame.draw.rect(s, ORANGE, (x - sz//2, y - sz, sz, sz), border_radius=5)
        pygame.draw.polygon(s, ORANGE, [(x - sz//2, y - sz), (x - sz//2 + 4, y - sz - 11), (x - sz//2 + 9, y - sz)])
        pygame.draw.polygon(s, ORANGE, [(x + sz//2, y - sz), (x + sz//2 - 4, y - sz - 11), (x + sz//2 - 9, y - sz)])
        pygame.draw.circle(s, WHITE, (x + sz//2 + 7, y - 8), 5)                      # fluffy tail tip
        pygame.draw.rect(s, BLACK, (x - 6, y - sz + 8, 3, 3)); pygame.draw.rect(s, BLACK, (x + 3, y - sz + 8, 3, 3))
    elif who == 'PLOMBO':
        pygame.draw.rect(s, (230, 60, 60), (x - 12, y - 24, 24, 12))
        pygame.draw.rect(s, (60, 60, 230), (x - 12, y - 12, 24, 12))
        pygame.draw.rect(s, (40, 30, 20), (x - 8, y - 15, 16, 4))  # mustache
    elif who == 'BECCA':
        pygame.draw.rect(s, (240, 200, 220), (x - 11, y - 26, 22, 26), border_radius=6)
    elif who == 'JOSEPH':
        pygame.draw.rect(s, (250, 210, 90), (x - 13, y - 28, 26, 28), border_radius=6)
        pygame.draw.circle(s, (180, 120, 30), (x, y - 30), 6)

SPEAKER_COL = {'AC': BLUE, 'RYEN': PURPLE, 'LASSE': ORANGE, 'PLOMBO': RED,
               'BECCA': (240,200,220), 'JOSEPH': (250,210,90),
               'WRENCHARD': GREEN, '': GRAY}

# ---------------------------------------------------------------- game data
def make_party():
    return [
        {'name': 'AC',    'hp': 90,  'mx': 90,  'atk': 10, 'col': BLUE,
         'spell': ('MEOW', 10, 'mercy')},
        {'name': 'RYEN',  'hp': 110, 'mx': 110, 'atk': 14, 'col': PURPLE,
         'spell': ('REWIND', 32, 'healall')},
        {'name': 'LASSE', 'hp': 75,  'mx': 75,  'atk': 7,  'col': ORANGE,
         'spell': ('FOXFIRE', 20, 'damage')},
    ]

ITEMS = {'ChocCone': 60, 'CatTea': 45, 'PipeSoda': 80, 'DustBun': 30}

MINIONS = [
 {'name':'DUSTLING','hp':60,'atk':4,'pat':'rain','col':GRAY,
  'quotes':['* Dustling drifts in a small circle.','* Smells like an old chalkboard.'],
  'acts':[('SWEEP',45,'* You sweep gently. Dustling feels organized.'),
          ('SNEEZE',30,'* You sneeze. Dustling relates deeply.')]},
 {'name':'SPARKFISH','hp':70,'atk':5,'pat':'aim','col':(120,220,255),
  'quotes':['* Sparkfish swims through pure signal.','* It hums at 60hz.'],
  'acts':[('UNPLUG',45,'* You mime unplugging it. Sparkfish calms down.'),
          ('SPLASH',30,'* You splash imaginary water. Refreshing!')]},
 {'name':'TAPE GHOST','hp':80,'atk':6,'pat':'wave','col':(220,220,255),
  'quotes':['* Tape Ghost rewinds itself nervously.','* Please be kind. Rewind.'],
  'acts':[('REWIND',45,'* You rewind it carefully. It sighs in stereo.'),
          ('LABEL',30,'* You write a nice label. It feels remembered.')]},
 {'name':'HYMNLING','hp':90,'atk':6,'pat':'notes','col':(255,240,170),
  'quotes':['* Hymnling holds a very long note.','* The echo has an echo.'],
  'acts':[('HARMONIZE',45,'* You hum a third above. Beautiful.'),
          ('CONDUCT',30,'* You wave your paws. It follows tempo.')]},
 {'name':'PIPELING','hp':100,'atk':7,'pat':'pipes','col':GREEN,
  'quotes':['* Pipeling gurgles menacingly.','* Water pressure rising.'],
  'acts':[('TIGHTEN',45,'* You tighten its valve. Much less drippy.'),
          ('KNOCK',30,'* You knock twice. It knocks back. Friends?')]},
]

BOSSES = [
 {'name':'CARD PREFECT','hp':260,'atk':5,'pat':'cards','col':(255,120,120),'song':'boss0',
  'quotes':['* The Prefect checks your hall pass.','* "RUNNING IN THE HALLS?!"','* Detention slips flutter.'],
  'acts':[('APOLOGIZE',35,'* You apologize for existing. Accepted, barely.'),
          ('HALLPASS',40,'* You present a hall pass drawn in crayon. ...It works?!'),
          ('MEOW',25,'* You meow. The Prefect softens 3%.')],
  'intro':[('','* A towering playing card in a school uniform blocks the exit!'),
           ('RYEN',"Great. Middle management."),('AC','...meow.')]},
 {'name':'CIRCUIT QUEEN','hp':300,'atk':6,'pat':'grid','col':(120,255,220),'song':'boss1',
  'quotes':['* The Queen boots up a grand speech.','* "PING me later, darlings."','* Royal firmware updating...'],
  'acts':[('REBOOT',35,'* You suggest turning her off and on. She is FLATTERED.'),
          ('CURTSY',40,'* You curtsy at 60fps. Impeccable frame timing.'),
          ('MEOW',25,'* Meow.exe executed successfully.')],
  'intro':[('','* The Circuit Queen descends on a throne of routers!'),
           ('RYEN',"I've seen the future. She monologues."),('AC','mrow.')]},
 {'name':'STATIC JESTER','hp':340,'atk':7,'pat':'spiral','col':(255,160,255),'song':'boss2',
  'quotes':['* The Jester laughs on channel 3.','* "STAY TUNED!!"','* Signal integrity: comedic.'],
  'acts':[('LAUGH',35,'* You laugh politely. It DEMANDS a real laugh.'),
          ('CHANGE CH.',40,'* You change the channel. It chases the remote.'),
          ('MEOW',25,'* The meow gets great ratings.')],
  'intro':[('','* A jester made of broadcast static tumbles out of the screen!'),
           ('LASSE',"O-oh no. I hate live television."),('RYEN',"Then let's cancel him.")]},
 {'name':'CHOIR WARDEN','hp':380,'atk':7,'pat':'notes2','col':(255,230,150),'song':'boss3',
  'quotes':['* The Warden demands PERFECT pitch.','* "FROM THE TOP."','* A thousand-year rehearsal continues.'],
  'acts':[('SING',35,'* You sing your heart out. Slightly flat. He weeps anyway.'),
          ('METRONOME',40,'* You become the metronome. Tick. Tock. Respect.'),
          ('MEOW',25,'* A meow in G major.')],
  'intro':[('','* The Choir Warden raises a baton the size of a lamppost!'),
           ('LASSE',"Everyone... sing like your HP depends on it."),('RYEN',"It literally does.")]},
 {'name':'WRENCHARD','hp':440,'atk':8,'pat':'knight','col':GREEN,'song':'final',
  'quotes':['* The Pipe Knight says nothing.','* Water drips from ancient valves.','* The fountain howls behind him.'],
  'acts':[('PLEAD',30,'* You plead for the surface world. His wrench trembles.'),
          ('REMEMBER',40,'* You remind him fountains were for WISHES once.'),
          ('MEOW',30,'* Even knights cannot resist the meow.')],
  'intro':[('','* WRENCHARD, THE PIPE KNIGHT, bars the final fountain.'),
           ('WRENCHARD','...'),('RYEN',"All this time. A PLUMBER?!"),
           ('LASSE',"Everyone... together!"),('AC','MEOW!!')]},
]

CH_INTRO = [
 [('BECCA',"AC, sweetie! You'll be late for class. Take Ryen with you."),
  ('RYEN',"I'm from the year 3026 and even I can't fix your bedhead."),
  ('',"* The supply closet floor gives way... into the STATIC WORLD."),
  ('RYEN',"Okay. New timeline. Rules: I punch, you meow."),
  ('AC',"...meow.")],
 [('',"* CH2. The dark water glows with neon signage."),
  ('RYEN',"A whole harbor made of wifi. My era invented this, you're welcome."),
  ('AC',"mrrp?"),
  ('RYEN',"No, you can't fish in it. ...Okay, ONE fish.")],
 [('',"* CH3. A boardwalk flickers between channels."),
  ('LASSE',"U-um! AC! Ryen! I fell through my TV and I— is that a battle box?!"),
  ('RYEN',"Welcome aboard, fox. You're the healer now. Congrats on the promotion."),
  ('LASSE',"I didn't apply for this...!")],
 [('',"* CH4. A choir hums beneath the floorboards of the world."),
  ('LASSE',"The music is... kind of beautiful?"),
  ('RYEN',"It's a boss theme, Lasse. It's ALWAYS a boss theme."),
  ('AC',"meow. (agreement)")],
 [('',"* CH5. Pipes. Endless pipes. All roads flow down."),
  ('JOSEPH',"Oh hey little buddies! I planted sunflowers in the drainage. Be safe down there!"),
  ('RYEN',"The final fountain is below. I've seen how this ends. ...Actually, no. I haven't."),
  ('LASSE',"Then we write it ourselves."),
  ('AC',"...meow. (resolve)")],
]

CH_OUTRO = [
 [('',"* The Static Fountain is sealed. The classroom rebuilds itself around you."),
  ('BECCA',"There you two are! Dinner's ready. ...Why are you covered in chalk?")],
 [('',"* The Neon Fountain dims to a gentle glow. The harbor sleeps."),
  ('RYEN',"Two down. My future self says hi, by the way. He's proud. Weird.")],
 [('',"* The VHS Fountain rewinds itself shut. Roll credits? Not yet."),
  ('LASSE',"I... I helped! I actually helped!")],
 [('',"* The Choir Fountain resolves on a perfect final chord."),
  ('RYEN',"One fountain left. The big one. Bring snacks.")],
 [('',"* The last fountain closes. Light pours through every pipe."),
  ('WRENCHARD',"...thank you."),
  ('JOSEPH',"GROUP HUG! I brought sunflowers!"),
  ('BECCA',"You're all grounded. Lovingly."),
  ('',"* AC RUNE 0.1 — THE END (for now) — [C] 2026 AC HOLDING"),
  ('',"* thank you for playing. meow.")],
]

PLOMBO_SCENE = [
 ('',"* A figure leans against the last doorway, spinning a pipe wrench."),
 ('PLOMBO',"heya. it's-a me. the guy before the guy."),
 ('PLOMBO',"five fountains. zero rage-quits. not bad, little cat."),
 ('PLOMBO',"my brother wrenchard is through that door. he's... complicated."),
 ('PLOMBO',"be rude to him and you'll have a bad tuesday. capisce?"),
 ('RYEN',"Is EVERYONE in this world a plumber?!"),
 ('PLOMBO',"union's strong down here, kid. go get 'em."),
]

# ---------------------------------------------------------------- the game
class Game:
    def __init__(self):
        pygame.mixer.pre_init(SR, -16, 1, 512)
        pygame.init()
        audio_ok = True
        try: pygame.mixer.init(SR, -16, 1, 512)
        except Exception: audio_ok = False
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("AC RUNE 0.1 — [C] 2026 AC HOLDING")
        self.clock = pygame.time.Clock()
        self.music = Music(audio_ok)
        self.sfx = {}
        if audio_ok:
            try:
                self.sfx = {'blip': tone(880,.045,'sq',.2), 'ok': tone(660,.08,'sq',.25,660),
                            'no': tone(220,.12,'saw',.25,-80), 'hurt': tone(180,.16,'saw',.3,-120),
                            'heal': tone(520,.14,'tri',.25,520), 'slash': tone(90,.1,'noise',.3),
                            'graze': tone(1200,.03,'tri',.12), 'win': tone(440,.3,'sq',.25,440)}
            except Exception: pass
        self.state = 'title'; self.frame = 0
        self.progress = 0                       # chapters cleared
        self.sel = 0
        self.party = make_party()
        self.inv = ['ChocCone', 'CatTea']
        self.tp = 0
        self.ch = 0
        self.dlg = []; self.dlg_i = 0; self.dlg_t = 0; self.dlg_next = 'title'
        self.toast = ""; self.toast_t = 0
        self.flash = 0
        # overworld
        self.px = 60.0; self.trail = []
        self.fought = False
        # battle
        self.b = None

    # ---------------- util
    def play_sfx(self, k):
        s = self.sfx.get(k)
        if s and not self.music.mute: s.play()
    def song(self, key):
        self.music.play(key)
        if self.music.ok:
            self.toast = "♪ now playing: " + SONGS[key][5]; self.toast_t = 150
    def say(self, lines, nxt):
        self.dlg = lines; self.dlg_i = 0; self.dlg_t = 0
        self.dlg_next = nxt; self.state = 'dialog'

    def active_party(self):
        n = 3 if self.ch >= 2 else 2
        return self.party[:n]

    # ---------------- chapter flow
    def begin_chapter(self, ch):
        self.ch = ch
        self.px = 60.0; self.trail = []; self.fought = False
        for m in self.party: m['hp'] = m['mx']
        self.tp = 20
        for it in ('ChocCone', 'CatTea', 'PipeSoda'):
            if len(self.inv) < 6: self.inv.append(it)
        self.say(CH_INTRO[ch], 'over')
        self.song('world%d' % ch)

    def end_chapter(self):
        self.progress = max(self.progress, self.ch + 1)
        if self.ch == 4:
            self.say(CH_OUTRO[4], 'credits'); self.song('end')
        else:
            self.say(CH_OUTRO[self.ch], 'select'); self.song('title')

    # ---------------- battle setup
    def start_battle(self, boss):
        e = dict(BOSSES[self.ch] if boss else MINIONS[self.ch])
        e['mx'] = e['hp']; e['mercy'] = 0; e['boss'] = boss
        self.b = {'e': e, 'phase': 'intro' if boss else 'menu', 'mi': 0, 'sel': 0,
                  'msg': '', 'turn': 0, 'bullets': [], 't': 0, 'soul': [BOX.centerx, BOX.centery],
                  'inv_sel': 0, 'bar': 0.0, 'bardir': 1, 'dmg_pop': [], 'iframes': 0,
                  'quote': random.choice(e['quotes'])}
        self.state = 'battle'
        self.song(e['song'] if boss else 'battle')
        if boss: self.say(e['intro'], 'battle')

    # ---------------- battle logic
    def next_member(self):
        b = self.b; ap = self.active_party()
        b['mi'] += 1
        while b['mi'] < len(ap) and ap[b['mi']]['hp'] <= 0: b['mi'] += 1
        if b['mi'] >= len(ap):
            b['phase'] = 'dodge'; b['t'] = 0; b['bullets'] = []
            b['soul'] = [BOX.centerx, BOX.centery]
            b['quote'] = random.choice(b['e']['quotes'])
        else:
            b['phase'] = 'menu'; b['sel'] = 0

    def apply_damage(self, dmg):
        b = self.b; e = b['e']
        e['hp'] -= dmg; self.play_sfx('slash'); self.flash = 6
        b['dmg_pop'].append([320, 150, str(dmg), 40, RED])
        if e['hp'] <= 0:
            e['hp'] = 0; b['phase'] = 'win'
            b['msg'] = "* You won! %s was defeated." % e['name']
            self.play_sfx('win')

    def try_spare(self):
        b = self.b; e = b['e']
        if e['mercy'] >= 100:
            b['phase'] = 'win'; b['msg'] = "* You won! %s was SPARED." % e['name']
            self.play_sfx('win')
        else:
            b['msg'] = "* %s isn't ready to be spared. (mercy %d%%)" % (e['name'], e['mercy'])
            b['phase'] = 'text'

    def cast(self, m):
        b = self.b; name, cost, kind = m['spell']
        if self.tp < cost:
            b['msg'] = "* Not enough TP! (%d needed)" % cost; b['phase'] = 'text'; return
        self.tp -= cost
        if kind == 'mercy':
            b['e']['mercy'] = min(100, b['e']['mercy'] + 20)
            b['msg'] = "* AC meows with maximum sincerity. Mercy +20%!"
            self.play_sfx('heal')
        elif kind == 'healall':
            for p in self.active_party(): p['hp'] = min(p['mx'], p['hp'] + 45)
            b['msg'] = "* RYEN rewinds everyone's bruises. Party healed 45!"
            self.play_sfx('heal')
        else:
            b['msg'] = "* LASSE unleashes FOXFIRE!"
            self.apply_damage(random.randint(46, 58))
        if b['phase'] != 'win': b['phase'] = 'text'

    def spawn_bullets(self):
        b = self.b; t = b['t']; e = b['e']; ch = self.ch
        sp = 1.6 + ch * 0.28
        pat = e['pat']
        def add(x, y, vx, vy, r=5, col=None, w=0, h=0):
            b['bullets'].append({'x':x,'y':y,'vx':vx,'vy':vy,'r':r,'c':col or e['col'],'w':w,'h':h,'g':False})
        if pat == 'rain':
            if t % 13 == 0: add(random.randint(BOX.left+8, BOX.right-8), BOX.top-8, 0, sp)
        elif pat == 'aim':
            if t % 34 == 0:
                sx, sy = random.choice([(BOX.left-6,BOX.top-6),(BOX.right+6,BOX.top-6)])
                dx, dy = b['soul'][0]-sx, b['soul'][1]-sy; d = math.hypot(dx,dy) or 1
                add(sx, sy, dx/d*sp*1.4, dy/d*sp*1.4, 6)
        elif pat == 'wave':
            if t % 11 == 0:
                add(BOX.right+8, BOX.centery + math.sin(t*0.08)*60, -sp*1.3, 0, 5)
        elif pat == 'notes':
            if t % 16 == 0:
                y0 = random.randint(BOX.top+10, BOX.bottom-10)
                add(BOX.right+8, y0, -sp, math.sin(t)*0.6, 6, (255,240,170))
        elif pat == 'pipes':
            if t % 55 == 0:
                gap = random.randint(BOX.top+30, BOX.bottom-50)
                add(BOX.right+12, BOX.top, -sp, 0, 0, GREEN, 14, gap-BOX.top)
                add(BOX.right+12, gap+44, -sp, 0, 0, GREEN, 14, BOX.bottom-(gap+44))
        elif pat == 'cards':
            if t % 20 == 0:
                y0 = BOX.top + 14 + ((t//20) % 5) * 28
                side = -1 if (t//20) % 2 else 1
                add(BOX.centerx + side*170, y0, -side*sp*1.2, 0, 0, (255,120,120), 18, 10)
        elif pat == 'grid':
            if t % 26 == 0:
                add(random.randint(BOX.left+8,BOX.right-8), BOX.top-8, 0, sp, 5, (120,255,220))
                add(BOX.left-8, random.randint(BOX.top+8,BOX.bottom-8), sp, 0, 5, (120,255,220))
        elif pat == 'spiral':
            if t % 7 == 0:
                a = t * 0.19
                add(BOX.centerx, BOX.top+10, math.cos(a)*sp, abs(math.sin(a))*sp+0.6, 5, (255,160,255))
        elif pat == 'notes2':
            if t % 12 == 0:
                add(BOX.right+8, BOX.top+15+((t//12)%6)*24, -sp*1.15, math.sin(t*0.5)*0.4, 6, (255,230,150))
            if t % 50 == 0: add(random.randint(BOX.left+8,BOX.right-8), BOX.top-8, 0, sp*0.9)
        elif pat == 'knight':
            ph = (b['turn']) % 3
            if ph == 0 and t % 45 == 0:
                gap = random.randint(BOX.top+30, BOX.bottom-56)
                add(BOX.right+12, BOX.top, -sp*1.1, 0, 0, GREEN, 14, gap-BOX.top)
                add(BOX.right+12, gap+50, -sp*1.1, 0, 0, GREEN, 14, BOX.bottom-(gap+50))
            elif ph == 1 and t % 6 == 0:
                a = t * 0.23
                add(BOX.centerx, BOX.top+10, math.cos(a)*sp*1.1, abs(math.sin(a))*sp+0.7, 5, GREEN)
            elif ph == 2 and t % 26 == 0:
                sx = random.choice([BOX.left-6, BOX.right+6])
                dx, dy = b['soul'][0]-sx, b['soul'][1]-BOX.top; d = math.hypot(dx,dy) or 1
                add(sx, BOX.top-6, dx/d*sp*1.5, dy/d*sp*1.5, 6, GREEN)

    def update_dodge(self, keys):
        b = self.b; s = b['soul']; spd = 2.6
        if keys[pygame.K_LEFT]:  s[0] -= spd
        if keys[pygame.K_RIGHT]: s[0] += spd
        if keys[pygame.K_UP]:    s[1] -= spd
        if keys[pygame.K_DOWN]:  s[1] += spd
        s[0] = max(BOX.left+7, min(BOX.right-7, s[0]))
        s[1] = max(BOX.top+7, min(BOX.bottom-7, s[1]))
        self.spawn_bullets()
        if b['iframes'] > 0: b['iframes'] -= 1
        alive = [p for p in self.active_party() if p['hp'] > 0]
        for bl in b['bullets'][:]:
            bl['x'] += bl['vx']; bl['y'] += bl['vy']
            if bl['x'] < BOX.left-40 or bl['x'] > BOX.right+40 or bl['y'] > BOX.bottom+40 or bl['y'] < BOX.top-60:
                b['bullets'].remove(bl); continue
            if bl['w']:  # rect bullet
                r = pygame.Rect(bl['x'], bl['y'], bl['w'], bl['h'])
                hit = r.collidepoint(s[0], s[1])
                near = r.inflate(22, 22).collidepoint(s[0], s[1])
            else:
                d = math.hypot(bl['x']-s[0], bl['y']-s[1])
                hit = d < bl['r'] + 6; near = d < bl['r'] + 20
            if near and not bl['g'] and not hit:
                bl['g'] = True; self.tp = min(100, self.tp + 2); self.play_sfx('graze')
            if hit and b['iframes'] == 0:
                b['iframes'] = 45; self.play_sfx('hurt'); self.flash = 5
                victim = random.choice(alive) if alive else None
                if victim:
                    victim['hp'] = max(0, victim['hp'] - (b['e']['atk'] + self.ch))
                    b['dmg_pop'].append([120 + 130*self.party.index(victim), 430,
                                         "-%d" % (b['e']['atk']+self.ch), 35, RED])
                alive = [p for p in self.active_party() if p['hp'] > 0]
                if not alive:
                    self.state = 'gameover'; return
        b['t'] += 1
        dur = 290 + self.ch * 35 + (60 if b['e']['boss'] else 0)
        if b['t'] > dur:
            b['e']['mercy'] = min(100, b['e']['mercy'] + (6 if b['e']['boss'] else 10))
            b['turn'] += 1; b['mi'] = -1; self.next_member()
            b['mi'] = 0
            while self.active_party()[b['mi']]['hp'] <= 0: b['mi'] += 1
            b['phase'] = 'menu'; b['sel'] = 0

    # ---------------- events
    def handle_key(self, k):
        st = self.state
        if k == pygame.K_m: self.music.toggle(); return
        if st == 'title':
            if k in (pygame.K_z, pygame.K_RETURN): self.play_sfx('ok'); self.state = 'select'
        elif st == 'select':
            if k == pygame.K_UP:   self.sel = (self.sel - 1) % 5; self.play_sfx('blip')
            if k == pygame.K_DOWN: self.sel = (self.sel + 1) % 5; self.play_sfx('blip')
            if k in (pygame.K_z, pygame.K_RETURN):
                if self.sel <= self.progress: self.play_sfx('ok'); self.begin_chapter(self.sel)
                else: self.play_sfx('no')
            if k == pygame.K_x: self.state = 'title'
        elif st == 'dialog':
            if k in (pygame.K_z, pygame.K_RETURN):
                sp, tx_ = self.dlg[self.dlg_i]
                if self.dlg_t < len(tx_): self.dlg_t = len(tx_)
                else:
                    self.dlg_i += 1; self.dlg_t = 0; self.play_sfx('blip')
                    if self.dlg_i >= len(self.dlg):
                        self.state = self.dlg_next
                        if self.dlg_next == 'battle' and self.b: self.b['phase'] = 'menu'
        elif st == 'battle':
            self.battle_key(k)
        elif st == 'gameover':
            if k in (pygame.K_z, pygame.K_RETURN):
                for m in self.party: m['hp'] = m['mx'] // 2 + 10
                boss = self.b['e']['boss']
                self.say([('RYEN', "Nope. Rewinding THAT one. Nobody dies on my watch.")], 'battle')
                self.start_battle(boss)
        elif st == 'credits':
            if k in (pygame.K_z, pygame.K_RETURN): self.state = 'select'; self.song('title')

    def battle_key(self, k):
        b = self.b; ap = self.active_party(); m = ap[b['mi']] if b['mi'] < len(ap) else ap[0]
        ph = b['phase']
        if ph == 'menu':
            opts = 5
            if k == pygame.K_LEFT:  b['sel'] = (b['sel'] - 1) % opts; self.play_sfx('blip')
            if k == pygame.K_RIGHT: b['sel'] = (b['sel'] + 1) % opts; self.play_sfx('blip')
            if k in (pygame.K_z, pygame.K_RETURN):
                self.play_sfx('ok')
                c = ['FIGHT','ACT','MAGIC','ITEM','SPARE'][b['sel']]
                if c == 'FIGHT': b['phase'] = 'fight'; b['bar'] = 0.0; b['bardir'] = 1
                elif c == 'ACT': b['phase'] = 'act'; b['sel2'] = 0
                elif c == 'MAGIC': self.cast(m)
                elif c == 'ITEM':
                    if self.inv: b['phase'] = 'item'; b['sel2'] = 0
                    else: b['msg'] = "* Your pockets contain one (1) crumb."; b['phase'] = 'text'
                elif c == 'SPARE': self.try_spare()
        elif ph == 'act':
            acts = b['e']['acts']
            if k == pygame.K_UP:   b['sel2'] = (b['sel2'] - 1) % len(acts); self.play_sfx('blip')
            if k == pygame.K_DOWN: b['sel2'] = (b['sel2'] + 1) % len(acts); self.play_sfx('blip')
            if k == pygame.K_x: b['phase'] = 'menu'
            if k in (pygame.K_z, pygame.K_RETURN):
                nm, mc, txt_ = acts[b['sel2']]
                b['e']['mercy'] = min(100, b['e']['mercy'] + mc)
                b['msg'] = txt_ + "  (mercy +%d%%)" % mc
                b['phase'] = 'text'; self.play_sfx('heal')
        elif ph == 'item':
            if k == pygame.K_UP:   b['sel2'] = (b['sel2'] - 1) % len(self.inv); self.play_sfx('blip')
            if k == pygame.K_DOWN: b['sel2'] = (b['sel2'] + 1) % len(self.inv); self.play_sfx('blip')
            if k == pygame.K_x: b['phase'] = 'menu'
            if k in (pygame.K_z, pygame.K_RETURN):
                it = self.inv.pop(b['sel2'])
                heal = ITEMS[it]
                m['hp'] = min(m['mx'], m['hp'] + heal)
                b['msg'] = "* %s ate the %s. Recovered %d HP!" % (m['name'], it, heal)
                b['phase'] = 'text'; self.play_sfx('heal')
        elif ph == 'fight':
            if k in (pygame.K_z, pygame.K_RETURN):
                acc = 1.25 - 2.2 * abs(b['bar'] - 0.5)
                dmg = max(3, int(m['atk'] * max(0.15, acc) * random.uniform(0.9, 1.15) * 2.2))
                self.apply_damage(dmg)
                if b['phase'] != 'win': b['phase'] = 'text'; b['msg'] = "* %s attacks! %d damage!" % (m['name'], dmg)
        elif ph == 'text':
            if k in (pygame.K_z, pygame.K_RETURN): self.next_member()
        elif ph == 'win':
            if k in (pygame.K_z, pygame.K_RETURN):
                boss = b['e']['boss']; self.b = None
                self.tp = min(100, self.tp + 15)
                if boss:
                    self.say([('', "* You reach the DARK FOUNTAIN."),
                              ('AC', "meow. (sealing sounds)"),
                              ('', "* The fountain closes gently.")], 'chend')
                else:
                    self.state = 'over'; self.song('world%d' % self.ch)

    # ---------------- update / draw
    def update(self):
        self.frame += 1
        if self.toast_t > 0: self.toast_t -= 1
        if self.flash > 0: self.flash -= 1
        keys = pygame.key.get_pressed()
        if self.state == 'over':
            spd = 3.2
            moved = False
            if keys[pygame.K_RIGHT]: self.px += spd; moved = True
            if keys[pygame.K_LEFT]:  self.px = max(40, self.px - spd); moved = True
            room = 1500 + self.ch * 200
            self.trail.append(self.px)
            if len(self.trail) > 40: self.trail.pop(0)
            if not self.fought and self.px > room * 0.45:
                self.fought = True
                self.say([('', "* %s draws near!" % MINIONS[self.ch]['name'])], 'over')
                self.start_battle(False)
            if self.px > room - 80:
                self.start_battle(True)
        elif self.state == 'battle':
            b = self.b
            if b['phase'] == 'fight':
                b['bar'] += 0.022 * b['bardir']
                if b['bar'] >= 1: b['bar'], b['bardir'] = 1, -1
                if b['bar'] <= 0: b['bar'], b['bardir'] = 0, 1
            elif b['phase'] == 'dodge':
                self.update_dodge(keys)
            for p in b['dmg_pop'][:] if b else []:
                p[1] -= 0.7; p[3] -= 1
                if p[3] <= 0: b['dmg_pop'].remove(p)
        elif self.state == 'dialog':
            sp, tx_ = self.dlg[self.dlg_i]
            if self.dlg_t < len(tx_):
                self.dlg_t += 1
                if self.dlg_t % 3 == 0: self.play_sfx('blip')
        elif self.state == 'chend':
            pass

    def draw_dialog_box(self):
        s = self.screen
        r = pygame.Rect(30, 350, W - 60, 110)
        pygame.draw.rect(s, BLACK, r); pygame.draw.rect(s, WHITE, r, 3)
        sp, tx_ = self.dlg[self.dlg_i]
        shown = tx_[:self.dlg_t]
        if sp:
            txt(s, sp, r.x + 14, r.y + 8, 18, SPEAKER_COL.get(sp, WHITE))
            draw_actor(s, r.x + 40, r.y + 95, sp, self.frame)
            x0 = r.x + 80
        else:
            x0 = r.x + 16
        # word wrap
        words = shown.split(' '); line = ''; y = r.y + (32 if sp else 16)
        for wd in words:
            if len(line + wd) > (52 if not sp else 44):
                txt(s, line, x0, y, 17); y += 22; line = ''
            line += wd + ' '
        txt(s, line, x0, y, 17)
        txt(s, "[Z]", r.right - 40, r.bottom - 24, 14, GRAY)

    def draw(self):
        s = self.screen; st = self.state
        bg, ac = CH_PAL[self.ch]
        s.fill(BLACK if st in ('title', 'select', 'gameover', 'credits') else bg)

        if st == 'title':
            for i in range(24):  # static specks
                s.set_at((random.randrange(W), random.randrange(H)), (30, 30, 45))
            txt(s, "A C   R U N E", W//2, 130, 54, BLUE, True)
            txt(s, "0.1  —  2026  —  [C] AC HOLDING", W//2, 185, 18, WHITE, True)
            txt(s, "a Team Flames / Samsoft original AU", W//2, 212, 15, GRAY, True)
            if (self.frame // 30) % 2: txt(s, "[ PRESS Z ]", W//2, 300, 22, YELLOW, True)
            draw_actor(s, W//2 - 60, 380, 'AC', self.frame, 1.6)
            draw_actor(s, W//2, 380, 'RYEN', self.frame + 10, 1.6)
            draw_actor(s, W//2 + 60, 380, 'LASSE', self.frame + 20, 1.6)
            txt(s, "Z confirm   X cancel   M mute", W//2, 440, 14, GRAY, True)
        elif st == 'select':
            txt(s, "SELECT CHAPTER", W//2, 60, 30, BLUE, True)
            for i, t in enumerate(CH_TITLES):
                locked = i > self.progress
                col = GRAY if locked else (YELLOW if i == self.sel else WHITE)
                pre = "> " if i == self.sel else "  "
                suf = "  [LOCKED]" if locked else ("  * CLEAR *" if i < self.progress else "")
                txt(s, pre + t + suf, 120, 130 + i * 46, 21, col)
            txt(s, "meow through them in order. nya.", W//2, 420, 15, GRAY, True)
        elif st in ('over', 'dialog', 'chend') and self.b is None:
            room = 1500 + self.ch * 200
            cam = max(0, min(self.px - W//2, room - W))
            # parallax stripes
            for i in range(10):
                y = 60 + i * 20
                pygame.draw.line(s, ac, (0, y + int(math.sin(self.frame*0.02 + i)*4)), (W, y), 1)
            pygame.draw.rect(s, ac, (0, 330, W, 6))
            pygame.draw.rect(s, (bg[0]+8, bg[1]+8, bg[2]+8), (0, 336, W, H-336))
            # signposts + door
            for sx, label in ((300, CH_TITLES[self.ch]), (room//2 - 120, "battle zone ahead. stretch first."),):
                x = sx - cam
                if -50 < x < W + 50:
                    pygame.draw.rect(s, GRAY, (x, 290, 6, 40))
                    pygame.draw.rect(s, GRAY, (x - 40, 272, 86, 22))
                    txt(s, label[:20], x + 3, 276, 12, BLACK, True)
            dx = room - 60 - cam
            pygame.draw.rect(s, ac, (dx, 250, 44, 80)); pygame.draw.rect(s, YELLOW, (dx, 250, 44, 80), 2)
            txt(s, "BOSS", dx + 22, 240, 14, YELLOW, True)
            # party
            ap = self.active_party()
            draw_actor(s, self.px - cam, 330, 'AC', self.frame)
            if len(self.trail) > 12 and len(ap) > 1:
                draw_actor(s, self.trail[-12] - cam, 330, 'RYEN', self.frame + 8)
            if len(self.trail) > 24 and len(ap) > 2:
                draw_actor(s, self.trail[-24] - cam, 330, 'LASSE', self.frame + 16)
            txt(s, CH_TITLES[self.ch], 12, 10, 16, BLUE)
            txt(s, "→ walk right", W - 110, 10, 14, GRAY)
            if st == 'chend':
                pygame.draw.circle(s, WHITE, (W//2, 200), 30 + (self.frame % 60))
                self.end_chapter()
        elif st == 'battle' or (st in ('dialog',) and self.b):
            b = self.b; e = b['e']
            # enemy
            ex, ey = 320, 120 + int(math.sin(self.frame * 0.06) * 6)
            pygame.draw.rect(s, e['col'], (ex - 34, ey - 34, 68, 68), border_radius=10)
            pygame.draw.rect(s, WHITE, (ex - 34, ey - 34, 68, 68), 2, border_radius=10)
            if e['name'] == 'WRENCHARD':
                pygame.draw.rect(s, (200,200,200), (ex - 6, ey - 60, 12, 30))  # wrench
            txt(s, e['name'], ex, ey - 55, 20, YELLOW if e['mercy'] >= 100 else WHITE, True)
            # hp+mercy
            pygame.draw.rect(s, (60,0,0), (ex - 60, ey + 44, 120, 8))
            pygame.draw.rect(s, RED, (ex - 60, ey + 44, int(120 * e['hp'] / e['mx']), 8))
            txt(s, "mercy %d%%" % e['mercy'], ex, ey + 62, 14, YELLOW, True)
            # box
            pygame.draw.rect(s, BLACK, BOX); pygame.draw.rect(s, WHITE, BOX, 3)
            ph = b['phase']
            if ph == 'dodge':
                for bl in b['bullets']:
                    if bl['w']: pygame.draw.rect(s, bl['c'], (bl['x'], bl['y'], bl['w'], bl['h']))
                    else: pygame.draw.circle(s, bl['c'], (int(bl['x']), int(bl['y'])), bl['r'])
                if b['iframes'] % 8 < 5:
                    x0, y0 = int(b['soul'][0]), int(b['soul'][1])
                    pygame.draw.polygon(s, RED, [(x0, y0+7), (x0-7, y0-2), (x0-3, y0-7),
                                                 (x0, y0-3), (x0+3, y0-7), (x0+7, y0-2)])
                txt(s, b['quote'], W//2, 218, 15, GRAY, True)
            elif ph == 'fight':
                bar = pygame.Rect(BOX.x + 20, BOX.centery - 14, BOX.w - 40, 28)
                pygame.draw.rect(s, (40,40,40), bar); pygame.draw.rect(s, WHITE, bar, 2)
                pygame.draw.rect(s, GREEN, (bar.centerx - 7, bar.y, 14, bar.h), 2)
                cx = bar.x + int(b['bar'] * bar.w)
                pygame.draw.rect(s, YELLOW, (cx - 2, bar.y - 4, 4, bar.h + 8))
                txt(s, "press Z in the center!", W//2, 218, 15, GRAY, True)
            elif ph in ('text', 'win', 'intro'):
                words = b['msg'].split(' '); line = ''; y = BOX.y + 18
                for wd in words:
                    if len(line + wd) > 36: txt(s, line, BOX.x + 14, y, 16); y += 22; line = ''
                    line += wd + ' '
                txt(s, line, BOX.x + 14, y, 16)
                txt(s, "[Z]", BOX.right - 36, BOX.bottom - 24, 14, GRAY)
            elif ph == 'menu':
                txt(s, b['quote'], BOX.x + 14, BOX.y + 12, 15, GRAY)
                ap = self.active_party()
                txt(s, "%s's move" % ap[b['mi']]['name'], BOX.x + 14, BOX.y + 40, 17, ap[b['mi']]['col'])
                for i, o in enumerate(['FIGHT','ACT','MAGIC','ITEM','SPARE']):
                    col = YELLOW if i == b['sel'] else WHITE
                    if o == 'SPARE' and e['mercy'] >= 100: col = YELLOW if i == b['sel'] else GREEN
                    txt(s, o, BOX.x + 20 + i * 56, BOX.bottom - 34, 15, col)
            elif ph in ('act', 'item'):
                lst = [a[0] for a in e['acts']] if ph == 'act' else self.inv
                for i, o in enumerate(lst):
                    txt(s, ("> " if i == b['sel2'] else "  ") + o, BOX.x + 24, BOX.y + 16 + i * 24,
                        16, YELLOW if i == b['sel2'] else WHITE)
                txt(s, "[X back]", BOX.right - 70, BOX.bottom - 24, 13, GRAY)
            # party hud
            ap = self.active_party()
            for i, p in enumerate(ap):
                x0 = 90 + i * 170
                col = p['col'] if p['hp'] > 0 else GRAY
                txt(s, p['name'], x0, 412, 15, col)
                pygame.draw.rect(s, (60,0,0), (x0, 432, 100, 10))
                pygame.draw.rect(s, GREEN if p['hp'] > p['mx']//4 else RED,
                                 (x0, 432, int(100 * p['hp'] / p['mx']), 10))
                txt(s, "%d/%d" % (p['hp'], p['mx']), x0 + 104, 428, 13)
            pygame.draw.rect(s, (40,20,0), (16, 240, 14, 160))
            pygame.draw.rect(s, ORANGE, (16, 400 - int(160 * self.tp / 100), 14, int(160 * self.tp / 100)))
            txt(s, "TP", 23, 408, 13, ORANGE, True)
            for p in b['dmg_pop']:
                txt(s, p[2], int(p[0]), int(p[1]), 20, p[4], True)
        elif st == 'gameover':
            txt(s, "SOUL SHATTERED", W//2, 180, 40, RED, True)
            txt(s, "...but somewhere, a clock ticks backwards.", W//2, 240, 17, GRAY, True)
            txt(s, "[Z] let Ryen rewind", W//2, 300, 18, YELLOW, True)
        elif st == 'credits':
            txt(s, "AC RUNE 0.1", W//2, 70, 36, BLUE, True)
            lines = ["directed by catsan  //  Team Flames", "engine: one (1) python file. files = off.",
                     "", "AC ... a cat", "RYEN ... a time traveller", "LASSE ... a fox",
                     "PLOMBO & WRENCHARD ... union plumbers", "BECCA ... mom energy", "JOSEPH ... sunflower guy",
                     "", "OST: 14 original chiptune tracks", "rendered live at %d hz" % SR,
                     "", "[C] 2026 AC HOLDING   —   meow."]
            for i, l in enumerate(lines):
                txt(s, l, W//2, 130 + i * 22, 16, WHITE if l else GRAY, True)
            txt(s, "[Z] back to chapter select", W//2, 452, 14, YELLOW, True)

        if st == 'dialog': self.draw_dialog_box()
        if self.toast_t > 0:
            txt(s, self.toast, W - 8, H - 20, 14, BLUE)
            r = txt(s, self.toast, 0, -100, 14)  # measure offscreen
            txt(s, self.toast, W - r.w - 10, H - 22, 14, BLUE)
        if self.flash: pygame.draw.rect(s, WHITE, (0, 0, W, H), 6)
        pygame.display.flip()

    # ---------------- main loop
    def run(self):
        self.song('title')
        smoke_t = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); return
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: pygame.quit(); return
                    self.handle_key(ev.key)
            self.update()
            self.draw()
            self.clock.tick(FPS)
            if SMOKE:
                smoke_t += 1
                if smoke_t == 20: self.state = 'select'
                if smoke_t == 40: self.begin_chapter(0); self.state = 'over'
                if smoke_t == 60: self.start_battle(False); self.b['phase'] = 'menu'
                if smoke_t == 80: self.b['phase'] = 'dodge'; self.b['t'] = 0
                if smoke_t == 200: self.b['phase'] = 'fight'
                if smoke_t == 220: self.battle_key(pygame.K_z)
                if smoke_t == 240 and self.b: self.next_member()
                if smoke_t == 400:
                    print("SMOKE OK — states exercised, no crash. meow.")
                    pygame.quit(); return

if __name__ == '__main__':
    Game().run()
