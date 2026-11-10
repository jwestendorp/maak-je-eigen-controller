"""Genereer de blokken van het overzicht in README.md.

Gebruik: python3 scripts/overzicht.py . > /tmp/blokken.html
De SVG's komen in img/overzicht/; plak de geprinte HTML in README.md onder "Overzicht per niveau".
"""
import re, os, sys
from xml.sax.saxutils import escape

ROOT = sys.argv[1]
OUT = f'{ROOT}/img/overzicht'
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(f'{OUT}/{f}')

COL, H, M = 260, 52, 3          # column width, block height, margin inside each svg
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
STYLE = {  # fill, stroke, stroke-width, dashed
    'normal':     ('#f4f8fb', '#4a7ba6', 1.5, False),
    'opt':        ('#f4f8fb', '#4a7ba6', 1.5, True),
    'keuze':      ('#f4f8fb', '#c9a400', 4, False),
    'todo':       ('#ffd6d6', '#d33', 1.5, False),
    'todoOpt':    ('#ffd6d6', '#d33', 1.5, True),
    'deels':      ('#ffe9c7', '#e08a00', 1.5, False),
    'deelsKeuze': ('#ffe9c7', '#c9a400', 4, False),
}

def slug(h):
    return re.sub(r'[^\w\- ]', '', h.strip().lower()).replace(' ', '-')

def anchors(step):
    s = open(f'{ROOT}/stappen/{step}/README.md').read()
    return {slug(m) for m in re.findall(r'^#+ (.+)$', s, re.M)}

def wrap(text, width):
    per_line = int((width - 2 * M - 16) / 7.0)
    lines, cur = [], ''
    for w in text.split(' '):
        if cur and len(cur) + 1 + len(w) > per_line:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    lines.append(cur)
    assert len(lines) <= 2, text
    return lines

def svg(name, label, width, style, pill=False):
    fill, stroke, sw, dashed = STYLE[style]
    lines = wrap(label, width)
    dash = ' stroke-dasharray="6 4"' if dashed else ''
    rx = 16 if pill else 3
    i = sw / 2
    tspans = ''.join(
        f'<tspan x="{width / 2}" dy="{0 if n == 0 else 18}">{escape(l)}</tspan>'
        for n, l in enumerate(lines))
    y = H / 2 + 5 - (9 if len(lines) == 2 else 0)
    body = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{H}" viewBox="0 0 {width} {H}">'
            f'<rect x="{M + i}" y="{M + i}" width="{width - 2 * M - sw}" height="{H - 2 * M - sw}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'
            f'<text y="{y}" font-family="{FONT}" font-size="14" fill="#1f2328" text-anchor="middle">{tspans}</text></svg>\n')
    open(f'{OUT}/{name}.svg', 'w').write(body)
    return f'./img/overzicht/{name}.svg'

SPACER = 'space'
def spacer(width):
    name = f'space-{width}'
    open(f'{OUT}/{name}.svg', 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{H}"/>\n')
    return f'<img src="./img/overzicht/{name}.svg" width="{width}" height="{H}" alt="">'

def b(name, label, step, anchor=None, style='normal', span=1.0):
    if anchor:
        assert anchor in anchors(step), (step, anchor)
    width = int(COL * span)
    src = svg(name, label, width, style)
    href = f'./stappen/{step}/README.md' + (f'#{anchor}' if anchor else '')
    return f'<a href="{href}"><img src="{src}" width="{width}" height="{H}" alt="{escape(label)}"></a>'

def s(span=1): return spacer(COL * span)

def header(name, label):
    src = svg(name, label, COL, 'normal', pill=True)
    return f'<img src="{src}" width="{COL}" height="{H}" alt="{escape(label)}">'

rows = [
 [header('h-simpel', 'Simpel · <14'), header('h-gemiddeld', 'Gemiddeld · 14-18'), header('h-gevorderd', 'Gevorderd · >16')],
 [b('01s', '🚧 01 Wat is een stroomkring?', '01-stroomkring', style='todo'),
  b('01g', '🚧 01 Wat is een stroomkring?', '01-stroomkring', style='todoOpt'), s()],
 [b('02s', '02 Analoog vs. digitaal', '02-analoog-digitaal', 'microbit', 'opt'),
  b('02', '02 Analoog vs. digitaal signaal', '02-analoog-digitaal', span=2)],
 [b('03', '03 Je eerste code (Micro:bit)', '03-eerste-code', span=2),
  b('03x', '03 Zelfstudie Micro:bit', '03-eerste-code', style='opt')],
 [b('04s', '⚠️ 04 Micro:bit + HID-extensie', '04-bord-opzetten', 'microbit-als-hid', 'deelsKeuze'),
  b('04g', '04 RP2040-Zero + CircuitPython', '04-bord-opzetten', 'rp2040-zero-met-circuitpython', 'keuze'),
  b('04a-promicro', '⚠️ 04 Pro Micro', '04-bord-opzetten', 'wired-pro-micro-with-hid-project', 'deelsKeuze', 0.5),
  b('04a-esp32', '🚧 04 ESP32', '04-bord-opzetten', 'wireless-esp32-with-bluetooth-ble', 'todo', 0.5)],
 [b('05', '05 Breadboard: prototype drukknop (digitaal)', '05-drukknop', span=3)],
 [b('06s', '06 Potmeter (analoog)', '06-potmeter', 'potentiometer-op-de-microbit', 'opt'),
  b('06', '06 Breadboard: prototype potmeter (analoog)', '06-potmeter', span=2)],
 [s(2), b('07', '07 Bedenk je eigen input signaal', '07-eigen-input')],
 [b('08', '08 Schets je controller en pitch je idee', '08-schetsen-pitch', span=3)],
 [b('09', '09 Circuit simuleren in Tinkercad', '09-circuit-simuleren'), s(2)],
 [b('10', '10 Breadboard: maak een prototype voor je circuit', '10-prototype-circuit', span=3)],
 [b('11s', '11 Code: Keyboard-template', '11-code', 'microbit-makecode'),
  b('11g', '11 Code: Keyboard, Gamepad', '11-code', 'rp2040-zero-circuitpython'),
  b('11a', '⚠️ 11 Code: Keyboard, Gamepad, Mouse, MIDI', '11-code', 'pro-micro-hid-project', 'deels')],
 [b('12', '12 Testen en debuggen', '12-testen-debuggen', span=3)],
 [b('13s', '13 Tinkercad: soldeerloos ontwerp pimpen', '13-tinkercad', 'een-bestaand-ontwerp-pimpen-soldeerloos', 'opt'),
  b('13g', '🚧 13 Tinkercad: ontwerp voor solderen', '13-tinkercad', 'ontwerp-voor-solderen', 'todo', 2)],
 [s(2), b('14', '🚧 14 Eigen 3D-pakket, bijv. Blender', '14-eigen-3d-pakket', style='todoOpt')],
 [s(), b('15', '15 Zelf 3D printen: slicer-instellingen', '15-3d-printen', span=2)],
 [b('16s', '🚧 16 Draadjes op maat knippen', '16-bedrading', 'draadjes-op-maat-knippen', 'todo'),
  b('16g', '🚧 16 Solderen', '16-bedrading', 'solderen', 'todo', 2)],
 [b('17', '⚠️ 17 Controller assembleren en presenteren', '17-assembleren-presenteren', style='deels', span=3)],
]
for r in rows:
    assert sum(int(w) for w in re.findall(r'width="(\d+)" height', ''.join(r))) == 3 * COL, r
print('<p>\n' + '<br>\n'.join(''.join(r) for r in rows) + '\n</p>')
