"""Editable vector label artwork, rasterized from the same drawing commands; no noise/filter pass."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import html
D=Path(__file__).resolve().parent;R=D.parents[4];dest=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ApothecaryFurnishings01/Textures/CM_AF01_BotanicalLabels.png'
W,H=1536,1024;im=Image.new('RGB',(W,H),(221,209,177));draw=ImageDraw.Draw(im);svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#ddd1b1"/>']
ink='#514937';light='#9d9567';sage='#707852';font='/System/Library/Fonts/Supplemental/Georgia.ttf'
def line(points,fill=ink,width=3):
 draw.line(points,fill=fill,width=width,joint='curve');svg.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{fill}" stroke-width="{width}" stroke-linecap="round"/>')
def poly(points,fill):
 draw.polygon(points,fill=fill);svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}"/>')
def text(x,y,t,size):
 f=ImageFont.truetype(font,size);draw.text((x,y),t,font=f,fill=ink,anchor='mt');svg.append(f'<text x="{x}" y="{y+size}" text-anchor="middle" font-family="Georgia,serif" font-size="{size}" fill="{ink}">{html.escape(t)}</text>')
names=['SALVIA','THYMUS','ROSMARIN','MATRICARIA','TINCTURA','SIMPLEX','REMEDIES','OBSERVATIONS']
for i,name in enumerate(names):
 x=(i%4)*384;y=(i//4)*512
 line([(x+22,y+22),(x+360,y+22),(x+360,y+490),(x+22,y+490),(x+22,y+22)],light,4)
 line([(x+31,y+34),(x+350,y+34)],light,2)
 text(x+192,y+64,'THE CROOKED MORTAR',16);text(x+192,y+112,name,28)
 if i<6:
  stem=[(x+185,y+363),(x+194,y+320),(x+186,y+270),(x+200,y+219)];line(stem,sage,5)
  for j in range(4):
   h=y+255+j*27;side=(-1 if (j+i)%2 else 1);a=x+190;b=a+side*(47+j*4)
   poly([(a,h+12),(b,h-21),(a+side*25,h-14),(b,h+3)],sage);line([(a,h+12),(b,h-14)],light,2)
  text(x+192,y+394,'Gathered & prepared by hand',17);text(x+192,y+433,'Herbs for the living',16)
 else:
  for j in range(7):
   yy=y+193+j*33;line([(x+53,yy),(x+278-(j%3)*15,yy+2)],light,2)
   if i==6:text(x+310,yy-11,str((j+1)*3),17)
  line([(x+300,y+175),(x+300,y+444)],light,2)
svg.append('</svg>');(D/'CM_AF01_BotanicalLabels.svg').write_text('\n'.join(svg));im.save(dest);print(dest)
