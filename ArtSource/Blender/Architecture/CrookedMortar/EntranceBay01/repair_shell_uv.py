"""Detach one bevel UV face identified by validate_uvs.py; repack without mesh edits.
For the initial generated entrance source only; safe before the painted bake.
"""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
out=Path(__file__).parent;source=out/'CM_EntranceBay01_Geometry_v01.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
o=bpy.data.objects['01_Shell_Plaster_With_Arched_Opening'];p=o.data.polygons[207]
# Audit found 4 sub-pixel intersections of this bevel face with adjacent UVs.
original={'normal':list(p.normal),'area':p.area,'loop_count':len(p.loop_indices)}
normal=p.normal.normalized();ref=Vector((1,0,0)) if abs(normal.x)<.9 else Vector((0,0,1));u=normal.cross(ref).normalized();v=normal.cross(u).normalized();uv=o.data.uv_layers[0]
for li in p.loop_indices:
 point=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(2+point.dot(u),2+point.dot(v))
bpy.ops.object.select_all(action='DESELECT')
for obj in objects:obj.select_set(True)
bpy.context.view_layer.objects.active=o;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.004);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.wm.save_as_mainfile(filepath=str(source));(out/'uv_repair.json').write_text(json.dumps({'repaired_object':o.name,'detached_polygon':207,'face':original,'mesh_geometry_modified':False,'action':'independent planar UV island plus global average-scale/repack'},indent=2));print('UV bevel island detached and atlas repacked')
