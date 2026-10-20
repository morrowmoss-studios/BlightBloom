import bpy,json,math
from pathlib import Path
p=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(p/'BB_PlagueDoctor_Locomotion03.blend'))
r=bpy.data.objects['BB_DoctorRig'];o=bpy.data.objects['DoctorSkin'];s=bpy.context.scene
bad=[v.index for v in o.data.vertices if abs(sum(g.weight for g in v.groups)-1)>.002];samples=[];loops=[]
for a in bpy.data.actions:
 if not a.name.startswith('Doctor03'):continue
 r.animation_data.action=a
 endpoints=[]
 for endpoint in [1,61]:
  s.frame_set(endpoint);bpy.context.view_layer.update();endpoints.append([b.matrix.copy() for b in r.pose.bones])
 loops.append(dict(action=a.name,maxEndpointMatrixDelta=max(abs(endpoints[0][i][j][k]-endpoints[1][i][j][k]) for i in range(len(r.pose.bones)) for j in range(4) for k in range(4))))
 for f in [1,8,16,24,31,39,46,54,61]:
  s.frame_set(f);bpy.context.view_layer.update()
  def bend(a,b,c):return math.degrees((r.pose.bones[b].head-r.pose.bones[a].head).angle(r.pose.bones[c].head-r.pose.bones[b].head))
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();v=[v.co for v in me.vertices]
  samples.append(dict(action=a.name,frame=f,elbowL=bend('UpperArmL','ForearmL','HandL'),elbowR=bend('UpperArmR','ForearmR','HandR'),kneeL=bend('ThighL','ShinL','FootL'),kneeR=bend('ThighR','ShinR','FootR'),min=[min(c[i] for c in v) for i in range(3)],max=[max(c[i] for c in v) for i in range(3)]));ev.to_mesh_clear()
uv=o.data.uv_layers.active.data
report=dict(nonFiniteCoordinates=sum(not all(math.isfinite(x) for x in v.co) for v in o.data.vertices),nonFiniteUVs=sum(not all(math.isfinite(x) for x in u.uv) for u in uv),invalidNormals=sum(not all(math.isfinite(x) for x in f.normal) or f.normal.length<.9 for f in o.data.polygons),loopChecks=loops,vertices=len(o.data.vertices),triangles=sum(len(f.vertices)-2 for f in o.data.polygons),bones=len(r.data.bones),badWeightCount=len(bad),maxInfluences=max(len(v.groups) for v in o.data.vertices),uvLayers=len(o.data.uv_layers),samples=samples)
(p/'SourceValidation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
