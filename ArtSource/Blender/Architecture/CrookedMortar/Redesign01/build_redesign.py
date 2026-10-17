"""Crooked Mortar architectural redesign: authored massing and functional shell.
Coordinates in plan are Unity metres (x,y-up,z); P maps them into Blender.
Separate visual/collision meshes, no edits to existing source assets.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent
SOURCE=OUT/'CM_Redesign01_Geometry.blend'
if SOURCE.exists() and '--refine-created-design' not in sys.argv:raise RuntimeError('Refusing to overwrite existing redesign source')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats={}
for key,col in [('Plaster',(.72,.66,.54,1)),('Timber',(.24,.16,.10,1)),('Slate',(.33,.38,.36,1)),('Stone',(.56,.53,.46,1)),('Glass',(.26,.30,.27,1))]:
 m=bpy.data.materials.new('Redesign_'+key);m.diffuse_color=col;m.use_nodes=True;mats[key]=m
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

# Ground floor at 0.20m, upper floor at 3.50m.
box('Floor_Shop',(-3,.10,-1.5),(5,.2,9),'Timber')
box('Floor_Residential',(2.9,.10,1.65),(6.8,.2,8.3),'Timber')
box('Floor_WorkAnnex',(5.3,.10,8),(5.4,.2,4.4),'Timber')
# Upper storey slabs explicitly leave the 1.9m-wide stairwell void.
box('Floor_Upper_Shop',(-3,3.40,-1.5),(5,.2,9),'Timber')
box('Floor_Upper_ResidentialWest',(1.9,3.40,1.65),(4.8,.2,8.3),'Timber')
box('Floor_Upper_StairFoot',(5.3,3.40,-1.85),(2,.2,1.3),'Timber')
box('Floor_Upper_Landing',(5.3,3.40,5.15),(2,.2,1.3),'Timber')
# Hero shop front is actually pierced for the reused modules.
front=box('Shell_Shop_Front',(-3,3.5,-6),(5,6.6,.24))
arch_cut(front,-3,-6,.10,.9,1.70,.95)
arch_cut(front,-3,-6,4.60,.8,5.25,.65)
# West facade has a shop display window and an offset bedroom window.
wall('Shell_Shop_West','Z',-5.5,-6,3,.2,6.8,[(-4.7,-2.5,1.05,2.35),(-.9,.7,4.7,6.1)])
wall('Shell_Shop_Rear','X',3,-5.5,-.5,.2,6.8,[(-4.3,-2.9,4.8,6.15)])
wall('Shell_Shop_Right_Return','Z',-.5,-6,-2.5,.2,6.8)
# Shared structural spine: ground doorways to treatment and service hall; upstairs bedroom access.
wall('Interior_SharedSpine_Ground','Z',-.5,-2.5,3,.2,3.30,[(-1.8,.1,.2,2.95),(.8,3.0,.2,2.95)])
wall('Interior_SharedSpine_Upper','Z',-.5,-2.5,3,3.5,6.65,[(-1.9,.1,3.5,6.25)])
# Recessed main wing, with smaller upper living window.
bfront=box('Shell_Residential_Front',(2.9,3.4,-2.5),(6.8,6.4,.24))
arch_cut(bfront,1.5,-2.5,4.60,.60,5.185,.4875)
wall('Shell_Residential_East','Z',6.3,-2.5,5.8,.2,6.6,[(2.4,4.1,4.65,6.15)])
wall('Shell_Residential_West_Return','Z',-.5,3,5.8,.2,6.6,[(3.6,5.1,4.65,6.1)])
# Rear garden door remains on exposed section, annex links at the east end.
wall('Shell_Residential_Rear_Ground','X',5.8,-.5,6.3,.2,3.3,[(.10,1.90,.2,2.95),(3.5,5.3,.2,2.95)])
wall('Shell_Residential_Rear_Upper','X',5.8,-.5,6.3,3.5,6.6,[(.6,2.1,4.7,6.0)])
# Annex has its own actual single-storey perimeter and rear garden exit.
wall('Shell_WorkAnnex_FrontReturn','X',5.8,6.3,8,.2,3.2)
wall('Shell_WorkAnnex_East','Z',8,5.8,10.2,.2,3.2,[(6.5,8.0,1.1,2.4)])
wall('Shell_WorkAnnex_West','Z',2.6,5.8,10.2,.2,3.2,[(6.4,7.7,1.1,2.4)])
wall('Shell_WorkAnnex_Rear','X',10.2,2.6,8,.2,3.2,[(5.45,7.15,.2,2.95)])
# Room partition thresholds, keeping a real service circulation route.
wall('Interior_Shop_Dispensary','X',-1.0,-5.5,-.5,.2,3.30,[(-4,-2,.2,2.95)])
wall('Interior_Treatment_East','Z',2.35,-2.5,1.0,.2,3.30,[(-.6,.85,.2,2.95)])
wall('Interior_Treatment_Rear','X',1.0,-.5,2.35,.2,3.30)
wall('Interior_Annex_PrepStorage','X',8.35,2.6,8,.2,3.2,[(4.4,6.2,.2,2.95)])
wall('Interior_Upper_LivingStudy','X',1.3,-.5,4.3,3.5,6.55,[(.8,2.7,3.5,6.25)])
# Compact straight stair: 17 x 0.1941m rises, 0.31m treads, 1.7m clear width.
start=-.9;run=.31;rise=3.3/17
profile=[(start,.2)]
for i in range(17):profile += [(start+i*run,.2+(i+1)*rise),(start+(i+1)*run,.2+(i+1)*rise)]
profile += [(start+17*run,.2)]
n=len(profile);vs=[P(x,y,z) for x in [4.4,6.1] for z,y in profile];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
mesh('Stairs_17_Risers',vs,fs,'Timber')
# Guard planes form real safety barriers; their visible top rails are part of one mesh group.
for x in [4.33,6.17]:
 poly=[(-.9,.35),(-.9,1.35),(4.37,4.65),(4.37,3.65)]
 n=len(poly);vs=[P(xx,y,z) for xx in [x-.055,x+.055] for z,y in poly];fs=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
 mesh('Stair_Guard_Sloped',vs,fs,'Timber',.012)
wall('Stairwell_Upper_Guard','X',-1.22,4.3,6.3,3.5,4.6)
# Solid attic masses with roof-to-roof Boolean union: real cross-gable intersection.
def roof(name,axis,section,a,b):
 n=len(section);vs=[P(u,h,end) if axis=='Z' else P(end,h,u) for end in [a,b] for u,h in section]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,'Slate')
ra=roof('Roof_Main_CrossGable','Z',[(-5.85,6.78),(-5.1,7.25),(-3.72,8.9),(-3,9.70),(-2.28,8.9),(-.90,7.25),(-.15,6.78)],-6.4,3.3)
rb=roof('TEMP_ResidentialRoof','X',[(-2.85,6.58),(-1.7,7.0),(1.65,8.55),(5.0,7.0),(6.15,6.58)],-2.15,6.65)
bpy.context.view_layer.objects.active=ra;mod=ra.modifiers.new('Intersecting cross gables','BOOLEAN');mod.operation='UNION';mod.solver='EXACT';mod.object=rb;bpy.ops.object.modifier_apply(modifier=mod.name);objects.remove(rb);bpy.data.objects.remove(rb,do_unlink=True)
rc=roof('Roof_Lower_WorkAnnex','Z',[(2.30,3.22),(3.1,3.55),(5.30,4.85),(7.5,3.55),(8.30,3.22)],5.78,10.5)
for o in [ra,rc]:
 o.data.materials.clear()
 for k in ['Slate','Plaster','Timber']:o.data.materials.append(mats[k])
 for p in o.data.polygons:p.material_index=1 if abs(p.normal.z)<.05 else (2 if p.normal.z<0 else 0)
# Structural framing is authored into a few combined meshes, not a decoration cloud.
def beam(name,a,b,width=.16):
 a,b=Vector(P(*a)),Vector(P(*b));d=b-a;mid=(a+b)/2
 bpy.ops.mesh.primitive_cube_add(size=1,location=mid);o=bpy.context.object;o.name=name;o.dimensions=(width,width,d.length);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);o.data.materials.append(mats['Timber']);objects.append(o);return o
for x in [-5.5,-.5]:beam('Frame_Shop_Corner',(x,.2,-6.14),(x,6.78,-6.14),.19)
beam('Frame_Shop_Storey_Belt',(-5.5,3.48,-6.15),(-.5,3.48,-6.15),.19)
beam('Frame_Gable_Collar',(-5.65,6.90,-6.43),(-.35,6.90,-6.43),.18)
for a,b in [((-5.85,6.78,-6.43),(-5.1,7.25,-6.43)),((-5.1,7.25,-6.43),(-3.72,8.9,-6.43)),((-3.72,8.9,-6.43),(-3,9.7,-6.43)),((-3,9.7,-6.43),(-2.28,8.9,-6.43)),((-2.28,8.9,-6.43),(-.90,7.25,-6.43)),((-.90,7.25,-6.43),(-.15,6.78,-6.43)),((-5.85,6.78,-6.35),(-5.85,6.78,3.3)),((6.68,6.58,-2.85),(6.68,8.55,1.65)),((6.68,8.55,1.65),(6.68,6.58,6.15))]:beam('Frame_Roof_Fascia',a,b,.18)
for x,z in [(-5.5,3),(6.3,-2.5),(6.3,5.8),(8,10.2),(2.6,10.2)]:beam('Frame_Corner_Post',(x,.2,z),(x,3.18 if z>6 else 6.55,z),.16)
beam('Frame_Residential_Belt',(-.45,3.48,-2.64),(6.35,3.48,-2.64),.16)
# One structural chimney at the shared service wall; no isolated floating flues.
box('Chimney_Stone_Stack',(-4.0,5.25,2.65),(.80,10.1,.86),'Stone',.03)
box('Chimney_Cap',(-4.0,10.30,2.65),(1.04,.20,1.10),'Stone',.025)
box('Chimney_Flue',(-4.20,10.62,2.65),(.22,.48,.26),'Stone',.02)
box('Chimney_Flue',(-3.80,10.56,2.65),(.22,.36,.26),'Stone',.02)
# Quiet secondary rectangular windows, sized for room use rather than repeated Gothic bays.
def window(name,axis,fixed,c,bottom,width,height):
 # Frames around glazing; closed thin glazing also provides safe window collision later.
 if axis=='X':
  box(name+'_Glass',(c,bottom+height/2,fixed),(width,.99*height,.035),'Glass')
  for u in [-1,1]:box(name+'_Frame',(c+u*width/2,bottom+height/2,fixed-.035),(.085,height+.16,.13),'Timber')
  for v in [0,height]:box(name+'_Frame',(c,bottom+v,fixed-.035),(width+.16,.085,.13),'Timber')
  box(name+'_Mullion',(c,bottom+height/2,fixed-.07),(.06,height,.10),'Timber')
 else:
  box(name+'_Glass',(fixed,bottom+height/2,c),(.035,.99*height,width),'Glass')
  for u in [-1,1]:box(name+'_Frame',(fixed,bottom+height/2,c+u*width/2),(.13,height+.16,.085),'Timber')
  for v in [0,height]:box(name+'_Frame',(fixed,bottom+v,c),(.13,.085,width+.16),'Timber')
  box(name+'_Mullion',(fixed,bottom+height/2,c),(.10,height,.06),'Timber')
window('Window_Shop_Display','Z',-5.64,-3.6,1.05,2.2,1.30)
window('Window_Bedroom_Side','Z',-5.64,-.1,4.70,1.6,1.40)
window('Window_Bedroom_Rear','X',3.14,-3.6,4.8,1.4,1.35)
window('Window_Study_East','Z',6.44,3.25,4.65,1.7,1.50)
window('Window_Study_West','Z',-.64,4.35,4.65,1.5,1.45)
window('Window_Study_Rear','X',5.94,1.35,4.7,1.5,1.30)
window('Window_Prep_East','Z',8.14,7.25,1.1,1.5,1.30)
window('Window_Prep_West','Z',2.46,7.05,1.1,1.3,1.30)
# Consolidate by architectural role, preserving materials and few scene transforms.
def category(o):
 n=o.name
 for key in ['Floor','Interior','Shell','Stairs','Stair_Guard','Stairwell','Roof','Frame','Chimney','Window']:
  if n.startswith(key):return n.split('.')[0] if key in ['Roof','Floor','Stairs'] else key
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
# Add consistent unique atlas UVs across all architecture; separate painted reuse bake later.
bpy.ops.object.select_all(action='DESELECT')
for o in final:o.select_set(True)
bpy.context.view_layer.objects.active=final[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.003);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
report={'asset':'CM_Redesign01','storeys':{'ground':.2,'upper':3.5},'volumes':{'shop_bedroom':[-5.5,-.5,-6,3],'residential_study':[-.5,6.3,-2.5,5.8],'preparation_storage_annex':[2.6,8,5.8,10.2]},'roof_ridges':[9.70,8.55,4.85],'stairs':{'risers':17,'rise':rise,'tread':run,'width':1.7,'start_z':start,'top_z':4.37},'parts':[]}
for o in final:
 o.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 assert bad==0 and vol>0,(o.name,bad,vol)
 report['parts'].append({'name':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'nonmanifold':bad,'volume':vol})
report['triangles']=sum(o['triangles'] for o in report['parts']);report['mesh_count']=len(final)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE));(OUT/'geometry_validation.json').write_text(json.dumps(report,indent=2));print('REDESIGN_READY',json.dumps({k:v for k,v in report.items() if k!='parts'}))
