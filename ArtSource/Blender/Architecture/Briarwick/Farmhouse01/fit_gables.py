"""Local roof/gable fit: inset board ends below thatch and close narrow plank gaps."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Farmhouse01.blend'));bpy.context.preferences.filepaths.save_version=0
o=bpy.data.objects['BW_Farmhouse01_Gables']
if o.get('roof_fit_done'):raise RuntimeError('Already fitted')
for v in o.data.vertices:
 q=P.inverted()@v.co;q.y=min(q.y,6.15-abs(q.z)*3.10/4.12-.28+.12);v.co=P@q
# Back boards behind the open joints; no playable interior is implied.
V=[];F=[];UV=[]
for side in [-1,1]:
 outline=[(-3.6,3.05),(3.6,3.05),(3.6,3.15),(0,5.87),(-3.6,3.15)];b=len(V)
 for x in [side*4.45-.02,side*4.45+.02]:
  for z,y in outline:V.append(P@Vector((x,y+.12,z)));UV.append((.06+.85*(z+3.6)/7.2,.05+.90*(y-3.05)/3))
 F += [tuple(b+i for i in range(4,-1,-1)),tuple(b+5+i for i in range(5))]
 for i in range(5):j=(i+1)%5;F.append((b+i,b+j,b+5+j,b+5+i))
me=bpy.data.meshes.new('Closed gable backing');me.from_pydata(V,[],F);me.materials.append(bpy.data.materials['wood3']);uv=me.uv_layers.new(name='UVMap')
for p in me.polygons:
 for li in p.loop_indices:uv.data[li].uv=UV[me.loops[li].vertex_index]
back=bpy.data.objects.new('Gable backing',me);bpy.context.scene.collection.objects.link(back)
bpy.ops.object.select_all(action='DESELECT');back.select_set(True);o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.join()
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o['roof_fit_done']=True;o.data.calc_loop_triangles()
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Farmhouse01/Models/BW_Farmhouse01_Gables.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Gables':row['triangles']=len(o.data.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Farmhouse01.blend'))
