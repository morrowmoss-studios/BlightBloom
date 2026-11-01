"""Fitted closures of newly exposed boundaries only. Never remesh or move retained source vertices."""
import bpy,bmesh,numpy as np,json,hashlib,collections
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'Stage05.blend'));s=bpy.context.scene;o=bpy.data.objects['House_Standalone01'];source=bpy.data.objects['House_Optimized'];m=source.data;me=o.data
code=(D.parent/'BoundaryMapping01/create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);source_hash=mesh_hash(source)
A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];nv=len(co)
# Original boundary edges must not be silently 'fixed' outside this task.
ed=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);keys=ed.min(1).astype('int64')*nv+ed.max(1);k,c=np.unique(keys,return_counts=True);old_open=set(k[c==1].tolist())
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();sid=bm.verts.layers.int.get('source_vertex_id');fid=bm.faces.layers.int.get('source_face_id');uvlayers=[bm.loops.layers.uv.get(u.name) for u in me.uv_layers]
newedges=[]
for e in bm.edges:
 if len(e.link_faces)==1:
  a,b=[v[sid] for v in e.verts]
  if min(a,b)*nv+max(a,b) not in old_open:newedges.append(e)
# Keep a baseline map of source face identity + winding/UV before closure.
kept_before={f[fid]:tuple(v[sid] for v in f.verts) for f in bm.faces}
# Add only the short exposed returns at the two removed rock contacts.
# Existing edge positions stay fixed; the strips occupy formerly hidden rock-contact cavities.
faces=[];strip_records=[]
for name,xsign,yrange,zmin,base in [('LeftRockReturn',-1,(-3.85,-2.60),.67,.53),('RightRootReturn',1,(-3.90,-2.70),.67,.52)]:
 chosen=[]
 for e in newedges:
  c=(e.verts[0].co+e.verts[1].co)*.5
  if xsign*c.x>2.2 and yrange[0]<c.y<yrange[1] and c.z>zmin:chosen.append(e)
 newverts={}
 for e in chosen:
  a,b=e.verts
  for v in [a,b]:
   if v not in newverts:
    q=bm.verts.new((v.co.x,v.co.y,base));q[sid]=-1;newverts[v]=q
  # Oppose the source face edge winding.
  l=next(l for l in e.link_faces[0].loops if l.edge==e)
  aa,bb=l.vert,l.link_loop_next.vert
  try:
   f=bm.faces.new([bb,aa,newverts[aa],newverts[bb]]);f[fid]=-1;faces.append(f)
  except ValueError:pass
 strip_records.append(dict(name=name,source_edges=len(chosen),new_vertices=len(newverts),base_z=base))
# Recompute only the newly exposed boundary, then split touching loops at their shared vertices.
newedges=[]
for e in bm.edges:
 if len(e.link_faces)==1:
  a,b=[v[sid] for v in e.verts]
  if min(a,b)<0 or min(a,b)*nv+max(a,b) not in old_open:newedges.append(e)
adj=collections.defaultdict(list)
for i,e in enumerate(newedges):
 a,b=e.verts;adj[a].append((b,i));adj[b].append((a,i))
unused=set(range(len(newedges)));cycles=[]
while unused:
 seed=next(iter(unused));start=newedges[seed].verts[0];stack=[start];walk=[]
 while stack:
  v=stack[-1]
  while adj[v] and adj[v][-1][1] not in unused:adj[v].pop()
  if adj[v]:
   w,i=adj[v].pop();unused.remove(i);stack.append(w)
  else:walk.append(stack.pop())
 walk.reverse();simple=[];where={}
 for v in walk:
  if v in where:
   j=where[v];loop=simple[j:]
   if len(loop)>=3:cycles.append(loop)
   for w in simple[j+1:]:where.pop(w,None)
   simple=simple[:j+1]
  else:where[v]=len(simple);simple.append(v)
for loop in cycles:
 edge=bm.edges.get((loop[0],loop[1]))
 if edge is None:continue
 l=next(l for l in edge.link_faces[0].loops if l.edge==edge)
 if l.vert==loop[0]:loop=loop[::-1]
 try:
  f=bm.faces.new(loop);f[fid]=-1;faces.append(f)
 except ValueError:pass
print('FITTED_CLOSURES',len(faces),'cycles',len(cycles),'strips',strip_records,flush=True)
# UV sample reuse from immediate retained neighbors; never touch existing loops.
patches=[]
for index,f in enumerate(faces):
 neighbors=[]
 for e in f.edges:
  neighbors.extend(g for g in e.link_faces if g!=f and g[fid]>=0)
 if not neighbors:continue
 center=f.calc_center_median();neighbor=min(neighbors,key=lambda x:(x.calc_center_median()-center).length);f.material_index=neighbor.material_index;f.smooth=False
 f.normal_update();normal=f.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis];pts=np.array([v.co[:] for v in f.verts]);lo=pts[:,axes].min(0);hi=pts[:,axes].max(0);span=np.maximum(hi-lo,1e-6)
 for layer in uvlayers:
  sample=np.array([l[layer].uv[:] for l in neighbor.loops]);mid=sample.mean(0);extent=np.maximum(np.ptp(sample,axis=0),.00025)
  # Confine new hidden-return UVs to a neighboring atlas patch, rather than sampling unrelated atlas regions.
  for l in f.loops:
   t=(np.array(l.vert.co[:])[axes]-lo)/span;l[layer].uv=mid+(t-.5)*extent*.7
 patches.append(dict(index=index,vertices=len(f.verts),bounds=[pts.min(0).tolist(),pts.max(0).tolist()],material=f.material_index,uv_source_face=neighbor[fid],kind='fitted underside/lower return; no expanded footprint'))
bmesh.ops.triangulate(bm,faces=faces,quad_method='BEAUTY',ngon_method='BEAUTY');bm.normal_update()
# Verify no retained face winding or coordinates was altered by cap operations.
assert kept_before=={f[fid]:tuple(v[sid] for v in f.verts) for f in bm.faces if f[fid]>=0}
remaining=[]
for e in bm.edges:
 if len(e.link_faces)==1:
  a,b=[v[sid] for v in e.verts]
  if min(a,b)<0 or min(a,b)*nv+max(a,b) not in old_open:remaining.append([a,b])
cap_tri=sum(f[fid]<0 for f in bm.faces);bm.to_mesh(me);bm.free();me.update()
# Restore exact original per-corner normals after BMesh, not globally recalculated visible shading.
ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3);allnorm=[]
for p in me.polygons:
 f=int(ids[p.index])
 if f>=0:
  for v in p.vertices:allnorm.append(norm[f,int(np.where(tri[f]==vs[v])[0][0])].tolist())
 else:allnorm.extend([p.normal[:]]*len(p.vertices))
me.normals_split_custom_set(allnorm)
# Reconfirm coordinates and per-corner UVs on retained triangles.
actual=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',actual);assert np.array_equal(actual.reshape(-1,3)[vs>=0],co[vs[vs>=0]].astype(np.float32))
uv_ok=True
for a,b in zip(m.uv_layers,me.uv_layers):
 original=np.empty(len(m.loops)*2,np.float32);a.data.foreach_get('uv',original);original=original.reshape(-1,3,2)
 for p in me.polygons:
  f=int(ids[p.index])
  if f>=0:
   for li,v in zip(p.loop_indices,p.vertices):uv_ok &= np.array_equal(np.array(b.data[li].uv),original[f,int(np.where(tri[f]==vs[v])[0][0])])
assert uv_ok and mesh_hash(source)==source_hash
report=dict(new_cap_triangles=int(cap_tri),closed_loops=len(patches),local_return_strips=strip_records,remaining_new_boundary_edges=len(remaining),remaining_edges_source_ids=remaining,source_mesh_hash_unchanged=True,retained_coordinates_exact=True,retained_corner_uvs_exact=bool(uv_ok),retained_corner_normals_restored=True,patches=patches,uv_limitation='New lower returns reuse neighboring atlas samples. Original visible surfaces/UVs unchanged; new cap texture scale requires visual review.')
(D/'ClosureValidation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_WORKING.blend'));print('CLOSURES',cap_tri,'new openedges',len(remaining),flush=True)
