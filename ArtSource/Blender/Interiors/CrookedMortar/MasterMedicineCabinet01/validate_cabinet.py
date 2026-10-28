import bpy,bmesh,math,json,struct
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));rows=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me);edges=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();uv=me.uv_layers[0]
 uvbad=0
 for t in me.loop_triangles:
  a,b,c=[uv.data[i].uv for i in t.loops];uvbad+=abs((b-a).cross(c-a))<1e-13
 rows.append({'name':o.name,'group':o['logical_group'],'solid':bool(o['solid']),'triangles':len(me.loop_triangles),'nonmanifoldEdges':edges,'signedVolume':vol,'badCoordinates':sum(not all(math.isfinite(v) for v in p.co) for p in me.vertices),'badNormals':sum(not all(math.isfinite(v) for v in f.normal) or f.normal.length<.9 for f in me.polygons),'degenerateTriangles':sum(t.area<1e-12 for t in me.loop_triangles),'uvLayers':len(me.uv_layers),'degenerateUVs':uvbad,'badUVs':sum(not all(math.isfinite(c) for c in x.uv) or min(x.uv)<0 or max(x.uv)>1 for x in uv.data)})
issues=[r for r in rows if r['badCoordinates'] or r['badNormals'] or r['degenerateTriangles'] or r['badUVs'] or r['degenerateUVs'] or r['uvLayers']!=1 or r['solid'] and (r['nonmanifoldEdges'] or r['signedVolume']<=0)]
# Inspect actual GLB structure/embedded images and UV channels without requiring a Unity plugin.
p=(D/'Exports/CM_MasterMedicineCabinet01.glb').read_bytes();length,typ=struct.unpack_from('<II',p,12);g=json.loads(p[20:20+length].decode());stats={'meshes':len(g.get('meshes',[])),'materials':len(g.get('materials',[])),'images':len(g.get('images',[])),'primitives':sum(len(m['primitives']) for m in g['meshes']),'missingUVPrimitives':sum('TEXCOORD_0' not in q['attributes'] for m in g['meshes'] for q in m['primitives']),'missingNormalPrimitives':sum('NORMAL' not in q['attributes'] for m in g['meshes'] for q in m['primitives']),'alphaMaterials':[{ 'name':m['name'],'alphaMode':m.get('alphaMode','OPAQUE'),'doubleSided':m.get('doubleSided',False)} for m in g['materials'] if 'Ivy' in m['name'] or 'Moss' in m['name']]}
report={'passed':not issues,'triangles':sum(r['triangles'] for r in rows),'sourceParts':len(rows),'issues':issues,'parts':rows,'glb':stats,'units':bpy.context.scene.unit_settings.system,'scaleLength':bpy.context.scene.unit_settings.scale_length};(D/'GeometryValidation.json').write_text(json.dumps(report,indent=2));print('CABINET_VALIDATION',report['passed'],'issues',[(r['name'],r['nonmanifoldEdges'],r['degenerateTriangles'],r['degenerateUVs'],r['badUVs']) for r in issues],stats)
