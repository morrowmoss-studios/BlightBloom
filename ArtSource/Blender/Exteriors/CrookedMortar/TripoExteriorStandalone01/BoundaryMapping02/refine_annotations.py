"""Refine inspection annotation confidence and explicit loose-rock exclusions only."""
import bpy,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_BoundaryMapping02_UNCUT.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;cam=s.camera;vl=s.view_layers[0];G=bpy.data.collections['BOUNDARY02_REVIEW_ONLY__NO_CUT']
code=(D.parent/'BoundaryMapping01/create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);check=json.loads((D/'PreservationValidation.json').read_text());before=check['mesh_hashes']
red=bpy.data.materials.new('GUIDE02_Red_LooseTerrainExclusion');red.use_nodes=True;red.diffuse_color=(1,.03,.03,1);n=red.node_tree.nodes;n.clear();a=n.new('ShaderNodeEmission');a.inputs[0].default_value=(1,.03,.03,1);b=n.new('ShaderNodeOutputMaterial');red.node_tree.links.new(a.outputs[0],b.inputs[0]);cyan=bpy.data.materials['GUIDE02_Cyan_LocalRepairContact']
def curve(name,pts,material,view):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=.014;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);G.objects.link(o);c.materials.append(material);o['view']=view;o['annotation_only']=True;return o
retired=bpy.data.collections.new('BOUNDARY02_SUPERSEDED_DETAIL_GUIDES_HIDDEN');s.collection.children.link(retired)
for name,cyanedges in [('PlanterLeft',{3,4,7,9}),('PlanterRight',{3,6,7})]:
 o=bpy.data.objects['RESOLVED_CONTACT_'+name];pts=[tuple(p.co[:3]) for p in o.data.splines[0].points];retired.objects.link(o);G.objects.unlink(o)
 for i,(p,q) in enumerate(zip(pts,pts[1:])):
  ob=curve('CONTACT02_'+name+f'_{i:02d}',[p,q],cyan if i in cyanedges else o.data.materials[0],name);ob['confidence']='Obscured connector, lower return needs local review' if i in cyanedges else 'Visible retained architectural toe'
for c in vl.layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=True
views=json.loads((D/'Views.json').read_text());V={a:(b,c,d) for a,b,c,d in views}
exclude={'PorchLeft':[(160,373)],'PorchRight':[(390,520),(990,450)],'RockIvyLeft':[(730,408)],'RockIvyRight':[(465,477),(615,531),(713,513)],'PlanterLeft':[(739,519)],'PlanterRight':[(349,518)],'Rear':[(135,500),(995,482)]};records={}
for name,pixels in exclude.items():
 pos,target,size=V[name];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();records[name]=[]
 for i,(x,y) in enumerate(pixels):
  origin=cam.location+q@Vector(((x/1100-.5)*size,(.5-y/850)*size*850/1100,0));h=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,q@Vector((0,0,-1)));assert h[0]
  p=h[1]+q@Vector((0,0,.025));r=.09
  for j,ends in enumerate([((-r,-r,0),(r,r,0)),((-r,r,0),(r,-r,0))]):
   o=curve(f'EXCLUDE_LOOSE_ROCK_{name}_{i}_{j}',[tuple(p+q@Vector(v)) for v in ends],red,name);o['purpose']='Remove isolated terrain rock in future approved surgery; not structural stone'
  records[name].append(dict(pixel=[x,y],surface_point=list(h[1]),face_index=h[3],object=h[4].name))
(D/'LooseRockReviewPicks.json').write_text(json.dumps(records,indent=2))
s.render.resolution_x=1100;s.render.resolution_y=850;s.render.resolution_percentage=100;s.cycles.samples=4;s.render.film_transparent=True
for name,pos,target,size in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size
 tmp=bpy.data.collections.new('TEMP02_ANNOTATIONS');s.collection.children.link(tmp)
 for o in G.objects:
  if o.get('view')==name:tmp.objects.link(o);o.hide_render=False
 states=[]
 for c in vl.layer_collection.children:
  if c.name!=tmp.name:states.append((c,c.exclude));c.exclude=True
 bpy.context.view_layer.update();s.render.filepath=str(D/(name+'_After_Guide.png'));bpy.ops.render.render(write_still=True)
 for c,v in states:c.exclude=v
 bpy.data.collections.remove(tmp)
for c in vl.layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=c.name!=G.name
s.render.film_transparent=False;s.cycles.samples=12
cam.location=(16,-24,15);cam.rotation_euler=(Vector((0,0,4.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=21
assert before=={n:mesh_hash(bpy.data.objects[n]) for n in before}
check['post_refinement_original_mesh_hashes_match']=True;check['red_crosses_are_annotation_curves_only']=True;check['new_building_meshes']=0
(D/'PreservationValidation.json').write_text(json.dumps(check,indent=2));s['Boundary02_Status']='Ownership reviewed. Cyan hidden contacts require local repair after approval; NOT a certified continuous cut operand.'
bpy.ops.wm.save_as_mainfile(filepath=str(f));print('ANNOTATION_REFINEMENT_OK')
