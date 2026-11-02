"""Prepare a softly finished generated painting for URP, with editable OpenRaster source.
No source/package map is overwritten. Normals are restrained height derivatives, not noise.
"""
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,io,zipfile,xml.etree.ElementTree as ET,json
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures';A.mkdir(parents=True,exist_ok=True)
src=Image.open(H/'Thatch_PaintedSource01.png').convert('RGB');im=src.resize((2048,2048),Image.Resampling.LANCZOS);a=np.asarray(im,dtype=np.float32)/255
soft=np.asarray(im.filter(ImageFilter.GaussianBlur(1.1)),dtype=np.float32)/255
# Keep illustrated brush direction while avoiding razor-sharp fibres and yellow saturation.
rgb=a*.58+soft*.42;mean=rgb.mean(axis=(0,1));rgb=mean+(rgb-mean)*.78
lum=rgb@np.array([.2126,.7152,.0722]);rgb=lum[:,:,None]*.12+rgb*.88;rgb*=np.array([.95,.965,.99])
base=Image.fromarray(np.uint8(np.clip(rgb,0,1)*255));base.save(A/'BW_StableA03_Thatch_BaseColor.png')
height=np.asarray(base.filter(ImageFilter.GaussianBlur(1)),dtype=np.float32).mean(2)/255;dy,dx=np.gradient(height);normal=np.stack([-dx*1.15,-dy*1.15,np.ones_like(dx)],2);normal/=np.linalg.norm(normal,axis=2)[:,:,None];Image.fromarray(np.uint8((normal*.5+.5)*255)).save(A/'BW_StableA03_Thatch_Normal.png')
packed=np.zeros((2048,2048,4),dtype=np.uint8);packed[:,:,3]=np.uint8(np.clip(.075+(height-height.mean())*.10,.055,.105)*255);Image.fromarray(packed).save(A/'BW_StableA03_Thatch_MetallicSmoothness.png')
# OpenRaster layers retain both the full original painting and the restrained working finish.
root=ET.Element('image',{'w':str(src.width),'h':str(src.height),'name':'Stable A03 Thatch painting'});stack=ET.SubElement(root,'stack')
def png(i):b=io.BytesIO();i.save(b,format='PNG');return b.getvalue()
with zipfile.ZipFile(H/'Thatch_Painting01.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 layers=[('Soft working finish',base.resize(src.size,Image.Resampling.LANCZOS),'visible'),('Original generated painting',src,'hidden')]
 for i,(name,layer,visible) in enumerate(layers):
  path=f'data/layer{i}.png';ET.SubElement(stack,'layer',{'name':name,'src':path,'opacity':'1.0','visibility':visible,'composite-op':'svg:src-over','x':'0','y':'0'});z.writestr(path,png(layer))
 z.writestr('stack.xml',ET.tostring(root));z.writestr('mergedimage.png',png(base.resize(src.size)));thumb=base.copy();thumb.thumbnail((256,256));z.writestr('Thumbnails/thumbnail.png',png(thumb))
(H/'MaterialPreparation.json').write_text(json.dumps({'source':'Thatch_PaintedSource01.png','workingResolution':[2048,2048],'normalStrengthUnity':.30,'metallic':0,'smoothnessRange':[float(packed[:,:,3].min()/255),float(packed[:,:,3].max()/255)],'uvPolicy':'Continuous non-tiled slope UVs; different source regions for front, back and lean-to','editablePainting':'Thatch_Painting01.ora'},indent=2))
print('THATCH_MAPS_READY',src.size)
