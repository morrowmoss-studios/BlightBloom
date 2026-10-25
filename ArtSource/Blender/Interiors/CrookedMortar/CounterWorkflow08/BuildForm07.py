# Comparison-only derivative. Opens WF07 read-only; writes ONLY within WF08.
import bpy,bmesh,math
from pathlib import Path
from mathutils import Matrix
D=Path(__file__).resolve().parent;R=D.parents[4];A=R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow08/Models'
bpy.ops.wm.open_mainfile(filepath=str(D.parent/'CounterWorkflow07/CM_CounterWorkflow07.blend'))
g=bpy.data.objects['CM_CW07_HeroCounter'];bm=bmesh.new();bm.from_mesh(g.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if g.data.materials[f.material_index].name=='CM_CW07_CarvedWalnut'],context='FACES');bm.to_mesh(g.data);bm.free()
# Replace sculpt with the same plane datum, without changing original structural framing.
for cx,w in [(-.7,.527),(0,.65),(.7,.527)]:
 bm=bmesh.new();bm.from_mesh(g.data);v=[bm.verts.new((x,.314,y)) for x,y in [(cx-w/2,.252),(cx+w/2,.252),(cx+w/2,.789),(cx-w/2,.789)]];bm.faces.new(v);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(g.data);bm.free()
g.name='CM_CW07_FormOnlyComparison';g.data.name=g.name+'_Mesh';g.matrix_world=Matrix.Rotation(math.pi,4,'Z')@g.matrix_world;bpy.ops.object.select_all(action='DESELECT');g.hide_set(False);g.select_set(True);bpy.context.view_layer.objects.active=g;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'CM_CW07_FormOnlyComparison.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
