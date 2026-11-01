from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).resolve().parent;f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24);small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
names=['FullFront','FullRear','FullLeft','FullRight','Overview','Underside','PorchLeft','PorchRight','RockIvyLeft','RockIvyRight','PlanterLeft','PlanterRight']
for name in names:
 out=Image.new('RGB',(2800,1100),(27,29,31));d=ImageDraw.Draw(out)
 for i,mode in enumerate(['Original','Separated']):
  im=Image.open(D/(name+'_'+mode+'.png')).convert('RGB');assert im.size==(1400,1000);out.paste(im,(i*1400,50));d.text((i*1400+20,12),name+' | '+('BoundaryMapping02 source' if i==0 else 'Controlled separation — retained contacts flagged'),font=f,fill='white')
 d.text((20,1060),'Identical camera / lighting / exposure. Right: giant platform removed; local inseparable rock/root collars remain for review.',font=small,fill=(230,221,199));out.save(D/(name+'_Comparison.jpg'),quality=94)
for title,group in [('Elevations',['FullFront','FullRear','FullLeft','FullRight']),('Contacts',['PorchLeft','PorchRight','RockIvyLeft','RockIvyRight','PlanterLeft','PlanterRight'])]:
 rows=(len(group)+1)//2;sheet=Image.new('RGB',(1800,rows*354),(27,29,31))
 for i,name in enumerate(group):
  im=Image.open(D/(name+'_Comparison.jpg'));im.thumbnail((900,354));sheet.paste(im,((i%2)*900,(i//2)*354))
 sheet.save(D/(title+'_ContactSheet.jpg'),quality=94)
print('Matched comparisons saved')
