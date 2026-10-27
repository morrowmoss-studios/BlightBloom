import bpy,math,json
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));s=bpy.context.scene
coll=bpy.data.collections['CM_SW13_ServiceCounter editable components'];added=[]
for o in list(coll.objects):
 if o.name.startswith('Stepped engaged counter standard'):
  p=o.copy();p.data=o.data.copy();p.name='Rear bearing counter standard';coll.objects.link(p)
  for v in p.data.vertices:v.co.y-=.53
  p.hide_set(True);p.hide_render=True;added.append(p)
g=bpy.data.objects['CM_SW13_ServiceCounter'];bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True)
for o in added:
 p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.hide_set(False);p.hide_render=False;p.select_set(True)
bpy.context.view_layer.objects.active=g;bpy.ops.object.join();g.data.calc_loop_triangles();cat=json.loads((D/'AssetCatalog.json').read_text());row=next(r for r in cat['modules'] if r['name']==g.name);row['triangles']=len(g.data.loop_triangles);row['vertices']=len(g.data.vertices);cat['triangles']=sum(r['triangles'] for r in cat['modules']);(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Models/CM_SW13_ServiceCounter.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP');print('COUNTER_SUPPORTED',row['triangles'])
