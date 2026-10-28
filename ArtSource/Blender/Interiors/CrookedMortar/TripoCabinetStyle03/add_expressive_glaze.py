"""B-only wood pigment interpretation from virtual welded curvature; never moves mesh vertices."""
import bpy,numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent;p=D/'CabinetB_Style03_PrototypeB.blend';bpy.ops.wm.open_mainfile(filepath=str(p));o=bpy.data.objects['CabinetB_Style03_SameGeometry'];me=o.data
co=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',co);co=co.reshape(-1,3);norm=np.empty_like(co);me.vertices.foreach_get('normal',norm.reshape(-1));edge=np.empty(len(me.edges)*2,dtype=np.int32);me.edges.foreach_get('vertices',edge);edge=edge.reshape(-1,2)
_,first,inv=np.unique(np.round(co,6),axis=0,return_index=True,return_inverse=True);pos=co[first].astype(np.float64);e=np.sort(inv[edge],axis=1);e=np.unique(e[e[:,0]!=e[:,1]],axis=0);num=len(pos);sums=np.zeros_like(pos);counts=np.zeros(num,dtype=np.float64);nn=np.zeros_like(pos)
np.add.at(nn,inv,norm);nn/=np.maximum(np.linalg.norm(nn,axis=1)[:,None],1e-12)
np.add.at(sums,e[:,0],pos[e[:,1]]);np.add.at(sums,e[:,1],pos[e[:,0]]);np.add.at(counts,e[:,0],1);np.add.at(counts,e[:,1],1)
lap=sums/np.maximum(counts[:,None],1)-pos;curv=-np.sum(lap*nn,axis=1);v=np.clip((curv-.000025)/.00050,0,1);v=v*v*(3-2*v);values=v[inv].astype(np.float32)
a=me.attributes.get('BB_WoodPigmentConvexity') or me.attributes.new('BB_WoodPigmentConvexity','FLOAT','POINT');a.data.foreach_set('value',values)
mat=me.materials[0];n=mat.node_tree.nodes;l=mat.node_tree.links;dest=n['Paint and modeled crevice tone'];previous=dest.inputs[1].links[0].from_socket
attr=n.new('ShaderNodeAttribute');attr.attribute_name='BB_WoodPigmentConvexity';attr.name='B — model-aware pigment glaze';attr.label='Soft convex pigment glaze, wood only';attr.location=(dest.location.x-650,dest.location.y+400)
scale=n.new('ShaderNodeMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=.62;l.new(attr.outputs['Fac'],scale.inputs[0]);scale.location=(dest.location.x-420,dest.location.y+400)
mix=n.new('ShaderNodeMixRGB');mix.name='B — carved wood warm pigment';mix.label='No photographed highlights; pigment anchored to actual relief';mix.inputs[2].default_value=(.22,.105,.042,1);l.new(scale.outputs[0],mix.inputs[0]);l.new(previous,mix.inputs[1]);l.new(mix.outputs[0],dest.inputs[1]);mix.location=(dest.location.x-220,dest.location.y+400)
# B uses pigment/real lighting rather than an extra AO multiplier.
for link in list(dest.inputs[2].links):l.remove(link)
dest.inputs[2].default_value=(1,1,1,1)
bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
(D/'CurvaturePigment.json').write_text(json.dumps({'method':'Virtual coincident-coordinate grouping and neighbourhood Laplacian, only a new point attribute saved. No weld, vertex displacement, face or UV edits.','attribute':a.name,'raw_convexity_percentiles_m':np.percentile(curv,[0,25,50,75,95,99,100]).tolist(),'positive_glaze_vertex_fraction':float((values>0).mean()),'max_color_mix':.62,'wood_only':True},indent=2));print('B_GLAZE_READY',flush=True)
