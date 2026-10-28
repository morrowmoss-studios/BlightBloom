import bpy,json,hashlib,struct,math,random
from pathlib import Path
from mathutils.bvhtree import BVHTree
from mathutils import Vector
import numpy as np
D=Path(__file__).resolve().parent;out={}
for label in ['CabinetA','CabinetB']:
 path=D/label/(label+'.blend');bpy.ops.wm.open_mainfile(filepath=str(path));h=bpy.data.objects[label+'_HighDetail'];o=bpy.data.objects[label+'_Optimized']
 # Restore byte-exact extracted original images, resolve paths and retain packed copies.
 for im in bpy.data.images:
  if im.type=='IMAGE':
   name=im.name;im.unpack(method='REMOVE');im.filepath=str(D/'Textures'/name);im.reload();im.pack()
 bpy.ops.wm.save_as_mainfile(filepath=str(path))
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.gltf(filepath=str(D/label/'Exports'/(label+'_Optimized.glb')),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
 def meshcheck(m):
  m.calc_loop_triangles();co=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',co)
  uv=np.empty(len(m.uv_layers.active.data)*2,dtype=np.float32);m.uv_layers.active.data.foreach_get('uv',uv);uv=uv.reshape(-1,2)
  loops=np.array([t.loops for t in m.loop_triangles]);a=uv[loops[:,1]]-uv[loops[:,0]];b=uv[loops[:,2]]-uv[loops[:,0]];areas=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])*.5
  return dict(finite_positions=bool(np.isfinite(co).all()),finite_uvs=bool(np.isfinite(uv).all()),zero_uv_triangles=int((areas<1e-12).sum()),triangles=len(m.loop_triangles))
 # Geometric connectivity after deduplicating coincident UV seam vertices (analysis only).
 co=np.array([v.co[:] for v in h.data.vertices]);_,inv=np.unique(np.round(co,6),axis=0,return_inverse=True);parent=list(range(int(inv.max())+1))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for e in h.data.edges:
  a=root(int(inv[e.vertices[0]]));b=root(int(inv[e.vertices[1]]))
  if a!=b:parent[b]=a
 sizes={}
 for i in inv:
  r=root(int(i));sizes[r]=sizes.get(r,0)+1
 # Deterministic nearest-surface errors; no destructive normal repair or hole filling.
 trees={}
 for ob in [h,o]:trees[ob.name]=BVHTree.FromPolygons([v.co for v in ob.data.vertices],[p.vertices[:] for p in ob.data.polygons],all_triangles=True)
 errors=[]
 for src,dst in [(h,o),(o,h)]:
  step=max(1,len(src.data.polygons)//6000)
  for p in list(src.data.polygons)[::step]:
   pt=sum((src.data.vertices[i].co for i in p.vertices),Vector())/3
   near=trees[dst.name].find_nearest(pt)
   if near:errors.append(near[3])
 dct={'high':meshcheck(h.data),'optimized':meshcheck(o.data),'geometric_components_rounded_1micrometre':len(sizes),'largest_component_vertex_fraction':max(sizes.values())/len(inv),'sampled_surface_error_metres':{'max':max(errors),'p95':float(np.percentile(errors,95)),'mean':float(np.mean(errors))},'materials':[m.name for m in o.data.materials],'images':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images if i.type=='IMAGE']}
 # Separate fresh import validates exported self-contained material/texture setup and bounds.
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(D/label/'Exports'/(label+'_Optimized.glb')))
 meshes=[x for x in bpy.context.scene.objects if x.type=='MESH'];dct['export_roundtrip']={'mesh_count':len(meshes),'triangles':sum(len(x.data.polygons) for x in meshes),'dimensions_m':[list(x.dimensions) for x in meshes],'images':[{'name':i.name,'size':list(i.size)} for i in bpy.data.images if i.type=='IMAGE']}
 out[label]=dct;print('VALIDATED',label,json.dumps(dct),flush=True)
src=D.parent/'TripoImports/rustic wooden cabinet 3d model.glb';out['original_sha256_unchanged']=hashlib.sha256(src.read_bytes()).hexdigest()==json.loads((D/'Inspection.json').read_text())['sha256'];(D/'Validation.json').write_text(json.dumps(out,indent=2))
