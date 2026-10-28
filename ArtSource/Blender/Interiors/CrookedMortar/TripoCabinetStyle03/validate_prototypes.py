import bpy,json,hashlib,numpy as np
from pathlib import Path
D=Path(__file__).resolve().parent;inspect=json.loads((D/'Diagnostics/MaterialInspection.json').read_text());r={}
for v in ['A','B']:
 p=D/f'CabinetB_Style03_Prototype{v}.blend';bpy.ops.wm.open_mainfile(filepath=str(p));obs=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(obs)==1;o=obs[0];m=o.data
 co=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('co',co);uv=np.empty(len(m.uv_layers.active.data)*2,dtype=np.float32);m.uv_layers.active.data.foreach_get('uv',uv);normal=np.empty(len(m.vertices)*3,dtype=np.float32);m.vertices.foreach_get('normal',normal)
 a={'mesh_count':len(obs),'vertices':len(m.vertices),'triangles':len(m.polygons),'dimensions_m':list(o.dimensions),'coordinates_sha256':hashlib.sha256(co.tobytes()).hexdigest(),'uv_sha256':hashlib.sha256(uv.tobytes()).hexdigest(),'finite_coordinates':bool(np.isfinite(co).all()),'finite_uvs':bool(np.isfinite(uv).all()),'finite_normals':bool(np.isfinite(normal).all()),'material':m.materials[0].name,'principled_nodes':sum(n.type=='BSDF_PRINCIPLED' for n in m.materials[0].node_tree.nodes),'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file)} for im in bpy.data.images if im.type=='IMAGE']}
 assert a['coordinates_sha256']==inspect['mesh_position_hash'];assert a['uv_sha256']==inspect['uv_hash'];assert a['triangles']==inspect['triangles'];assert a['principled_nodes']==1
 a['same_geometry_and_uv_as_style02']=True;r[v]=a
assert hashlib.sha256(Path(inspect['source']).read_bytes()).hexdigest()==inspect['source_sha256'];r['Style02_source_unchanged']=True
old=json.loads((D.parent/'TripoCabinetRecovery01/Inspection.json').read_text());r['original_glb_unchanged']=hashlib.sha256(Path(old['source']).read_bytes()).hexdigest()==old['sha256'];assert r['original_glb_unchanged']
(D/'Validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2),flush=True)
