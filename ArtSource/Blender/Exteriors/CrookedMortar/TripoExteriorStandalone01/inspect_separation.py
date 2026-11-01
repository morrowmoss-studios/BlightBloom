"""Read-only source geometry analysis. Scene additions are saved to a NEW inspection file only."""
import bpy,numpy as np,json,hashlib
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;S=D.parent/'TripoExteriorRecovery01';src=S/'CrookedMortar_Optimized.blend'
bpy.ops.wm.open_mainfile(filepath=str(src));col=bpy.data.collections['OPTIMIZED_GAMEPLAY_CANDIDATE'];body=bpy.data.objects['House_Optimized'];m=body.data
co=np.empty(len(m.vertices)*3);m.vertices.foreach_get('co',co);co=co.reshape(-1,3)
ed=np.empty(len(m.edges)*2,dtype=np.int32);m.edges.foreach_get('vertices',ed);ed=ed.reshape(-1,2)
parent=np.arange(len(co),dtype=np.int32)
def find(x):
 while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
 return x
for a,b in ed:
 a=find(a);b=find(b)
 if a!=b:parent[b]=a
roots=np.array([find(i) for i in range(len(co))]);loops=np.empty(len(m.loops),dtype=np.int32);m.loops.foreach_get('vertex_index',loops);tri=loops.reshape(-1,3);tr=roots[tri[:,0]]
parts=[]
for r,num in zip(*np.unique(tr,return_counts=True)):
 pts=co[roots==r];parts.append(dict(root=int(r),triangles=int(num),vertices=len(pts),min=pts.min(0).tolist(),max=pts.max(0).tolist()))
parts.sort(key=lambda x:-x['triangles']);p=co[tri];ct=p.mean(1)
# Counts are diagnostic only: NEVER use a height threshold as a deletion mask.
levels={str(z):dict(triangles_crossing=int(((p[:,:,2].min(1)<z)&(p[:,:,2].max(1)>z)).sum()),vertices_below=int((co[:,2]<z).sum())) for z in [.10,.25,.4,.6,.9,1.15]}
rep=dict(source=str(src),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),body_vertices=len(co),body_triangles=len(tri),visible_mesh_objects=[dict(name=o.name,triangles=sum(len(p.vertices)-2 for p in o.data.polygons),uv_layers=[l.name for l in o.data.uv_layers]) for o in col.objects if o.type=='MESH'],body_components=parts,height_threshold_diagnostics_NOT_DELETION_RULES=levels)
(D/'SeparationInspection.json').write_text(json.dumps(rep,indent=2));np.savez_compressed(D/'InspectionArrays.npz',co=co,tri=tri,roots=roots)
print(json.dumps(rep,indent=2)[:10000],flush=True)
# Matched neutral views of the actual recovered asset, including underside; no parts removed.
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('InspectionNeutralWorld');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.22,.22,.22,1)
for pos,power in [((12,-17,20),4500),((-14,-9,8),2500),((0,10,-10),3000)]:
 ld=bpy.data.lights.new('InspectionLight','AREA');ld.energy=power;ld.size=12;ob=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector((0,0,3))-ob.location).to_track_quat('-Z','Y').to_euler()
cd=bpy.data.cameras.new('InspectionCamera');cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);s.camera=cam;cd.type='ORTHO';cd.clip_start=.01;cd.clip_end=200
views=[('Existing_FrontThreeQuarter',(16,-24,14),(0,0,4.5),20),('Existing_Underside',(12,-18,-14),(0,0,.6),18),('FoundationAndStoop',(9,-17,3.3),(0,-3.9,.9),10),('Existing_Plan',(0,0,28),(0,0,0),18)]
for name,pos,target,size in views:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.ortho_scale=size;s.render.filepath=str(D/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'SeparationInspection_UNCUT.blend'))
