import bpy,json,numpy as np
from pathlib import Path
D=Path(__file__).resolve().parent;report={}
for label in ['CabinetA','CabinetB']:
 bpy.ops.wm.open_mainfile(filepath=str(D/label/(label+'.blend')));results={}
 for ob in [o for o in bpy.data.objects if o.type=='MESH']:
  m=ob.data;m.calc_loop_triangles();uv=np.array([v.uv[:] for v in m.uv_layers.active.data]);t=np.array([v.loops[:] for v in m.loop_triangles]);a=uv[t[:,1]]-uv[t[:,0]];b=uv[t[:,2]]-uv[t[:,0]];area=abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])*.5
  normals=np.array([v.normal[:] for v in m.vertices]);co=np.array([v.co[:] for v in m.vertices]);tri=np.array([v.vertices[:] for v in m.loop_triangles]);ga=np.linalg.norm(np.cross(co[tri[:,1]]-co[tri[:,0]],co[tri[:,2]]-co[tri[:,0]]),axis=1)*.5
  results[ob.name]={'exact_or_numerically_collapsed_uv_triangles_lt_1e_20':int((area<1e-20).sum()),'subpixel_uv_triangles_lt_half_texel_at_4k':int((area<.5/4096**2).sum()),'geometric_zero_area_triangles_lt_1e_16m2':int((ga<1e-16).sum()),'finite_vertex_normals':bool(np.isfinite(normals).all()),'zero_vertex_normals':int((np.linalg.norm(normals,axis=1)<.1).sum())}
 report[label]=results;print(label,results,flush=True)
(D/'SurfaceDetails.json').write_text(json.dumps(report,indent=2))
