import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent
for label in ['CabinetA','CabinetB']:
 bpy.ops.wm.open_mainfile(filepath=str(D/label/(label+'.blend')));s=bpy.context.scene
 s.render.engine='CYCLES';s.cycles.samples=20;s.cycles.use_denoising=True;s.render.resolution_x=1000;s.render.resolution_y=1100;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
 s.world=bpy.data.worlds.new('Neutral studio');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.20,.22,.25,1);s.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
 for p,e,size,col in [((-3,-4,4),450,3,(1,.88,.75)),((3,-2,2.5),300,3,(.8,.9,1)),((1,2,3),400,2,(1,.92,.8))]:
  d=bpy.data.lights.new('StudioArea','AREA');d.energy=e;d.size=size;d.color=col;o=bpy.data.objects.new('StudioArea',d);s.collection.objects.link(o);o.location=p;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
 d=bpy.data.cameras.new('ReviewCamera');cam=bpy.data.objects.new('ReviewCamera',d);s.collection.objects.link(cam);s.camera=cam
 views=[('Front',(0,-5,1.0),(0,0,.97),2.70),('ThreeQuarter',(3,-5,2.5),(0,0,1),2.85),('Side',(5,0,1.1),(0,0,.97),2.70),('CrownDetail',(.65,-3,2),(0,0,1.7),.85),('DrawerDetail',(.5,-3,.85),(0,-.1,.35),.85),('Gameplay',(1.7,-5.5,2.5),(0,0,1),3.8)]
 if '--quick' in sys.argv:views=views[:2]
 if '--remaining' in sys.argv:views=views[2:]
 for state,collname in [('High','01_HIGH_DETAIL_preserved'),('Optimized','02_OPTIMIZED_candidate')]:
  for c in ['01_HIGH_DETAIL_preserved','02_OPTIMIZED_candidate']:
   bpy.data.collections[c].hide_render=c!=collname
  for name,p,target,scale in views:
   cam.location=p;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale
   out=D/label/'Previews';out.mkdir(exist_ok=True);s.render.filepath=str(out/f'{state}_{name}.png');bpy.ops.render.render(write_still=True)
   print('RENDERED',label,state,name,flush=True)
