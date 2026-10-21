"""Authored metric interior family. +Y up / +Z front, pivots at floor or work surface.
Reuses the approved painted sheet; no global subdivision, random noise or generated clutter.
"""
import bpy,bmesh,math,json,sys
from mathutils import Vector,Matrix
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ApothecaryFurnishings01'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mats={};palette={'Walnut':(.35,.22,.12,1),'Sage':(.42,.48,.31,1),'Linen':(.85,.79,.61,1),'Ceramic':(.82,.79,.62,1),'Iron':(.16,.18,.15,1),'Brass':(.50,.38,.17,1),'Glass':(.32,.43,.31,.5),'Labels':(.85,.81,.68,1),'Water':(.29,.40,.37,1),'Cloth':(.42,.51,.34,1)}
for key,color in palette.items():
 m=bpy.data.materials.new('CM_AF01_'+key);m.diffuse_color=color;m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.85;mats[key]=m
paint=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production01/Textures/CM_Production01_ApprovedPaint.png'));paint.pack();labels=bpy.data.images.load(str(A/'Textures/CM_AF01_BotanicalLabels.png'));labels.pack()
for key in ['Walnut','Sage','Linen','Ceramic','Brass','Labels','Cloth']:
 m=mats[key];t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=labels if key=='Labels' else paint;m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
parts=[];catalog=[];current=None
P=lambda v:Vector((v[0],v[2],v[1]))
def start(name,collider=None,sockets=None):
 global current,parts
 current=name;parts=[];catalog.append(dict(name=name,collider=collider,sockets=sockets or []))
def uvmap(o,key):
 uv=o.data.uv_layers.new(name='PaintUV');coords=[v.co for v in o.data.vertices];lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)];dim=[hi[i]-lo[i] for i in range(3)];along=max(range(3),key=lambda i:dim[i]);cross=max((i for i in range(3) if i!=along),key=lambda i:dim[i]);u0=.52 if key=='Walnut' else .02;v0=.02 if key=='Sage' else .52
 for face in o.data.polygons:
  for li in face.loop_indices:
   v=coords[o.data.loops[li].vertex_index]
   u=.5+(v[cross]-(hi[cross]+lo[cross])/2)/max(.55,dim[cross]*1.4);w=.12+(v[along]-lo[along])/max(1.8,dim[along]*1.5)
   uv.data[li].uv=(u0+.45*max(.02,min(.98,u)),v0+.45*max(.02,min(.98,w)))
def mesh(name,vs,fs,key='Walnut',bevel=0):
 me=bpy.data.meshes.new(name);me.from_pydata([P(v) for v in vs],[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);me.materials.append(mats[key]);bpy.context.view_layer.objects.active=o
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if bevel:
  mod=o.modifiers.new('Soft carved edges','BEVEL');mod.width=bevel;mod.segments=3;mod.affect='EDGES';mod.harden_normals=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 me=o.data
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
 me.set_sharp_from_angle(angle=math.radians(48));uvmap(o,key);parts.append(o);return o
faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
def box(n,p,d,k='Walnut',b=.007):
 return mesh(n,[(p[0]+x*d[0]/2,p[1]+y*d[1]/2,p[2]+z*d[2]/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]],faces,k,b)
def loft(n,rings,k='Walnut',segments=24):
 # rings are (height, x-radius, z-radius, x-drift, z-drift)
 vs=[(cx+rx*math.cos(a*2*math.pi/segments),y,cz+rz*math.sin(a*2*math.pi/segments)) for y,rx,rz,cx,cz in rings for a in range(segments)]
 fs=[tuple(reversed(range(segments))),tuple(range(len(vs)-segments,len(vs)))]+[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(len(rings)-1) for i in range(segments)]
 return mesh(n,vs,fs,k)
def lathe(n,p,profile,k='Ceramic',seg=32):return loft(n,[(p[1]+h,r,r,p[0],p[2]) for h,r in profile],k,seg)
def rod(n,a,b,r,k='Walnut',seg=12):
 axis=(P(b)-P(a)).normalized();u=axis.cross(Vector((1,0,0)))
 if u.length<.01:u=axis.cross(Vector((0,0,1)))
 u.normalize();v=axis.cross(u);verts=[]
 for point in [P(a),P(b)]:
  for i in range(seg):
   q=point+r*(u*math.cos(2*math.pi*i/seg)+v*math.sin(2*math.pi*i/seg));verts.append((q.x,q.z,q.y))
 return mesh(n,verts,[tuple(reversed(range(seg))),tuple(range(seg,seg*2))]+[(i,(i+1)%seg,(i+1)%seg+seg,i+seg) for i in range(seg)],k)
def tube(n,points,r,k='Brass'):
 for i in range(len(points)-1):rod(n+str(i),points[i],points[i+1],r,k,8)
def label(n,p,w,h,index):
 x,y,z=p;o=mesh(n,[(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)],[(0,1,2,3)],'Labels');uv=o.data.uv_layers[0];col=index%4;row=index//4
 for i,v in enumerate([(0,0),(1,0),(1,1),(0,1)]):uv.data[i].uv=((col+.03+.94*v[0])/4,1-(row+.97-.94*v[1])/2)
 return o
def top(n,w,d,h):
 for j in range(3):box(n+str(j),(0,h,(-1+j)*d/3),(w,.065,d/3-.003),'Walnut',.012)
def legs(w,d,h):
 for side in [-1,1]:
  for back in [-1,1]:
   x=side*(w/2-.09);z=back*(d/2-.09)
   loft('Turned squared leg',[(0,.06,.06,x+.008*side,z+.008*back),(.08,.066,.066,x,z),(.15,.043,.043,x,z),(.38,.044,.044,x+.003*side,z),(.45,.063,.063,x,z),(h,.057,.057,x,z)],'Walnut',12)
def drawers(w,count,y,z):
 for j in range(count):
  x=-w/2+(j+.5)*w/count;box('Fitted drawer front',(x,y,z),(w/count-.022,.19,.05),'Sage',.009);box('Raised drawer field',(x,y,z+.029),(w/count-.082,.13,.018),'Sage',.006)
  rod('Pull foot',(x-.04,y,z+.03),(x-.04,y,z+.064),.009,'Brass');rod('Pull foot',(x+.04,y,z+.03),(x+.04,y,z+.064),.009,'Brass');rod('Curved pull',(x-.04,y,z+.064),(x+.04,y,z+.064),.009,'Brass')
def leaf_inlay(x,y,z,size=.12):
 tube('Botanical stem',[(x,y-size/2,z),(x+.008,y,z),(x,y+size/2,z)],.003,'Brass')
 for sign in [-1,1]:
  for j in [0,1]:
   yy=y+size*(j*.30-.15);mesh('Leaf carving',[(x,yy,z),(x+sign*size*.33,yy+size*.20,z+.002),(x+sign*size*.15,yy+size*.30,z),(x,yy+size*.1,z)],[(0,1,2,3)],'Brass')
def finish():
 # One material-batched mesh per module, logical region slots retained; variants/dressing are separate prefab children.
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=current;o.data.name=current+'_Mesh';o['family']='CM_ApothecaryFurnishings01';o.data.calc_loop_triangles();me=o.data;bm=bmesh.new();bm.from_mesh(me);boundary=sum(e.is_boundary for e in bm.edges);bad=sum(len(set(f.verts))<3 or f.calc_area()<1e-12 for f in bm.faces);bm.free()
 catalog[-1].update(triangles=len(me.loop_triangles),vertices=len(me.vertices),bounds=[[min(v.co[i] for v in me.vertices) for i in range(3)],[max(v.co[i] for v in me.vertices) for i in range(3)]],boundaryEdges=boundary,degenerateFaces=bad,uvLayers=len(me.uv_layers),materials=[m.name for m in me.materials]);assert bad==0,current
 # Root pivot at datum, not the last joined object's centre.
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');return o
# Counter: customer-facing framed panel, six service drawers, pilasters and recessed toe base.
start('CM_AF01_SalesCounter',[[0,.50,0],[2.20,1.0,.70]],[['Customer',[0,0,1.20]],['Shopkeeper',[0,0,-1.10]],['WorkSurface',[0,1.055,0]],['Scale',[.67,1.055,0]],['Ledger',[-.56,1.055,0]]])
box('Carcass',(0,.52,0),(2.12,.84,.62));box('Inset front',(0,.56,.326),(1.94,.63,.035),'Sage',.015)
for x in [-1.04,-.36,.36,1.04]:box('Front stile',(x,.55,.36),(.064,.80,.07))
for x in [-.70,0,.70]:leaf_inlay(x,.55,.39,.25)
box('Toe plinth',(0,.075,0),(2.16,.15,.65));box('Top cornice',(0,.94,0),(2.23,.11,.72),b=.015);top('Hand planed counter',2.28,.76,1.02)
# Service drawers face -Z; flip their construction together around Y.
old=len(parts);drawers(1.98,3,.76,.33);drawers(1.98,3,.52,.33)
for o in parts[old:]:
 for v in o.data.vertices:v.co.y=-v.co.y
 # Reflection corrected explicitly below, preserving front-facing normals.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
finish()
start('CM_AF01_MedicineShelving',[[0,1.10,0],[1.80,2.20,.34]],[['WallFix',[0,1.7,-.17]]])
box('Back slats',(0,1.16,-.14),(1.70,2.10,.055),'Sage')
for x in [-.86,.86]:
 box('Stile',(x,1.13,0),(.09,2.24,.36));box('Grounded post shoe',(x,.02,0),(.105,.04,.37))
for y in [.08,.50,.96,1.42,1.88,2.18]:box('Shelf',(0,y,.01),(1.78,.055,.38),b=.009)
for x in [-.30,.30]:box('Lower partition',(x,.29,0),(.04,.38,.32))
for i in range(3):leaf_inlay((i-1)*.55,2.23,.045,.09)
# A gently bowed pediment rather than a flat modern cabinet top.
for i in range(12):
 x=-.9+i*.15;box('Shaped crown',(x+.075,2.23+.06*math.cos((x+.075)*math.pi/1.8),-.02),(.154,.07,.36),b=.01)
finish()
for name,w in [('CM_AF01_PreparationBench',3.20),('CM_AF01_SideWorktable',1.50)]:
 start(name,[[0,.46,0],[w,.92,.65]],[['Use',[0,0,1.15]],['CraftingFocus',[0,.98,0]],['CameraPreview',[0,1.5,2.25]]]);legs(w,.65,.89);top('Workbench plank',w+.06,.68,.94);box('Rear rail',(0,.80,-.26),(w-.10,.20,.07));box('Lower shelf',(0,.22,0),(w-.11,.045,.54));drawers(w-.12,4 if w>2 else 2,.78,.29);finish()
start('CM_AF01_InstrumentStand',[[0,.35,0],[.65,.70,.46]],[['Use',[0,0,.9]]]);legs(.65,.46,.66);top('Instrument stand top',.67,.48,.69);box('Instrument shelf',(0,.20,0),(.50,.035,.32));finish()
start('CM_AF01_ExaminationCouch',[[0,.39,0],[.94,.78,2.0]],[['PatientApproach',[0,0,-1.60]],['Clinician',[-1.25,0,0]],['PatientLying',[0,.82,0]],['ExaminationFocus',[0,1.05,.15]]]);legs(.90,1.9,.51);box('Bed frame',(0,.49,0),(.96,.17,2.02),b=.018)
loft('Soft mattress',[(.55,.43,.94,0,0),(.60,.47,.98,0,0),(.71,.46,.98,0,0),(.74,.42,.94,0,0)],'Linen',48)
vs=[];rings=[(.74,.25,.15),(.77,.34,.23),(.83,.34,.23),(.88,.27,.17),(.90,.04,.025)]
for y,rx,rz in rings:
 for i in range(32):
  a=2*math.pi*i/32;c=math.cos(a);ss=math.sin(a);vs.append((rx*math.copysign(abs(c)**.55,c),y,.64+rz*math.copysign(abs(ss)**.55,ss)))
fs=[tuple(reversed(range(32))),tuple(range(128,160))]+[(j*32+i,j*32+(i+1)%32,(j+1)*32+(i+1)%32,(j+1)*32+i) for j in range(4) for i in range(32)];mesh('Soft linen pillow',vs,fs,'Linen')
for z,h in [(.98,.99),(-.98,.71)]:
 for x in [-.44,.44]:lathe('Bed end post',(x,0,z),[(.48,.035),(h-.04,.035),(h,.05),(h+.04,.025)],'Walnut',16)
 box('Curved end rail',(0,h-.10,z),(.88,.13,.065),b=.025)
# Folded sage cover at the foot, leaving the examination surface clear.
xs=[-.50,-.46,-.36,-.26,0,.26,.36,.46,.50];zs=[-.83,-.72,-.62,-.50,-.40];vs=[]
for z in zs:
 half=.42*math.sqrt(max(0,1-(z/.94)**2))
 for x in xs:vs.append((x,.746-min(.22,max(0,abs(x)-half)*.9),z))
fs=[(j*9+i,j*9+i+1,(j+1)*9+i+1,(j+1)*9+i) for j in range(len(zs)-1) for i in range(8)];cover=mesh('Draped woven sage cover',vs,fs,'Cloth');bpy.context.view_layer.objects.active=cover;mod=cover.modifiers.new('Fabric thickness','SOLIDIFY');mod.thickness=.009;bpy.ops.object.modifier_apply(modifier=mod.name);finish()
start('CM_AF01_PhysicianStool',[[0,.25,0],[.43,.50,.43]])
lathe('Scooped stool seat',(0,0,0),[(.43,.21),(.47,.225),(.50,.21),(.495,.05)],'Walnut',32)
for i in range(3):
 a=2*math.pi*i/3;rod('Splayed stool leg',(.19*math.cos(a),.02,.19*math.sin(a)),(.12*math.cos(a),.45,.12*math.sin(a)),.028)
finish()
start('CM_AF01_Washstand',[[0,.43,0],[.78,.86,.56]],[['Use',[0,0,1.0]],['Basin',[0,.89,0]]]);legs(.75,.55,.84);box('Basin platform',(0,.84,0),(.80,.065,.60),b=.02)
lathe('Hollow glazed washbasin',(0,.87,0),[(0,.13),(.025,.22),(.10,.27),(.16,.29),(.17,.27),(.13,.245),(.06,.18),(.04,.04)],'Ceramic',40)
lathe('Still water',(0,.95,0),[(0,.19),(.002,.19)],'Water',32);rod('Towel bar',(-.33,.61,.33),(.33,.61,.33),.014,'Brass');box('Folded wash linen',(.16,.57,.34),(.22,.22,.025),'Linen',.012);box('Lower slats',(0,.20,0),(.64,.03,.44));finish()
start('CM_AF01_SupplyCabinet',[[0,.92,0],[1.45,1.84,.40]],[['Use',[0,0,1.15]]]);box('Cabinet body',(0,.94,-.02),(1.38,1.74,.35));box('Base plinth',(0,.07,0),(1.46,.14,.43),b=.014);box('Crown',(0,1.84,0),(1.48,.10,.44),b=.015)
for x in [-.36,.36]:
 box('Sage raised panel door',(x,1.01,.19),(.67,1.43,.05),'Sage',.014);box('Recessed door field',(x,1.01,.219),(.53,1.25,.015),'Sage',.010);leaf_inlay(x,1.18,.234,.23)
 for y in [.48,1.53]:box('Strap hinge',(x+(-.27 if x<0 else .27),y,.23),(.10,.025,.025),'Iron',.005)
 lathe('Cabinet knob',(x+(.24 if x<0 else -.24),.94,.25),[(0,.012),(.035,.018)],'Brass',16)
finish()
start('CM_AF01_DryingRack',None,[['WallFix',[0,.55,-.13]],['HerbL',[-.48,.54,.23]],['HerbM',[0,.54,.23]],['HerbR',[.48,.54,.23]]])
box('Wall rail',(0,.56,-.10),(1.4,.09,.08));box('Front hanging rail',(0,.56,.23),(1.4,.07,.07))
for x in [-.64,.64]:rod('Rack arm',(x,.56,-.10),(x,.56,.26),.022);rod('Triangular bracket',(x,.28,-.10),(x,.54,.23),.019)
for x in [-.48,0,.48]:tube('Herb peg',[(x,.60,.23),(x,.57,.23),(x,.52,.23)],.008,'Iron')
finish()
# Countertop instruments and containers: separate, surface-origin reusable modules.
start('CM_AF01_BalanceScales',None,[['PanL',[-.19,.16,0]],['PanR',[.19,.16,0]]]);lathe('Scale foot',(0,0,0),[(0,.12),(.025,.14),(.05,.11),(.065,.06)],'Walnut');lathe('Brass turned pillar',(0,.05,0),[(0,.035),(.08,.025),(.30,.018),(.35,.028),(.38,.012)],'Brass',20)
rod('Balance beam',(-.22,.40,0),(.22,.415,0),.011,'Brass');rod('Indicator',(0,.41,0),(0,.48,0),.004,'Brass')
for side in [-1,1]:
 lathe('Dish pan',(side*.19,.145,0),[(0,.035),(.009,.075),(.028,.10),(.036,.10),(.029,.087),(.014,.035)],'Brass',28)
 for z in [-.055,.055]:rod('Fine pan chain',(side*.19,.40,0),(side*.19,.18,z),.0025,'Iron',6)
finish()
start('CM_AF01_MortarPestle');lathe('Hollow ceramic mortar',(0,0,0),[(0,.09),(.025,.13),(.12,.15),(.17,.14),(.18,.12),(.13,.105),(.055,.075)],'Ceramic',36);rod('Pestle',(0,.08,.02),(.09,.30,.03),.025,'Walnut',20);finish()
start('CM_AF01_InstrumentTray');box('Instrument tray',(0,.015,0),(.48,.03,.28),'Walnut',.012)
for x in [-.23,.23]:box('Tray rim',(x,.05,0),(.025,.06,.28),b=.008)
for z in [-.13,.13]:box('Tray rim',(0,.05,z),(.46,.06,.02),b=.007)
box('Linen tray liner',(0,.034,0),(.42,.008,.22),'Linen',.004)
for x in [-.13,0,.13]:
 rod('Turned instrument handle',(x,.055,-.045),(x,.055,.045),.015,'Walnut',12);rod('Period probe',(x,.055,.045),(x+.015,.055,.10),.004,'Iron',8)
finish()
start('CM_AF01_MeasuringTools');lathe('Measure cup',(0,0,0),[(0,.04),(.07,.04),(.085,.055),(.09,.05),(.075,.03),(.01,.03)],'Brass',24)
for x,h in [(.11,.045),(.18,.025)]:lathe('Balance weight',(x,0,.01),[(0,.025),(h-.01,.025),(h,.014)],'Brass',16)
rod('Scoop handle',(-.16,.03,-.05),(-.07,.03,.05),.009,'Walnut',12);lathe('Scoop bowl',(-.18,.015,-.07),[(0,.025),(.02,.045),(.025,.04),(.009,.025)],'Brass',20);finish()
def jar(x,z,h,index,glass=False):
 r=h*.30;lathe('Hand-thrown vessel',(x,0,z),[(0,r*.7),(.02,r),(.60*h,r*1.02),(.78*h,r*.9),(.84*h,r*.67),(.92*h,r*.67)],'Glass' if glass else 'Ceramic',28)
 lathe('Lid and lip',(x,0,z),[(.88*h,r*.70),(.92*h,r*.78),(.97*h,r*.75),(h,r*.60)],'Walnut',24)
 label('Botanical paper label',(x,.46*h,z+r*1.025),r*1.5,h*.40,index)
 if glass:lathe('Medicine contents',(x,0,z),[(.025,r*.83),(.57*h,r*.83)],'Sage',24)
start('CM_AF01_CeramicJar');jar(0,0,.28,0);finish()
start('CM_AF01_TinctureBottle');jar(0,0,.32,4,True);finish()
for variant in [0,1]:
 start('CM_AF01_MedicineRow'+('A' if variant==0 else 'B'))
 for i,(x,h) in enumerate([(-.58,.24),(-.19,.31),(.19,.27),(.58,.25)]):jar(x,0,h,(i+variant*2)%6,variant==1 and i==2)
 finish()
start('CM_AF01_OpenLedger');box('Bound ledger',(0,.025,0),(.45,.045,.32),'Sage',.012)
for side,index in [(-1,6),(1,7)]:
 # UV mapped pages lie on the open book plane; broad pale paper with botanical-ink headings.
 o=label('Ledger page',(side*.108,0,0),.21,.28,index)
 for v in o.data.vertices:v.co=Vector((v.co.x,v.co.z,v.co.y+.052))
 rod('Bound paper edge',(side*.21,.05,-.13),(side*.21,.05,.13),.005,'Linen',8)
finish()
start('CM_AF01_LinenRolls')
for i in range(3):
 o=lathe('Rolled dressing',(i*.065-.065,0,0),[(0,.032),(.12,.032)],'Linen',20)
finish()
# Save editable source at origin per asset; temporary layout positions are not exported.
report={'modules':catalog,'totalTriangles':sum(m['triangles'] for m in catalog),'paintSource':paint.filepath,'labelSource':str(R/'ArtSource/Paint/Interiors/CrookedMortar/ApothecaryFurnishings01/CM_AF01_BotanicalLabels.svg'),'axes':'Unity +Y up / +Z front','scaleMetres':1,'notes':'Intentional open label/inlay sheets. Solid furniture and vessels are closed meshes; no collider geometry in FBX.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ApothecaryFurnishings01.blend'))
conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 if '--export-only' in sys.argv and entry['name'] not in sys.argv[sys.argv.index('--export-only')+1:]:continue
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps(report,indent=2));print('FURNISHINGS_READY',len(catalog),report['totalTriangles'])
