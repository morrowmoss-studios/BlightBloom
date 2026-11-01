"""Restore the original local contacts, including their fused ground collars, after rejected cut trials.
Only restore immutable source faces. This does not generate replacement architecture.
"""
from pathlib import Path
import numpy as np,json
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];ct=co[tri].mean(1);gone=np.load(D/'TerrainFaceSelection.npy');guard=np.zeros(len(tri),bool)
volumes=[('LeftBoulderFullContact',[-2.83,-3.34,.67],.90),('RightRootFullContact',[2.95,-3.30,.64],.85),('RightBoulderChainContact',[3.28,-2.45,.45],.58)]
for name,center,radius in volumes:
 # Keep a small original source collar around each inseparable cluster; never delete by this guard.
 guard |= np.linalg.norm(co[tri]-np.array(center),axis=2).min(1)<radius
restore=gone[guard[gone]];newgone=gone[~guard[gone]];np.save(D/'RestoredLocalContactSourceFaces.npy',restore);np.save(D/'TerrainFaceSelection.npy',newgone);labels=np.load(D/'RemovalSectionLabels.npy');labels[restore]=0;np.save(D/'RemovalSectionLabels.npy',labels)
(D/'RestoredContactCollars.json').write_text(json.dumps(dict(reason='Rejected local cut/repair trials. Restore entire original contact clusters and bounded fused ground collars rather than retain visibly truncated rocks.',keep_volumes=[dict(name=n,center=c,radius_m=r) for n,c,r in volumes],restored_original_triangles=len(restore),restored_source_faces=restore.tolist(),not_a_deletion_mask=True),indent=2));print('RESTORED_ORIGINAL_CONTACT_FACES',len(restore),'removed',len(newgone))
