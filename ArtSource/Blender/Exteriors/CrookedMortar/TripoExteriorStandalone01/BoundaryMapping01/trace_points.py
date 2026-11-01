"""Manual image picks from all four inspected elevations; ray casting locates guides only."""
import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D.parent/'SeparationInspection_UNCUT.blend'));s=bpy.context.scene;cam=s.camera;cam.data.type='ORTHO';s.render.resolution_x=1400;s.render.resolution_y=950
views={
'Front':dict(pos=(0,-22,4.3),target=(0,-3.6,1.1),size=10.8,pixels=[(390,533),(422,548),(480,553),(505,565),(600,571),(700,574),(804,574),(876,575),(897,586),(947,584),(974,570)]),
'Left':dict(pos=(-22,0,4.3),target=(-1,0,1.1),size=17,pixels=[(1116,522),(1040,532),(926,542),(847,550),(750,550),(667,550),(600,548),(565,552),(482,553),(435,554),(391,551),(300,550),(215,550),(160,551)]),
'Rear':dict(pos=(0,22,4.3),target=(0,4,1.1),size=10.8,pixels=[(333,604),(417,613),(575,615),(736,617),(899,614),(1067,606)]),
'Right':dict(pos=(22,0,4.3),target=(1,0,1.1),size=17,pixels=[(1220,546),(1124,546),(1055,550),(972,550),(926,552),(863,554),(783,551),(730,551),(650,552),(547,550),(500,545),(450,540),(408,533),(354,537),(281,528)])}
out={}
for name,v in views.items():
 cam.location=v['pos'];cam.rotation_euler=(Vector(v['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=v['size'];bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();pts=[]
 for x,y in v['pixels']:
  origin=cam.location+q@Vector(((x/1400-.5)*v['size'],(.5-y/950)*v['size']*950/1400,0));r=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,q@Vector((0,0,-1)))
  pts.append(dict(pixel=[x,y],point=list(r[1]) if r[0] else None,object=r[4].name if r[0] else None))
 out[name]=pts
(D/'ManualElevationPicks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
