import bpy,numpy as np,json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;src=D.parent/'BoundaryMapping02/CM_CrookedMortar_BoundaryMapping02_UNCUT.blend';bpy.ops.wm.open_mainfile(filepath=str(src));o=bpy.data.objects['House_Optimized'];m=o.data
co=np.empty(len(m.vertices)*3,np.float64);m.vertices.foreach_get('co',co);co=co.reshape(-1,3);idx=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',idx);tri=idx.reshape(-1,3)
ed=np.empty(len(m.edges)*2,np.int32);m.edges.foreach_get('vertices',ed);ed=ed.reshape(-1,2)
np.savez_compressed(D/'Topology.npz',co=co,tri=tri,edges=ed)
(D/'SourceProvenance.json').write_text(json.dumps({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'triangles':len(tri),'vertices':len(co),'bounds':[co.min(0).tolist(),co.max(0).tolist()]},indent=2));print('TOPOLOGY',len(co),len(tri),len(ed),flush=True)
# New untouched working duplicate before any operations.
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend'))
