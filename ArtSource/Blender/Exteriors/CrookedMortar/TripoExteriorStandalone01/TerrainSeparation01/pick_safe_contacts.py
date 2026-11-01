import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend'));s=bpy.context.scene;cam=s.camera
for c in s.view_layers[0].layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=True
V={a:(b,c,d) for a,b,c,d in json.loads((D.parent/'BoundaryMapping02/Views.json').read_text())};Q=json.loads((D/'LocalContactFacePicks.json').read_text())
for name,view,pixels in [('LeftRockContact','RockIvyLeft',[(530,477),(600,482),(680,482),(760,477),(825,467),(870,455),(940,450)]),('RightRockRootContact','RockIvyRight',[(175,520),(250,536),(330,546),(430,553),(520,565),(620,570),(710,557),(770,540),(810,519),(850,508),(900,500)])]:
 pos,target,size=V[view];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();rows=[]
 for x,y in pixels:
  origin=cam.location+q@Vector(((x/1100-.5)*size,(.5-y/850)*size*850/1100,0));h=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,q@Vector((0,0,-1)));assert h[0];rows.append(dict(pixel=[x,y],point=list(h[1]),face=h[3],object=h[4].name))
 Q[name]=rows
P=json.loads((D.parent/'BoundaryMapping02/ManualCloseupPicks.json').read_text());Q['LeftBedToe']=P['PlanterLeft'][4:];Q['RightBedToe']=P['PlanterRight'][1:9]
(D/'SafeContactFacePicks.json').write_text(json.dumps(Q,indent=2));print('SAFE_CONTACTS_PICKED')
