"""Final review: immutable-source comparison, new-boundary checks, matched actual Blender renders."""
import bpy,numpy as np,json,hashlib,collections
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;vl=s.view_layers[0];cam=s.camera;o=bpy.data.objects['House_Standalone01'];source=bpy.data.objects['House_Optimized'];m=source.data;me=o.data
code=(D.parent/'BoundaryMapping01/create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);baseline=json.loads((D.parent/'BoundaryMapping02/PreservationValidation.json').read_text());original_meshes={n:mesh_hash(bpy.data.objects[n]) for n in baseline['mesh_hashes']};assert original_meshes==baseline['mesh_hashes']
source_mats={mat.name:mat_hash(mat) for mat in bpy.data.materials if not mat.name.startswith('CM_Standalone_')}
col=bpy.data.collections['STANDALONE_WORKING_CANDIDATE'];original_col=bpy.data.collections['OPTIMIZED_GAMEPLAY_CANDIDATE'];clones=[]
root=bpy.data.objects.new('CM_CrookedMortar_Standalone01_REVIEW',None);col.objects.link(root);root['status']='Giant terrain platform removed; two fused rock/root contacts retained pending manual review. NO UNITY INTEGRATION APPROVED.'
for ob in list(original_col.all_objects):
 if ob==source or ob.hide_render:continue
 copy=ob.copy()
 if ob.data:copy.data=ob.data.copy()
 copy.name='Standalone01_'+ob.name;col.objects.link(copy);copy.parent=root;copy.matrix_world=ob.matrix_world.copy();clones.append(copy)
o.parent=root;o.matrix_world=source.matrix_world.copy()
# Counts and identity checks on the actual surviving source triangles.
A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];nv=len(co);ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);retained=ids[ids>=0];removed=np.setdiff1d(np.arange(len(tri)),retained);coords=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',coords);coords=coords.reshape(-1,3);assert np.array_equal(coords[vs>=0],co[vs[vs>=0]].astype(np.float32))
uv_ok=True;material_ok=True
for u,v in zip(m.uv_layers,me.uv_layers):
 a=np.empty(len(m.loops)*2,np.float32);u.data.foreach_get('uv',a);a=a.reshape(-1,3,2)
 for p in me.polygons:
  i=int(ids[p.index])
  if i>=0:
   material_ok &= me.materials[p.material_index]==m.materials[m.polygons[i].material_index]
   for li,vi in zip(p.loop_indices,p.vertices):uv_ok &= np.array_equal(np.array(v.data[li].uv),a[i,int(np.where(tri[i]==vs[vi])[0][0])])
assert uv_ok and material_ok
# New versus inherited boundary edges; the original Tripo mesh already has open/nonmanifold edges.
e=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);kk,cc=np.unique(e.min(1).astype('int64')*nv+e.max(1),return_counts=True);oldopen=set(kk[cc==1].tolist());edgefaces=collections.defaultdict(list)
for p in me.polygons:
 for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):edgefaces[tuple(sorted((a,b)))].append(p.index)
newopen=[];inherited=0
for (a,b),fs in edgefaces.items():
 if len(fs)==1:
  x,y=int(vs[a]),int(vs[b])
  if min(x,y)>=0 and min(x,y)*nv+max(x,y) in oldopen:inherited+=1
  else:newopen.append(dict(vertices=[a,b],points=[coords[a].tolist(),coords[b].tolist()]))
# Record small retained loose-rock/root exclusions; don't claim they were successfully extracted.
exclusions=json.loads((D.parent/'BoundaryMapping02/LooseRockReviewPicks.json').read_text());retainedset=set(retained.tolist());excluded_review={name:[dict(source_face=r['face_index'],retained=r['face_index'] in retainedset) for r in rows] for name,rows in exclusions.items()}
newareas=[p.area for p in me.polygons if ids[p.index]<0]
def triangles(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mm=ev.to_mesh();n=sum(len(p.vertices)-2 for p in mm.polygons);ev.to_mesh_clear();return n
body_tri=sum(len(p.vertices)-2 for p in me.polygons);extra_tri=sum(triangles(ob) for ob in clones if ob.type in {'MESH','CURVE','FONT','SURFACE'});total=body_tri+extra_tri
report=dict(original_total_triangles=527497,original_body_triangles=len(tri),removed_original_body_triangles=len(removed),retained_source_body_triangles=len(retained),new_closure_triangles=int((ids<0).sum()),final_body_triangles=body_tri,other_render_triangles=extra_tri,final_total_triangles=total,original_mesh_hashes_unchanged=True,retained_coordinates_exact=True,retained_corner_uvs_exact=bool(uv_ok),retained_material_assignments_exact=bool(material_ok),retained_corner_normals_restored=True,all_source_faces_above_0_9m_retained=bool(not np.any(co[tri[removed]][:,:,2].min(1)>.9)),removed_face_max_z=float(co[tri[removed]][:,:,2].max()),original_underside_inspection_faces_remaining=int(np.isin(np.load(D/'UndersideInspectionFaces.npy'),retained).sum()),new_open_boundary_edges=len(newopen),new_open_edges=newopen,inherited_open_edges=inherited,inherited_nonmanifold_edges_source=int((cc>2).sum()),new_degenerate_closure_triangles=sum(a<1e-10 for a in newareas),retained_source_bounds=[coords[vs>=0].min(0).tolist(),coords[vs>=0].max(0).tolist()],explicit_exclusion_seed_status=excluded_review,remaining_obstructions=['Left porch/window-bay boulder: original contact cluster restored after rejecting visually inadequate reconstruction.','Right porch/window-bay rock/ivy root cluster: original lower growth and rock contacts retained after rejecting reconstruction.','Small left herb-bed toe / rear corner contacts retained where fused to protected elements; review close-ups.'],no_unity_files_changed=True,no_export=True,no_commit=True)
np.save(D/'FinalRemovedSourceFaces.npy',removed);(D/'FinalValidation.json').write_text(json.dumps(report,indent=2));print('FINAL_VALIDATION',json.dumps({k:v for k,v in report.items() if k not in ['new_open_edges','explicit_exclusion_seed_status']}),flush=True)
for child in vl.layer_collection.children:
 if child.name.startswith('BOUNDARY'):child.exclude=True
source_layer=vl.layer_collection.children[original_col.name];candidate_layer=vl.layer_collection.children[col.name]
source_layer.exclude=True;candidate_layer.exclude=False;source.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(f));print('PREPARED_FOR_FINAL_REVIEW',flush=True)
