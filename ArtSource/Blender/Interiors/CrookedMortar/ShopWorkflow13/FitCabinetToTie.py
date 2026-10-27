"""Fitted rear upper register clears the existing cross-tie/bearing. Lower stock datums unchanged."""
import bpy,bmesh,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
for name in ['CM_SW13_FittedApothecaryCabinet','CM_SW13_RemedyDisplay']:
 group=list(bpy.data.collections[name+' editable components'].objects)+[bpy.data.objects[name]]
 for o in group:
  for v in o.data.vertices:
   if v.co.z>2.35:
    u=max(0,min(1,(-v.co.x-.40)/.32));u=u*u*(3-2*u);factor=1-.62*u;v.co.z=2.35+(v.co.z-2.35)*factor
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
for name in ['CM_SW13_FittedApothecaryCabinet','CM_SW13_RemedyDisplay']:
 o=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');o.hide_set(False);o.select_set(True);bpy.context.view_layer.objects.active=o;o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Models'/(name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
