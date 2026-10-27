"""Fixed-layout reference-element reconstruction. New masonry and stair visuals; no collision regeneration."""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow14'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[]
def mat(n,tex=None,c=(1,1,1,1)):
 m=bpy.data.materials.new(n);m.diffuse_color=c;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=c;bs.inputs['Roughness'].default_value=.94
 if tex:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(A/'Textures'/tex));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=mat('CM_SW14_WorkedWalnut','CM_SW14_WorkedWalnut.png');stone=mat('CM_SW14_DressedStone','CM_SW14_DressedStone.png');lime=mat('CM_SW14_LayeredLime','CM_SW14_LayeredLime.png');mortar=mat('CM_SW14_LimeBedding',None,(.40,.36,.28,1));lead=mat('CM_SW14_DullLead',None,(.15,.16,.12,1))
t=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(t[t.index('def smooth('):t.index('ogee=')]);t=(D.parent/'ShopWorkflow10/build_shop10.py').read_text();exec(t[t.index('def timber('):t.index('# Medicine cabinet:')])
# Distinct UV origins for each member while retaining physical grain scale.
mesh_base=mesh
member=0
def mesh(n,vs,fs,m=wood,bevel=0,register=True):
 global member
 o=mesh_base(n,vs,fs,m,bevel,register);member+=1
 if m==wood:
  for li in o.data.uv_layers[0].data:li.uv.x+=.173*(member%7);li.uv.y+=.117*(member%5)
 return o
# At fixed inner radius the reveal remains unchanged. Each dressed stone has a radial bed,
# asymmetric broad front tool planes, shallow arris loss, and a connected closed return.
def stoneuv(o,index):
 uv=o.data.uv_layers[0];coords=[v.co for v in o.data.vertices];lo=Vector(tuple(min(v[i] for v in coords) for i in range(3)))
 for f in o.data.polygons:
  axes=[i for i in range(3) if i!=max(range(3),key=lambda i:abs(f.normal[i]))]
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co-lo;uv.data[li].uv=(.08+(index*.173)% .47+co[axes[0]]/.95,.06+(index*.127)% .39+co[axes[1]]/1.6)
 # subtle per-stone painted tone; no checkerboard material assignments
 at=o.data.color_attributes.new(name='PaintedCavity',type='FLOAT_COLOR',domain='POINT')
 for v in o.data.vertices:
  shade=.93+.035*math.sin(index*1.7);at.data[v.index].color=(shade,shade,shade,1)
def dressed(n,poly,index):
 o=extrude(n,poly,-.034,.160+.004*math.sin(index*2.1),stone,.009)
 bm=bmesh.new();bm.from_mesh(o.data);front=[f for f in bm.faces if f.normal.y>.96 and f.calc_center_median().y>.145]
 bmesh.ops.triangulate(bm,faces=front);ed=list({e for f in bm.faces if f.normal.y>.95 and f.calc_center_median().y>.145 for e in f.edges});bmesh.ops.subdivide_edges(bm,edges=ed,cuts=2,use_grid_fill=True)
 for v in bm.verts:
  if v.co.y>.149:v.co.y-=.0035*(.5+.5*math.sin(v.co.x*8+index))*(.5+.5*math.cos(v.co.z*5-index))
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();stoneuv(o,index)
 for f in o.data.polygons:f.use_smooth=False
 return o
C=3.7;spring=1.92;ri=1.;ro=1.25
arc=[(C+r*math.cos(t),spring+r*math.sin(t)) for r,seq in [(ri+.012,np.linspace(0,math.pi,55)),(ro,np.linspace(math.pi,0,55))] for t in seq]
extrude('Continuous recessed lime arch bed',arc,-.035,.065,mortar,.001)
heights=[.2,.60,1.03,1.49,1.92]
for side in [-1,1]:
 lo=min(C+side*(ri+.012),C+side*ro);hi=max(C+side*(ri+.012),C+side*ro)
 extrude('Bonded lime jamb bed',[(lo,.2),(hi,.2),(hi,spring),(lo,spring)],-.035,.065,mortar,.001)
 for k,(a,b) in enumerate(zip(heights[:-1],heights[1:])):
  edge=side*.003*math.sin(k*2.2);inner=C+side*ri;outer=C+side*ro+edge;lo=min(inner,outer);hi=max(inner,outer);dressed('Dressed jamb '+str(side)+' '+str(k),[(lo,a+.003),(hi,a+.003),(hi,b-.003),(lo,b-.003)],k+(0 if side<0 else 4))
angles=[0,12,25,39,53,67,81,99,114,128,142,155,168,180]
for k,(a,b) in enumerate(zip(angles[:-1],angles[1:])):
 ta,tb=math.radians(a+.13),math.radians(b-.13);outer=ro+(.022 if a==81 else .002*math.sin(k*1.6))
 poly=[(C+ri*math.cos(t),spring+ri*math.sin(t)) for t in np.linspace(ta,tb,6)]+[(C+outer*math.cos(t),spring+outer*math.sin(t)) for t in np.linspace(tb,ta,6)]
 dressed('Individually dressed radial arch stone '+str(k),poly,k+8)
for i,(a,b) in enumerate([(.2,.405),(.409,.62)]):dressed('Bonded pier return '+str(i),[(4.951,a),(5.255,a),(5.255,b),(4.951,b)],i+22)
finish('CM_SW14_DressedEntrance')
# Visible stairs are rebuilt on measured original world datums; physics steps stay untouched.
rows=json.loads((D/'MeasuredStairs.json').read_text());oldsteps=[]
for row in rows:
 if '/Lower tread ' not in row['path'] and '/Upper tread ' not in row['path']:continue
 vv=np.array(row['vertices']);lo=vv.min(0);hi=vv.max(0);x0,y0,z0=lo;x1,y1,z1=hi;upper='/Upper tread ' in row['path'];num=int(row['path'].rsplit(' ',1)[1]);oldsteps.append(row['path'])
 # Three broad boards with a tiny flush joint; top stays exactly on approved walk datum.
 for j in range(3):
  xa=x0+(x1-x0)*j/3;xb=x0+(x1-x0)*(j+1)/3
  slab(('Upper' if upper else 'Lower')+' tread '+str(num)+' fitted board '+str(j),[(xa+.001,z0+.001),(xb-.001,z0+.001),(xb-.001,z1-.001),(xa+.001,z1-.001)],y1-.047,y1,.005)
 # Closed riser to preceding tread. No open stair trap; original foot-support envelope retained.
 a=y1-(1.7/9)-.005;riser=extrude('Recessed framed riser '+str(num),[(x0+.004,a),(x1-.004,a),(x1-.004,y1-.043),(x0+.004,y1-.043)],z0,z1,wood,.002)
 # Dressed nosing profile is contained in original .30m depth and below walking plane.
 zz=z1-.010 if upper else z0+.010
 path=[(x,y1-.021,zz) for x in np.linspace(x0+.008,x1-.008,16)]
 profile_sweep('Hand-planed rounded stair nose',path,[(-.020,-.006),(-.020,.005),(-.014,.012),(.009,.012),(.020,.003),(.020,-.006)])
 if not upper:
  # Existing lower flight is solid; a single fitted side field covers same vertical profile.
  extrude('Solid lower step cheek',[(x1-.024,.2),(x1-.006,.2),(x1-.006,y1-.047),(x1-.024,y1-.047)],z0+.001,z1-.001,wood,.002)
finish('CM_SW14_StairTreads')
# Export exact old floor construction with corrected stone UVs, not regenerated flagstones.
row=next(r for r in json.loads((D/'MeasuredSurfaces.json').read_text()) if r['name']=='CM_SW10_FlagstoneFloor')
o=mesh('Retained flagstones - corrected hand-painted stone UV',row['vertices'],[tuple(row['triangles'][i:i+3]) for i in range(0,len(row['triangles']),3)],stone)
stoneuv(o,2);finish('CM_SW14_FlagstoneFinish')
# Existing lime surfaces: exact triangle positions, newly registered physical-scale UVs and edge tint.
for row in json.loads((D/'MeasuredSurfaces.json').read_text()):
 if row['name'] not in ['CM_EW11_PreservedOtherPlaster','CM_EW11_LimeReturns']:continue
 o=mesh('Retained lime surface '+row['name'],row['vertices'],[tuple(row['triangles'][i:i+3]) for i in range(0,len(row['triangles']),3)],lime)
 uv=o.data.uv_layers[0]
 for f in o.data.polygons:
  axis=0 if abs(f.normal.y)>.5 else 1
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axis]/1.8,v.z/3.6)
 at=o.data.color_attributes.new(name='PaintedCavity',type='FLOAT_COLOR',domain='POINT')
 for v in o.data.vertices:
  y=v.co.z;floorfade=max(0,1-(y-.2)/.5);ceilingfade=max(0,1-abs(y-3.20)/.22)
  value=1-.11*floorfade-.10*ceilingfade;at.data[v.index].color=(value,value,value,1)
finish('CM_SW14_RegisteredLime')
# Lead bars are fitted to original rectangular glazing in the paired casements, not new windows.
for x in [.91,1.69]:
 for y in [1.67,2.18,2.69]:
  o=timber('Existing casement lead crossbar',(x-.253,y,-.251),(x+.253,y,-.251),.018,.016,.002);o.data.materials[0]=lead
 o=timber('Existing casement central lead',(x,1.35,-.251),(x,2.87,-.251),.015,.016,.002);o.data.materials[0]=lead
finish('CM_SW14_FittedWindowLeads')
# Consistent grain on stair boards and molded stone UVs. One material group per module.
for g,row in modules:
 g.data.calc_loop_triangles();row['triangles']=len(g.data.loop_triangles)
 bpy.context.view_layer.objects.active=g
 while len(g.data.uv_layers)>1:g.data.uv_layers.remove(g.data.uv_layers[-1])
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow14.blend'))
for g,row in modules:
 bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':[r for g,r in modules],'triangles':sum(r['triangles'] for g,r in modules),'replacedVisualSteps':oldsteps},indent=2));print('SHOP14_READY',sum(r['triangles'] for g,r in modules))
