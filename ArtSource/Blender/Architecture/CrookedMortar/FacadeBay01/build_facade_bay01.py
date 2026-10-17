"""Facade kit, real closed meshes, approved paint, metric keyed modules. Background only."""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/FacadeBay01'
if not bpy.app.background:raise RuntimeError('Background Blender required')
if (OUT/'CM_FacadeBay01.blend').exists() and '--refine-own-kit' not in sys.argv:raise RuntimeError('Refusing overwrite')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1
parts=[];modules={};current=None
paint=bpy.data.images.load(str(ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));paint.colorspace_settings.name='sRGB';paint.pack()
mats={}
for key in ['Plaster','Walnut']:
 m=bpy.data.materials.new('CM_FacadeBay01_'+key);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');uv=n.new('ShaderNodeUVMap');uv.uv_map='PaintProjection';tex=n.new('ShaderNodeTexImage');tex.image=paint;tex.extension='EXTEND';m.node_tree.links.new(uv.outputs[0],tex.inputs['Vector']);m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs[0]);mats[key]=m

def start(name,w,h,description,sockets=None):
 global current
 current=name;modules[name]={'name':name,'grid_width':w,'height':h,'description':description,'parts':[],'sockets':sockets or [{'name':'LeftGrid','position':[-w/2,0,0]},{'name':'RightGrid','position':[w/2,0,0]},{'name':'StackTop','position':[0,h,0]},{'name':'ExteriorPlane','position':[0,0,0]}]}

def P(x,y,z):return(x,z,y)
def seat_edges(o,axis=1):
 a=o.data.attributes.get('bevel_weight_edge') or o.data.attributes.new('bevel_weight_edge','FLOAT','EDGE')
 for e in o.data.edges:
  d=o.data.vertices[e.vertices[0]].co-o.data.vertices[e.vertices[1]].co;a.data[e.index].value=0 if abs(d[axis])>.999*d.length else 1

def finish(name,vs,fs,key='Plaster',bevel=.004):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.data.materials.append(mats[key]);o['module']=current;o['paint']=key
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();bpy.context.view_layer.objects.active=o
 if bevel:
  mod=o.modifiers.new('Restrained hand-crafted bevel','BEVEL');mod.width=bevel;mod.segments=2;mod.harden_normals=True
  if key=='Plaster':seat_edges(o,0 if 'PlasterSide' in name else 1);mod.limit_method='WEIGHT'
  bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.use_smooth=True
 bm=bmesh.new();bm.from_mesh(o.data)
 for e in bm.edges:e.smooth=e.is_manifold and e.calc_face_angle()<math.radians(44)
 bm.to_mesh(o.data);bm.free();mod=o.modifiers.new('Weighted architectural normals','WEIGHTED_NORMAL');mod.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o);modules[current]['parts'].append(name);return o

def box(name,p,d,key='Plaster',bevel=.004):
 x,y,z=p;a,b,c=[v/2 for v in d];vs=[P(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
 return finish(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],key,bevel)

def prism(name,poly,back=-.28,front=0,key='Plaster',bevel=.004):
 n=len(poly);return finish(name,[P(x,y,z) for z in [back,front] for x,y in poly],[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],key,bevel)

def boolean(o,cutter,operation='DIFFERENCE'):
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('True architectural opening','BOOLEAN');mod.solver='EXACT';mod.operation=operation;mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);parts.remove(cutter);modules[current]['parts'].remove(cutter.name);bpy.data.objects.remove(cutter,do_unlink=True)

for w,h in [(3,3.35),(1.5,3.35),(3,3.6)]:
 name='CM_FacadeBay01_Plain_'+('3m' if w==3 else '1p5m')+('_Tall' if h==3.6 else '')
 start(name,w,h,'Plaster infill, .28m thick; .18m shared post grid and .22m floor/head beams; exterior at Z=0.')
 box(name+'_Plaster',(0,h/2,-.14),(w-.18,h-.44,.28),bevel=.006)
for h in [3.35,3.6]:
 name='CM_FacadeBay01_Post_'+('3p35m' if h==3.35 else '3p60m');start(name,.18,h,'Single shared boundary post; 0.18m width, .42m depth. No duplicate posts between bays.')
 # Interfaces stay straight; subtle hewn side-face changes are confined between exact end rings.
 vs=[]
 for y,drift,w in [(0,0,.18),(.12,0,.18),(h*.5,.002,.179),(h-.12,0,.18),(h,0,.18)]:
  for x,z in [(-w/2,-.28),(w/2,-.28),(w/2,.14),(-w/2,.14)]:vs.append(P(x+drift,y,z))
 fs=[(3,2,1,0),tuple(range(16,20))]+[(r*4+i,r*4+(i+1)%4,(r+1)*4+(i+1)%4,(r+1)*4+i) for r in range(4) for i in range(4)]
 finish(name+'_Timber',vs,fs,'Walnut',.004)
for w in [3,1.5]:
 name='CM_FacadeBay01_Beam_'+('3m' if w==3 else '1p5m');start(name,w,.22,'Between-post shoulder length grid width minus .18m; bottom-centre pivot, .22m height, .42m depth.')
 box(name+'_Timber',(0,.11,-.07),(w-.18,.22,.42),'Walnut',.004)
for hand in ['L','R']:
 name='CM_FacadeBay01_Brace45_'+hand;start(name,1,1,'Flat seated end shoulders fit post face and beam underside; embedded rear depth, grain follows diagonal.', [{'name':'PostShoulder','position':[0,0,0]},{'name':'BeamShoulder','position':[1 if hand=='L' else -1,1,0]}])
 poly=[(0,0),(.14,0),(1,.86),(1,1),(.86,1),(0,.14)]
 if hand=='R':poly=[(-x,y) for x,y in poly][::-1]
 prism(name+'_Timber',poly,-.12,.14,'Walnut',.004)
name='CM_FacadeBay01_Corner90';start(name,3,3.35,'Exterior vertex pivot; walnut corner with two complete 3m grid return bays and mitred timber/plaster transitions.', [{'name':'FrontReturnEnd','position':[-3,0,0]},{'name':'SideReturnEnd','position':[0,0,-3]},{'name':'StackTop','position':[0,3.35,0]}])
box(name+'_Post',(0,1.675,0),(.28,3.35,.28),'Walnut',.004)
# Plan-view mitres partition the internal corner; no coincident plaster return faces.
for suffix,poly in [('Front',[(-2.91,-.28),(-.28,-.28),(-.14,-.14),(-.14,0),(-2.91,0)]),('Side',[(-.28,-2.91),(0,-2.91),(0,-.14),(-.14,-.14),(-.28,-.28)])]:
 n=len(poly);vs=[P(x,y,z) for y in [.22,3.13] for x,z in poly];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];finish(name+'_Plaster'+suffix,vs,fs,'Plaster',.002)
# Mitred horizontal rails meet the corner post and shared end posts without duplicate faces.
for suffix,poly in [('Front',[(-2.91,-.28),(-.28,-.28),(-.14,-.14),(-.14,.14),(-2.91,.14)]),('Side',[(-.28,-2.91),(.14,-2.91),(.14,-.14),(-.14,-.14),(-.28,-.28)])]:
 for y in [0,3.13]:
  n=len(poly);vs=[P(x,yy,z) for yy in [y,y+.22] for x,z in poly];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];finish(name+'_Rail'+suffix+str(y),vs,fs,'Walnut',.003)
name='CM_FacadeBay01_WindowOpening_3m';start(name,3,3.35,'Actual 1.6m wide arch through .28m plaster. Approved WindowBay01 insert at same origin; original wall/framing/eave omitted in adapter.')
wall=box(name+'_RevealedPlaster',(0,1.675,-.14),(2.82,2.91,.28),bevel=0)
outline=[(-.8,1.1),(.8,1.1)]+[(.8*math.cos(i*math.pi/32),1.75+.65*math.sin(i*math.pi/32)) for i in range(33)]
cut=prism('TEMP_ArchOpening',outline,-.65,.65,bevel=0);boolean(wall,cut)
bpy.context.view_layer.objects.active=wall;mod=wall.modifiers.new('Soft reveal edges','BEVEL');mod.width=.005;mod.segments=2;seat_edges(wall);mod.limit_method='WEIGHT';bpy.ops.object.modifier_apply(modifier=mod.name)
modules[name]['sockets'] += [{'name':'WindowBay01_Insert','position':[0,0,0]},{'name':'SillCentre','position':[0,1.1,0]}]
# Exact approved finished-floor rise: 3.44 - .20 = 3.24m. Keep standard variants too.
import copy
for src,suffix in [('CM_FacadeBay01_Plain_3m','CM_FacadeBay01_Plain_3m_Benchmark'),('CM_FacadeBay01_Post_3p35m','CM_FacadeBay01_Post_3p24m'),('CM_FacadeBay01_Corner90','CM_FacadeBay01_Corner90_Benchmark'),('CM_FacadeBay01_WindowOpening_3m','CM_FacadeBay01_WindowOpening_3m_Benchmark')]:
 meta=copy.deepcopy(modules[src]);meta['name']=suffix;meta['height']=3.24;meta['description']+=' Benchmark variant: 3.24m finished-floor rise.';meta['parts']=[]
 for sock in meta['sockets']:
  if sock['name']=='StackTop':sock['position'][1]=3.24
 modules[suffix]=meta
 for o in list(parts):
  if o['module']!=src:continue
  c=o.copy();c.data=o.data.copy();c.name=o.name.replace(src,suffix);c['module']=suffix;s.collection.objects.link(c)
  for v in c.data.vertices:
   if v.co.z>3:v.co.z-=.11
  c.data.update();parts.append(c);meta['parts'].append(c.name)
# Gables follow wall infill only; no roof, tiles or botanical family assets.
for name,w,profile in [
 ('CM_FacadeBay01_Gable_HeroB',5.55,[(-2.745,0),(-2.275,.45),(-1.325,3.22),(-.575,4.37),(.075,3.60),(2.245,.55),(2.805,.05)]),
 ('CM_FacadeBay01_Gable_Secondary',3,[(-1.5,0),(0,1.95),(1.5,0)])]:
 height=max(p[1] for p in profile);start(name,w,height,'B-derived asymmetric wall-end profile; no roof surfaces. Bottom baseline pivot. Shared .28m wall depth.', [{'name':'LeftEave','position':[profile[0][0],0,0]},{'name':'RightEave','position':[profile[-1][0],profile[-1][1],0]},{'name':'Apex','position':[*next((x,y) for x,y in profile if y==height),0]}])
 # Clip rake/infill to common base plane; no timber projects into the wall below.
 def clip_y(poly):
  out=[];prev=poly[-1]
  for cur in poly:
   if (cur[1]>=0)!=(prev[1]>=0):
    t=-prev[1]/(cur[1]-prev[1]);out.append((prev[0]+t*(cur[0]-prev[0]),0))
   if cur[1]>=0:out.append(cur)
   prev=cur
  clean=[]
  for p in out:
   if not clean or (Vector(p)-Vector(clean[-1])).length>1e-7:clean.append(p)
  if len(clean)>1 and (Vector(clean[0])-Vector(clean[-1])).length<1e-7:clean.pop()
  return clean
 inner=[(x,y-.14) for x,y in profile]
 bandpoly=clip_y(profile+list(reversed(inner)))
 infillpoly=clip_y([inner[0],inner[-1]]+list(reversed(inner[1:-1])))
 infill=prism(name+'_Plaster',infillpoly,-.28,0,bevel=.003)
 band=prism(name+'_ContinuousRake',bandpoly,-.28,.14,'Walnut',.003)
 apex=next((x,y) for x,y in profile if y==height);post=box(name+'_KingPost',(apex[0],(height-.14)/2,-.07),(.14,height-.14,.42),'Walnut',.003)
 # Seat the king post against the actual inner rake, then house it into plaster.
 clip=prism('TEMP_KingSlope',infillpoly,-.5,.5,'Walnut',0);boolean(post,clip,'INTERSECT')
 cut=box('TEMP_KingSeat',(apex[0],height/2,-.14),(.14,height+1,.7),'Walnut',0);boolean(infill,cut)
modules['CM_FacadeBay01_Gable_HeroB']['profile_unity']=modules['CM_FacadeBay01_Gable_HeroB'].get('profile_unity',[[-2.745,0],[-2.275,.45],[-1.325,3.22],[-.575,4.37],[.075,3.6],[2.245,.55],[2.805,.05]])
# Unique UV0 across kit, then painted projection transfer into a reusable shared albedo.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.002);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
for o in parts:
 uv=o.data.uv_layers.new(name='PaintProjection');coords=[v.co for v in o.data.vertices];dims=[max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3)];long=max(range(3),key=lambda i:dims[i]);across=max([i for i in range(3) if i!=long],key=lambda i:dims[i]);mins=[min(v[i] for v in coords) for i in range(3)]
 for p in o.data.polygons:
  for li in p.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co
   if o['paint']=='Plaster':u=.50+(v.y if abs(p.normal.x)>.7 else v.x)/6.3;w=.06+v.z/5.2;startu=.012
   else:
    if 'Brace45' in o.name:along=(abs(v.x)+v.z)*.7071;cross=(v.z-abs(v.x))*.7071;u=.5+cross/.85;w=.10+along/3.6
    elif 'ContinuousRake' in o.name:u=.5+(v.z/4.5-v.x/6)*.15;w=.10+(v.x-mins[0])/6
    else:u=.5+(v[across]-(mins[across]+dims[across]/2))/.85;w=.10+(v[long]-mins[long])/3.6
    startu=.512
   u=max(.025,min(.975,u));w=max(.025,min(.975,w));uv.data[li].uv=(startu+.476*u,.512+.476*w)
 o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in parts:c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();receiver=bpy.context.object
atlas=bpy.data.images.new('CM_FacadeBay01_Painted_BaseColor',width=4096,height=4096,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(ASSET/'Textures/CM_FacadeBay01_Painted_BaseColor.png');atlas.file_format='PNG'
for m in receiver.data.materials:n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=atlas;m.node_tree.nodes.active=n
s.render.bake.margin=8;bpy.ops.object.bake(type='EMIT');atlas.save();atlas.pack();bpy.data.objects.remove(receiver,do_unlink=True)
for o in parts:o.data.uv_layers.remove(o.data.uv_layers['PaintProjection']);o.data.uv_layers.active_index=0
for m in mats.values():
 n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=1;tex=n.new('ShaderNodeTexImage');tex.image=atlas;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(bs.outputs[0],out.inputs[0])
report={'parts':[],'units':'metres','up':'Unity +Y','front':'Unity +Z','wall_depth':.28,'storey_heights':[3.24,3.35,3.6],'paint_source':paint.filepath,'atlas':4096}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 assert bad==0 and volume>0 and deg==0,(o.name,bad,volume,deg)
 report['parts'].append({'name':o.name,'module':o['module'],'triangles':len(o.data.loop_triangles),'nonmanifold_edges':bad,'volume':volume,'degenerate_triangles':deg})
# Layout editable source for inspection; export temporarily returns each module to its canonical pivot.
for idx,(name,meta) in enumerate(modules.items()):
 for o in [p for p in parts if p['module']==name]:o.location=Vector((idx%5*7,idx//5*-7,0))
for name,meta in modules.items():
 for sock in meta['sockets']:
  e=bpy.data.objects.new(name+'__'+sock['name'],None);s.collection.objects.link(e);idx=list(modules).index(name);e.location=Vector(P(*sock['position']))+Vector((idx%5*7,idx//5*-7,0));e.empty_display_type='ARROWS';e.empty_display_size=.15
s.render.film_transparent=False;bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CM_FacadeBay01.blend'))
for name,meta in modules.items():
 bpy.ops.object.select_all(action='DESELECT');selected=[o for o in parts if o['module']==name]
 for o in selected:o.location=(0,0,0);o.select_set(True)
 bpy.context.view_layer.update()
 for o in selected:o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
 bpy.context.view_layer.objects.active=selected[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(ASSET/'Models'/f'{name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(OUT/'ModuleCatalog.json').write_text(json.dumps(list(modules.values()),indent=2));(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));print('FACADE_KIT_READY',len(modules),len(parts),sum(p['triangles'] for p in report['parts']))
