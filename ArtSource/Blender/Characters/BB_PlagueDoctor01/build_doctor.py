"""First-pass articulated storybook avatar. Unity coordinates: metres, +Z forward."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[3];A=R/'Assets/BlightBloom/Characters/PlagueDoctor01'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
image=bpy.data.images.load(str(A/'Textures/BB_Doctor_PaintedAtlas.png'));image.pack()
mat=bpy.data.materials.new('BB_Doctor_Painted');mat.use_nodes=True
bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1
tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=image;mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
parts=[]
def mesh(name,vs,fs,paint=0):
 me=bpy.data.meshes.new(name);me.from_pydata([(x,z,y) for x,y,z in vs],[],fs);me.update()
 o=bpy.data.objects.new(name,me);s.collection.objects.link(o);me.materials.append(mat)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 uv=me.uv_layers.new(name='PaintUV');lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
 for p in me.polygons:
  for li in p.loop_indices:
   v=vs[me.loops[li].vertex_index];u=(v[0]-lo[0])/max(.001,hi[0]-lo[0]);w=(v[1]-lo[1])/max(.001,hi[1]-lo[1])
   # PNG origin is top-left; material quadrant is selected explicitly.
   uv.data[li].uv=((paint%2)*.5+.025+u*.45,(1-paint//2)*.5+.025+w*.45)
 o['paintRegion']=paint;parts.append(o);return o
def loft(name,rings,paint=0,n=16):
 vs=[]
 for y,rx,rz,cx,cz in rings:
  for i in range(n):
   t=2*math.pi*i/n;vs.append((cx+rx*math.sin(t),y,cz+rz*math.cos(t)))
 fs=[tuple(reversed(range(n)))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]+[tuple((len(rings)-1)*n+i for i in range(n))]
 return mesh(name,vs,fs,paint)
def ell(name,c,scale,paint=0,n=12):
 x,y,z=c;rx,ry,rz=scale
 return loft(name,[(y+ry*math.sin(t),max(.004,rx*math.cos(t)),max(.004,rz*math.cos(t)),x,z) for t in [-math.pi/2,-math.pi/3,-math.pi/6,0,math.pi/6,math.pi/3,math.pi/2]],paint,n)
def box(name,c,size,paint=2):
 x,y,z=c;a,b,c=[k/2 for k in size];return mesh(name,[(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]],[(0,3,2,1),(4,5,6,7),(0,1,5,4),(3,7,6,2),(0,4,7,3),(1,2,6,5)],paint)
# Tall layered coat rather than a capsule body. Feet remain at zero; hat below 2m.
loft('Torso',[(.86,.205,.16,0,0),(1.12,.20,.145,0,0),(1.38,.28,.165,0,0),(1.48,.21,.13,0,0)],1)
loft('Underskirt',[(.28,.31,.23,0,0),(.33,.325,.24,0,0),(.93,.21,.16,0,0),(1.02,.20,.15,0,0)],1)
for side in [-1,1]:
 # Open coat tails: wedge cross-section, inner linen skirt remains visible.
 name='CoatL' if side<0 else 'CoatR';vs=[]
 for y,rx,rz in [(.31,.35,.255),(.56,.30,.23),(.85,.235,.18),(1.03,.215,.16)]:
  for i in range(10):
   t=side*(.17+(math.pi-.34)*i/9);vs.append((rx*math.sin(t),y,rz*math.cos(t)))
 fs=[(j*10+i,j*10+i+1,(j+1)*10+i+1,(j+1)*10+i) for j in range(3) for i in range(9)]
 o=mesh(name,vs,fs);sol=o.modifiers.new('Cloth thickness','SOLIDIFY');sol.thickness=.012;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
 arm='ArmL' if side<0 else 'ArmR'
 loft(arm,[(.91,.065,.067,side*.31,.035),(1.08,.09,.09,side*.34,0),(1.30,.10,.10,side*.28,0),(1.40,.075,.075,side*.235,0)],1)
 loft(arm,[(.81,.052,.055,side*.335,.045),(.92,.068,.069,side*.32,.035),(.98,.065,.07,side*.32,.025)],2)
 ell(arm,(side*.34,.76,.05),(.054,.095,.045),2)
 ell(arm,(side*.294,.79,.08),(.024,.05,.027),2)
 leg='LegL' if side<0 else 'LegR'
 loft(leg,[(.10,.074,.10,side*.125,.025),(.20,.078,.08,side*.125,0),(.43,.075,.07,side*.125,0),(.88,.07,.07,side*.125,0)],2)
 ell(leg,(side*.125,.09,.065),(.09,.09,.155),2)
 for y in [.21,.32]:
  box(leg,(side*.125,y,.075),(.14,.035,.035),2);box(leg,(side*.17,y,.10),(.045,.045,.017),3)
# Hood, wrapped scarf and shoulder cape.
loft('Body',[(1.40,.17,.13,0,-.01),(1.51,.19,.17,0,-.015),(1.72,.165,.16,0,-.025),(1.84,.12,.125,0,-.03)],0)
loft('Body',[(1.24,.335,.205,0,-.01),(1.27,.34,.21,0,-.01),(1.42,.29,.18,0,0),(1.49,.17,.14,0,0)],0)
loft('Body',[(1.43,.185,.16,0,.01),(1.48,.205,.17,0,.005),(1.53,.18,.16,0,0)],0)
# Ivory mask with a long gracefully curving beak, not a cone stuck on a sphere.
ell('Head',(0,1.675,.105),(.126,.155,.105),1,16)
vs=[]
for z,y,w,h in [(.135,1.65,.102,.105),(.23,1.62,.09,.080),(.32,1.565,.055,.043),(.38,1.51,.006,.008)]:
 for x,yy in [(-w,y),(-w*.55,y+h),(w*.55,y+h),(w,y),(w*.6,y-h),(0,y-h*.8),(-w*.6,y-h)]:vs.append((x,yy,z))
mesh('Head',vs,[tuple(reversed(range(7)))]+[(j*7+i,j*7+(i+1)%7,(j+1)*7+(i+1)%7,(j+1)*7+i) for j in range(3) for i in range(7)]+[tuple(range(21,28))],1)
# Raised aged-gold lens rims with dark inset lenses, plus narrow mask seam.
for side in [-1,1]:
 ell('Head',(side*.073,1.715,.191),(.048,.054,.026),3,16)
 ell('Head',(side*.073,1.716,.213),(.035,.041,.013),2,16)
 ell('Head',(side*.062,1.732,.224),(.008,.011,.004),1,8)
# Broad crooked brim and low dented crown.
loft('Hat',[(1.823,.405,.31,0,-.018),(1.845,.412,.315,0,-.018),(1.866,.19,.16,-.01,-.02)],2,24)
loft('Hat',[(1.85,.185,.16,-.01,-.02),(1.92,.17,.145,-.02,-.03),(1.985,.12,.105,-.045,-.025),(1.992,.10,.08,-.055,-.02)],2,16)
loft('Hat',[(1.855,.187,.162,-.01,-.02),(1.89,.18,.155,-.014,-.025)],3,16)
# Leather belt, satchel, straps, buttons, small herb vials and hat botanicals.
loft('Body',[(1.005,.223,.17,0,0),(1.06,.217,.166,0,0)],2)
box('Body',(0,1.034,.177),(.075,.062,.025),3)
box('Body',(.24,.91,-.13),(.19,.23,.12),2);box('Body',(.24,1.015,-.145),(.20,.055,.13),2)
box('Body',(.24,.92,-.21),(.025,.095,.016),3)
for i in range(3):
 x=-.15+i*.063;loft('Body',[(.86,.019,.019,x,.175),(.95,.021,.021,x,.175),(.975,.015,.015,x,.175)],1,8);box('Body',(x,.98,.175),(.03,.025,.034),2)
for x,y,z in [(-.19,1.90,.20),(-.23,1.88,.18),(-.26,1.87,.16)]:
 ell('Hat',(x,y,z),(.038,.014,.018),0,8)
ell('Hat',(-.20,1.90,.22),(.023,.020,.012),3,8)
# Join by articulated region: few renderers, all source parts remain editable in blend.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'BB_PlagueDoctor01.blend'))
groups={name:[o for o in parts if o.name.split('.')[0]==name] for name in set(o.name.split('.')[0] for o in parts)}
for name,selected in sorted(groups.items()):
 bpy.ops.object.select_all(action='DESELECT')
 for o in selected:o.select_set(True)
 bpy.context.view_layer.objects.active=selected[0]
 if len(selected)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=name;o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
checks=[]
for o in list(s.objects):
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free()
 checks.append(dict(name=o.name,triangles=len(o.data.loop_triangles),nonManifoldEdges=bad,positiveVolume=vol>0,uv0=len(o.data.uv_layers)>0))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=str(A/'Models/BB_PlagueDoctor01.fbx'),use_selection=True,object_types={'MESH'},axis_forward='-Z',axis_up='Y',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'MeshValidation.json').write_text(json.dumps(checks,indent=2));print('DOCTOR_EXPORT_OK',sum(c['triangles'] for c in checks))
