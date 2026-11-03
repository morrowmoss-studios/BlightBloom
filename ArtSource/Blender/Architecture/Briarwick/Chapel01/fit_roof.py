"""Restore native eave boards: wood3 is eave closure, not gable infill."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Chapel01.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};mats={m.name:m for m in bpy.data.materials};helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'roof_helpers.py'),'exec'))
bpy.data.objects.remove(bpy.data.objects['BW_Chapel01_Roof'],do_unlink=True)
for i in range(6):
 z=-4.7+(i+.5)*11.6/6;native('roof_wide1_3.002','Complete native roof',lambda v,z=z:(v.x/1.69875622*4.15,3.45+v.y/2.38497162*3.8+.12,z+v.z*11.6/12),'Roof')
bpy.ops.object.select_all(action='DESELECT')
for o in groups['Roof']:o.select_set(True)
bpy.context.view_layer.objects.active=groups['Roof'][0];bpy.ops.object.join();o=bpy.context.object;o.name='BW_Chapel01_Roof';o.data.name=o.name;bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.calc_loop_triangles()
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Chapel01/Models/BW_Chapel01_Roof.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Roof':row['triangles']=len(o.data.loop_triangles);row['materialOrder']=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Chapel01.blend'))
