"""Ensure exterior normals after the reflected oven placement and open roof construction."""
import bpy,bmesh,math
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Bakery02.blend'))
for group in ['InternalOven','ClayRoof','RoofDeck']:
 o=bpy.data.objects['BW_Bakery02_'+group];bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
 if group=='InternalOven' and not o.get('CorrectedWinding02'):bmesh.ops.reverse_faces(bm,faces=list(bm.faces));o['CorrectedWinding02']=True
 if group=='ClayRoof':bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<-.01])
 if group=='RoofDeck':
  flip=[]
  for f in bm.faces:
   c=f.calc_center_median();x=-c.x;z=-c.y;top=5.58-(5.58-3.13)*abs(x+.35)/(3.37 if x<-.35 else 4.07)+.016*math.sin(z*.8)+.008*math.sin(x*2+z);desired=1 if c.z>top-.05 else -1
   if f.normal.z*desired<-.01:flip.append(f)
  bmesh.ops.reverse_faces(bm,faces=flip)
 bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models/BW_Bakery02_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery02.blend'))
