"""Targeted final sculpt/paint refinement in the existing candidate source; no room regeneration."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Matrix,Vector
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/EntranceWorkflow11';bpy.ops.wm.open_mainfile(filepath=str(D/'CM_EntranceWorkflow11.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
P=lambda v:Vector((v[0],v[2],v[1]));stone=bpy.data.materials['CM_EW11_DressedSandstone'];image=bpy.data.images.load(str(A/'Textures/CM_EW11_PaintedStone.png'));image.pack();next(n for n in stone.node_tree.nodes if n.type=='TEX_IMAGE').image=image;stone.diffuse_color=(.95,.94,.90,1)
# Only a few plausible tool chips: concentrated at exposed bed/front corners, not noisy erosion.
chips=[('Dressed jamb course 1 0',(4.949,.596,.137),.027),('Dressed jamb course -1 2',(2.447,1.485,.141),.025),('Hand-dressed voussoir 2',(4.670,2.704,.148),.022),('Fitted keystone',(3.895,3.174,.159),.021)]
for name,co,radius in chips:
 o=bpy.data.objects[name];o.hide_set(False);bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=radius,location=P(co));cut=bpy.context.object;cut.scale=(1,.72,1.05);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Selective chisel corner wear','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
# Stone-face UVs read the dedicated single-surface paint, with appropriate side-face projection.
coll=bpy.data.collections['CM_EW11_InnerMasonry editable parts'];index=0
for o in coll.objects:
 if not o.data.materials or o.data.materials[0]!=stone:continue
 lo=[min(v.co[i] for v in o.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in o.data.vertices) for i in range(3)];uv=o.data.uv_layers[0]
 for f in o.data.polygons:
  normal=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=normal];ua,va=axes
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;u=(co[ua]-lo[ua])/max(.001,hi[ua]-lo[ua]);v=(co[va]-lo[va])/max(.001,hi[va]-lo[va]);uv.data[li].uv=(.04+.17*(index%3)+u*.42,.04+.09*(index%3)+v*.48)
 index+=1
# Broad hand-trowelled surface relief, preserving boundary datums and avoiding dense displacement.
for name in ['Left hand-trowelled spandrel','Right hand-trowelled pier and spandrel']:
 o=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(o.data);front=[f for f in bm.faces if f.normal.y>.85];bmesh.ops.triangulate(bm,faces=front);edges=list(set(e for f in bm.faces if f.normal.y>.85 for e in f.edges));bmesh.ops.subdivide_edges(bm,edges=edges,cuts=1,use_grid_fill=True)
 for v in bm.verts:
  if v.co.y>.034:
   x=v.co.x;y=v.co.z;v.co.y+=.0025*math.sin((x-2.2)*2.8)*math.sin((y-.2)*2.2)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
o=bpy.data.objects['Repaired lime base coat']
for v in o.data.vertices:
 if v.co.y>.04:v.co.y+=.006
# Rejoin only two altered module copies from editable components; timber remains untouched/export not repeated.
for name in ['CM_EW11_InnerMasonry','CM_EW11_LimeReturns']:
 old=bpy.data.objects[name];bpy.data.objects.remove(old,do_unlink=True);coll=bpy.data.collections[name+' editable parts'];bpy.ops.object.select_all(action='DESELECT')
 for o in coll.objects:
  p=o.copy();p.data=o.data.copy();s.collection.objects.link(p);p.hide_set(False);p.hide_render=False;p.select_set(True);o.hide_set(True);o.hide_render=True
 bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.join();g=bpy.context.object;g.name=name;g.data.name=name+'_Mesh';s.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_EntranceWorkflow11.blend'))
for name in ['CM_EW11_InnerMasonry','CM_EW11_LimeReturns']:
 g=bpy.data.objects[name];bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/f'{name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((D/'AssetCatalog.json').read_text())
for row in cat['modules']:
 o=bpy.data.objects[row['name']];o.data.calc_loop_triangles();row['triangles']=len(o.data.loop_triangles);row['vertices']=len(o.data.vertices)
cat['triangles']=sum(r['triangles'] for r in cat['modules']);cat['refinement']='Four selected chisel chips, broad low-density trowel relief, dedicated gouache stone paint with per-face UVs; timber and original outline unchanged.';(D/'AssetCatalog.json').write_text(json.dumps(cat,indent=2));print('REFINED_ENTRANCE',cat['triangles'])
