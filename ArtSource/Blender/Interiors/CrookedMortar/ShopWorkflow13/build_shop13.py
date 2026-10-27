"""Reference-led fitted shop reconstruction. Authored sections/profiles/lathed vessels; no room regeneration."""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[]
def material(n,col,path=None):
 m=bpy.data.materials.new(n);m.diffuse_color=col;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=.9
 if path:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(path));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=material('CM_SW13_PaintedWalnut',(.35,.19,.08,1),A/'Textures/CM_SW13_PaintedWalnut.png');sage=material('CM_SW13_Sage',(.19,.25,.15,1));brass=material('CM_SW13_AgedBrass',(.37,.23,.08,1));iron=material('CM_SW13_Iron',(.09,.085,.06,1));ceramic=material('CM_SW13_IvoryCeramic',(.61,.56,.40,1));amber=material('CM_SW13_AmberVessel',(.22,.11,.035,1));green=material('CM_SW13_SageVessel',(.15,.25,.12,1));paper=material('CM_SW13_Paper',(.60,.53,.36,1));labels=material('CM_SW13_HerbLabels',(1,1,1,1),A/'Textures/CM_SW13_HerbLabels.png')
t=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(t[t.index('def smooth('):t.index('ogee=')])
t=(D.parent/'ShopWorkflow10/build_shop10.py').read_text();exec(t[t.index('def timber('):t.index('# Medicine cabinet:')])
# Per-member UV offsets, no repeated stripe patch on every board.
mesh0=mesh
serial=0
def mesh(n,vs,fs,m=None,bevel=0,register=True):
 global serial
 o=mesh0(n,vs,fs,m or wood,bevel,register);serial+=1
 if o.data.materials[0]==wood:
  uv=o.data.uv_layers[0]
  for l in uv.data:l.uv.x=l.uv.x*.65+.163*(serial%5);l.uv.y=l.uv.y*.76+.097*(serial%7)
 return o
# Gentle bowed members, broad chamfers, joint-bearing shoulders. Avoid dense sculpt noise.
def rail(n,x0,x1,y,z,h=.06,d=.05):
 path=[(x,y+.006*math.sin((x-x0)/(x1-x0)*math.pi),z) for x in np.linspace(x0,x1,25)]
 return profile_sweep(n,path,[(-h,-d),(-h,.005),(-h*.65,.018),(h*.25,.025),(h,.008),(h,-d)])
def peg(n,x,y,z,r=.009,m=None):
 N=10;vs=[(x+r*math.cos(i*math.tau/N),y+r*math.sin(i*math.tau/N),q) for q in [z,z+.004] for i in range(N)]
 return mesh(n,vs,[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m or wood)
def arch_apron(n,a,b,y,z,drop=.18):
 c=bez([(a,y-drop),(a+(b-a)*.20,y-.045),(b-(b-a)*.20,y-.045),(b,y-drop)],20)
 return extrude(n,[(a,y),(b,y)]+list(reversed(c)),z-.065,z,b=.005)
# Fitted apothecary cabinet: old 1.86m wide footprint; extends upward into previously blank wall.
for side in [-1,1]:
 inside=bez([(side*.77,.003),(side*.74,.70),(side*.79,1.95),(side*.77,2.91)],24)
 outside=bez([(side*.92,.003),(side*.85,.75),(side*.94,2.06),(side*.92,2.93)],24)
 extrude('Continuous fitted cabinet standard',inside+list(reversed(outside)),-.18,.17,b=.008)
 for y in [.22,.48,1.42,2.34,2.82]:peg('Flush drawbore pin',side*.845,y,.173)
# Divided, inset planked backing has a gentle concavity and short intentional grain.
for k in range(7):
 x=-.74+k*.245
 extrude('Inset sage back',[(x-.120,.08),(x+.120,.08),(x+.120,2.85),(x-.120,2.85)],-.177,-.151,sage,.004)
for y in [.52,.98,1.44,1.90,2.37,2.84]:shaped_shelf('Continuous nosed cabinet shelf',1.79,.17,y)
# Tall top register of three arched niches; larger rhythm instead of a thin furniture crown.
for a,b in [(-.77,-.28),(-.25,.25),(.28,.77)]:arch_apron('Arched upper register',a,b,2.83,.178,.24)
for x in [-.265,.265]:timber('Upper register mullion',(x,2.38,.12),(x,2.83,.12),.035,.09,.002)
for a,b in [(-.77,-.02),(.02,.77)]:arch_apron('Lower shelf bearing arch',a,b,.51,.17,.12)
# Carved sign frieze is a real recessed board (plain blank for future shop lettering, not a new poster).
crest=bez([(-.93,2.86),(-.70,2.94),(-.30,2.88),(0,3.03)],24)+bez([(0,3.03),(.30,2.88),(.71,2.96),(.93,2.88)],24)[1:]
extrude('Broad swept cabinet cornice',[(-.93,2.82),(.93,2.82)]+list(reversed(crest)),-.18,.165,b=.006)
rail('Cabinet crown cove',-.92,.92,2.84,.175,.035,.05)
# Eight small fitted remedy drawers below existing first shelf datum; no loose decoration.
for j in range(2):
 for i in range(4):
  x=-.60+i*.40;y=.07+j*.205
  extrude('Mortised herb drawer',[(x-.184,y),(x+.184,y),(x+.184,y+.174),(x-.184,y+.174)],-.11,.169,b=.006)
  extrude('Recessed drawer field',[(x-.146,y+.035),(x+.146,y+.035),(x+.146,y+.141),(x-.146,y+.141)],.170,.172,sage,.003)
  peg('Cast drawer pull backplate',x,y+.088,.176,.016,brass)
  # a small real drop handle loop, broad enough to read without ornate microgeometry
  path=[(x+.025*math.cos(t),y+.065+.023*math.sin(t),.195) for t in np.linspace(0,math.tau,17)]
  # vertical XY sweep frame; closed path tangent does not vanish
  profile_sweep('Drawer pull loop',path,[(-.003,-.003),(.003,-.003),(.004,.002),(-.003,.003)]).data.materials[0]=brass
finish('CM_SW13_FittedApothecaryCabinet')
# Replacement original medicine stock: deliberate bottle families, rolled necks, corks and fitted labels.
def lathe(n,x,y,z,height,radius,profile,m):
 N=20;vs=[]
 for h,r in profile:
  for i in range(N):
   a=i*math.tau/N;vs.append((x+math.sin(a)*radius*r,y+height*h,z+math.cos(a)*radius*r))
 fs=[tuple(reversed(range(N))),tuple(range((len(profile)-1)*N,len(profile)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(profile)-1) for i in range(N)]
 return mesh(n,vs,fs,m)
def label(n,x,y,z,r,h,index):
 N=12;vs=[]
 for yy in [y,y+h]:
  for a in np.linspace(-1.05,1.05,N):vs.append((x+math.sin(a)*r,yy,z+math.cos(a)*r))
 fs=[(i,i+1,N+i+1,N+i) for i in range(N-1)];o=mesh(n,vs,fs,labels);uv=o.data.uv_layers[0];cx=index%3;cy=1-index//3
 for f in o.data.polygons:
  for li in f.loop_indices:
   vi=o.data.loops[li].vertex_index;row,k=divmod(vi,N);uv.data[li].uv=((cx+.08+.84*k/(N-1))/3,(cy+.08+.84*row)/2)
 return o
jar=[(0,.80),(.025,.95),(.08,1),(.70,1),(.80,.93),(.85,.78),(.92,.78),(.94,.90),(.99,.9),(1,.78)]
bottle=[(0,.7),(.035,.9),(.12,1),(.58,.96),(.70,.70),(.78,.34),(.91,.34),(.93,.45),(.98,.45),(1,.34)]
# Same four stock-bearing levels, deliberately grouped in families with calm negative space.
for row,y in enumerate([.52,.98,1.44,1.90]):
 for i,x in enumerate([-.62,-.31,0,.31,.62]):
  is_bottle=(i+row)%3==0;h=(.30 if is_bottle else .255)+.015*((i+2*row)%3);r=.074 if is_bottle else .092;z=.025+.012*((i+row)%2);m=[ceramic,amber,green][(i+row)%3]
  lathe('Lathed remedy bottle' if is_bottle else 'Shouldered medicinal jar',x,y,z,h,r,bottle if is_bottle else jar,m)
  neck=.37 if is_bottle else .81;lathe('Cork stopper',x,y+h*.96,z,h*.13,r*neck,[(0,.94),(.20,1),(1,.96)],wood)
  label('Registered hand-lettered remedy label',x,y+h*.20,z,r*1.015,h*.43,(i+row)%6)
# Two closed folios in the top register are built-in reference records, not random shelf stuffing.
for x in [-.52,.05]:
 extrude('Reference folio cover',[(x-.13,2.39),(x+.13,2.39),(x+.13,2.65),(x-.13,2.65)],-.07,.035,sage,.004)
finish('CM_SW13_RemedyDisplay')
# Fitted east-wall records cupboard: preserves existing mounting and retained contents.
for side in [-1,1]:
 inside=bez([(side*.57,.02),(side*.55,.32),(side*.60,.66),(side*.56,.86)],18)
 outside=bez([(side*.67,.02),(side*.70,.27),(side*.65,.66),(side*.68,.89)],18)
 extrude('Register case shaped cheek',inside+list(reversed(outside)),0,.27,b=.005)
for y in [.10,.42,.76]:shaped_shelf('Fitted register shelf',1.28,.28,y,0)
extrude('Register sage back',[(-.59,.04),(.59,.04),(.59,.86),(-.59,.86)],0,.035,sage,.004)
crest=bez([(-.68,.77),(-.48,.96),(-.23,.82),(0,.97)],18)+bez([(0,.97),(.23,.82),(.48,.96),(.68,.77)],18)[1:]
extrude('Register bearing crown',[(-.68,.74),(.68,.74)]+list(reversed(crest)),0,.25,b=.005)
for a,b in [(-.57,-.02),(.02,.57)]:arch_apron('Register shelf apron',a,b,.74,.26,.13)
finish('CM_SW13_RecordsCase')
# All shop interior structural finish reconstructed in one module, replacing earlier thin batches.
for x in [.12,5.26]:
 timber('Hewn shop tie standard',(x,.203,1.9),(x,3.21,1.9),.19,.20,.012)
 for y in [2.79,2.98]:peg('Tie joint drawbore',x,y,2.007,.012)
timber('Slightly cambered principal tie',(.12,3.07,1.9),(5.26,3.07,1.9),.25,.27,.018)
for side,x in [(1,.12),(-1,5.26)]:
 outside=bez([(x,2.56),(x+side*.10,2.84),(x+side*.41,3.03),(x+side*.68,3.06)],24)
 inside=bez([(x+side*.075,2.58),(x+side*.22,2.86),(x+side*.45,2.94),(x+side*.69,2.98)],24)
 extrude('Housed curved tie bearing',outside+list(reversed(inside)),1.80,2.0,b=.007)
# Correct frame datums around the existing treatment and kitchen openings.
for x in [2.47,4.73]:timber('Treatment opening standard',(x,.203,4.35),(x,3.22,4.35),.16,.12,.006)
timber('Treatment lintel',(2.47,3.13,4.35),(4.73,3.13,4.35),.17,.12,.005)
for z in [1.96,4.04]:timber('Kitchen opening standard',(5.33,.203,z),(5.33,3.22,z),.16,.12,.006)
timber('Kitchen opening lintel',(5.33,3.13,1.96),(5.33,3.13,4.04),.17,.12,.006)
for x in [.70,2.30,3.90,5.05]:timber('Hand-planed ceiling joist',(x,3.23,.08),(x,3.23,4.32),.15,.16,.008)
timber('West bearing plate',(.09,3.16,.10),(.09,3.16,1.83),.17,.18,.007)
timber('Window head bearing plate',(.19,3.13,.08),(2.18,3.13,.08),.18,.15,.009)
for x in [.35,2.22]:timber('Inner window reveal casing',(x,1.16,.065),(x,3.04,.065),.10,.13,.004)
slab('Deep joined window sill',[(.35,-.01),(2.22,-.01),(2.25,.15),(2.16,.18),(.40,.18),(.32,.13)],1.19,1.27,.007)
finish('CM_SW13_StructuralJoinery')
# Save editable native source before the established metric Unity axis conversion.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
for g,row in modules:
 bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':[r for g,r in modules],'triangles':sum(r['triangles'] for g,r in modules),'originalStockCoursesReplaced':4,'medicineVessels':20},indent=2));print('SHOP13_READY',sum(r['triangles'] for g,r in modules))
