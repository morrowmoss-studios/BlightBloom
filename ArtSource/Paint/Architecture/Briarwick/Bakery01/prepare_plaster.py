"""Extract an unframed soft plaster region; discard source-specific timber AO."""
from pathlib import Path
from PIL import Image,ImageFilter
import json
H=Path(__file__).parent;R=H.parents[4];src=R/'Assets/Medieval_house_lite/Textures/concrete';A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures'
rect=(.860,.220,.875,.285)
for role in ['BaseColor','Normal','Roughness']:
 im=Image.open(src/f'concrete_{role}.png');w,h=im.size;crop=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(rect))).resize((512,1024),Image.Resampling.LANCZOS)
 if role=='BaseColor':crop=crop.filter(ImageFilter.GaussianBlur(.4));crop.save(H/'Plaster_CleanRegion01.png')
 crop.save(A/f'BW_Bakery01_Plaster_{role}.png')
(H/'PlasterRegion.json').write_text(json.dumps({'source':str(src.relative_to(R)),'cropImageCoordinates':rect,'sourceAO':'not reused: original atlas contains black timber silhouettes unrelated to new geometry','UV':'normalized previous bakery plaster region'},indent=2))
