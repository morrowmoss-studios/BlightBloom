"""Parametric torus UVs for two plain rope bindings. Geometry/material appearance unchanged."""
import bpy,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;E=D/'Exports';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
for o in s.objects:
 if o.type!='MESH' or not o.name.startswith('Circumferential rope binding'):continue
 me=o.data;vv=[v.co for v in me.vertices];cx=sum(v.x for v in vv)/len(vv);cy=sum(v.y for v in vv)/len(vv);cz=sum(v.z for v in vv)/len(vv);rad=lambda v:math.hypot(v.x-cx,v.y-cy);rr=sum(rad(v) for v in vv)/len(vv)
 for f in me.polygons:
  values=[]
  for li in f.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;values.append([li,math.atan2(v.y-cy,v.x-cx)/math.tau+.5,math.atan2((v.z-cz)/.90,rad(v)-rr)/math.tau+.5])
  for axis in [1,2]:
   if max(v[axis] for v in values)-min(v[axis] for v in values)>.5:
    for v in values:
     if v[axis]<.5:v[axis]+=1
  for li,u,v in values:me.uv_layers[0].data[li].uv=(.01+.48*u,.01+.48*v)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'))
groups={c.name:c for c in s.collection.children};source=(D/'build_cabinet.py').read_text();tail=source[source.index('# FBX transport copies:'):source.index("print('MASTER_CABINET_READY'")];exec(tail);print('FINAL_ROPE_UV_EXPORT_READY')
