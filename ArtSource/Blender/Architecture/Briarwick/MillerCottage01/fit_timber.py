"""Resolve only new cottage's flush sill/tie coplanarity against plaster."""
import bpy,bmesh,json
from pathlib import Path
from mathutils import Matrix
H=Path(__file__).parent;R=H.parents[4];P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_MillerCottage01.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['BW_MillerCottage01_Timber']
if o.get('flush_fit'):raise RuntimeError('Already fitted')
bm=bmesh.new();bm.from_mesh(o.data);remaining=set(bm.verts);count=0
while remaining:
 start=remaining.pop();vs={start};stack=[start]
 while stack:
  for e in stack.pop().link_edges:
   for v in e.verts:
    if v in remaining:remaining.remove(v);vs.add(v);stack.append(v)
 qs=[P.inverted()@v.co for v in vs];lo=[min(q[i] for q in qs) for i in range(3)];hi=[max(q[i] for q in qs) for i in range(3)];cz=(lo[2]+hi[2])/2
 if hi[0]-lo[0]>1 and hi[1]-lo[1]<.3 and abs(abs(cz)-3.9)<.02:
  for v in vs:q=P.inverted()@v.co;q.z=cz+(q.z-cz)*1.4;v.co=P@q
  count+=1
bm.to_mesh(o.data);bm.free();o['flush_fit']=True;o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.ops.export_scene.fbx(filepath=str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/MillerCottage01/Models/BW_MillerCottage01_Timber.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP');bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_MillerCottage01.blend'));print('Fitted',count,'ties/sills')
