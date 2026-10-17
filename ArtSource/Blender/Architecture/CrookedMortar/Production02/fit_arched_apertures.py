"""Correct only the four new Production02 arched wall adapters; roof and kits unchanged."""
import bpy,bmesh,math,ast,json
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[5];O=Path(__file__).parent;A=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02'
bpy.ops.wm.open_mainfile(filepath=str(O/'CM_CrookedMortar_Production02.blend'));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene
mats={k:bpy.data.materials['CM02_'+k] for k in ['Plaster','Walnut','Stone','Slate','Linen']};rects={'Plaster':(.015,.515,.47,.47),'Walnut':(.515,.515,.47,.47),'Stone':(.015,.515,.47,.47),'Linen':(.015,.515,.47,.47)}
tree=ast.parse((O/'build_production02.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['P','box','cut','arch_cutter','uvmap']],type_ignores=[]),'<fitted opening helpers>','exec'))
lookup={'StudyFront':'Study front','KitchenEast':'Wing east ground','StudyEast':'Study east','LivingWest':'Upper shop west front'}
for w in json.loads((O/'WindowPlacements.json').read_text()):
 if w['name'] not in lookup:continue
 o=bpy.data.objects[lookup[w['name']]];cut(o,arch_cutter(w));uvmap(o,'Plaster');bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);assert bm.calc_volume(signed=True)>0;bm.to_mesh(o.data);bm.free()
 # Direct horizontal ray through the centre must miss this wall from both sides.
 from mathutils import Vector
 p=P((w['x'],w['y']+1.5,w['z']));direction=P((math.sin(math.radians(w['yaw'])),0,math.cos(math.radians(w['yaw']))));p=Vector(p);d=Vector(direction)
 assert not o.ray_cast(p+d*.4,-d,distance=.8)[0],w['name']
 assert not o.ray_cast(p-d*.4,d,distance=.8)[0],w['name']
 print('REAL_ARCH_OPENING',w['name'],flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(O/'CM_CrookedMortar_Production02.blend'))
objects=[o for o in bpy.data.objects if o.type=='MESH' and o.get('materialRole')];bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM02_FittedArchitecture.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
