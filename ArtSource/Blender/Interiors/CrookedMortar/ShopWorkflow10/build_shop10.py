"""Shop only: shaped joinery, cabinet construction, and fitted stone floor. Established helper/export reuse."""
import bpy,bmesh,math,json
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow10'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[]
def material(n,path=None,col=(.32,.18,.09,1)):
 m=bpy.data.materials.new(n);m.diffuse_color=col;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=.9
 if path:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(path));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=material('CM_CW09_Walnut',R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow09/Textures/CM_CW09_Walnut.png');sage=material('CM_SW10_PaintedSage',col=(.185,.225,.155,1));iron=material('CM_CW09_Iron',col=(.13,.15,.12,1));stone=material('CM_SW10_PaintedStone',A/'Textures/CM_SW10_PlasterStone.png')
text=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(text[text.index('def smooth('):text.index('ogee=')])
# A structural timber solid with changing chamfered profiles, not an inflated primitive.
def timber(n,a,b,width,depth,curve=.007,m=None):
 a=Vector(a);b=Vector(b);direction=(b-a).normalized();side=direction.cross(Vector((0,0,1)))
 if side.length<.1:side=direction.cross(Vector((0,1,0)))
 side.normalize();other=direction.cross(side).normalized();N=8;prof=[(-1,-.74),(-.74,-1),(.74,-1),(1,-.74),(1,.74),(.74,1),(-.74,1),(-1,.74)];vs=[]
 for j in range(13):
  t=j/12;co=a.lerp(b,t)+side*(curve*math.sin(t*math.pi));w=width*(1-.025*math.sin(t*math.pi));d=depth*(1-.025*math.sin(t*math.pi))
  for u,v in prof:vs.append(tuple(co+side*(u*w/2)+other*(v*d/2)))
 fs=[tuple(reversed(range(N))),tuple(range(len(vs)-N,len(vs)))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(12) for i in range(N)]
 return mesh(n,vs,fs,m or wood)
def finish(n):
 global parts
 src=bpy.data.collections.new(n+' editable components');s.collection.children.link(src)
 for o in parts:
  for c in list(o.users_collection):c.objects.unlink(o)
  src.objects.link(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:
  c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.select_set(True)
 bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();g=bpy.context.object;g.name=n;g.data.name=n+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');g.data.calc_loop_triangles();modules.append((g,{'name':n,'triangles':len(g.data.loop_triangles),'vertices':len(g.data.vertices),'materials':[m.name for m in g.data.materials]}))
 for o in parts:o.hide_set(True);o.hide_render=True
 parts=[]
def shaped_shelf(n,w,front,y,back=-.16):
 line=bez([(-w/2,front-.025),(-w*.2,front+.008),(w*.24,front+.014),(w/2,front-.025)],24);poly=[(-w/2,back),(w/2,back)]+list(reversed(line));return slab(n,poly,y-.05,y,.005)
def knee(n,x,y,z,side=1):
 points=bez([(x+side*.16,y),(x+side*.12,y-.02),(x+side*.07,y-.13),(x,y-.15)],16)
 return extrude(n,[(x,y+.018),(x+side*.17,y+.018)]+points+[(x,y-.15)],z-.035,z+.035,b=.004)
# Medicine cabinet: shelf tops coincide with retained original stocked courses.
for x in [-.853,.853]:
 timber('Hewn cabinet upright',(x,.04,.0),(x,2.32,.0),.105,.34,.006)
# Separate inset back boards, with grain and very slight bow for illustrated depth.
for k in range(6):
 x=-.70+k*.28
 o=extrude('Quiet sage field',[(x-.138,.24),(x+.138,.24),(x+.138,2.29),(x-.138,2.29)],-.177,-.145,sage,.006)
for y in [.52,.98,1.44,1.90,2.31]:shaped_shelf('Shaped load-bearing shelf',1.79,.17,y)
# Upper crown has actual arched shoulders and depth, without being more ornate than the counter.
outline=[(-.91,2.30),(-.91,2.37)]+bez([(-.91,2.37),(-.66,2.43),(-.31,2.37),(0,2.445)],20)+bez([(0,2.445),(.27,2.37),(.65,2.43),(.91,2.37)],20)+[(.91,2.30)]
extrude('Hand-shaped cornice',outline,-.19,.155,b=.005)
for x in [-.853,.853]:knee('Housed cornice knee',x,2.30,.11,-1 if x>0 else 1)
# Base storage fronts: actual stiles, inset fields, shaped arris and shallow finger recesses.
for x in [-.55,0,.55]:
 extrude('Fitted lower drawer',[(x-.255,.12),(x+.255,.12),(x+.262,.18),(x+.25,.45),(x-.25,.45),(x-.262,.18)],-.1,.17,b=.007)
 extrude('Sage inset drawer field',[(x-.212,.17),(x+.212,.17),(x+.212,.40),(x-.212,.40)],.171,.178,sage,.004)
 timber('Drawer finger lip',(x-.047,.352,.18),(x+.047,.352,.18),.013,.015,0)
for x in [-.87,.87]:
 for y in [.47,2.26]:
  # Peg ends lie flush in the timber faces.
  vs=[(x+.008*math.cos(t),y+.008*math.sin(t),z) for z in [.170,.173] for t in np.linspace(0,math.tau,13)[:-1]];fs=[tuple(reversed(range(12))),tuple(range(12,24))]+[(j,(j+1)%12,(j+1)%12+12,j+12) for j in range(12)];mesh('Cabinet drawbore peg',vs,fs)
finish('CM_SW10_MedicineCabinet')
# Small records cabinet, same old wall datum / shelf heights; contents are reused in Unity.
for x in [-.61,.61]:timber('Register cabinet cheek',(x,.005,.14),(x,.75,.14),.065,.27,.004)
for y in [.10,.42,.76]:shaped_shelf('Register shelf',1.28,.28,y,0)
extrude('Register inset back',[(-.59,.04),(.59,.04),(.59,.75),(-.59,.75)],0,.035,sage,.005)
for x in [-.59,.59]:knee('Register carved bearing cheek',x,.415,.20,-1 if x>0 else 1)
extrude('Register arched crown',[(-.65,.75),(-.65,.80)]+bez([(-.65,.80),(-.26,.78),(-.25,.87),(0,.86)],16)+bez([(0,.86),(.26,.87),(.26,.78),(.65,.80)],16)+[(.65,.75)],0,.25,b=.004)
finish('CM_SW10_RecordsCabinet')
# One replacement shop tie beam fitted to its existing support and herb hooks.
# Local +Y is height; the original root sits at (2.7,3.21,1.9).
timber('Hand-planed spanning tie',(-2.7,-.13,0),(2.7,-.13,0),.25,.20,.012)
for x in [-2.53,2.53]:
 extrude('Beam bearing shoulder',[(x-.12,-.30),(x+.12,-.30),(x+.12,.02),(x-.12,.02)],-.11,.11,b=.008)
finish('CM_SW10_ShopBeam')
# Room-specific inside timber only, avoiding openings and the stair area.
# Slim threshold-side posts stay outboard of existing door clearances.
for x in [2.47,4.73]:timber('Treatment doorway joined post',(x,.2,4.35),(x,3.22,4.35),.16,.12,.008)
timber('Treatment doorway shaped lintel',(2.47,3.13,4.35),(4.73,3.13,4.35),.17,.12,.008)
for z in [1.96,4.04]:timber('Kitchen doorway joined post',(5.33,.2,z),(5.33,3.22,z),.16,.12,.006)
timber('Kitchen doorway shaped lintel',(5.33,3.13,1.96),(5.33,3.13,4.04),.17,.12,.006)
# Tapered bearing brackets at room perimeter; no braces across routes.
for x in [.10,5.28]:
 timber('Shop wall shaft',(x,.2,1.90),(x,3.18,1.90),.13,.14,.008)
 knee('Tie bearing knee',x,3.08,1.90,1 if x<1 else -1)
# Low dado timber breaks up blank plaster without adding panels to every surface.
for a,b in [((.055,.67,.24),(.055,.67,1.8)),((5.32,.67,.2),(5.32,.67,1.75)),((4.78,.67,4.34),(5.25,.67,4.34))]:timber('Quiet wall dado rail',a,b,.065,.055,.002)
# Existing ceiling surface stays; authored secondary joists establish a coherent structural rhythm.
for x in [.70,2.30,3.90,5.05]:timber('Ceiling joist',(x,3.235,.08),(x,3.235,4.32),.11,.12,.009)
finish('CM_SW10_RoomJoinery')
# Shallow flagstones keep exactly the same walking plane (+3mm visual arris only).
# No extra Unity object per slab. Broad original painted colour regions, not procedural noise.
for iz in range(7):
 z0=.008+iz*(4.384/7);z1=.008+(iz+1)*(4.384/7)
 widths=[.82,.77,.95,.88,1.00,.98] if iz%2==0 else [1.04,.84,.92,.89,.84,.87]
 scale=5.384/sum(widths);x0=.008
 for ix,w in enumerate(widths):
  x1=x0+w*scale;gap=.004
  poly=[(x0+gap,z0+gap),(x1-gap-.012,z0+gap),(x1-gap,z0+.018),(x1-gap,z1-gap-.012),(x1-gap-.015,z1-gap),(x0+gap+.008,z1-gap),(x0+gap,z1-gap-.018)]
  o=slab('Hand-finished floor flagstone',poly,.17,.203,.002)
  o.data.materials.clear();o.data.materials.append(stone)
  uv=o.data.uv_layers[0]
  for f in o.data.polygons:
   for li in f.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(.535+((co.x/2.2+.13*ix)%1)*.42,.04+((co.y/2+.11*iz)%1)*.90)
  x0=x1
finish('CM_SW10_FlagstoneFloor')
# Save unconverted editable parts, export only joined copies with validated conversion.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow10.blend'))
for g,row in modules:
 bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':[r for g,r in modules],'newTriangles':sum(r['triangles'] for g,r in modules),'counter':'Unmodified Workflow09 prefab reused, not regenerated'},indent=2));print('SHOP10_READY',sum(r['triangles'] for g,r in modules))
