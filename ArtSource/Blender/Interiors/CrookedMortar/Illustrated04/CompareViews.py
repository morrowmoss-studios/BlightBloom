from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent/'Previews';(D/'Comparison').mkdir(exist_ok=True)
for before in (D/'Before').glob('*.png'):
 after=D/'After'/before.name
 if not after.exists():continue
 ims=[Image.open(before).convert('RGB'),Image.open(after).convert('RGB')]
 width=1000;h=round(ims[0].height*width/ims[0].width);canvas=Image.new('RGB',(width*2,h+30),(35,29,25))
 for i,im in enumerate(ims):canvas.paste(im.resize((width,h),Image.Resampling.LANCZOS),(i*width,30))
 draw=ImageDraw.Draw(canvas);draw.text((15,9),'BEFORE',fill=(238,222,194));draw.text((width+15,9),'AFTER',fill=(238,222,194));canvas.save(D/'Comparison'/(before.stem+'.jpg'),quality=94)
