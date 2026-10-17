import bpy,bmesh,json
from pathlib import Path
out=Path(__file__).parent;path=out/'CM_Redesign01_Geometry.blend';bpy.ops.wm.open_mainfile(filepath=str(path))
# Extend the landing slab to meet the exact final tread (no 13cm gap).
o=bpy.data.objects['Floor_Upper_Landing']
for v in o.data.vertices:v.co.y=4.37+(v.co.y-4.5)*(5.8-4.37)/1.3
# Trim the cross-wing attic back to a 35cm supported overhang at the rear return.
# This volume lies behind the shop roof, so it preserves the actual roof-to-roof valley.
roof=bpy.data.objects['Roof_Main_CrossGable']
bpy.ops.mesh.primitive_cube_add(size=1,location=(-1.58,4.9,7.7));cut=bpy.context.object;cut.dimensions=(1.46,3.2,3.3);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
bpy.context.view_layer.objects.active=roof;mod=roof.modifiers.new('Supported rear roof return','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
for p in roof.data.polygons:p.material_index=1 if abs(p.normal.z)<.05 else (2 if p.normal.z<0 else 0)
# Re-unwrap the changed roof and repack all islands after the junction correction.
objs=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=roof;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=.96,island_margin=.003);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
r=json.loads((out/'geometry_validation.json').read_text());r['parts']=[]
for o in objs:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();assert bad==0 and vol>0,(o.name,bad,vol)
 o.data.calc_loop_triangles();r['parts'].append({'name':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'nonmanifold':bad,'volume':vol})
r['triangles']=sum(p['triangles'] for p in r['parts']);r['junction_refinements']=['landing extended to z4.37','roof rear return clipped to supported footprint']
bpy.ops.wm.save_as_mainfile(filepath=str(path));(out/'geometry_validation.json').write_text(json.dumps(r,indent=2));print('JUNCTIONS',r['triangles'])
