import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(D.parent/'BoundaryMapping01/CM_CrookedMortar_BoundaryMapping01_UNCUT.blend'))
s=bpy.context.scene;cam=s.camera
for c in s.view_layers[0].layer_collection.children:
 if c.name.startswith('BOUNDARY_MAPPING'):c.exclude=True
s.render.resolution_x=1100;s.render.resolution_y=850;s.render.resolution_percentage=100;s.cycles.samples=12;s.cycles.use_denoising=True
views=[('PorchLeft',(-9,-14,3),(-2,-4.9,.8),4.4),('PorchRight',(9,-14,3),(1.9,-4.9,.8),4.4),('RockIvyLeft',(-14,-6,2.5),(-2.8,-2.5,.8),4.8),('RockIvyRight',(14,-6,2.5),(2.9,-2.5,.8),4.8),('PlanterLeft',(-14,4,3),(-2.9,3.5,.9),5.2),('PlanterRight',(14,4,3),(2.8,3.5,.9),5.2),('Rear',(1,18,3),(0,6.2,.9),7.6),('RearUnder',(8,14,-3),(0,5.8,.5),8)]
(D/'Views.json').write_text(json.dumps(views,indent=2))
for name,pos,target,size in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;cam.data.clip_start=.01;s.render.filepath=str(D/(name+'_House.png'));bpy.ops.render.render(write_still=True)
