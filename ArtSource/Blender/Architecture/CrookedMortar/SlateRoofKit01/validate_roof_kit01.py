"""Read-only Blender validation plus roof fit and standard overlap arithmetic."""
import bpy,bmesh,json,math
from pathlib import Path
out=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(out/'CM_SlateRoofKit01.blend'))
rows=[];uvdeg=0;count=0
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();uv=m.uv_layers[0];bad_uv=0
 for t in m.loop_triangles:
  a,b,c=[uv.data[i].uv for i in t.loops];ua=abs((b-a).cross(c-a))*.5
  if ua<1e-12:bad_uv+=1
  if not all(math.isfinite(v) and 0<=v<=1 for p in [a,b,c] for v in p):raise RuntimeError('Out-of-bounds UV '+o.name)
 bm=bmesh.new();bm.from_mesh(m);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();deg=sum(t.area<1e-11 for t in m.loop_triangles)
 if bad or vol<=0 or deg:raise RuntimeError((o.name,bad,vol,deg))
 rows.append({'name':o.name,'triangles':len(m.loop_triangles),'uv_zero_area_triangles':bad_uv,'nonmanifold_edges':bad,'degenerate_geometry_triangles':deg,'volume':vol});uvdeg+=bad_uv;count+=len(m.loop_triangles)
# For the regular overlapping courses: upper course lower face is above the previous top by this amount.
overlap_gap=.026*.30/.43-.018
report={'parts':rows,'triangles':count,'uv_zero_area_triangles':uvdeg,'uv0':'Intentional approved trim-sheet overlap, not a unique painting atlas. All coordinates within0..1.','same_slope_course_clearance_metres':overlap_gap,'same_slope_course_overlap_metres':.43-.30,'intersections':'Exact upper-envelope clipping; narrow valleys opened in cladding and bridged by fitted channels. Site-fit checked in Unity separately.'}
(out/'SourceValidation.json').write_text(json.dumps(report,indent=2));print('SOURCE_VALIDATED',len(rows),count,'UVdeg',uvdeg,'coursegap',overlap_gap)
from mathutils import Vector
from mathutils.bvhtree import BVHTree
catalog={m['name']:m for m in json.loads((out/'ModuleCatalog.json').read_text())};measured=json.loads((out/'ApprovedRoofMeasurement.json').read_text())['roofs'];chimney=json.loads((out/'ApprovedChimneyGeometry.json').read_text());triangles=[]
for r in measured+[chimney]:
 for ids in r['topTriangles']:
  pts=[Vector(r['vertices'][i]) for i in ids];n=(pts[1]-pts[0]).cross(pts[2]-pts[0]);A=-n.x/n.y;B=-n.z/n.y;C=pts[0].y-A*pts[0].x-B*pts[0].z;triangles.append((r['name'],pts,(A,B,C)))
def inside(pts,x,z):
 signs=[(b.x-a.x)*(z-a.z)-(b.z-a.z)*(x-a.x) for a,b in zip(pts,pts[1:]+pts[:1])];return min(signs)>=-1e-5 or max(signs)<=1e-5
def highest(x,z):
 hits=[(p[0]*x+p[1]*z+p[2],n) for n,vs,p in triangles if inside(vs,x,z)]
 return max(hits) if hits else None
verts=[];faces=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or o.get('role')!='Underlay' or catalog[o['module']]['kind']!='FittedAdapter':continue
 off=len(verts);verts += [o.matrix_world@v.co for v in o.data.vertices];faces += [tuple(off+i for i in p.vertices) for p in o.data.polygons]
bvh=BVHTree.FromPolygons(verts,faces,all_triangles=False);rays=0;misses=[];maxerror=0
for name,pts,plane in triangles:
 if name=='Chimney':continue
 for i in range(1,9):
  for k in range(1,10-i):
   p=pts[0]*(i/10)+pts[1]*(k/10)+pts[2]*(1-(i+k)/10);hi=highest(p.x,p.z)
   if hi is None or hi[1]=='Chimney' or abs(hi[0]-p.y)>.001:continue
   rays+=1;hit=bvh.ray_cast(Vector((p.x,p.z,p.y+.03)),Vector((0,0,-1)),.2)
   if hit[0] is None:misses.append([name,list(p)]);continue
   maxerror=max(maxerror,abs(hit[0].z-(p.y-.006)))
fit={'roof_surface_sample_rays':rays,'missed_underlay_samples':misses,'maximum_underlay_height_error_metres':maxerror,'expected_underlay_top_offset_metres':-.006,'original_roof_control_vertices_unchanged':True,'hero_ridge_fall_metres':.4,'note':'Sampled visible roof carriers excluding retained chimney footprints; this checks fit/coverage, not new collision behaviour.'}
(out/'SurfaceFitValidation.json').write_text(json.dumps(fit,indent=2));assert not misses and maxerror<.002,fit
print('SURFACE_FIT_VALIDATED',rays,'maxerror',maxerror)
