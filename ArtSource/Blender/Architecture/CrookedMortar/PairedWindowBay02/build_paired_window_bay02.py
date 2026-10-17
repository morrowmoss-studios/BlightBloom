"""Paired casement production candidate measured from approved StyledDetails07.
Metric, Unity +Y up/+Z exterior; existing assets are read only. Explicit regeneration flag.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/PairedWindowBay02'
if (OUT/'CM_PairedWindowBay02.blend').exists() and '--refine-own-asset' not in sys.argv:raise RuntimeError('Refusing existing source')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;bpy.context.preferences.filepaths.save_version=0
paint=bpy.data.images.load(str(ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));paint.pack();paint.colorspace_settings.name='sRGB'
mats={}
for key in ['Timber','Shutters','Plaster','Glass','Iron','Soil']:
 m=bpy.data.materials.new('CM_Paired_'+key);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');m.node_tree.links.new(em.outputs[0],out.inputs[0])
 if key in ['Glass','Iron','Soil']:em.inputs['Color'].default_value={'Glass':(.36,.185,.055,1),'Iron':(.045,.052,.043,1),'Soil':(.075,.048,.025,1)}[key]
 else:
  uv=n.new('ShaderNodeUVMap');uv.uv_map='PaintProjection';tex=n.new('ShaderNodeTexImage');tex.image=paint;tex.extension='EXTEND';m.node_tree.links.new(uv.outputs[0],tex.inputs['Vector']);m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color'])
 mats[key]=m
parts=[];modules={};current='';sockets=[]
def P(x,y,z):return(x,z,y)
def module(key,pivot=(0,0,0),placement=(0,0,0),rotation=0,notes=''):
 global current
 current='CM_PairedWindowBay02_'+key;modules[current]={'name':current,'pivot':pivot,'placement':placement,'rotationY':rotation,'notes':notes,'parts':[]}
def mesh(name,vs,fs,key='Timber',bevel=.004):
 me=bpy.data.meshes.new(current+'_'+name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(me.name,me);s.collection.objects.link(o);me.materials.append(mats[key]);o['module']=current;o['paint']=key;bpy.context.view_layer.objects.active=o
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if bevel:
  mod=o.modifiers.new('Small hand-crafted edge bevel','BEVEL');mod.width=bevel;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in me.polygons:p.use_smooth=True
 bm=bmesh.new();bm.from_mesh(me)
 for e in bm.edges:e.smooth=e.is_manifold and e.calc_face_angle()<math.radians(42)
 bm.to_mesh(me);bm.free();wn=o.modifiers.new('Weighted crafted normals','WEIGHTED_NORMAL');wn.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=wn.name)
 parts.append(o);modules[current]['parts'].append(o.name);return o

def box(n,p,d,k='Timber',b=.004):
 x,y,z=p;a,c,e=[q/2 for q in d];vs=[P(x+sx*a,y+sy*c,z+sz*e) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
 return mesh(n,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],k,b)
def prism(n,poly,z0,z1,k='Timber',b=.004):
 count=len(poly);vs=[P(x,y,z) for z in [z0,z1] for x,y in poly];fs=[tuple(range(count-1,-1,-1)),tuple(range(count,2*count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)];return mesh(n,vs,fs,k,b)
def beam(n,a,b,w,d=.12,k='Timber',bow=.002):
 aa,bb=Vector(P(*a)),Vector(P(*b));t=(bb-aa).normalized();ref=Vector((0,1,0));u=t.cross(ref).normalized();v=t.cross(u);vs=[]
 for f in [0,.5,1]:
  c=aa.lerp(bb,f)+u*bow*math.sin(f*math.pi)
  for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(tuple(c+u*i*w/2+v*j*d/2))
 return mesh(n,vs,[(3,2,1,0),(8,9,10,11)]+[(r*4+i,r*4+(i+1)%4,(r+1)*4+(i+1)%4,(r+1)*4+i) for r in range(2) for i in range(4)],k,.003)
module('FixedFrame',notes='Approved rectangular pair: centres +/-0.49m; each frame-centre width .76m, height1.60m, sill datum1.11m. Central housed stile .135m.')
for side in [-1,1]:
 x=side*.49
 for edge in [-1,1]:beam('Jamb_'+str(side)+'_'+str(edge),(x+edge*.38,1.11,.105),(x+edge*.38,2.71,.105),.085,.17,bow=side*.002)
 for y in [1.11,2.71]:beam('Rail_'+str(side)+'_'+str(y),(x-.3375,y,.105),(x+.3375,y,.105),.09,.17,bow=.0015)
beam('CentralHousedPost',(0,1.065,.095),(0,2.82,.095),.135,.20,bow=.001)
box('CommonLintel',(0,2.80,.065),(2.04,.13,.22),b=.006)
module('Casement_L',pivot=(-.805,1.16,.09),placement=(-.805,1.16,.09),notes='Closed left casement insert; hinge pivot for later authoring, no behaviour.')
for side in [-1,1]:
 if side==1:module('Casement_R',pivot=(.805,1.16,.09),placement=(.805,1.16,.09))
 x=side*.49
 box('PaintedWarmGlazing',(x,1.91,.065),(.651,1.489,.018),'Glass',.002)
 beam('CentralGlazingBar',(x,1.165,.115),(x,2.655,.115),.048,.065,bow=.0015)
 for y in [1.16,2.66]:beam('RebatedLeafRail',(x-.324,y,.115),(x+.324,y,.115),.035,.065,bow=.001)
 for xx in [x-.324,x+.324]:beam('RebatedLeafStile',(xx,1.16,.115),(xx,2.66,.115),.035,.065,bow=.001)
 box('SmallLatch',(x-side*.265,1.83,.16),(.025,.11,.025),'Iron',.003)
module('ArchedHood_Optional',notes='Quiet segmental hood; off by default to preserve the benchmark rectangular front elevation.')
N=24;outer=[];inner=[]
for i in range(N+1):
 x=-1.03+2.06*i/N;y=2.78+.20*(1-(x/1.03)**2);outer.append((x,y+.027));inner.append((x,y-.027))
prism('ContinuousShallowArch',outer+list(reversed(inner)),.09,.17,b=.003)
for side in [-1,1]:
 pivot=(side*.99,1.11,.16);module('Shutter_'+('L' if side<0 else 'R'),pivot=pivot,placement=pivot,rotation=side*153,notes='Detachable .96m curved-top plank shutter with actual hinge pivot; default opens153deg. Matching individual planks, rails and straps.')
 for i in range(3):
  a=.014+i*.316;b=a+.305;x0,x1=sorted((side*(.99-a),side*(.99-b)))
  top=lambda x:2.25+.24*(1-(x/1.0)**2)
  poly=[(x0,1.17),(x1,1.17)]+[(x1+(x0-x1)*j/5,top(x1+(x0-x1)*j/5)) for j in range(6)]
  prism('SagePlank_'+str(i),poly,.132,.188,'Shutters',.006)
 for y in [1.384,1.923]:
  box('RearCrossRail',(side*.51,y,.115),(.91,.075,.042),'Timber',.004)
  box('HingeStrap',(side*.82,y,.207),(.33,.035,.025),'Iron',.003)
 for y in [1.384,1.923]:box('HingeKnuckle',(side*.988,y,.158),(.028,.07,.09),'Iron',.004)
module('Sill',notes='Projecting sill2.04m wide; bottom drip bevel; independent toggle.')
# Continuous x-extruded water-shedding timber profile.
profile=[(-.13,1.105),(.35,1.091),(.38,1.075),(.38,.985),(.35,.965),(-.13,.965)];n=len(profile);vs=[P(x,y,z) for x in [-1.02,1.02] for z,y in profile];mesh('WaterShedSill',vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],bevel=.006)
module('PlanterBrackets',notes='Two seated corbels support planter bottom at y.65; independent from sill.')
for x in [-.62,.62]:
 # Side profile extruded across x.
 poly=[(.035,.39),(.035,.65),(.49,.65),(.49,.59),(.18,.59),(.115,.39)];n=len(poly);vs=[P(xx,y,z) for xx in [x-.045,x+.045] for z,y in poly];mesh('HousedCorbel',vs,[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],bevel=.005)
module('FlowerBox',notes='Open-top fitted wooden planter; soil separate mesh, no mandatory flowers. 2.1m wide approved scale.')
box('Base',(0,.674,.37),(1.97,.048,.32),b=.005)
prism('FrontTaperedBoard',[(-.99,.65),(.99,.65),(1.05,.93),(-1.05,.93)],.52,.565,b=.007)
prism('BackTaperedBoard',[(-.99,.65),(.99,.65),(1.05,.93),(-1.05,.93)],.175,.22,b=.006)
for x in [-1.015,1.015]:box('EndCheek',(x,.80,.37),(.065,.25,.39),b=.006)
box('RecessedSoil',(0,.87,.37),(1.95,.026,.29),'Soil',.002)
# New measured host, not a modification of existing facade-kit models.
module('FacadeInfill_4p5m',notes='4.5m post-centre span /3.24m floor rise; .28m plaster, two true .84x1.69m openings. Wide header omits an obstructing intermediate post.')
wall=box('IvoryPlasterWithTrueOpenings',(0,1.62,-.14),(4.32,2.8,.28),'Plaster',0)
for x in [-.49,.49]:
 cut=box('TEMP',(x,1.915,-.1),(.84,1.69,1.0),'Plaster',0);parts.remove(cut);modules[current]['parts'].remove(cut.name);bpy.context.view_layer.objects.active=wall;mod=wall.modifiers.new('Through rough casement opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
mod=wall.modifiers.new('Soft reveal edge','BEVEL');mod.width=.004;mod.segments=2;bpy.context.view_layer.objects.active=wall;bpy.ops.object.modifier_apply(modifier=mod.name)
module('WideHeader_4p5m',notes='4.32m shoulder length plus shared .18m posts gives4.5m grid. Same facade .22m height/.42m depth.')
box('WalnutHeader',(0,.11,-.07),(4.32,.22,.42),b=.004)
# Unique UV0, consistent density across the complete component family.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.002);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.003);bpy.ops.object.mode_set(mode='OBJECT')
for o in parts:
 uv=o.data.uv_layers.new(name='PaintProjection');cs=[v.co for v in o.data.vertices];lo=[min(p[i] for p in cs) for i in range(3)];sp=[max(p[i] for p in cs)-lo[i] for i in range(3)];along=max(range(3),key=lambda i:sp[i]);cross=max([i for i in range(3) if i!=along],key=lambda i:sp[i])
 for face in o.data.polygons:
  for li in face.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co
   if o['paint']=='Plaster':u=.5+v.x/6.3;w=.06+v.z/5.2;uu,vv=.012,.512
   elif o['paint']=='Shutters':u=.5+(v.x-(lo[0]+sp[0]/2))/.85;w=.10+(v.z-lo[2])/3.6;uu,vv=.012,.012
   else:u=.5+(v[cross]-(lo[cross]+sp[cross]/2))/.85;w=.10+(v[along]-lo[along])/3.6;uu,vv=.512,.512
   uv.data[li].uv=(uu+.476*max(.025,min(.975,u)),vv+.476*max(.025,min(.975,w)))
 o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in parts:c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();receiver=bpy.context.object
atlas=bpy.data.images.new('CM_PairedWindowBay02_Painted_BaseColor',width=2048,height=2048,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(ASSET/'Textures/CM_PairedWindowBay02_Painted_BaseColor.png');atlas.file_format='PNG'
for m in receiver.data.materials:n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=atlas;m.node_tree.nodes.active=n
s.render.bake.margin=8;bpy.ops.object.bake(type='EMIT');atlas.save();atlas.pack();bpy.data.objects.remove(receiver,do_unlink=True)
for o in parts:o.data.uv_layers.remove(o.data.uv_layers['PaintProjection']);o.data.uv_layers.active_index=0
for m in mats.values():
 n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=1;tex=n.new('ShaderNodeTexImage');tex.image=atlas;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(bs.outputs[0],out.inputs[0])
report={'parts':[],'dimensions':{'floorRise':3.24,'hostGridWidth':4.5,'wallThickness':.28,'casementCentres':[-.49,.49],'casementWidth':.76,'casementHeight':1.6,'base':1.11,'top':2.71},'up':'Unity+Y','front':'Unity+Z','uniqueAtlas':2048};dims={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles)
 if bad or vol<=0 or deg:raise RuntimeError((o.name,bad,vol,deg))
 uv=o.data.uv_layers[0];uvbad=0
 for t in o.data.loop_triangles:
  a,b,c=[uv.data[i].uv for i in t.loops];uvbad+=abs((b-a).cross(c-a))<2e-12
 if uvbad:raise RuntimeError(('degenerate UV',o.name,uvbad))
 assert all(0<=q.uv.x<=1 and 0<=q.uv.y<=1 for q in uv.data)
 report['parts'].append({'name':o.name,'module':o['module'],'triangles':len(o.data.loop_triangles),'nonmanifold':bad,'volume':vol,'degenerateTriangles':deg,'degenerateUVs':uvbad})
 pivot=Vector(P(*modules[o['module']]['pivot']))
 for v in o.data.vertices:v.co-=pivot
 pts=[(v.co.x,v.co.z,v.co.y) for v in o.data.vertices];entry=dims.setdefault(o['module'],{'points':[],'triangles':0});entry['points']+=pts;entry['triangles']+=len(o.data.loop_triangles)
for key,v in dims.items():pts=v.pop('points');v['min']=[min(p[i] for p in pts) for i in range(3)];v['max']=[max(p[i] for p in pts) for i in range(3)]
sockets=[{'name':'FloorDatum','position':[0,0,0]},{'name':'FloorAbove','position':[0,3.24,0]},{'name':'GridLeft','position':[-2.25,0,0]},{'name':'GridRight','position':[2.25,0,0]},{'name':'ShutterHinge_L','position':[-.99,1.11,.16]},{'name':'ShutterHinge_R','position':[.99,1.11,.16]},{'name':'Planter','position':[0,.65,.37]},{'name':'Sill','position':[0,1.035,.11]}]
# Editable source shows assembled closed components; hinges and independent meshes retain named groups.
for name in modules:
 col=bpy.data.collections.new(name);s.collection.children.link(col)
 for o in [p for p in parts if p['module']==name]:
  s.collection.objects.unlink(o);col.objects.link(o);o.location=Vector(P(*modules[name]['placement']))
for sock in sockets:e=bpy.data.objects.new('Socket_'+sock['name'],None);s.collection.objects.link(e);e.location=P(*sock['position']);e.empty_display_type='ARROWS';e.empty_display_size=.1
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CM_PairedWindowBay02.blend'))
for name,meta in modules.items():
 bpy.ops.object.select_all(action='DESELECT');selected=[]
 for o in [p for p in parts if p['module']==name]:
  c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.location=(0,0,0);c.rotation_euler=(0,0,0);c.select_set(True);selected.append(c)
 bpy.context.view_layer.objects.active=selected[0];bpy.ops.object.join();export=bpy.context.object;export.name=name+'_Geometry'
 # All paint roles have already been transferred into one UV atlas. One draw material per component.
 export.data.materials.clear();export.data.materials.append(mats['Timber'])
 for face in export.data.polygons:face.material_index=0
 bpy.context.view_layer.update();export.matrix_world=Matrix.Rotation(math.pi,4,'Z')@export.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(ASSET/'Models'/f'{name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 bpy.data.objects.remove(export,do_unlink=True)
(OUT/'ModuleCatalog.json').write_text(json.dumps(list(modules.values()),indent=2));(OUT/'AttachmentPoints.json').write_text(json.dumps(sockets,indent=2));(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(OUT/'SourceDimensions.json').write_text(json.dumps(dims,indent=2));print('PAIRED_WINDOW_READY',len(modules),len(parts),sum(p['triangles'] for p in report['parts']))
