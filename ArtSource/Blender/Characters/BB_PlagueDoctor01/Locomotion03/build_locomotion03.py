"""Locomotion revision on the approved 27-bone skin; no environment or controller changes."""
import bpy,math,json,ast
from mathutils import Vector,Matrix
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Characters/PlagueDoctor01/Locomotion03'
bpy.ops.wm.open_mainfile(filepath=str(D.parent/'Rigged02/BB_PlagueDoctor01_Rigged02.blend'))
bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.render.fps=60
rig=bpy.data.objects['BB_DoctorRig'];skin=bpy.data.objects['DoctorSkin']
tree=ast.parse((D.parent/'Rigged02/build_rigged_doctor.py').read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['P','pose_world','assign_pose','aim']],type_ignores=[]),'<existing rig helpers>','exec'),globals())
rig.animation_data_clear()
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
# Tailored split panels follow the supporting thigh through sprint knee recovery.
# Blend at the waist, retain a small secondary-bone contribution at the hem.
for v in skin.data.vertices:
 garment=[(skin.vertex_groups[g.group].name,g.weight) for g in v.groups if skin.vertex_groups[g.group].name.startswith('Coat') and g.weight>0]
 if garment:
  name=max(garment,key=lambda p:p[1])[0];strength=max(0,min(.98,(1.02-v.co.z)/.25))
  for g in list(v.groups):skin.vertex_groups[g.group].remove([v.index])
  for group,weight in [('Hips',1-strength),(name,strength*.07),('Thigh'+name[-1],strength*.93)]:
   skin.vertex_groups[group].add([v.index],weight,'REPLACE')
 # The existing toes can now roll without folding the whole boot.
 if v.co.y>.13 and v.co.z<.16:
  side='L' if v.co.x<0 else 'R';foot=skin.vertex_groups.get('Foot'+side);toe=skin.vertex_groups.get('Toe'+side) or skin.vertex_groups.new(name='Toe'+side)
  w=next((g.weight for g in v.groups if g.group==foot.index),0)
  if w>.7:
   t=min(.85,max(0,(v.co.y-.13)/.11));foot.add([v.index],w*(1-t),'REPLACE');toe.add([v.index],w*t,'REPLACE')

# Tailor the existing split linen's narrow centre edges into walking vents.
# The original overlapping centre seam was pierced by the opposite recovery boot.
adj=[[] for _ in skin.data.vertices]
for e in skin.data.edges:
 a,b=e.vertices;adj[a].append(b);adj[b].append(a)
unseen=set(range(len(adj)));tailored=0
while unseen:
 start=unseen.pop();component=[start];stack=[start]
 while stack:
  for n in adj[stack.pop()]:
   if n in unseen:unseen.remove(n);component.append(n);stack.append(n)
 verts=[skin.data.vertices[i] for i in component]
 if 300<=len(verts)<=350 and .98<max(v.co.z for v in verts)<1.025 and .32<min(v.co.z for v in verts)<.38:
  side=-1 if sum(v.co.x for v in verts)<0 else 1
  for v in verts:
   vent=max(0,1-abs(v.co.x)/.14)*max(0,min(1,(.88-v.co.z)/.35))
   v.co.x+=side*.085*vent
  tailored+=1
print('TAILORED_LINEN_PANELS',tailored)

def smooth(u):return max(0,min(1,u))**3*(10-15*max(0,min(1,u))+6*max(0,min(1,u))**2)
def rotate_world(pb,angle,axis):
 M=pose_world(pb);pos=M.translation.copy();M=Matrix.Rotation(angle,4,P(axis))@M;M.translation=pos;assign_pose(pb,M)
def chain(upper,lower,end,target,pole):
 a=rig.pose.bones[upper];b=rig.pose.bones[lower];c=rig.pose.bones[end]
 head=pose_world(a).translation.copy();l1=a.bone.length;l2=b.bone.length;delta=target-head
 distance=min(delta.length,l1+l2-.0005);axis=delta.normalized();target=head+axis*distance
 along=(l1*l1-l2*l2+distance*distance)/(2*distance);bend=pole-axis*pole.dot(axis);bend.normalize()
 joint=head+axis*along+bend*math.sqrt(max(0,l1*l1-along*along));aim(a,head,joint);aim(b,joint,target)
 return head,joint,target

def leg(tag,t,run):
 side=-1 if tag=='L' else 1;duty=.32 if run else .55;distance=2.5 if run else 1.4;reach=distance*duty*.5
 if t<duty:
  q=t/duty;z=reach-distance*t;lift=0
  heel=(math.radians(7 if run else 10)*(1-smooth(q/.14)) if q<.14 else 0)
  toe=-math.radians(22 if run else 14)*smooth((q-.76)/.24)
  roll=heel+toe
 else:
  u=(t-duty)/(1-duty);z=-reach+2*reach*smooth(u)
  lift=(.28 if run else .11)*math.sin(math.pi*u)**1.25
  if run:z-=.055*math.sin(math.pi*min(1,u*2))*(1-u)
  roll=math.radians(-18 if run else -7)*math.sin(math.pi*u)+math.radians(8)*smooth((u-.75)/.25)
 # Floor support under the pitched boot (heel/toe approximation), leaving a 7mm sole margin.
 marker_a=Matrix.Rotation(roll,3,'X')@P((0,-.14,-.06));marker_b=Matrix.Rotation(roll,3,'X')@P((0,-.138,.22))
 ankle_height=max(.15,-min(marker_a.z,marker_b.z)+.007)
 target=P((side*.13,ankle_height+lift,z));hip,knee,ankle=chain('Thigh'+tag,'Shin'+tag,'Foot'+tag,target,P((side*.04,0,1)))
 foot=rig.pose.bones['Foot'+tag];M=foot.bone.matrix_local.copy();M=Matrix.Rotation(roll,4,'X')@M;M.translation=ankle;assign_pose(foot,M)
 if t<duty:rotate_world(rig.pose.bones['Toe'+tag],-toe*.55,(1,0,0))
 return dict(stance=t<duty,lift=lift,foot=[ankle.x,ankle.z,ankle.y])

def arm(tag,t,run):
 side=-1 if tag=='L' else 1;phase=2*math.pi*t
 # Shoulder leads wrist; the second harmonic gives an eased recovery, not a rigid pendulum.
 swing=-math.cos(phase-.12)+.08*math.sin(phase*2-.25);swing=max(-1,min(1,swing))
 positive=max(0,swing)
 shoulder=pose_world(rig.pose.bones['UpperArm'+tag]).translation.copy()
 if run:dy=.31-.085*positive;forward=.11+.23*swing
 else:dy=.47-.15*positive;forward=.07+.20*swing
 target=shoulder+P((side*(.09+.005*math.sin(phase+.4)),-dy,forward))
 _,elbow,wrist=chain('UpperArm'+tag,'Forearm'+tag,'Hand'+tag,target,P((side*.35,.02,-1)))
 direction=(wrist-elbow).normalized()+P((0,-.18 if not run else -.06,.07))
 aim(rig.pose.bones['Hand'+tag],wrist,wrist+direction.normalized()*rig.data.bones['Hand'+tag].length)
 rotate_world(rig.pose.bones['Hand'+tag],math.radians(5 if not run else 8)*math.sin(phase-.5),(0,1,0))

def make(name,mode):
 run=mode=='sprint';moving=mode!='idle';rig.animation_data_create();action=bpy.data.actions.new(name);action.use_fake_user=True;rig.animation_data.action=action
 measures=[]
 for frame in range(1,62):
  s.frame_set(frame);f=(frame-1)/60;p=f*2*math.pi
  for pb in rig.pose.bones:pb.rotation_mode='QUATERNION';pb.matrix_basis=Matrix.Identity(4)
  if not moving:
   rotate_world(rig.pose.bones['Chest'],math.radians(.45)*math.sin(p),(1,0,0))
   for tag in ['L','R']:
    shoulder=pose_world(rig.pose.bones['UpperArm'+tag]).translation.copy();side=-1 if tag=='L' else 1
    _,elbow,wrist=chain('UpperArm'+tag,'Forearm'+tag,'Hand'+tag,shoulder+P((side*.09,-.47,.08)),P((side*.35,.02,-1)))
    aim(rig.pose.bones['Hand'+tag],wrist,wrist+P((0,-.16,.015)))
  else:
   duty=.32 if run else .55
   flight=0
   if run:
    half=f%.5
    if half>duty:flight=math.sin(math.pi*(half-duty)/(.5-duty))
   drop=(-.08+.035*flight) if run else (-.05-.04*math.cos(2*p))
   sway=(-.012 if run else -.022)*math.cos(p-.05)
   hips=rig.pose.bones['Hips'];M=hips.bone.matrix_local.copy()
   yaw=math.radians(5 if run else 3.5)*math.sin(p)
   roll=math.radians(2.8 if run else 2)*math.cos(p-.1)
   lean=math.radians(4 if run else 1.5)
   M=(Matrix.Rotation(yaw,4,'Z')@Matrix.Rotation(roll,4,'Y')@Matrix.Rotation(-lean,4,'X'))@M;M.translation=hips.bone.head_local+P((sway,drop,0));assign_pose(hips,M)
   rotate_world(rig.pose.bones['Spine'],-math.radians(5 if run else 1.5),(1,0,0))
   rotate_world(rig.pose.bones['Chest'],-math.radians(5 if run else 1.5),(1,0,0))
   rotate_world(rig.pose.bones['Chest'],-yaw*1.65,(0,1,0))
   rotate_world(rig.pose.bones['Chest'],-roll*.7,(0,0,1))
   rotate_world(rig.pose.bones['Head'],math.radians(6 if run else 2),(1,0,0))
   for tag,offset in [('L',0),('R',.5)]:
    t=(f+offset)%1
    rotate_world(rig.pose.bones['Shoulder'+tag],math.radians(2 if run else 1)*math.sin(2*math.pi*t+.2),(0,0,1))
    arm(tag,t,run);m=leg(tag,t,run)
    for region in ['Front','Back']:
     wave=math.sin(2*math.pi*t-.45)+.18*math.sin(4*math.pi*t+.2)
     rotate_world(rig.pose.bones['Coat'+region+tag],(.075 if run else .035)*wave,(1,0,0))
    if frame in [1,16,31,46,61]:measures.append(dict(frame=frame,side=tag,**m))
   rotate_world(rig.pose.bones['Satchel'],math.radians(4 if run else 1.8)*math.sin(p-.65),(1,0,0))
   rotate_world(rig.pose.bones['Satchel'],math.radians(2 if run else .8)*math.sin(p-.35),(0,0,1))
  bpy.context.view_layer.update()
  for pb in rig.pose.bones:
   for path in ['location','rotation_quaternion','scale']:pb.keyframe_insert(data_path=path,frame=frame,group=pb.name)
 return action,measures
reports=[];actions=[]
for name,mode in [('Doctor03_Idle','idle'),('Doctor03_Walk','walk'),('Doctor03_Sprint','sprint')]:
 action,samples=make(name,mode);actions.append(action);reports.append(dict(action=name,mode=mode,sourceFps=60,duration=1,cycleDistance=0 if mode=='idle' else 1.4 if mode=='walk' else 2.5,stanceFraction=0 if mode=='idle' else .55 if mode=='walk' else .32,samples=samples))
rig.animation_data.action=actions[0];s.frame_start=1;s.frame_end=61;s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'BB_PlagueDoctor_Locomotion03.blend'))
root=bpy.data.objects.new('BB_DoctorExport',None);s.collection.objects.link(root);rig.parent=root;root.rotation_euler.z=math.pi
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);rig.select_set(True);skin.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/BB_PlagueDoctor_Locomotion03.fbx'),use_selection=True,object_types={'MESH','ARMATURE','EMPTY'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=False,mesh_smooth_type='FACE',bake_anim=True,bake_anim_use_all_actions=True,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,add_leaf_bones=False,path_mode='STRIP')
(D/'AnimationCatalog.json').write_text(json.dumps(reports,indent=2));print('LOCOMOTION03_EXPORTED',len(rig.data.bones),len(skin.data.vertices),[a.name for a in actions])
