"""Seat the fixed-open service leaf clear of its portal and orient closed hood shells."""
import bpy,bmesh
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Blacksmith01.blend'));bpy.context.preferences.filepaths.save_version=0
for group in ['ServiceDoor','ForgeMasonry']:
 o=bpy.data.objects['BW_Blacksmith01_'+group];bm=bmesh.new();bm.from_mesh(o.data)
 if group=='ServiceDoor' and not o.get('FoldedClear'):
  # Blender Y = -Unity Z.
  for v in bm.verts:v.co.y=2.46-v.co.y
  bmesh.ops.reverse_faces(bm,faces=list(bm.faces));o['FoldedClear']=True
 if group=='ForgeMasonry':bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/Models/BW_Blacksmith01_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Blacksmith01.blend'))
