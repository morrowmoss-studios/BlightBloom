"""Focused editable-source refinement. Does not regenerate WF08's unchanged furniture."""
import bpy,bmesh,math,json,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow09';bpy.ops.wm.open_mainfile(filepath=str(D.parent/'CounterWorkflow08/CM_CounterWorkflow08.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));parts=list(bpy.data.collections['Editable shaped joinery'].objects);highs=[]
wood=bpy.data.materials['CM_CW08_Walnut'];iron=bpy.data.materials['CM_CW08_Iron'];carved=bpy.data.materials['CM_CW08_CarvedWalnut']
for m in [wood,iron,carved]:m.name=m.name.replace('CW08','CW09')
# Reuse only the established geometry/UV helpers, not factory-reset or construction sections.
text=(D.parent/'CounterWorkflow08/build_counter08.py').read_text();exec(text[text.index('def smooth('):text.index('ogee=')])
for o in list(parts):
 if 'swept shouldered standard' in o.name:
  parts.remove(o);bpy.data.objects.remove(o,do_unlink=True)
for name in ['CM_CW08_HeroCounter','CM_CW08_FormOnly','Plain board for form-only review','Integrated mortar board']:
 o=bpy.data.objects.get(name)
 if o:
  if o in parts:parts.remove(o)
  bpy.data.objects.remove(o,do_unlink=True)
# Square hewn posts, deliberately tapered and very mildly splayed; no swollen formal cabriole shape.
profile=[(-1,-.72),(-.72,-1),(.72,-1),(1,-.72),(1,.72),(.72,1),(-.72,1),(-1,.72)]
for side in [-1,1]:
 for back in [False,True]:
  rings=[(0,1.002,.247,.080,.071),(.065,1.002,.247,.080,.071),(.18,.988,.246,.070,.065),(.38,.977,.244,.067,.064),(.66,.981,.246,.069,.066),(.79,.990,.25,.079,.073),(.88,.994,.25,.082,.075),(.965,.994,.25,.082,.075)]
  vs=[(side*(cx+u*rx),y,(-cz if back else cz)+v*rz) for y,cx,cz,rx,rz in rings for u,v in profile];n=len(profile)
  fs=[tuple(reversed(range(n))),tuple(range(len(vs)-n,len(vs)))]+[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
  ob=mesh(('Rear' if back else 'Front')+' chamfered hewn joint-post '+str(side),vs,fs,bevel=.003)
  # Flat timber faces and narrow bevels keep planed construction readable in clay.
  for f in ob.data.polygons:f.use_smooth=False
  # A short curved knee reads as an actual rail-to-post bearing, not applied ornament.
  curve=bez([(side*.805,.925),(side*.865,.916),(side*.91,.852),(side*.965,.807)],18)
  poly=[(side*.975,.962),(side*.79,.962),(side*.79,.925)]+curve+[(side*.975,.807)]
  z0,z1=(-.29,-.215) if back else (.215,.29);extrude('Housed timber bearing knee',poly,z0,z1,b=.004)
  # Drawbored peg ends at the rail/post joint, shallow and flush rather than protruding studs.
  for y in [.838,.915]:
   cx=side*.994;cz=(-.25 if back else .25);out=(-1 if back else 1);zbase=cz+out*.075
   vs=[(cx+.0085*math.cos(j*math.tau/12),y+.0085*math.sin(j*math.tau/12),z) for z in [zbase,zbase+out*.003] for j in range(12)];fs=[tuple(reversed(range(12))),tuple(range(12,24))]+[(j,(j+1)%12,(j+1)%12+12,j+12) for j in range(12)];mesh('Drawbored oak peg',vs,fs,bevel=.0006)
# Reuse the actual dense sculpt source and UV topology; sharpen forms, retain soft edge falloff.
hi=bpy.data.objects['Editable integrated mortar field - dense sculpt'];hi.hide_set(False);hi.hide_render=False
H=np.load(D.parent/'CounterWorkflow07/SculptFields.npy')[1];N=H.shape[0]
blur=(H+np.roll(H,1,0)+np.roll(H,-1,0)+np.roll(H,1,1)+np.roll(H,-1,1))/5
sharpen=np.maximum(0,H+.65*(H-blur));height=sharpen*1.06
for vi,v in enumerate(hi.data.vertices):
 j,i=divmod(vi,N);uv=j/(N-1);x=v.co.x;base=.286+.052*math.cos(math.pi*x/1.04)+.012*math.cos(3*math.pi*x/1.04)-.020+.010*math.sin(math.pi*uv);v.co.y=base+float(height[N-1-j,i])
smooth(hi.data)
# Existing painterly walnut, modest hue/value tuning baked natively, not new artwork generation.
def paint_material(n,image,sculpt=False):
 m=bpy.data.materials.new(n);m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();lk=m.node_tree.links;out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');tex=ns.new('ShaderNodeTexImage');tex.image=image;hue=ns.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=.88;hue.inputs['Value'].default_value=1.07;lk.new(tex.outputs['Color'],hue.inputs['Color'])
 mult=ns.new('ShaderNodeMixRGB');mult.blend_type='MULTIPLY';mult.inputs[0].default_value=1;mult.inputs[2].default_value=(1.025,1.00,.97,1);lk.new(hue.outputs[0],mult.inputs[1]);col=mult.outputs[0]
 if sculpt:
  quiet=ns.new('ShaderNodeMixRGB');quiet.inputs[0].default_value=.57;quiet.inputs[2].default_value=(.15,.074,.032,1);lk.new(col,quiet.inputs[1]);att=ns.new('ShaderNodeVertexColor');att.layer_name='SculptPaintValues';mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;lk.new(quiet.outputs[0],mix.inputs[1]);lk.new(att.outputs[0],mix.inputs[2]);col=mix.outputs[0]
 lk.new(col,em.inputs['Color']);lk.new(em.outputs[0],out.inputs[0]);return m
sourceimage=next(n.image for n in wood.node_tree.nodes if n.type=='TEX_IMAGE')
def bake(o,material,name,size):
 prior=list(o.data.materials);o.data.materials.clear();o.data.materials.append(material);bpy.ops.object.select_all(action='DESELECT');o.hide_set(False);o.hide_render=False;o.select_set(True);bpy.context.view_layer.objects.active=o
 image=bpy.data.images.new(name,size,size,alpha=False);node=material.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;material.node_tree.nodes.active=node;s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.device='CPU';bpy.ops.object.bake(type='EMIT',margin=8);image.filepath_raw=str(A/'Textures'/f'{name}.png');image.file_format='PNG';image.save();image.pack();o.data.materials.clear()
 for m in prior:o.data.materials.append(m)
 return image
# Tiny UV quad is only a texture bake surface and is deleted before source save.
quad=mesh('Temporary colour bake quad',[(0,0,0),(1,0,0),(1,1,0),(0,1,0)],[(0,1,2,3)],register=False);uv=quad.data.uv_layers[0]
for li,co in zip(quad.data.polygons[0].loop_indices,[(0,0),(1,0),(1,1),(0,1)]):uv.data[li].uv=co
woodimage=bake(quad,paint_material('Walnut paint adjustment source',sourceimage),'CM_CW09_Walnut',1536);bpy.data.objects.remove(quad,do_unlink=True)
attr=hi.data.color_attributes['SculptPaintValues']
# Broad top highlights and shallow incised edge values follow the exact sculpture, not albedo noise.
curvature=height-(height+np.roll(height,2,0)+np.roll(height,-2,0)+np.roll(height,2,1)+np.roll(height,-2,1))/5
for vi in range(len(hi.data.vertices)):
 j,i=divmod(vi,N);h=float(height[N-1-j,i]);v=min(1,h/.026);edge=max(-.10,min(.10,float(curvature[N-1-j,i])*95));attr.data[vi].color=(.88+.66*v+edge,.85+.55*v+edge,.81+.43*v+edge,1)
carveimage=bake(hi,paint_material('Registered carving paint source',woodimage,True),'CM_CW09_CarvedWalnut',1536)
for m,img in [(wood,woodimage),(carved,carveimage)]:
 node=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE');node.image=img
hi.data.materials.clear();hi.data.materials.append(carved)
# Use the established curvature reduction + flat cap, with more budget on the focal carving.
low=hi.copy();low.data=hi.data.copy();s.collection.objects.link(low);low.name='Integrated mortar board - refined';bpy.context.view_layer.objects.active=low
mod=low.modifiers.new('Curvature-preserving sculpt reduction','DECIMATE');mod.ratio=.12;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
bm=bmesh.new();bm.from_mesh(low.data);edges=[e for e in bm.edges if e.is_boundary];border=set(v for e in edges for v in e.verts);copies={v:bm.verts.new((v.co.x,.270,v.co.z)) for v in border};adj={v:[] for v in border}
for e in edges:
 a,b=e.verts;adj[a].append(b);adj[b].append(a);bm.faces.new((a,b,copies[b],copies[a]))
order=[next(iter(border))];prev=None
while True:
 nxt=next((v for v in adj[order[-1]] if v is not prev),None)
 if nxt is None or nxt is order[0]:break
 prev=order[-1];order.append(nxt)
bm.faces.new([copies[v] for v in reversed(order)]);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(low.data);bm.free();parts.append(low)
# Move additions into the same editable collection and create an export copy only.
collection=bpy.data.collections['Editable shaped joinery']
for o in parts:
 for c in list(o.users_collection):c.objects.unlink(o)
 collection.objects.link(o);o.hide_set(False);o.hide_render=False
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
 p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.select_set(True)
bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();game=bpy.context.object;game.name='CM_CW09_HeroCounter';game.data.name=game.name+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
for o in parts+[hi]:o.hide_set(True);o.hide_render=True
game.data.calc_loop_triangles();report={'name':game.name,'triangles':len(game.data.loop_triangles),'vertices':len(game.data.vertices),'materials':[m.name for m in game.data.materials],'workSurfaceMetres':1.0525,'footprintMetres':[2.28,.78],'source':'Workflow08 editable Blender source; unchanged construction reused directly','changes':'Four chamfered joint-posts and bearing knees with drawbore pegs; refined central sculpt and higher focal reduction budget; reused walnut colour tuned and exact registered sculpture value bake.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CounterWorkflow09.blend'));bpy.ops.object.select_all(action='DESELECT');game.select_set(True);bpy.context.view_layer.objects.active=game;game.matrix_world=Matrix.Rotation(math.pi,4,'Z')@game.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM_CW09_HeroCounter.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetReport.json').write_text(json.dumps(report,indent=2));print('COUNTER09_READY',report)
