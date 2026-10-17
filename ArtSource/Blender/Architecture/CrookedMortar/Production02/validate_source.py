"""Read-only current .blend validation; writes only the new candidate report."""
import bpy,bmesh,json,math
from pathlib import Path
O=Path(__file__).parent
assert bpy.app.background
bpy.ops.wm.open_mainfile(filepath=str(O/'CM_CrookedMortar_Production02.blend'))
report=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 me=o.data;bm=bmesh.new();bm.from_mesh(me);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();me.calc_loop_triangles();deg=sum(t.area<1e-11 for t in me.loop_triangles);uv=me.uv_layers[0];finite=all(math.isfinite(p.uv.x) and math.isfinite(p.uv.y) and 0<=p.uv.x<=1 and 0<=p.uv.y<=1 for p in uv.data)
 entry=dict(name=o.name,nonmanifold=bad,volume=volume,degenerate=deg,triangles=len(me.loop_triangles),uv0=uv.name,uvValid=finite);report.append(entry)
 assert bad==0 and volume>0 and deg==0 and finite,entry
(O/'GeometryValidation.json').write_text(json.dumps(report,indent=2));print('SOURCE_VALIDATED',len(report),sum(e['triangles'] for e in report))
