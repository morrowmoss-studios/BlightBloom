"""Reference/stencil-led hero counter. Bespoke Bezier profiles + continuous sculpt fields + unique paint.
Scripts are transport/authoring tools; this intentionally does NOT reuse the previous furniture recipe.
"""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow08';(A/'Models').mkdir(exist_ok=True);(A/'Prefabs').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]))
def mat(n,tex=None,color=(.32,.17,.08,1)):
 m=bpy.data.materials.new(n);m.diffuse_color=color;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.88
 if tex:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(A/'Textures'/tex));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=mat('CM_CW08_Walnut','CM_CW08_Walnut.png');carved=wood;iron=mat('CM_CW08_Iron',color=(.13,.15,.12,1));parts=[];highs=[]
def smooth(me):
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
 me.set_sharp_from_angle(angle=math.radians(45))
def grain(o):
 me=o.data;uv=me.uv_layers.new(name='PaintUV');lo=[min(v.co[i] for v in me.vertices) for i in range(3)];hi=[max(v.co[i] for v in me.vertices) for i in range(3)];dim=[hi[i]-lo[i] for i in range(3)];along=max(range(3),key=lambda i:dim[i])
 for f in me.polygons:
  normal=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=normal];vaxis=along if along in axes else max(axes,key=lambda i:dim[i]);uaxis=next(i for i in axes if i!=vaxis)
  for li in f.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(.13+(co[uaxis]-lo[uaxis])/.8,.08+(co[vaxis]-lo[vaxis])/2.5)
def mesh(n,vs,fs,m=wood,bevel=0,register=True):
 me=bpy.data.meshes.new(n);me.from_pydata([P(v) for v in vs],[],fs);me.update();o=bpy.data.objects.new(n,me);s.collection.objects.link(o);me.materials.append(m);bpy.context.view_layer.objects.active=o;smooth(me)
 if bevel:
  mod=o.modifiers.new('Crafted arris','BEVEL');mod.width=bevel;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name);smooth(o.data)
 grain(o)
 if register:parts.append(o)
 return o
def bez(points,N=30):
 a,b,c,d=[Vector(p) for p in points];return [tuple((1-t)**3*a+3*(1-t)**2*t*b+3*(1-t)*t*t*c+t**3*d) for t in [j/N for j in range(N+1)]]
def extrude(n,poly,z0,z1,m=wood,b=.005):
 N=len(poly);return mesh(n,[(x,y,z) for z in [z0,z1] for x,y in poly],[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],m,b)
def slab(n,poly,y0,y1,b=.005):
 N=len(poly);return mesh(n,[(x,y,z) for y in [y0,y1] for x,z in poly],[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],wood,b)
def profile_sweep(n,path,profile):
 vs=[];N=len(profile)
 for j,(x,y,z) in enumerate(path):
  a=path[max(0,j-1)];b=path[min(len(path)-1,j+1)];dx=b[0]-a[0];dy=b[1]-a[1];ll=math.hypot(dx,dy)
  for u,v in profile:vs.append((x-dy/ll*u,y+dx/ll*u,z+v))
 fs=[tuple(reversed(range(N))),tuple(range((len(path)-1)*N,len(path)*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(path)-1) for i in range(N)]
 return mesh(n,vs,fs)
ogee=[(-.040,-.020),(-.040,.012),(-.033,.024),(-.018,.028),(-.010,.017),(.004,.011),(.020,.027),(.033,.033),(.041,.020),(.041,-.020)]
# WF08: shaped frame-and-panel cabinet on four structural scroll-foot standards.
# A flat usable worktop stays within the same 2.28 x .78 m working envelope.
def frontz(x):return .286+.052*math.cos(math.pi*x/1.04)+.012*math.cos(3*math.pi*x/1.04)
def bottom(x):return .245+.082*math.sin(math.pi*abs(x)/1.0)**2-.025*math.exp(-(x/.29)**2)
def upper(x):return .905+.034*math.cos(math.pi*x/1.04)
def rail(n,fun,depth=.025,height=.045):
 path=[(x,fun(x),frontz(x)) for x in np.linspace(-1.01,1.01,85)]
 return profile_sweep(n,path,[(-height,-depth),(-height,.008),(-height*.7,.024),(0,.029),(height*.65,.022),(height,.008),(height,-depth)])
# Rounded lobes at the end-grain breadboard shoulders: no box-shaped top.
outline=[]
for j in range(128):
 t=2*math.pi*j/128;c=math.cos(t);q=math.sin(t)
 x=1.14*math.copysign(abs(c)**.32,c);z=.39*math.copysign(abs(q)**.50,q)
 if z>0:z-=.045*(math.sin(math.pi*x/1.14)**2)
 outline.append((x,z))
# Ogee edge is a genuine changing section, top remains planar.
vs=[];nr=len(outline)
for y,sx,sz in [( .958,.975,.94),(.973,.986,.96),(.989,1,1),(1.031,1,1),(1.0525,.994,.984)]:
 vs += [(x*sx,y,z*sz) for x,z in outline]
fs=[tuple(reversed(range(nr))),tuple(range(4*nr,5*nr))]+[(j*nr+i,j*nr+(i+1)%nr,(j+1)*nr+(i+1)%nr,(j+1)*nr+i) for j in range(4) for i in range(nr)]
mesh('Shaped breadboard worktop - flat service datum',vs,fs,bevel=.002)
# Sweeping apron, a scalloped underside and inset cavity replace long straight horizontal strips.
rail('Upper load-bearing ogee apron',upper,.038,.048)
rail('Scalloped lower bearing rail',bottom,.031,.035)
# Four continuous sculpted supports: broad bearing shoulder, inward waist, outward foot.
def leg(side,back=False):
 N=24;vs=[];rows=48
 control=[(0,.99,.245,.095,.075),(.10,1.015,.25,.10,.08),(.19,.997,.248,.072,.064),(.36,.928,.23,.047,.047),(.57,.916,.232,.053,.054),(.76,.968,.256,.091,.077),(.86,.996,.264,.103,.082),(.966,.995,.26,.077,.075)]
 # Smooth cubic interpolation between authored cross-sections; no random wiggle.
 def interp(y):
  for k in range(len(control)-1):
   if y<=control[k+1][0]:break
  a=control[k];b=control[k+1];t=(y-a[0])/(b[0]-a[0]);t=t*t*(3-2*t)
  return [a[i]+(b[i]-a[i])*t for i in range(1,5)]
 for y in np.linspace(0,.966,rows):
  x,z,rx,rz=interp(y)
  if back:z=-z
  for j in range(N):
   t=j*2*math.pi/N;cs=math.cos(t);sn=math.sin(t)
   vs.append((side*(x+rx*math.copysign(abs(cs)**.62,cs)),y,z+rz*math.copysign(abs(sn)**.62,sn)))
 fs=[tuple(reversed(range(N))),tuple(range((rows-1)*N,rows*N))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(rows-1) for i in range(N)]
 o=mesh(('Rear' if back else 'Front')+' swept shouldered standard '+str(side),vs,fs)
 # Parametric timber grain follows the member along its curved length, not world axes.
 uv=o.data.uv_layers[0]
 for f in o.data.polygons:
  for li in f.loop_indices:
   vi=o.data.loops[li].vertex_index;j,i=divmod(vi,N);uv.data[li].uv=(.18+i/N*.38,.05+j/(rows-1)*.76)
for side in [-1,1]:
 leg(side);leg(side,True)
# Front field assembled as shaped timber boards with a calm central carving.
H=np.load(D.parent/'CounterWorkflow07/SculptFields.npy')[1];N=H.shape[0]
# One continuous field spans between supporting stiles. Curvature under ornament is shared.
def facepoint(x,v):
 lo=bottom(x)+.018;hi=upper(x)-.024;y=lo+v*(hi-lo)
 z=frontz(x)-.020+.010*math.sin(math.pi*v)
 return y,z
# Side fields are intentionally free from dense botanical imagery, gently convex and recessed.
for side in [-1,1]:
 nx=42;ny=42;vs=[]
 for j in range(ny):
  v=j/(ny-1)
  for i in range(nx):
   x=side*(.37+.56*i/(nx-1));y,z=facepoint(x,v);vs.append((x,y,z-.009+ .010*math.sin(math.pi*i/(nx-1))*math.sin(math.pi*v)))
 fs=[(j*nx+i,j*nx+i+1,(j+1)*nx+i+1,(j+1)*nx+i) for j in range(ny-1) for i in range(nx-1)]
 o=mesh('Quiet shaped side field '+str(side),vs,fs);bpy.context.view_layer.objects.active=o;sol=o.modifiers.new('Solid hardwood field','SOLIDIFY');sol.thickness=.022;bpy.ops.object.modifier_apply(modifier=sol.name)
# Integrated central relief board: silhouette follows curved frame; no separately painted motif.
vs=[];flatvs=[]
for j in range(N):
 v=j/(N-1)
 for i in range(N):
  u=i/(N-1);x=(u-.5)*.70;y,z=facepoint(x,v)
  # relief softens before it reaches joinery; center remains a warm, readable modest motif
  h=float(H[N-1-j,i])*.94
  vs.append((x,y,z+h));flatvs.append((x,y,z))
fs=[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i) for j in range(N-1) for i in range(N-1)]
hi=mesh('Editable integrated mortar field - dense sculpt',vs,fs,wood,register=False);highs.append(hi)
# Continuous one-piece UVs across the whole sculpture. Exact correspondence removes projection seams.
uv=hi.data.uv_layers[0]
for f in hi.data.polygons:
 for li in f.loop_indices:
  vi=hi.data.loops[li].vertex_index;j,i=divmod(vi,N);uv.data[li].uv=(i/(N-1),j/(N-1))
attr=hi.data.color_attributes.new(name='SculptPaintValues',type='FLOAT_COLOR',domain='POINT')
for vi in range(len(vs)):
 j,i=divmod(vi,N);value=min(1,float(H[N-1-j,i])/.028)
 # Intentional illustrated value grouping, registered to real sculpt height, no random texture/noise.
 attr.data[vi].color=(.86+.62*value,.84+.53*value,.82+.43*value,1)
bakeMat=bpy.data.materials.new('Registered sculpt painting');bakeMat.use_nodes=True;nodes=bakeMat.node_tree.nodes;nodes.clear();links=bakeMat.node_tree.links
out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(A/'Textures/CM_CW08_Walnut.png'));tex.image.pack();att=nodes.new('ShaderNodeVertexColor');att.layer_name='SculptPaintValues';mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
quiet=nodes.new('ShaderNodeMixRGB');quiet.blend_type='MIX';quiet.inputs[0].default_value=.55;quiet.inputs[2].default_value=(.16,.081,.037,1);links.new(tex.outputs['Color'],quiet.inputs[1]);links.new(quiet.outputs[0],mix.inputs[1]);links.new(att.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],em.inputs['Color']);links.new(em.outputs[0],out.inputs['Surface'])
baked=bpy.data.images.new('CM_CW08_CarvedWalnut',1536,1536,alpha=False);target=nodes.new('ShaderNodeTexImage');target.image=baked;nodes.active=target;hi.data.materials.clear();hi.data.materials.append(bakeMat)
bpy.ops.object.select_all(action='DESELECT');hi.select_set(True);bpy.context.view_layer.objects.active=hi;s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.device='CPU';bpy.ops.object.bake(type='EMIT',margin=8)
baked.filepath_raw=str(A/'Textures/CM_CW08_CarvedWalnut.png');baked.file_format='PNG';baked.save();baked.pack()
carved=mat('CM_CW08_CarvedWalnut','CM_CW08_CarvedWalnut.png');hi.data.materials.clear();hi.data.materials.append(carved)
low=hi.copy();low.data=hi.data.copy();s.collection.objects.link(low);low.name='Integrated mortar board';bpy.context.view_layer.objects.active=low
mod=low.modifiers.new('Curvature-preserving sculpt reduction','DECIMATE');mod.ratio=.085;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
# Close only the border and one flat rear cap, avoiding a redundant dense sculpture on the back.
bm=bmesh.new();bm.from_mesh(low.data);edges=[e for e in bm.edges if e.is_boundary];border=set(v for e in edges for v in e.verts);copies={v:bm.verts.new((v.co.x,.270,v.co.z)) for v in border};adj={v:[] for v in border}
for e in edges:
 a,b=e.verts;adj[a].append(b);adj[b].append(a);bm.faces.new((a,b,copies[b],copies[a]))
order=[next(iter(border))];prev=None
while True:
 nxt=next((v for v in adj[order[-1]] if v is not prev),None)
 if nxt is None or nxt is order[0]:break
 prev=order[-1];order.append(nxt)
bm.faces.new([copies[v] for v in reversed(order)]);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(low.data);bm.free();smooth(low.data);parts.append(low)
# A plain board replacement is exported only for a relief-free silhouette comparison.
plain=mesh('Plain board for form-only review',flatvs,fs,wood,register=False);bpy.context.view_layer.objects.active=plain
mod=plain.modifiers.new('Plain field simplification','DECIMATE');mod.ratio=.004;bpy.ops.object.modifier_apply(modifier=mod.name)
sol=plain.modifiers.new('Solid board','SOLIDIFY');sol.thickness=.012;bpy.ops.object.modifier_apply(modifier=sol.name)
# Shaped vertical structural mullions tie directly into the top and lower rails.
for side in [-1,1]:
 path=[]
 for v in np.linspace(0,1,40):
  x=side*(.356+.015*math.sin(v*math.pi));y,z=facepoint(x,v);path.append((x,y,z+.014))
 profile_sweep('Sinuous joined central stile',path,[(-.019,-.021),(-.023,.002),(-.015,.016),(0,.020),(.015,.016),(.023,.002),(.019,-.021)])
 # Left/right side walls are bowed inward at waist and fully join front/back shoulders.
 vs=[];nx=25;ny=30
 for j in range(ny):
  v=j/(ny-1);y=.29+v*.61
  for i in range(nx):
   u=i/(nx-1);z=-.255+.51*u;x=side*(.972-.045*math.sin(math.pi*v)-.024*math.sin(math.pi*u));vs.append((x,y,z))
 fs=[(j*nx+i,j*nx+i+1,(j+1)*nx+i+1,(j+1)*nx+i) for j in range(ny-1) for i in range(nx-1)]
 o=mesh('Recessed curved end field '+str(side),vs,fs);bpy.context.view_layer.objects.active=o;sol=o.modifiers.new('End field thickness','SOLIDIFY');sol.thickness=.025;bpy.ops.object.modifier_apply(modifier=sol.name)
 # Rounded continuous side apron, and lower arch with visible negative space beneath.
 for base in [False,True]:
  path=[]
  for z in np.linspace(-.26,.27,35):
   v=(z+.26)/.53;y=(.27+.072*math.sin(math.pi*v)) if base else (.921+.02*math.sin(math.pi*v));path.append((side*.98,y,z))
  # use a solid section loft in side YZ plane
  vs=[(side*(.98+dx),y+dy,z) for x,y,z in path for dx,dy in [(-.028,-.027),(.030,-.027),(.038,.0),(.030,.027),(-.028,.027)]];n=5
  fs=[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(path)-1) for i in range(n)]
  mesh('Side arched bearing rail',vs,fs)
slab('Inset load-bearing cupboard bottom',[(-.93,-.235),(.93,-.235)]+[(float(x),frontz(float(x))-.055) for x in np.linspace(.93,-.93,49)],.372,.395,.004)
# Service side keeps enclosed storage, inset doors/drawers and the existing functional volume.
extrude('Service back structure',[(-.94,.27),(.94,.27),(.94,.93),(-.94,.93)],-.27,-.235,b=.008)
for y in [.49,.76]:
 for x in [-.62,0,.62]:
  p=[(x-.284,y-.103),(x+.284,y-.103),(x+.294,y-.075),(x+.284,y+.084),(x+.24,y+.11),(x-.24,y+.11),(x-.284,y+.084)]
  extrude('Inset storage drawer',p,-.300,-.265,b=.009)
  path=[(x+.05*math.cos(t),y-.01+.028*math.sin(t),-.321) for t in np.linspace(math.pi,2*math.pi,20)]
  cu=bpy.data.curves.new('Forged iron bail','CURVE');cu.dimensions='3D';cu.bevel_depth=.005;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(path)-1)
  for p,co in zip(sp.points,path):p.co=(*P(co),1)
  ob=bpy.data.objects.new('Forged drawer bail',cu);s.collection.objects.link(ob);cu.materials.append(iron);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob=bpy.context.object
  for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
  grain(ob);parts.append(ob)
# Editable source retains logical construction, no destructive joining of originals.
source=bpy.data.collections.new('Editable shaped joinery');s.collection.children.link(source)
for o in parts:
 for c in list(o.users_collection):c.objects.unlink(o)
 source.objects.link(o)
def joined_copy(items,name):
 copies=[];bpy.ops.object.select_all(action='DESELECT')
 for o in items:
  p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.select_set(True);copies.append(p)
 bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();g=bpy.context.object;g.name=name;g.data.name=name+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');smooth(g.data);return g
game=joined_copy(parts,'CM_CW08_HeroCounter');form=joined_copy([p for p in parts if p!=low]+[plain],'CM_CW08_FormOnly')
for o in parts+highs+[plain,form]:o.hide_render=True;o.hide_set(True)
game.data.calc_loop_triangles();report={'name':game.name,'triangles':len(game.data.loop_triangles),'vertices':len(game.data.vertices),'materials':[m.name for m in game.data.materials],'workSurfaceMetres':1.0525,'footprintMetres':[2.28,.78],'axes':'Unity +Y up +Z front','method':'Authored continuous lofts, scalloped structural rails, serpentine ogee worktop, quiet bowed infills, integrated central relief on shared curved substrate. Directional UVs and dedicated painted walnut; no mismatched printed carving overlay.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CounterWorkflow08.blend'))
for g in [game,form]:
 g.hide_set(False);bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{g.name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetReport.json').write_text(json.dumps(report,indent=2));print('COUNTER08_READY',report)
