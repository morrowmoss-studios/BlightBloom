"""Skinned, generic-rig successor. Preserves the original source, FBX and prefab."""
import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Characters/PlagueDoctor01/Rigged02'
bpy.ops.wm.open_mainfile(filepath=str(D.parent/'BB_PlagueDoctor01.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.render.fps=30;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
mat=bpy.data.materials.get('BB_Doctor_Painted');parts=[]
# Original mesh helper retains approved palette/UV regions. New topology is purpose-built for bending.
tree=ast.parse((D.parent/'build_doctor.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['mesh','loft','ell','box']],type_ignores=[]),'<approved mesh helpers>','exec'),globals())
for o in list(s.objects):
 if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True);continue
 if o.name.startswith(('Arm','Leg','Coat','Torso','Underskirt')) or o.name=='Body.001':bpy.data.objects.remove(o,do_unlink=True)
# Coordinates remain Unity metres (x, up, forward), stored as Blender (x, forward, up).
def tube(name,rings,paint=0,n=24):
 dense=[]
 for j in range(len(rings)-1):
  a,b=rings[j],rings[j+1]
  for k in range(3):dense.append(tuple(a[i]+(b[i]-a[i])*k/3 for i in range(5)))
 dense.append(rings[-1]);return loft(name,dense,paint,n)
newroles={}
def role(o,key):newroles[o.name]=key;return o
role(tube('TailoredTorso',[(.92,.195,.145,0,0),(1.06,.205,.15,0,0),(1.20,.225,.155,0,0),(1.36,.255,.155,0,0),(1.44,.23,.145,0,0),(1.48,.155,.12,0,0)],1,28),'torso')
for side,tag in [(-1,'L'),(1,'R')]:
 # Continuous sleeve with elbow support loops and gentle rest bend.
 role(tube('Sleeve'+tag,[(.89,.06,.065,side*.335,.065),(1.00,.072,.075,side*.33,.035),(1.095,.085,.082,side*.32,.005),(1.13,.086,.083,side*.315,0),(1.17,.089,.086,side*.305,-.005),(1.30,.103,.095,side*.27,-.008),(1.40,.095,.09,side*.235,-.005),(1.455,.055,.065,side*.215,0)],1,24),'arm'+tag)
 role(tube('Glove'+tag,[(.73,.047,.04,side*.34,.08),(.79,.055,.045,side*.34,.078),(.86,.054,.048,side*.335,.07),(.95,.065,.063,side*.332,.05)],2,24),'arm'+tag)
 role(ell('Thumb'+tag,(side*.294,.80,.10),(.024,.053,.028),2,16),'hand'+tag)
 role(tube('Trousers'+tag,[(.24,.07,.07,side*.125,0),(.40,.075,.073,side*.125,-.012),(.48,.080,.077,side*.125,.004),(.52,.081,.078,side*.125,.01),(.56,.084,.08,side*.125,.005),(.72,.09,.085,side*.125,0),(.94,.095,.085,side*.125,0)],2,24),'leg'+tag)
 role(tube('BootShaft'+tag,[(.09,.075,.09,side*.125,.02),(.16,.077,.084,side*.125,.01),(.24,.080,.077,side*.125,0),(.34,.082,.079,side*.125,-.005)],2,24),'boot'+tag)
 role(ell('BootToe'+tag,(side*.125,.085,.085),(.09,.078,.155),2,24),'foot'+tag)
 # Low rounded sole with a clean ground datum.
 role(loft('Sole'+tag,[(.008,.075,.135,side*.125,.08),(.018,.091,.155,side*.125,.08),(.045,.09,.154,side*.125,.08),(.057,.083,.145,side*.125,.08)],2,28),'foot'+tag)
 for y in [.20,.30]:
  role(box('LeatherBootBand'+tag,(side*.125,y,.075),(.145,.027,.025),2),'boot'+tag)
  o=role(box('BootBuckle'+tag,(side*.17,y,.092),(.04,.038,.016),3),'boot'+tag)
 # Split front panels and back panels with vertical topology supporting cloth bones.
 for back in [False,True]:
  name=('CoatBack' if back else 'CoatFront')+tag;vs=[];nr=13;nc=17
  for j in range(nr):
   f=j/(nr-1);y=.36+.66*f;rx=.375-(.375-.215)*f;rz=.285-(.285-.16)*f
   for i in range(nc):
    u=i/(nc-1);theta=side*((math.pi/2 if back else .21)+(math.pi/2-.21)*u)
    # A slightly lifted front cutaway permits the legs to clear the hem.
    yy=y+(0 if back else .15*(1-f)**2*(1-u)**3)
    ripple=1+.025*math.cos(theta*7+.4)*(1-f)
    vs.append((rx*math.sin(theta)*ripple,yy,rz*math.cos(theta)*ripple))
  fs=[(j*nc+i,j*nc+i+1,(j+1)*nc+i+1,(j+1)*nc+i) for j in range(nr-1) for i in range(nc-1)]
  o=role(mesh(name,vs,fs,0),'cloth'+('Back' if back else 'Front')+tag)
  sol=o.modifiers.new('Tailored cloth thickness','SOLIDIFY');sol.thickness=.009;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
 # Inner linen follows separate soft coat weights, also split rather than a rigid tube.
 vs=[];nr=11;nc=15
 for j in range(nr):
  f=j/(nr-1)
  for i in range(nc):
   t=side*(math.pi*i/(nc-1));y=.34+.66*f+.16*(1-f)**2*max(0,math.cos(t))**5
   vs.append(((.315-.12*f)*math.sin(t),y,(.238-.09*f)*math.cos(t)))
 o=role(mesh('LinenSkirt'+tag,vs,[(j*nc+i,j*nc+i+1,(j+1)*nc+i+1,(j+1)*nc+i) for j in range(nr-1) for i in range(nc-1)],1),'linen'+tag)
 sol=o.modifiers.new('Linen thickness','SOLIDIFY');sol.thickness=.007;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
# Rounded shoulder mantle: curved contour rather than straight bucket-like cape.
vs=[];nr=8;nc=40
for j in range(nr):
 f=j/(nr-1)
 for i in range(nc):
  t=2*math.pi*i/nc;rx=.17+.165*f;rz=.135+.075*f;edge=1.23+.065*math.sin(t)**2
  vs.append((rx*math.sin(t),1.49+(edge-1.49)*f,rz*math.cos(t)))
o=role(mesh('ShoulderMantle',vs,[(j*nc+i,j*nc+(i+1)%nc,(j+1)*nc+(i+1)%nc,(j+1)*nc+i) for j in range(nr-1) for i in range(nc)],0),'mantle');sol=o.modifiers.new('Mantle thickness','SOLIDIFY');sol.thickness=.012;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
# Smooth normals and controlled bevels on hard accessories. No global subdivision.
for o in list(s.objects):
 if o.type!='MESH':continue
 if not o.data.uv_layers:raise RuntimeError('Missing UV '+o.name)
 if len(o.data.polygons)<=6:
  bevel=o.modifiers.new('Soft leather edges','BEVEL');bevel.width=.004;bevel.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bevel.name)
 for p in o.data.polygons:p.use_smooth=True
 o.data.set_sharp_from_angle(angle=math.radians(48))
# Skeleton (deformation bones and reusable interaction-ready joints).
arm=bpy.data.armatures.new('BB_Doctor_Skeleton');rig=bpy.data.objects.new('BB_DoctorRig',arm);s.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
bones={}
def P(v):return Vector((v[0],v[2],v[1]))
def bone(name,head,tail,parent=None):
 b=arm.edit_bones.new(name);b.head=P(head);b.tail=P(tail)
 if parent:b.parent=arm.edit_bones[parent]
 bones[name]=(head,tail,parent)
 return b
bone('Root',(0,0,0),(0,.18,0));bone('Hips',(0,.96,0),(0,1.10,0),'Root');bone('Spine',(0,1.10,0),(0,1.28,0),'Hips');bone('Chest',(0,1.28,0),(0,1.46,0),'Spine');bone('Neck',(0,1.46,0),(0,1.57,0),'Chest');bone('Head',(0,1.57,0),(0,1.88,0),'Neck')
for side,tag in [(-1,'L'),(1,'R')]:
 bone('Shoulder'+tag,(0,1.42,0),(side*.235,1.39,0),'Chest');bone('UpperArm'+tag,(side*.235,1.39,0),(side*.315,1.13,0),'Shoulder'+tag);bone('Forearm'+tag,(side*.315,1.13,0),(side*.335,.90,.06),'UpperArm'+tag);bone('Hand'+tag,(side*.335,.90,.06),(side*.34,.74,.08),'Forearm'+tag)
 bone('Thigh'+tag,(side*.125,.94,0),(side*.125,.51,.015),'Hips');bone('Shin'+tag,(side*.125,.51,.015),(side*.125,.15,0),'Thigh'+tag);bone('Foot'+tag,(side*.125,.15,0),(side*.125,.09,.20),'Shin'+tag);bone('Toe'+tag,(side*.125,.09,.20),(side*.125,.06,.25),'Foot'+tag)
 for back in [False,True]:bone(('CoatBack' if back else 'CoatFront')+tag,(side*.14,.98,-.10 if back else .10),(side*.28,.36,-.22 if back else .22),'Hips')
bone('Satchel',(.24,1.02,-.12),(.24,.79,-.13),'Hips')
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
# Smooth, explicit weights; no automatic proximity weights pulling sleeves onto the torso.
def mix(a,b,t):return {a:1-max(0,min(1,t)),b:max(0,min(1,t))}
checks=[]
for o in list(s.objects):
 if o.type!='MESH':continue
 rolekey=newroles.get(o.name,'original');groups={}
 for v in o.data.vertices:
  x,z,y=v.co;tag='L' if x<0 else 'R'
  if rolekey.startswith('arm'):
   tag=rolekey[-1]
   if y>1.20:w={'UpperArm'+tag:1}
   elif y>.99:w=mix('Forearm'+tag,'UpperArm'+tag,(y-1.06)/.14)
   else:w=mix('Hand'+tag,'Forearm'+tag,(y-.86)/.12)
  elif rolekey.startswith('hand'):w={'Hand'+rolekey[-1]:1}
  elif rolekey.startswith('leg'):
   tag=rolekey[-1];w=mix('Shin'+tag,'Thigh'+tag,(y-.43)/.16)
  elif rolekey.startswith('boot'):
   tag=rolekey[-1];w=mix('Foot'+tag,'Shin'+tag,(y-.17)/.12)
  elif rolekey.startswith('foot'):w={'Foot'+rolekey[-1]:1}
  elif rolekey.startswith('cloth') or rolekey.startswith('linen'):
   n=rolekey[5:] if rolekey.startswith('cloth') else ('Front' if z>0 else 'Back')+rolekey[-1]
   strength=max(0,min(.95,(1.02-y)/.55))
   if rolekey.startswith('linen'):strength*=min(1,abs(x)/.12)
   secondary=.35*min(1,abs(z)/.08)
   w={'Hips':1-strength,'Coat'+n:strength*secondary,'Thigh'+n[-1]:strength*(1-secondary)}
  elif rolekey=='torso':w=mix('Hips','Chest',(y-1.04)/.34)
  elif rolekey=='mantle':w=mix('Chest','UpperArm'+tag,max(0,(abs(x)-.18)/.20)*.28)
  elif o.name.startswith(('Head','Hat')) or y>1.53:w={'Head':1}
  elif y>1.23:w={'Chest':1}
  elif x>.13 and z<-.07 and y<1.08:w={'Satchel':1}
  else:w={'Hips':1}
  for key,value in w.items():
   if value>.00001:
    if key not in groups:groups[key]=o.vertex_groups.new(name=key)
    groups[key].add([v.index],value,'REPLACE')
 o.parent=rig;mod=o.modifiers.new('Skeletal skin','ARMATURE');mod.object=rig
 o.data.calc_loop_triangles();checks.append(dict(mesh=o.name,triangles=len(o.data.loop_triangles),uv0=True,weightedVertices=len(o.data.vertices)))
# One shared skinned draw mesh; source parts retained by material/vertex groups.
bpy.ops.object.select_all(action='DESELECT');meshes=[o for o in s.objects if o.type=='MESH']
for o in meshes:o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0];bpy.ops.object.join();skin=bpy.context.object;skin.name='DoctorSkin';skin.data.materials.clear();skin.data.materials.append(mat)
for p in skin.data.polygons:p.material_index=0
# Bake idle and an in-place walk with two-bone IK into ordinary deform-bone transforms.
# Analytical pose targets keep stance feet level; no Blender-only constraints required in Unity.
def orient(pb,head,tail):
 rest=pb.bone.matrix_local.to_quaternion();direction=(tail-head).normalized();q=Vector((0,1,0)).rotation_difference(direction)
 M=q.to_matrix().to_4x4();M.translation=head;pb.matrix=M
# Use rest-bone roll while aiming each segment: preserve a stable perpendicular axis.
def pose_world(pb):
 if pb.parent:return pose_world(pb.parent)@pb.parent.bone.matrix_local.inverted()@pb.bone.matrix_local@pb.matrix_basis
 return pb.bone.matrix_local@pb.matrix_basis

def assign_pose(pb,M):
 if pb.parent:pb.matrix_basis=pb.bone.convert_local_to_pose(M,pb.bone.matrix_local,parent_matrix=pose_world(pb.parent),parent_matrix_local=pb.parent.bone.matrix_local,invert=True)
 else:pb.matrix_basis=pb.bone.matrix_local.inverted()@M

def aim(pb,head,tail):
 rest=pb.bone.matrix_local;v=(rest.to_3x3()@Vector((0,1,0))).normalized();q=v.rotation_difference((tail-head).normalized());M=(q.to_matrix()@rest.to_3x3()).to_4x4();M.translation=head;assign_pose(pb,M)

def solve_leg(tag,foot_z,foot_y):
 side=-1 if tag=='L' else 1;hip=P((side*.125,.87,0));ankle=P((side*.125,.15+foot_y,foot_z));l1=(P(bones['Thigh'+tag][0])-P(bones['Thigh'+tag][1])).length;l2=(P(bones['Shin'+tag][0])-P(bones['Shin'+tag][1])).length
 d=ankle-hip;dist=min(d.length,l1+l2-.001);axis=d.normalized();along=(l1*l1-l2*l2+dist*dist)/(2*dist);bend=P((0,0,1));bend=(bend-axis*bend.dot(axis)).normalized();knee=hip+axis*along+bend*math.sqrt(max(0,l1*l1-along*along))
 aim(rig.pose.bones['Thigh'+tag],hip,knee);aim(rig.pose.bones['Shin'+tag],knee,ankle)
 # Foot remains approximately horizontal during stance, with a little toe lift in swing.
 foot=rig.pose.bones['Foot'+tag];rest=foot.bone.matrix_local.copy();rest.translation=ankle;assign_pose(foot,rest)
 toe=rig.pose.bones['Toe'+tag];toe.rotation_mode='XYZ';toe.rotation_euler=(0,0,0)

def make_action(name,walk=False):
 rig.animation_data_create();action=bpy.data.actions.new(name);rig.animation_data.action=action;action.use_fake_user=True
 for frame in range(1,32):
  s.frame_set(frame);f=(frame-1)/30;phase=f*2*math.pi
  for pb in rig.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
  # No vertical root bob; breathing belongs to the chest, not capsule motion.
  rig.pose.bones['Chest'].rotation_quaternion=Vector((1,0,0)).rotation_difference(Vector((1,0,.012*math.sin(phase))))
  if walk:
   hips=rig.pose.bones['Hips'];M=hips.bone.matrix_local.copy();M.translation+=P((0,-.07,0));assign_pose(hips,M)
   for tag,offset in [('L',0),('R',.5)]:
    t=(f+offset)%1
    if t<.6:z=.32-(t/.6)*.64;lift=0
    else:
     u=(t-.6)/.4;ease=u*u*(3-2*u);z=-.32+.64*ease;lift=.12*math.sin(math.pi*u)
    solve_leg(tag,z,lift)
    swing=math.sin(phase+(0 if tag=='L' else math.pi))
    pb=rig.pose.bones['UpperArm'+tag];pb.rotation_quaternion=Vector((0,1,0)).rotation_difference(Vector((0,math.cos(.25*swing),math.sin(.25*swing))))
    pb=rig.pose.bones['Forearm'+tag];pb.rotation_quaternion=Vector((0,1,0)).rotation_difference(Vector((0,math.cos(.20+.13*swing),math.sin(.20+.13*swing))))
    for region in ['Front','Back']:
     pb=rig.pose.bones['Coat'+region+tag];pb.rotation_quaternion=Vector((0,1,0)).rotation_difference(Vector((0,math.cos(.065*swing),math.sin(.065*swing))))
   rig.pose.bones['Satchel'].rotation_quaternion=Vector((0,1,0)).rotation_difference(Vector((.04*math.sin(phase+.4),1,.025*math.sin(phase))))
  else:
   for tag in ['L','R']:
    # Gentle relaxed elbows, feet at rest.
    rig.pose.bones['Forearm'+tag].rotation_quaternion=Vector((0,1,0)).rotation_difference(Vector((0,math.cos(.08),math.sin(.08))))
  bpy.context.view_layer.update()
  for pb in rig.pose.bones:
   pb.keyframe_insert(data_path='location',frame=frame,group=pb.name);pb.keyframe_insert(data_path='rotation_quaternion',frame=frame,group=pb.name);pb.keyframe_insert(data_path='scale',frame=frame,group=pb.name)
 return action
idle=make_action('Doctor_Idle',False);walk=make_action('Doctor_Walk',True)
rig.animation_data.action=idle;s.frame_start=1;s.frame_end=31;s.frame_set(1)
# Preserve editable native source before export coordinate root conversion.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'BB_PlagueDoctor01_Rigged02.blend'))
# Established metric FBX axes, with a parent conversion node (do not bake armature bind transforms).
root=bpy.data.objects.new('BB_DoctorExport',None);s.collection.objects.link(root);rig.parent=root;root.rotation_euler.z=math.pi
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);rig.select_set(True);skin.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/BB_PlagueDoctor01_Rigged02.fbx'),use_selection=True,object_types={'MESH','ARMATURE','EMPTY'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=False,mesh_smooth_type='FACE',bake_anim=True,bake_anim_use_all_actions=True,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,add_leaf_bones=False,path_mode='STRIP')
(D/'BuildValidation.json').write_text(json.dumps(dict(parts=checks,bones=list(bones),actions=[idle.name,walk.name],triangles=sum(c['triangles'] for c in checks),vertices=len(skin.data.vertices)),indent=2));print('RIGGED_DOCTOR_EXPORTED',len(bones),len(skin.data.vertices))
