"""Clip long native shaft triangles at the hood level, preserving interpolated source UVs."""
import bpy,bmesh,json
from mathutils import Vector,Matrix
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Blacksmith01.blend'));bpy.context.preferences.filepaths.save_version=0;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
old=bpy.data.objects['BW_Blacksmith01_Chimney'];mat=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True)
src=next(m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text()) if m['name']=='chimney_outside_size1.001');V=[];F=[];UV=[]
for si,ts in enumerate(src['submeshes']):
 if src['materials'][si]!='rock2':continue
 for k in range(0,len(ts),3):
  poly=[(Vector(src['vertices'][i]),Vector(src['uv'][i])) for i in ts[k:k+3]];out=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   da=a[0].y-1.713;db=b[0].y-1.713
   if da>=0:out.append(a)
   if (da>=0)!=(db>=0):
    t=da/(da-db);out.append((a[0].lerp(b[0],t),a[1].lerp(b[1],t)))
  if len(out)<3:continue
  start=len(V)
  for v,u in out:V.append(tuple(P@Vector((2.75+v.x*.75,3+(v.y-1.713)*.75,.55+v.z*.75))));UV.append(tuple(u))
  F.append(tuple(range(start,len(V)))[::-1])
me=bpy.data.meshes.new('BW_Blacksmith01_Chimney');me.from_pydata(V,[],F);me.materials.append(mat);uv=me.uv_layers.new(name='UVMap')
for p in me.polygons:
 for li in p.loop_indices:uv.data[li].uv=UV[me.loops[li].vertex_index]
o=bpy.data.objects.new('BW_Blacksmith01_Chimney',me);bpy.context.scene.collection.objects.link(o);bpy.context.view_layer.objects.active=o;bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(me);bm.free();me.update();me.calc_loop_triangles();bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/Models/BW_Blacksmith01_Chimney.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
cat=json.loads((H/'ModelCatalog.json').read_text())
for row in cat['models']:
 if row['group']=='Chimney':row['triangles']=len(me.loop_triangles)
(H/'ModelCatalog.json').write_text(json.dumps(cat,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Blacksmith01.blend'));print('FLUE_TRIANGLES',len(me.loop_triangles))
