"""Face-level edge paths through individually inspected contact anchors. No Blender mesh edits.
Local corridors guide shortest-edge tracing only; there is NO height, box or Boolean deletion mask.
"""
import numpy as np,json,heapq,collections,time
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];ed=A['edges'];nv=len(co)
P=json.loads((D.parent/'BoundaryMapping02/ManualCloseupPicks.json').read_text());Q=json.loads((D/'LocalContactFacePicks.json').read_text());O=json.loads((D.parent/'BoundaryMapping01/ManualElevationPicks.json').read_text())
def pts(rows):return [r['point'] for r in rows if r['point'] is not None]
# Keep front stone returns, follow the inspected hidden-rock contact arch, wrap each side planter.
sections=[('Front',pts(P['PorchLeft'][2:])+pts(O['Front'][3:8])+pts(Q['RightPorchToe'])),
 ('RightFrontRock',pts(Q['RightRockRootContact'])),
 ('RightWall',pts(P['RockIvyRight'][1:])+pts(O['Right'][7:5:-1])+pts(P['PlanterRight'][:1])),
 ('RightPlanters',pts(Q['RightBedToe'])),
 ('RightAnnexRear',pts(P['PlanterRight'][9:])+pts(O['Right'][1::-1])+pts(Q['RearFeet'][:3])),
 ('Rear',pts(P['Rear'][2:7])+pts(Q['RearFeet'][4:])),
 ('LeftAnnexRear',pts(O['Left'][13:10:-1])+pts(P['PlanterLeft'][:4])),
 ('LeftPlanters',pts(Q['LeftBedToe'])),
 ('LeftWall',pts(O['Left'][6:3:-1])+pts(P['RockIvyLeft'][:4])),
 ('LeftFrontRock',pts(Q['LeftRockContact']))]
anchors=[]
for name,ps in sections:
 for p in ps:
  if not anchors or np.linalg.norm(np.array(p)-anchors[-1]['point'])>.025:anchors.append(dict(section=name,point=p))
anchors.append(dict(section='LeftPorchReturn',point=anchors[0]['point']))
# Compressed adjacency, with immutable source vertex IDs.
e=np.vstack([ed,ed[:,::-1]]);order=np.argsort(e[:,0],kind='stable');e=e[order];offset=np.searchsorted(e[:,0],np.arange(nv+1));neigh=e[:,1];length=np.linalg.norm(co[e[:,0]]-co[e[:,1]],axis=1)
ids=[int(np.argmin(((co-np.array(a['point']))**2).sum(1))) for a in anchors]
paths=[];loop=[];t=time.time()
for k,(start,goal) in enumerate(zip(ids,ids[1:])):
 if start==goal:continue
 a=co[start];b=co[goal];ab=b-a;t0=np.clip(((co-a)@ab)/max(ab@ab,1e-10),0,1);dist=np.linalg.norm(co-(a+t0[:,None]*ab),axis=1)
 # A narrow local inspection corridor, never a geometry selection operation.
 penalty=1+(dist/.055)**2;allowed=dist<max(.4,np.linalg.norm(ab)*.55)
 heap=[(0.,start)];cost={start:0.};prev={};found=False
 while heap:
  c,v=heapq.heappop(heap)
  if c!=cost[v]:continue
  if v==goal:found=True;break
  lo,hi=offset[v:v+2]
  for j in range(lo,hi):
   w=int(neigh[j])
   if not allowed[w]:continue
   nc=c+length[j]*(penalty[v]+penalty[w])*.5
   if nc<cost.get(w,float('inf')):cost[w]=nc;prev[w]=v;heapq.heappush(heap,(nc,w))
 assert found,('no safe local edge path',k,anchors[k])
 path=[goal]
 while path[-1]!=start:path.append(prev[path[-1]])
 path.reverse();loop+=path[:-1];paths.append(dict(index=k,section=anchors[k+1]['section'],vertices=path,max_distance_from_inspected_span=float(dist[path].max()),length=float(np.linalg.norm(np.diff(co[path],axis=0),axis=1).sum())))
 print('PATH',k,anchors[k+1]['section'],len(path),round(dist[path].max(),3),flush=True)
# Loop erasure removes backtracking at the junction between neighboring traced spans only.
clean=[];where={}
for v in loop:
 if v in where:
  n=where[v]
  for w in clean[n+1:]:where.pop(w,None)
  clean=clean[:n+1]
 else:where[v]=len(clean);clean.append(v)
assert len(clean)>100
barrier={min(a,b)*nv+max(a,b) for a,b in zip(clean,clean[1:]+clean[:1])}
np.save(D/'TracedBoundaryVertices.npy',np.array(clean,np.int32));(D/'EdgePaths.json').write_text(json.dumps(dict(anchors=anchors,paths=paths,closed_boundary_vertices=len(clean)),indent=2))
# Find triangle adjacency; flood only across edges outside the closed traced barrier.
edgefaces={};adj=[[] for _ in tri]
for f,vs in enumerate(tri):
 for a,b in zip(vs,np.roll(vs,-1)):
  key=int(min(a,b))*nv+int(max(a,b))
  if key in edgefaces:
   g=edgefaces[key]
   if key not in barrier:adj[f].append(g);adj[g].append(f)
  else:edgefaces[key]=f
ct=co[tri].mean(1);seed=int(np.argmin(ct[:,2]));seen=np.zeros(len(tri),bool);seen[seed]=True;stack=[seed]
while stack:
 f=stack.pop()
 for g in adj[f]:
  if not seen[g]:seen[g]=True;stack.append(g)
# Safety validation only: tall architecture must never enter the terrain selection.
assert not np.any(seen & (co[tri][:,:,2].min(1)>1.4)),('path leaked into architecture',int(seen.sum()))
assert seen.sum()>1000 and seen.sum()<len(tri)*.3,int(seen.sum())
np.save(D/'TerrainFaceSelection.npy',np.where(seen)[0]);np.save(D/'TracedBoundaryVertices.npy',np.array(clean,np.int32));(D/'EdgePaths.json').write_text(json.dumps(dict(anchors=anchors,paths=paths,closed_boundary_vertices=len(clean),terrain_faces=int(seen.sum()),kept_body_faces=int((~seen).sum()),method='bounded face flood from terrain underside, with manually anchored local mesh-edge barriers; no height/box/Boolean deletion',time_s=time.time()-t),indent=2));print('PLAN_OK',len(clean),int(seen.sum()),len(tri)-int(seen.sum()),flush=True)
