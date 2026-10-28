import bpy,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;E=D/'Exports';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));s=bpy.context.scene;groups={c.name:c for c in s.collection.children}
# FBX transport copies: combine sensible groups; eight drawers remain separate modules in source/GLB.
exports=[]
for name,c in groups.items():
 bpy.ops.object.select_all(action='DESELECT');copies=[]
 for o in c.objects:
  if o.type!='MESH':continue
  p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.parent=None;p.matrix_world=Matrix.Identity(4);p.select_set(True);copies.append(p)
 bpy.context.view_layer.objects.active=copies[0]
 if len(copies)>1:bpy.ops.object.join()
 g=bpy.context.object;g.name='CM_MMC01_'+name[3:];s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');exports.append(g)
bpy.ops.object.select_all(action='DESELECT')
for g in exports:g.select_set(True)
bpy.context.view_layer.objects.active=exports[0]
for g in exports:
 bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.object.select_all(action='DESELECT')
for g in exports:g.select_set(True)
bpy.context.view_layer.objects.active=exports[0]
bpy.ops.export_scene.gltf(filepath=str(E/'CM_MasterMedicineCabinet01.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_materials='EXPORT')
bpy.ops.export_scene.fbx(filepath=str(E/'CM_MasterMedicineCabinet01.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='RELATIVE')
