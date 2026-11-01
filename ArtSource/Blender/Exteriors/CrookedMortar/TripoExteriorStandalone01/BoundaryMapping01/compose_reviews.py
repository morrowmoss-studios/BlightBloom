from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent;names=['Front','Rear','Left','Right','Underside','Overview']
for name in names:
 a=D/f'{name}_House.png';b=D/f'{name}_Guides.png'
 if a.exists() and b.exists():Image.alpha_composite(Image.open(a).convert('RGBA'),Image.open(b).convert('RGBA')).convert('RGB').save(D/f'Boundary_{name}.png')
if all((D/f'Boundary_{n}.png').exists() for n in names):
 sheet=Image.new('RGB',(1800,1390),(38,38,36));dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',20)
 for i,name in enumerate(names):
  im=Image.open(D/f'Boundary_{name}.png');im.thumbnail((600,429),Image.Resampling.LANCZOS);x=(i%3)*600;y=(i//3)*465;sheet.paste(im,(x,y+26));dr.text((x+10,y+2),name,font=font,fill=(245,235,215))
 # two rows only; crop excess unused space
 sheet.crop((0,0,1800,930)).save(D/'Boundary_AllViews.jpg',quality=96)
