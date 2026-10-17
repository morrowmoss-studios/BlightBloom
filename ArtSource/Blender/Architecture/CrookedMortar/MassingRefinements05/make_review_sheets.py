"""Contact sheets of actual Unity captures, unchanged apart from uniform resizing and labels."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
out=Path(__file__).parent/'Previews'
font='/System/Library/Fonts/Supplemental/Arial.ttf'
for view in ['Front','ThreeQuarter']:
 sheet=Image.new('RGB',(1800,598),'#34383c');draw=ImageDraw.Draw(sheet)
 for i,(id,title) in enumerate([('A','Conservative refinement'),('B','Moderate refinement'),('C','Bold refinement')]):
  pic=Image.open(out/f'{id}_{view}.png').convert('RGB');pic=pic.resize((600,514),Image.Resampling.LANCZOS);sheet.paste(pic,(i*600,74));draw.text((i*600+20,14),f'{id}  {title}',font=ImageFont.truetype(font,25),fill='#f2f2f2');draw.text((i*600+20,44),'FRONT' if view=='Front' else 'FRONT THREE-QUARTER',font=ImageFont.truetype(font,16),fill='#c8ced4')
 sheet.save(out/f'{view}_Comparison.png')
