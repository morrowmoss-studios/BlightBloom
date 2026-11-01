import numpy as np,json,collections
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];nv=len(co);v=np.load(D/'TracedBoundaryVertices.npy');ct=co[tri].mean(1);n=np.cross(co[tri[:,1]]-co[tri[:,0]],co[tri[:,2]]-co[tri[:,0]]);n/=np.maximum(1e-12,np.linalg.norm(n,axis=1))[:,None];barrier={int(min(a,b))*nv+int(max(a,b)) for a,b in zip(v,np.roll(v,-1))};byedge={};adj=[[] for _ in tri]
for f,t in enumerate(tri):
 for a,b in zip(t,np.roll(t,-1)):
  key=int(min(a,b))*nv+int(max(a,b))
  if key in byedge:
   g=byedge[key]
   if key not in barrier:adj[f].append(g);adj[g].append(f)
  else:byedge[key]=f
seed=int(np.argmin(ct[:,2]));bottom=set([seed]);stack=[seed]
while stack:
 f=stack.pop()
 for g in adj[f]:
  if g not in bottom and n[g,2]<-.55:bottom.add(g);stack.append(g)
print('bottom',len(bottom),'bounds',ct[list(bottom)].min(0),ct[list(bottom)].max(0),flush=True)
# Analyze only: no deletion mask accepted without viewing the corresponding faces.
seen=np.zeros(len(tri),bool);seen[list(bottom)]=True;parts=[]
for f in range(len(tri)):
 if seen[f]:continue
 component=[];stack=[f];seen[f]=True
 while stack:
  g=stack.pop();component.append(g)
  for h in adj[g]:
   if not seen[h]:seen[h]=True;stack.append(h)
 if len(component)>20:
  a=np.array(component);parts.append(a);print('region',len(parts)-1,len(a),ct[a].min(0),ct[a].max(0),flush=True)
np.save(D/'UndersideInspectionFaces.npy',np.array(sorted(bottom)))
for i,a in enumerate(parts):np.save(D/f'Region_{i:02d}.npy',a)
