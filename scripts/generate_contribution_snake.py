import html,re,urllib.request
from datetime import date,timedelta
from pathlib import Path

USER='MiladShzDev'
COLORS=['#161b22','#0e4429','#006d32','#26a641','#39d353']
CELL,GAP=12,4

p=urllib.request.Request(f'https://github.com/{USER}',headers={'User-Agent':'Mozilla/5.0'})
page=urllib.request.urlopen(p,timeout=30).read().decode('utf-8','replace')
pat=re.compile(r'<td\\b[^>]*data-date="(\\d{4}-\\d{2}-\\d{2})"[^>]*data-level="([0-4])"',re.I)
rows={(date.fromisoformat(d)):int(l) for d,l in pat.findall(page)}
if len(rows)<300: raise SystemExit(f'contribution cells not found: {len(rows)}')
first=min(rows); start=first-timedelta(days=(first.weekday()+1)%7); weeks=((max(rows)-start).days//7)+1; weeks=max(53,weeks)
order=[]
for x in range(weeks):
    ys=range(7) if x%2==0 else range(6,-1,-1)
    order += [(x,y) for y in ys]
idx={p:i for i,p in enumerate(order)}
w=weeks*(CELL+GAP)+12; h=7*(CELL+GAP)+42
s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">','<style>@keyframes eat{0%,62%{opacity:1}64%{opacity:.15}66%,100%{opacity:.15}}.c{animation:eat 14s linear infinite}</style>',f'<rect width="{w}" height="{h}" rx="14" fill="#0d1117"/>']
for x in range(weeks):
  for y in range(7):
    d=start+timedelta(days=x*7+y); level=rows.get(d,0); delay=idx[(x,y)]*32
    s.append(f'<rect class="c" x="{6+x*(CELL+GAP)}" y="{28+y*(CELL+GAP)}" width="{CELL}" height="{CELL}" rx="2" fill="{COLORS[level]}" style="animation-delay:{delay}ms"/>')
pts=' '.join(f'{6+x*(CELL+GAP)+CELL/2},{28+y*(CELL+GAP)+CELL/2}' for x,y in order)
s.append(f'<polyline id="p" points="{pts}" fill="none" stroke="none"/>')
for i in range(5):
  s.append(f'<circle r="{4 if i==0 else 3}" fill="{ "#fff" if i==0 else "#a371f7" }"><animateMotion dur="14s" begin="-{i*180}ms" repeatCount="indefinite"><mpath href="#p"/></animateMotion></circle>')
s.append('</svg>')
Path('assets').mkdir(exist_ok=True)
Path('assets/contribution-snake.svg').write_text('\\n'.join(s),encoding='utf-8')
print(f'generated {len(rows)} cells across {weeks} weeks')
