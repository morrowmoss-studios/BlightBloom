import bpy,json,sys
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CabinetB_Style03_PrototypeB.blend'));s=bpy.context.scene;o=bpy.data.objects['CabinetB_Style03_SameGeometry'];s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.seed=41;s.cycles.use_denoising=True;s.render.resolution_x=1000;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0;s.view_settings.gamma=1
s.world=bpy.data.worlds.new('FIXED neutral comparison world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.16,.16,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.55
for name,p,e,size in [('Fixed key',(-3,-4,4),500,3.0),('Fixed fill',(3,-2,2.5),280,3.0),('Fixed rim',(1,2,3),300,2.5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=e;d.size=size;d.color=(1,1,1);ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=p;ob.rotation_euler=(Vector((0,0,1))-ob.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Fixed comparison camera');cam=bpy.data.objects.new('Fixed comparison camera',d);s.collection.objects.link(cam);s.camera=cam;d.type='PERSP';d.lens=55;d.dof.use_dof=False
views=[('ThreeQuarter',(3,-4.5,2.4),(0,0,1)),('CrownWood',(.55,-1.8,2.05),(.15,0,1.66)),('FoliagePlanter',(-1.65,-1.6,1.55),(-.8,-.08,1.38)),('ContentsBrass',(.25,-1.9,1.05),(.1,0,.69)),('Gameplay',(1.1,-5.5,1.65),(0,0,.95))]
if '--pilot' in sys.argv:views=views[:1]
if '--remaining' in sys.argv:views=views[1:]
states=[('Original','COMPARE_01_RecoveredTripo'),('Style02','COMPARE_02_Style02'),('PrototypeA','COMPARE_03_PrototypeA'),('PrototypeB','COMPARE_04_PrototypeB')]
if '--prototypes-only' in sys.argv:states=states[2:]
if '--b-only' in sys.argv:states=states[3:]
if '--final' in sys.argv:pass
for view,p,target in views:
 cam.location=p;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
 for label,mname in states:
  if '--final' in sys.argv and view=='ThreeQuarter' and label in ['Original','Style02']:continue
  o.data.materials[0]=bpy.data.materials[mname];s.render.filepath=str(D/'Previews'/f'{label}_{view}.png');bpy.ops.render.render(write_still=True);print('RENDERED',label,view,flush=True)
o.data.materials[0]=bpy.data.materials['COMPARE_04_PrototypeB'];cam.location=(3,-4.5,2.4);cam.rotation_euler=(Vector((0,0,1))-cam.location).to_track_quat('-Z','Y').to_euler();bpy.ops.wm.save_as_mainfile(filepath=str(D/'FourWay_Neutral_Review.blend'),compress=True)
(D/'RenderConditions.json').write_text(json.dumps({'all_versions_same_geometry':True,'all_versions_same_rig':True,'lens_mm':55,'samples':24,'seed':41,'resolution':[1000,1100],'view_transform':'AgX Medium High Contrast','exposure':0,'gamma':1,'white_lights':True,'world_color':[.16,.16,.16],'world_strength':.55,'lights':[['key',[-3,-4,4],500,3],['fill',[3,-2,2.5],280,3],['rim',[1,2,3],300,2.5]],'views':[['ThreeQuarter',[3,-4.5,2.4],[0,0,1]],['CrownWood',[.55,-1.8,2.05],[.15,0,1.66]],['FoliagePlanter',[-1.65,-1.6,1.55],[-.8,-.08,1.38]],['ContentsBrass',[.25,-1.9,1.05],[.1,0,.69]],['Gameplay',[1.1,-5.5,1.65],[0,0,.95]]],'no_bloom_fog_blur_dof':True,'denoising':'sampling noise only'},indent=2))
