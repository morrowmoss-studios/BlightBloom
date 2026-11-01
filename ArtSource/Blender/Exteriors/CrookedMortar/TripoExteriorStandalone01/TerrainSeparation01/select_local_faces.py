"""Conservative per-face selection in local traced perimeter bands, plus inspected underside.
This does not move/cut vertices. The height of each local edge varies with the actual traced contact;
no global height plane, rectangular crop, Boolean, remesh or component deletion is used.
"""
import numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];ct=co[tri].mean(1);loop=np.load(D/'TracedBoundaryVertices.npy');p=co[loop];n=len(ct)
inside=np.zeros(n,bool);best=np.full(n,np.inf);local_z=np.zeros(n);edge_id=np.zeros(n,int)
for i,(a,b) in enumerate(zip(p,np.roll(p,-1,axis=0))):
 if (a[1]>ct[:,1]).any() or (b[1]>ct[:,1]).any():
  inside^=((a[1]>ct[:,1])!=(b[1]>ct[:,1])) & (ct[:,0]<(b[0]-a[0])*(ct[:,1]-a[1])/(b[1]-a[1]+1e-20)+a[0])
 ab=b[:2]-a[:2];t=np.clip(((ct[:,:2]-a[:2])@ab)/max(ab@ab,1e-15),0,1);d=((ct[:,:2]-(a[:2]+t[:,None]*ab))**2).sum(1);take=d<best;best[take]=d[take];local_z[take]=a[2]+t[take]*(b[2]-a[2]);edge_id[take]=i
# The visible apron is on the terrain side of the inspected contact, below its individual edge.
# Any face above that local contact is retained, including projecting botanical/architectural detail.
apron=(~inside)&(ct[:,2]<local_z-.006)
underside=np.zeros(n,bool);underside[np.load(D/'UndersideInspectionFaces.npy')]=True
remove=apron|underside
# Protect all faces visibly above the highest approved contact (validation, not a deletion plane).
assert not (remove & (co[tri][:,:,2].min(1)>1.25)).any()
# Divide selected existing faces into small perimeter sections; underside is a separate final stage.
labels=np.zeros(n,np.int8);closest=p[edge_id];
labels[remove & ~underside & (closest[:,1]<-4.3)]=1
labels[remove & ~underside & (closest[:,0]>0) & (labels==0)]=2
labels[remove & ~underside & (closest[:,1]>5.5) & (labels==0)]=3
labels[remove & ~underside & (labels==0)]=4
labels[underside]=5
np.save(D/'TerrainFaceSelection.npy',np.where(remove)[0]);np.save(D/'RemovalSectionLabels.npy',labels)
report={'method':'Existing-face selection along the individually traced local perimeter; underside normal-continuity inspection separately. No global height/box/Boolean cut. Candidate subject to per-section render review.','selected_faces':int(remove.sum()),'section_counts':{str(i):int((labels==i).sum()) for i in range(1,6)},'removed_max_z':float(co[tri[remove]][:,:,2].max()),'kept_body_faces':int((~remove).sum())}
(D/'SelectionReview.json').write_text(json.dumps(report,indent=2));print(report)
