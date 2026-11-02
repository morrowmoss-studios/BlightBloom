"""Eight restrained native-roof grain swatches for individually modeled wooden shingles."""
from pathlib import Path
from PIL import Image,ImageEnhance,ImageFilter
import json
H=Path(__file__).parent;R=H.parents[4];src=R/'Assets/Medieval_house_lite/Textures/roof/roof_BaseColor.png';im=Image.open(src).convert('RGB');w,h=im.size;out=Image.new('RGB',(1024,1024));rects=[]
for i in range(8):
 # Interior of one painted shingle in the first clean atlas course, no baked course shadow.
 x=3+i*8;rect=((x+.5)/900,3/900,(x+6.2)/900,24/900);crop=im.crop((round(rect[0]*w),round(rect[1]*h),round(rect[2]*w),round(rect[3]*h))).resize((256,512),Image.Resampling.BICUBIC);crop=ImageEnhance.Contrast(crop).enhance(.72);crop=ImageEnhance.Color(crop).enhance(.88);crop=crop.filter(ImageFilter.GaussianBlur(.6));out.paste(crop,((i%4)*256,(i//4)*512));rects.append(rect)
out.save(H/'Shingle_GrainAtlas01.png');out.save(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Textures/BW_Inn01_Shingle_BaseColor.png');(H/'SourceRegions.json').write_text(json.dumps({'source':str(src.relative_to(R)),'normalizedImageCropRegions':rects,'changes':'gentle contrast/color restraint, no sharpening or added noise','atlas':'4 columns x 2 rows, one region per physical shingle'},indent=2))
