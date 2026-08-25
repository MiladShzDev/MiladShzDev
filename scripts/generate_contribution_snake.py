import re, urllib.request
from datetime import date, timedelta
from pathlib import Path

USER = 'MiladShzDev'
COLORS = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']
CELL, GAP = 12, 4

url = f'https://github.com/users/{USER}/contributions'
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'https://github.com/{USER}',
    },
)
page = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')

pairs = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="([0-4])"', page)
rows = {date.fromisoformat(d): int(level) for d, level in pairs}
if len(rows) < 300:
    raise SystemExit(f'contribution calendar not found or incomplete: {len(rows)} cells')

first = min(rows)
start = first - timedelta(days=(first.weekday() + 1) % 7)
weeks = max(53, ((max(rows) - start).days // 7) + 1)

order = []
for x in range(weeks):
    ys = range(7) if x % 2 == 0 else range(6, -1, -1)
    order += [(x, y) for y in ys]

index = {pos: i for i, pos in enumerate(order)}
width = weeks * (CELL + GAP) + 12
height = 7 * (CELL + GAP) + 42

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
    '<title>GitHub contribution snake for MiladShzDev</title>',
    '<style>@keyframes eat{0%,62%{opacity:1;transform:scale(1)}64%{opacity:.2;transform:scale(.86)}66%,100%{opacity:.16;transform:scale(.72)}}.c{transform-box:fill-box;transform-origin:center;animation:eat 14s linear infinite}</style>',
    f'<rect width="{width}" height="{height}" rx="14" fill="#0d1117"/>',
]

for x in range(weeks):
    for y in range(7):
        day = start + timedelta(days=x * 7 + y)
        level = rows.get(day, 0)
        delay = index[(x, y)] * 32
        px = 6 + x * (CELL + GAP)
        py = 28 + y * (CELL + GAP)
        svg.append(
            f'<rect class="c" x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{COLORS[level]}" style="animation-delay:{delay}ms"/>'
        )

points = ' '.join(
    f'{6 + x * (CELL + GAP) + CELL / 2},{28 + y * (CELL + GAP) + CELL / 2}'
    for x, y in order
)
svg.append(f'<polyline id="path" points="{points}" fill="none" stroke="none"/>')

for i in range(5):
    color = '#ffffff' if i == 0 else '#a371f7'
    radius = 4 if i == 0 else 3
    begin = -i * 180
    svg.append(
        f'<circle r="{radius}" fill="{color}">'
        f'<animateMotion dur="14s" begin="{begin}ms" repeatCount="indefinite">'
        '<mpath href="#path"/></animateMotion></circle>'
    )

svg.append('</svg>')
Path('assets').mkdir(exist_ok=True)
Path('assets/contribution-snake.svg').write_text('\n'.join(svg), encoding='utf-8')
print(f'generated {len(rows)} contribution cells across {weeks} weeks')
