"""Local roof lap adjustment and front gable joinery, without regenerating body assets."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Bakery02.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};mats={m.name:m for m in bpy.data.materials};helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'helpers_from_A02.py'),'exec'))
for group in ['ClayRoof','RoofDeck']:bpy.data.objects.remove(bpy.data.objects['BW_Bakery02_'+group],do_unlink=True)
ridge=-.35;peak=5.58
code=(H/'reconstruct_bakery.py').read_text();code=code[code.index('rect='):code.index('# Retain source data')]
code=code.replace('x0=ridge+(end-ridge)*v0;x1=ridge+(end-ridge)*v1;', 'offset=.045*math.sin(col*1.55+row*.91);x0=ridge+(end-ridge)*v0+(offset if row>0 else 0);x1=ridge+(end-ridge)*v1+(offset if row<rows-1 else 0);')
code=code.replace('p.y+=.022+(rows-row)*.002+', 'p.y+=.020+(rows-row)*.003+.035*t*t+')
exec(compile(code,str(H/'reconstruct_bakery.py'),'exec'))
# Lift the king posts into their plaster reveals, not behind the plaster surface.
o=bpy.data.objects['BW_Bakery02_Timber'];bm=bmesh.new();bm.from_mesh(o.data);left=set(bm.verts)
while left:
 v=left.pop();comp={v};stack=[v]
 while stack:
  for e in stack.pop().link_edges:
   for q in e.verts:
    if q in left:left.remove(q);comp.add(q);stack.append(q)
 ps=[P.inverted()@q.co for q in comp];c=sum(ps,Vector())/len(ps)
 if abs(c.x+.35)<.04 and 4.1<c.y<4.5 and abs(c.z-4.5)<.02:
  for q in comp:q.co+=P@Vector((0,0,.12))
 if abs(c.x+.35)<.04 and 4.1<c.y<4.5 and abs(c.z+2.9)<.02:
  for q in comp:q.co+=P@Vector((0,0,-.12))
bm.to_mesh(o.data);bm.free();groups['Timber']=[o]
# Two restrained, seated front braces terminate against the tie beam and king post.
for a,b in [((-2.50,3.18,4.63),(-.43,4.42,4.63)),((2.45,3.18,4.63),(-.27,4.42,4.63))]:
 a,b=Vector(a),Vector(b);delta=b-a;u=Vector((delta.y,-delta.x,0)).normalized()*.052;v=Vector((0,0,.075));V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 create('Seated front gable brace',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.035,(j//4)*delta.length,.11,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'Timber',True,.003)
cat=json.loads((H/'ModelCatalog.json').read_text())
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Bakery02_'+group;o.data.name=o.name
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.update();o.data.calc_loop_triangles()
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models/BW_Bakery02_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 for row in cat['models']:
  if row['group']==group:row['triangles']=len(o.data.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery02.blend'))
