"""Real standalone Blender renders; neutral studio. No reference projection or generated beauty shot."""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));s=bpy.context.scene
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=1280;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s.world=bpy.data.worlds.new('Neutral review world') if s.world is None else s.world
s.world.color=(.14,.14,.14);s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
world=s.world;world.use_nodes=True;world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.18,.20,.23,1);world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.42
# Separate unsaved studio collection; no studio meshes in delivered exports/source.
studio=bpy.data.collections.new('RENDER_STUDIO_ONLY');s.collection.children.link(studio)
def area(n,p,power,size,col,target=(0,1.1,0)):
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=col;o=bpy.data.objects.new(n,d);studio.objects.link(o);o.location=(p[0],p[2],p[1]);q=Vector((target[0],target[2],target[1]))-o.location;o.rotation_euler=q.to_track_quat('-Z','Y').to_euler()
area('Broad warm key',(-2.7,3.8,3.0),400,3.0,(1,.84,.68));area('Soft neutral fill',(2.4,2.8,2.2),240,2.8,(.78,.87,1));area('Upper edge light',(.0,3.3,-2),350,2.4,(1,.90,.74))
# Matte neutral ground; no glossy reflection or fog.
me=bpy.data.meshes.new('Studio ground');me.from_pydata([(-200,-200,-.012),(200,-200,-.012),(200,200,-.012),(-200,200,-.012)],[],[(0,1,2,3)]);o=bpy.data.objects.new('Neutral ground',me);studio.objects.link(o);m=bpy.data.materials.new('Studio charcoal');m.diffuse_color=(.055,.06,.065,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.055,.06,.065,1);m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=1;me.materials.append(m)
camD=bpy.data.cameras.new('Review Camera');cam=bpy.data.objects.new('Review Camera',camD);studio.objects.link(cam);s.camera=cam
saved={o:list(o.data.materials) for o in s.objects if o.type=='MESH' and o!=bpy.data.objects['Neutral ground']};clay=bpy.data.materials.new('Review neutral clay');clay.use_nodes=True;bs=clay.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.42,.40,.36,1);bs.inputs['Roughness'].default_value=.9
views=[('Front',(0,1.10,4.5),(0,1.07,0),2.45,False),('ThreeQuarter',(3.15,2.3,4.0),(0,1.05,0),2.60,False),('Side',(4,1.15,.02),(0,1.06,.02),2.42,False),('Clay',(3.15,2.3,4),(0,1.05,0),2.60,True),('WoodAndDrawers',(.66,.77,2.2),(.33,.41,.12),1.06,False),('MossDetail',(.60,.38,1.3),(.53,.19,.205),.38,False),('BotanicalAndPlanter',(1.25,1.73,2.0),(.60,1.53,.22),.90,False),('Back',(2.8,2.25,-4.0),(0,1.05,0),2.60,False)]
if "--quick" in sys.argv:views=views[:2]
if "--paint-finish" in sys.argv:views=[v for v in views if v[0]!="Clay"]
if "--back-only" in sys.argv:views=[v for v in views if v[0]=="Back"]
if "--final-details" in sys.argv:views=[v for v in views if v[0] in ["MossDetail","Back"]]
report=[]
for name,p,target,scale,isclay in views:
 for o,materials in saved.items():
  o.hide_render=isclay and o.get('logical_group','').startswith(('06_','07_','08_'))
  if isclay:
   for i in range(len(o.data.materials)):o.data.materials[i]=clay
  else:
   for i,m in enumerate(materials):o.data.materials[i]=m
 cam.location=(p[0],p[2],p[1]);q=Vector((target[0],target[2],target[1]))-cam.location;cam.rotation_euler=q.to_track_quat('-Z','Y').to_euler();camD.type='PERSP' if name in ['ThreeQuarter','Back'] else 'ORTHO';camD.lens=55;camD.ortho_scale=scale;s.render.filepath=str(D/'Previews'/f'{name}.png');bpy.ops.render.render(write_still=True);report.append({'view':name,'cameraUnity':p,'targetUnity':target,'orthoScale':scale,'clay':isclay})
(D/'RenderViews.json').write_text(json.dumps({'method':'Cycles CPU neutral studio, actual asset geometry and materials; no reference backdrop. Studio not saved to asset/source/export.','views':report},indent=2));print('CABINET_RENDERS_READY')
