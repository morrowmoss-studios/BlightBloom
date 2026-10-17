"""Audit the current authored geometry, detach overlapping projection faces, repack UVs.
Only new Redesign01 source is affected. Vertex positions and topology are preserved.
"""
from pathlib import Path
import bpy,json
from mathutils import Vector
out=Path(__file__).parent
# Reuse the exact positive-area triangle clipping audit, stopping before its assert.
code=(out/'validate_uvs.py').read_text().split("(out/'uv_overlap_details.json')")[0]
exec(compile(code,str(out/'validate_uvs.py'),'exec'))
faces=sorted(set(owners[t] for pair in overlaps for t in pair));print('UV_REPAIR_FACES',faces)
for idx,(name,face_id) in enumerate(faces):
 o=bpy.data.objects[name];p=o.data.polygons[face_id];normal=p.normal.normalized();ref=Vector((1,0,0)) if abs(normal.x)<.9 else Vector((0,1,0));u=normal.cross(ref).normalized();v=normal.cross(u).normalized()
 for li in p.loop_indices:
  pt=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers[0].data[li].uv=(20+idx*30+pt.dot(u),20+idx*30+pt.dot(v))
bpy.ops.object.select_all(action='SELECT');bpy.context.view_layer.objects.active=bpy.context.selected_objects[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'CM_Redesign01_Geometry.blend'));(out/'uv_repair.json').write_text(json.dumps({'detached_faces':faces,'mesh_geometry_changed':False},indent=2))
