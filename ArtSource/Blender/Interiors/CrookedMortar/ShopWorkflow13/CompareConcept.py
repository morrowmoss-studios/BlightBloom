from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent
for view in ['CounterGameplay','EntranceWide']:
 a=Image.open(D/'ReferenceTarget.png').convert('RGB');b=Image.open(D/'Previews/After'/f'{view}.png').convert('RGB');a.thumbnail((1100,750));b.thumbnail((1100,750));h=max(a.height,b.height);im=Image.new('RGB',(a.width+b.width,h+40),(28,25,21));im.paste(a,(0,40+(h-a.height)//2));im.paste(b,(a.width,40+(h-b.height)//2));dr=ImageDraw.Draw(im);dr.text((14,12),'APPROVED ILLUSTRATED TARGET',fill='white');dr.text((a.width+14,12),'WORKFLOW13 - ACTUAL UNITY GAME VIEW / ADAPTED EXISTING LAYOUT',fill='white');im.save(D/'Previews/Comparison'/f'Concept_{view}.jpg',quality=94)
