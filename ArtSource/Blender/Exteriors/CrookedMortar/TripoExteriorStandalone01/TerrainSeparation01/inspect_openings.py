"""Analyze newly exposed edge loops only, without editing geometry."""
import numpy as np,json,collections
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];t=A['tri'];remove=np.load(D/'TerrainFaceSelection.npy');keep=np.ones(len(t),bool);keep[remove]=False;nv=len(co)
def edge_counts(tri):
 e=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);keys=e.min(1).astype('int64')*nv+e.max(1);k,idx,c=np.unique(keys,return_index=True,return_counts=True);return k,e[idx],c
ok,oe,oc=edge_counts(t);nk,ne,nc=edge_counts(t[keep]);origcount=oc[np.searchsorted(ok,nk)];ed=ne[(nc==1)&(origcount>=2)];adj=collections.defaultdict(list)
for a,b in ed:adj[int(a)].append(int(b));adj[int(b)].append(int(a))
seen=set();components=[]
for v in adj:
 if v in seen:continue
 group=[];stack=[v];seen.add(v)
 while stack:
  a=stack.pop();group.append(a)
  for b in adj[a]:
   if b not in seen:seen.add(b);stack.append(b)
 pts=co[group];degrees=collections.Counter(len(adj[v]) for v in group);components.append(dict(vertices=group,count=len(group),degrees=dict(degrees),min=pts.min(0).tolist(),max=pts.max(0).tolist()))
components.sort(key=lambda a:-a['count']);(D/'ExposedBoundaryComponents.json').write_text(json.dumps(components,indent=2));np.save(D/'NewBoundaryEdges.npy',ed)
print('new boundary edges',len(ed),'components',len(components),'existing boundary edges',int((oc==1).sum()),flush=True)
for c in components[:20]:print(c['count'],c['degrees'],np.round(c['min'],3),np.round(c['max'],3))
