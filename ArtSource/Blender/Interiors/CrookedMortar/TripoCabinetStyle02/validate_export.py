import bpy,json,hashlib,shutil
from pathlib import Path
import numpy as np
D=Path(__file__).resolve().parent;baseline=D.parent/'TripoCabinetRecovery01/CabinetB/CabinetB.blend';expected=json.loads((D/'BuildReport.json').read_text())
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==expected['base_sha256']
def sig(o):
 m=o.data;co=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',co);uv=np.empty(len(m.uv_layers.active.data)*2,dtype=np.float32);m.uv_layers.active.data.foreach_get('uv',uv)
 return {'coordinates_sha256':hashlib.sha256(co.tobytes()).hexdigest(),'uv_sha256':hashlib.sha256(uv.tobytes()).hexdigest(),'triangles':len(m.polygons),'dimensions_m':list(o.dimensions),'finite_geometry':bool(np.isfinite(co).all()),'finite_uv':bool(np.isfinite(uv).all())}
bpy.ops.wm.open_mainfile(filepath=str(baseline));before=sig(bpy.data.objects['CabinetB_Optimized'])
bpy.ops.wm.open_mainfile(filepath=str(D/'CM_BotanicalCabinet_Style02.blend'));o=bpy.data.objects['CM_BotanicalCabinet_Style02'];after=sig(o);assert before['coordinates_sha256']==after['coordinates_sha256'];assert before['uv_sha256']==after['uv_sha256']
# Explicit external normal source for transparent Unity material setup and native FBX interchange.
shutil.copy2(D.parent/'TripoCabinetRecovery01/Textures/rustic_wooden_cabinet_3d_model_normal.png',D/'Textures/CM_Cabinet_Original_Normal.png')
for im in bpy.data.images:
 if im.name=='CM_Cabinet_Style02_BaseColor':
  im.unpack(method='REMOVE');im.filepath=str(D/'Textures/CM_Cabinet_Style02_BaseColor.png');im.reload();im.pack()
 if '_normal' in im.name:im.filepath=str(D/'Textures/CM_Cabinet_Original_Normal.png')
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_BotanicalCabinet_Style02.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(D/'Exports/CM_BotanicalCabinet_Style02.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.ops.export_scene.fbx(filepath=str(D/'Exports/CM_BotanicalCabinet_Style02.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='COPY',embed_textures=True)
r={'baseline_unchanged':True,'before':before,'styled':after,'geometry_identical':True,'uvs_identical':True}
for fmt in ['glb','fbx']:
 bpy.ops.wm.read_factory_settings(use_empty=True);p=str(D/'Exports'/('CM_BotanicalCabinet_Style02.'+fmt))
 if fmt=='glb':bpy.ops.import_scene.gltf(filepath=p)
 else:bpy.ops.import_scene.fbx(filepath=p)
 obs=[x for x in bpy.context.scene.objects if x.type=='MESH'];r[fmt]={'meshes':len(obs),'triangles':sum(sum(len(f.vertices)-2 for f in x.data.polygons) for x in obs),'dimensions_m':[list(x.dimensions) for x in obs],'materials':[m.name for x in obs for m in x.data.materials],'images':[{'name':i.name,'size':list(i.size)} for i in bpy.data.images if i.type=='IMAGE']}
(D/'Validation.json').write_text(json.dumps(r,indent=2));print('VALIDATED',json.dumps(r),flush=True)
