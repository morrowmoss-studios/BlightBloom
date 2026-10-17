"""Read-only source mesh/UV audit; writes a report and UV template beside source."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
out=Path(__file__).parent
bpy.ops.wm.open_mainfile(filepath=str(out/'CM_Redesign01_Geometry.blend'))
triangles=[];ratios=[];uv_bounds=[];owners=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();uv=m.uv_layers.active
 for t in m.loop_triangles:
  pts=[tuple(uv.data[i].uv) for i in t.loops];uv_bounds+=pts
  area=abs((pts[1][0]-pts[0][0])*(pts[2][1]-pts[0][1])-(pts[1][1]-pts[0][1])*(pts[2][0]-pts[0][0]))*.5
  a,b,c=[o.matrix_world@m.vertices[i].co for i in t.vertices];worldarea=(b-a).cross(c-a).length*.5
  if area>1e-12 and worldarea>1e-10:ratios.append(math.sqrt(area/worldarea))
  triangles.append(pts);owners.append((o.name,t.polygon_index))
assert all(-1e-6<=p[i]<=1.000001 for p in uv_bounds for i in [0,1])
# Convex polygon clipping reports positive-area overlaps, ignoring shared edges.
def intersect_area(a,b):
 clip=list(b)
 if sum(clip[i][0]*clip[(i+1)%3][1]-clip[(i+1)%3][0]*clip[i][1] for i in range(3))<0:clip.reverse()
 poly=list(a)
 for i in range(3):
  q,r=clip[i],clip[(i+1)%3]
  def d(p):return (r[0]-q[0])*(p[1]-q[1])-(r[1]-q[1])*(p[0]-q[0])
  prev=poly[-1] if poly else None;new=[]
  for cur in poly:
   dc,dp=d(cur),d(prev)
   if (dc>=0)!=(dp>=0):
    t=dp/(dp-dc);new.append((prev[0]+t*(cur[0]-prev[0]),prev[1]+t*(cur[1]-prev[1])))
   if dc>=0:new.append(cur)
   prev=cur
  poly=new
  if not poly:return 0
 return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))*.5
buckets={};tested=set();overlaps=[]
for idx,tri in enumerate(triangles):
 x0,x1=[int(v*64) for v in [min(p[0] for p in tri),max(p[0] for p in tri)]];y0,y1=[int(v*64) for v in [min(p[1] for p in tri),max(p[1] for p in tri)]]
 for x in range(x0,x1+1):
  for y in range(y0,y1+1):
   bucket=buckets.setdefault((x,y),[])
   for other in bucket:
    pair=(other,idx)
    if pair in tested:continue
    tested.add(pair)
    if intersect_area(tri,triangles[other])>1e-9:overlaps.append(pair)
   bucket.append(idx)
(out/'uv_overlap_details.json').write_text(json.dumps([(owners[a],owners[b],intersect_area(triangles[a],triangles[b])) for a,b in overlaps],indent=2));assert not overlaps,('UV positive-area overlaps',len(overlaps))
r=sorted(ratios);report={'uv_bounds':'within 0..1','positive_area_triangle_overlaps':len(overlaps),'triangles':len(triangles),'uv_linear_scale_p05':r[int(len(r)*.05)],'uv_linear_scale_p50':r[len(r)//2],'uv_linear_scale_p95':r[int(len(r)*.95)],'note':'Unique shared atlas. Small bevel islands and projection distortion cause local texel-density variation; main surfaces averaged together.'}
(out/'uv_validation.json').write_text(json.dumps(report,indent=2))
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4096 4096"><rect width="4096" height="4096" fill="#303030"/><g fill="none" stroke="#cccccc" stroke-width="1">']
for tri in triangles:svg.append('<polygon points="'+' '.join(f'{p[0]*4096:.2f},{(1-p[1])*4096:.2f}' for p in tri)+'"/>')
svg.append('</g></svg>');(out/'CM_Redesign01_UV.svg').write_text('\n'.join(svg))
print('UV_VALIDATION',json.dumps(report))
