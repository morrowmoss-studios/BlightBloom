"""Two controlled craft benchmarks. Sculptural derivatives, no loose props or architecture rebuild."""
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4]
text=(R/'ArtSource/Blender/Interiors/CrookedMortar/LivedIn03/build_lived03.py').read_text().split('# Back face is exactly')[0].replace("CrookedMortar/LivedIn03'","CrookedMortar/Craftsmanship05'")
exec(compile(text,str(__file__),'exec'))
for node in mats['Walnut'].node_tree.nodes:
 if node.type=='TEX_IMAGE':node.image=paint
# All forms use the established matte approved paint. Grain follows each part's longitudinal UV axis.
def plan_solid(n,pts,y0,y1,k='Walnut',b=.004):
 N=len(pts);return mesh(n,[(x,y,z) for y in [y0,y1] for x,z in pts],[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],k,b)
def hewn_beam(n,c,L,h,d):
 # Continuous coved section and subtle author-placed centreline, rather than a block with strips on it.
 yz=[(-.50,-.45),(-.45,-.50),(.43,-.50),(.50,-.43),(.50,.40),(.43,.50),(.29,.50),(.22,.41),(-.20,.41),(-.30,.49),(-.43,.50),(-.50,.41)]
 vs=[];N=len(yz);steps=24
 for j in range(steps+1):
  t=j/steps;x=c[0]-L/2+L*t;dy=.003*math.sin(math.pi*t)*math.sin(math.pi*t*2);scale=1-.018*math.sin(math.pi*t)**2
  for yy,zz in yz:vs.append((x,c[1]+h*yy*scale+dy,c[2]+d*zz))
 fs=[tuple(reversed(range(N))),tuple(range(steps*N,(steps+1)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(steps) for i in range(N)]
 return mesh(n,vs,fs,'Walnut',.003)
def timber_post(n,x,y0,y1,z,w,d):
 levels=[(y0,w,d),(y0+.10,w,d),(y0+.17,w*.83,d*.96),(y0+.40,w*.82,d*.95),(y1-.35,w*.88,d*.97),(y1-.16,w*.80,d*.96),(y1-.10,w,d),(y1,w,d)]
 section=[(-.5,-.42),(-.42,-.5),(.42,-.5),(.5,-.42),(.5,.42),(.42,.5),(.27,.5),(.19,.44),(-.2,.44),(-.29,.5),(-.42,.5),(-.5,.42)]
 vs=[];N=len(section)
 for j,(y,ww,dd) in enumerate(levels):
  drift=.0015*math.sin(j*1.1) if j not in [0,len(levels)-1] else 0
  for xx,zz in section:vs.append((x+ww*xx+drift,y,z+dd*zz))
 fs=[tuple(reversed(range(N))),tuple(range((len(levels)-1)*N,len(levels)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(levels)-1) for i in range(N)]
 return mesh(n,vs,fs,'Walnut',.003)
def leaf_relief(n,a,b,width,z,depth=.013):
 # Real lenticular carved volume, not a printed leaf on a quad.
 ax,ay=a;bx,by=b;dx=bx-ax;dy=by-ay;length=math.hypot(dx,dy);nx=-dy/length;ny=dx/length
 vs=[]
 for t,w in [(0,0),(.23,width*.65),(.55,width),(.82,width*.57),(1,0)]:
  for side in [-1,0,1]:vs.append((ax+dx*t+nx*w*side,ay+dy*t+ny*w*side,z+depth*math.sin(math.pi*t)*(1 if side==0 else .08)))
 fs=[(j*3+i,j*3+i+1,(j+1)*3+i+1,(j+1)*3+i) for j in range(4) for i in range(2)];o=mesh(n,vs,fs,'Walnut');bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Carving root thickness','SOLIDIFY');mod.thickness=.002;bpy.ops.object.modifier_apply(modifier=mod.name)
def vine_carving(x,y,z,side=1):
 # A curved branching herb/root motif. Paired fields have deliberately different silhouettes.
 ps=[(x-.03*side,y-.19,z),(x-.09*side,y-.13,z),(x-.06*side,y-.04,z+.002),(x+.035*side,y+.04,z+.002),(x+.02*side,y+.13,z),(x+.07*side,y+.22,z)]
 tube('Continuous carved botanical branch',ps,.0075,'Walnut')
 for j,(yy,sg,ln) in enumerate([(-.12,-1,.13),(-.025,1,.15),(.065,-1,.13),(.13,1,.09)]):
  leaf_relief('Modelled branching sage leaf',(x, y+yy),(x+sg*ln,y+yy+.09),.032 if side<0 else .023,z,.014)
 # Root curl grows into the lower frame, not a separate applied symbol.
 curl=[(x+side*(.085+.052*math.cos(i*.20)),y-.13+.052*math.sin(i*.20),z+.004) for i in range(25)]
 tube('Carved root volute',curl,.007,'Walnut')
# A replacement carcass, not an overlay over a rectangular prototype.
start('CM_C05_SalesCounter')
# Footboard, stepped plinth and a recessed carcass preserve the exact working envelope.
box('Cabinet core',(0,.48,-.015),(2.05,.73,.63),'Walnut',.014)
plan=[(-1.10,-.35),(1.10,-.35),(1.13,-.31),(1.13,.31),(1.09,.35),(-1.09,.35),(-1.13,.31),(-1.13,-.31)]
plan_solid('Octagonal base moulding',plan,.025,.095,'Walnut',.012)
for sign in [-1,1]:
 for z in [-.29,.31]:
  x=sign*1.035
  loft('Carved engaged cabinet column',[(.08,.055,.055,x,z),(.16,.063,.060,x,z),(.22,.041,.043,x,z),(.70,.046,.043,x+sign*.003,z),(.77,.063,.060,x,z),(.86,.058,.055,x,z),(.93,.066,.06,x,z)],'Walnut',16)
# Three genuinely recessed fields with shaped top rails and carved stiles.
for x,w in [(-.73,.55),(0,.67),(.73,.55)]:
 outline('Arched recessed walnut field',[(x-w/2,.25),(x+w/2,.25),(x+w/2,.68),(x+w*.36,.75),(x,.79),(x-w*.36,.75),(x-w/2,.68)],(.345,.375),'Sage',.012)
 # Raised frame follows a shaped panel perimeter instead of masking a flat rectangle with an image.
 pts=[(x-w/2,.25,.401),(x+w/2,.25,.401),(x+w/2,.68,.401),(x+w*.36,.75,.401),(x,.79,.401),(x-w*.36,.75,.401),(x-w/2,.68,.401),(x-w/2,.25,.401)]
 tube('Hand carved panel bead',pts,.016,'Walnut')
for x in [-.73,.73]:vine_carving(x,.48,.387,1 if x<0 else -1)
# Central mortar bas-relief with real convex surfaces, restrained to the previous applique depth.
loft('Carved mortar bowl',[(.37,.085,.012,0,.391),(.40,.12,.018,0,.393),(.52,.17,.027,0,.395),(.56,.175,.028,0,.395),(.58,.15,.023,0,.394)],'Walnut',36)
rod('Carved relief pestle',(-.065,.52,.407),(.12,.75,.409),.020,'Walnut',16)
for side in [-1,1]:leaf_relief('Mortar wreath',(side*.19,.39),(side*.24,.64),.035,.393,.012)
box('Curved lower panel stretcher',(0,.215,.35),(2.10,.07,.09),'Walnut',.014)
# A continuous pierced/scalloped apron supports the worktop between engaged capitals.
outline('Sweeping carved apron',[(-1.08,.96),(1.08,.96),(1.06,.85),(.89,.83),(.72,.80),(.42,.83),(0,.79),(-.39,.84),(-.74,.81),(-.93,.84),(-1.08,.86)],(.30,.365),'Walnut',.009)
# Three broad hand-planed planks. The support datum remains 1.0525m for existing objects and markers.
for j,(z0,z1) in enumerate([(-.39,-.13),(-.127,.13),(.133,.39)]):
 pts=[(-1.11,z0),(1.10,z0),(1.14,z0+.025),(1.14,z1-.025),(1.105,z1),(-1.11,z1),(-1.14,z1-.022),(-1.14,z0+.025)]
 plan_solid('Soft bullnose worktop plank '+str(j),pts,.984,1.0525,'Walnut',.010)
# Service drawers face -Z and retain the original working access.
old=len(parts)
for yy in [.75,.51]:
 for j in range(3):
  x=(j-1)*.66
  outline('Curved drawer front',[(x-.314,yy-.09),(x+.314,yy-.09),(x+.325,yy-.055),(x+.314,yy+.075),(x+.23,yy+.095),(x-.23,yy+.095),(x-.314,yy+.075)],(.288,.328),'Walnut',.008)
  outline('Recessed painted drawer field',[(x-.26,yy-.055),(x+.26,yy-.055),(x+.27,yy+.04),(x+.23,yy+.063),(x-.23,yy+.063),(x-.27,yy+.04)],(.327,.334),'Sage',.005)
  tube('Forged drawer bail',[(x-.05,yy,.334),(x-.05,yy-.016,.368),(x,yy-.027,.375),(x+.05,yy-.016,.368),(x+.05,yy,.334)],.008,'Brass')
for o in parts[old:]:
 for v in o.data.vertices:v.co.y=-v.co.y
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
finish()
# Approved portal opening and centreline are retained. New profiles are genuinely modelled.
start('CM_C05_EntrancePortal')
for side in [-1,1]:
 x=side*1.1;timber_post('Tapered fluted portal post',x,.02,2.52,0,.145,.145)
 for y0,y1,w,d in [(.035,.075,.21,.21),(.075,.26,.196,.196),(.26,.325,.21,.21),(2.49,2.54,.19,.19),(2.54,2.59,.23,.21),(2.59,2.61,.21,.20)]:
  box('Shaped shoe and capital',(x,(y0+y1)/2,0),(w,y1-y0,d),'Walnut',min(.009,(y1-y0)*.2))
 for y in [.16,2.55]:rod('Driven oak drawbore',(x,y,.065),(x,y,.107),.014,'Walnut',12)
# Compound coved arch section swept continuously over the original quadratic curve.
def arch(n,a,c,b,width,depth,z):
 points=[(-.5,-.42),(-.42,-.5),(.42,-.5),(.5,-.42),(.5,.32),(.42,.5),(.26,.5),(.20,.40),(-.20,.40),(-.28,.5),(-.42,.5),(-.5,.34)];N=len(points);vs=[];steps=60
 for j in range(steps+1):
  t=j/steps;x=(1-t)**2*a[0]+2*(1-t)*t*c[0]+t*t*b[0];y=(1-t)**2*a[1]+2*(1-t)*t*c[1]+t*t*b[1];tx=2*(1-t)*(c[0]-a[0])+2*t*(b[0]-c[0]);ty=2*(1-t)*(c[1]-a[1])+2*t*(b[1]-c[1]);length=math.hypot(tx,ty);nx=-ty/length;ny=tx/length
  for u,v in points:vs.append((x+nx*u*width,y+ny*u*width,z+v*depth))
 fs=[tuple(reversed(range(N))),tuple(range(steps*N,(steps+1)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(steps) for i in range(N)];return mesh(n,vs,fs,'Walnut',.002)
arch('Coved outer architectural arch',(-1.1,2.5),(0,3.34),(1.1,2.5),.16,.16,0)
arch('Rounded inner architrave',(-.97,2.4),(0,3.10),(.97,2.4),.055,.055,.08)
# Shallow curved carved leaves are integrated into the existing capital faces, not hanging ornaments.
for side in [-1,1]:leaf_relief('Capital acanthus', (side*1.1,2.47),(side*1.1+.035*side,2.59),.028,.109,.008)
finish()
start('CM_C05_FrontTimber')
for y in [3.47,6.74]:
 hewn_beam('Coved front storey beam',(2.7,y,-.17),5.40,.218,.40)
 for x in [.12,5.28]:rod('Floor beam oak drawbore',(x,y,-.355),(x,y,-.384),.022,'Walnut',12)
for x in [-.11,5.51]:
 for y0,y1 in [(.20,3.45),(3.60,6.85)]:timber_post('Hewn front corner post',x,y0,y1,-.17,.18,.40)
finish()
start('CM_C05_ShopBeam')
hewn_beam('Continuous coved shop beam',(0,0,0),5.4,.16,.17)
for sign in [-1,1]:
 x=sign*2.64;box('Shaped beam bearing',(x,-.12,0),(.10,.40,.22),'Walnut',.014)
 outline('Curved timber knee',[(x-sign*.05,-.04),(x+sign*.05,-.04),(x+sign*.05,-.30),(x,-.28),(x-sign*.025,-.21),(x-sign*.07,-.10)],(-.1,.1),'Walnut',.008)
finish()
# Preserve all openings and original UVs in measured wall meshes; broad authored plaster swelling only.
measured=json.loads((D/'MeasuredSurfaces.json').read_text())
for k,row in enumerate(measured):
 key='CM_C05_StoneSurround' if row['name'].startswith('Fitted Entry') else 'CM_C05_Plaster_'+str(k)
 start(key);vs=[P(v) for v in row['vertices']];me=bpy.data.meshes.new(key);me.from_pydata(vs,[],[tuple(row['triangles'][i:i+3]) for i in range(0,len(row['triangles']),3)]);me.update();o=bpy.data.objects.new(key,me);s.collection.objects.link(o);me.materials.append(mats['Linen']);uv=me.uv_layers.new(name='PaintUV')
 for p in me.polygons:
  for li in p.loop_indices:uv.data[li].uv=row['uv'][me.loops[li].vertex_index]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.subdivide_edges(bm,edges=list(bm.edges),cuts=2 if key.endswith('StoneSurround') else 5,use_grid_fill=True)
 # A few explicit broad trowel pads, not a noise displacement or new wall plane.
 for v in bm.verts:
  x,z,y=v.co
  if key.endswith('StoneSurround'):
   if z<.025:v.co.y-=.0028*math.exp(-((x-.8)/.45)**2-((y-1.6)/.65)**2)+.002*math.exp(-((x+.9)/.35)**2-((y-1.0)/.6)**2)
  elif z<-.19:
   amount=sum(amp*math.exp(-((x-cx)/sx)**2-((y-cy)/sy)**2) for cx,cy,sx,sy,amp in [(1.0,2.95,.8,.6,.005),(5.1,1.1,.3,.7,.006),(3.8,5.7,.8,.7,.005),(1.0,4.1,.6,.5,.004)])
   v.co.y-=amount
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 me.set_sharp_from_angle(angle=math.radians(38))
 parts.append(o);finish()
# Retain the corrected roof-edge junction vertices. Cove only the two front horizontal eave faces.
for row in json.loads((D/'MeasuredEaves.json').read_text()):
 start('CM_C05_EaveTimber');me=bpy.data.meshes.new('FittedEaveDerivative');me.from_pydata([P(v) for v in row['vertices']],[],[tuple(row['triangles'][i:i+3]) for i in range(0,len(row['triangles']),3)]);me.update();o=bpy.data.objects.new(current,me);s.collection.objects.link(o);me.materials.append(mats['Walnut']);uv=me.uv_layers.new(name='PaintUV')
 for p in me.polygons:
  for li in p.loop_indices:uv.data[li].uv=row['uv'][me.loops[li].vertex_index]
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 chosen=[e for e in bm.edges if all(v.co.y<-.8 and 3.0<v.co.z<3.65 for v in e.verts)]
 bmesh.ops.subdivide_edges(bm,edges=chosen,cuts=5,use_grid_fill=True)
 for v in bm.verts:
  x,z,y=v.co
  # Author-selected eave spans; joint end zones and all upper/rear roof geometry stay fixed.
  for left,right,face,cy in [(-.35,2.25,-1.95,3.22),(2.25,5.85,-2.90,3.24)]:
   if left+.15<x<right-.15 and abs(z-face)<.13 and abs(y-cy)<.10:
    end=min(1,(x-left-.15)/.16,(right-.15-x)/.16);v.co.y+=.008*end*math.exp(-((y-cy)/.035)**2)
 bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
 me.set_sharp_from_angle(angle=math.radians(38));parts.append(o);finish()
# Fitted plaster spandrels close the existing rectangular-to-arched reveal corner voids.
# Both patches lie outside the measured arched door leaf, leaving its full sweep untouched.
start('CM_C05_EntranceReturns')
left=[(2.68,2.97),(2.92,2.97),(2.92,2.94),(2.86,2.86),(2.78,2.79),(2.68,2.73)]
for side in [-1,1]:outline('Fitted plaster arch spandrel',left if side<0 else [(7.4-x,y) for x,y in left],(-.199,-.015),'Linen',.002)
finish()
report={'modules':catalog,'axes':'Unity +Y up / +Z front','scaleMetres':1,'notes':'Only two benchmarks: existing front architecture and shop counter. No loose objects added. Existing colliders and markers preserved.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_Craftsmanship05.blend'));conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 if '--export-only' in sys.argv and entry['name'] not in sys.argv[sys.argv.index('--export-only')+1:]:continue
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps(report,indent=2));print('CRAFT05_READY',len(catalog))
