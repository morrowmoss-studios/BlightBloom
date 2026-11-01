"""Boundary proposal only: manually chosen elevation picks, no mesh edits or extraction."""
import bpy,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;src=D.parent/'SeparationInspection_UNCUT.blend';source_hash=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;cam=s.camera
original_meshes=[o for o in bpy.data.objects if o.type=='MESH'];original_mats=list(bpy.data.materials)
def mesh_hash(o):
 h=hashlib.sha256();m=o.data
 for seq,attr,width,dtype in [(m.vertices,'co',3,np.float32),(m.edges,'vertices',2,np.int32),(m.loops,'vertex_index',1,np.int32),(m.polygons,'loop_start',1,np.int32),(m.polygons,'loop_total',1,np.int32)]:
  a=np.empty(len(seq)*width,dtype=dtype);seq.foreach_get(attr,a);h.update(a.tobytes())
 for uv in m.uv_layers:
  a=np.empty(len(uv.data)*2,np.float32);uv.data.foreach_get('uv',a);h.update(uv.name.encode());h.update(a.tobytes())
 h.update(str([x.name if x else None for x in m.materials]).encode());h.update(str([list(r) for r in o.matrix_world]).encode());return h.hexdigest()
def mat_hash(mat):
 if not mat.use_nodes:return hashlib.sha256(str(list(mat.diffuse_color)).encode()).hexdigest()
 n=mat.node_tree;data=[]
 for node in n.nodes:
  fields=[node.name,node.bl_idname]
  if node.type=='TEX_IMAGE':fields.append(node.image.name if node.image else None)
  for i in node.inputs:
   if hasattr(i,'default_value'):
    v=i.default_value
    try:v=list(v)
    except TypeError:v=str(v)
    fields.append([i.name,v])
  data.append(fields)
 data.append([(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in n.links]);return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
before={o.name:mesh_hash(o) for o in original_meshes};mbefore={m.name:mat_hash(m) for m in original_mats}
G=bpy.data.collections.new('BOUNDARY_MAPPING_ONLY__NO_CUT_NO_EXPORT');s.collection.children.link(G)
actual=bpy.data.collections.new('01_Proposed_Surface_Guide_EDITABLE');G.children.link(actual)
under=bpy.data.collections.new('02_XY_Projection_ONLY_Not_UndersideCut');G.children.link(under)
labels=bpy.data.collections.new('03_Review_Callouts_And_Legend');G.children.link(labels)
def emission(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(*color,1);em.inputs['Strength'].default_value=1.3;m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);return m
pink=emission('GUIDE_ONLY_Magenta_Proposed',(.96,.002,.25));orange=emission('GUIDE_ONLY_Orange_Uncertain',(1,.30,.002));white=emission('GUIDE_ONLY_LegendIvory',(.85,.85,.78))
picks=json.loads((D/'ManualElevationPicks.json').read_text());traces={}
for side,rows in picks.items():
 order=list(range(len(rows)))
 if side in ['Right','Left']:order=order[::-1]
 traces[side]=[(i,rows[i]['point']) for i in order if rows[i]['point'] is not None]
# Status explicitly assigned after visual review; no height threshold or geometry-based auto mask.
def status(side,a,b):
 if side=='Front':return ('Proposed','F1_LowestFrontStep') if min(a,b)>=3 and max(a,b)<=7 else ('Uncertain','U1_PorchBasesAndStepReturns')
 if side=='Rear':return ('Uncertain','U4_RearFencePlinthOwnership')
 if side=='Right':
  if max(a,b)>=10:return ('Uncertain','U2_RocksIvyAndPorchReturn')
  if min(a,b)>=3 and max(a,b)<=5:return ('Uncertain','U3_GroundPlanters')
  if min(a,b)==0:return ('Uncertain','U4_RearCorner')
  return ('Proposed','R_FoundationAndThreshold')
 if side=='Left':
  if min(a,b)==0:return ('Uncertain','U2_OccludedPorchToBayContact')
  if max(a,b)>=12:return ('Uncertain','U4_RearCorner')
  if min(a,b)>=6 and max(a,b)<=10:return ('Uncertain','U3_GroundPlanters')
  return ('Proposed','L_FoundationAndThreshold')
segments=[]
for side in ['Front','Right','Rear','Left']:
 for (ia,a),(ib,b) in zip(traces[side],traces[side][1:]):
  conf,reason=status(side,ia,ib);segments.append(dict(side=side,from_pick=ia,to_pick=ib,a=a,b=b,status=conf,reason=reason))
for side,nxt,reason in [('Front','Right','U1_PorchBaseCorner'),('Right','Rear','U4_RearCorner'),('Rear','Left','U4_RearCorner'),('Left','Front','U1_PorchBaseCorner')]:segments.append(dict(side=side+'_'+nxt,a=traces[side][-1][1],b=traces[nxt][0][1],status='Uncertain',reason=reason))
def curve(name,pts,mat,col,r=.028):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=r;cu.bevel_resolution=2;cu.use_fill_caps=True;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 ob=bpy.data.objects.new(name,cu);col.objects.link(ob);cu.materials.append(mat);ob.show_in_front=True;return ob
lines=[]
for i,seg in enumerate(segments):
 for projection,col in [(False,actual),(True,under)]:
  pts=[(p[0],p[1],-.10 if projection else p[2]+.025) for p in [seg['a'],seg['b']]]
  ob=curve(('XY_PROJECTION_' if projection else 'CONTACT_GUIDE_')+f'{i:02d}_'+seg['reason'],pts,orange if seg['status']=='Uncertain' else pink,col);ob['side']=seg['side'];ob['status']=seg['status'];ob['purpose']='Review annotation only; not a mesh-edge selection or cutting operand';lines.append((ob,seg,projection))
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Georgia.ttf')
def text(name,body,mat,size=.24):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.size=size;cu.align_x='CENTER';cu.materials.append(mat);ob=bpy.data.objects.new(name,cu);labels.objects.link(ob);ob.show_in_front=True;return ob
legend=[text('VIEW_TITLE','',white),text('VIEW_LEGEND_PINK','MAGENTA: proposed contact boundary',pink),text('VIEW_LEGEND_ORANGE','ORANGE: uncertain — manual review required',orange),text('VIEW_FOOTNOTE','',white)]
for ob in legend:ob.parent=cam;ob.rotation_euler=(0,0,0);ob.data.align_x='LEFT'
review=[('U1',(-2.05,-5.4,.82),['Front','Left','Overview']),('U1',(1.9,-5.4,.82),['Front','Right','Overview']),('U2',(-2.75,-3.55,.64),['Left','Overview']),('U2',(3.10,-2.8,.65),['Right','Overview']),('U3',(-3.12,2.65,.55),['Left','Overview']),('U3',(2.92,2.9,.55),['Right','Overview']),('U4',(0,6.7,.55),['Rear','Overview'])]
callouts=[]
for i,(tag,p,views) in enumerate(review):
 ob=text(f'REVIEW_{tag}_{i}',tag,orange,.32);ob['review_zone']=tag;ob.location=Vector(p)+Vector((0,0,.65));leader=curve(f'REVIEW_LEADER_{i}',[p,tuple(ob.location-Vector((0,0,.12)))],orange,labels,.013);callouts.append((ob,leader,p,views))
# One extra collection dedicated to guide rendering. Original collections/materials are never edited.
s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
vl=s.view_layers[0];others=list(s.view_layers)[1:]
for layer in others:layer.use=False
vl.use=True
# Excluding a layer collection changes inspection visibility only, never source objects or data.
def layer_node(name,root=None):
 root=root or vl.layer_collection
 if root.name==name:return root
 for c in root.children:
  v=layer_node(name,c)
  if v:return v
 return None
views=[('Front',(0,-22,4.6),(0,-3.6,1.0),11.5),('Rear',(0,22,4.6),(0,4,1.0),11.5),('Left',(-22,0,4.8),(-1,0,1),17),('Right',(22,0,4.8),(1,0,1),17),('Underside',(12,-18,-14),(0,0,.6),19),('Overview',(16,-24,15),(0,0,4.5),21)]
(D/'BoundaryProposal.json').write_text(json.dumps(dict(coordinates='Blender metres, front -Y, left -X; Unity FBX conversion mirrors X',source=str(src),surface_guide_display_lift_m=.025,underside_projection_z_m=-.10,segments=segments,review_zones={'U1':'Porch-base stones and step returns; irregular contacts partly occluded','U2':'Loose rocks versus structural stones; ivy at porch-to-shop-bay returns; one side has no visible ray-picked contact','U3':'Ground-level pots, masonry herb beds and their fused soil/vegetation contacts','U4':'Rear fence/plinth classification and corner feet: provisional keep envelope, final building-versus-terrain ownership unresolved'},continuous_proposal=True,continuous_verified_safe_cut=False,underside_is_projection_not_reconstruction=True),indent=2))
for name,pos,target,width in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=width;cam.data.clip_start=.01;cam.data.clip_end=200;bpy.context.view_layer.update();height=width*1000/1400
 for i,ob in enumerate(legend):
  y=height/2-.42-i*.34 if i<3 else -height/2+.34;ob.location=(-width*.48,y,-1);ob.data.size=width*(.018 if i==0 else .0125)
 legend[0].data.body=name.upper()+' — FOUNDATION BOUNDARY PROPOSAL'
 legend[3].data.body='XY PROJECTION ONLY: underside cut level is unresolved. No geometry changed.' if name=='Underside' else 'Review overlay / 25 mm display lift. Not a cutting tool or approved mesh-edge path.'
 for ob,seg,projection in lines:
  side=seg['side'];visible=(name in ['Overview','Underside'] or side==name or name in side.split('_')) and (projection==(name=='Underside'));ob.hide_render=not visible
 for ob,leader,p,visible_views in callouts:
  vis=name in visible_views or name=='Underside';ob.hide_render=leader.hide_render=not vis
  point=Vector((p[0],p[1],-.1)) if name=='Underside' else Vector(p);ob.location=point+cam.rotation_euler.to_quaternion()@Vector((0,.65,0));ob.rotation_euler=cam.rotation_euler
  sp=leader.data.splines[0]
  for v,co in zip(sp.points,[point,ob.location]):v.co=(*co,1)
 # Render actual unmodified house first, then transparent annotation layer for readable X-ray review.
 node=layer_node(G.name);node.exclude=True;s.render.film_transparent=False;s.render.filepath=str(D/f'{name}_House.png');bpy.ops.render.render(write_still=True)
 source_nodes=[c for c in vl.layer_collection.children if c.name!=G.name];states=[c.exclude for c in source_nodes]
 for c in source_nodes:c.exclude=True
 node.exclude=False;s.render.film_transparent=True;s.cycles.samples=4;s.render.filepath=str(D/f'{name}_Guides.png');bpy.ops.render.render(write_still=True)
 for c,st in zip(source_nodes,states):c.exclude=st
 s.cycles.samples=16;s.render.film_transparent=False
# Store a useful overview in the marked copy. Surface guide visible; underside projection/legend can toggle independently.
for ob,seg,projection in lines:ob.hide_render=projection
for ob,leader,p,vis in callouts:ob.hide_render=leader.hide_render=False
for ob in legend:ob.hide_render=True
under.hide_viewport=True;under.hide_render=True
for area in bpy.context.screen.areas if bpy.context.screen else []:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_distance=24;area.spaces.active.region_3d.view_location=(0,0,4)
after={o.name:mesh_hash(o) for o in original_meshes};mafter={m.name:mat_hash(m) for m in original_mats};check=dict(source_file_unchanged=hashlib.sha256(src.read_bytes()).hexdigest()==source_hash,source_sha256=source_hash,all_original_mesh_geometry_uvs_assignments_and_transforms_unchanged=before==after,all_original_material_nodes_unchanged=mbefore==mafter,original_mesh_count=len(original_meshes),new_building_meshes=0,new_objects_are_annotation_curves_or_text_only=True,original_mesh_hashes=before)
assert all([check['source_file_unchanged'],before==after,mbefore==mafter]);(D/'PreservationValidation.json').write_text(json.dumps(check,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CrookedMortar_BoundaryMapping01_UNCUT.blend'));print('PRESERVATION',json.dumps({k:v for k,v in check.items() if k!='original_mesh_hashes'}),flush=True)
