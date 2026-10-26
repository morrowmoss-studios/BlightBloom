import bpy,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow12.blend'))
# The floor is y=.203 and the installation pivot y=.2: use local .003 as contact plane.
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith('Stepped foot') or o.name=='CM_SW12_MedicineCabinet'):
  for v in o.data.vertices:
   if v.co.z<.041:v.co.z=.003+(v.co.z-.04)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow12.blend'))
g=bpy.data.objects['CM_SW12_MedicineCabinet'];bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow12/Models/CM_SW12_MedicineCabinet.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
