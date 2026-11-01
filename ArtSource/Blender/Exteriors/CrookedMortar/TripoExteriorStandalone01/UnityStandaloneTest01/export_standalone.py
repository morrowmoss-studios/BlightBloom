import bpy,json,hashlib,time,os
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;ROOT=D.parents[5];SRC=D.parent/'TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend'
# Actual root from path above: locate existing project, never create nested Unity folders.
ROOT=next(p for p in D.parents if (p/'Assets').is_dir() and (p/'AGENTS.md').is_file())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def free():return os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize
assert free()>3_000_000_000,'Disk safety reserve'
export=D/'Exports';export.mkdir(exist_ok=True);fbx=export/'CM_CrookedMortar_Standalone01.fbx';assert not fbx.exists(),'Do not overwrite a prior export'
protected=[SRC]+list((ROOT/'Assets/Scenes').glob('*.unity'))
baseline={str(p.relative_to(ROOT)):sha(p) for p in protected};(D/'ProtectedHashes.json').write_text(json.dumps(baseline,indent=2))
start=time.perf_counter();bpy.ops.wm.open_mainfile(filepath=str(SRC));scene=bpy.context.scene
col=bpy.data.collections['STANDALONE_WORKING_CANDIDATE'];layer=bpy.context.view_layer.layer_collection.children[col.name];layer.exclude=False;bpy.context.view_layer.update()
objects=[o for o in col.all_objects if o.type in {'MESH','FONT','CURVE'} and not o.hide_render]
assert any(o.name=='House_Standalone01' for o in objects)
dg=bpy.context.evaluated_depsgraph_get();tmp=bpy.data.collections.new('TEMP_EXPORT_ONLY');scene.collection.children.link(tmp);clones=[];manifest=[];materials={};bounds=[]
for o in objects:
 mesh=bpy.data.meshes.new_from_object(o.evaluated_get(dg),preserve_all_data_layers=True,depsgraph=dg)
 ob=bpy.data.objects.new(o.name,mesh);tmp.objects.link(ob);ob.matrix_world=o.matrix_world.copy();clones.append(ob)
 mats=[]
 for mat in mesh.materials:
  assert mat is not None,(o.name,'missing material');mats.append(mat.name)
  if mat.name not in materials:
   material={'diffuse':list(mat.diffuse_color),'images':[]}
   if mat.use_nodes:
    bs=next((n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    if bs:material.update(baseColor=list(bs.inputs['Base Color'].default_value),roughness=float(bs.inputs['Roughness'].default_value),metallic=float(bs.inputs['Metallic'].default_value))
    for n in mat.node_tree.nodes:
     if n.type=='TEX_IMAGE' and n.image:material['images'].append({'name':n.image.name,'path':n.image.filepath,'size':list(n.image.size),'colorSpace':n.image.colorspace_settings.name})
   materials[mat.name]=material
 count=sum(len(p.vertices)-2 for p in mesh.polygons);manifest.append({'name':o.name,'sourceType':o.type,'triangles':count,'vertices':len(mesh.vertices),'uvLayers':[u.name for u in mesh.uv_layers],'materials':mats,'worldMatrix':[list(r) for r in ob.matrix_world]})
 bounds.extend(ob.matrix_world@Vector(v) for v in ob.bound_box)
assert sum(x['triangles'] for x in manifest)==503363,manifest
for o in bpy.context.selected_objects:o.select_set(False)
for o in clones:o.select_set(True)
bpy.context.view_layer.objects.active=clones[0]
# Same validated export axis, metric unit, tangent/normal and scale conventions as Recovery01.
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='COPY',embed_textures=False)
result={'source':str(SRC.relative_to(ROOT)),'sourceSHA256':baseline[str(SRC.relative_to(ROOT))],'objects':manifest,'materials':materials,'triangles':sum(x['triangles'] for x in manifest),'boundsBlenderMetres':[[min(v[i] for v in bounds) for i in range(3)],[max(v[i] for v in bounds) for i in range(3)]],'exportSeconds':time.perf_counter()-start,'fbxBytes':fbx.stat().st_size,'fbxSHA256':sha(fbx),'freeBytesAfterExport':free(),'sourceHashUnchanged':sha(SRC)==baseline[str(SRC.relative_to(ROOT))],'sourceSaved':False,'hiddenReferenceGeometryExported':False}
assert result['sourceHashUnchanged'];(D/'ExportManifest.json').write_text(json.dumps(result,indent=2));print('EXPORT_RESULT',json.dumps(result),flush=True)
