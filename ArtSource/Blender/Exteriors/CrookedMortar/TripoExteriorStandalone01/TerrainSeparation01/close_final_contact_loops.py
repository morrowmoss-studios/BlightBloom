import bpy,bmesh,numpy as np,json,hashlib
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;o=bpy.data.objects['House_Standalone01'];me=o.data;m=bpy.data.objects['House_Optimized'].data;report=json.loads((D/'FinalValidation.json').read_text());assert report['new_open_boundary_edges']>0
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();fid=bm.faces.layers.int['source_face_id'];sid=bm.verts.layers.int['source_vertex_id'];edges=[bm.edges.get(tuple(bm.verts[i] for i in r['vertices'])) for r in report['new_open_edges']];assert all(e is not None for e in edges)
# Include the inherited source-open edges that complete these tiny contact loops.
allboundary={e for e in bm.edges if len(e.link_faces)==1};seen=set();groups=[]
for seed in edges:
 if seed in seen:continue
 stack=[seed];group=[];seen.add(seed)
 while stack:
  e=stack.pop();group.append(e)
  for v in e.verts:
   for n in v.link_edges:
    if n in allboundary and n not in seen:seen.add(n);stack.append(n)
 verts=list({v for e in group for v in e.verts});span=np.ptp(np.array([v.co[:] for v in verts]),axis=0)
 assert max(span)<.5 and max(v.co.z for v in verts)<.9,('not local',span)
 assert all(sum(e in group for e in v.link_edges)%2==0 for v in verts)
 groups.append((group,verts))
simplegroups=[]
for group,verts in groups:
 unused=set(group);adj={v:[e for e in v.link_edges if e in unused] for v in verts}
 while unused:
  seed=next(iter(unused));stack=[seed.verts[0]];walk=[]
  while stack:
   v=stack[-1]
   while adj[v] and adj[v][-1] not in unused:adj[v].pop()
   if adj[v]:
    e=adj[v].pop();unused.remove(e);stack.append(e.other_vert(v))
   else:walk.append(stack.pop())
  walk.reverse();simple=[];where={}
  for v in walk:
   if v in where:
    j=where[v];loop=simple[j:]
    if len(loop)>=3:simplegroups.append(([bm.edges.get((a,b)) for a,b in zip(loop,loop[1:]+loop[:1])],loop))
    for w in simple[j+1:]:where.pop(w,None)
    simple=simple[:j+1]
   else:where[v]=len(simple);simple.append(v)
groups=simplegroups
uv=bm.loops.layers.uv.get(me.uv_layers[0].name);slot=me.materials.find('CM_Standalone_LocalFoundationReturns');added=0
for group,verts in groups:
 p=sum((v.co for v in verts),Vector())/len(verts);p.z-=.002;c=bm.verts.new(p);c[sid]=-1
 for e in group:
  l=next(l for l in e.link_faces[0].loops if l.edge==e);a,b=l.vert,l.link_loop_next.vert;face=bm.faces.new([b,a,c]);face[fid]=-1;face.material_index=slot;added+=1
  for loop in face.loops:loop[uv].uv=(loop.vert.co.x/1.1,loop.vert.co.y/.65)
bm.normal_update();bm.to_mesh(me);bm.free();me.update();A=np.load(D/'Topology.npz');tri=A['tri'];nv=len(A['co']);ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3);normal=[]
for p in me.polygons:
 i=int(ids[p.index])
 if i>=0:
  for vi in p.vertices:normal.append(norm[i,int(np.where(tri[i]==vs[vi])[0][0])].tolist())
 else:normal.extend([p.normal[:]]*len(p.vertices))
me.normals_split_custom_set(normal)
# Recheck every final exposed boundary against inherited source edges.
e=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);kk,cc=np.unique(e.min(1).astype('int64')*nv+e.max(1),return_counts=True);oldopen=set(kk[cc==1].tolist());counts={}
for p in me.polygons:
 for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):key=tuple(sorted((a,b)));counts[key]=counts.get(key,0)+1
newopen=[]
for (a,b),n in counts.items():
 if n==1:
  x,y=int(vs[a]),int(vs[b])
  if min(x,y)<0 or min(x,y)*nv+max(x,y) not in oldopen:newopen.append([a,b])
assert not newopen,newopen
report['new_open_boundary_edges']=0;report['new_open_edges']=[];report['new_closure_triangles']=int((ids<0).sum());report['final_body_triangles']=len(me.polygons);report['final_total_triangles']=len(me.polygons)+report['other_render_triangles'];report['final_toe_closure']={'local_contact_loops':len(groups),'max_span_m':.5,'added_center_vertices':len(groups),'added_triangles':added};report['new_degenerate_closure_triangles']=sum(p.area<1e-10 for p in me.polygons if ids[p.index]<0)
(D/'FinalValidation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(f));print('FINAL_BOUNDARY_OK',report['final_total_triangles'],flush=True)
