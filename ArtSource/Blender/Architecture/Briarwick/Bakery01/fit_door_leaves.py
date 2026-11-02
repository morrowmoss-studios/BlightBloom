"""Fit static leaves by actual wood panel bounds, not protruding hinge hardware."""
import bpy
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Bakery01.blend'))
for group,centre,width in [('CustomerDoor',.9,1.4),('ServiceDoor',1.8,1.3)]:
 o=bpy.data.objects['BW_Bakery01_'+group];ids={i for p in o.data.polygons if o.data.materials[p.material_index].name=='doors' for i in p.vertices};lo=min(o.data.vertices[i].co.x for i in ids);hi=max(o.data.vertices[i].co.x for i in ids);mid=(lo+hi)/2;scale=(width-.016)/(hi-lo)
 for v in o.data.vertices:v.co.x=centre+(v.co.x-mid)*scale
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;o.data.update()
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Models/BW_Bakery01_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery01.blend'))
