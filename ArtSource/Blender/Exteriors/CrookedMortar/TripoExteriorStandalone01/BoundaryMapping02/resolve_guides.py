"""Annotations only. Hand-picked visible contacts; hidden contacts remain explicit repair proposals."""
import bpy,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;old=D.parent/'BoundaryMapping01';src=old/'CM_CrookedMortar_BoundaryMapping01_UNCUT.blend'
source_sha=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;cam=s.camera;vl=s.view_layers[0]
code=(old/'create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')])
meshes={o.name:mesh_hash(o) for o in bpy.data.objects if o.type=='MESH'};mats={m.name:mat_hash(m) for m in bpy.data.materials}
G=bpy.data.collections.new('BOUNDARY02_REVIEW_ONLY__NO_CUT');s.collection.children.link(G)
def mat(name,col):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();a=n.new('ShaderNodeEmission');a.inputs[0].default_value=(*col,1);a.inputs[1].default_value=1.2;b=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(a.outputs[0],b.inputs[0]);return m
pink=bpy.data.materials['GUIDE_ONLY_Magenta_Proposed'];cyan=mat('GUIDE02_Cyan_LocalRepairContact',(.002,.7,1))
def line(name,pts,material):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=.018;c.bevel_resolution=2;c.use_fill_caps=True;p=c.splines.new('POLY');p.points.add(len(pts)-1)
 for a,b in zip(p.points,pts):a.co=(*b,1)
 o=bpy.data.objects.new(name,c);G.objects.link(o);c.materials.append(material);o['annotation_only']=True;return o
views=json.loads((D/'Views.json').read_text());V={a:(b,c,d) for a,b,c,d in views}
# Pixel selections were made after close-up inspection of each rendered house view.
paths={
'PorchLeft':[(315,418),(380,427),(470,439),(560,449),(650,450),(700,447)],
'PorchRight':[(80,407),(180,433),(285,460),(350,465),(385,510),(460,510),(560,505),(625,490)],
'RockIvyLeft':[(40,474),(170,474),(310,475),(440,476),(530,477)],
'RockIvyRight':[(700,490),(850,492),(1040,495)],
'PlanterLeft':[(180,518),(300,520),(460,520),(490,518),(550,515),(588,525),(700,532),(820,527),(850,510),(940,512),(1000,503)],
'PlanterRight':[(40,478),(150,479),(170,500),(255,503),(280,522),(400,526),(495,526),(530,502),(600,509),(730,516),(890,519),(980,520)],
'Rear':[(130,500),(170,488),(300,494),(460,495),(620,493),(800,493),(900,489),(960,491)]}
# Only source meshes participate in ray hits; annotation collections excluded.
for c in vl.layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=True
records={};new_by_view={}
for name,pixels in paths.items():
 pos,target,size=V[name];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();pts=[];rows=[]
 for x,y in pixels:
  origin=cam.location+q@Vector(((x/1100-.5)*size,(.5-y/850)*size*850/1100,0));hit=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,q@Vector((0,0,-1)))
  rows.append(dict(pixel=[x,y],point=list(hit[1]) if hit[0] else None,object=hit[4].name if hit[0] else None))
  if hit[0]:pts.append(tuple(hit[1]+Vector((0,0,.018))))
 records[name]=rows
 assert len(pts)==len(pixels),(name,rows)
 o=line('RESOLVED_CONTACT_'+name,pts,pink);o['view']=name;o['confidence']='Visible contact proposal; not mesh edge or cut operand';new_by_view[name]=[o]
# Hidden contact estimates stay cyan. They are not snapped to the rock or invented as known foundation edges.
repairpaths={
'RockIvyLeft':[(-2.904,-2.744,.567),(-2.70,-3.45,.64),(-2.408,-5.051,.737)],
'RockIvyRight':[(2.443,-4.201,.558),(2.72,-3.60,.55),(2.87,-2.65,.48),(2.87,-.607,.439)],
'RearUnder':[(-3.208,6.557,.503),(-2.831,6.636,.542),(0,6.70,.48),(2.831,6.650,.560),(2.778,6.314,.499)]}
for name,pts in repairpaths.items():
 o=line('LOCAL_REPAIR_PROPOSAL_'+name,pts,cyan);o['view']=name;o['confidence']='Approximate obscured contact / lower-return reconstruction proposal, NOT safe cutting coordinates';new_by_view.setdefault(name,[]).append(o)
# Carry forward already-readable magenta guide portions; preserve all old annotations hidden as historical reference.
for o in list(bpy.data.objects):
 if o.name.startswith('CONTACT_GUIDE_') and o.get('status')=='Proposed':
  n=o.copy();n.data=o.data.copy();n.name='UNCHANGED_APPROVED_REFERENCE_'+o.name;G.objects.link(n);n['annotation_only']=True
(D/'ManualCloseupPicks.json').write_text(json.dumps(records,indent=2))
(D/'LocalRepairProposals.json').write_text(json.dumps(repairpaths,indent=2))
s.render.resolution_x=1100;s.render.resolution_y=850;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.cycles.samples=4
oldlines=[o for o in bpy.data.objects if o.name.startswith('CONTACT_GUIDE_')]
for name,pos,target,size in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;cam.data.clip_start=.01
 if name.startswith('Porch'):sides={'Front','Left','Left_Front'} if name.endswith('Left') else {'Front','Right','Front_Right'}
 elif name.endswith('Left'):sides={'Left','Left_Front','Rear_Left'}
 elif name.endswith('Right'):sides={'Right','Front_Right','Right_Rear'}
 else:sides={'Rear','Rear_Left','Right_Rear'}
 for stage,chosen in [('Before',[o for o in oldlines if o.get('side') in sides]),('After',new_by_view.get(name,[]))]:
  tmp=bpy.data.collections.new('TEMP_GuideRender');s.collection.children.link(tmp)
  for o in chosen:tmp.objects.link(o);o.hide_render=False
  states=[]
  for c in vl.layer_collection.children:
   if c.name!=tmp.name:states.append((c,c.exclude));c.exclude=True
  s.render.film_transparent=True;bpy.context.view_layer.update();s.render.filepath=str(D/(name+'_'+stage+'_Guide.png'));bpy.ops.render.render(write_still=True)
  for c,v in states:c.exclude=v
  bpy.data.collections.remove(tmp)
# Old annotations remain recoverable but excluded; current guides visible in normal depth.
for c in vl.layer_collection.children:
 if c.name.startswith('BOUNDARY_MAPPING'):c.exclude=True
 if c.name==G.name:c.exclude=False
for o in G.all_objects:o.hide_render=False;o.show_in_front=False
s.render.film_transparent=False;s.cycles.samples=12
cam.location=(16,-24,15);cam.rotation_euler=(Vector((0,0,4.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=21
checks=dict(source_mapping_sha256=source_sha,source_mapping_unchanged=hashlib.sha256(src.read_bytes()).hexdigest()==source_sha,original_meshes_unchanged=meshes=={n:mesh_hash(bpy.data.objects[n]) for n in meshes},original_material_nodes_unchanged=mats=={n:mat_hash(bpy.data.materials[n]) for n in mats},original_mesh_count=len(meshes),new_building_meshes=0,geometry_cut_or_reconstructed=False,unity_files_changed=False,mesh_hashes=meshes)
assert checks['source_mapping_unchanged'] and checks['original_meshes_unchanged'] and checks['original_material_nodes_unchanged']
(D/'PreservationValidation.json').write_text(json.dumps(checks,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CrookedMortar_BoundaryMapping02_UNCUT.blend'));print('PRESERVATION_OK',flush=True)
