"""Retain original winding/UVs on thin plaster panels; do not infer 'outside' from open shells."""
import bpy,bmesh,json
from pathlib import Path
def restore_panels(o,reference):
 for col in o.users_collection:col.hide_viewport=False
 bm=bmesh.new();bm.from_mesh(o.data)
 indices={i for i,m in enumerate(o.data.materials) if m.name=='concrete'}
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in indices],context='FACES');bm.to_mesh(o.data);bm.free()
 copy=reference.copy();copy.data=reference.data.copy();bpy.context.scene.collection.objects.link(copy)
 bm=bmesh.new();bm.from_mesh(copy.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if copy.data.materials[f.material_index].name!='concrete'],context='FACES');bm.to_mesh(copy.data);bm.free()
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);copy.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.join()
if __name__=='__main__':
 H=Path(__file__).parent;R=H.parents[5];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageA/Style01/Models'
 bpy.ops.wm.open_mainfile(filepath=str(H/'BW_FamilyCottageA_Style01.blend'))
 edits=bpy.data.collections['EDITABLE_derivative_meshes_at_native_pivots'];edits.hide_viewport=False
 M=json.loads((H/'GeometryManifest.json').read_text())
 for m in M:
  if not m['replacement'].startswith('BW_Cottage01_GableEnd'):continue
  o=bpy.data.objects[m['replacement']];ref=bpy.data.collections['READ_ONLY_original_mesh_reference'].objects[m['sourceMesh']]
  restore_panels(o,ref)
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
  bpy.ops.export_scene.fbx(filepath=str(A/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
  o.data.calc_loop_triangles();m['triangles']=len(o.data.loop_triangles);m['vertices']=len(o.data.vertices);m['uvLoops']=len(o.data.uv_layers.active.data);m['exportMaterialOrder']=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
 # Refresh only changed owned texture sources embedded in the editable source.
 for im in bpy.data.images:
  if 'BW_Cottage01_' in im.name and any(role in im.name for role in ['roof','concrete','glass']):im.reload();im.pack()
 edits.hide_viewport=True;bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_FamilyCottageA_Style01.blend'))
 (H/'GeometryManifest.json').write_text(json.dumps(M,indent=2));print('OPEN_PANEL_WINDING_PRESERVED')
