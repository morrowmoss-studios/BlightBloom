"""Compute a sculpt scalar field from an explicit binary stencil, never albedo luminance."""
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json
D=Path(__file__).resolve().parent
im=Image.open(D/'CounterStencil.png').convert('L');w,h=im.size
fields=[]
for panel in range(3):
 a=im.crop((round(panel*w/3),0,round((panel+1)*w/3),h)).resize((384,384),Image.Resampling.LANCZOS)
 mask=a.point(lambda p:255 if p>140 else 0);distance=np.zeros((384,384),dtype=np.float32);filled=mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.MinFilter(7));eroded=filled
 for j in range(52):
  distance+=(np.asarray(eroded)>127)
  eroded=eroded.filter(ImageFilter.MinFilter(3))
 # Rounded continuous wood relief with smooth rising edges and cut veins.
 height=.038*(1-np.exp(-distance/10))
 # Veins are shallow incisions in a whole leaf, not full-height trenches splitting it into wires.
 grooves=((np.asarray(filled)>127)&(np.asarray(mask)<128)).astype(np.float32)
 height-=.0032*grooves
 # Numerical sculpt-surface fairing only; the painted albedo is never blurred.
 kernel=np.array([.035,.10,.20,.33,.20,.10,.035],dtype=np.float32);kernel/=kernel.sum()
 for axis in [0,1]:
  pad=np.pad(height,[(3,3) if ax==axis else (0,0) for ax in [0,1]],mode='edge');height=sum(k*np.take(pad,np.arange(384)+j,axis=axis) for j,k in enumerate(kernel))
 height=np.maximum(height,0)
 # Keep panel boundary exactly on the recessed field datum.
 yy,xx=np.mgrid[0:384,0:384];fade=np.clip(np.minimum.reduce([xx,yy,383-xx,383-yy])/14,0,1)
 height*=fade
 fields.append(height)
np.save(D/'SculptFields.npy',np.stack(fields))
(D/'ReliefRecipe.json').write_text(json.dumps({'input':'CounterStencil.png','method':'Silhouette closing separates leaf volumes from shallow incised vein masks; iterative interior distance, rounded inflation and numerical surface fairing. Never use albedo luminance as height.','maxReliefMetres':float(np.max(fields)),'samplesPerPanel':[384,384],'threshold':140},indent=2))
print('SCULPT_FIELDS',np.max(fields))
