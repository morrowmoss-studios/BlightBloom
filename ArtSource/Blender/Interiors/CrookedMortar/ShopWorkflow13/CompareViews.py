from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent/'Previews';out=D/'Comparison';out.mkdir(exist_ok=True)
for n in ['EntranceWide','CounterGameplay','CabinetClose','RoomClay','EntranceOpen','WorkingSide']:
 a=Image.open(D/'Before'/f'{n}.png').convert('RGB');b=Image.open(D/'After'/f'{n}.png').convert('RGB');assert a.size==b.size;a.thumbnail((1000,600));b.thumbnail((1000,600));w,h=a.size;c=Image.new('RGB',(2*w,h+36),(28,27,24));c.paste(a,(0,36));c.paste(b,(w,36));dr=ImageDraw.Draw(c);dr.text((15,10),'WORKFLOW12 BASELINE',fill='white');dr.text((w+15,10),'WORKFLOW13 RECONSTRUCTION',fill='white');c.save(out/f'{n}.jpg',quality=94)
