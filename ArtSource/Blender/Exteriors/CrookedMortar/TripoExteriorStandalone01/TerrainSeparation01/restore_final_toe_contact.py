"""Restore the original tiny toe contact; repair only generated bottom-cap topology around it."""
import bpy,bmesh,numpy as np,json,collections
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(f));o=bpy.data.objects['House_Standalone01'];me=o.data;m=bpy.data.objects['House_Optimized'].data;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];nv=len(co);center=np.array([1.74,-5.70,.55]);near=np.linalg.norm(co[tri]-center,axis=2).min(1)<.24
bm=bmesh.new();bm.from_mesh(me);sid=bm.verts.layers.int['source_vertex_id'];fid=bm.faces.layers.int['source_face_id'];layers=[bm.loops.layers.uv.get(x.name) for x in me.uv_layers]
remove=[p for p in bm.faces if p[fid]<0 and any((v.co-Vector(center)).length<.4 for v in p.verts)];bmesh.ops.delete(bm,geom=remove,context='FACES');present={p[fid] for p in bm.faces if p[fid]>=0};vmap={v[sid]:v for v in bm.verts if v[sid]>=0};restored=[]
uvsource=[]
for uv in m.uv_layers:
 a=np.empty(len(m.loops)*2,np.float32);uv.data.foreach_get('uv',a);uvsource.append(a.reshape(-1,3,2))
for i in np.where(near)[0]:
 if int(i) in present:continue
 verts=[]
 for j in tri[i]:
  if int(j) not in vmap:v=bm.verts.new(co[j]);v[sid]=int(j);vmap[int(j)]=v
  verts.append(vmap[int(j)])
 try:p=bm.faces.new(verts)
 except ValueError:continue
 p[fid]=int(i);p.material_index=m.polygons[i].material_index;p.smooth=m.polygons[i].use_smooth
 for layer,uv in zip(layers,uvsource):
  for k,l in enumerate(p.loops):l[layer].uv=uv[i,k]
 restored.append(int(i))
# Remove conflicting diagonals in generated caps only; never delete original faces here.
conflicting={p for e in bm.edges if len(e.link_faces)>2 for p in e.link_faces if p[fid]<0}
if conflicting:bmesh.ops.delete(bm,geom=list(conflicting),context='FACES')
# Trace the now-even boundary components touching the restored local contact.
e=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);kk,cc=np.unique(e.min(1).astype('int64')*nv+e.max(1),return_counts=True);oldopen=set(kk[cc==1].tolist());allboundary={e for e in bm.edges if len(e.link_faces)==1};new=[]
for e in allboundary:
 a,b=[v[sid] for v in e.verts]
 if min(a,b)<0 or min(a,b)*nv+max(a,b) not in oldopen:new.append(e)
seen=set();cycles=[]
for seed in new:
 if seed in seen:continue
 group=[];stack=[seed];seen.add(seed)
 while stack:
  e=stack.pop();group.append(e)
  for v in e.verts:
   for q in v.link_edges:
    if q in allboundary and q not in seen:seen.add(q);stack.append(q)
 verts={v for e in group for v in e.verts};assert max(v.co.z for v in verts)<.9
 assert all(sum(e in group for e in v.link_edges)%2==0 for v in verts),'odd boundary remains'
 unused=set(group);adj={v:[e for e in v.link_edges if e in unused] for v in verts}
 while unused:
  edge=next(iter(unused));stack=[edge.verts[0]];walk=[]
  while stack:
   v=stack[-1]
   while adj[v] and adj[v][-1] not in unused:adj[v].pop()
   if adj[v]:e=adj[v].pop();unused.remove(e);stack.append(e.other_vert(v))
   else:walk.append(stack.pop())
  walk.reverse();simple=[];where={}
  for v in walk:
   if v in where:
    j=where[v];loop=simple[j:]
    if len(loop)>=3:cycles.append(loop)
    for w in simple[j+1:]:where.pop(w,None)
    simple=simple[:j+1]
   else:where[v]=len(simple);simple.append(v)
slot=me.materials.find('CM_Standalone_LocalFoundationReturns')
for loop in cycles:
 p=sum((v.co for v in loop),Vector())/len(loop);p.z-=.001;c=bm.verts.new(p);c[sid]=-1
 for a,b in zip(loop,loop[1:]+loop[:1]):
  e=bm.edges.get((a,b));l=next(l for l in e.link_faces[0].loops if l.edge==e);aa,bb=l.vert,l.link_loop_next.vert;p=bm.faces.new([bb,aa,c]);p[fid]=-1;p.material_index=slot
  for l in p.loops:l[layers[0]].uv=(l.vert.co.x/1.1,l.vert.co.y/.65)
bm.normal_update();bm.to_mesh(me);bm.free();me.update();ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3);ns=[]
for p in me.polygons:
 i=int(ids[p.index])
 if i>=0:
  for v in p.vertices:ns.append(norm[i,int(np.where(tri[i]==vs[v])[0][0])].tolist())
 else:ns.extend([p.normal[:]]*len(p.vertices))
me.normals_split_custom_set(ns)
counts={}
for p in me.polygons:
 for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):key=tuple(sorted((a,b)));counts[key]=counts.get(key,0)+1
newopen=[];inherited=0
for (a,b),n in counts.items():
 if n==1:
  x,y=int(vs[a]),int(vs[b])
  if min(x,y)>=0 and min(x,y)*nv+max(x,y) in oldopen:inherited+=1
  else:newopen.append([a,b])
assert not newopen,newopen
r=json.loads((D/'FinalValidation.json').read_text());removed=np.setdiff1d(np.arange(len(tri)),ids[ids>=0]);np.save(D/'FinalRemovedSourceFaces.npy',removed);r.update(removed_original_body_triangles=len(removed),retained_source_body_triangles=int((ids>=0).sum()),new_closure_triangles=int((ids<0).sum()),final_body_triangles=len(me.polygons),final_total_triangles=len(me.polygons)+r['other_render_triangles'],new_open_boundary_edges=0,new_open_edges=[],inherited_open_edges=inherited,new_degenerate_closure_triangles=sum(p.area<1e-10 for p in me.polygons if ids[p.index]<0));r['restored_front_toe_contact_triangles']=len(restored);r['remaining_obstructions'].append('Original front toe-pebble contact and its small fused collar restored rather than forcing a defective cut.');(D/'FinalValidation.json').write_text(json.dumps(r,indent=2));(D/'RestoredToeFaces.json').write_text(json.dumps(restored));bpy.ops.wm.save_as_mainfile(filepath=str(f));print('FINAL_CLOSED',r['final_total_triangles'],len(restored),flush=True)
