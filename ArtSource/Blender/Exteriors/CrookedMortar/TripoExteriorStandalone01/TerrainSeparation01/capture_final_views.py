import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;vl=s.view_layers[0];cam=s.camera;source=bpy.data.objects['House_Optimized'];col=bpy.data.collections['STANDALONE_WORKING_CANDIDATE'];original_col=bpy.data.collections['OPTIMIZED_GAMEPLAY_CANDIDATE'];source_layer=vl.layer_collection.children[original_col.name];candidate_layer=vl.layer_collection.children[col.name]
s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.cycles.samples=12;s.cycles.use_denoising=True;s.render.film_transparent=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
views=[('FullFront',(0,-24,8),(0,0,4.5),15.8),('FullRear',(0,25,8),(0,1,4.5),15.8),('FullLeft',(-25,0,8),(0,0,4.5),18),('FullRight',(25,0,8),(0,0,4.5),18),('Overview',(16,-24,15),(0,0,4.5),21),('Underside',(12,-18,-14),(0,0,.6),19)]
close=[('PorchLeft',(-9,-14,3),(-2,-4.9,.8),4.4),('PorchRight',(9,-14,3),(1.9,-4.9,.8),4.4),('RockIvyLeft',(-14,-6,2.5),(-2.8,-2.5,.8),4.8),('RockIvyRight',(14,-6,2.5),(2.9,-2.5,.8),4.8),('PlanterLeft',(-14,4,3),(-2.9,3.5,.9),5.2),('PlanterRight',(14,4,3),(2.8,3.5,.9),5.2)]
for name,pos,target,width in views+close:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=width;cam.data.clip_start=.01
 for mode in ['Original','Separated']:
  path=D/(name+'_'+mode+'.png')
  if mode=='Original' and path.exists():continue
  source_layer.exclude=mode!='Original';candidate_layer.exclude=mode=='Original';source.hide_render=mode!='Original';bpy.context.view_layer.update();s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
source_layer.exclude=True;candidate_layer.exclude=False;source.hide_render=True
cam.location=(16,-24,15);cam.rotation_euler=(Vector((0,0,4.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=21
for area in bpy.context.screen.areas if bpy.context.screen else []:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_location=(0,0,4.5);area.spaces.active.region_3d.view_distance=23
bpy.ops.wm.save_as_mainfile(filepath=str(f));print('FINAL_REVIEW_CAPTURED',flush=True)
