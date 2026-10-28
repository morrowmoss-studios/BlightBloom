from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent;out=D/'Comparisons';out.mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28)
for view in ['Front','ThreeQuarter','Side','Gameplay','FinishDetail']:
 ps=[D/'Previews'/f'{s}_{view}.png' for s in ['Before','Style02']]
 if not all(p.exists() for p in ps):continue
 ims=[Image.open(p).convert('RGB') for p in ps];w,h=ims[0].size;sheet=Image.new('RGB',(w*2,h+60),(30,32,30));draw=ImageDraw.Draw(sheet)
 for i,im in enumerate(ims):
  sheet.paste(im,(i*w,60));draw.text((i*w+20,16),f'{"Recovered B — before" if i==0 else "Style02 — painted finish"} | {view}',font=font,fill=(235,230,220))
 sheet.save(out/f'{view}_Comparison.jpg',quality=94)
print('COMPARISONS',len(list(out.glob('*.jpg'))))
