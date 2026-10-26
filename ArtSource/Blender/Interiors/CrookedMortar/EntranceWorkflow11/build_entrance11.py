"""One fitted interior architectural bay. Low-density construction profiles; no dense sculpture or clutter."""
import bpy,bmesh,math,json
import numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/EntranceWorkflow11'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[]
def material(n,path,color=(1,1,1,1)):
 m=bpy.data.materials.new(n);m.diffuse_color=color;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.92;t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(path));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color']);return m
wood=material('CM_CW09_Walnut',R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow09/Textures/CM_CW09_Walnut.png')
paint=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow10/Textures/CM_SW10_PlasterStone.png'
stone=material('CM_EW11_DressedSandstone',paint,(.90,.84,.72,1));plaster=material('CM_EW11_AgedLime',paint,(1,.98,.93,1));mortar=material('CM_EW11_Mortar',paint,(.62,.58,.49,1));repair=material('CM_EW11_RenewedLime',paint,(.96,.93,.84,1))
text=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(text[text.index('def smooth('):text.index('ogee=')])
def finish(n):
 global parts
 coll=bpy.data.collections.new(n+' editable parts');s.collection.children.link(coll)
 for o in parts:
  for c in list(o.users_collection):c.objects.unlink(o)
  coll.objects.link(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:
  p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.select_set(True)
 bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();g=bpy.context.object;g.name=n;g.data.name=n+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');g.data.calc_loop_triangles();modules.append((g,{'name':n,'triangles':len(g.data.loop_triangles),'vertices':len(g.data.vertices),'materials':[m.name for m in g.data.materials]}))
 for o in parts:o.hide_render=True;o.hide_set(True)
 parts=[]
def paintuv(o,kind,index=0):
 # Stable face projection with moderate physical scale; never sample across the atlas divide.
 uv=o.data.uv_layers[0]
 for f in o.data.polygons:
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if kind=='stone':uv.data[li].uv=(.54+.025*(index%3)+(co.x-2.2)/3.2*.31,.05+(index%4)*.055+(co.z-.2)/3.1*.65)
   else:uv.data[li].uv=(.025+(co.x-2.2)/3.2*.44,.035+(co.z-.2)/3.1*.93)
def poly_solid(n,poly,z0,z1,m,b=.004,index=0):
 o=extrude(n,poly,z0,z1,m,b);paintuv(o,'stone' if m==stone else 'plaster',index);return o
C=3.7;spring=1.92;ri=1.0;ro=1.25
# Continuous lime bedding behind dressed blocks fills joints instead of leaving black gaps.
arc=[(C+r*math.cos(t),spring+r*math.sin(t)) for r,seq in [(ri,np.linspace(0,math.pi,65)),(ro,np.linspace(math.pi,0,65))] for t in seq]
poly_solid('Lime-bedded arch substrate',arc,-.035,.066,mortar,.001)
for side in [-1,1]:
 x0=C+side*ri;x1=C+side*ro;poly_solid('Continuous jamb bedding',[(min(x0,x1),.2),(max(x0,x1),.2),(max(x0,x1),spring),(min(x0,x1),spring)],-.035,.066,mortar,.001)
# Unequal course heights and controlled dressed edges. No random surface displacement.
heights=[.2,.60,1.03,1.49,1.92]
for side in [-1,1]:
 for k,(a,b) in enumerate(zip(heights[:-1],heights[1:])):
  inner=C+side*ri;outer=C+side*(ro+[.006,-.003,.004,0][k]);lo=min(inner,outer);hi=max(inner,outer);gap=.003
  # Deliberate chamfered corners and a slight bed slope follow a hand-dressed block, not a soft cube.
  d=.008 if k!=1 else .012;poly=[(lo+d,a+gap),(hi-d,a+gap),(hi,a+gap+d),(hi,b-gap-d),(hi-d,b-gap),(lo+d,b-gap),(lo,b-gap-d),(lo,a+gap+d)]
  poly_solid('Dressed jamb course '+str(side)+' '+str(k),poly,-.035,.135+[.003,-.002,.004,0][k],stone,.004,k+(side+1)*2)
# True radial voussoirs with fitted intrados and a restrained taller central key.
angles=[0,12,25,39,53,67,81,99,114,128,142,155,168,180]
for k,(a,b) in enumerate(zip(angles[:-1],angles[1:])):
 gap=.10;ta=math.radians(a+gap);tb=math.radians(b-gap);key=(a==81);outer=ro+(.024 if key else [0,.004,-.002,.003][k%4]);inner=ri
 poly=[(C+inner*math.cos(t),spring+inner*math.sin(t)) for t in np.linspace(ta,tb,7)]+[(C+outer*math.cos(t),spring+outer*math.sin(t)) for t in np.linspace(tb,ta,7)]
 poly_solid('Fitted keystone' if key else 'Hand-dressed voussoir '+str(k),poly,-.035,.148+(.012 if key else .003*(k%3-1)),stone,.004,k)
# A low seated stone return on the right pier, bonded into the jamb course.
poly_solid('Right pier lower return',[(4.951,.2),(5.255,.2),(5.255,.405),(4.951,.405)],.005,.135,stone,.004,3)
poly_solid('Right pier upper return',[(4.951,.409),(5.255,.409),(5.255,.62),(4.951,.62)],.005,.127,stone,.004,5)
finish('CM_EW11_InnerMasonry')
# Fitted plaster spandrels: actual polygon boundaries track the masonry, not a rectangular cover plate.
# The 10mm bedding overlap is behind stone faces, preventing open seams at imperfect coursing.
rp=1.240
leftedge=[(C+rp*math.cos(t),spring+rp*math.sin(t)) for t in np.linspace(math.pi,math.pi/2,37)]
rightedge=[(C+rp*math.cos(t),spring+rp*math.sin(t)) for t in np.linspace(0,math.pi/2,37)]
left=[(2.23,.2),(C-rp,.2)]+leftedge+[(C,3.205),(2.23,3.205)]
right=[(C+rp,.2),(5.4,.2),(5.4,3.205),(C,3.205)]+list(reversed(rightedge))
poly_solid('Left hand-trowelled spandrel',left,-.006,.038,plaster,.004)
poly_solid('Right hand-trowelled pier and spandrel',right,-.006,.040,plaster,.004)
# Maintenance is part of the rendered thickness: a new lime edge blends into dressed stone at the base.
# A small scalloped edge reveals a lower coat; no paper/ornament/loose masonry added.
patch=[(5.02,.62),(5.26,.62),(5.26,1.32),(5.22,1.35),(5.19,1.32),(5.16,1.37),(5.12,1.35),(5.09,1.32),(5.06,1.34),(5.02,1.29)]
poly_solid('Repaired lime base coat',patch,.035,.043,repair,.001)
finish('CM_EW11_LimeReturns')
# Timber is structural-looking chamfered solid with broad planed faces and a housed scarfed plate.
def post(n,x):
 prof=[(-1,-.72),(-.72,-1),(.72,-1),(1,-.72),(1,.72),(.72,1),(-.72,1),(-1,.72)];vs=[]
 rows=[(.20,x,.070,.075),(.34,x,.073,.075),(.66,x-.003,.066,.070),(1.30,x-.007,.064,.071),(2.10,x-.003,.066,.074),(3.18,x,.070,.075),(3.30,x,.070,.075)]
 for y,cx,w,d in rows:
  for u,v in prof:vs.append((cx+u*w,y,.105+v*d))
 N=8;fs=[tuple(reversed(range(N))),tuple(range(len(vs)-N,len(vs)))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(rows)-1) for i in range(N)];o=mesh(n,vs,fs,wood,.002)
 for f in o.data.polygons:f.use_smooth=False
post('Hand-planed window-side joint post',2.28);post('Corner bearing post',5.33)
# Two pieces form a housed diagonal scarf, not an engraved line over a single beam.
extrude('Scarfed wall plate A',[(2.205,3.20),(4.90,3.20),(4.855,3.245),(4.90,3.30),(2.205,3.30)],.025,.185,b=.002)
extrude('Scarfed wall plate B',[(4.903,3.20),(5.40,3.20),(5.40,3.30),(4.903,3.30),(4.858,3.245)],.025,.185,b=.002)
# Recessed sockets are represented by actual housed shoulder joins, flush oak pins, and short bearing knees.
for x,side in [(2.28,1),(5.33,-1)]:
 curve=bez([(x+side*.23,3.188),(x+side*.14,3.15),(x+side*.10,3.03),(x,2.98)],18)
 extrude('Housed short bearing knee',[(x,3.20),(x+side*.24,3.20)]+curve+[(x,2.98)],.038,.155,b=.004)
 for y in [.42,3.24]:
  # Fingered end grain is subtly dark from the actual texture, not a metal rivet.
  vs=[(x+.009*math.cos(t),y+.009*math.sin(t),z) for z in [.177,.182] for t in np.linspace(0,math.tau,13)[:-1]];fs=[tuple(reversed(range(12))),tuple(range(12,24))]+[(j,(j+1)%12,(j+1)%12+12,j+12) for j in range(12)];mesh('Drawbored oak fixing',vs,fs,wood,.0007)
# A shallow stopped chamfer at the jamb-side edge reads in raking light; no fluting or Victorian capitals.
finish('CM_EW11_FittedTimber')
# Editable unconverted source, then validated transport conversion only.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_EntranceWorkflow11.blend'))
for g,row in modules:
 bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':[r for g,r in modules],'triangles':sum(r['triangles'] for g,r in modules),'opening':{'centerX':3.7,'width':2.0,'springY':spring,'peakY':spring+ri,'floorY':.2},'method':'Dressed radial and coursed masonry; continuous bedding; curved fitted lime spandrels; broad timber arrises, short housed knees, real two-part scarf. No dense displacement.'},indent=2));print('ENTRANCE11_READY',sum(r['triangles'] for g,r in modules))
