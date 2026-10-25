from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent/'Previews';out=D/'Comparison';out.mkdir(exist_ok=True)
for name in ['GameplayDressed','FrontBare','AngledBare','FrontDressed','CarvingClose','ClayBare']:
 a=Image.open(D/'Existing'/f'{name}.png').convert('RGB');b=Image.open(D/'Candidate'/f'{name}.png').convert('RGB');assert a.size==b.size
 a.thumbnail((1000,600));b.thumbnail((1000,600));w,h=a.size;canvas=Image.new('RGB',(2*w,h+38),(28,27,24));canvas.paste(a,(0,38));canvas.paste(b,(w,38));draw=ImageDraw.Draw(canvas);draw.text((16,12),'EXISTING COUNTER',fill='white');draw.text((w+16,12),'WORKFLOW 07 CANDIDATE',fill='white');canvas.save(out/f'{name}.jpg',quality=94)
