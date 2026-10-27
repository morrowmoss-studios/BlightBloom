"""Restore only candidate cabinet from recorded construction, then fit individual watertight members."""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));s=bpy.context.scene
name='CM_SW13_FittedApothecaryCabinet';coll=bpy.data.collections[name+' editable components']
for o in list(coll.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.data.collections.remove(coll);bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[];wood=bpy.data.materials['CM_SW13_PaintedWalnut'];sage=bpy.data.materials['CM_SW13_Sage'];brass=bpy.data.materials['CM_SW13_AgedBrass']
t=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(t[t.index('def smooth('):t.index('ogee=')]);t=(D.parent/'ShopWorkflow10/build_shop10.py').read_text();exec(t[t.index('def timber('):t.index('# Medicine cabinet:')]);t=(D/'build_shop13.py').read_text();exec(t[t.index('# Per-member UV'):t.index('# Fitted apothecary cabinet:')]);exec(t[t.index('# Fitted apothecary cabinet:'):t.index("finish('CM_SW13_FittedApothecaryCabinet')")])
# Fit against only three closed structural solids, never an overlapping compound cutter.
struct=bpy.data.collections['CM_SW13_StructuralJoinery editable components'];tools=[]
for o in struct.objects:
 if not any(o.name.startswith(n) for n in ['Hewn shop tie standard','Slightly cambered principal tie','Housed curved tie bearing']):continue
 if min(v.co.x for v in o.data.vertices)>.4:continue
 cut=o.copy();cut.data=o.data.copy();s.collection.objects.link(cut);cut.hide_set(False)
 for v in cut.data.vertices:v.co=(1.15-v.co.y,v.co.x-.23,v.co.z-.2)
 tools.append(cut)
for o in parts:
 # Small upper step into the retained tie: lower four vessel levels remain identical.
 for v in o.data.vertices:
  if v.co.z>2.35:
   u=max(0,min(1,(-v.co.x-.40)/.32));u=u*u*(3-2*u);v.co.z=2.35+(v.co.z-2.35)*(1-.62*u)
 if min(v.co.x for v in o.data.vertices)>-.5:continue
 bpy.context.view_layer.objects.active=o
 for cut in tools:
  mod=o.modifiers.new('Individual bearing rebate','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name)
for cut in tools:bpy.data.objects.remove(cut,do_unlink=True)
finish(name);g=modules[0][0];attr=g.data.color_attributes.new(name='PaintedCavity',type='FLOAT_COLOR',domain='POINT')
for v in attr.data:v.color=(1,1,1,1)
# Pull only the rear vessel column forward onto the shelf nose, clear of the retained standard.
stockName='CM_SW13_RemedyDisplay'
for o in list(bpy.data.collections[stockName+' editable components'].objects)+[bpy.data.objects[stockName]]:
 for v in o.data.vertices:
  if v.co.x<-.5 and v.co.z<2.35:v.co.y+=.05
 bpy.context.view_layer.update()
cat=json.loads((D/'AssetCatalog.json').read_text());row=next(r for r in cat['modules'] if r['name']==name);row.update(modules[0][1]);cat['triangles']=sum(r['triangles'] for r in cat['modules']);(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2));bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
for n in [name,stockName]:
 g=bpy.data.objects[n];bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(n+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
print('INDIVIDUALLY_FITTED',row)
