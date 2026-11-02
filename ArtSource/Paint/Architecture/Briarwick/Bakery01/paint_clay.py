"""Muted clay swatches for modeled pan-and-cover tiles. Editable SVG master, raster maps."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import math,json
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures'
w=1024;im=Image.new('RGB',(w,w));d=ImageDraw.Draw(im);svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024">']
colors=[(133,105,88),(141,113,93),(128,106,94),(146,117,97),(138,106,85),(132,112,100),(143,115,98),(136,109,91)]
for k,c in enumerate(colors):
 x=(k%4)*256;y=(k//4)*512;d.rectangle((x,y,x+255,y+511),fill=c);svg.append(f'<rect x="{x}" y="{y}" width="256" height="512" fill="rgb{c}"/>')
 for j in range(18):
  xx=x+8+j*14;co=tuple(min(255,max(0,v+int(7*math.sin(j*.8+k)))) for v in c)
  pts=[(xx+4*math.sin(t*.04+k),y+t) for t in range(0,513,12)];d.line(pts,fill=co,width=13)
  svg.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{a:.1f},{b:.1f}' for i,(a,b) in enumerate(pts))+'" fill="none" stroke="rgb'+str(co)+'" stroke-width="13" opacity=".6"/>')
 # broad kiln blushes, restrained rain-darkened upper lap, worn bottom edge
 for yy in range(512):
  delta=round(-6*math.exp(-yy/70)+3*math.exp(-((yy-475)/35)**2))
  if delta:
   for xx in range(256):
    c0=im.getpixel((x+xx,y+yy));im.putpixel((x+xx,y+yy),tuple(v+delta for v in c0))
 svg.append(f'<path d="M{x+12},{y+478} Q{x+128},{y+470} {x+244},{y+482}" stroke="#bc9a7c" stroke-width="5" opacity=".25" fill="none"/>')
svg.append('</svg>');(H/'ClayTile_Painting01.svg').write_text('\n'.join(svg));im=im.filter(ImageFilter.GaussianBlur(2));im.save(H/'ClayTile_PaintedSwatches.png');im.save(A/'BW_Bakery01_Clay_BaseColor.png')
Image.new('RGBA',(128,128),(0,0,0,16)).save(A/'BW_Bakery01_Clay_MetallicSmoothness.png')
(H/'Palette.json').write_text(json.dumps({'swatches':colors,'layout':'4 columns x 2 rows; each physical tile gets one swatch','finish':'muted earthen clay, nonmetallic, smoothness .063; modeled curvature provides shading'},indent=2))
