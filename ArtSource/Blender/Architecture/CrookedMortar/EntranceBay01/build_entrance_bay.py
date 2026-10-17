"""Build isolated CM_EntranceBay01 using the approved CM_WindowBay01 shape language.
Metres, +X right, +Y exterior, +Z up. Refuses existing source output.
"""
import bpy,bmesh,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).parent
SOURCE=OUT/'CM_EntranceBay01_Geometry_v01.blend'
if SOURCE.exists():raise RuntimeError('Refusing existing entrance source')
if not bpy.app.background:raise RuntimeError('Use background Blender')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats={};parts=[]
for name,color in [('Plaster',(.66,.63,.57,1)),('Timber',(.23,.20,.17,1)),('Sage',(.39,.41,.38,1)),('Slate',(.29,.31,.32,1)),('Iron',(.16,.17,.17,1)),('Stone',(.57,.55,.49,1))]:
 m=bpy.data.materials.new('Entrance_'+name);m.diffuse_color=color;m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.95;mats[name]=m
def finish(o,mat,bevel=.01):
 bpy.context.view_layer.objects.active=o;o.select_set(True)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
 if bevel:
  mod=o.modifiers.new('Crafted edge bevel','BEVEL');mod.width=bevel;mod.segments=2
  bpy.ops.object.modifier_apply(modifier=mod.name)
 # Recalculate outward normals, retain flat large planes and smooth only bevel faces.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free()
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
 a,b=Vector(a),Vector(b);axis=(b-a).normalized();ref=Vector((0,1,0));ref=Vector((0,0,1)) if abs(axis.dot(ref))>.95 else ref;u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
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
# Through-opening and reveals. Keep the prototype door separate from the shell.
r=.9;spring=1.7;rise=.95;floor=.15
arch=[(r*math.cos(i*math.pi/32),spring+rise*math.sin(i*math.pi/32)) for i in range(33)]
wall=box('01_Shell_Plaster_With_Arched_Opening',(0,-.16,1.8),(3.4,.32,3.6),'Plaster',0)
cutter=prism('TEMP_Arch_Cutter',[(-r,.10),(r,.10)]+arch,-.7,.7,'Plaster',0);parts.remove(cutter)
bpy.context.view_layer.objects.active=wall;mod=wall.modifiers.new('True entry arch','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
mod=wall.modifiers.new('Soft plaster corners','BEVEL');mod.width=.012;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
# Roof underside deliberately conceals shell and post ends.
def roofz(y):return 3.64-.48*(y+.3)
for v in wall.data.vertices:
 w=wall.matrix_world@v.co
 if w.z>3.25:v.co.z=min(w.z,roofz(w.y)-.105)-wall.location.z
# Individual softly hewn stone jambs and voussoirs, with restrained joints.
for side in [-1,1]:
 for i in range(4):
  z=.15+i*.3875
  prism('02_Stone_Jamb_%s_%02d'%(side,i),[(side*.915,z+.012),(side*1.16,z+.016),(side*1.155,z+.374),(side*.915,z+.376)],-.075,.18,'Stone',.014)
for i in range(11):
 a=i*math.pi/11+.008;b=(i+1)*math.pi/11-.008
 # Subdivisions retain a clean curved reveal while large voussoir faces stay readable.
 inner=[(.915*math.cos(t),spring+.966*math.sin(t)) for t in [a+(b-a)*k/3 for k in range(4)]]
 outer=[(1.16*math.cos(t),spring+1.20*math.sin(t)) for t in [b-(b-a)*k/3 for k in range(4)]]
 prism('02_Stone_Arch_Voussoir_%02d'%i,inner+outer,-.075,.18,'Stone',.012)
# Continuous timber door stop follows the arch behind the stone surround.
n=33;inner=[(.885*math.cos(i*math.pi/32),spring+.93*math.sin(i*math.pi/32)) for i in range(n)];outer=[(.945*math.cos(i*math.pi/32),spring+.99*math.sin(i*math.pi/32)) for i in range(n)]
vs=[(x,y,z) for y in [-.07,.07] for ring in [inner,outer] for x,z in ring];fs=[]
for i in range(n-1):
 for off in [0,2*n]:fs.append((off+i,off+i+1,off+n+i+1,off+n+i))
 for off in [0,n]:fs.append((off+i,off+2*n+i,off+2*n+i+1,off+i+1))
fs += [(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
mesh('02B_Door_Curved_Timber_Stop',vs,fs,'Timber',.004)
for side in [-1,1]:beam('02B_Door_Timber_Jamb_'+str(side),(side*.913,0,.21),(side*.913,0,1.70),.06,.14,bend=.003)
# Leaf made from five shaped planks; all leaf parts later join to one hinged mesh.
leaf=[]
for i in range(5):
 lo=-.875+i*.35+.004;hi=lo+.342
 def top(x):return spring+.92*math.sqrt(max(0,1-(x/.885)**2))-.024
 poly=[(lo,.22),(hi,.22)]+[(hi+(lo-hi)*k/8,top(hi+(lo-hi)*k/8)) for k in range(9)]
 leaf.append(prism('03_Door_Plank_%02d'%i,poly,-.095,.035,'Timber',.009))
# Rear structure, not stuck-on front plank clutter.
for z in [.48,1.59]:leaf.append(box('03_Door_Back_Rail',(0,-.135,z),(1.65,.07,.12),'Timber',.01))
leaf.append(beam('03_Door_Back_Diagonal',(-.72,-.135,.5),(.73,-.135,1.56),.085,.07,bend=.005))
# Forged strap hinges, shaped backing plate and ring pull.
for z in [.47,1.58]:
 leaf.append(prism('03_Door_Forged_HingeStrap',[(-.88,z-.04),(-.32,z-.028),(-.23,z),(-.32,z+.028),(-.88,z+.04)],.045,.07,'Iron',.005))
 bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.025,depth=.22,location=(-.88,.06,z));o=bpy.context.object;o.name='03_Door_Hinge_Pin';leaf.append(finish(o,'Iron',.003))
leaf.append(prism('03_Door_Handle_Backplate',[(.57,1.05),(.64,1.15),(.57,1.28),(.50,1.15)],.048,.072,'Iron',.005))
bpy.ops.mesh.primitive_torus_add(major_segments=16,minor_segments=6,location=(.57,.115,1.13),rotation=(math.pi/2,0,0),major_radius=.067,minor_radius=.011);o=bpy.context.object;o.name='03_Door_Ring_Pull';bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);leaf.append(finish(o,'Iron',0))
# Small timber diamond inset, rather than a false opaque glass aperture.
leaf.append(prism('03_Door_Diamond_Inlay',[(0,1.89),(.105,2.045),(0,2.20),(-.105,2.045)],.039,.053,'Sage',.008))
bpy.ops.object.select_all(action='DESELECT')
for o in leaf:o.select_set(True);parts.remove(o)
bpy.context.view_layer.objects.active=leaf[0];bpy.ops.object.join();door=bpy.context.object;door.name='03_Door_Leaf_Hinged';parts.append(door)
# Establish a useful static leaf pivot without adding behaviour or collision.
pivot=Vector((-.89,-.03,.20));door.data.transform(door.matrix_world);door.matrix_world=Matrix.Identity(4);door.data.transform(Matrix.Translation(-pivot));door.location=pivot
bpy.ops.object.select_all(action='DESELECT')
# Structural timber and shoulders, intentionally below roof boarding.
for side in [-1,1]:
 beam('04_Frame_Post_'+str(side),(side*1.52,.055,.15),(side*1.50,.055,3.31),.18,.21,bend=side*.014)
 beam('04_Canopy_Knee_'+str(side),(side*1.49,.07,2.55),(side*1.49,.79,3.05),.13,.14,bend=.014)
beam('04_Frame_Header',(-1.64,.055,3.18),(1.64,.055,3.18),.19,.22,bend=.012)
# Stone threshold flush with the door foot, plus a broad lower step.
box('05_Threshold_Stone',(0,.20,.10),(2.40,.82,.20),'Stone',.024)
box('05_Lower_Step_Stone',(0,.72,.045),(2.57,.53,.09),'Stone',.02)
# Build a solid canopy deck and staggered tiled skin; no exposed post stubs.
vs=[(x,y,roofz(y)+dz) for dz in [-.075,-.025] for x,y in [(-1.81,-.3),(1.81,-.3),(1.81,1.02),(-1.81,1.02)]]
mesh('06_Canopy_Solid_Boarding',vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Timber',.006)
for x in [-1.49,-.5,.5,1.49]:beam('06_Canopy_Rafter',(x,-.25,roofz(-.25)-.15),(x,.99,roofz(.99)-.15),.10,.13,bend=.01)
beam('06_Canopy_Fascia',(-1.83,.99,roofz(.99)-.10),(1.83,.99,roofz(.99)-.10),.14,.14,bend=.014)
for row in range(5):
 y=.70-row*.24
 for col in range(10):
  x=-1.72+col*.38+(.19 if row%2 else 0);l=max(-1.86,x-.185);rr=min(1.86,x+.185)
  if rr-l<.08:continue
  end=y+.37;poly=[(l+.016,y),(rr-.01,y),(rr,end-.02),(rr-.02,end),(l+.022,end+.005),(l,end-.018)]
  off=.025+row*.018+math.sin(col*2.7+row)*.004
  vs=[(xx,yy,roofz(yy)+off+dz) for dz in [0,.038] for xx,yy in poly];n=len(poly)
  mesh('06_Slate_Course%02d_Tile%02d'%(row,col),vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(k,(k+1)%n,(k+1)%n+n,k+n) for k in range(n)],'Slate',.006)
# A restrained hanging sign with a mortar emblem, without unapproved lettering.
beam('07_Sign_Timber_Outrigger',(1.5,.10,2.83),(1.5,.87,2.83),.075,.075,bend=.009)
for x in [1.29,1.63]:beam('07_Sign_Iron_Hanger',(x,.80,2.82),(x,.80,2.60),.014,.014,'Iron',bend=0)
signpoly=[(1.20,2.05),(1.13,2.13),(1.13,2.53),(1.22,2.62),(1.71,2.62),(1.79,2.53),(1.79,2.13),(1.70,2.05)]
prism('07_Sign_Sage_Board',signpoly,.77,.83,'Sage',.016)
# Mortar bowl silhouette and diagonal pestle in quiet ivory, readable at modest distance.
prism('07_Sign_Mortar_Emblem',[(1.28,2.36),(1.65,2.36),(1.61,2.23),(1.55,2.19),(1.38,2.19),(1.32,2.23)],.834,.845,'Stone',.007)
beam('07_Sign_Pestle_Emblem',(1.48,.845,2.35),(1.62,.845,2.51),.045,.022,'Stone',bend=0)
# Two small low-poly herb bundles, composed of authored leaf silhouettes, not sphere clutter.
for idx,x in enumerate([-1.30,1.18]):
 herb=[]
 for j in range(3):
  y=.71+j*.045;z=2.80-j*.015
  herb.append(beam('08_Herb_Stem',(x,y,z),(x+(j-1)*.045,y,z-.27),.009,.009,'Sage',bend=.006))
  for k in range(2):
   side=-1 if k==0 else 1;xx=x+(j-1)*.045;zz=z-.12-k*.07
   poly=[(xx,zz+.035),(xx+side*.055,zz+.015),(xx+side*.08,zz-.07),(xx+side*.025,zz-.048)]
   herb.append(prism('08_Herb_Leaf',poly,y-.009,y+.009,'Sage',.002))
 bpy.ops.object.select_all(action='DESELECT')
 for o in herb:o.select_set(True);parts.remove(o)
 bpy.context.view_layer.objects.active=herb[0];bpy.ops.object.join();o=bpy.context.object;o.name='08_Drying_Herb_Bundle_%02d'%idx;parts.append(o)
# Shared unique atlas at comparable texel scale to the approved window.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=wall
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.008,area_weight=0);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.004);bpy.ops.object.mode_set(mode='OBJECT')
report={'asset':'CM_EntranceBay01','authoring_axes':'+X right, +Y exterior, +Z up','wall':[3.4,.32,3.6],'opening':{'width':1.8,'spring':1.7,'apex':2.65,'threshold':.20},'door_leaf_pivot':list(pivot),'existing_gameplay_opening_width':2.4,'integration':'isolated art prototype only; narrower door requires deliberate future gameplay integration','parts':[]}
allvs=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();deg=sum(p.area<1e-10 for p in o.data.polygons)
 assert bad==0 and vol>0 and deg==0,(o.name,bad,vol,deg)
 o.data.calc_loop_triangles();report['parts'].append({'name':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'signed_volume':vol,'nonmanifold':bad,'degenerate':deg})
 allvs += [o.matrix_world@v.co for v in o.data.vertices]
 if '04_Frame_Post' in o.name:
  assert min(roofz(v.y)-.075-v.z for v in allvs[-len(o.data.vertices):])>.02,'Post protrudes through canopy'
report['triangles']=sum(x['triangles'] for x in report['parts']);report['mesh_count']=len(parts);report['bounds']={'min':[min(v[i] for v in allvs) for i in range(3)],'max':[max(v[i] for v in allvs) for i in range(3)]}
# Verify opening without treating the intentionally closed door as collision geometry.
from mathutils.bvhtree import BVHTree
bvh=BVHTree.FromObject(wall,bpy.context.evaluated_depsgraph_get())
for x,z,expected in [(0,1.1,False),(1.25,1.1,True),(0,2.9,True)]:assert (bvh.ray_cast(Vector((x,2,z))-wall.location,Vector((0,-1,0)),4)[0] is not None)==expected
report['shell_opening_rays']='PASS';s['asset_notes']='Closed static door prototype, no colliders or interaction. Approved window v02 material benchmark.'
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE));(OUT/'geometry_validation.json').write_text(json.dumps(report,indent=2));print('ENTRANCE_GEOMETRY',json.dumps({k:v for k,v in report.items() if k!='parts'}))
