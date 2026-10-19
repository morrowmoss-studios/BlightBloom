"""Fitted Production02 shop shutters/returns. Reuses approved modeling/export helpers and paint sheet."""
import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[5];A=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/Models'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
paint=bpy.data.images.load(str(R/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));paint.pack()
mats={}
for key in ['Sage','Walnut','Iron','Plaster']:
 m=bpy.data.materials.new('CM02_EntryShop_'+key);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1
 if key=='Iron':bs.inputs['Base Color'].default_value=(.075,.06,.045,1)
 else:
  tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=paint;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
 mats[key]=m
parts=[];current='CM02_EntryShop05';modules={current:{'parts':[]}}
tree=ast.parse((R/'ArtSource/Blender/Architecture/CrookedMortar/PairedWindowBay02/build_paired_window_bay02.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['P','mesh','box','prism']],type_ignores=[]),'<approved mesh helpers>','exec'),globals())
# Two equal-width folding leaves per side: a .72m closed cover folds to a .36m stack.
W=.36;angle=math.radians(12)
for side in [-1,1]:
 hx=1.3+side*.792
 for leaf in [0,1]:
  label=('Left' if side<0 else 'Right')+('_FixedLeaf' if leaf==0 else '_FoldedLeaf')
  z=-.39-leaf*.090
  def at(u,y,offset=0):return(hx+side*u*math.cos(angle),y,z-u*math.sin(angle)+offset)
  created=[]
  for plank in range(3):
   u0=.009+plank*(W-.012)/3;u1=u0+(W-.012)/3-.006
   # Work in an unrotated panel coordinate frame; rotate all craftsmanship together.
   top=lambda u:2.925+.025*math.sin(math.pi*u/W)
   o=prism(label+'_SagePlank_%d'%plank,[(u0,1.32),(u1,1.32),(u1,top(u1)),((u0+u1)/2,top((u0+u1)/2)),(u0,top(u0))],-.020,.020,'Sage',.005);created.append(o)
  for y in [1.48,2.74]:created.append(box(label+'_BackRail',(W/2,y,.030),(W-.025,.055,.035),'Walnut',.004))
  # Explicit panel transform, including opposite hand, with baked positive-volume mesh data.
  for o in created:
   for v in o.data.vertices:
    u,y,depth=v.co.x,v.co.z,v.co.y
    q=at(u,y,depth);v.co=Vector(P(*q))
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  for y in [1.53,2.73]:
   # Visible slender straps sit on the viewer-facing leaf face.
   p=at(.18,y,-.028);o=box(label+'_HingeBand',p,(.26,.028,.018),'Iron',.003)
   centre=Vector(P(*p));rot=Matrix.Rotation(-side*angle,3,'Z')
   for v in o.data.vertices:v.co=centre+rot@(v.co-centre)
 # Fixed jamb hinges and outer folding knuckles make the narrow stacks legible as bi-folds.
 for y in [1.53,2.73]:
  box(('Left' if side<0 else 'Right')+'_JambHingePlate',(hx-side*.035,y,-.375),(.12,.115,.018),'Iron',.003)
  box(('Left' if side<0 else 'Right')+'_JambKnuckle',(hx,y,-.392),(.030,.11,.055),'Iron',.004)
  box(('Left' if side<0 else 'Right')+'_FoldKnuckle',(hx+side*W*math.cos(angle),y,-.435-W*math.sin(angle)),(.032,.09,.110),'Iron',.004)
# Flush, thick plaster returns close the former wider rough opening behind the fitted frame.
for x in [.48,2.12]:box('ShopWindow_PlasterReturn',(x,2.115,-.10),(.205,1.70,.20),'Plaster',.003)
# Quiet lintel shoulders tie the smaller shop bay to the canopy; no extra ornamental layers.
box('ShopWindow_HeaderShoulder',(1.3,2.995,-.245),(1.90,.10,.19),'Walnut',.005)
rects={'Plaster':(.015,.515,.47,.47),'Walnut':(.515,.515,.47,.47),'Sage':(.015,.015,.47,.47),'Iron':(.515,.515,.47,.47)}
prod=ast.parse((D.parent/'build_production02.py').read_text());exec(compile(ast.Module(body=[n for n in prod.body if isinstance(n,ast.FunctionDef) and n.name=='uvmap'],type_ignores=[]),'<approved UV helper>','exec'),globals())
checks=[]
for o in parts:
 uvmap(o,o['paint']);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 if bad or deg or vol<=0:raise RuntimeError((o.name,bad,deg,vol))
 checks.append(dict(name=o.name,role=o['paint'],triangles=len(o.data.loop_triangles),nonManifold=bad,degenerate=deg,volume=vol))
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM02_EntryShopComposition05.blend'))
# Four draw groups, not one renderer per plank/hinge.
groups={key:[o for o in parts if o['paint']==key] for key in mats}
for key,selected in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in selected:o.select_set(True)
 bpy.context.view_layer.objects.active=selected[0]
 if len(selected)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='CM02_EntryShop_'+key;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=str(A/'CM02_EntryShopComposition05.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'MeshValidation.json').write_text(json.dumps(checks,indent=2));print('ENTRY_SHOP_OK',len(parts),sum(x['triangles'] for x in checks))
