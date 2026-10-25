"""Selective rebuilt construction. Reuses established export and approved painted surfaces."""
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4]
base=R/'ArtSource/Blender/Interiors/CrookedMortar'
text=(base/'LivedIn03/build_lived03.py').read_text().split('# Back face is exactly')[0].replace("CrookedMortar/LivedIn03'","CrookedMortar/Reconstruction06'")
exec(compile(text,str(__file__),'exec'))
A.mkdir(parents=True,exist_ok=True);(A/'Models').mkdir(exist_ok=True);(A/'Prefabs').mkdir(exist_ok=True)
for node in mats['Walnut'].node_tree.nodes:
 if node.type=='TEX_IMAGE':node.image=paint
base_finish=finish
def finish():
 for o in parts:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 return base_finish()
# Broad intentional profiles, keeping all work-surface and attachment datums.
def plan(n,pts,y0,y1,k='Walnut',b=.004):
 N=len(pts);return mesh(n,[(x,y,z) for y in [y0,y1] for x,z in pts],[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],k,b)
def sweep(n,xy,profile,z=0,k='Walnut'):
 vs=[];N=len(profile)
 for j,(x,y) in enumerate(xy):
  a=xy[max(0,j-1)];b=xy[min(len(xy)-1,j+1)];dx=b[0]-a[0];dy=b[1]-a[1];ll=math.hypot(dx,dy);nx=-dy/ll;ny=dx/ll
  for u,v in profile:vs.append((x+u*nx,y+u*ny,z+v))
 fs=[tuple(reversed(range(N))),tuple(range((len(xy)-1)*N,len(xy)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(xy)-1) for i in range(N)]
 return mesh(n,vs,fs,k)
def ogee(w,d):return [(-w*.5,-d*.5),(-w*.5,d*.25),(-w*.39,d*.5),(-w*.23,d*.5),(-w*.12,d*.24),(w*.08,d*.17),(w*.31,d*.46),(w*.45,d*.5),(w*.5,d*.34),(w*.5,-d*.5)]
def relieved_panel(n,cx,y,w,h,z,seed=0,k='Walnut'):
 # Continuous carved wood field: the leaf volumes grow out of the same surface, no loose applique.
 leaves=[(-.27,-.22,-.60,.04,.105,.039),(.03,-.08,.45,.19,.10,.034),(-.04,.10,-.48,.39,.10,.035),(.07,.29,.39,.57,.074,.030)]
 vs=[];nx=42;ny=56
 for j in range(ny+1):
  v=j/ny;yy=y+(v-.5)*h
  for i in range(nx+1):
   u=i/nx;xx=cx+(u-.5)*w;X=(u-.5)*2;Y=(v-.5)*2
   relief=0
   # flowing stem between asymmetric paired leaves
   stemx=.085*math.sin((Y+.5)*3+seed*.4)
   relief=max(relief,.016*math.exp(-((X-stemx)/.046)**2)*max(0,1-abs(Y)/.90))
   for ax,ay,bx,by,ww,dep in leaves:
    if seed%2:ax,bx=-ax,-bx
    dx=bx-ax;dy=by-ay;t=((X-ax)*dx+(Y-ay)*dy)/(dx*dx+dy*dy)
    if 0<t<1:
     dd=abs((X-ax)*dy-(Y-ay)*dx)/math.hypot(dx,dy);width=ww*math.sin(math.pi*t)**.75
     if dd<width:relief=max(relief,dep*math.sin(math.pi*t)**.65*(1-(dd/width)**2)**1.2)
   # Broad rising bevel around recessed field, integrated rather than an extra strip.
   edge=min(u,1-u,v,1-v);rim=.011*max(0,1-edge/.075)**1.5
   vs.append((xx,yy,z+relief+rim))
 fs=[(j*(nx+1)+i,j*(nx+1)+i+1,(j+1)*(nx+1)+i+1,(j+1)*(nx+1)+i) for j in range(ny) for i in range(nx)]
 o=mesh(n,vs,fs,k);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Solid carved panel','SOLIDIFY');mod.thickness=.022;mod.offset=-1;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o
# COUNTER: new framed carcass, concave/scalloped apron, swelling end standards, proper recessed fields.
start('CM_R06_SalesCounter',None,[['WorkSurface',[0,1.0525,0]],['Customer',[0,0,1.2]],['Shopkeeper',[0,0,-1.1]]])
box('Closed back and drawer carcass',(0,.49,-.015),(2.04,.70,.57),'Walnut',.016)
plan('Splayed shaped plinth',[(-1.08,-.32),(1.08,-.32),(1.12,-.27),(1.12,.29),(1.06,.35),(-1.06,.35),(-1.12,.29),(-1.12,-.27)],.045,.13,b=.013)
# Real engaged standards, flowing bulge/splay instead of stacked boxes.
for x in [-1.025,1.025]:
 for z in [-.27,.28]:
  loft('Hand-shaped cabinet standard',[(.08,.065,.060,x,z),(.16,.070,.063,x,z),(.22,.054,.049,x,z),(.34,.047,.043,x,z),(.65,.055,.049,x+.006*(1 if x>0 else -1),z),(.79,.074,.068,x,z),(.86,.065,.060,x,z),(.96,.078,.072,x,z)],'Walnut',24)
# Molded rails are continuous ogees with true reveal depth.
for yy in [.20,.83]:sweep('Counter compound rail',[(-1.045,yy),(1.045,yy)],ogee(.075,.058),.328)
for x,w in [(-.715,.56),(0,.66),(.715,.56)]:
 # Panel sitting within structural frame, not a second cabinet laid over the first.
 relieved_panel('Carved continuous botanical field',x,.51,w,.55,.337,0 if x<0 else 1)
for x in [-.371,.371]:
 loft('Shaped dividing mullion',[(.21,.025,.027,x,.354),(.26,.036,.034,x,.354),(.71,.030,.029,x,.354),(.81,.040,.035,x,.354)],'Walnut',16)
outline('Integral flowing apron',[(-1.10,.96),(1.10,.96),(1.08,.86),(.96,.83),(.83,.76),(.69,.79),(.52,.83),(.27,.84),(0,.81),(-.28,.845),(-.57,.82),(-.80,.77),(-.97,.83),(-1.10,.86)],(.27,.36),'Walnut',.009)
for j,(z0,z1) in enumerate([(-.39,-.13),(-.127,.13),(.133,.39)]):
 plan('Hand-planed bullnose worktop',[(-1.10,z0),(1.10,z0),(1.14,z0+.028),(1.14,z1-.026),(1.105,z1),(-1.105,z1),(-1.14,z1-.023),(-1.14,z0+.026)],.984,1.0525,b=.012)
# Drawer boxes, shaped fronts, inset fields and independently visible bails on staff face.
old=len(parts)
for y in [.51,.76]:
 for x in [-.66,0,.66]:
  outline('Shouldered drawer face',[(x-.31,y-.095),(x+.31,y-.095),(x+.322,y-.065),(x+.31,y+.065),(x+.25,y+.095),(x-.25,y+.095),(x-.31,y+.065)],(.284,.329),'Walnut',.009)
  outline('Inset drawer field',[(x-.255,y-.051),(x+.255,y-.051),(x+.26,y+.035),(x+.22,y+.060),(x-.22,y+.060),(x-.26,y+.035)],(.329,.338),'Sage',.004)
  tube('Drop bail',[(x-.052,y+.008,.339),(x-.056,y-.023,.363),(x,y-.036,.375),(x+.056,y-.023,.363),(x+.052,y+.008,.339)],.007,'Iron')
for o in parts[old:]:
 for v in o.data.vertices:v.co.y=-v.co.y
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Frame-and-panel ends, readable without the counter's loose dressing.
for side in [-1,1]:
 o=relieved_panel('End-grain framed side carving',0,.51,.43,.52,.01,1)
 for v in o.data.vertices:
  X,Z,Y=v.co;v.co=P((side*(1.065+Z),Y,X))
finish()
# SHELVING: complete construction replacement. Existing four stock-course datums remain exact.
start('CM_R06_MedicineShelving',None,[['WallFix',[0,1.7,-.17]],['Shelf1',[0,.53,.015]],['Shelf2',[0,.99,.015]],['Shelf3',[0,1.45,.015]],['Shelf4',[0,1.91,.015]]])
for j in range(7):
 x=-.73+j*.243
 outline('Hand-planed fitted backboard',[(x-.119,.09),(x+.119,.09),(x+.119,2.16),(x+.09,2.23),(x-.08,2.23),(x-.119,2.16)],(-.174,-.133),'Sage',.004)
for side in [-1,1]:
 x=side*.856
 loft('Coved cabinet stile',[(0,.051,.175,x,0),(.08,.060,.181,x,0),(.15,.048,.165,x,0),(.42,.046,.165,x,0),(.52,.057,.178,x,0),(1.96,.043,.160,x,0),(2.12,.055,.174,x,0),(2.20,.058,.18,x,0)],'Walnut',16)
 # Side panels have functional solid rear portions and scooped front edges; shelves house into them.
 outline('Sculpted cabinet side cheek',[(x-.04,.12),(x+.04,.12),(x+.04,2.13),(x,2.21),(x-.04,2.13)],(-.15,.15),'Walnut',.006)
for yy in [.08,.50,.96,1.42,1.88,2.18]:
 # Same stock-contact tops as original shelves: yy+.0275
 plan('Housed shelf with bowed front',[(-.86,-.17),(.86,-.17),(.886,.15),(.84,.192),(.45,.205),(0,.212),(-.46,.204),(-.84,.192),(-.886,.15)],yy-.0275,yy+.0275,b=.006)
 sweep('Continuous carved shelf nose',[(-.85,yy-.014),(-.48,yy-.015),(0,yy-.014),(.45,yy-.015),(.85,yy-.014)],ogee(.052,.035),.196)
for yy in [.49,.95,1.41,1.87,2.17]:
 for side in [-1,1]:
  x=side*.814
  # Real curved shelf corbel within end bay, not thin front ornament.
  points=[(x-side*.055,yy-.025),(x+side*.026,yy-.025),(x+side*.026,yy-.22),(x-side*.018,yy-.215),(x-side*.03,yy-.16),(x-side*.08,yy-.085)]
  outline('Housed scalloped shelf console',points,(.10,.197),'Walnut',.006)
# Lower apothecary drawers; unbroken storage body, mortised divisions.
for x in [-.56,0,.56]:
 box('Drawer box',(x,.285,-.015),(.52,.35,.28),'Walnut',.008)
 outline('Arched drawer front',[(x-.25,.13),(x+.25,.13),(x+.254,.40),(x+.18,.445),(x-.18,.445),(x-.254,.40)],(.15,.207),'Walnut',.006)
 relieved_panel('Carved drawer panel',x,.28,.41,.235,.211,1)
 tube('Forged drawer bail',[(x-.035,.29,.221),(x-.037,.26,.244),(x,.25,.25),(x+.037,.26,.244),(x+.035,.29,.221)],.006,'Iron')
# Connected arched pediment rather than a triangle of boards with a printed decal.
crown=[(-.912,2.17),(.912,2.17),(.912,2.25),(.78,2.26),(.66,2.30),(.47,2.32),(.28,2.38),(.10,2.425),(-.08,2.45),(-.25,2.40),(-.43,2.34),(-.65,2.31),(-.79,2.27),(-.912,2.26)]
outline('Continuous carved swan-neck pediment',crown,(-.17,.168),'Walnut',.009)
sweep('Broken-wave crown rim',[(-.89,2.245),(-.77,2.26),(-.65,2.295),(-.43,2.325),(-.25,2.385),(-.08,2.435),(.10,2.41),(.28,2.365),(.47,2.305),(.66,2.285),(.79,2.245),(.89,2.235)],ogee(.035,.039),.17)
finish()
# TRUE FITTED MASONRY: tailored to the installed widened leaf, not scaled legacy voussoirs.
start('CM_R06_EntranceMasonry')
spring=1.78;ri=1.025;hi=.91;ro=1.274;ho=1.20
# Joint bed is a continuous fitted architectural arch behind the finished stones.
archinner=[(ri*math.cos(i*math.pi/64),spring+hi*math.sin(i*math.pi/64)) for i in range(65)]
archouter=[(ro*math.cos(i*math.pi/64),spring+ho*math.sin(i*math.pi/64)) for i in reversed(range(65))]
outline('Structural arch bedding',archinner+archouter,(-.005,.235),'Linen',0)
for side in [-1,1]:
 for i in range(5):
  y0=.002+i*spring/5+.003;y1=(i+1)*spring/5-.003
  # Jamb and reveal are a single solid block, with front shoulder coved back toward plaster.
  outline('Bonded dressed jamb',[(side*ri,y0),(side*ro,y0+.003),(side*ro,y1),(side*ri,y1)],(-.045,.24),'Linen',.010)
for i in range(13):
 a=i*math.pi/13+.003;b=(i+1)*math.pi/13-.003
 inner=[(ri*math.cos(a+(b-a)*j/6),spring+hi*math.sin(a+(b-a)*j/6)) for j in range(7)]
 outer=[(ro*math.cos(b-(b-a)*j/6),spring+ho*math.sin(b-(b-a)*j/6)) for j in range(7)]
 outline('Radially fitted arch voussoir',inner+outer,(-.049 if i==6 else -.04,.24),'Linen',.010)
finish()
# PLASTER is a continuous arch-headed lintel/spandrel, replacing old rectangular lintel and patch pieces.
start('CM_R06_EntrancePlaster')
pts=[(2.7,3.3),(4.7,3.3)]
for i in range(65):
 x=4.7-2*i/64;xx=x-3.7;y=.2+spring+hi*math.sqrt(max(0,1-(xx/ri)**2));pts.append((x,y))
outline('Fitted plaster lintel and intrados',pts,(-.20,0),'Linen',.002)
finish()
# ONE coherent timber doorway, fitted at actual wall thickness; no mirrored dangling applique posts.
for name,w in [('CM_R06_TreatmentFrame',2.0),('CM_R06_KitchenFrame',1.8)]:
 start(name,None,[['ClearOpening',[0,0,0]]])
 for side in [-1,1]:
  x=side*(w/2+.075)
  loft('Housed door jamb',[(0,.070,.126,x,0),(.10,.077,.132,x,0),(.19,.063,.126,x,0),(2.55,.063,.126,x,0),(2.64,.078,.137,x,0),(2.75,.080,.14,x,0)],'Walnut',16)
 # Head and jambs actually meet, both faces finished, full original clear height retained.
 sweep('Joined molded lintel',[(-w/2-.15,2.83),(w/2+.15,2.83)],ogee(.16,.28),0)
 for side in [-1,1]:
  x=side*(w/2+.08)
  for z in [-.142,.142]:rod('Drawbored head joint',(x,2.79,z-.006),(x,2.79,z+.006),.014,'Walnut',12)
 finish()
# CANOPY: 05 arch is sound; replace the parallel disconnected inner arch with correctly seated geometry later only if inspection warrants.
# Save unconverted editable originals, then export through the validated native conversion.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_Reconstruction06.blend'));conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps({'modules':catalog,'axes':'Unity +Y up / +Z exterior','scaleMetres':1},indent=2));print('RECONSTRUCTION06_READY',len(catalog))
