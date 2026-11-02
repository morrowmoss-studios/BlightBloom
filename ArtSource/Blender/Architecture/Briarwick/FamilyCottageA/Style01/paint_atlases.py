"""Project-owned registered atlas derivatives; originals are read-only.
Broad palette painting, restrained retained grain, geometry-registered slate courses.
Roughness is inverted into URP Lit smoothness alpha; colour maps stay sRGB.
"""
from pathlib import Path
import json, math, sys
import numpy as np
from PIL import Image, ImageFilter
ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).parent
OUT=ROOT/'Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageA/Style01/Textures'
OUT.mkdir(parents=True,exist_ok=True)
N=2048
materials=json.loads((HERE/'SourceMaterials.json').read_text())
meshes=json.loads((HERE/'SourceMeshReadOnly.json').read_text())
def load(path):return Image.open(ROOT/path).convert('RGB').resize((N,N),Image.Resampling.LANCZOS)
def arr(im):return np.asarray(im,dtype=np.float32)/255
def blur(im,r):return arr(im.filter(ImageFilter.GaussianBlur(r)))
def colour(a,b,t):return np.array(a,dtype=np.float32)[None,None,:]*(1-t[:,:,None])+np.array(b,dtype=np.float32)[None,None,:]*t[:,:,None]
def save(rgb,path):Image.fromarray(np.uint8(np.clip(rgb,0,1)*255)).save(path)
roofpaint=np.zeros((N,N,3),dtype=np.float32);roofmask=np.zeros((N,N),dtype=bool)
for m in meshes:
 for slot,role in enumerate(m['materials']):
  if role!='roof':continue
  V=np.array(m['vertices']);U=np.array(m['uv']);T=np.array(m['submeshes'][slot]).reshape(-1,3)
  for face in T:
   uv=U[face]*[N-1,-(N-1)]+[0,N-1];v=V[face]
   lo=np.maximum(np.floor(uv.min(0)).astype(int),0);hi=np.minimum(np.ceil(uv.max(0)).astype(int),N-1)
   if np.any(hi<=lo):continue
   yy,xx=np.mgrid[lo[1]:hi[1]+1,lo[0]:hi[0]+1];A=uv[1]-uv[0];B=uv[2]-uv[0];den=A[0]*B[1]-A[1]*B[0]
   if abs(den)<1e-8:continue
   X=xx-uv[0,0];Y=yy-uv[0,1];a=(X*B[1]-Y*B[0])/den;b=(A[0]*Y-A[1]*X)/den
   inside=(a>=0)&(b>=0)&(a+b<=1);patch=roofmask[lo[1]:hi[1]+1,lo[0]:hi[0]+1];inside&=~patch
   p=v[0]+a[:,:,None]*(v[1]-v[0])+b[:,:,None]*(v[2]-v[0])
   normal=np.cross(v[1]-v[0],v[2]-v[0])
   along=p[:,:,0] if abs(normal[2])>abs(normal[0]) else p[:,:,2]
   # A restrained palette per broad slate. Course lines follow actual surface height,
   # not atlas X/Y, so rotated islands retain the same physical tile scale.
   h=p[:,:,1]+.007*np.sin(along*9)+.003*np.sin(along*21)
   row=np.floor(h/.17);phase=h/.17-row
   x=along/.31+.5*np.mod(row,2);col=np.floor(x);fx=x-col
   variation=.5+.5*np.sin(col*2.39996+row*1.732)
   t=np.clip(.40+.20*variation+.10*np.sin(along*1.7+h*2.3),0,1)
   rgb=colour([.23,.29,.32],[.43,.49,.50],t)
   seam=np.exp(-phase*28)*.035+np.exp(-fx*38)*.012
   lip=np.exp(-((phase-.91)/.065)**2)*.024
   rgb+=(-seam+lip)[:,:,None]
   dst=roofpaint[lo[1]:hi[1]+1,lo[0]:hi[0]+1];dst[inside]=rgb[inside];patch[inside]=True
manifest=[]
roles=set(sys.argv[1:])
prior=json.loads((HERE/'PaintManifest.json').read_text()) if (HERE/'PaintManifest.json').exists() else []
for m in materials:
 key=m['name']
 if key in ['firewood','floor','interior_roof']:continue
 if roles and key not in roles:
  manifest.append(next(p for p in prior if p['sourceRole']==key));continue
 props={t['property']:t['path'] for t in m['textures']}
 source=load(props['_BaseMap']);src=arr(source);med=blur(source,2.0);broad=blur(source,16)
 lum=src@np.array([.2126,.7152,.0722]);L=med@np.array([.2126,.7152,.0722]);B=broad@np.array([.2126,.7152,.0722]);detail=lum-L
 if key.startswith('wood') or key=='doors':
  # Three tonal paints, preserving source grain orientation and island-specific wear.
  t=np.clip((.65*L+.35*B-.12)/.65,0,1)
  dark=np.array([.18,.116,.077]);mid=np.array([.355,.235,.151]);light=np.array([.59,.438,.284])
  if key=='doors':mid+=np.array([.025,.018,.013]);light+=.025
  rgb=colour(dark,mid,np.minimum(t*2,1));rgb=rgb*(1-np.maximum(t-.5,0)[:,:,None]*2)+light[None,None,:]*np.maximum(t-.5,0)[:,:,None]*2
  # Broad warm/cool brush variation comes from existing differently aged boards.
  warm=np.clip((B-.42)*.14,-.028,.028);rgb+=warm[:,:,None]*np.array([1,.15,-.55]);rgb+=detail[:,:,None]*.22
 elif key=='concrete':
  t=np.clip(.52+(B-.5)*.90+(L-B)*.35,0,1)
  rgb=colour([.65,.59,.47],[.96,.91,.79],t)
  rgb+=detail[:,:,None]*.075
 elif key=='rock2':
  t=np.clip(.43+(L-.42)*.77,0,1);rgb=colour([.36,.34,.291],[.71,.669,.569],t)
  rgb+=detail[:,:,None]*.17
 elif key=='roof':
  rgb=colour([.28,.32,.33],[.43,.46,.44],np.clip(L,0,1))
  rgb[roofmask]=roofpaint[roofmask]
  rgb+=(L-B)[:,:,None]*.03+detail[:,:,None]*.015
 elif key=='glass':
  t=np.clip(.4+L*.7,0,1);rgb=colour([.16,.21,.19],[.38,.43,.37],t)
 elif key=='metals':
  rgb=colour([.115,.115,.102],[.335,.316,.253],np.clip(L*.85,0,1))
 else:raise ValueError(key)
 base=OUT/f'BW_Cottage01_{key}_Painted.png';save(rgb,base)
 rough=arr(load(props['_SpecGlossMap']))[:,:,0]
 if key=='glass':smooth=np.clip(.36+(1-rough)*.13,.36,.49);metal=np.zeros_like(smooth)
 elif key=='metals':smooth=np.clip(.13+(1-rough)*.15,.13,.28);metal=np.full_like(smooth,.65)
 else:
  baseSmooth={'roof':.12,'concrete':.07,'rock2':.10}.get(key,.14)
  smooth=np.clip(baseSmooth+(1-rough)*.11,baseSmooth,baseSmooth+.11);metal=np.zeros_like(smooth)
 packed=np.zeros((N,N,4),dtype=np.float32);packed[:,:,0]=metal;packed[:,:,3]=smooth
 packedPath=OUT/f'BW_Cottage01_{key}_MetallicSmoothness.png';Image.fromarray(np.uint8(packed*255)).save(packedPath)
 manifest.append({'sourceRole':key,'baseMap':str(base.relative_to(ROOT)),'metallicSmoothness':str(packedPath.relative_to(ROOT)),'normal':props.get('_BumpMap'),'occlusion':props.get('_OcclusionMap'),'normalScale':{'roof':.12,'concrete':.22,'rock2':.38,'glass':.08}.get(key,.42),'smoothnessRange':[float(smooth.min()),float(smooth.max())],'normalReadOnlySource':True})
(HERE/'PaintManifest.json').write_text(json.dumps(manifest,indent=2))
print('PAINTED_ATLASES',len(manifest),'resolution',N,'roofRegisteredPixels',int(roofmask.sum()))
