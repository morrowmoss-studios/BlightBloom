import numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];rem=np.load(D/'TerrainFaceSelection.npy');mask=np.ones(len(tri),bool);mask[rem]=False;ids=np.where(mask)[0];t=tri[ids];parent=np.arange(len(co),dtype=np.int32)
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for vs in t:
 a=find(vs[0])
 for v in vs[1:]:
  b=find(v)
  if a!=b:parent[b]=a
root=np.array([find(v) for v in t[:,0]]);parts=[]
for r in np.unique(root):
 fs=ids[root==r];pts=co[tri[fs]].reshape(-1,3);parts.append(dict(count=len(fs),faces=fs.tolist(),min=pts.min(0).tolist(),max=pts.max(0).tolist()))
parts.sort(key=lambda a:-a['count']);(D/'FragmentInspection.json').write_text(json.dumps(parts,indent=2));print('pieces',len(parts))
for i,p in enumerate(parts):
 if i<40:print(i,p['count'],np.round(p['min'],3),np.round(p['max'],3))
