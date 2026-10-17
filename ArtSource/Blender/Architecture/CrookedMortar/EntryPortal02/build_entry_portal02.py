"""CM_EntryPortal02: exact approved portal curves, continuous joined timber construction.
Unity asset axes: +Y up, +Z exterior. Approved placement (.85,.20,-5.52), yaw180.
Only new EntryPortal02 outputs can be regenerated with --refine-new-asset.
"""
import bpy,bmesh,math,json,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02';PAINT=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/EntryPortal02'
BLEND=OUT/'CM_EntryPortal02.blend';FBX=ASSET/'Models/CM_EntryPortal02.fbx';ATLAS=ASSET/'Textures/CM_EntryPortal02_Walnut_BaseColor.png'
if any(p.exists() for p in [BLEND,FBX,ATLAS]) and '--refine-new-asset' not in sys.argv:raise RuntimeError('Refusing to overwrite existing asset')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1
mats={}
for key,col in [('Walnut',(.25,.15,.075,1)),('SoftEdge',(.28,.18,.10,1)),('Endgrain',(.22,.135,.07,1)),('Pegs',(.18,.10,.05,1))]:
 m=bpy.data.materials.new('Portal_'+key);m.diffuse_color=col;mats[key]=m
parts=[];part_notes={}
def P(x,y,z):return(x,z,y)
def mesh(name,vs,fs,key='Walnut',bevel=.005,origin=(0,0,0)):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);s.collection.objects.link(o);me.materials.append(mats[key]);me.materials.append(mats['SoftEdge'])
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();bpy.context.view_layer.objects.active=o
 if bevel:
  mod=o.modifiers.new('Controlled hand-hewn edge bevel','BEVEL');mod.width=bevel;mod.segments=2;mod.profile=.55;mod.affect='EDGES';mod.material=1;mod.harden_normals=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in o.data.polygons:p.use_smooth=True
 bm=bmesh.new();bm.from_mesh(o.data)
 for e in bm.edges:e.smooth=e.is_manifold and e.calc_face_angle()<math.radians(44)
 bm.to_mesh(o.data);bm.free()
 wn=o.modifiers.new('Weighted timber normals','WEIGHTED_NORMAL');wn.keep_sharp=True;wn.weight=40;bpy.ops.object.modifier_apply(modifier=wn.name)
 q=Vector(P(*origin))
 for v in o.data.vertices:v.co-=q
 o.location=q;o.data.update();parts.append(o);return o

def ruled_post(name,x):
 levels=[(.02,.145,0),(.12,.147,.002),(1.25,.144,-.003),(2.42,.146,.002),(2.52,.145,0)]
 vs=[]
 for y,w,drift in levels:
  for sx,sz in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(P(x+sx*w/2+drift,y,sz*.145/2+.002*math.sin(y*1.4)))
 fs=[(3,2,1,0),tuple(range(len(vs)-4,len(vs)))]+[(j*4+i,j*4+(i+1)%4,(j+1)*4+(i+1)%4,(j+1)*4+i) for j in range(len(levels)-1) for i in range(4)]
 o=mesh(name,vs,fs,bevel=.005,origin=(x,.02,0));part_notes[name]='2.50m post with <=3mm centreline irregularity; approved .145m section'
 return o

def box(name,p,d,key='Walnut',bevel=.004):
 x,y,z=p;a,b,c=[v/2 for v in d];vs=[P(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
 return mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],key,bevel,p)

def cap(name,x):
 # Stepped cap with a real concealed mortise for the arch springing.
 o=box(name,(x,2.55,0),(.23,.12,.21),bevel=.005)
 cutter=box('TEMP_Mortise',(x,2.545,0),(.084,.15,.104),bevel=0)
 bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Concealed mortise in cap','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);parts.remove(cutter);bpy.data.objects.remove(cutter,do_unlink=True)
 part_notes[name]='Cap .230x.120x.210m; concealed .084x.104m mortise, fitted .080x.100m tenon'
 return o

def sleeve(name,x):
 # Connected sleeve with sloped lip and open inner socket, matching the approved shoe bounds.
 outer=[(.035,.21),(.057,.21),(.295,.21),(.325,.196)];inner=[(.325,.154),(.068,.154)]
 vs=[]
 for y,w in outer+inner:
  for sx,sz in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(P(x+sx*w/2,y,sz*w/2))
 # outer rings 0..3; inner top ring4, inner lower ring5; close underside and socket bottom.
 fs=[]
 for r in range(3):
  for i in range(4):fs.append((r*4+i,r*4+(i+1)%4,(r+1)*4+(i+1)%4,(r+1)*4+i))
 for i in range(4):fs.append((12+i,12+(i+1)%4,16+(i+1)%4,16+i));fs.append((16+i,16+(i+1)%4,20+(i+1)%4,20+i))
 fs += [(3,2,1,0),(20,21,22,23)]
 o=mesh(name,vs,fs,bevel=.003,origin=(x,.035,0));part_notes[name]='Open fitted shoe sleeve; 4.5mm nominal radial clearance to post; no hidden solid block through stem';return o

def sweep(name,a,c,b,width,depth,z,segments):
 # Continuous four-sided arch, not intersecting short cubes.
 vs=[]
 for i in range(segments+1):
  t=i/segments;x=(1-t)**2*a[0]+2*(1-t)*t*c[0]+t*t*b[0];y=(1-t)**2*a[1]+2*(1-t)*t*c[1]+t*t*b[1]
  tangent=Vector((2*(1-t)*(c[0]-a[0])+2*t*(b[0]-c[0]),2*(1-t)*(c[1]-a[1])+2*t*(b[1]-c[1]))).normalized();n=Vector((-tangent.y,tangent.x))
  zz=z+.0025*math.sin(math.pi*t)
  for side,front in [(-1,-1),(1,-1),(1,1),(-1,1)]:vs.append(P(x+n.x*side*width/2,y+n.y*side*width/2,zz+front*depth/2))
 fs=[(3,2,1,0),tuple(range(len(vs)-4,len(vs)))]+[(r*4+i,r*4+(i+1)%4,(r+1)*4+(i+1)%4,(r+1)*4+i) for r in range(segments) for i in range(4)]
 o=mesh(name,vs,fs,bevel=.004 if width>.1 else .002,origin=(0,a[1],z));part_notes[name]=dict(curve=[a,c,b],section=[width,depth],segments=segments,front_bow_max=.0025);return o

def peg(name,x):
 # Modest tapered wooden dowel, seated in the front cap surface.
 vs=[]
 for z,r in [(.077,.012),(.116,.0115)]:
  for i in range(8):a=i*math.tau/8;vs.append(P(x+math.cos(a)*r,2.55+math.sin(a)*r,z))
 fs=[tuple(range(7,-1,-1)),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
 return mesh(name,vs,fs,'Pegs',.001,(x,2.55,.105))

for side,x in [('L',-1.1),('R',1.1)]:
 ruled_post('01_Post_'+side,x);sleeve('02_BaseShoe_'+side,x);cap('03_PostCap_'+side,x)
 box('06_ConcealedTenon_'+side,(x,2.53,0),(.080,.13,.100),bevel=.001)
 peg('07_JoineryPeg_'+side,x)
sweep('04_ContinuousOuterArch',(-1.1,2.5),(0,3.34),(1.1,2.5),.16,.16,0,28)
sweep('05_ContinuousInnerTrim',(-.97,2.4),(0,3.10),(.97,2.4),.055,.055,.08,26)
# Mark end-grain faces while preserving bevel material slots.
for o in parts:
 o.data.materials.append(mats['Endgrain'])
 if o.name.startswith(('01_','06_')):
  for p in o.data.polygons:
   if abs(p.normal.z)>.92 and p.material_index==0:p.material_index=2
# Unique packed UV atlas with area-normalized islands.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.004);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.004);bpy.ops.object.mode_set(mode='OBJECT')
# Store geometry/UV fingerprint before paint transfer.
def fingerprint(o):return hashlib.sha256(json.dumps({'v':[tuple(v.co) for v in o.data.vertices],'f':[tuple(p.vertices) for p in o.data.polygons],'uv':[tuple(v.uv) for v in o.data.uv_layers[0].data],'matrix':[list(row) for row in o.matrix_world]}).encode()).hexdigest()
before={o.name:fingerprint(o) for o in parts}
source=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png';paint=bpy.data.images.load(str(source));paint.colorspace_settings.name='sRGB'
for key,m in mats.items():
 m.use_nodes=True;nodes=m.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);uv=nodes.new('ShaderNodeUVMap');uv.uv_map='PaintProjection';tex=nodes.new('ShaderNodeTexImage');tex.image=paint;tex.extension='EXTEND';m.node_tree.links.new(uv.outputs[0],tex.inputs['Vector'])
 # Broad brushwork from approved walnut, with restrained bevel/endgrain contrast only.
 mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;v={'Walnut':1.0,'SoftEdge':1.065,'Endgrain':.93,'Pegs':.83}[key];mix.inputs[2].default_value=(v,v,v,1);m.node_tree.links.new(tex.outputs['Color'],mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],em.inputs['Color'])
# Physical paint scale: same walnut patch scale as the approved modules; grain follows arch arc length.
for oi,o in enumerate(parts):
 uv=o.data.uv_layers.new(name='PaintProjection');coords=[o.matrix_world@v.co for v in o.data.vertices];center=sum(coords,Vector())/len(coords);dims=[max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3)];long=max(range(3),key=lambda i:dims[i]);across=next(i for i in [0,1,2] if i!=long and dims[i]==max(dims[j] for j in range(3) if j!=long))
 curve=part_notes.get(o.name);samples=[]
 if isinstance(curve,dict):
  a,c,b=curve['curve'];length=0;previous=None
  for i in range(257):
   t=i/256;p=Vector(((1-t)**2*a[0]+2*(1-t)*t*c[0]+t*t*b[0],(1-t)**2*a[1]+2*(1-t)*t*c[1]+t*t*b[1]))
   if previous is not None:length+=(p-previous).length
   samples.append((p,length));previous=p
 for p in o.data.polygons:
  for li in p.loop_indices:
   v=coords[o.data.loops[li].vertex_index]
   if samples:
    point=Vector((v.x,v.z));near=min(samples,key=lambda q:(q[0]-point).length_squared);u=.5+(point-near[0]).length/.85;w=.10+near[1]/3.6
   else:u=.5+(v[across]-center[across])/.85;w=.12+(v[long]-min(x[long] for x in coords))/3.6
   u=max(.03,min(.97,u+((oi*7)%9)*.008));w=max(.03,min(.97,w+((oi*3)%7)*.008));uv.data[li].uv=(.512+.476*u,.512+.476*w)
 o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
# Bake into the unique production atlas; no lighting, AO, shader noise or blur.
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in parts:c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();receiver=bpy.context.object
atlas=bpy.data.images.new('CM_EntryPortal02_Walnut_BaseColor',width=2048,height=2048,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(ATLAS);atlas.file_format='PNG'
for m in receiver.data.materials:
 n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=atlas;m.node_tree.nodes.active=n;n.select=True
s.render.bake.margin=8;s.render.bake.use_clear=True;bpy.ops.object.bake(type='EMIT');atlas.save();bpy.data.objects.remove(receiver,do_unlink=True)
for o in parts:o.data.uv_layers.remove(o.data.uv_layers['PaintProjection']);o.data.uv_layers.active_index=0
assert before=={o.name:fingerprint(o) for o in parts},'Paint transfer changed UV0/geometry'
for m in mats.values():
 nodes=m.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');bs=nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=1;bs.inputs['Metallic'].default_value=0;tex=nodes.new('ShaderNodeTexImage');tex.image=atlas;m.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(bs.outputs[0],out.inputs['Surface'])
paint.pack();atlas.pack()
# Reusable attachment reference empties, also emitted as explicit Unity-local JSON.
sockets=[('OpeningCenter',(0,1.3,0),(0,0,0),'Clear portal opening; no door is installed here'),('DoorModule_RearRecess',(0,-.20,-3.32),(0,0,0),'Existing approved door module root, 3.32m behind portal'),('SignBoard',(0,3.44,.38),(0,180,0),'Existing sign backing center; replaceable separate assembly'),('Sign_WallBracket',(0,4.13,-1.34),(0,180,0),'Requires support from existing wall/canopy, not the arch'),('Lantern_ReferenceLeft',(1.25,2.08,.16),(0,180,0),'Approved west lantern body center'),('Lantern_ReferenceRight',(-1.25,2.30,.09),(0,180,0),'Approved east lantern body center'),('Herb_PortalLeft',(.97,2.40,.15),(0,180,0),'Keep bundles outside the central head clearance'),('Herb_PortalRight',(-.97,2.40,.15),(0,180,0),'Keep bundles outside the central head clearance')]
for i in range(5):sockets.append((f'Herb_CanopyLine_{i+1:02d}',(3.21-i*.37,2.72,-.07),(0,180,0),'Existing shop canopy hook; outside the portal span'))
for name,pos,rot,note in sockets:
 e=bpy.data.objects.new('Socket_'+name,None);s.collection.objects.link(e);e.location=P(*pos);e.empty_display_type='ARROWS';e.empty_display_size=.10;e['unity_local_euler']=json.dumps(rot);e['purpose']=note
(OUT/'AttachmentPoints.json').write_text(json.dumps([dict(name=n,position=p,rotation=r,purpose=t) for n,p,r,t in sockets],indent=2))
# Optional distance mesh: UV-preserving collapse of a joined copy, original logical parts retained.
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in parts:c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();lod=bpy.context.object;lod.name='90_DistanceMesh';mod=lod.modifiers.new('Distance-only reduction','DECIMATE');mod.ratio=.55;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
all_meshes=parts+[lod];report={'reference_scene':'CM_CrookedMortar_B_StyledDetails07','placement':{'position':[.85,.20,-5.52],'rotation_euler':[0,180,0],'scale':[1,1,1]},'atlas_size':[2048,2048],'paint_source':str(source),'paint_geometry_uv0_unchanged':True,'part_notes':part_notes,'parts':[]}
for o in all_meshes:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-10 for t in o.data.loop_triangles);assert bad==0 and volume>0 and deg==0,(o.name,bad,volume,deg)
 report['parts'].append(dict(name=o.name,triangles=len(o.data.loop_triangles),nonmanifold_edges=bad,degenerate_triangles=deg,signed_volume=volume))
report['lod0_triangles']=sum(x['triangles'] for x in report['parts'] if x['name']!='90_DistanceMesh');report['lod1_triangles']=report['parts'][-1]['triangles']
# Keep distance mesh hidden in editable source; export selection explicitly includes it.
lod.hide_set(True);lod.hide_render=True
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND));lod.hide_set(False);lod.hide_render=False
bpy.ops.object.select_all(action='DESELECT')
for o in all_meshes:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
conversion=Matrix.Rotation(math.pi,4,'Z')
for o in all_meshes:o.matrix_world=conversion@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(FBX),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(PAINT/'PaintTransferValidation.json').write_text(json.dumps(dict(source=str(source),source_packed_in_blend=True,atlas=str(ATLAS),atlas_resolution=2048,albedo_only=True,noise=False,uv0_unchanged_during_bake=True,padding_pixels=8),indent=2));print('PORTAL_READY',report['lod0_triangles'],report['lod1_triangles'])
