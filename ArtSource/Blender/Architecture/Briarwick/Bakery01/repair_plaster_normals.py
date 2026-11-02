"""Repair only bakery plaster custom split normals after triangulation."""
import bpy
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4]
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Bakery01.blend'))
o=bpy.data.objects['BW_Bakery01_Plaster'];bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
for p in o.data.polygons:p.use_smooth=False
for uv in ([] if o.data.materials[0].name.startswith("Bakery_CleanPlaster") else o.data.uv_layers.active.data):uv.uv=((uv.uv.x-.8588129)/(.906400144-.8588129),(uv.uv.y-.599580944)/(.784569-.599580944))
mat=o.data.materials[0];mat=mat.copy();mat.name='Bakery_CleanPlaster';o.data.materials[0]=mat
node=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');node.image=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures/BW_Bakery01_Plaster_BaseColor.png'));node.image.pack()
o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update()
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Models/BW_Bakery01_Plaster.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery01.blend'))
