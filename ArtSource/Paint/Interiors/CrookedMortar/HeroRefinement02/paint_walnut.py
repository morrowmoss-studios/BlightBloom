"""Broad authored timber brush shapes, preserved as SVG. No random grain or scratch pass."""
from pathlib import Path
from PIL import Image,ImageDraw
import math
D=Path(__file__).resolve().parent;R=D.parents[4]
a=Image.open(R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production01/Textures/CM_Production01_ApprovedPaint.png').convert('RGB');w,h=a.size;n=w//2
im=Image.new('RGB',(n,n),'#684228');dr=ImageDraw.Draw(im);sv=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{n}" height="{n}"><rect width="100%" height="100%" fill="#684228"/>']
strokes=[(35,17,29,'#70482d'),(86,-14,42,'#634027'),(147,24,20,'#785033'),(203,-19,57,'#624029'),(278,23,33,'#70482e'),(345,-17,52,'#694129'),(411,21,24,'#795035'),(469,-12,41,'#634029'),(542,19,32,'#70492f'),(597,-16,25,'#764e33')]
for x,bend,wide,c in strokes:
 ps=[(x+bend*math.sin(t/80),t) for t in range(-10,n+10,3)];dr.line(ps,fill=c,width=wide,joint='curve');sv.append('<polyline points="'+' '.join(f'{x:.2f},{y}' for x,y in ps)+f'" stroke="{c}" stroke-width="{wide}" fill="none"/>')
# A small number of quieter long grain accents grouped at planed edges.
for x,b,c in [(26,9,'#805536'),(155,6,'#845b3c'),(283,8,'#805337'),(416,11,'#895e3d'),(548,7,'#805437')]:
 ps=[(x+b*math.sin(t/110),t) for t in range(32,n-29,4)];dr.line(ps,fill=c,width=3,joint='curve');sv.append('<polyline points="'+' '.join(f'{x:.2f},{y}' for x,y in ps)+f'" stroke="{c}" stroke-width="3" fill="none"/>')
sv.append('</svg>');(D/'CM_HR02_WalnutBrushwork.svg').write_text('\n'.join(sv));a.paste(im,(n,0));a.save(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/HeroRefinement02/Textures/CM_HR02_PaintedSheet.png')
