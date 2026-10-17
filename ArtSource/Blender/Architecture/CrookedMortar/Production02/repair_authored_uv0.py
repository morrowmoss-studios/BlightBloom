import bpy,ast,math,json
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[5];O=Path(__file__).parent;A=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02'
bpy.ops.wm.open_mainfile(filepath=str(O/'CM_CrookedMortar_Production02.blend'));bpy.context.preferences.filepaths.save_version=0
mats={k:(bpy.data.materials.get('CM02_'+k) or bpy.data.materials.new('CM02_'+k)) for k in ['Plaster','Walnut','Stone','Slate','Linen','Glass']};mats['Linen'].diffuse_color=(.43,.44,.28,1);rects={'Plaster':(.015,.515,.47,.47),'Walnut':(.515,.515,.47,.47),'Stone':(.015,.515,.47,.47),'Linen':(.015,.515,.47,.47)}
tree=ast.parse((O/'build_production02.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='uvmap'],type_ignores=[]),'<UV helper>','exec'))
objects=[o for o in bpy.data.objects if o.type=='MESH' and o.get('materialRole')]
for o in objects:
 key=o['materialRole'];uvmap(o,'Linen' if o.name.startswith('Bedroom bed') or o.name.startswith('Examination bed') or o.name.startswith('Living bench') else key)
bpy.ops.wm.save_as_mainfile(filepath=str(O/'CM_CrookedMortar_Production02.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM02_FittedArchitecture.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
print('REPAIRED_AUTHORED_UV0',len(objects))
