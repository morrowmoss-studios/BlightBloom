"""Break only the continuous ground sill beams at the two actual doorway openings."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Inn01.blend'));bpy.context.preferences.filepaths.save_version=0
P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));s=bpy.context.scene;mats={m.name:m for m in bpy.data.materials};src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
o=bpy.data.objects['BW_Inn01_Timber']
if o.get('DoorSillsCleared'):raise RuntimeError('Already cleared')
bm=bmesh.new();bm.from_mesh(o.data);left=set(bm.verts);remove=[];count=0
while left:
 v=left.pop();part={v};stack=[v]
 while stack:
  for e in stack.pop().link_edges:
   for q in e.verts:
    if q in left:left.remove(q);part.add(q);stack.append(q)
 c=sum((P.inverted()@q.co for q in part),Vector())/len(part)
 if abs(c.y-.16)<.02 and ((abs(c.x+1.65)<.02 and abs(c.z-7.5)<.02) or (abs(c.x-3.1)<.02 and abs(c.z+1.7)<.02)):remove.extend(part);count+=1
if count!=2:raise RuntimeError('Unexpected sill islands; no save: '+str(count))
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(o.data);bm.free();groups['Timber']=[o]
for z,intervals in [(7.5,[(-4.575,-.76),(.76,1.275)]),(-1.7,[(1.13,2.54),(3.86,5.07)])]:
 for a,b in intervals:box('Interrupted ground sill',((a+b)/2,.16,z),(b-a,.2,.24),'wood2','Timber',.004)
bpy.ops.object.select_all(action='DESELECT')
for ob in groups['Timber']:ob.select_set(True)
bpy.context.view_layer.objects.active=o;bpy.ops.object.join();o.name='BW_Inn01_Timber';o.data.name=o.name;bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.calc_loop_triangles();o['DoorSillsCleared']=True
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Models/BW_Inn01_Timber.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Timber':row['triangles']=len(o.data.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Inn01.blend'))
