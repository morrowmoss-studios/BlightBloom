from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
D=Path(__file__).resolve().parent
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',17)
notes={
'PorchLeft':['KEEP: full dressed-stone corner, post base, pot and lowest step.','REMOVE: loose rounded boulder left of porch; path and ground weeds.'],
'PorchRight':['KEEP: projecting masonry toe, full step return, porch pot and wall ivy.','REMOVE: cobbles and loose boulders; CYAN side contact needs local repair.'],
'RockIvyLeft':['KEEP: window box, all coursed foundation stones and porch masonry.','REMOVE: rounded boulder. CYAN: hidden foundation return; not a cut edge.'],
'RockIvyRight':['KEEP: wall-attached ivy and window box; preserve architectural foliage.','REMOVE: loose rock chain/ground mat. CYAN: separate roots locally; patch lower return.'],
'PlanterLeft':['KEEP: masonry herb bed + plants, adjacent container, door threshold and timber.','REMOVE: path weeds, dirt apron and small loose rock in front of bed.'],
'PlanterRight':['KEEP: complete herb bed, adjacent container, plants and annex threshold.','REMOVE: loose toe rock, lawn/weed mat and cobbled path.'],
'Rear':['KEEP: rail/posts, raised plank platform and plinth as one attached assembly.','REMOVE: cobbled skirt and loose corner rocks. Hidden underside needs closure review.'],
'RearUnder':['Platform underside remains fused: no hidden foundation cut level established.','CYAN is the projected rear contact proposal, not a verified underside edge.']}
for name in notes:
 house=Image.open(D/(name+'_House.png')).convert('RGBA')
 for stage in ['Before','After']:
  im=Image.alpha_composite(house,Image.open(D/(name+'_'+stage+'_Guide.png')).convert('RGBA')).convert('RGB')
  out=Image.new('RGB',(1100,1005),(28,30,32));out.paste(im,(0,50));dr=ImageDraw.Draw(out)
  dr.text((18,14),name+' | '+('BEFORE: Mapping01 guides' if stage=='Before' else 'AFTER: reviewed contact / repair proposals'),font=font,fill='white')
  dr.text((18,908),'MAGENTA: visible contact   ORANGE: previous uncertainty   CYAN: local repair   RED X: loose terrain rock',font=small,fill=(230,220,200))
  for j,t in enumerate(notes[name]):dr.text((18,939+j*25),t,font=small,fill='white')
  out.save(D/(name+'_'+stage+'.jpg'),quality=94)
 pair=Image.new('RGB',(2200,1005));pair.paste(Image.open(D/(name+'_Before.jpg')),(0,0));pair.paste(Image.open(D/(name+'_After.jpg')),(1100,0));pair.save(D/(name+'_Comparison.jpg'),quality=94)
thumb=Image.new('RGB',(1600,1464),(28,30,32))
for i,n in enumerate(notes):
 im=Image.open(D/(n+'_Comparison.jpg'));im.thumbnail((800,366));thumb.paste(im,((i%2)*800,(i//2)*366))
thumb.save(D/'Boundary02_AllCloseups.jpg',quality=92)
