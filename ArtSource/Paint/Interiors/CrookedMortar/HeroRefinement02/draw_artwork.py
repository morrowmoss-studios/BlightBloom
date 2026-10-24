"""Authored ink-and-gouache style paper atlas. Matching editable SVG, no noise or scratch generator."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import math,html
D=Path(__file__).resolve().parent;R=D.parents[4];W,H=2048,1024
im=Image.new('RGB',(W,H),'#dbc89d');dr=ImageDraw.Draw(im);sv=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#dbc89d"/>']
font='/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
def path(ps,c='#75694c',w=3):
 dr.line(ps,fill=c,width=w,joint='curve');sv.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in ps)+f'" stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round"/>')
def poly(ps,c):
 dr.polygon(ps,fill=c);sv.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in ps)+f'" fill="{c}"/>')
def text(x,y,t,size=28):
 f=ImageFont.truetype(font,size);dr.text((x,y),t,font=f,fill='#4b4433',anchor='mt');sv.append(f'<text x="{x}" y="{y+size}" text-anchor="middle" font-family="Georgia" font-style="italic" font-size="{size}" fill="#4b4433">{html.escape(t)}</text>')
def sprig(x,y,scale=1):
 ps=[(x-8*scale,y+70*scale),(x+4*scale,y+20*scale),(x-4*scale,y-35*scale),(x+8*scale,y-78*scale)];path(ps,'#5b6948',int(5*scale))
 for j in range(5):
  yy=y+45*scale-j*26*scale;side=1 if j%2 else -1;poly([(x,yy),(x+side*44*scale,yy-26*scale),(x+side*51*scale,yy-13*scale),(x+side*10*scale,yy+5*scale)],'#78815b');path([(x,yy),(x+side*42*scale,yy-18*scale)],'#b4ac76',2)
for i in range(8):
 x=i%4*512;y=i//4*512
 # Broad warm paper edge shapes, selective rather than noise.
 poly([(x,y),(x+512,y),(x+512,y+24),(x+375,y+18),(x+98,y+30),(x,y+20)],'#cbb88e')
 path([(x+25,y+35),(x+478,y+30),(x+483,y+478),(x+29,y+482),(x+25,y+35)],'#9b895f',3)
 if i<4:
  names=['Sage leaf','Feverfew','Lavender','Willow bark'];text(x+256,y+68,names[i],43);sprig(x+260,y+265,1.2)
  text(x+256,y+402,['For throat & breath','Gather before noon','For a quiet night','Dried in the shade'][i],23);text(x+256,y+448,'R. — The Crooked Mortar',20)
 elif i==4:
  text(x+256,y+53,'Robert’s Formulary',33);text(x+256,y+98,'Observations / Spring',23);sprig(x+125,y+247,.85)
  for yy,t in [(172,'Sage, two parts'),(211,'Thyme, one part'),(250,'Steep; do not boil'),(305,'Mrs. Bell — revisit'),(345,'after the third day')]:text(x+330,y+yy,t,20)
  path([(x+75,y+414),(x+440,y+410)],'#9b895f',2);text(x+256,y+439,'Always leave enough for seed.',20)
 elif i==5:
  text(x+256,y+70,'The Crooked Mortar',32);sprig(x+256,y+250,1);text(x+256,y+371,'Consultations & Remedies',25);text(x+256,y+418,'Herbs for the living',23);text(x+256,y+452,'Care for the lost',20)
 elif i==6:
  text(x+256,y+57,'Apothecary accounts',31)
  for j,t in enumerate(['Willow bark   /   2 c.','Clean linen   /   6 rolls','Sage tincture /   3 vials','Mrs. Bell     /   paid','New hinges    /   owing','Roof slates   /   mended']):text(x+250,y+135+j*48,t,23)
  path([(x+65,y+433),(x+445,y+428)],'#9b895f',3);text(x+280,y+449,'R.',25)
 else:
  text(x+256,y+62,'Gathering notes',33);sprig(x+180,y+266,1.25);text(x+356,y+190,'Fresh tips',20);text(x+357,y+239,'only',20);path([(x+332,y+284),(x+225,y+262)],'#75694c',2);text(x+256,y+425,'Return the roots to earth.',23)
sv.append('</svg>');(D/'CM_HR02_InkArtwork.svg').write_text('\n'.join(sv));im.save(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/HeroRefinement02/Textures/CM_HR02_InkArtwork.png')
