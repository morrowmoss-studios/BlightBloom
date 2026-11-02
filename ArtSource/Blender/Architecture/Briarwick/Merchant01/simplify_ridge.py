"""Retain the continuous hipped coat; remove the separate raised dressing from rough build."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Merchant01.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['BW_Merchant01_Thatch']
if o.get('ContinuousRidgeOnly'):raise RuntimeError('Already simplified')
bm=bmesh.new();bm.from_mesh(o.data);left=set(bm.verts);remove=[];count=0
while left:
 v=left.pop();part={v};stack=[v]
 while stack:
  for e in stack.pop().link_edges:
   for q in e.verts:
    if q in left:left.remove(q);part.add(q);stack.append(q)
 size=[max(v.co[i] for v in part)-min(v.co[i] for v in part) for i in range(3)]
 if size[0]<2 and size[1]<1 and min(v.co.z for v in part)>6.3:remove.extend(part);count+=1
if count!=1:raise RuntimeError('Unexpected ridge component count; no save: '+str(count))
bmesh.ops.delete(bm,geom=remove,context='VERTS');bm.to_mesh(o.data);bm.free();o['ContinuousRidgeOnly']=True;o.data.update();o.data.calc_loop_triangles();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Merchant01/Models/BW_Merchant01_Thatch.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Thatch':row['triangles']=len(o.data.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Merchant01.blend'));print('Continuous ridge retained; total',sum(row['triangles'] for row in cat['models']))
