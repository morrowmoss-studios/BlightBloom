"""Editable flat-colour / brush-shape painting source; no photographic noise."""
from PIL import Image, ImageDraw
from pathlib import Path
R=Path(__file__).resolve().parents[4]
out=R/'Assets/BlightBloom/Characters/PlagueDoctor01/Textures/BB_Doctor_PaintedAtlas.png'
im=Image.new('RGB',(1024,1024));d=ImageDraw.Draw(im)
colours=[(77,82,54),(205,192,151),(73,48,32),(154,120,62)]
for i,c in enumerate(colours):
 x=(i%2)*512;y=(i//2)*512;d.rectangle((x,y,x+511,y+511),fill=c)
 # Broad, intentionally placed brush ribbons, kept within a small value range.
 for j in range(9):
  xx=x+20+j*56;v=6 if j%3==0 else -3
  cc=tuple(max(0,min(255,k+v)) for k in c)
  d.polygon([(xx,y+12),(xx+24,y+20),(xx+39,y+188),(xx+19,y+352),(xx+35,y+496),(xx+6,y+490),(xx-3,y+314),(xx+8,y+173)],fill=cc)
 # Quiet painted hems and hand-drawn botanical sprigs in cloth region.
 if i==0:
  for yy in [31,479]:d.line((x+12,y+yy,x+499,y+yy),fill=(152,130,77),width=4)
  for xx in [67,193,319,445]:
   d.line([(xx,446),(xx-4,399),(xx+5,356),(xx+1,316)],fill=(151,133,82),width=3)
   for yy in [335,365,395,421]:
    d.polygon([(xx,yy+5),(xx-23,yy-10),(xx-27,yy-24),(xx-9,yy-17)],fill=(147,131,80))
    d.polygon([(xx,yy-5),(xx+19,yy-25),(xx+29,yy-27),(xx+22,yy-9)],fill=(160,140,85))
im.save(out)
print(out)
