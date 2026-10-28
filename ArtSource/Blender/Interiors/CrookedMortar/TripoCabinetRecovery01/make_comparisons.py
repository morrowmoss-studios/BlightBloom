from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
D=Path(__file__).resolve().parent;out=D/'Comparisons';out.mkdir(exist_ok=True);report={}
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28)
for label in ['CabinetA','CabinetB']:
 report[label]={}
 for view in ['Front','ThreeQuarter','Side','CrownDetail','DrawerDetail','Gameplay']:
  paths=[D/label/'Previews'/f'{state}_{view}.png' for state in ['High','Optimized']]
  if not all(p.exists() for p in paths):continue
  ims=[Image.open(p).convert('RGB') for p in paths];w,h=ims[0].size
  sheet=Image.new('RGB',(w*2,h+60),(30,32,35));dr=ImageDraw.Draw(sheet)
  for i,im in enumerate(ims):
   sheet.paste(im,(i*w,60));dr.text((i*w+20,16),f'{label} | {"Original high detail" if i==0 else "Optimized 45% reduction"} | {view}',font=font,fill=(235,230,220))
  sheet.save(out/f'{label}_{view}_Comparison.jpg',quality=94)
  diff=abs(np.array(ims[0],dtype=float)-np.array(ims[1],dtype=float));report[label][view]={'full_frame_mean_absolute_RGB_difference_0_255':float(diff.mean()),'p99_channel_difference':float(np.percentile(diff,99))}
(D/'ImageComparisonMetrics.json').write_text(json.dumps(report,indent=2));print(report)
