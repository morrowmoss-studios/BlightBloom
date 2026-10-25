# Targeted corrections in the existing new source; unchanged modules are not rebuilt/exported.
import bpy,bmesh,math,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow10';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow10.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
# Reproject each disconnected stone by its own bounds; never wrap across a polygon.
def floor_uv(o):
 bm=bmesh.new();bm.from_mesh(o.data);groups=[];pending=set(bm.verts)
 while pending:
  seed=pending.pop();group={seed};todo=[seed]
  while todo:
   v=todo.pop()
   for e in v.link_edges:
    p=e.other_vert(v)
    if p in pending:pending.remove(p);group.add(p);todo.append(p)
  groups.append(group)
 uv=bm.loops.layers.uv.active
 for k,vs in enumerate(groups):
  x0=min(v.co.x for v in vs);x1=max(v.co.x for v in vs);z0=min(v.co.y for v in vs);z1=max(v.co.y for v in vs)
  for f in set(f for v in vs for f in v.link_faces):
   for l in f.loops:l[uv].uv=(.54+.08*(k%3)+(l.vert.co.x-x0)/max(.001,x1-x0)*.12,.05+.11*((k//3)%4)+(l.vert.co.y-z0)/max(.001,z1-z0)*.30)
 bm.to_mesh(o.data);bm.free()
for o in list(bpy.data.objects):
 if o.type=='MESH' and (o.name.startswith('Hand-finished floor flagstone') or o.name=='CM_SW10_FlagstoneFloor'):floor_uv(o)
# Add fitted shaped end cheeks as actual continuous structural timber, within the existing footprint.
P=lambda v:Vector((v[0],v[2],v[1]));wood=bpy.data.materials['CM_CW09_Walnut'];parts=[]
text=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(text[text.index('def smooth('):text.index('ogee=')])
for side in [-1,1]:
 inside=bez([(side*.78,.12),(side*.847,.68),(side*.805,1.66),(side*.785,2.29)],28)
 outside=bez([(side*.91,.12),(side*.885,.76),(side*.897,1.72),(side*.925,2.36)],28)
 poly=inside+list(reversed(outside));extrude('Shaped bearing cabinet cheek',poly,-.18,.172,b=.004)
coll=bpy.data.collections['CM_SW10_MedicineCabinet editable components']
for o in parts:
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o)
# Add copies into only the existing cabinet export mesh; sources remain separately editable.
g=bpy.data.objects['CM_SW10_MedicineCabinet'];g.hide_set(False);bpy.ops.object.select_all(action='DESELECT');g.select_set(True)
for o in parts:
 p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.hide_set(False);p.hide_render=False;p.select_set(True)
bpy.context.view_layer.objects.active=g;bpy.ops.object.join()
for o in parts:o.hide_set(True);o.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow10.blend'))
for name in ['CM_SW10_MedicineCabinet','CM_SW10_FlagstoneFloor']:
 g=bpy.data.objects[name];g.hide_set(False);bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
# Refresh catalog only for the two altered meshes.
import json
cat=json.loads((D/'AssetCatalog.json').read_text())
for row in cat['modules']:
 o=bpy.data.objects[row['name']];o.data.calc_loop_triangles();row['triangles']=len(o.data.loop_triangles);row['vertices']=len(o.data.vertices)
cat['newTriangles']=sum(r['triangles'] for r in cat['modules']);(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2));print('REFINED',cat['newTriangles'])
