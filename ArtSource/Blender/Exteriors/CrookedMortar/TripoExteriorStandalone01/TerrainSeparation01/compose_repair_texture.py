from PIL import Image,ImageFilter
import numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'FoundationReprojection.npz');uv=A['uv'];depth=A['depth'];images=json.loads((D/'SourceTextureInspection.json').read_text());source=next(i for i in images if i['colorspace']=='sRGB');im=np.array(Image.open(source['read_only_copy']).convert('RGB'),np.float32);h,w=im.shape[:2];x=np.clip(uv[:,:,0]*(w-1),0,w-1);y=np.clip((1-uv[:,:,1])*(h-1),0,h-1);x0=x.astype(int);y0=y.astype(int);x1=np.minimum(x0+1,w-1);y1=np.minimum(y0+1,h-1);tx=x-x0;ty=y-y0;out=im[y0,x0]*(1-tx[:,:,None])*(1-ty[:,:,None])+im[y0,x1]*tx[:,:,None]*(1-ty[:,:,None])+im[y1,x0]*(1-tx[:,:,None])*ty[:,:,None]+im[y1,x1]*tx[:,:,None]*ty[:,:,None];Image.fromarray(np.clip(out,0,255).astype('uint8')).save(D/'FoundationReturn_MatchedStone.png')
# Broad source-surface relief, not added procedural noise.
sm=np.array(Image.fromarray(depth).filter(ImageFilter.GaussianBlur(1.8))) if False else depth.copy()
# Finite differences with conservative amplitude and source-world texture scale.
gy,gx=np.gradient(sm,.65/(sm.shape[0]-1),1.1/(sm.shape[1]-1));normal=np.dstack([-gx,gy,np.ones_like(gx)]);normal/=np.linalg.norm(normal,axis=2)[:,:,None];Image.fromarray(np.clip((normal*.5+.5)*255,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6)).save(D/'FoundationReturn_Normal.png')
print('matched stone texture saved')
