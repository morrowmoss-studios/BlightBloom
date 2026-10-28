"""One reference-specified cabinet. Bespoke sections, housed construction, closed drawers,
real shell pulls, shaped living foliage. Does not import, modify or save any Unity scene."""
import bpy,bmesh,math,json,random
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];T=D/'Textures';E=D/'Exports'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));mats={};parts=[];groups={};current='';serial=0
# Preserve separate logical source groups; game exports batch only coherent pieces.
def group(n):
 global current
 current=n;c=bpy.data.collections.new(n);s.collection.children.link(c);groups[n]=c

def material(n,tex=None,col=(1,1,1,1),rough=.9,metal=0,alpha=False):
 m=bpy.data.materials.new(n);m.use_nodes=True;m.diffuse_color=col;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=col;bs.inputs['Roughness'].default_value=rough;bs.inputs['Metallic'].default_value=metal
 if tex:
  im=m.node_tree.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(T/tex),check_existing=True);im.image.pack();mul=m.node_tree.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=col;m.node_tree.links.new(im.outputs['Color'],mul.inputs[1]);m.node_tree.links.new(mul.outputs[0],bs.inputs['Base Color'])
  if alpha:
   clip=m.node_tree.nodes.new('ShaderNodeMath');clip.operation='GREATER_THAN';clip.inputs[1].default_value=.40;m.node_tree.links.new(im.outputs['Alpha'],clip.inputs[0]);m.node_tree.links.new(clip.outputs[0],bs.inputs['Alpha']);m.surface_render_method='DITHERED';m.use_backface_culling=False
 mats[n]=m;return m
wood=material('CM_MMC01_Walnut','CM_MMC01_CabinetPaint.png',(.62,.55,.44,1));shade=material('CM_MMC01_CutWalnut','CM_MMC01_CabinetPaint.png',(.72,.65,.52,1));sage=material('CM_MMC01_SageBacking','CM_MMC01_CabinetPaint.png',(.58,.66,.49,1));brass=material('CM_MMC01_AgedBrass',col=(.38,.22,.055,1),rough=.47,metal=.65);paper=material('CM_MMC01_Parchment',col=(.60,.49,.29,1));stem=material('CM_MMC01_VineStem',col=(.13,.16,.045,1));rope=material('CM_MMC01_Rope',col=(.36,.27,.13,1));iron=material('CM_MMC01_ForgedIron',col=(.09,.075,.052,1),rough=.75,metal=.3);leafmat=material('CM_MMC01_PaintedIvy','CM_MMC01_LivingBotany.png',col=(.43,.55,.30,1),alpha=True);mossmat=material('CM_MMC01_PaintedMoss','CM_MMC01_LivingBotany.png',col=(.43,.55,.30,1),alpha=True);ceramic=material('CM_MMC01_SageCeramic','CM_MMC01_ReusedCeramicPaint.png',rough=.78);soil=material('CM_MMC01_Soil',col=(.055,.04,.022,1))

def finishmesh(o,bevel=0):
 bpy.context.view_layer.objects.active=o
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 if bevel:
  mod=o.modifiers.new('Dressed arris - controlled width','BEVEL');mod.width=bevel;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8);bm.to_mesh(o.data);bm.free()
 for f in o.data.polygons:f.use_smooth=True
 o.data.set_sharp_from_angle(angle=math.radians(38))

def uvpaint(o,kind='vertical',index=0):
 me=o.data;uv=me.uv_layers.new(name='PaintUV') if not me.uv_layers else me.uv_layers[0];lo=Vector(tuple(min(v.co[i] for v in me.vertices) for i in range(3)));hi=Vector(tuple(max(v.co[i] for v in me.vertices) for i in range(3)));along=max(range(3),key=lambda i:hi[i]-lo[i])
 for f in me.polygons:
  drop=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=drop]
  if kind in ['vertical','sage']:
   va=2 if 2 in axes else along if along in axes else axes[1];ua=next(i for i in axes if i!=va);base=(.012,.512) if kind=='vertical' else (.012,.012)
  else:
   ua=along if along in axes else axes[0];va=next(i for i in axes if i!=ua);base=(.512,.512) if kind=='horizontal' else (.512,.012)
  spanU=(hi[ua]-lo[ua])*.235;spanV=(hi[va]-lo[va])*.235;ou=.005+((index*.071)%max(.005,.47-spanU));ov=.005+((index*.047)%max(.005,.47-spanV))
  for li in f.loop_indices:
   p=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(base[0]+ou+(p[ua]-lo[ua])*.235,base[1]+ov+(p[va]-lo[va])*.235)

def mesh(n,vs,fs,m=wood,bevel=0,paint='vertical',register=True):
 global serial
 me=bpy.data.meshes.new(n);me.from_pydata([P(v) for v in vs],[],fs);me.update();o=bpy.data.objects.new(n,me);groups[current].objects.link(o);me.materials.append(m);finishmesh(o,bevel);serial+=1;uvpaint(o,paint,serial);o['logical_group']=current;o['solid']=True
 if register:parts.append(o)
 return o

def extrude(n,poly,z0,z1,m=wood,b=.004,paint='vertical'):
 poly=[p for i,p in enumerate(poly) if i==0 or (Vector(p)-Vector(poly[i-1])).length>1e-7]
 if (Vector(poly[0])-Vector(poly[-1])).length<1e-7:poly=poly[:-1]
 N=len(poly);return mesh(n,[(x,y,z) for z in [z0,z1] for x,y in poly],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m,b,paint)
def slab(n,poly,y0,y1,m=wood,b=.004):
 N=len(poly);return mesh(n,[(x,y,z) for y in [y0,y1] for x,z in poly],[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m,b,'horizontal')
def bez(c,N=20):
 a,b,c,d=[Vector(p) for p in c];return [tuple((1-t)**3*a+3*t*(1-t)**2*b+3*t*t*(1-t)*c+t**3*d) for t in [i/N for i in range(N+1)]]
def sweep(n,path,profile,m=wood,paint='trim'):
 points=[Vector(v) for v in path];closed=(points[-1]-points[0]).length<1e-6
 if closed:points=points[:-1]
 vs=[];N=len(profile)
 for i,p in enumerate(points):
  tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();ref=Vector((0,0,1));side=ref.cross(tangent)
  if side.length<.01:side=Vector((1,0,0))
  side.normalize();front=tangent.cross(side).normalized()
  for u,v in profile:vs.append(tuple(p+side*u+front*v))
 fs=([(j*N+i,j*N+(i+1)%N,((j+1)%len(points))*N+(i+1)%N,((j+1)%len(points))*N+i) for j in range(len(points)) for i in range(N)] if closed else [tuple(reversed(range(N))),tuple(range((len(points)-1)*N,len(points)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(points)-1) for i in range(N)])
 return mesh(n,vs,fs,m,0,paint)
def tube(n,path,r,m=rope,N=6):return sweep(n,path,[(r*math.cos(i*math.tau/N),r*math.sin(i*math.tau/N)) for i in range(N)],m,'trim')
def section(n,rows,m=wood):
 # Authored octagonal planes; changing cross-sections form actual hewn timbers, not scaled cubes.
 prof=[(-1,-.70),(-.72,-1),(.72,-1),(1,-.70),(1,.70),(.72,1),(-.72,1),(-1,.70)];vs=[]
 for y,x,z,rx,rz in rows:
  for u,v in prof:vs.append((x+u*rx,y,z+v*rz))
 fs=[tuple(reversed(range(8))),tuple(range(len(vs)-8,len(vs)))]+[(j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i) for j in range(len(rows)-1) for i in range(8)]
 return mesh(n,vs,fs,m,.0015)
def pin(n,p,r=.006,m=wood):
 x,y,z=p;N=10;vs=[(x+r*math.cos(t),y+r*math.sin(t),zz) for zz in [z,z+.003] for t in [i*math.tau/N for i in range(N)]];return mesh(n,vs,[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m,.0005,'trim')

group('01_MainStructure')
for side in [-1,1]:
 x=side*.822
 # Four continuous stiles and substantial foot shoulders.
 rows=[(.05,x,.135,.060,.058),(.13,x,.135,.067,.063),(.20,x,.135,.061,.059),(.43,x-side*.002,.135,.057,.058),(.72,x,.135,.063,.060),(1.05,x+side*.002,.135,.057,.058),(1.50,x-side*.001,.135,.058,.060),(1.91,x,.135,.066,.063),(1.97,x,.135,.063,.060)]
 post=section(('Left' if side<0 else 'Right')+' front continuous hewn stile',rows)
 # Actual small botanical V-tool cuts directly into the stile. No attached relief board.
 cutters=[]
 stempath=[(x+.004*math.sin(t*math.pi*1.3),.24+t*.37,.199) for t in [i/12 for i in range(13)]];cut=tube('Carving cutter stem',stempath,.0027,wood,5);cutters.append(cut)
 for k in range(6):
  yy=.28+k*.052;sg=-1 if k%2 else 1;a=(x,yy);tip=(x+sg*.028,yy+.037);mid=((a[0]+tip[0])/2,(a[1]+tip[1])/2)
  poly=[a,(mid[0]-sg*.008,mid[1]+.008),tip,(mid[0]+sg*.008,mid[1]-.008)];cut=extrude('Carving cutter leaf',poly,.191,.211,wood,0);cutters.append(cut)
 for cut in cutters:
  bpy.context.view_layer.objects.active=post;mod=post.modifiers.new('Incised botanical edge tooling','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);parts.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
 finishmesh(post);uvpaint(post,'vertical',3 if side<0 else 8)
 section('Rear upright '+str(side),[(.05,x,-.174,.050,.049),(.2,x,-.174,.052,.049),(1.92,x,-.174,.050,.049)])
 # Foot is a carved bearing block with coved shoulders and a shaped toe, not a formal cabriole leg.
 for zz in [.135,-.173]:
  section('Shouldered foot '+str(side)+' '+str(zz),[(.006,x,zz+.005,.077,.075),(.018,x,zz+.010,.078,.077),(.047,x,zz+.006,.074,.073),(.062,x,zz,.063,.063),(.077,x,zz,.060,.060)])
  for xx in [-.035,0,.035]:
   tube('Foot end-grain tool flute',[(x+xx,.008,zz+.074),(x+xx,.025,zz+.075),(x+xx,.047,zz+.065)],.0017,shade,5)
 for yy in [.18,.65,1.88]:pin('Drawbore fixing',(x,yy,.199),.007)
 # Substantial side infill, inside front/rear stiles. Closed solid and inset moulded stile line.
 poly=[(-.135,.18),(.075,.18),(.075,.642),(-.135,.642)]
 # Side board lies YZ, built as a rotated extruded panel.
 o=extrude('Recessed walnut side field '+str(side),[(-.13,.18),(.078,.18),(.078,.644),(-.13,.644)],-.016,.016,wood,.004)
 for v in o.data.vertices:
  old=v.co.copy();v.co=P((x+side*(old.y),old.z,old.x))
 finishmesh(o);uvpaint(o,'vertical',6 if side<0 else 10)
# Under drawers and load-bearing top rail sit within actual case envelope.
for yy,hh in [(.12,.065)]:
 slab('Broad bearing plinth '+str(yy),[(-.89,-.232),(.89,-.232),(.895,.190),(.875,.222),(-.875,.222),(-.895,.190)],yy,yy+hh,b=.006)
# Four framed drawer rails plus vertical dividers, all behind drawer faces.
for yy in [.179,.402,.625]:extrude('Housed drawer cross rail', [(-.770,yy-.014),(.770,yy-.014),(.770,yy+.014),(-.770,yy+.014)],-.165,.199,b=.003,paint='horizontal')
extrude('Upper drawer bearing apron',[(-.772,.637),(.772,.637),(.772,.672),(-.772,.672)],-.16,.201,b=.002,paint='horizontal')
for xx in [-.772,-.386,0,.386,.772]:extrude('Drawer division stile',[(xx-.012,.178),(xx+.012,.178),(xx+.012,.633),(xx-.012,.633)],-.16,.201,b=.002)
# Crown: a true arched pediment with two differently profiled molded edges, not flat applique.
crest=bez([(-.9,1.947),(-.65,1.947),(-.48,1.947),(-.27,2.015)],22)+bez([(-.27,2.015),(-.09,2.075),(.07,2.075),(.27,2.015)],20)[1:]+bez([(.27,2.015),(.46,1.955),(.66,1.947),(.9,1.947)],22)[1:]
extrude('Continuous arched walnut crown',[(-.9,1.897),(.9,1.897)]+list(reversed(crest)),-.221,.171,b=.005,paint='trim')
profile=[(-.018,-.018),(-.018,.006),(-.012,.013),(-.005,.012),(.002,.003),(.010,.003),(.018,.015),(.022,.009),(.022,-.018)]
sweep('Shaped crown upper cove',[(x,y,.184) for x,y in crest],profile)
sweep('Crown lower bearing ovolo',[(x,1.900+.002*math.sin(x*3),.192) for x in [i*.025-.875 for i in range(71)]],[(-.024,-.014),(-.024,.004),(-.016,.014),(.016,.014),(.024,.003),(.024,-.014)])
# Seated corner knees with an actual changing curved section.
for side in [-1,1]:
 x=side*.778;curve=bez([(x-side*.15,1.892),(x-side*.105,1.889),(x-side*.055,1.85),(x,1.757)],18)
 extrude('Housed crown shoulder knee '+str(side),[(x,1.909),(x-side*.15,1.909)]+curve+[(x,1.757)],.112,.185,b=.005)
# Nine fitted tongue-and-groove back boards. Sage on front, walnut on reverse.
group('02_Backing')
for k in range(9):
 x=-.728+k*.182;left=max(-.805,x-.090);right=min(.805,x+.090)
 o=extrude('Tongued sage back board '+str(k),[(left,.16),(right,.16),(right,1.899),(left,1.899)],-.216,-.193,sage,.002,'sage');o.data.materials.append(wood)
 for f in o.data.polygons:
  if f.normal.y<-.5:f.material_index=1
 # Front/back use their actual treatments with separate paint quadrant, no stretched whole atlas.
 for f in o.data.polygons:
  if abs(f.normal.y)<.5:continue
  for li in f.loop_indices:
   p=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers[0].data[li].uv=(.018+(p.x+.82)*.26,(.012 if f.material_index==0 else .512)+(p.z-.10)*.235)
for yy in [.16,.68,1.30,1.87]:extrude('Rear housed cross batten', [(-.770,yy-.025),(.770,yy-.025),(.770,yy+.025),(-.770,yy+.025)],-.232,-.211,b=.002,paint='horizontal')
# Three wide useful open storage shelves; no contents or false inner partitions.
group('03_Shelves')
for j,yy in enumerate([.726,1.119,1.512]):
 outline=[(-.782,-.190),(.782,-.190),(.782,.181),(.756,.207),(.35,.211),(0,.215),(-.35,.209),(-.756,.207),(-.782,.181)]
 if j==0:
  slab('Lower shelf seated bearing plinth',[(-.89,-.232),(.89,-.232),(.895,.190),(.875,.222),(-.875,.222),(-.895,.190)],.666,.726,b=.006)
  continue
 slab('Nosed solid storage shelf '+str(j),outline,yy-.042,yy,b=.004)
 sweep('Shelf housed bullnose '+str(j),[(x,yy-.024,.203+.004*math.cos(x*3)) for x in [i*.0385-.77 for i in range(41)]],[(-.017,-.011),(-.017,.002),(-.012,.010),(.010,.010),(.017,.001),(.017,-.011)],paint='horizontal')
 for side in [-1,1]:
  x=side*.773;curve=bez([(x-side*.11,yy-.045),(x-side*.065,yy-.049),(x-side*.030,yy-.090),(x,yy-.132)],14)
  extrude('Housed shelf corbel '+str(j)+' '+str(side),[(x,yy-.038),(x-side*.11,yy-.038)]+curve+[(x,yy-.132)],.125,.186,b=.003)
# Drawers: 8 real independent boxes with shaped fronts, not rectangular stamp panels.
group('04_Drawers')
for row in range(2):
 for col in range(4):
  x=(col-1.5)*.386;y=.194+row*.223;w=.358;h=.195;idx=row*4+col
  poly=[(x-w/2+.004,y),(x+w/2-.005,y),(x+w/2,y+.005),(x+w/2-.001,y+h-.005),(x+w/2-.005,y+h),(x-w/2+.005,y+h-.001),(x-w/2,y+h-.006),(x-w/2,y+.005)]
  o=extrude('Drawer%02d - shaped solid front'%(idx+1),poly,.188,.214,wood,.004,'horizontal');o['drawer']=idx+1
  # Real edge rebates frame the drawer body without another ornamental plaque.
  slab('Drawer%02d bottom'%(idx+1),[(x-.165,-.145),(x+.165,-.145),(x+.165,.188),(x-.165,.188)],y+.014,y+.027,b=.0015)
  for xx in [x-.166,x+.166]:extrude('Drawer%02d box side'%(idx+1),[(xx-.008,y+.025),(xx+.008,y+.025),(xx+.008,y+.171),(xx-.008,y+.171)],-.145,.188,b=.0015)
  extrude('Drawer%02d box back'%(idx+1),[(x-.16,y+.025),(x+.16,y+.025),(x+.16,y+.165),(x-.16,y+.165)],-.155,-.140,b=.0015,paint='horizontal')
  # Short exposed end-grain pins and restrained real stopped edge work.
  for dx in [-.156,.156]:
   for dy in [.035,.151]:pin('Drawer%02d wooden joint pin'%(idx+1),(x+dx,y+dy,.215),.0025,shade)
# Shell cup handles and label-holder frames are separate replaceable hardware.
group('05_Hardware')
for row in range(2):
 for col in range(4):
  x=(col-1.5)*.386;y=.194+row*.223;idx=row*4+col
  # outer and inner ellipsoid domes, connected at upper/lower opening rims: a real thin cup.
  N=16;K=5;vs=[]
  for inner in [False,True]:
   for k in range(K):
    v=(math.pi/2-.11)*k/(K-1);r=math.cos(v);d=math.sin(v)
    for i in range(N+1):
     a=math.pi*i/N;vs.append((x+(.047 if not inner else .044)*r*math.cos(a),y+.067+(.028 if not inner else .025)*r*math.sin(a),.219+(.025 if not inner else .021)*d))
   vs.append((x,y+.067,.244 if not inner else .240))
  sidecount=K*(N+1)+1;fs=[]
  for side in range(2):
   off=side*sidecount
   for k in range(K-1):
    for i in range(N):
     f=(off+k*(N+1)+i,off+k*(N+1)+i+1,off+(k+1)*(N+1)+i+1,off+(k+1)*(N+1)+i);fs.append(f if side==0 else tuple(reversed(f)))
   for i in range(N):
    f=(off+(K-1)*(N+1)+i,off+(K-1)*(N+1)+i+1,off+sidecount-1);fs.append(f if side==0 else tuple(reversed(f)))
  # Rim connection around open back arch and bottom longitudinal boundaries.
  boundary=list(range(N+1))+[k*(N+1)+N for k in range(1,K)]+[sidecount-1]+[k*(N+1) for k in reversed(range(1,K))]
  for a,b in zip(boundary,boundary[1:]+boundary[:1]):fs.append((a,b,b+sidecount,a+sidecount))
  mesh('Drawer%02d hollow cast cup pull'%(idx+1),vs,fs,brass)
  for dx in [-.059,.059]:pin('Cup handle cast fixing',(x+dx,y+.078,.216),.006,brass)
  # Brass label frame surrounds actual recessed parchment. No text geometry noise.
  cy=y+.151;outer=[(x-.053,cy-.017),(x+.053,cy-.017),(x+.053,cy+.017),(x-.053,cy+.017)];inner=[(x-.044,cy-.011),(x+.044,cy-.011),(x+.044,cy+.011),(x-.044,cy+.011)]
  vv=[(xx,yy,zz) for zz in [.217,.221] for poly in [outer,inner] for xx,yy in poly];ff=[]
  for i in range(4):j=(i+1)%4;ff += [(i,j,j+4,i+4),(i+8,i+12,j+12,j+8),(i,j,j+8,i+8),(i+4,i+12,j+12,j+4)]
  mesh('Drawer%02d label holder'%(idx+1),vv,ff,brass,0);extrude('Drawer%02d replaceable paper label'%(idx+1),inner,.216,.218,paper,.0004)
  for dx in [-.049,.049]:pin('Label holder pin',(x+dx,cy,.221),.0023,brass)
# Foliage: actual bent silhouette meshes on continuously curved branched stems.
group('06_TrailingVines')
leafcount=0
def living_leaf(n,a,b,width,variant=0,normal=(0,.05,1)):
 global leafcount
 a,b=Vector(a),Vector(b);up=(b-a).normalized();normal=Vector(normal).normalized();right=up.cross(normal)
 if right.length<.01:right=up.cross(Vector((1,0,0)))
 right.normalize();normal=right.cross(up).normalized();vs=[];uvs=[]
 # Texture stems are at top. Rows define actual heart silhouette, not a rectangular card.
 widths=[.08,.38,.52,.50,.38,.22,.035];N=len(widths)
 cx,cy=[(.0,.5),(.5,.5),(.0,0)][variant%3]
 for j,hw in enumerate(widths):
  t=j/(N-1)
  for k in range(3):
   u=(k-1)*hw;p=a.lerp(b,t)+right*u*width+normal*(.12*math.sin(math.pi*t)+(.06 if k==1 else 0))*width;vs.append(tuple(p));uvs.append((cx+.25+(k-1)*hw*.42,cy+.465-t*.43))
 fs=[(j*3+k,j*3+k+1,(j+1)*3+k+1,(j+1)*3+k) for j in range(N-1) for k in range(2)]
 o=mesh(n,vs,fs,leafmat);o['solid']=False
 for f in o.data.polygons:f.use_smooth=True
 for f in o.data.polygons:
  for li in f.loop_indices:o.data.uv_layers[0].data[li].uv=uvs[o.data.loops[li].vertex_index]
 leafcount+=1;return o

def vine(n,control,count,width=.115,phase=0,normal=(0,.05,1)):
 path=bez(control,60)
 # Upper runners rest on the authored crown, rather than bridging it like suspended wire.
 def crown_y(x):
  for (a,ya),(b,yb) in zip(crest,crest[1:]):
   if a<=x<=b:return ya+(yb-ya)*(x-a)/max(1e-6,b-a)
  return 1.947
 path=[(x,min(y,crown_y(x)+.010) if y>1.94 else y,z) for x,y,z in path]
 tube(n+' woody runner',path,.0035,stem,5)
 for j in range(count):
  t=(j+.4)/count;k=min(len(path)-2,int(t*(len(path)-1)));a=Vector(path[k]);side=-1 if j%2 else 1
  length=.105+.028*math.sin(j*1.7+phase);direction=Vector((side*(.65+.2*math.cos(j)), -.55,.12));b=a+direction*length
  tube(n+' petiole '+str(j),[a,a.lerp(b,.35)],.0013,stem,4)
  living_leaf(n+' leaf '+str(j),a.lerp(b,.25),b,width*(.85+.18*math.sin(j*2+phase)),(j+phase)%3,Vector(normal)+Vector((.32*math.sin(j*1.83+phase),.24*math.cos(j*1.37+phase),0)))
# Crown runners follow the actual moldings then spill asymmetrically; no woody gold ornament.
vine('Left crown to stile',[(.16,2.070,.195),(-.32,2.075,.192),(-.85,1.98,.213),(-.805,1.58,.215)],22,.123,1)
vine('Left full trailing stem',[(-.806,1.86,.210),(-.72,1.32,.240),(-.88,.79,.235),(-.83,.31,.215)],24,.119,3)
vine('Right crown cascade',[(.38,2.052,.19),(.86,2.01,.205),(.79,1.79,.232),(.84,1.40,.230)],16,.116,2)
vine('Right side descending',[(.83,1.50,.205),(.88,1.16,.205),(.79,.71,.225),(.85,.40,.22)],18,.107,4)
vine('Quiet crown second runner',[(-.62,1.979,-.09),(-.24,2.08,-.10),(.15,2.10,-.09),(.50,2.02,-.08)],13,.10,3,normal=(.1,1,1))
# Short branches create nonuniform clusters rather than one stamped ladder of leaves.
for i,(x,y,z,side) in enumerate([(-.78,1.68,.22,1),(-.79,1.04,.23,1),(.80,1.30,.23,-1),(.69,2.02,.18,-1),(-.50,2.06,.18,-1)]):
 vine('Secondary growing tip '+str(i),[(x,y,z),(x+side*.04,y+.02,z+.01),(x+side*.10,y-.04,z+.018),(x+side*.11,y-.13,z+.02)],5,.085,i)
# Moss: shallow curved irregular cutout cushions seated on humid crevices/edges, no cubes/balls.
group('07_Moss')
from mathutils.bvhtree import BVHTree
# Fit living moss to actual timber triangles. Reject roots falling off a ledge or inside a post.
woodverts=[];woodtris=[]
for ob in parts:
 if ob.get('logical_group','') not in ['01_MainStructure','02_Backing','03_Shelves','04_Drawers']:continue
 ob.data.calc_loop_triangles();base=len(woodverts);woodverts.extend(Vector((v.co.x,v.co.z,v.co.y)) for v in ob.data.vertices);woodtris.extend(tuple(base+i for i in t.vertices) for t in ob.data.loop_triangles)
woodbvh=BVHTree.FromPolygons(woodverts,woodtris,all_triangles=True)
def moss_patch(n,center,rx,ry,normal=(0,1,0),phase=0):
 c=Vector(center);nrm=Vector(normal).normalized();right=nrm.cross(Vector((0,0,1)))
 if right.length<.1:right=nrm.cross(Vector((1,0,0)))
 right.normalize();up=right.cross(nrm).normalized();vs=[];uv=[];fs=[];roots=0
 for j in range(38):
  a=j*2.399963+phase*.7;rad=math.sqrt((j+.5)/38);sample=c+right*math.cos(a)*rx*rad+up*math.sin(a)*ry*rad
  hit,no,face,dist=woodbvh.ray_cast(sample+nrm*.055,-nrm,.145)
  if hit is None or (-no).dot(nrm)<.30:continue
  roots+=1;root=hit+nrm*.0007
  for k in range(3):
   angle=a+k*2.1;height=.005+.006*(.5+.5*math.sin(j*1.9+k+phase));direction=right*math.cos(angle)+up*math.sin(angle);cross=nrm.cross(direction).normalized();width=.0018+.0007*math.cos(j+k);base=len(vs)
   for t in [0,.55,1.]:
    p=root+nrm*height*t+direction*height*t*t*.65;w=width*(1-t*.8)
    for side in [-1,1]:vs.append(tuple(p+cross*side*w));uv.append((.75+side*.016+.018*math.sin(j+phase),.25+t*.055+.014*math.cos(j*2)))
   fs.extend([(base,base+1,base+3,base+2),(base+2,base+3,base+5,base+4)])
 if not fs:return
 o=mesh(n+' - surface rooted moss tufts',vs,fs,mossmat);o['solid']=False;o['surface_roots']=roots
 for f in o.data.polygons:
  for li in f.loop_indices:o.data.uv_layers[0].data[li].uv=uv[o.data.loops[li].vertex_index]
for i,(x,y,z,rx,rz) in enumerate([(-.81,.083,.17,.074,.042),(.81,.083,.17,.066,.05),(-.53,.188,.205,.080,.016),(.37,.731,.16,.075,.03),(-.68,1.124,.15,.056,.034),(.72,1.517,.15,.052,.03),(-.70,1.98,.11,.082,.035),(.57,2.007,.10,.087,.04),(-.83,.665,.14,.07,.04)]):moss_patch('Seated moss cushion '+str(i),(x,y,z),rx,rz,phase=i)
# Small vertical tongues follow side/post cracks, intentionally sparse.
for i,(x,y) in enumerate([(-.85,.18),(-.855,.65),(.85,.58),(.84,1.88)]):moss_patch('Moss in timber seam '+str(i),(x,y,.202),.020,.055,(0,0,1),i)
# One detachable planter: hollow hand-shaped ceramic with an actual rope suspension.
group('08_HangingPlanter')
px=-.715;pz=.355;py=1.26;N=28;profile=[(0,.064),(.014,.078),(.04,.094),(.105,.108),(.13,.105),(.139,.113),(.153,.114),(.158,.102),(.14,.095),(.038,.067)]
vs=[]
for y,r in profile:
 for j in range(N):
  a=j*math.tau/N;rr=r*(1+.012*math.sin(j*.7));vs.append((px+math.cos(a)*rr,py+y,pz+math.sin(a)*rr))
fs=[tuple(reversed(range(N))),tuple(range((len(profile)-1)*N,len(profile)*N))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j) for k in range(len(profile)-1) for j in range(N)]
o=mesh('Hollow sage hanging ceramic planter',vs,fs,ceramic);uv=o.data.uv_layers[0]
for f in o.data.polygons:
 for li in f.loop_indices:
  idx=o.data.loops[li].vertex_index;k,j=divmod(idx,N)
  if abs(f.normal.z)>.8:
   p=o.data.vertices[idx].co;uv.data[li].uv=(.75+(p.x-px)*1.5,.75+(p.y-pz)*1.5)
  else:
   js=[o.data.loops[l].vertex_index%N for l in f.loop_indices];jj=N if j==0 and max(js)-min(js)>N/2 else j;uv.data[li].uv=(.54+jj/N*.40,.54+k/(len(profile)-1)*.40)
# Soil sits below rim, with roots hidden inside the pot.
slab('Planter recessed soil',[(px+math.cos(j*math.tau/24)*.091,pz+math.sin(j*math.tau/24)*.091) for j in range(24)],py+.125,py+.130,soil,0)
# Metal mounting eye and top knot physically attach to crown underside.
tube('Forged planter hook',bez([(-.735,1.92,.18),(-.735,1.91,.28),(-.730,1.87,.37),(-.715,1.85,.355)],20),.005,iron,8)
tube('Rope top binding',[(px+.009*math.cos(t),1.84+.009*math.sin(t),pz) for t in [j*math.tau/24 for j in range(25)]],.004,rope,6)
for j in range(4):
 a=j*math.tau/4+.4;bx=px+math.cos(a)*.109;bz=pz+math.sin(a)*.109
 tube('Planter rope sling '+str(j),[(px,1.84,pz),(px+math.cos(a)*.045,1.70,pz+math.sin(a)*.045),(bx,py+.15,bz),(px+math.cos(a)*.072,py+.007,pz+math.sin(a)*.072),(px,py-.017,pz)],.0036,rope,6)
# Short knotted cross bindings around the real basket/pot belly.
for yy,r in [(py+.12,.111),(py+.035,.09)]:tube('Circumferential rope binding',[(px+math.cos(t)*r,yy,pz+math.sin(t)*r) for t in [j*math.tau/32 for j in range(33)]],.0035,rope,6)
for j in range(3):
 a=j*2.1;vine('Planter living trailing stem '+str(j),[(px,py+.13,pz),(px+math.sin(a)*.13,py+.23,pz+.04),(px+math.sin(a)*.17,py+.04,pz+.10),(px+math.sin(a)*.15,py-.18-j*.035,pz+.12)],7,.078,j)
# Concept-fit: wider reading by reducing only the open-case height, retaining practical drawers.
# Source front is Blender +Y: its reference-left is native +X when viewed head-on.
for o in parts:
 for v in o.data.vertices:
  v.co.x=-v.co.x
  if v.co.z>.726:v.co.z=.726+(v.co.z-.726)*.90
 finishmesh(o)
for o in s.objects:
 if o.type!='MESH' or not o.name.startswith('Circumferential rope binding'):continue
 me=o.data;vv=[v.co for v in me.vertices];cx=sum(v.x for v in vv)/len(vv);cy=sum(v.y for v in vv)/len(vv);cz=sum(v.z for v in vv)/len(vv);rad=lambda v:math.hypot(v.x-cx,v.y-cy);rr=sum(rad(v) for v in vv)/len(vv)
 for f in me.polygons:
  values=[]
  for li in f.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;values.append([li,math.atan2(v.y-cy,v.x-cx)/math.tau+.5,math.atan2((v.z-cz)/.90,rad(v)-rr)/math.tau+.5])
  for axis in [1,2]:
   if max(v[axis] for v in values)-min(v[axis] for v in values)>.5:
    for v in values:
     if v[axis]<.5:v[axis]+=1
  for li,u,v in values:me.uv_layers[0].data[li].uv=(.01+.48*u,.01+.48*v)

# Hero drawer faces receive denser, individually offset paint islands; side/end grain keeps its own mapping.
for o in parts:
 if 'shaped solid front' not in o.name:continue
 idx=int(o.name[6:8])-1;lo=Vector((min(v.co.x for v in o.data.vertices),min(v.co.y for v in o.data.vertices),min(v.co.z for v in o.data.vertices)))
 for f in o.data.polygons:
  if f.normal.y<.5:continue
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers[0].data[li].uv=(.536+(idx%2)*.09+(v.x-lo.x)*.8,.548+idx*.022+(v.z-lo.z)*.8)
# Save native source with all meaningful components separate. A single floor-level root is export pivot.
root=bpy.data.objects.new('CM_MasterMedicineCabinet01',None);s.collection.objects.link(root)
for o in parts:o.parent=root
for name,pos in {'PlanterMount':(-.735,1.92,.18),'FloorPivot':(0,0,0),'ShelfLower':(0,.726,0),'ShelfMiddle':(0,1.119,0),'ShelfUpper':(0,1.512,0),'WallAnchorL':(-.72,1.85,-.225),'WallAnchorR':(.72,1.85,-.225)}.items():
 o=bpy.data.objects.new('Attach_'+name,None);s.collection.objects.link(o);o.parent=root;x,y,z=pos;o.location=P((-x,.726+(y-.726)*.90 if y>.726 else y,z));o.empty_display_type='ARROWS';o.empty_display_size=.06
# Native material edits remain fully editable. No geometry/normal displacements from noisy textures.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'))
report=[]
for name,c in groups.items():
 os=[o for o in c.objects if o.type=='MESH'];tri=0
 for o in os:o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles)
 report.append({'group':name,'objects':len(os),'triangles':tri,'materials':sorted({m.name for o in os for m in o.data.materials})})
pts=[tuple((v.co.x,v.co.z,v.co.y)) for o in parts for v in o.data.vertices];bounds={'min':[min(p[i] for p in pts) for i in range(3)],'max':[max(p[i] for p in pts) for i in range(3)]}
(D/'AssetCatalog.json').write_text(json.dumps({'name':root.name,'groups':report,'triangles':sum(r['triangles'] for r in report),'boundsUnity':bounds,'leafCount':leafcount,'coreTargetMetres':[1.8,1.93,.45],'materials':list(mats),'shelfTopY':[.726,1.0797,1.4334],'drawers':8},indent=2))
# FBX transport copies: combine sensible groups; eight drawers remain separate modules in source/GLB.
exports=[]
for name,c in groups.items():
 bpy.ops.object.select_all(action='DESELECT');copies=[]
 for o in c.objects:
  if o.type!='MESH':continue
  p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.parent=None;p.matrix_world=Matrix.Identity(4);p.select_set(True);copies.append(p)
 bpy.context.view_layer.objects.active=copies[0]
 if len(copies)>1:bpy.ops.object.join()
 g=bpy.context.object;g.name='CM_MMC01_'+name[3:];s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');exports.append(g)
bpy.ops.object.select_all(action='DESELECT')
for g in exports:g.select_set(True)
bpy.context.view_layer.objects.active=exports[0]
for g in exports:
 bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.object.select_all(action='DESELECT')
for g in exports:g.select_set(True)
bpy.context.view_layer.objects.active=exports[0]
bpy.ops.export_scene.gltf(filepath=str(E/'CM_MasterMedicineCabinet01.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_materials='EXPORT')
bpy.ops.export_scene.fbx(filepath=str(E/'CM_MasterMedicineCabinet01.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='RELATIVE')
print('MASTER_CABINET_READY',sum(r['triangles'] for r in report),bounds)
