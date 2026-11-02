"""Close only the local serving alcove down to floor level; no complete interior."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Merchant01.blend'));bpy.context.preferences.filepaths.save_version=0
P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));s=bpy.context.scene;mats={m.name:m for m in bpy.data.materials};src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
bpy.data.objects.remove(bpy.data.objects['BW_Merchant01_ServingRecess'],do_unlink=True)
box('Serving rear wall',(-2.05,1.15,3.60),(2.42,2.30,.05),'wood3','ServingRecess',.002)
for x in [-3.22,-.88]:box('Serving side wall',(x,1.15,4.30),(.05,2.30,1.4),'wood3','ServingRecess',.002)
box('Serving ceiling',(-2.05,2.30,4.30),(2.4,.05,1.4),'wood3','ServingRecess',.002);box('Serving floor',(-2.05,-.03,4.30),(2.4,.06,1.4),'wood3','ServingRecess',.002)
bpy.ops.object.select_all(action='DESELECT')
for o in groups['ServingRecess']:o.select_set(True)
bpy.context.view_layer.objects.active=groups['ServingRecess'][0];bpy.ops.object.join();o=bpy.context.object;o.name='BW_Merchant01_ServingRecess';o.data.name=o.name
for v in o.data.vertices:v.co.z+=.15
m=mats['wood3'].copy();m.name='ServingLining';o.data.materials.clear();o.data.materials.append(m)
for p in o.data.polygons:p.material_index=0
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.calc_loop_triangles()
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Merchant01/Models/BW_Merchant01_ServingRecess.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='ServingRecess':row['triangles']=len(o.data.loop_triangles);row['materialOrder']=['ServingLining']
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Merchant01.blend'))
