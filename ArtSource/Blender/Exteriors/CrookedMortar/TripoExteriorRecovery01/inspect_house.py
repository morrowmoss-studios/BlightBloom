import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;ROOT=D.parents[4];src=ROOT/'ArtSource/Blender/Architecture/CrookedMortar/TripoImports/storybook cottage 3d model.glb'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(src))
col=bpy.data.collections.new('ORIGINAL_HIGH_DETAIL_UNTOUCHED');bpy.context.scene.collection.children.link(col)
report=[]
for o in list(bpy.context.scene.objects):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o)
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();co=np.empty(len(m.vertices)*3);m.vertices.foreach_get('co',co);co=co.reshape(-1,3)
 ed=np.empty(len(m.edges)*2,dtype=np.int32);m.edges.foreach_get('vertices',ed);ed=ed.reshape(-1,2)
 parent=np.arange(len(co))
 def find(a):
  while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
  return a
 for a,b in ed:
  a=find(a);b=find(b)
  if a!=b:parent[b]=a
 roots=np.array([find(i) for i in range(len(co))]);u,cnt=np.unique(roots,return_counts=True)
 loops=np.empty(len(m.loops),dtype=np.int32);m.loops.foreach_get('vertex_index',loops)
 tri=np.array([p.vertices[:] for p in m.loop_triangles]);uv=np.empty(len(m.loops)*2);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);tl=np.array([p.loops[:] for p in m.loop_triangles]);tuv=uv[tl];area=np.abs(np.cross(tuv[:,1]-tuv[:,0],tuv[:,2]-tuv[:,0]))*.5
 # edge face usage via triangle endpoint pairs
 ee=np.sort(np.concatenate([tri[:,[0,1]],tri[:,[1,2]],tri[:,[2,0]]]),axis=1);_,ec=np.unique(ee,axis=0,return_counts=True)
 islands=[]
 for r,n in sorted(zip(u,cnt),key=lambda x:-x[1])[:60]:
  pts=co[roots==r];islands.append(dict(root=int(r),vertices=int(n),min=pts.min(0).tolist(),max=pts.max(0).tolist()))
 report.append(dict(name=o.name,vertices=len(co),triangles=len(tri),bounds=[co.min(0).tolist(),co.max(0).tolist()],uv_layers=[l.name for l in m.uv_layers],uv_collapsed_triangles=int((area<1e-14).sum()),uv_subpixel_triangles=int((area<.5/4096**2).sum()),open_edges=int((ec==1).sum()),nonmanifold_edges=int((ec>2).sum()),island_count=len(u),largest_islands=islands))
np.savez_compressed(D/'InspectionArrays.npz',co=co,tri=tri,uv=uv,tri_loops=tl,roots=roots)
rep=dict(meshes=report,textures=[dict(name=i.name,size=list(i.size),colorspace=i.colorspace_settings.name) for i in bpy.data.images if i.type=='IMAGE'])
(D/'Inspection.json').write_text(json.dumps(rep,indent=2));print(json.dumps(rep,indent=2)[:16000])
bpy.ops.wm.save_as_mainfile(filepath=str(D/'OriginalReference.blend'))
# Consistent broad, neutral inspection illumination, native source dimensions.
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('InspectionWorld');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
lo=co.min(0);hi=co.max(0);center=Vector((lo+hi)/2);span=float(max(hi-lo))
for p,e in [((-2,-3,4),500),((3,-1,2),250),((1,3,3),350)]:
 d=bpy.data.lights.new('InspectionArea','AREA');d.energy=e*span**2;d.shape='DISK';d.size=span*2;o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=center+Vector(p)*span;o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('InspectionCamera');cam=bpy.data.objects.new(d.name,d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=span*1.48;d.clip_end=span*100
for name,pos in [('front',(1,-2,1)),('rear',(-1,2,1)),('left',(-2,-1,1)),('roof',(1,-1,2.5))]:
 cam.location=center+Vector(pos)*span;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(D/f'Inspect_{name}.png');bpy.ops.render.render(write_still=True)
