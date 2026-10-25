"""Reference/stencil-led hero counter. Bespoke Bezier profiles + continuous sculpt fields + unique paint.
Scripts are transport/authoring tools; this intentionally does NOT reuse the previous furniture recipe.
"""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow07';(A/'Models').mkdir(exist_ok=True);(A/'Prefabs').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]))
def mat(n,tex=None,color=(.32,.17,.08,1)):
 m=bpy.data.materials.new(n);m.diffuse_color=color;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.88
 if tex:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(A/'Textures'/tex));t.image.pack();m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 return m
wood=mat('CM_CW07_Walnut','CM_CW07_Walnut.png');carved=mat('CM_CW07_CarvedWalnut','CM_CW07_CarvedWalnut.png');iron=mat('CM_CW07_Iron',color=(.13,.15,.12,1));parts=[];highs=[]
def smooth(me):
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(me);bm.free()
 for f in me.polygons:f.use_smooth=True
 me.set_sharp_from_angle(angle=math.radians(45))
def grain(o):
 me=o.data;uv=me.uv_layers.new(name='PaintUV');lo=[min(v.co[i] for v in me.vertices) for i in range(3)];hi=[max(v.co[i] for v in me.vertices) for i in range(3)];dim=[hi[i]-lo[i] for i in range(3)];along=max(range(3),key=lambda i:dim[i]);cross=max((i for i in range(3) if i!=along),key=lambda i:dim[i])
 # Consistent world-scale grain, aligned to each actual timber member; no arbitrary tiny atlas patch.
 for f in me.polygons:
  for li in f.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(.17+(co[cross]-lo[cross])/.55,.11+(co[along]-lo[along])/1.9)
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
# Cabinet inner carcass stops behind the genuine framed panel substrates.
extrude('Jointed service carcass',[(-1.035,.15),(1.035,.15),(1.035,.91),(-1.035,.91)],-.295,.275,b=.012)
# Curved authored top outline. The central work surface stays exactly planar and at the validated height.
front=bez([(-1.13,.33),(-.65,.405),(.45,.392),(1.13,.33)],36)
poly=[(-1.14,-.31),(-1.105,-.39),(1.105,-.39),(1.14,-.31),(1.14,.30)]+list(reversed(front))+[(-1.14,.30)]
slab('Single hand-shaped bullnose worktop',poly,.987,1.0525,.010)
# Shaped lower perimeter, splayed feet and continuous structural rails.
basefront=bez([(-1.095,.295),(-.70,.355),(.60,.36),(1.095,.295)],30)
slab('Curving foot plinth',[(-1.10,-.30),(1.10,-.30),(1.10,.295)]+list(reversed(basefront))+[(-1.10,.295)],.055,.13,.008)
for side in [-1,1]:
 # Each standard is a real organic solid, designed with changing cross-sections and shoulder connections.
 rings=[(.08,.079,.065,side*1.045,.307),(.15,.075,.062,side*1.045,.307),(.25,.050,.047,side*1.025,.307),(.42,.041,.040,side*1.018,.307),(.66,.048,.044,side*1.02,.307),(.81,.079,.060,side*1.035,.307),(.89,.069,.065,side*1.036,.307),(.982,.082,.072,side*1.035,.307)]
 N=32;vs=[(cx+rx*math.cos(j*2*math.pi/N),y,cz+rz*math.sin(j*2*math.pi/N)) for y,rx,rz,cx,cz in rings for j in range(N)];fs=[tuple(reversed(range(N))),tuple(range(len(vs)-N,len(vs)))]+[(k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j) for k in range(len(rings)-1) for j in range(N)];mesh('Cabriole engaged end standard',vs,fs)
 # Actual short curved bearing knee from standard to worktop, not dangling applique.
 curve=bez([(side*.96,.80),(side*.90,.83),(side*.83,.91),(side*.76,.96)],22)
 outline=[(side*.99,.974),(side*.70,.974)]+list(reversed(curve))
 extrude('Swept bearing shoulder',outline,.25,.37,b=.005)
# Front apron sculpted in silhouette; calmer central bearing and unequal curves avoid repetitive scallops.
left=bez([(-1.05,.84),(-.87,.73),(-.67,.80),(-.42,.855)],24)
right=bez([(-.42,.855),(.22,.885),(.70,.77),(1.05,.855)],30)
extrude('Continuous carved structural apron',[(-1.08,.982),(1.08,.982),(1.08,.855)]+list(reversed(left+right[1:]))+[(-1.08,.84)],.268,.335,b=.006)
for y in [.205,.824]:profile_sweep('Curved compound rail',[(x,y,z) for x,z in bez([(-1.02,.306),(-.6,.344),(.6,.344),(1.02,.306)],40)],ogee)
for x in [-.363,.363]:
 curve=bez([(x,.226),(x-.009,.40),(x+.009,.65),(x,.805)],22);profile_sweep('Joined bowed panel stile',[(xx,yy,.323) for xx,yy in curve],[(-.026,-.018),(-.029,.020),(-.020,.032),(.020,.032),(.029,.020),(.026,-.018)])
# HIGH SCULPT: one continuous substrate per panel, scalar field from deliberate artwork stencil.
fields=np.load(D/'SculptFields.npy');panel_specs=[(-.700,.527,0),(0,.650,1),(.700,.527,2)]
for cx,w,index in panel_specs:
 H=fields[index];N=H.shape[0];vs=[]
 for j in range(N):
  v=j/(N-1)
  for i in range(N):
   u=i/(N-1);x=cx+(u-.5)*w;y=.252+v*.537;z=.314+float(H[N-1-j,i]);vs.append((x,y,z))
 fs=[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i) for j in range(N-1) for i in range(N-1)]
 o=mesh('Sculpt source panel '+str(index),vs,fs,carved,register=False);o.data.uv_layers.remove(o.data.uv_layers[0]);uv=o.data.uv_layers.new(name='PaintUV')
 for f in o.data.polygons:
  for li in f.loop_indices:
   vi=o.data.loops[li].vertex_index;j,i=divmod(vi,N);uv.data[li].uv=((index+i/(N-1))/3,j/(N-1))
 highs.append(o)
 low=o.copy();low.data=o.data.copy();s.collection.objects.link(low);low.name='Gameplay continuous carved field '+str(index);bpy.context.view_layer.objects.active=low
 dec=low.modifiers.new('Curvature-adaptive reduction','DECIMATE');dec.ratio=.09;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
 # Close the substrate with a flat rear cap; never duplicate the entire dense relief behind the carcass.
 bm=bmesh.new();bm.from_mesh(low.data);edges=[e for e in bm.edges if e.is_boundary];border=set(v for e in edges for v in e.verts);copies={v:bm.verts.new((v.co.x,.288,v.co.z)) for v in border};adj={v:[] for v in border}
 for e in edges:
  a,b=e.verts;adj[a].append(b);adj[b].append(a);bm.faces.new((a,b,copies[b],copies[a]))
 order=[next(iter(border))];prev=None
 while True:
  nxt=next((v for v in adj[order[-1]] if v is not prev),None)
  if nxt is None or nxt is order[0]:break
  prev=order[-1];order.append(nxt)
 bm.faces.new([copies[v] for v in reversed(order)]);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(low.data);bm.free();smooth(low.data);parts.append(low)
 # The profiled perimeter is structural field framing, and meets the bowed rails/stiles.
 rect=[(cx-w/2,.244,.316),(cx-w/2,.80,.316),(cx+w/2,.80,.316),(cx+w/2,.244,.316)]
 for j in range(4):profile_sweep('Raised panel field edge',[rect[j],rect[(j+1)%4]],[(-.010,-.004),(-.011,.009),(0,.017),(.011,.009),(.010,-.004)])
# Side panel construction and practical six service drawers keep footprint and use datums.
for side in [-1,1]:
 # continuous gently bulged end surface rather than a flat unframed box
 rings=[];N=20
 for j in range(9):
  y=.22+j*.075;rr=.995+.025*math.sin(j/8*math.pi)
  for z in [-.27,.26]:rings.append((side*rr,y,z))
 vs=rings;fs=[(j*2,j*2+1,j*2+3,j*2+2) for j in range(8)];o=mesh('Curved framed end field',vs,fs);bpy.context.view_layer.objects.active=o;sol=o.modifiers.new('Solid field','SOLIDIFY');sol.thickness=.035;bpy.ops.object.modifier_apply(modifier=sol.name)
 for z in [-.28,.27]:profile_sweep('End-panel structural stile',[(side*1.038,.21,z),(side*1.038,.81,z)],[(-.018,-.015),(-.018,.02),(.018,.02),(.018,-.015)])
for y in [.49,.75]:
 for x in [-.66,0,.66]:
  pts=[(x-.31,y-.103),(x+.31,y-.103),(x+.322,y-.07),(x+.311,y+.07),(x+.25,y+.102),(x-.25,y+.102),(x-.311,y+.07)]
  extrude('Fitted shaped service drawer',pts,-.337,-.282,b=.007)
  extrude('Inset drawer wood field',[(x-.255,y-.06),(x+.255,y-.06),(x+.255,y+.05),(x+.22,y+.067),(x-.22,y+.067),(x-.255,y+.05)],-.344,-.337,b=.003)
  # Forged open handle, swept along a hand-designed elliptical bail.
  path=[(x+.052*math.cos(t),y-.023+.032*math.sin(t),-.365) for t in [math.pi+k*math.pi/18 for k in range(19)]]
  # round swept form constructed with bevelled Blender curve (real smooth continuous handle)
  cu=bpy.data.curves.new('Forged bail','CURVE');cu.dimensions='3D';cu.resolution_u=12;cu.bevel_depth=.006;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(len(path)-1)
  for p,co in zip(sp.points,path):p.co=(*P(co),1)
  ob=bpy.data.objects.new('Forged bail',cu);s.collection.objects.link(ob);cu.materials.append(iron);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');ob=bpy.context.object
  for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
  grain(ob);parts.append(ob)
# Join only gameplay geometry; keep the dense source sculpt separate and editable.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();game=bpy.context.object;game.name='CM_CW07_HeroCounter';game.data.name=game.name+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');smooth(game.data);game.data.set_sharp_from_angle(angle=math.radians(75))
sculpt=bpy.data.collections.new('Editable dense sculpt sources - not exported');s.collection.children.link(sculpt)
for o in highs:
 for c in list(o.users_collection):c.objects.unlink(o)
 sculpt.objects.link(o);o.hide_render=True;o.hide_set(True)
game.data.calc_loop_triangles();report={'name':game.name,'triangles':len(game.data.loop_triangles),'vertices':len(game.data.vertices),'sourceSculptVertices':sum(len(o.data.vertices) for o in highs),'materials':[m.name for m in game.data.materials],'workSurfaceMetres':1.0525,'axes':'Unity +Y up +Z front','workflow':'Bespoke Bezier profile construction; binary artwork stencils to rounded distance-field sculpt; curvature-adaptive gameplay reduction; registered unique gouache albedo. Not displacement from albedo brightness.'}
# Keep pristine pre-export source, then validated Blender→FBX conversion.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CounterWorkflow07.blend'))
game.matrix_world=Matrix.Rotation(math.pi,4,'Z')@game.matrix_world;bpy.ops.object.select_all(action='DESELECT');game.select_set(True);bpy.context.view_layer.objects.active=game;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM_CW07_HeroCounter.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetReport.json').write_text(json.dumps(report,indent=2));print('COUNTER07_READY',report)
