import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_BotanicalCabinet_Style02.blend'));s=bpy.context.scene;o=bpy.data.objects['CM_BotanicalCabinet_Style02'];styled=o.data.materials[0]
with bpy.data.libraries.load(str(D.parent/'TripoCabinetRecovery01/CabinetB/CabinetB.blend'),link=False) as (a,b):b.materials=[x for x in a.materials if x.startswith('tripo_material')]
before=b.materials[0];before.use_fake_user=True
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=32;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1200;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
s.world=bpy.data.worlds.new('Soft sage studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.145,.135,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.55
for p,e,size,col in [((-3,-4,4),500,3.2,(1,.85,.69)),((3,-2,2.5),230,3,(.80,.89,1)),((1,2,3),350,2.5,(1,.91,.75))]:
 d=bpy.data.lights.new('Soft studio area','AREA');d.energy=e;d.size=size;d.color=col;ob=bpy.data.objects.new('Soft studio area',d);s.collection.objects.link(ob);ob.location=p;ob.rotation_euler=(Vector((0,0,1))-ob.location).to_track_quat('-Z','Y').to_euler()
# Seamless physical cyclorama; no horizon, compositing blur or fog.
profile=[(-50,-.002),(2,-.002)]+[(2+3*math.sin(i*math.pi/80),3-3*math.cos(i*math.pi/80)-.002) for i in range(1,41)]+[(5,30)]
verts=[(x,y,z) for y,z in profile for x in [-50,50]];faces=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(profile)-1)]
me=bpy.data.meshes.new('Review cyclorama');me.from_pydata(verts,[],faces);ground=bpy.data.objects.new('REVIEW_ONLY_Cyclorama',me);s.collection.objects.link(ground)
for poly in me.polygons:poly.use_smooth=True
mat=bpy.data.materials.new('Matte warm charcoal');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.065,.073,.064,1);bs.inputs['Roughness'].default_value=1;ground.data.materials.append(mat)
d=bpy.data.cameras.new('Review camera');cam=bpy.data.objects.new('Review camera',d);s.collection.objects.link(cam);s.camera=cam
views=[('ThreeQuarter',(3,-4.5,2.4),(0,0,1),'PERSP',55),('Front',(0,-4.8,1.05),(0,0,.97),'ORTHO',2.7),('Side',(4.8,0,1.05),(0,0,.97),'ORTHO',2.7),('Gameplay',(1.1,-4.4,1.65),(0,0,1),'PERSP',50),('FinishDetail',(.65,-2.5,.8),(.2,-.2,.40),'ORTHO',1.0)]
if '--quick' in sys.argv:views=views[:1]
if '--rest' in sys.argv:views=views[1:]
if '--detail' in sys.argv:views=views[-1:]
if '--skip-detail' in sys.argv:views=views[:-1]
for name,p,target,typ,setting in views:
 cam.location=p;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();d.type=typ
 if typ=='ORTHO':d.ortho_scale=setting
 else:d.lens=setting
 for label,material in [('Before',before),('Style02',styled)]:
  if '--styled-only' in sys.argv and label=='Before':continue
  if '--reuse-threequarter' in sys.argv and label=='Style02' and name=='ThreeQuarter':continue
  o.data.materials[0]=material;s.render.filepath=str(D/'Previews'/f'{label}_{name}.png');bpy.ops.render.render(write_still=True);print('RENDERED',label,name,flush=True)
o.data.materials[0]=styled
cam.location=(3,-4.5,2.4);cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();d.type='PERSP';d.lens=55
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_Cabinet_Style02_RenderReview.blend'),compress=True)
(D/'ReviewLighting.json').write_text(json.dumps({'matching_before_after':True,'views':views,'engine':'Cycles CPU 32samples, denoised only for sampling noise','exposure':0,'bloom':False,'depth_of_field':False},indent=2))
