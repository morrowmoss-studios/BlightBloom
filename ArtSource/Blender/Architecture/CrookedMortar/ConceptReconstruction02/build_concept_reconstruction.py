"""Concept-derived neutral architecture, built after Analysis/MassingDiagram.png.
A dominant longitudinal roof; B roof dormer; C parallel lower wing;
P deep front porch; D low side shop. Hidden rear dimensions are design inferences.
Unity-plan coordinates (X,Y-up,Z) map to Blender X,Y-ground,Z-up via P.
"""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent
SOURCE=OUT/'CM_ConceptReconstruction02.blend'
EXPORT=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/ConceptReconstruction02/Models/CM_ConceptReconstruction02.fbx'
if (SOURCE.exists() or EXPORT.exists()) and '--refine-created-study' not in __import__('sys').argv:raise RuntimeError('Refusing to overwrite concept reconstruction')
if not bpy.app.background:raise RuntimeError('Use background Blender')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats={}
for key,col in [('Plaster',(.62,.62,.59,1)),('Timber',(.29,.29,.28,1)),('Slate',(.34,.35,.35,1)),('Stone',(.48,.48,.46,1)),('Glass',(.12,.13,.13,1))]:
 m=bpy.data.materials.new('Study_'+key);m.diffuse_color=col;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=1;mats[key]=m
objects=[]
def P(x,y,z):return (x,z,y)
def mesh(name,vs,fs,key,bevel=0):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free()
 if bevel:
  bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Soft architectural edges','BEVEL');mod.width=bevel;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
 o.data.materials.append(mats[key]);objects.append(o);return o

def box(name,loc,dims,key='Plaster',bevel=0):
 x,y,z=loc;a,b,c=[d/2 for d in dims];vs=[P(x+dx*a,y+dy*b,z+dz*c) for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
 return mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],key,bevel)

def wall(name,axis,fixed,start,end,bottom,top,holes=[]):
 # Grid-decompose a straight wall around real openings; join into few semantic meshes later.
 cuts=sorted(set([start,end]+[v for h in holes for v in h[:2] if start<v<end]));ys=sorted(set([bottom,top]+[v for h in holes for v in h[2:] if bottom<v<top]));result=[]
 for a,b in zip(cuts,cuts[1:]):
  for c,d in zip(ys,ys[1:]):
   if any(h[0]<(a+b)/2<h[1] and h[2]<(c+d)/2<h[3] for h in holes):continue
   result.append(box(name,( (a+b)/2,(c+d)/2,fixed) if axis=='X' else (fixed,(c+d)/2,(a+b)/2),(b-a,d-c,.24) if axis=='X' else (.24,d-c,b-a)))
 return result

def arch_cut(o,x,z,base,r,spring,rise):
 poly=[(-r,base-.1),(r,base-.1)]+[(r*math.cos(i*math.pi/32),spring+rise*math.sin(i*math.pi/32)) for i in range(33)]
 n=len(poly);vs=[P(x+a,y,z+depth) for depth in [-.6,.6] for a,y in poly]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 cutter=mesh('TEMP_cut',vs,fs,'Plaster');bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('True arched aperture','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(cutter);bpy.data.objects.remove(cutter,do_unlink=True)

# Floors express connected volumes, not the old rectangular house footprint.
box('Floor_A_MainGround',(0,.1,.9),(5.6,.2,7.8),'Timber')
box('Floor_D_ShopSide',(4.15,.1,.35),(2.7,.2,2.9),'Timber')
box('Floor_C_WorkWingGround',(4.4,.1,4.3),(3.2,.2,5),'Timber')
box('Floor_P_DeepPorch',(0,.1,-4.1),(6.3,.2,2.2),'Stone')
box('Porch_ApproachStep',(.8,.05,-5.45),(2.3,.1,.5),'Stone')
# Main upper floor leaves the actual U-stair void on the left rear.
box('Floor_A_UpperFront',(0,3.25,-1.325),(5.6,.2,3.95),'Timber') # Z -3.3..0.65
box('Floor_A_UpperRight',(1.525,3.25,2.725),(2.55,.2,4.15),'Timber') # X .25..2.8
box('Floor_A_UpperRear',(-1.275,3.25,4.75),(3.05,.2,.10),'Timber')
box('Floor_C_UpperStudy',(4.4,3.25,4.3),(3.2,.2,5),'Timber')
# Main body front lower wall: offset door and display window behind a deep porch.
front=box('Shell_A_FrontGround',(0,1.775,-3),(5.6,3.15,.24))
arch_cut(front,.8,-3,.1,.702,1.7,.95)
# Display aperture is below the porch, not a second entrance.
cut=box('TEMP_DisplayCut',(-1.55,1.65,-3),(1.45,1.4,1.2));bpy.context.view_layer.objects.active=front;mod=front.modifiers.new('Front shop display opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
# Upper gable end projects 0.30m over the recessed ground-level door wall.
fupper=box('Shell_A_FrontUpper_Jetty',(0,4.75,-3.3),(5.6,2.80,.24));arch_cut(fupper,-.25,-3.3,4.35,.8,5.0,.65)
wall('Shell_A_West','Z',-2.8,-3,4.8,.2,6.15,[(-1.7,-.3,1.1,2.4),(1.2,2.6,4.4,5.6)])
wall('Shell_A_Rear','X',4.8,-2.8,2.8,.2,6.15,[(.8,2.4,.2,2.8)])
# Main visible long elevation: upper arch above the low shop-side roof.
side=box('Shell_A_EastUpper',(2.8,4.75,.9),(.24,2.8,7.8))
# Arched side window, perpendicular to the main gable. Rotate cutter around Y in plan.
r=.70;spring=5.05;rise=.585;base=4.465;centre=.25
poly=[(-r,base),(r,base)]+[(r*math.cos(i*math.pi/28),spring+rise*math.sin(i*math.pi/28)) for i in range(29)];n=len(poly)
vs=[P(x,y,centre+z) for x in [2.1,3.5] for z,y in poly];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
cut=mesh('TEMP_SideArch',vs,fs,'Plaster');bpy.context.view_layer.objects.active=side;mod=side.modifiers.new('Side upper arch','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
# Upper connection into the parallel study wing must also cut the continuous main elevation.
cut=box('TEMP_UpperStudyDoor',(2.8,4.5,3.25),(1.2,2.3,1.6));bpy.context.view_layer.objects.active=side;mod=side.modifiers.new('Actual upstairs study passage','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
# Ground right wall is open to the shop-side projection; rear portion connects treatment to workroom.
wall('Shell_A_EastGroundFront','Z',2.8,-3,-1.1,.2,3.35)
wall('Interior_A_D_ShopLink','Z',2.8,-1.1,1.8,.2,3.35,[(-.6,1.2,.2,2.9)])
wall('Interior_A_C_GroundLink','Z',2.8,1.8,4.8,.2,3.35,[(2.65,4.25,.2,2.9)])
# C is a genuinely smaller parallel wing, with upper study under its lower gable.
cf=box('Shell_C_FrontUpper',(4.4,4.5,1.8),(3.2,2.3,.24));arch_cut(cf,4.4,1.8,4.53,.64,5.05,.52)
wall('Interior_D_C_FrontGround','X',1.8,2.8,6,.2,3.35,[(3.45,5.25,.2,2.9)])
wall('Shell_C_East','Z',6,1.8,6.8,.2,5.65,[(3.4,4.6,1.1,2.4),(4.2,5.6,4.25,5.35)])
wall('Shell_C_Rear','X',6.8,2.8,6,.2,5.65,[(3.5,5.1,.2,2.9)])
wall('Interior_A_C_UpperLink','Z',2.8,1.8,4.8,3.35,5.65,[(2.45,4.05,3.35,5.65)])
wall('Shell_C_WestReturn','Z',2.8,4.8,6.8,.2,5.65)
# D: one-storey side shop projection with a large right-facing display.
wall('Shell_D_Front','X',-1.1,2.8,5.5,.2,3.05)
wall('Shell_D_East','Z',5.5,-1.1,1.8,.2,3.05,[(-.65,1.20,.95,2.55)])
wall('Shell_D_BackCorner','X',1.8,5.5,6,.2,3.05)
# Compact adapted interior: treatment rear-right, U stairs rear-left, workspace/storage in C.
wall('Interior_Treatment_Front','X',.75,.25,2.8,.2,3.15,[(.65,2.2,.2,2.9)])
wall('Interior_Stair_Treatment','Z',.25,.75,4.8,.2,3.15)
wall('Interior_C_PrepStorage','X',4.6,2.8,6,.2,3.15,[(3.4,5.0,.2,2.9)])
wall('Interior_UpperBedroom','Z',-.05,-3.3,.4,3.35,5.9,[(-.7,.4,3.35,5.9)])
# U stair: 18 x .175m rises, 9 treads each way, with a full turning landing.
step=.175;tread=.29;start=.75;turn=3.36
for flight,(left,right,ascending) in enumerate([(-2.6,-1.35,True),(-1.15,.1,False)]):
 prof=[(start,.2 if ascending else 1.775)]
 if ascending:
  for i in range(9):prof += [(start+i*tread,.2+(i+1)*step),(start+(i+1)*tread,.2+(i+1)*step)]
  prof += [(turn,.2)]
 else:
  # Return flight rises while walking back toward the front.
  prof=[(start,1.775),(start,3.35)]
  for i in range(9):prof += [(start+(i+1)*tread,3.35-i*step),(start+(i+1)*tread,3.35-(i+1)*step)]
  prof += [(turn,1.775)]
 prof=[v for i,v in enumerate(prof) if i==0 or (Vector(v)-Vector(prof[i-1])).length>1e-7]
 n=len(prof);vs=[P(x,y,z) for x in [left,right] for z,y in prof];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh('Stairs_U_Flight_'+str(flight),vs,fs,'Timber')
box('Stairs_U_MidLanding',(-1.25,1.675,4.03),(2.7,.2,1.34),'Timber')
# Solid side guards for collision safety; leave turning landing and top approach clear.
wall('Stairs_Guard_UpperRight','Z',.16,.75,4.7,3.35,4.40)
wall('Stairs_Guard_UpperFront','X',.68,-2.75,-1.20,3.35,4.40)
# Roof masses — actual longitudinal roof + cross-dormer + parallel smaller wing.
def roof(name,axis,profile,a,b):
 n=len(profile);vs=[P(u,h,end) if axis=='Z' else P(end,h,u) for end in [a,b] for u,h in profile];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return mesh(name,vs,fs,'Slate')
main_profile=[(-3.25,5.92),(-2.7,6.22),(-1.45,8.75),(-.35,10.25),(.55,9.15),(2.35,6.52),(3.3,5.96)]
main=roof('Roof_A_DominantLongitudinal','Z',main_profile,-3.65,5.15)
dormer=roof('TEMP_B_Dormer','X',[(-.45,6.05),(-.45,6.9),(.55,8.1),(1.55,6.9),(1.55,6.05)],.5,2.95)
bpy.context.view_layer.objects.active=main;mod=main.modifiers.new('B structural cross dormer union','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=dormer;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(dormer);bpy.data.objects.remove(dormer,do_unlink=True)
# A real recessed dormer window: cutter stops inside the attic mass.
cut=box('TEMP_DormerRecess',(2.93,6.975,.55),(.8,.95,.85));bpy.context.view_layer.objects.active=main;mod=main.modifiers.new('Dormer window reveal','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
wing=roof('Roof_C_ParallelLowerGable','Z',[(2.45,5.65),(3,6.0),(4.35,7.7),(5.7,6.05),(6.35,5.65)],1.45,7.1)
# Lean-to roof prisms, genuine depth and thickness rather than applied facade caps.
def lean(name,corners):
 vs=[P(x,y+dy,z) for dy in [-.14,0] for x,y,z in corners];return mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Slate')
porch=lean('Roof_P_DeepEntrancePorch',[(-3.5,4.0,-2.95),(3.5,4.0,-2.95),(3.5,3.05,-5.4),(-3.5,3.05,-5.4)])
side_roof=lean('Roof_D_LowShopLeanTo',[(2.65,4.0,-1.4),(2.65,4.0,2.0),(5.8,3.02,2.0),(5.8,3.02,-1.4)])
for o in [main,wing]:
 o.data.materials.clear()
 for k in ['Slate','Plaster','Timber']:o.data.materials.append(mats[k])
 for p in o.data.polygons:p.material_index=1 if abs(p.normal.z)<.06 else (2 if p.normal.z<0 else 0)
# Fundamental supporting members only; no decorative timbers or greenery.
def beam(name,a,b,width=.15):
 a,b=Vector(P(*a)),Vector(P(*b));delta=b-a;bpy.ops.mesh.primitive_cube_add(size=1,location=(a+b)/2);o=bpy.context.object;o.name=name;o.dimensions=(width,width,delta.length);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);o.data.materials.append(mats['Timber']);objects.append(o);return o
for x in [-3.05,3.05]:
 beam('Porch_SupportPost',(x,.2,-5.10),(x,2.94,-5.10),.18)
 beam('Porch_KneeBrace',(x,2.25,-5.10),(x,3.22,-4.3),.13)
beam('Porch_FrontBeam',(-3.25,2.93,-5.10),(3.25,2.93,-5.10),.20)
beam('Porch_WallLedger',(-3.2,3.82,-2.98),(3.2,3.82,-2.98),.18)
beam('Jetty_SupportBeam',(-2.9,3.27,-3.32),(2.9,3.27,-3.32),.18)
for (x,y),(xx,yy) in zip(main_profile,main_profile[1:]):beam('Roof_A_ProfileBargeboard',(x,y,-3.68),(xx,yy,-3.68),.15)
for a,b in [((-3.25,5.92,-3.65),(-3.25,5.92,5.15)),((3.3,5.96,-3.65),(3.3,5.96,5.15)),((2.45,5.65,1.42),(4.35,7.7,1.42)),((4.35,7.7,1.42),(6.35,5.65,1.42))]:beam('Roof_EaveStructure',a,b,.13)
# Staggered chimney volumes deliberately reproduce the reference's roof accents.
box('Chimney_MainTall',(1.9,5.7,3.9),(.9,11.0,.95),'Stone')
box('Chimney_MainCap',(1.9,11.28,3.9),(1.15,.20,1.20),'Stone')
for x,h in [(1.67,11.65),(2.1,11.56)]:box('Chimney_MainPot',(x,h,3.9),(.22,.55,.25),'Stone')
box('Chimney_Secondary',(-1.5,5.2,3.2),(.55,10.0,.55),'Stone')
box('Chimney_SecondaryCap',(-1.5,10.3,3.2),(.77,.18,.75),'Stone')
# Purposeful non-hero window openings and quiet neutral frames.
def window(name,axis,fixed,c,bottom,width,height):
 if axis=='X':
  box(name+'_Recess',(c,bottom+height/2,fixed),(width,height,.035),'Glass')
  for v in [-1,1]:box(name+'_Frame',(c+v*width/2,bottom+height/2,fixed-.03),(.075,height+.10,.10),'Timber')
  for y in [bottom,bottom+height]:box(name+'_Frame',(c,y,fixed-.03),(width+.10,.075,.10),'Timber')
 else:
  box(name+'_Recess',(fixed,bottom+height/2,c),(.035,height,width),'Glass')
  for v in [-1,1]:box(name+'_Frame',(fixed,bottom+height/2,c+v*width/2),(.10,height+.10,.075),'Timber')
  for y in [bottom,bottom+height]:box(name+'_Frame',(fixed,bottom+height/2,c),(.10,.075,width+.10),'Timber')
window('Window_FrontShop','X',-3.14,-1.55,.95,1.45,1.4)
window('Window_D_ShopSide','Z',5.64,.275,.95,1.85,1.6)
window('Window_A_WestGround','Z',-2.94,-1.0,1.1,1.4,1.3)
window('Window_A_WestUpper','Z',-2.94,1.9,4.4,1.4,1.2)
window('Window_C_WorkGround','Z',6.14,4.0,1.1,1.2,1.3)
window('Window_C_UpperStudy','Z',6.14,4.9,4.25,1.4,1.1)
window('Window_B_Dormer','Z',2.55,.55,6.50,.85,.95)
# Minimal upper dormer frame is on its true front plane; recessed glazing is farther back.
for z in [.125,.975]:box('Window_B_Dormer_FrontFrame',(2.975,6.975,z),(.1,1.05,.075),'Timber')
for y in [6.5,7.45]:box('Window_B_Dormer_FrontFrame',(2.975,y,.55),(.1,.075,.95),'Timber')
# Consolidate roles into logical meshes, keeping roof systems separate for silhouette iteration.
def category(o):
 n=o.name
 for k in ['Roof','Floor','Stairs']:
  if n.startswith(k):return n.split('.')[0]
 for k in ['Shell','Interior','Porch','Jetty','Chimney','Window']:
  if n.startswith(k):return k
 return n
by={}
for o in objects:by.setdefault(category(o),[]).append(o)
final=[]
for key,items in by.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in items:o.select_set(True)
 bpy.context.view_layer.objects.active=items[0]
 if len(items)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=key;final.append(o)
# UVs retained for future asset work; neutral study has no painted texture dependency.
bpy.ops.object.select_all(action='DESELECT')
for o in final:o.select_set(True)
bpy.context.view_layer.objects.active=final[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.003);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
report={'asset':'CM_ConceptReconstruction02','reference_analysis':'Analysis/MassingDiagram.png','key_geometry':{'A_core':[-2.8,2.8,-3,4.8],'C_parallel_wing':[2.8,6,1.8,6.8],'D_low_side_shop':[2.8,5.5,-1.1,1.8],'P_open_porch':[-3.15,3.15,-5.2,-3],'main_ridge':10.25,'dormer_ridge':8.1,'parallel_wing_ridge':7.7,'porch_depth':2.2},'floors':[.2,3.35],'stairs':{'type':'U','risers':18,'rise':.175,'tread':.29,'flight_width':1.25,'turning_landing_depth':1.34},'parts':[]}
for o in final:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();assert bad==0 and vol>0,(o.name,bad,vol)
 o.data.calc_loop_triangles();report['parts'].append({'name':o.name,'triangles':len(o.data.loop_triangles),'nonmanifold':bad,'volume':vol})
report['triangles']=sum(p['triangles'] for p in report['parts']);report['mesh_count']=len(final)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
# Established static axis conversion, export only. Source remains +X/+Y/+Z.
conversion=Matrix.Rotation(math.pi,4,'Z')
for o in final:o.matrix_world=conversion@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(EXPORT),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False)
(OUT/'geometry_validation.json').write_text(json.dumps(report,indent=2));print('CONCEPT_STUDY_READY',json.dumps({k:v for k,v in report.items() if k!='parts'}))
