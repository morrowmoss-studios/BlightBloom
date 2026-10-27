import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));s=bpy.context.scene
if bpy.data.objects.get('CM_SW13_ServiceCounter'):raise RuntimeError('Already built')
P=lambda v:Vector((v[0],v[2],v[1]));parts=[];modules=[];wood=bpy.data.materials['CM_SW13_PaintedWalnut'];sage=bpy.data.materials['CM_SW13_Sage'];brass=bpy.data.materials['CM_SW13_AgedBrass']
carved=bpy.data.materials.new('CM_SW13_RegisteredCarving');carved.use_nodes=True;bs=carved.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;t=carved.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow07/Textures/CM_CW07_CarvedWalnut.png'));t.image.pack();carved.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
t=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(t[t.index('def smooth('):t.index('ogee=')]);t=(D.parent/'ShopWorkflow10/build_shop10.py').read_text();exec(t[t.index('def timber('):t.index('# Medicine cabinet:')])
# Recover the successful shaped worktop, use its exact planar service surface and envelope.
with bpy.data.libraries.load(str(D.parent/'CounterWorkflow09/CM_CounterWorkflow09.blend'),link=False) as (f,to):to.objects=['Shaped breadboard worktop - flat service datum']
top=to.objects[0];s.collection.objects.link(top);top.hide_set(False);top.hide_render=False;top.data.materials.clear();top.data.materials.append(wood);parts.append(top)
# A continuous bowed service body is fitted behind the carved fields; deliberate full mass unlike the old light table.
extrude('Jointed closed service body',[(-1.025,.12),(1.025,.12),(1.025,.95),(-1.025,.95)],-.285,.274,b=.009)
front=lambda x:.303+.036*math.cos(math.pi*x/1.04)
bottom=lambda x:.175+.025*math.sin(abs(x)*math.pi)**2
for side in [-1,1]:
 rings=[(.003,1.018,.265,.080,.070),(.10,1.018,.265,.080,.070),(.20,.995,.264,.061,.061),(.47,.990,.262,.061,.062),(.78,.997,.264,.067,.067),(.94,1.012,.270,.078,.071)]
 profile=[(-1,-.75),(-.75,-1),(.75,-1),(1,-.75),(1,.75),(.75,1),(-.75,1),(-1,.75)];N=len(profile)
 vs=[(side*(x+u*w),y,z+v*d) for y,x,z,w,d in rings for u,v in profile];fs=[tuple(reversed(range(N))),tuple(range(len(vs)-N,len(vs)))]+[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(len(rings)-1) for i in range(N)];mesh('Stepped engaged counter standard',vs,fs,wood,.003)
 # Shaped end panel, a genuine quiet recessed area.
 poly=[(-.27,.18),(.26,.18),(.27,.89),(-.27,.89)]
 # local XY extrusion is rotated into the end plane after creation
 o=extrude('Inset end field',poly,-.012,.012,sage,.004)
 for v in o.data.vertices:
  x,y,z=v.co.x,v.co.z,v.co.y;v.co=P((side*1.031+side*z,y,x))
 smooth(o.data)
# Curved plinth and two structural face rails; foreground silhouette carries real shape.
poly=[(-1.10,-.30),(1.10,-.30),(1.10,.29)]+[(x,front(x)+.01) for x in np.linspace(1.10,-1.10,41)]+[(-1.10,.29)]
slab('Splayed shaped foot plinth',poly,.055,.135,.007)
for y in [.19,.90]:
 profile_sweep('Bowed bearing face rail',[(x,y,front(x)) for x in np.linspace(-1.01,1.01,49)],[(-.037,-.023),(-.037,.008),(-.022,.026),(.022,.026),(.037,.008),(.037,-.023)])
for x in [-.35,.35]:
 profile_sweep('Fitted panel stile',[(x,.20,front(x)),(x+.006,.52,front(x)+.003),(x,.88,front(x))],[(-.025,-.012),(-.025,.017),(.025,.017),(.025,-.012)])
# Three deliberately registered relief fields, existing approved sculpt artwork, adapted to the new bowed substrate.
fields=np.load(D.parent/'CounterWorkflow07/SculptFields.npy');N=97
for index,(cx,w) in enumerate([(-.70,.52),(0,.62),(.70,.52)]):
 H=fields[index];vs=[]
 for j in range(N):
  v=j/(N-1)
  for i in range(N):
   u=i/(N-1);x=cx+(u-.5)*w;y=.245+v*.60;h=float(H[round((1-v)*(H.shape[0]-1)),round(u*(H.shape[1]-1))]);vs.append((x,y,front(x)-.012+h*.70))
 fs=[(j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i) for j in range(N-1) for i in range(N-1)];o=mesh('Integrated registered relief field '+str(index),vs,fs,carved);uv=o.data.uv_layers[0]
 for f in o.data.polygons:
  for li in f.loop_indices:
   vi=o.data.loops[li].vertex_index;j,i=divmod(vi,N);uv.data[li].uv=((index+i/(N-1))/3,j/(N-1))
 bpy.context.view_layer.objects.active=o;dec=o.modifiers.new('Focal curvature reduction','DECIMATE');dec.ratio=.28;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
 # Close only the boundary/back, not a second dense relief.
 bm=bmesh.new();bm.from_mesh(o.data);edges=[e for e in bm.edges if e.is_boundary];border=set(v for e in edges for v in e.verts);cp={v:bm.verts.new((v.co.x,.277,v.co.z)) for v in border};adj={v:[] for v in border}
 for e in edges:
  a,b=e.verts;adj[a].append(b);adj[b].append(a);bm.faces.new((a,b,cp[b],cp[a]))
 order=[next(iter(border))];previous=None
 while True:
  nxt=next((v for v in adj[order[-1]] if v is not previous),None)
  if nxt is None or nxt is order[0]:break
  previous=order[-1];order.append(nxt)
 bm.faces.new([cp[v] for v in reversed(order)]);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();smooth(o.data)
 for a,b in [((cx-w/2,.235),(cx+w/2,.235)),((cx-w/2,.855),(cx+w/2,.855)),((cx-w/2,.235),(cx-w/2,.855)),((cx+w/2,.235),(cx+w/2,.855))]:
  timber('Carved field housing',(a[0],a[1],front(a[0])+.002),(b[0],b[1],front(b[0])+.002),.020,.025,.002)
# Real service-side drawers are usable from the existing staff aisle.
for j,y in enumerate([.44,.73]):
 for x in [-.65,0,.65]:
  extrude('Fitted service drawer',[(x-.29,y-.10),(x+.29,y-.10),(x+.29,y+.10),(x-.29,y+.10)],-.335,-.282,b=.006)
  o=extrude('Inset drawer field',[(x-.24,y-.065),(x+.24,y-.065),(x+.24,y+.065),(x-.24,y+.065)],-.340,-.336,sage,.003)
finish('CM_SW13_ServiceCounter');g=modules[0][0]
# Give this reused-shape counter neutral cavity by default; the registered sculpt carries its own paint values.
attr=g.data.color_attributes.new(name='PaintedCavity',type='FLOAT_COLOR',domain='POINT')
for q in attr.data:q.color=(1,1,1,1)
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM_SW13_ServiceCounter.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((D/'AssetCatalog.json').read_text());cat['modules'].append(modules[0][1]);cat['triangles']=sum(r['triangles'] for r in cat['modules']);(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2));print('COUNTER13_READY',modules[0][1])
