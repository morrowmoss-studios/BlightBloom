from pathlib import Path
import bpy, json, sys
from mathutils import Vector, Matrix
import math
if not bpy.app.background:
 raise RuntimeError('This disposable calibration script must run in a separate background Blender process.')
out=Path(sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else '/private/tmp/blightbloom-pipeline-validation').resolve()
project=Path(__file__).resolve().parents[3]
if out==project or project in out.parents:
 raise RuntimeError('Calibration output must remain outside the Unity project.')
out.mkdir(parents=True,exist_ok=True)
for obj in list(bpy.data.objects): bpy.data.objects.remove(obj,do_unlink=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1.0;scene.unit_settings.length_unit='METERS'
def box(name,location,dimensions):
 bpy.ops.mesh.primitive_cube_add(size=1,location=location)
 obj=bpy.context.object;obj.name=name;obj.dimensions=dimensions
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 mod=obj.modifiers.new('Explicit triangulation','TRIANGULATE');bpy.ops.object.modifier_apply(modifier=mod.name)
 return obj
box('Body_1mWide_2mHigh_0p5mDeep',(0,0,1),(1,.5,2))
box('Right_BlenderPosX',(1.5,0,.1),(.2,.2,.2))
box('Forward_BlenderPosY',(0,1.5,.1),(.2,.2,.2))
box('Up_BlenderPosZ',(0,0,2.8),(.2,.2,.2))
def summary():
 result={}
 for obj in sorted(bpy.context.scene.objects,key=lambda o:o.name):
  if obj.type!='MESH':continue
  verts=[obj.matrix_world@v.co for v in obj.data.vertices]
  result[obj.name]={'location':list(obj.location),'rotation':list(obj.rotation_euler),'scale':list(obj.scale),'world_min':[min(v[i] for v in verts) for i in range(3)],'world_max':[max(v[i] for v in verts) for i in range(3)],'dimensions':list(obj.dimensions),'vertices':len(obj.data.vertices),'triangles':len(obj.data.polygons),'uv_layers':len(obj.data.uv_layers)}
 return result
report={'version':bpy.app.version_string,'source':summary(),'authoring_convention':'metres; +X right, +Y forward, +Z up; source origin at body feet'}
bpy.ops.wm.save_as_mainfile(filepath=str(out/'PipelineProbe.blend'))
bpy.ops.object.select_all(action='SELECT')
# Explicit static FBX coordinate conversion; source .blend remains untouched.
# This exporter/importer combination maps Blender X/Y to Unity -X/-Z.
# Rotate the disposable export copy 180 degrees around Blender Z to retain +X right/+Y forward.
backups=[(obj,obj.data.copy(),obj.matrix_world.copy()) for obj in bpy.context.selected_objects if obj.type=='MESH']
conversion=Matrix.Rotation(math.pi,4,'Z')
for obj,mesh,matrix in backups:obj.matrix_world=conversion@matrix
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
report['fbx_coordinate_conversion']='180 degrees around Blender Z, export copy only; source +X right/+Y forward/+Z up maps to Unity +X/+Z/+Y'
report['fbx_export']=list(bpy.ops.export_scene.fbx(filepath=str(out/'PipelineProbe.fbx'),use_selection=True,object_types={'MESH'},global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False))
for obj,mesh,matrix in backups:obj.data=mesh;obj.matrix_world=matrix
bpy.context.view_layer.update()
report['gltf_export']=list(bpy.ops.export_scene.gltf(filepath=str(out/'PipelineProbe.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True,export_materials='NONE',export_animations=False))
for kind in ['fbx','glb']:
 for obj in list(bpy.data.objects):bpy.data.objects.remove(obj,do_unlink=True)
 if kind=='fbx':bpy.ops.import_scene.fbx(filepath=str(out/'PipelineProbe.fbx'))
 else:bpy.ops.import_scene.gltf(filepath=str(out/'PipelineProbe.glb'))
 report[kind+'_blender_roundtrip']=summary()
(out/'export_report.json').write_text(json.dumps(report,indent=2))
print('PIPELINE_REPORT',json.dumps(report))
