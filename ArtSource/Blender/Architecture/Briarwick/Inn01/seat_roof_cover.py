"""Local roof fit: clear the deck from visible shingles, fit ridge boards, map timber soffits."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Inn01.blend'));bpy.context.preferences.filepaths.save_version=0
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};mats={m.name:m for m in bpy.data.materials};s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
cat=json.loads((H/'ModelCatalog.json').read_text())
for group in ['Shingles','RoofDeck']:
 o=bpy.data.objects['BW_Inn01_'+group]
 if o.get('RoofCoversSeated'):raise RuntimeError('Already seated')
 if group=='Shingles':
  bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update();caps=[f for f in bm.faces if max(v.co.y for v in f.verts)-min(v.co.y for v in f.verts)>1.0];verts={v for f in caps for v in f.verts}
  for v in verts:
   x,z=-v.co.x,-v.co.y
   if v.co.z<4.2:ridge,peak,left,right=0,3.65,.85/1.55,.85/1.55
   elif abs(x-3.2)<.2:ridge,peak,left,right=3.2,7.25,1.15/1.94,1.8/2.15
   else:ridge,peak,left,right=-1.8,8.5,2.55/3.05,2.4/2.94
   v.co.z=peak-abs(x-ridge)*(left if x<ridge else right)+.014*math.sin(z*.72)+.008*math.sin(x*1.8+z*.7)+.060
  bmesh.ops.solidify(bm,geom=caps,thickness=-.012);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free()
 else:
  for v in o.data.vertices:v.co.z-=.045
  o.data.materials.clear();o.data.materials.append(mats['wood2'])
  for p in o.data.polygons:
   ps=[Vector((-o.data.vertices[i].co.x,o.data.vertices[i].co.z,-o.data.vertices[i].co.y)) for i in p.vertices];span=[max(v[i] for v in ps)-min(v[i] for v in ps) for i in range(3)];va=max(range(3),key=lambda i:span[i]);ua=max((i for i in range(3) if i!=va),key=lambda i:span[i]);lo=min(v[va] for v in ps);mid=(max(v[ua] for v in ps)+min(v[ua] for v in ps))/2
   for li,v in zip(p.loop_indices,ps):o.data.uv_layers.active.data[li].uv=timberUV(v[ua]-mid,v[va]-lo,max(span[ua],.001),max(span[va],.001),'wood2')
 o.data.update();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.calc_loop_triangles();o['RoofCoversSeated']=True;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Models/BW_Inn01_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 for row in cat['models']:
  if row['group']==group:row['triangles']=len(o.data.loop_triangles);row['materialOrder']=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Inn01.blend'))
