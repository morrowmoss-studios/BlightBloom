import bpy,bmesh,numpy as np,json,collections,hashlib
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(D/'SafeSeparated_CLOSURES.blend'));s=bpy.context.scene;o=bpy.data.objects['House_Standalone01'];source=bpy.data.objects['House_Optimized'];me=o.data;m=source.data
A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];nv=len(co);code=(D.parent/'BoundaryMapping01/create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);source_hash=mesh_hash(source)
parts=json.loads((D/'FragmentInspection.json').read_text());fragment_ids=set(f for part in parts if (part['max'][2]<.30 or (part['max'][2]<.9 and part['count']<100)) for f in part['faces']);foreground=set(np.load(D/'InspectedForegroundGroundFragmentFaces.npy').tolist())
bm=bmesh.new();bm.from_mesh(me);sid=bm.verts.layers.int.get('source_vertex_id');fid=bm.faces.layers.int.get('source_face_id');remove=set()
# Remove inspected detached low terrain chips, preserving the source's separate upper 135-triangle feature.
seen=set()
for face in bm.faces:
 if face in seen:continue
 component=[];stack=[face];seen.add(face)
 while stack:
  a=stack.pop();component.append(a)
  for v in a.verts:
   for b in v.link_faces:
    if b not in seen:seen.add(b);stack.append(b)
 ids={a[fid] for a in component if a[fid]>=0}
 if ids & fragment_ids and len(component)<800:remove.update(component)
# Specific already-inspected foreground path fragments; all lie beyond the lowest front step.
remove.update(a for a in bm.faces if a[fid] in foreground)
remove.update(a for a in bm.faces if a[fid]<0 and any(v.co.y < -5.75 and v.co.z < .9 for v in a.verts))
removed_source=sorted({a[fid] for a in remove if a[fid]>=0});removed_caps=sum(a[fid]<0 for a in remove);bmesh.ops.delete(bm,geom=list(remove),context='FACES');bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
# A few residual triangles were open-sided retained terrain flakes, not true foundation holes.
# The per-section report locates these before removal; do not duplicate a face over itself.
flakes=[a for a in bm.faces if len(a.verts)==3 and all(len(e.link_faces)==1 for e in a.edges) and a.calc_center_median().z<.7]
removed_source+= [a[fid] for a in flakes if a[fid]>=0];bmesh.ops.delete(bm,geom=flakes,context='FACES')
# Fill any small cut holes introduced by this local fragment cleanup only.
all_edges=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);keys=all_edges.min(1).astype('int64')*nv+all_edges.max(1);kk,cc=np.unique(keys,return_counts=True);old_open=set(kk[cc==1].tolist());boundary=[]
for e in bm.edges:
 if len(e.link_faces)==1:
  a,b=[v[sid] for v in e.verts]
  if min(a,b)<0 or min(a,b)*nv+max(a,b) not in old_open:boundary.append(e)
res=bmesh.ops.holes_fill(bm,edges=boundary,sides=32)
for a in res['faces']:a[fid]=-1
bmesh.ops.triangulate(bm,faces=res['faces']);bm.normal_update()
# Dedicated source-reprojected material on NEW return/underside faces only.
mat=bpy.data.materials.new('CM_Standalone_LocalFoundationReturns');mat.use_nodes=True;n=mat.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.87
image=bpy.data.images.load(str(D/'FoundationReturn_MatchedStone.png'),check_existing=True);image.pack();tex=n.new('ShaderNodeTexImage');tex.image=image;mat.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
normal=bpy.data.images.load(str(D/'FoundationReturn_Normal.png'),check_existing=True);normal.colorspace_settings.name='Non-Color';normal.pack();nt=n.new('ShaderNodeTexImage');nt.image=normal;nm=n.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.18;mat.node_tree.links.new(nt.outputs['Color'],nm.inputs['Color']);mat.node_tree.links.new(nm.outputs['Normal'],p.inputs['Normal']);me.materials.append(mat);slot=len(me.materials)-1;uv=bm.loops.layers.uv.get(me.uv_layers[0].name)
new_return_count=0
for a in bm.faces:
 if a[fid]>=0:continue
 a.material_index=slot;new_return_count+=1;a.normal_update();center=a.calc_center_median()
 for l in a.loops:
  v=l.vert.co
  if abs(a.normal.z)<.65:
   # Continuous side-wall alignment across all triangles in each short repair strip.
   u=(v.y+3.85)/1.25 if center.y<0 else v.y/1.1
   vv=(v.z-.52)/.65
  else:u=v.x/1.1;vv=v.y/.65
  l[uv].uv=(u,vv)
# Remove only orphaned vertices/edges left by the approved face deletions.
loose=[v for v in bm.verts if not v.link_faces]
if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
# Preserve exact source surface normals after the local BMesh operations.
bm.to_mesh(me);bm.free();me.update();ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3);normals=[]
for a in me.polygons:
 i=ids[a.index]
 if i>=0:
  for v in a.vertices:normals.append(norm[i,int(np.where(tri[i]==vs[v])[0][0])].tolist())
 else:normals.extend([a.normal[:]]*len(a.vertices))
me.normals_split_custom_set(normals);assert mesh_hash(source)==source_hash
(D/'FragmentCleanup.json').write_text(json.dumps(dict(removed_source_faces=sorted(set(removed_source)),removed_cap_faces=removed_caps,new_return_faces=new_return_count,protected_separate_upper_feature_retained=True),indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(f));print('FINISH_REPAIRS',len(set(removed_source)),new_return_count,flush=True)
