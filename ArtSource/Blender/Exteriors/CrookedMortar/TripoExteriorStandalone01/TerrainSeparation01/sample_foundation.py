"""Reproject an intact foundation patch for new local returns only. Never paint source textures."""
import bpy,numpy as np,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_CrookedMortar_TerrainSeparation01_WORKING.blend'));o=bpy.data.objects['House_Optimized'];m=o.data;A=np.load(D/'Topology.npz');co=A['co'];tri=A['tri'];bvh=BVHTree.FromPolygons(co.tolist(),tri.tolist(),all_triangles=True);uv=np.empty(len(m.loops)*2,np.float32);m.uv_layers[0].data.foreach_get('uv',uv);uv=uv.reshape(-1,3,2)
# Intact dressed-stone panel, left wall beneath the window planter; no rock or wood sample.
W,H=768,512;grid=np.full((H,W,2),-1.,np.float32);depth=np.zeros((H,W),np.float32);valid=np.zeros((H,W),bool)
for yy in range(H):
 z=.52+(H-1-yy)/(H-1)*.65
 for xx in range(W):
  y=-2.25+xx/(W-1)*1.1;loc,n,f,d=bvh.ray_cast(Vector((-10,y,z)),Vector((1,0,0)))
  if loc is None:continue
  a,b,c=[Vector(v) for v in co[tri[f]]];u,v,w=[Vector((t[0],t[1],0)) for t in uv[f]];result=barycentric_transform(loc,a,b,c,u,v,w);grid[yy,xx]=result[:2];depth[yy,xx]=loc.x;valid[yy,xx]=True
np.savez_compressed(D/'FoundationReprojection.npz',uv=grid,depth=depth,valid=valid)
images=[]
for mat in m.materials:
 for n in mat.node_tree.nodes:
  if n.type=='TEX_IMAGE' and n.image:
   im=n.image;images.append(dict(name=im.name,filepath=im.filepath,colorspace=im.colorspace_settings.name,size=list(im.size)))
   if im.packed_file:
    name='SourceTextureReadOnlyCopy_'+im.name.replace('/','_');p=D/name
    p.write_bytes(im.packed_file.data);images[-1]['read_only_copy']=str(p)
(D/'SourceTextureInspection.json').write_text(json.dumps(images,indent=2));print('SAMPLED',float(valid.mean()),images,flush=True)
