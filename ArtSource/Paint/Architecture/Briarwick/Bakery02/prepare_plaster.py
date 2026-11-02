from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures'
base=Image.open(R/'ArtSource/Paint/Architecture/Briarwick/Bakery01/Plaster_CleanRegion01.png').convert('RGB');base=ImageEnhance.Contrast(base).enhance(.45)
atlas=Image.new('RGB',(2048,2048));svg=['<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="2048">']
for i in range(4):
 panel=base.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if i%2 else base.copy();panel=panel.resize((1024,1024),Image.Resampling.BICUBIC)
 wash=Image.new('RGBA',(1024,1024));d=ImageDraw.Draw(wash);d.ellipse((-160+i*65,590,850,1350),fill=(109,101,84,40));d.ellipse((220,-190,1150,410),fill=(208,195,166,30));wash=wash.filter(ImageFilter.GaussianBlur(100));panel=Image.alpha_composite(panel.convert('RGBA'),wash).convert('RGB');atlas.paste(panel,((i%2)*1024,(i//2)*1024));svg.append(f'<g transform="translate({i%2*1024},{i//2*1024})"><rect width="1024" height="1024" fill="#b7b5a7"/><ellipse cx="{300+i*65}" cy="950" rx="500" ry="350" fill="#82765d" opacity=".13"/><ellipse cx="680" cy="110" rx="490" ry="270" fill="#d0c3a6" opacity=".1"/></g>')
atlas=atlas.filter(ImageFilter.GaussianBlur(1));atlas.save(H/'Plaster_PaintedAtlas02.png');atlas.save(A/'BW_Bakery02_Plaster_BaseColor.png');svg.append('</svg>');(H/'Plaster_Washes02.svg').write_text('\n'.join(svg))
