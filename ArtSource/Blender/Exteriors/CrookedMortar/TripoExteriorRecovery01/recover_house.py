"""Source-specific, non-destructive recovery. No semantic island extraction or UV rebake."""
import bpy,numpy as np,json,math,shutil
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;ROOT=D.parents[4];SCALE=15.0
bpy.ops.wm.open_mainfile(filepath=str(D/'OriginalReference.blend'));original=next(o for o in bpy.context.scene.objects if o.type=='MESH');original.name='Original_Tripo_1880780tri_UNMODIFIED'
# Byte-exact extracted texture copies, packed for portable editable source.
for im in bpy.data.images:
 if im.type!='IMAGE':continue
 idx=0 if 'basecolor' in im.name else 2 if 'normal' in im.name else 1
 p=D/'Textures'/('Original_%02d.%s'%(idx,'png' if idx==2 else 'jpg'))
 if im.packed_file:im.unpack(method='REMOVE')
 im.filepath=str(p);im.reload();im.pack()
origcol=original.users_collection[0];origcol.hide_render=True;origcol.hide_viewport=True
col=bpy.data.collections.new('REPAIRED_HIGH_DETAIL');bpy.context.scene.collection.children.link(col)
a=np.load(D/'InspectionArrays.npz');co=a['co'];tri=a['tri'];uv=a['uv'];tl=a['tri_loops'];ct=co[tri].mean(1)
# Remove malformed sign inset (both sides) inside retained perimeter, including raised glyph geometry.
inset=(ct[:,0]>-.066)&(ct[:,0]<-.046)&(ct[:,1]>-.456)&(ct[:,1]<-.394)&(ct[:,2]>.235)&(ct[:,2]<.309)
# Orphan melted blue-green iron cluster, forward of the front gable; wall remains behind y=-.28.
orphan=np.isin(a['roots'][tri[:,0]],[334456,335526,330384,331586,331453,334681,331317,324333,325893])
keep=~(inset|orphan);faces=tri[keep];used,inv=np.unique(faces,return_inverse=True);faces=inv.reshape(-1,3);m=bpy.data.meshes.new('Repaired_source_surface_UVs_retained');m.vertices.add(len(used));m.vertices.foreach_set('co',co[used].ravel());m.loops.add(faces.size);m.loops.foreach_set('vertex_index',faces.ravel());m.polygons.add(len(faces));m.polygons.foreach_set('loop_start',np.arange(len(faces),dtype=np.int32)*3);m.polygons.foreach_set('loop_total',np.full(len(faces),3,dtype=np.int32));m.uv_layers.new(name='SourceUV_PRESERVED');m.uv_layers.active.data.foreach_set('uv',uv[tl[keep]].ravel());m.update();m.polygons.foreach_set('use_smooth',np.ones(len(faces),dtype=bool))
for mat in original.data.materials:m.materials.append(mat)
body=bpy.data.objects.new('House_RepairedHigh',m);col.objects.link(body)
# Fused bracket left no intact rear wall surface. Reconstruct a recessed, fitted plaster return.
# This is a perimeter-shaped surface, not a replacement building volume or a cover over bad geometry.
pvs=[(-.171,-.289,.318),(-.100,-.289,.318),(-.100,-.289,.373),(-.103,-.289,.430),(-.138,-.290,.435),(-.171,-.289,.423),(-.175,-.289,.365)]
pm=bpy.data.meshes.new('Local_FittedPlasterReturn');pm.from_pydata(pvs,[],[tuple(range(len(pvs)))]);pm.update();pm.materials.append(original.data.materials[0]);pm.uv_layers.new(name='SourcePlasterPatch');uvpatch=json.loads((D/'PlasterPatchUV.json').read_text())['uv'];u0=np.mean(uvpatch,axis=0)
for lp in pm.loops:pm.uv_layers.active.data[lp.index].uv=u0+(np.array(uvpatch[lp.index%3])-u0)*.7
patch=bpy.data.objects.new('Fitted_PlasterReturn_AfterFusedBracketRemoval',pm);col.objects.link(patch)
# Existing painted walnut atlas reused only on replacement sign inset; the house textures are unchanged.
wp=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/Textures/CM_EntryPortal02_Walnut_BaseColor.png';dest=D/'Textures/Sign_ApprovedWalnut.png';shutil.copy2(wp,dest)
wood=bpy.data.materials.new('Sign_ApprovedPaintedWalnut');wood.use_nodes=True;n=wood.node_tree.nodes;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.84;bs.inputs['Specular IOR Level'].default_value=.18;tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(dest));tex.image.pack();wood.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
def flat(name,color,rough=.85,metal=0):
 mat=bpy.data.materials.new(name);mat.use_nodes=True;b=mat.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*color,1);b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal;return mat
ivory=flat('Sign_AgedIvoryLettering',(.74,.63,.39));iron=flat('Sign_WeatheredIron',(.06,.045,.03),.8,.2)
def move_col(ob):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 col.objects.link(ob)
def board(name,center,dims):
 bpy.ops.mesh.primitive_cube_add(size=1,location=center);ob=bpy.context.object;ob.name=name;ob.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(wood);be=ob.modifiers.new('Worn_rebated_edges','BEVEL');be.width=.00055;be.segments=3;bpy.ops.object.modifier_apply(modifier=be.name);move_col(ob)
 # Planar grain follows the upright sign boards; no stretched UV triangulation.
 for p in ob.data.polygons:
  for li in p.loop_indices:
   v=ob.data.vertices[ob.data.loops[li].vertex_index].co;ob.data.uv_layers.active.data[li].uv=((v.y/dims[1]+.5)*.023+.780,(v.z/dims[2]+.5)*.55+.12)
 return ob
for i in range(3):board('Sign_ReplacementInset_Plank%02d'%i,(-.056,-.425+(i-1)*.0211,.2715),(.011,.0214,.076))
font=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Georgia.ttf')
for side in [1,-1]:
 for i,(line,width) in enumerate([('The',.030),('Crooked',.055),('Mortar',.050)]):
  cu=bpy.data.curves.new('EDITABLE_Sign_'+line,'FONT');cu.body=line;cu.font=font;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=.014;cu.extrude=0;cu.bevel_depth=0;cu.resolution_u=3;ob=bpy.data.objects.new('SignText_'+line+('_Front' if side==1 else '_Back'),cu);col.objects.link(ob);ob.location=(-.0499 if side==1 else -.0621,-.425,.293-i*.0205);ob.rotation_euler=(math.pi/2,0,side*math.pi/2);cu.materials.append(ivory);bpy.context.view_layer.update();f=width/max(ob.dimensions);ob.scale*=f
# Curved restrained wrought hanger, anchored to original canopy fascia directly behind the sign.
def rod(name,points,r=.001):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=3;cu.use_fill_caps=True;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,xyz in zip(sp.bezier_points,points):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);col.objects.link(ob);cu.materials.append(iron);return ob
rod('Sign_FasciaMounted_Arm',[(-.058,-.367,.321),(-.058,-.391,.332),(-.058,-.424,.334),(-.058,-.455,.332)],.0014)
rod('Sign_Hanger_Brace',[(-.058,-.372,.303),(-.058,-.391,.318),(-.058,-.411,.332)],.0010)
for y in [-.403,-.447]:rod('Sign_ClosedDropLink',[(-.058,y,.333),(-.055,y-.0015,.324),(-.058,y,.316)],.00065)
# Uniform unit conversion only; no architecture rescaling or distortion. Source is a normalized miniature.
for ob in col.objects:ob.location*=SCALE;ob.scale*=SCALE
for ob in origcol.objects:ob.scale*=SCALE
# Save editable repair with editable text/curves plus hidden untouched high-detail reference.
bpy.context.scene.unit_settings.system='METRIC';bpy.ops.wm.save_as_mainfile(filepath=str(D/'CrookedMortar_RepairedHigh.blend'))
# Duplicate working body, retain high detail. Protect fine roof/eaves/foliage and trim more than broad surfaces.
optcol=bpy.data.collections.new('OPTIMIZED_GAMEPLAY_CANDIDATE');bpy.context.scene.collection.children.link(optcol)
opt=body.copy();opt.data=body.data.copy();opt.name='House_Optimized';optcol.objects.link(opt);bpy.context.view_layer.objects.active=opt;opt.select_set(True)
# Exact-position UV seam welding on optimization copy only, with unchanged per-corner UV data.
# No distance-threshold merge: nearby distinct surfaces cannot be joined accidentally.
uco,uinv=np.unique(co[used],axis=0,return_inverse=True);wf=uinv[faces];wm=bpy.data.meshes.new('Optimization_ExactSeamWeld');wm.vertices.add(len(uco));wm.vertices.foreach_set('co',uco.ravel());wm.loops.add(wf.size);wm.loops.foreach_set('vertex_index',wf.ravel());wm.polygons.add(len(wf));wm.polygons.foreach_set('loop_start',np.arange(len(wf),dtype=np.int32)*3);wm.polygons.foreach_set('loop_total',np.full(len(wf),3,dtype=np.int32));wm.uv_layers.new(name='SourceUV_PRESERVED');wm.uv_layers.active.data.foreach_set('uv',uv[tl[keep]].ravel());wm.update();wm.polygons.foreach_set('use_smooth',np.ones(len(wf),dtype=bool));wm.materials.append(body.data.materials[0]);opt.data=wm

vg=opt.vertex_groups.new(name='Keep_RoofEdges_Entrance');pts=uco;critical=(pts[:,2]>.32)|((pts[:,1]<-.24)&(pts[:,2]>.08)&(pts[:,2]<.32));vg.add(np.flatnonzero(critical).tolist(),1,'REPLACE')
from mathutils import Matrix
opt.data.transform(Matrix.Scale(SCALE,4));opt.scale=(1,1,1);opt.data.update()
dec=opt.modifiers.new('Selective_QuadricReduction','DECIMATE');dec.ratio=.28;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
for ob in list(col.objects):
 if ob==body:continue
 dup=ob.copy();dup.data=ob.data.copy();optcol.objects.link(dup)
col.hide_render=True;col.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CrookedMortar_Optimized.blend'))
# Export only candidate, convert editable text and curves on export copies, never source.
exports=D/'Exports';exports.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in optcol.objects:ob.select_set(True)
bpy.context.view_layer.objects.active=opt;bpy.ops.object.convert(target='MESH')
for ob in optcol.objects:
 if ob.type=='MESH':bpy.context.view_layer.objects.active=ob;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
tri_count=sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in optcol.objects if ob.type=='MESH')
bpy.ops.export_scene.gltf(filepath=str(exports/'CM_CrookedMortar_ExteriorRecovery01.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
bpy.ops.export_scene.fbx(filepath=str(exports/'CM_CrookedMortar_ExteriorRecovery01.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='COPY',embed_textures=False)
report=dict(exact_weld_vertices_before=len(used),exact_weld_vertices_after=len(uco),source_triangles=len(tri),removed_sign_inset_triangles=int(inset.sum()),removed_orphan_iron_triangles=int(orphan.sum()),repaired_body_triangles=len(faces),optimized_body_triangles=len(opt.data.polygons),optimized_total_triangles=tri_count,scale_factor=SCALE,house_bounds_m=[(co.min(0)*SCALE).tolist(),(co.max(0)*SCALE).tolist()],sign_text='The Crooked Mortar',sign_editable=True,uv_bake='Not attempted: invalid collapsed source UVs; original atlas retained',new_materials=[wood.name,ivory.name,iron.name])
(D/'Recovery.json').write_text(json.dumps(report,indent=2));print('RECOVERY',json.dumps(report),flush=True)
