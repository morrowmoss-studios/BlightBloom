"""Focused crafted shop evolution: existing source construction + fitted room pieces.
Run once into Workflow12; prior sources and assets are read-only.
"""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow12'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[]
def material(n,col,path=None):
 m=bpy.data.materials.new(n);m.diffuse_color=col;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=.92
 if path:
  node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(path));node.image.pack();m.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=material('CM_CW09_Walnut',(.32,.18,.09,1),R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow09/Textures/CM_CW09_Walnut.png');sage=material('CM_SW12_WornSage',(.34,.39,.27,1));iron=material('CM_CW09_Iron',(.13,.15,.12,1))
t=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(t[t.index('def smooth('):t.index('ogee=')])
t=(D.parent/'ShopWorkflow10/build_shop10.py').read_text();exec(t[t.index('def timber('):t.index('# Medicine cabinet:')])
# Retain the proven shelf datums, rebuild the cabinet silhouette around them.
# No stock added and no change to the existing shelf load surfaces or floor footprint.
for side in [-1,1]:
 inside=bez([(side*.77,.06),(side*.87,.52),(side*.75,1.63),(side*.78,2.30)],22)
 outside=bez([(side*.91,.06),(side*.87,.82),(side*.94,1.90),(side*.91,2.39)],22)
 extrude('Continuous shouldered standard',inside+list(reversed(outside)),-.18,.176,b=.009)
 # Actual stepped feet stay inside the previous widest bounds.
 extrude('Stepped foot',[ (side*.77,.04),(side*.92,.04),(side*.92,.14),(side*.89,.20),(side*.78,.20)],-.18,.176,b=.006)
for k in range(6):
 x=-.70+k*.28
 extrude('Recessed sage back board',[(x-.138,.20),(x+.138,.20),(x+.138,2.34),(x-.138,2.34)],-.177,-.145,sage,.005)
for i,y in enumerate([.52,.98,1.44,1.90,2.31]):
 shaped_shelf('Breadboard shelf datum',1.79,.17,y)
 # A swept under-shelf apron at the upper and lower levels creates recessed arched niches.
 if i in [0,4]:
  for a,b in [(-.77,-.03),(.03,.77)]:
   curve=bez([(a,y-.18),(a+(b-a)*.24,y-.075),(b-(b-a)*.24,y-.075),(b,y-.18)],16)
   extrude('Integral segmental shelf apron',[(a,y-.045),(b,y-.045)]+list(reversed(curve)),.115,.174,b=.004)
# Broad, quiet scalloped crown plus real coved transition; visibly hand-shaped at room scale.
crest=bez([(-.92,2.31),(-.76,2.46),(-.30,2.37),(0,2.51)],24)+bez([(0,2.51),(.29,2.39),(.71,2.44),(.92,2.34)],24)[1:]
extrude('Swept cabinet pediment',[(-.92,2.29),(.92,2.29)]+list(reversed(crest)),-.19,.16,b=.006)
profile_sweep('Coved crown bearing',[(x,y,.165) for x,y in crest],[(-.019,-.01),(-.019,.0),(-.012,.016),(.012,.02),(.02,.008),(.02,-.01)])
for x in [-.52,0,.52]:
 extrude('Framed medicine drawer',[(x-.246,.12),(x+.246,.12),(x+.246,.43),(x-.246,.43)],-.10,.16,b=.007)
 extrude('Recessed sage drawer',[(x-.19,.17),(x+.19,.17),(x+.19,.38),(x-.19,.38)],.160,.164,sage,.004)
 timber('Drawer integral finger pull',(x-.045,.34,.168),(x+.045,.34,.168),.018,.022,0)
for x in [-.78,.78]:
 for y in [.97,1.89,2.31]:knee('Housed shelf bearing',x,y-.02,.125,-1 if x>0 else 1)
finish('CM_SW12_MedicineCabinet')
# Small records case: same mounting and content datums, now a continuous shaped enclosure.
for side in [-1,1]:
 a=bez([(side*.57,.02),(side*.62,.22),(side*.55,.62),(side*.58,.77)],18)
 b=bez([(side*.65,.02),(side*.69,.18),(side*.63,.62),(side*.66,.84)],18)
 extrude('Shaped register end',a+list(reversed(b)),0,.27,b=.005)
for y in [.10,.42,.76]:shaped_shelf('Register shelf',1.28,.28,y,0)
extrude('Register inset sage backing',[(-.59,.04),(.59,.04),(.59,.78),(-.59,.78)],0,.035,sage,.004)
crown=bez([(-.67,.77),(-.46,.91),(-.21,.80),(0,.94)],18)+bez([(0,.94),(.27,.80),(.43,.91),(.67,.77)],18)[1:]
extrude('Register shaped crown',[(-.67,.75),(.67,.75)]+list(reversed(crown)),0,.25,b=.004)
# Recessed fitted cubbies under the lowest stock shelf, not additional loose records.
for x in [-.38,0,.38]:
 curve=bez([(x-.17,.09),(x-.15,-.06),(x+.15,-.06),(x+.17,.09)],16)
 extrude('Register scalloped underside',[(x-.19,.10),(x+.19,.10)]+list(reversed(curve)),.16,.25,b=.004)
finish('CM_SW12_RecordsCabinet')
# Fitted lower paneling: all construction stays within 65 mm of existing walls.
def dado(n,x0,x1,y0,y1,z=.05):
 count=max(1,round((x1-x0)/.47));w=(x1-x0)/count
 for j in range(count):
  l=x0+j*w+.018;r=x0+(j+1)*w-.018
  extrude(n+' recessed painted field',[(l,y0+.07),(r,y0+.07),(r,y1-.06),(l,y1-.06)],z-.032,z-.012,sage,.004)
 for y in [y0+.025,y1-.02]:timber(n+' mortised rail',(x0,y,z),(x1,y,z),.055,.045,.003)
 for j in range(count+1):
  x=x0+j*w;timber(n+' stile',(x,y0,z),(x,y1,z),.04,.045,.002)
dado('Shop window apron',.16,2.17,.22,1.12,.055)
# Short east-wall dado under existing mounted register (rotate local assembly only).
start=len(parts);dado('Register wall lining',.20,1.76,.22,.70,.05)
for o in parts[start:]:
 for v in o.data.vertices:
  x,y,z=v.co.x,v.co.z,v.co.y;v.co=P((5.4-z,y,x))
 smooth(o.data)
finish('CM_SW12_FittedPaneling')
# Room perimeter additions have structural purpose: broad coved wall plates, curved bearing braces,
# a deeper sill and joined window shoulders; openings stay intact.
timber('Front window wall plate',(.16,3.13,.08),(2.17,3.13,.08),.17,.14,.009)
for x in [.36,2.21]:timber('Window reveal standard',(x,1.16,.06),(x,3.05,.06),.10,.12,.004)
slab('Window breadboard sill',[(.36,-.01),(2.21,-.01),(2.25,.14),(2.16,.17),(.40,.17),(.32,.13)],1.19,1.27,.006)
# Curved knees are fitted to existing side shafts and spanning tie, remain well above player heads.
for side in [-1,1]:
 x=.10 if side<0 else 5.28;direction=1 if side<0 else -1
 outer=bez([(x,2.54),(x+direction*.12,2.81),(x+direction*.40,2.98),(x+direction*.61,3.07)],22)
 inner=bez([(x+direction*.06,2.55),(x+direction*.19,2.85),(x+direction*.43,2.92),(x+direction*.63,3.01)],22)
 extrude('Curved housed tie brace',outer+list(reversed(inner)),1.82,1.98,b=.005)
# shallow moulded cornice on the uninterrupted west wall; not a free-floating beam.
timber('West wall plate',(.08,3.14,.10),(.08,3.14,1.85),.16,.15,.006)
finish('CM_SW12_FittedJoinery')
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow12.blend'))
for g,row in modules:
 bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':[r for g,r in modules],'triangles':sum(r['triangles'] for g,r in modules)},indent=2));print('SHOP12_READY',sum(r['triangles'] for g,r in modules))
