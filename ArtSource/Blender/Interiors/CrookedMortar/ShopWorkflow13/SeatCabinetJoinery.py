raise RuntimeError("REJECTED compound-cutter experiment. Do not run; final fit is recorded in RepairCabinetFit.py.")
"""Actual fitted notches against retained shop tie/standard geometry; no covering pieces."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));s=bpy.context.scene
structure=bpy.data.objects['CM_SW13_StructuralJoinery'];cut=structure.copy();cut.data=structure.data.copy();cut.name='Temporary exact structural fitting tool';s.collection.objects.link(cut)
for v in cut.data.vertices:v.co=(1.15-v.co.y,v.co.x-.23,v.co.z-.2)
bm=bmesh.new();bm.from_mesh(cut.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(cut.data);bm.free()
coll=bpy.data.collections['CM_SW13_FittedApothecaryCabinet editable components'];count=0
for o in list(coll.objects)+[bpy.data.objects['CM_SW13_FittedApothecaryCabinet']]:
 # Only members reaching the rear bearing zone can meet the cross-tie/standard.
 if min(v.co.x for v in o.data.vertices)>-.5:continue
 o.hide_set(False);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Fitted rebate around existing tie and standard','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);count+=1
 if o.name!='CM_SW13_FittedApothecaryCabinet':o.hide_set(True)
bpy.data.objects.remove(cut,do_unlink=True);g=bpy.data.objects['CM_SW13_FittedApothecaryCabinet'];g.data.calc_loop_triangles();cat=json.loads((D/'AssetCatalog.json').read_text());row=next(r for r in cat['modules'] if r['name']==g.name);row['triangles']=len(g.data.loop_triangles);row['vertices']=len(g.data.vertices);cat['triangles']=sum(r['triangles'] for r in cat['modules']);(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2));bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
bpy.ops.object.select_all(action='DESELECT');g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Models'/(g.name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP');print('SEATED_MEMBERS',count,'TRIANGLES',row['triangles'])
