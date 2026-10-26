import bpy,math,json,bmesh
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow12.blend'));rows=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();rows.append(dict(name=o.name,triangles=len(me.loop_triangles),vertices=len(me.vertices),uvCount=len(me.uv_layers),badUV=sum(not all(math.isfinite(v) for v in x.uv) for x in me.uv_layers[0].data),badCoordinates=sum(not all(math.isfinite(v) for v in p.co) for p in me.vertices),badNormals=sum(not all(math.isfinite(v) for v in f.normal) or f.normal.length<.9 for f in me.polygons),degenerateTriangles=sum(t.area<1e-12 for t in me.loop_triangles),scale=list(o.scale),pivot=list(o.location)))
report=dict(passed=all(r['uvCount']==1 and not any(r[k] for k in ['badUV','badCoordinates','badNormals','degenerateTriangles']) for r in rows),modules=rows,units=bpy.context.scene.unit_settings.system,scaleLength=bpy.context.scene.unit_settings.scale_length)
(D/'SourceValidation.json').write_text(json.dumps(report,indent=2));print('SOURCE_VALIDATION',report['passed'],len(rows),sum(r['triangles'] for r in rows))
