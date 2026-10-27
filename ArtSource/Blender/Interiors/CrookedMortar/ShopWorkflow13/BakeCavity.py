"""Low-frequency mesh cavity in editable vertex colours, not noisy image texture or screen blur."""
import bpy,math,json
from pathlib import Path
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Models'
bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));names=json.loads((D/'AssetCatalog.json').read_text())['modules']
for row in names:
 o=bpy.data.objects[row['name']];me=o.data;me.calc_loop_triangles();bvh=BVHTree.FromPolygons([v.co for v in me.vertices],[tuple(t.vertices) for t in me.loop_triangles],all_triangles=True);attr=me.color_attributes.new(name='PaintedCavity',type='FLOAT_COLOR',domain='POINT');values=[]
 for v in me.vertices:
  n=v.normal.normalized();u=n.cross(Vector((0,0,1)))
  if u.length<.01:u=n.cross(Vector((0,1,0)))
  u.normalize();w=n.cross(u).normalized();occluded=0
  for j in range(12):
   z=.22+.72*((j+.5)/12);a=j*2.399963;r=math.sqrt(1-z*z);direction=n*z+(u*math.cos(a)+w*math.sin(a))*r
   loc,no,face,dist=bvh.ray_cast(v.co+n*.0025,direction,.24)
   if loc is not None:occluded+=(1-dist/.24)*.70+.30
  val=max(.28,1-occluded/12*.76);attr.data[v.index].color=(val,val,val,1);values.append(val)
 print('CAVITY',o.name,min(values),sum(values)/len(values))
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
for row in names:
 o=bpy.data.objects[row['name']];bpy.ops.object.select_all(action='DESELECT');o.hide_set(False);o.select_set(True);bpy.context.view_layer.objects.active=o;o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
