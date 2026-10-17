"""Read-only source/alpha audit; does not save or edit Blender source."""
import bpy,bmesh,json,math
from pathlib import Path
out=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(out/'CM_BotanicalPlanterKit01.blend'))
atlas=next(im for im in bpy.data.images if im.name.startswith('CM_BotanicalElements01'));W,H=atlas.size;px=list(atlas.pixels);solid=0;leaf=0;triangles=0;uvbad=0;area=0;covered=0
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();triangles+=len(m.loop_triangles);uv=m.uv_layers[0];bm=bmesh.new();bm.from_mesh(m)
 if o.get('solid'):
  solid+=1;assert all(e.is_manifold for e in bm.edges),o.name;assert bm.calc_volume(signed=True)>0,o.name
 else:leaf+=1
 bm.free()
 for t in m.loop_triangles:
  assert t.area>1e-12
  vals=[uv.data[i].uv for i in t.loops];a,b,c=vals;assert abs((b-a).cross(c-a))>1e-13,o.name;assert all(math.isfinite(q) and 0<=q<=1 for p in vals for q in p)
  if not o.get('leaf'):continue
  area+=t.area
  count=0;hits=0
  for i in range(1,5):
   for j in range(1,6-i):
    u=a*(i/6)+b*(j/6)+c*(1-(i+j)/6);x=min(W-1,max(0,int(u.x*W)));y=min(H-1,max(0,int(u.y*H)));hits+=px[(y*W+x)*4+3]>=.42;count+=1
  covered+=t.area*hits/count
for u,v in [(.44,.75),(.87,.25)]:
 assert all(px[(int((v+dy)*H)*W+int((u+dx)*W))*4+3]>=.42 for dx in [-.003,0,.003] for dy in [-.003,0,.003]),'Stem paint must remain opaque'
catalog=json.loads((out/'ModuleCatalog.json').read_text());a=sum(x['lods'][0]['triangles'] for x in catalog if len(x['lods'])>1);b=sum(x['lods'][1]['triangles'] for x in catalog if len(x['lods'])>1)
report={'solidSourceParts':solid,'openShapedLeafParts':leaf,'sourceTriangles':triangles,'degenerateGeometryOrUVs':0,'invalidNormals':sum(any(not math.isfinite(v) for v in p.normal) for o in bpy.context.scene.objects if o.type=='MESH' for p in o.data.polygons),'foliageLOD0Triangles':a,'foliageLOD1Triangles':b,'foliageLODReductionFraction':1-b/a,'alphaAcceptedSampledLeafAreaFraction':covered/area,'alphaCutoff':.42,'stemPaintPatchesOpaque':True,'uniquePaintingAtlas':False,'notes':'Intentional shared leaf-sprite and paint-trim UV reuse. Alpha-area sampling estimates mask waste on leaf surfaces, not screen-space overlap or GPU frame time; open foliage boundaries are intentional.'}
(out/'SourceValidation.json').write_text(json.dumps(report,indent=2));print('SOURCE_VALIDATED',json.dumps(report))
