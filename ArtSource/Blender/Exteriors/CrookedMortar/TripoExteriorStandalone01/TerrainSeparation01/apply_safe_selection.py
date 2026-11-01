"""Apply one reviewed face-removal section to a new candidate; immutable source remains in file."""
import bpy,numpy as np,json,hashlib,sys
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;stage=int(sys.argv[sys.argv.index('--')+1]);prev=D/'CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend';bpy.ops.wm.open_mainfile(filepath=str(prev));s=bpy.context.scene;cam=s.camera
for c in s.view_layers[0].layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=True
source=bpy.data.objects['House_Optimized'];m=source.data
code=(D.parent/'BoundaryMapping01/create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);original_hash=mesh_hash(source)
for o in list(bpy.data.objects):
 if o.name.startswith('House_Standalone01'):
  data=o.data;bpy.data.objects.remove(o,do_unlink=True)
  if data.users==0:bpy.data.meshes.remove(data)
col=bpy.data.collections.get('STANDALONE_WORKING_CANDIDATE')
if col is None:col=bpy.data.collections.new('STANDALONE_WORKING_CANDIDATE');s.collection.children.link(col)
A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];labels=np.load(D/'RemovalSectionLabels.npy');remove=(labels>0)&(labels<=stage);ids=np.where(~remove)[0];kept=tri[ids];used,inv=np.unique(kept,return_inverse=True)
new=bpy.data.meshes.new(f'StandaloneSectionStage{stage:02d}');new.from_pydata(co[used].tolist(),[],inv.reshape(-1,3).tolist());new.update()
for material in m.materials:new.materials.append(material)
for uv in m.uv_layers:
 a=np.empty(len(m.loops)*2,np.float32);uv.data.foreach_get('uv',a);uvnew=new.uv_layers.new(name=uv.name);uvnew.data.foreach_set('uv',a.reshape(-1,3,2)[ids].ravel())
mi=np.empty(len(m.polygons),np.int32);m.polygons.foreach_get('material_index',mi);new.polygons.foreach_set('material_index',mi[ids]);smooth=np.empty(len(m.polygons),bool);m.polygons.foreach_get('use_smooth',smooth);new.polygons.foreach_set('use_smooth',smooth[ids]);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);new.normals_split_custom_set(norm.reshape(-1,3,3)[ids].reshape(-1,3).tolist())
attr=new.attributes.new('source_face_id','INT','FACE');attr.data.foreach_set('value',ids);attr=new.attributes.new('source_vertex_id','INT','POINT');attr.data.foreach_set('value',used)
o=bpy.data.objects.new('House_Standalone01',new);col.objects.link(o);o.matrix_world=source.matrix_world.copy();o['source_body_unchanged']=True;o['stage']=stage;o['note']='Only selected original terrain faces omitted; retained face coordinates, corner UVs/materials/normals copied.'
source.hide_render=True;source.hide_set(True)
s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.cycles.samples=12;s.cycles.use_denoising=True;s.render.film_transparent=False;s.render.image_settings.file_format='PNG'
views={1:[('Front',(0,-22,4.6),(0,-3.6,1),11.5),('PorchRight',(9,-14,3),(1.9,-4.9,.8),4.4),('PorchLeft',(-9,-14,3),(-2,-4.9,.8),4.4)],2:[('Right',(22,0,4.8),(1,0,1),17),('RockIvyRight',(14,-6,2.5),(2.9,-2.5,.8),4.8),('PlanterRight',(14,4,3),(2.8,3.5,.9),5.2)],3:[('Rear',(0,22,4.6),(0,4,1),11.5)],4:[('Left',(-22,0,4.8),(-1,0,1),17),('RockIvyLeft',(-14,-6,2.5),(-2.8,-2.5,.8),4.8),('PlanterLeft',(-14,4,3),(-2.9,3.5,.9),5.2)],5:[('Underside',(12,-18,-14),(0,0,.6),19),('Overview',(16,-24,15),(0,0,4.5),21)]}
assert mesh_hash(source)==original_hash
# Retained corners/UVs copied from immutable source; confirm exact float data.
validation={'stage':stage,'removed_faces_cumulative':int(remove.sum()),'kept_body_triangles':len(ids),'source_mesh_hash_unchanged':True,'source_hash':original_hash,'retained_vertex_coordinates_exact':bool(np.array_equal(np.array([v.co[:] for v in new.vertices],np.float32),co[used].astype(np.float32))),'retained_uvs_exact':True,'other_assets_edited':False}
for a,b in zip(m.uv_layers,new.uv_layers):
 aa=np.empty(len(m.loops)*2,np.float32);a.data.foreach_get('uv',aa);bb=np.empty(len(new.loops)*2,np.float32);b.data.foreach_get('uv',bb);validation['retained_uvs_exact'] &= bool(np.array_equal(aa.reshape(-1,3,2)[ids].ravel(),bb))
assert validation['retained_vertex_coordinates_exact'] and validation['retained_uvs_exact'];(D/'SafeSelectionValidation.json').write_text(json.dumps(validation,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'SafeSeparated_UNCAPPED.blend'));print('STAGE_SAVED',json.dumps(validation),flush=True)
