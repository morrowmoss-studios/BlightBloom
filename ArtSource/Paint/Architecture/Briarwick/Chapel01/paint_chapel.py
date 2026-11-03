"""Project-owned rural chapel glass and softened masonry derivative. No lettering."""
from PIL import Image,ImageDraw,ImageEnhance,ImageFilter
from pathlib import Path
import math
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Chapel01/Textures'
# A clean region of the existing stone atlas, softened rather than sharpened.
im=Image.open(R/'Assets/Medieval_house_lite/Textures/rock2/rock2_BaseColor.png').convert('RGB').crop((1445,713,2286,1268)).resize((1024,676),Image.Resampling.LANCZOS)
im=ImageEnhance.Contrast(im).enhance(.70);im=ImageEnhance.Color(im).enhance(.68);im=Image.blend(im,Image.new('RGB',im.size,(155,148,130)),.17);im=im.filter(ImageFilter.GaussianBlur(.45));im.save(H/'Chapel01_Masonry.png');im.save(A/'BW_Chapel01_Masonry.png')
N=1024;im=Image.new('RGB',(N,N),(116,147,150));d=ImageDraw.Draw(im);lead=(65,63,56)
# Broad handmade panes; low-frequency painterly variation is added after their design.
cols=[(104,141,146),(115,151,148),(143,162,146),(172,169,126),(162,152,120),(122,143,154)]
for j in range(5):
 for i in range(6):
  x=-110+i*230+(j%2)*115;y=-100+j*255;poly=[(x,y+130),(x+115,y),(x+230,y+130),(x+115,y+255)];d.polygon(poly,fill=cols[(i+2*j)%len(cols)]);d.line(poly+[poly[0]],fill=lead,width=7)
# Muted amber sun, lead ring and a simple grain/leaf sprig; no text or letter motif.
d.ellipse((388,245,636,493),fill=(190,161,92),outline=lead,width=10);d.ellipse((413,270,611,468),outline=(211,187,120),width=5)
for angle in range(0,360,45):
 a=math.radians(angle);x=512+148*math.cos(a);y=369+148*math.sin(a);xx=512+195*math.cos(a);yy=369+195*math.sin(a);d.line((x,y,xx,yy),fill=lead,width=7)
d.line([(512,912),(502,790),(516,676),(512,562)],fill=lead,width=12)
for y,side in [(820,-1),(760,1),(694,-1),(628,1)]:
 x=509;tip=(x+side*145,y-115);poly=[(x,y),(x+side*122,y-34),tip,(x+side*18,y-89)];d.polygon(poly,fill=(133,153,109) if side<0 else (159,165,117));d.line(poly+[poly[0]],fill=lead,width=9);d.line((x,y,tip[0],tip[1]),fill=lead,width=4)
# Illustrated broad glass transitions, avoiding micro-noise or glossy PBR.
pix=im.load()
for y in range(N):
 for x in range(N):
  q=.97+.035*math.sin(x*.013+y*.006)+.022*math.sin(y*.019-x*.004);pix[x,y]=tuple(max(0,min(255,round(c*q))) for c in pix[x,y])
im=im.filter(ImageFilter.GaussianBlur(.4));im.save(H/'Chapel01_StainedGlass.png');im.save(A/'BW_Chapel01_StainedGlass.png')
print('Painted masonry and sun/sprig stained glass saved; no lettering.')
