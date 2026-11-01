import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_WORKING.blend'));s=bpy.context.scene;s.cycles.samples=10;s.render.resolution_x=1200;s.render.resolution_y=900;cam=s.camera
for name,pos,target,width in [('LeftReturn',(-14,-6,2.5),(-2.8,-2.5,.8),4.8),('RightReturn',(14,-6,2.5),(2.9,-2.5,.8),4.8),('ClosedUnderside',(12,-18,-14),(0,0,.6),19)]:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=width;s.render.filepath=str(D/(name+'_Review.png'));bpy.ops.render.render(write_still=True)
o=bpy.data.objects['House_Standalone01'];m=o.data;src=bpy.data.objects['House_Optimized'].data;v=np.empty(len(m.vertices),np.int32);m.attributes['source_vertex_id'].data.foreach_get('value',v);t=np.array([p.vertices[:] for p in src.polygons]);nv=len(src.vertices);e=np.stack([t[:,[0,1]],t[:,[1,2]],t[:,[2,0]]],1).reshape(-1,2);k,c=np.unique(e.min(1).astype('int64')*nv+e.max(1),return_counts=True);old=set(k[c==1].tolist());counts={}
for p in m.polygons:
 for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):counts[tuple(sorted((a,b)))]=counts.get(tuple(sorted((a,b))),0)+1
rows=[]
for (a,b),n in counts.items():
 if n==1:
  x,y=int(v[a]),int(v[b])
  if min(x,y)<0 or min(x,y)*nv+max(x,y) not in old:rows.append(dict(vertices=[a,b],points=[m.vertices[a].co[:],m.vertices[b].co[:]],source=[x,y]))
(D/'ResidualBoundaryInspection.json').write_text(json.dumps(rows,indent=2));print('REMAINING',rows,flush=True)
