"""Static architectural prototype. Run only in Blender --background --factory-startup.
Metres; Blender +X right, +Y exterior, +Z up. Unique shared atlas UVs.
Refuses overwriting any published source/export. No existing facade edits.
"""
import bpy, bmesh, math, json, sys
from pathlib import Path
from mathutils import Vector, Matrix
if not bpy.app.background: raise RuntimeError('Run in disposable background Blender only')
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).parent
EXPORT=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01/Models/CM_WindowBay01.fbx'
SOURCE=OUT/'CM_WindowBay01.blend'
if (SOURCE.exists() or EXPORT.exists()) and '--revise-this-prototype' not in sys.argv: raise RuntimeError('Refusing to overwrite an existing asset')
for o in list(bpy.data.objects): bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats={}
for name,color in [('Plaster',(.66,.63,.57,1)),('Timber',(.23,.20,.17,1)),('Shutters',(.39,.41,.38,1)),('Slate',(.29,.31,.32,1)),('Iron',(.16,.17,.17,1)),('Soil',(.21,.20,.18,1))]:
 m=bpy.data.materials.new('Review_'+name);m.diffuse_color=color;m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.9;mats[name]=m
parts=[]
def finish(o,mat,bevel=.01):
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
 if bevel:
  mod=o.modifiers.new('Crafted edge bevel','BEVEL');mod.width=bevel;mod.segments=2
  bpy.ops.object.modifier_apply(modifier=mod.name)
 # Recalculate outward normals, retain flat large planes and smooth only bevel faces.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
 for p in o.data.polygons:p.use_smooth=p.area<.012
 o.data.materials.append(mats[mat]);parts.append(o);o.select_set(False);return o

def mesh(name,verts,faces,mat,bevel=.008):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);return finish(o,mat,bevel)

def prism(name,poly,y0,y1,mat,bevel=.008):
 # polygon in X/Z plane, with real thickness
 n=len(poly);vs=[(x,y,z) for y in [y0,y1] for x,z in poly]
 fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,vs,fs,mat,bevel)

def beam(name,a,b,w,d,mat='Timber',bend=.012):
 a,b=Vector(a),Vector(b);axis=(b-a).normalized();ref=Vector((0,1,0));u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
 vs=[]
 for k,t in enumerate([0,.32,.69,1]):
  c=a.lerp(b,t)+u*(math.sin(t*math.pi)*bend)+v*(math.sin(t*math.pi)*bend*.35)
  taper=[1,.99,1.015,.97][k]
  for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(tuple(c+u*i*w*.5*taper+v*j*d*.5*taper))
 fs=[(3,2,1,0),(12,13,14,15)]+[(k*4+i,k*4+(i+1)%4,(k+1)*4+(i+1)%4,(k+1)*4+i) for k in range(3) for i in range(4)]
 return mesh(name,vs,fs,mat,min(.014,w*.12))

def box(name,loc,dims,mat,bevel=.01):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dims
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.select_set(False);return finish(o,mat,bevel)
# Hollow wall: exact Boolean cut with an extruded arch. Cutter is never exported.
r=.8;spring=1.75;rise=.65
arch=[(r*math.cos(i*math.pi/24),spring+rise*math.sin(i*math.pi/24)) for i in range(25)]
outline=[(-r,1.1),(r,1.1)]+arch
wall=box('01_Plaster_Wall_3m_ThroughOpening',(0,-.14,1.8),(3,.28,3.6),'Plaster',0)
cut=prism('TEMP_arch_cutter',outline,-.6,.6,'Plaster',0);parts.remove(cut)
bpy.context.view_layer.objects.active=wall
mod=wall.modifiers.new('True arched opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
mod=wall.modifiers.new('Soft plaster edges','BEVEL');mod.width=.012;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
# Fit the plaster top beneath the sloping eave rather than intersecting its tiles.
for vert in wall.data.vertices:
 world=wall.matrix_world@vert.co
 if world.z>3.3: vert.co.z=min(world.z,3.58-.58*(world.y+.3)-.115)-wall.location.z
# Curved frame is a continuous bent architectural band, not segmented cylinders.
inner=[(x*.92,1.75+(z-1.75)*.89) for x,z in arch]
outer=[(x*1.065,1.75+(z-1.75)*1.12) for x,z in arch]
vs=[(x,y,z) for y in [-.035,.115] for ring in [inner,outer] for x,z in ring];n=len(arch)
fs=[]
for i in range(n-1):
 for off in [0,2*n]:fs.append((off+i,off+i+1,off+n+i+1,off+n+i))
 for off in [0,n]:fs.append((off+i,off+2*n+i,off+2*n+i+1,off+i+1))
fs += [(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
mesh('02_Window_CurvedArch_Frame',vs,fs,'Timber',.009)
for side in [-1,1]:
 beam('02_Window_Jamb_'+str(side),(side*.795,.045,1.1),(side*.795,.045,1.75),.115,.15,bend=.005)
box('02_Window_Deep_Projecting_Sill',(0,.11,1.075),(1.89,.53,.13),'Timber',.018)
beam('02_Window_Centre_Mullion',(0,.045,1.13),(0,.045,2.36),.055,.075,bend=.004)
beam('02_Window_Spring_Transom',(-.73,.045,1.72),(.73,.045,1.72),.055,.075,bend=.004)
for side in [-1,1]:beam('02_Window_Fan_Tracery_'+str(side),(0,.045,1.74),(side*.47,.045,2.19),.039,.065,bend=.003)
# Shutters cut to the arch, hinged open: planks and straps rotate together around hinge.
for side in [-1,1]:
 hinge=Vector((side*.86,.12,0));rot=Matrix.Rotation(-side*math.radians(153),4,'Z');group=[]
 for i in range(3):
  lo=.018+i*.247;hi=lo+.237
  x0,x1=sorted((side*lo,side*hi));top=lambda x:spring+rise*math.sqrt(max(0,1-(x/.78)**2))-.055
  poly=[(x0,1.145),(x1,1.145)]+[(x1+(x0-x1)*t/6,top(x1+(x0-x1)*t/6)) for t in range(7)]
  group.append(prism('03_Shutter_%s_Plank_%02d'%('L' if side<0 else 'R',i),poly,.13,.19,'Shutters',.008))
 for z in [1.34,1.83]:
  group.append(box('03_Shutter_CrossRail',(side*.39,.205,z),(.69,.055,.075),'Timber',.007))
  group.append(box('03_Shutter_HingeStrap',(side*.61,.24,z),(.34,.025,.045),'Iron',.005))
 for o in group:
  o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
  for vert in o.data.vertices:vert.co=hinge+rot.to_3x3()@(vert.co-hinge)
# Visible post/beam housing joint, brace shoulders, restrained pegs.
beam('04_Left_Structural_Post',(-1.37,.075,.07),(-1.35,.075,3.47),.19,.22,bend=.019)
beam('04_Upper_Tie_Beam',(-1.48,.085,3.18),(1.48,.085,3.21),.21,.24,bend=.014)
beam('04_Right_Edge_Post',(1.39,.045,.08),(1.37,.045,3.48),.16,.19,bend=-.015)
beam('04_Lower_Storey_Rail',(-1.49,.07,.15),(1.49,.07,.15),.19,.21,bend=.014)
beam('04_Diagonal_Knee_Brace',(-1.34,.08,2.48),(-.85,.08,3.18),.14,.17,bend=.018)
for x,z in [(-1.35,3.18),(-1.31,2.58),(-.94,3.1),(1.38,3.2)]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.024,depth=.024,location=(x,.218,z),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='04_Joinery_Wooden_Peg';bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);finish(o,'Timber',.003)
# Hollow planter, open top, tapered end cheeks. No flowers faked with primitives.
prism('05_Planter_Front',[(-.81,.65),(.81,.65),(.88,.94),(-.88,.94)],.47,.53,'Timber',.012)
prism('05_Planter_Back',[(-.81,.65),(.81,.65),(.88,.94),(-.88,.94)],.14,.20,'Timber',.01)
box('05_Planter_Base',(0,.335,.66),(1.61,.29,.07),'Timber',.008)
for side in [-1,1]:box('05_Planter_End_'+str(side),(side*.82,.335,.8),(.07,.39,.29),'Timber',.01)
box('05_Planter_Recessed_Soil',(0,.335,.86),(1.55,.25,.035),'Soil',.004)
for side in [-1,1]:
 beam('05_Planter_Support_'+str(side),(side*.56,.06,.48),(side*.56,.44,.69),.09,.09,bend=.006)
# Eave assembly. Four staggered courses of thick individually shaped slate.
def roofz(y):return 3.58-.58*(y+.3)
# Continuous solid roof boarding supports the spaced slate courses.
vs=[(x,y,roofz(y)+dz) for dz in [-.075,-.025] for x,y in [(-1.64,-.3),(1.64,-.3),(1.64,.85),(-1.64,.85)]]
mesh('06_Eave_Solid_Roof_Boarding',vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Timber',.006)
for x in [-1.34,-.45,.45,1.34]:beam('06_Eave_Rafter',(x,-.30,roofz(-.3)-.10),(x,.78,roofz(.78)-.1),.10,.13,bend=.012)
beam('06_Eave_Fascia',(-1.64,.76,roofz(.76)-.07),(1.64,.76,roofz(.76)-.07),.14,.13,bend=.018)
for row in range(4):
 y=.48-row*.24
 for col in range(9):
  x=-1.59+col*.38+(.19 if row%2 else 0);left=max(-1.68,x-.185);right=min(1.68,x+.185)
  if right-left<.08:continue
  yy=y+.37
  poly=[(left+.018,y),(right-.012,y),(right,yy-.016),(right-.025,yy),(left+.022,yy+.008),(left,yy-.02)]
  zoff=.025+row*.018+math.sin(col*2.7+row)*.004
  vs=[(xx,py,roofz(py)+zoff+depth) for depth in [0,.038] for xx,py in poly];n=len(poly)
  fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  mesh('06_Slate_Course%02d_Tile%02d'%(row,col),vs,fs,'Slate',.006)
# Unique shared atlas. Average scale across ALL islands before packing.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=wall
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.008,area_weight=0)
bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.004)
bpy.ops.object.mode_set(mode='OBJECT')
# Geometry validation, signed volumes, UV presence and degenerates.
report={'asset':'CM_WindowBay01','units':'metres','wall_dimensions':[3,.28,3.6],'opening':{'width':1.6,'sill':1.1,'spring':1.75,'apex':2.4},'fit':{'existing_module_origin_unity':[-4.5,3.6,-6],'placement_yaw_degrees':180,'status':'measured reference only; not installed'},'parts':[]}
allworld=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data)
 nonmanifold=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free()
 degenerate=sum(p.area<1e-10 for p in o.data.polygons)
 uv=o.data.uv_layers.active
 assert uv and len(uv.data)==len(o.data.loops)
 assert nonmanifold==0 and volume>0 and degenerate==0,(o.name,nonmanifold,volume,degenerate)
 allworld += [o.matrix_world@v.co for v in o.data.vertices]
 o.data.calc_loop_triangles()
 report['parts'].append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'nonmanifold_edges':nonmanifold,'signed_volume':volume,'degenerate_faces':degenerate,'uv_loops':len(uv.data)})
report['bounds']={'min':[min(v[i] for v in allworld) for i in range(3)],'max':[max(v[i] for v in allworld) for i in range(3)]}
report['triangles']=sum(p['triangles'] for p in report['parts']);report['mesh_count']=len(parts)
# Demonstrate actual hole: ray through opening clear; wall side ray hit.
from mathutils.bvhtree import BVHTree
bvh=BVHTree.FromObject(wall,bpy.context.evaluated_depsgraph_get())
# Wall is at (0,-.14,1.8), so test in mesh local coordinates.
for x,z,expected in [(0,1.45,False),(1.1,1.45,True),(0,2.55,True)]:
 hit=bvh.ray_cast(Vector((x,2,z))-wall.location,Vector((0,-1,0)),4)[0] is not None
 assert hit==expected,('opening ray',x,z,hit)
report['opening_ray_tests']='PASS'
# Save .blend before disposable axis conversion. Source pivots retained.
s['asset_notes']='Static review module; no collision; no facade replacement. Shared unique atlas UVs. Exterior +Y.'
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE))
conversion=Matrix.Rotation(math.pi,4,'Z')
for o in parts:o.matrix_world=conversion@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(EXPORT),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False)
(OUT/'validation.json').write_text(json.dumps(report,indent=2))
print('BAY_VALIDATED',json.dumps({k:v for k,v in report.items() if k!='parts'}))
