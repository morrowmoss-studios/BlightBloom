"""Local face-level inspection anchors at previously obscured contacts. No mesh edits."""
import bpy,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend'));s=bpy.context.scene;cam=s.camera
for c in s.view_layers[0].layer_collection.children:
 if c.name.startswith('BOUNDARY'):c.exclude=True
V={a:(b,c,d) for a,b,c,d in json.loads((D.parent/'BoundaryMapping02/Views.json').read_text())}
P={
'LeftRockContact':('RockIvyLeft',[(530,477),(586,450),(610,402),(640,367),(690,342),(750,344),(805,364),(840,411),(870,445),(940,450)]),
'RightRockRootContact':('RockIvyRight',[(175,475),(220,435),(280,417),(330,420),(380,455),(450,470),(540,480),(620,487),(700,490)]),
'RightPorchToe':('PorchRight',[(350,465),(375,482),(412,494),(460,496),(510,493),(560,487),(625,480)]),
'LeftBedToe':('PlanterLeft',[(550,505),(570,520),(690,519),(770,520),(820,518),(838,499),(850,505),(940,505),(975,492)]),
'RightBedToe':('PlanterRight',[(150,477),(170,496),(240,496),(270,488),(285,508),(320,515),(380,512),(450,515),(495,516),(520,492),(600,502)]),
'RearFeet':('Rear',[(142,495),(160,497),(180,488),(900,489),(945,490),(967,480)])}
records={}
for name,(view,pixels) in P.items():
 pos,target,size=V[view];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=size;bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();rows=[]
 for x,y in pixels:
  origin=cam.location+q@Vector(((x/1100-.5)*size,(.5-y/850)*size*850/1100,0));h=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,q@Vector((0,0,-1)));assert h[0]
  rows.append(dict(pixel=[x,y],point=list(h[1]),face=h[3],object=h[4].name))
 records[name]=rows
(D/'LocalContactFacePicks.json').write_text(json.dumps(records,indent=2));print('PICKS_OK',flush=True)
