from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
D=Path(__file__).resolve().parent;import json;v=json.loads((D/'Validation.json').read_text());rec=json.loads((D/'Recovery.json').read_text());O=D/'Comparisons';font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia.ttf',23)
views=['FrontThreeQuarter','FrontEntrance','Side','Rear','RoofAbove','SignClose','GameplayDistance','RoofDetail','TimberDetail','FoliageDetail','WindowsDetail']
for name in views:
 paths=[O/f'{label}_{name}.png' for label in ['Original','Repaired','Optimized']]
 if not all(p.exists() for p in paths):continue
 sheet=Image.new('RGB',(1920,635),(34,34,32));draw=ImageDraw.Draw(sheet)
 for i,(p,label) in enumerate(zip(paths,['Original — 1,880,780 triangles',f"Repaired — {v['repaired_evaluated_triangles']:,} triangles",f"Optimized — {rec['optimized_total_triangles']:,} triangles"])):
  im=Image.open(p).convert('RGB');im.thumbnail((640,582),Image.Resampling.LANCZOS);sheet.paste(im,(i*640,45));draw.text((i*640+12,10),label,font=font,fill=(232,222,199))
 sheet.save(O/f'Compare_{name}.jpg',quality=94)
print('Comparison sheets',len(list(O.glob('Compare_*.jpg'))))
