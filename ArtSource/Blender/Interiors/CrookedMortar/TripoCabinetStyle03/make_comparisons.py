from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
D=Path(__file__).resolve().parent;out=D/'Comparisons';out.mkdir(exist_ok=True);font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',28);states=['Original','Style02','PrototypeA','PrototypeB'];metrics={}
for view in ['ThreeQuarter','CrownWood','FoliagePlanter','ContentsBrass','Gameplay']:
 paths=[D/'Previews'/f'{s}_{view}.png' for s in states]
 if not all(p.exists() for p in paths):continue
 ims=[Image.open(p).convert('RGB') for p in paths];w,h=ims[0].size;sheet=Image.new('RGB',(w*4,h+65),(29,29,29));draw=ImageDraw.Draw(sheet)
 for i,(im,label) in enumerate(zip(ims,['Tripo original finish','Style02','Style03 A — reconstructed','Style03 B — expressive'])):
  sheet.paste(im,(i*w,65));draw.text((i*w+18,18),label,font=font,fill=(235,232,224))
 sheet.save(out/f'{view}_FourWay.png')
 arrays=[np.asarray(im,dtype=np.float32) for im in ims];background=arrays[0][0,0];mask=np.max(np.abs(arrays[0]-background),axis=2)>5;metrics[view]={}
 for a,b in [(0,1),(1,2),(1,3),(2,3)]:
  dif=np.abs(arrays[a]-arrays[b])[mask];metrics[view][f'{states[a]}_vs_{states[b]}']={'foreground_mean_absolute_RGB_difference_0_255':float(dif.mean()),'foreground_fraction_mean_RGB_difference_over_15':float((dif.mean(axis=1)>15).mean())}
(D/'ImageDifferenceEvidence.json').write_text(json.dumps({'warning':'Pixel differences indicate change, not artistic quality or reference matching. Foreground mask derived from original frame against constant neutral background.','views':metrics},indent=2));print('FOUR_WAY_SHEETS',len(metrics));print(json.dumps(metrics.get('Gameplay',{}),indent=2))
