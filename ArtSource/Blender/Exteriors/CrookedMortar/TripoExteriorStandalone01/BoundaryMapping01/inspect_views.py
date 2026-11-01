import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;src=D.parent/'SeparationInspection_UNCUT.blend'
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;s.render.resolution_x=1400;s.render.resolution_y=950;s.cycles.samples=16;s.cycles.use_denoising=True
cam=s.camera;cam.data.clip_start=.01
views=[('Front',(0,-22,4.3),(0,-3.6,1.1),10.8),('Rear',(0,22,4.3),(0,4,1.1),10.8),('Left',(-22,0,4.3),(-1,0,1.1),17),('Right',(22,0,4.3),(1,0,1.1),17),('FoundationPlan_SectionOnly',(0,0,22),(0,0,0),17)]
for name,pos,target,size in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;cam.data.clip_start=20.6 if name.startswith('FoundationPlan') else .01;s.render.filepath=str(D/(name+'_Baseline.png'));bpy.ops.render.render(write_still=True)
