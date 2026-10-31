import bpy,numpy as np,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(__file__).resolve().parent;ROOT=D.parents[4];out={}
bpy.ops.wm.open_mainfile(filepath=str(D/'CrookedMortar_Optimized.blend'))
for c in bpy.data.collections:c.hide_viewport=False
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();h=bpy.data.objects['House_RepairedHigh'];o=bpy.data.objects['House_Optimized']
def check(ob):
 m=ob.data;m.calc_loop_triangles();co=np.empty(len(m.vertices)*3);m.vertices.foreach_get('co',co);co=co.reshape(-1,3);uv=np.empty(len(m.loops)*2);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2);pol=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',pol);pol=pol.reshape(-1,3);q=co[pol];ga=np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1);u=uv.reshape(-1,3,2);a=u[:,1]-u[:,0];b=u[:,2]-u[:,0];ua=abs(a[:,0]*b[:,1]-a[:,1]*b[:,0]);norm=np.empty(len(m.vertices)*3);m.vertices.foreach_get('normal',norm)
 return dict(triangles=len(pol),vertices=len(co),finite_positions=bool(np.isfinite(co).all()),finite_normals=bool(np.isfinite(norm).all()),finite_uvs=bool(np.isfinite(uv).all()),geometric_zero_area=int((ga<1e-15).sum()),collapsed_uv_triangles=int((ua<2e-14).sum()),bounds_native=[co.min(0).tolist(),co.max(0).tolist()],materials=[mat.name for mat in m.materials])
out['repaired_body']=check(h);out['optimized_body']=check(o);errors=[];bad=[]
for src,dst in [(h,o),(o,h)]:
 tree=BVHTree.FromObject(dst,dg)
 for i in range(0,len(src.data.polygons),max(1,len(src.data.polygons)//10000)):
  p=src.data.polygons[i];pt=sum((src.data.vertices[k].co for k in p.vertices),Vector())/3;world=src.matrix_world@pt;local=dst.matrix_world.inverted()@world;near=tree.find_nearest(local)
  if near:
   e=(world-dst.matrix_world@near[0]).length;errors.append(e)
   if e>.03:bad.append(dict(source=src.name,point=list(pt),error_m=e))
 del tree
out['sampled_bidirectional_surface_error_m']=dict(samples=len(errors),max=max(errors),p95=float(np.percentile(errors,95)),mean=float(np.mean(errors)),over_3cm=bad[:30]);out['repaired_evaluated_triangles']=0
for ob in bpy.data.collections['REPAIRED_HIGH_DETAIL'].objects:
 ev=ob.evaluated_get(dg);m=ev.to_mesh();m.calc_loop_triangles();out['repaired_evaluated_triangles']+=len(m.loop_triangles);ev.to_mesh_clear()
# Fresh GLB reimport: actual exported model, map resolution, bounds and assignments.
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(D/'Exports/CM_CrookedMortar_ExteriorRecovery01.glb'))
meshes=[ob for ob in bpy.context.scene.objects if ob.type=='MESH'];pts=[ob.matrix_world@Vector(v) for ob in meshes for v in ob.bound_box];out['glb_roundtrip']=dict(meshes=len(meshes),triangles=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in meshes),bounds_m=[[min(v[i] for v in pts) for i in range(3)],[max(v[i] for v in pts) for i in range(3)]],images=[dict(name=i.name,size=list(i.size)) for i in bpy.data.images if i.type=='IMAGE'],missing_material_slots=sum(1 for ob in meshes for mat in ob.data.materials if mat is None))
src=ROOT/'ArtSource/Blender/Architecture/CrookedMortar/TripoImports/storybook cottage 3d model.glb';out['original_sha256_unchanged']=hashlib.sha256(src.read_bytes()).hexdigest()==json.loads((D/'SourceManifest.json').read_text())['sha256'];(D/'Validation.json').write_text(json.dumps(out,indent=2));print('VALIDATION',json.dumps(out),flush=True)
