"""Offset the centre bearing assembly 0.45 m left so the original path centre stays clear."""
import bpy,bmesh
from mathutils import Vector
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Blacksmith01.blend'));bpy.context.preferences.filepaths.save_version=0
for group in ['Timber','Foundation']:
 o=bpy.data.objects['BW_Blacksmith01_'+group]
 if o.get('ApproachClear'):raise RuntimeError('Already offset')
 bm=bmesh.new();bm.from_mesh(o.data);left=set(bm.verts)
 while left:
  v=left.pop();part={v};stack=[v]
  while stack:
   for e in stack.pop().link_edges:
    for q in e.verts:
     if q in left:left.remove(q);part.add(q);stack.append(q)
  c=sum((Vector((-q.co.x,q.co.z,-q.co.y)) for q in part),Vector())/len(part)
  if -.72<c.x<-.01 and abs(c.z-3.7)<.3 and c.y<3.3:
   for q in part:q.co.x+=.45
 bm.to_mesh(o.data);bm.free();o['ApproachClear']=True;o.data.update();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/Models/BW_Blacksmith01_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Blacksmith01.blend'))
