"""Painted presentation overlay for unchanged study 05 B; no collision/gameplay sources edited."""
import bpy,math,json,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/StyledProof06'
FBX=ASSET/'Models/CM_B_StyledProof06.fbx';BLEND=OUT/'CM_B_StyledProof06.blend';ATLAS=ASSET/'Textures/CM_B_StyledAtlas06.png'
if (FBX.exists() or BLEND.exists()) and '--refine-created-proof' not in sys.argv:raise RuntimeError('Refusing overwrite')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'ArtSource/Blender/Architecture/CrookedMortar/MassingRefinements05/CM_Refinement05_B.blend'))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];original=list(objects)
def geom(o):return hashlib.sha256(json.dumps({'v':[tuple(v.co) for v in o.data.vertices],'f':[tuple(p.vertices) for p in o.data.polygons],'m':[list(x) for x in o.matrix_world]}).encode()).hexdigest()
before={o.name:geom(o) for o in original}
# Preserve underlying architecture: all new shape work is non-colliding dressing.
mats={k:bpy.data.materials.new('Dress_'+k) for k in ['Timber','Slate0','Slate1','Slate2','Stone','Soil','Terracotta']}
new=[]
def P(x,y,z):return(x,z,y)
def mesh(n,vs,fs,k):
 m=bpy.data.meshes.new(n);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(n,m);bpy.context.scene.collection.objects.link(o);m.materials.append(mats[k]);new.append(o);return o
def box(n,p,d,k):
 x,y,z=p;a,b,c=[v/2 for v in d];vs=[P(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
 return mesh(n,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],k)
def beam(n,a,b,w=.15):
 a,b=Vector(P(*a)),Vector(P(*b));v=b-a;bpy.ops.mesh.primitive_cube_add(size=1,location=(a+b)/2);o=bpy.context.object;o.name=n;o.dimensions=(w,w,v.length);o.rotation_euler=v.to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.data.materials.append(mats['Timber']);new.append(o);return o
# Restrained timber-frame composition follows real wall/floor edges and keeps door/window apertures.
for x in [-2.8,1.85]:beam('Dress_TimberFrontPost',(x,3.44,-4.20),(x,6.25,-4.20),.18)
for y in [3.50,6.25]:beam('Dress_TimberFrontPlate',(-2.8,y,-4.20),(1.85,y,-4.20),.18)
beam('Dress_PairedWindowPost',(-.46,4.48,-4.24),(-.46,6.28,-4.24),.12)
for a,b in [((-2.72,3.65,-4.2),(-1.62,4.5,-4.2)),((1.78,3.65,-4.2),(.68,4.5,-4.2))]:beam('Dress_JettyBrace',a,b,.17)
for z in [-3.9,.70]:beam('Dress_RightFacadePost',(1.98,3.44,z),(1.98,6.24,z),.17)
for y in [3.49,6.20]:beam('Dress_RightFacadePlate',(1.98,y,-3.95),(1.98,y,.8),.17)
beam('Dress_RightDiagonal',(1.98,3.65,.75),(1.98,4.48,-.05),.18)
for y in [3.48,5.88]:beam('Dress_WingFrontPlate',(2.1,y,1.20),(3.95,y,1.42),.14)
for x,z in [(2.1,1.20),(3.95,1.42)]:beam('Dress_WingFrontPost',(x,.55,z),(x,5.9,z),.16)
for y in [.58,3.38,5.85]:beam('Dress_WingSidePlate',(4.08,y,1.55),(4.08,y,4.85),.15)
for z in [1.6,3.6,4.8]:beam('Dress_WingSidePost',(4.08,.5,z),(4.08,5.9,z),.15)
beam('Dress_WingSideBrace',(4.08,3.6,4.70),(4.08,4.8,3.65),.16)
# Shallow foundation stones, chimney joints and window boxes are presentation geometry only.
for x,z,length,axis in [(0,-3.28,4.2,'X'),(3.32,-.65,3.1,'Z'),(4.1,3.2,3.1,'Z')]:
 for row in range(2):
  for i in range(int(length/.48)):
   t=-length/2+(i+.5)*.48+.10*(row%2)
   box('Dress_FoundationStone',(x+t,.20+row*.20,z) if axis=='X' else(x,.20+row*.20,z+t),(.45,.185,.12) if axis=='X' else(.12,.185,.45),'Stone')
for z in [-4.29]:
 box('Dress_FrontWindowBox',(-.46,4.35,z-.10),(2.10,.26,.38),'Timber');box('Dress_FrontWindowSoil',(-.46,4.49,z-.10),(1.98,.025,.27),'Soil')
box('Dress_SideWindowBox',(2.10,4.20,-.9),(.38,.24,1.65),'Timber')
box('Dress_WingWindowBox',(3.03,3.90,1.17),(1.45,.24,.36),'Timber')
for y in [6.3+i*.48 for i in range(9)]:
 for x in [1.70,2.0,2.30]:box('Dress_ChimneyJoint',(x,y,4.492),(.27,.018,.012),'Stone')
# Tile surfaces are sampled against the unchanged model, clipped at dormer/intersecting roofs.
s=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();tilevs=[[],[],[]];tilefs=[[],[],[]]
def warped(p):
 x,y,z=p
 if x>2.1 and z>.85:z+=.20*min(1,(x-2.1)/(3.95-2.1))*max(0,min(1,(4.9-z)/(4.9-1.35)))
 return Vector(P(x,y,z))
def patch(n,fn,ulen,vlen):
 nu=max(1,math.ceil(ulen/.32));nv=max(1,math.ceil(vlen/.42))
 for i in range(nu):
  for j in range(nv):
   u0=i/nu;u1=min(1,(i+1.08)/nu);v0=(j+.035)/nv;v1=min(1,(j+.965)/nv)
   pts=[fn(u,v) for u,v in [(u0,v0),(u1,v0),(u1,v1),(u0,v1)]]
   normal=(pts[1]-pts[0]).cross(pts[3]-pts[0]).normalized()
   reverse=normal.z<0
   if reverse:normal=-normal
   visible=True;projected=[]
   for p in pts+[sum(pts,Vector())/4]:
    hit,loc,no,fi,obj,ma=s.ray_cast(dg,p+normal*.35,-normal,distance=.70)
    if not hit or not obj.name.startswith('Roof_') or (loc-p).length>.18:visible=False;break
    if len(projected)<4:projected.append(loc)
   if not visible:continue
   pts=projected
   k=(i*3+j*5)%3;ids=[]
   for pi,p in enumerate(pts):
    lower=(pi in [0,3]) if pts[1].z>pts[0].z else (pi in [1,2])
    ids.append(len(tilevs[k]));tilevs[k].append(tuple(p+normal*(.025+(.028 if lower else 0))))
   tilefs[k].append(tuple(reversed(ids)) if reverse else tuple(ids))
def tiledroof(n,axis,profile,a,b,hero=False):
 for (u,h),(v,j) in zip(profile,profile[1:]):
  length=math.hypot(v-u,j-h)
  def fn(t,q):
   c=u+(v-u)*t;d=a+(b-a)*q
   fall=.4*max(0,min(1,(d+4.05)/5.18)) if hero else 0
   hh=h-fall if h>9 else h;jj=j-fall if j>9 else j;y=hh+(jj-hh)*t
   return warped((c,y,d) if axis=='Z' else(d,y,c))
  patch(n,fn,length,b-a)
tiledroof('Hero','Z',[(-3.22,6.03),(-2.75,6.48),(-1.80,9.25),(-1.05,10.40),(-.40,9.63),(1.77,6.58),(2.33,6.08)],-4.40,1.13,True)
tiledroof('Rear','X',[(.50,6.20),(1.05,6.5),(3.10,8.55),(5.5,6.2)],-2.48,2.48)
tiledroof('Wing','X',[(1.0,6.02),(1.45,6.35),(2.875,7.55),(4.8,6.35),(5.25,5.99)],1.80,4.30)
for vs in [ [(-.25,4.4,-4),(2.30,4.28,-4),(2.30,3.15,-5.8),(-.25,3.25,-5.8)], [(-3.15,4.1,-4),(0,4.1,-4),(0,3.05,-5.35),(-3.15,3.16,-5.35)], [(2.0,4.3,-2.65),(2.0,4.3,1.47),(3.55,3.3,1.47),(3.55,3.3,-2.65)] ]:
 p0,p1,p2,p3=[Vector(v) for v in vs]
 patch('Canopy',lambda u,v:warped(tuple(p0*(1-u)*(1-v)+p1*u*(1-v)+p2*u*v+p3*(1-u)*v)),(p1-p0).length,(p3-p0).length)
for k in range(3):
 if tilevs[k]:mesh('Dress_OverlappingSlate_'+str(k),tilevs[k],tilefs[k],'Slate'+str(k))
# Join dressing by material to keep scene hierarchy compact.
by={}
for o in new:by.setdefault(o.data.materials[0].name,[]).append(o)
for k,items in by.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in items:o.select_set(True)
 bpy.context.view_layer.objects.active=items[0]
 if len(items)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=k+'_PresentationOnly';objects.append(o)
assert before=={o.name:geom(o) for o in original},'Underlying B mesh changed'
# UV changes occur only in this new render copy; original model/collision meshes remain untouched.
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.002);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.0015);bpy.ops.object.mode_set(mode='OBJECT')
source=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png';image=bpy.data.images.load(str(source));image.colorspace_settings.name='sRGB'
used=set(m for o in objects for m in o.data.materials if m)
for mat in used:
 key=mat.name.replace('Study05_','').replace('Dress_','');mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');mat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 paintkey='Slate' if key=='Roof' or key.startswith('Slate') else key
 if paintkey in ['Plaster','Timber','Slate','Stone','Terracotta']:
  uvn=nodes.new('ShaderNodeUVMap');uvn.uv_map='PaintProjection';frac=nodes.new('ShaderNodeVectorMath');frac.operation='FRACTION';mat.node_tree.links.new(uvn.outputs[0],frac.inputs[0]);mul=nodes.new('ShaderNodeVectorMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=(.476,.476,1);mat.node_tree.links.new(frac.outputs[0],mul.inputs[0]);add=nodes.new('ShaderNodeVectorMath');add.operation='ADD';x,y=(.5,0) if paintkey=='Slate' else((.5,.5) if paintkey=='Timber' else(0,.5));add.inputs[1].default_value=(x+.012,y+.012,0);mat.node_tree.links.new(mul.outputs[0],add.inputs[0]);tex=nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';mat.node_tree.links.new(add.outputs[0],tex.inputs['Vector']);mat.node_tree.links.new(tex.outputs['Color'],em.inputs['Color'])
  if paintkey in ['Slate','Stone']:
   mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=({'Roof':(.64,.72,.68,1),'Slate0':(.86,.91,.83,1),'Slate1':(.73,.81,.78,1),'Slate2':(.91,.95,.86,1)}.get(key,(.80,.87,.80,1))) if paintkey=='Slate' else(.57,.64,.57,1);mat.node_tree.links.new(tex.outputs['Color'],mix.inputs[1]);mat.node_tree.links.new(mix.outputs[0],em.inputs['Color'])
 else:em.inputs['Color'].default_value=(.39,.21,.055,1) if key=='Glass' else(.11,.085,.05,1)
for oi,o in enumerate(objects):
 uv=o.data.uv_layers.new(name='PaintProjection')
 for p in o.data.polygons:
  key=o.data.materials[p.material_index].name.replace('Study05_','').replace('Dress_','');norm=o.matrix_world.to_3x3()@p.normal
  pts=[o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co for li in p.loop_indices];direction=max((pts[(i+1)%len(pts)]-pts[i] for i in range(len(pts))),key=lambda v:v.length).normalized();across=norm.cross(direction).normalized()
  for li in p.loop_indices:
   v=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   if key in ['Plaster','Stone']:u=(v.x if abs(norm.y)>=abs(norm.x) else v.y)/3.8;w=v.z/4.0
   elif key=='Roof' or key.startswith('Slate'):u=v.x/3.2+.08*(oi%3);w=v.y/3.2
   else:u=v.dot(across)/.8;w=v.dot(direction)/3.6
   uv.data[li].uv=(u,w)
 o.data.uv_layers.active_index=0;o.data.uv_layers[0].active_render=True
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in objects:
 c=o.copy();c.data=o.data.copy();bpy.context.scene.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();receiver=bpy.context.object
atlas=bpy.data.images.new('CM_B_StyledAtlas06',width=4096,height=4096,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(ATLAS);atlas.file_format='PNG'
for mat in receiver.data.materials:
 node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=atlas;node.select=True;mat.node_tree.nodes.active=node
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;s.render.bake.margin=12;s.render.bake.use_clear=True;bpy.ops.object.bake(type='EMIT');atlas.save();bpy.data.objects.remove(receiver,do_unlink=True)
for o in objects:o.data.uv_layers.remove(o.data.uv_layers['PaintProjection']);o.data.uv_layers.active_index=0
for mat in used:
 key=mat.name.replace('Study05_','').replace('Dress_','');nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');bs=nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=1;tex=nodes.new('ShaderNodeTexImage');tex.image=atlas;mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);mat.node_tree.links.new(bs.outputs[0],out.inputs['Surface']);mat.name='ProofPainted_'+key
image.pack();atlas.pack()
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
for o in objects:o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.ops.export_scene.fbx(filepath=str(FBX),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(OUT/'GeometryPaintValidation.json').write_text(json.dumps(dict(base='CM_Refinement05_B',original_vertices_faces_transforms_unchanged=True,original_meshes=len(original),presentation_meshes=len(objects)-len(original),slate_tiles=sum(len(f) for f in tilefs),paint_source=str(source),bake='Albedo only; approved brushwork, no baked lighting/AO',atlas_size=4096),indent=2));print('STYLED_PROOF_READY')
