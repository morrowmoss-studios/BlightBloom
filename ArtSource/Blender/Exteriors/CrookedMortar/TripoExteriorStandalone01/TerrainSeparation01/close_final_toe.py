import bpy,bmesh,numpy as np,json,hashlib
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_TerrainSeparated01.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;o=bpy.data.objects['House_Standalone01'];me=o.data;m=bpy.data.objects['House_Optimized'].data;report=json.loads((D/'FinalValidation.json').read_text());assert report['new_open_boundary_edges']==13
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();fid=bm.faces.layers.int['source_face_id'];sid=bm.verts.layers.int['source_vertex_id'];edges=[bm.edges.get(tuple(bm.verts[i] for i in r['vertices'])) for r in report['new_open_edges']];assert all(e is not None for e in edges)
verts=list({v for e in edges for v in e.verts});p=sum((v.co for v in verts),Vector())/len(verts);p.z-=.002;c=bm.verts.new(p);c[sid]=-1;uv=bm.loops.layers.uv.get(me.uv_layers[0].name);slot=me.materials.find('CM_Standalone_LocalFoundationReturns')
for e in edges:
 l=next(l for l in e.link_faces[0].loops if l.edge==e);a,b=l.vert,l.link_loop_next.vert;face=bm.faces.new([b,a,c]);face[fid]=-1;face.material_index=slot
 for loop in face.loops:loop[uv].uv=(loop.vert.co.x/1.1,loop.vert.co.y/.65)
bm.normal_update();bm.to_mesh(me);bm.free();me.update();A=np.load(D/'Topology.npz');tri=A['tri'];nv=len(A['co']);ids=np.empty(len(me.polygons),np.int32);me.attributes['source_face_id'].data.foreach_get('value',ids);vs=np.empty(len(me.vertices),np.int32);me.attributes['source_vertex_id'].data.foreach_get('value',vs);norm=np.empty(len(m.loops)*3,np.float32);m.corner_normals.foreach_get('vector',norm);norm=norm.reshape(-1,3,3);normal=[]
for p in me.polygons:
 i=int(ids[p.index])
 if i>=0:
  for vi in p.vertices:normal.append(norm[i,int(np.where(tri[i]==vs[vi])[0][0])].tolist())
 else:normal.extend([p.normal[:]]*len(p.vertices))
me.normals_split_custom_set(normal)
# Recheck every final exposed boundary against inherited source edges.
e=np.stack([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]],1).reshape(-1,2);kk,cc=np.unique(e.min(1).astype('int64')*nv+e.max(1),return_counts=True);oldopen=set(kk[cc==1].tolist());counts={}
for p in me.polygons:
 for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]):key=tuple(sorted((a,b)));counts[key]=counts.get(key,0)+1
newopen=[]
for (a,b),n in counts.items():
 if n==1:
  x,y=int(vs[a]),int(vs[b])
  if min(x,y)<0 or min(x,y)*nv+max(x,y) not in oldopen:newopen.append([a,b])
assert not newopen,newopen
report['new_open_boundary_edges']=0;report['new_open_edges']=[];report['new_closure_triangles']=int((ids<0).sum());report['final_body_triangles']=len(me.polygons);report['final_total_triangles']=len(me.polygons)+report['other_render_triangles'];report['final_toe_closure']={'boundary_edges':13,'max_span_m':.14,'added_center_vertices':1,'added_triangles':13};report['new_degenerate_closure_triangles']=sum(p.area<1e-10 for p in me.polygons if ids[p.index]<0)
(D/'FinalValidation.json').write_text(json.dumps(report,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(f));print('FINAL_BOUNDARY_OK',report['final_total_triangles'],flush=True)
# Refresh the affected close-up and underside, not all passing views.
cam=s.camera;s.render.resolution_x=1400;s.render.resolution_y=1000;s.cycles.samples=12
for name,pos,target,width in [('PorchRight',(9,-14,3),(1.9,-4.9,.8),4.4),('Underside',(12,-18,-14),(0,0,.6),19)]:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=width;s.render.filepath=str(D/(name+'_Separated.png'));bpy.ops.render.render(write_still=True)
