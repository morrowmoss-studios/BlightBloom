"""Remove only the two applied king posts and two front diagonal gable pieces.
Retains structural verges/plates. Hidden reference preserves previous timber geometry.
"""
import bpy,bmesh,json,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
H=Path(__file__).parent;R=H.parents[4];D=R/'ArtSource/Pipeline/Review/BriarwickBakery02';P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Bakery02.blend'));bpy.context.preferences.filepaths.save_version=0
o=bpy.data.objects['BW_Bakery02_Timber']
if o.get('AppliedGableBeamsRemoved'):raise RuntimeError('Cleanup already performed')
def signature(ob):
 return hashlib.sha256(repr(([(tuple(v.co)) for v in ob.data.vertices],[tuple(p.vertices) for p in ob.data.polygons],[[tuple(u.uv) for u in layer.data] for layer in ob.data.uv_layers],[m.name for m in ob.data.materials])).encode()).hexdigest()
before={ob.name:signature(ob) for ob in bpy.data.objects if ob.type=='MESH' and ob!=o}
bm=bmesh.new();bm.from_mesh(o.data);left=set(bm.verts);selected=[];records=[]
while left:
 v=left.pop();part={v};stack=[v]
 while stack:
  for e in stack.pop().link_edges:
   for q in e.verts:
    if q in left:left.remove(q);part.add(q);stack.append(q)
 ps=[P.inverted()@q.co for q in part];c=sum(ps,Vector())/len(ps)
 king=abs(c.x+.35)<.04 and 4.1<c.y<4.5 and (abs(c.z-4.62)<.025 or abs(c.z+3.02)<.025)
 diagonal=abs(c.z-4.63)<.025 and 3.7<c.y<3.9 and (abs(c.x+1.465)<.04 or abs(c.x-1.09)<.04)
 if king or diagonal:selected.extend(part);records.append({'type':'central applied vertical' if king else 'applied diagonal','centreUnityLocal':list(c),'vertices':len(part)})
if len(records)!=4:raise RuntimeError('Unexpected candidates; no geometry saved: '+repr(records))
col=bpy.data.collections.new('REFERENCE_BeforeGableCleanup_NOT_EXPORTED');bpy.context.scene.collection.children.link(col);ref=o.copy();ref.data=o.data.copy();ref.name='BeforeCleanup_Timber_REFERENCE';col.objects.link(ref);col.hide_render=True;col.hide_viewport=True;ref.hide_render=True
oldTriangles=len(o.data.polygons);bmesh.ops.delete(bm,geom=selected,context='VERTS');bm.to_mesh(o.data);bm.free();o.data.update();o.data.calc_loop_triangles();o['AppliedGableBeamsRemoved']=True
assert all(signature(bpy.data.objects[n])==h for n,h in before.items())
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
path=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models/BW_Bakery02_Timber.fbx'
bpy.ops.export_scene.fbx(filepath=str(path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Timber':row['triangles']=len(o.data.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery02.blend'))
(D/'GableCleanupGeometry.json').write_text(json.dumps({'removedPieces':records,'timberTrianglesBefore':oldTriangles,'timberTrianglesAfter':len(o.data.loop_triangles),'buildingTriangles':sum(row['triangles'] for row in cat['models']),'otherSourceMeshesUnchanged':True,'previousTimberPreservedInHiddenReference':True},indent=2));print(records)
