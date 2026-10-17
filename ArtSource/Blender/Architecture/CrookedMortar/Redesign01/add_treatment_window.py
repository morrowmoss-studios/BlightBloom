"""Add a small, high-sill treatment-room window to the recessed street elevation.
Keeps its position offset from the upper living window; no new decorative props.
"""
import bpy,bmesh,json,math
from pathlib import Path
out=Path(__file__).parent;path=out/'CM_Redesign01_Geometry.blend';bpy.ops.wm.open_mainfile(filepath=str(path))
if bpy.context.scene.get('treatment_window_added'):raise RuntimeError('Treatment window already present')
shell=bpy.data.objects['Shell']
# Boolean only the connected front-wall component; other joined wall solids stay untouched.
bm=bmesh.new();bm.from_mesh(shell.data);bm.verts.ensure_lookup_table();bm.verts.index_update();remaining=set(bm.verts);chosen=None
while remaining:
 seed=next(iter(remaining));todo=[seed];comp=set()
 while todo:
  v=todo.pop()
  if v in comp:continue
  comp.add(v);todo.extend(e.other_vert(v) for e in v.link_edges if e.other_vert(v) not in comp)
 remaining-=comp
 lo=[min(v.co[i] for v in comp) for i in range(3)];hi=[max(v.co[i] for v in comp) for i in range(3)]
 if abs(lo[0]+.5)<.01 and abs(hi[0]-6.3)<.01 and abs(lo[1]+2.62)<.01 and abs(hi[1]+2.38)<.01:chosen=comp;break
assert chosen is not None,'Front-wall component not found'
ids={v.index for v in chosen};isolated=bm.copy();isolated.verts.ensure_lookup_table();bmesh.ops.delete(isolated,geom=[v for v in isolated.verts if v.index not in ids],context='VERTS');me=bpy.data.meshes.new('Treatment facade component');isolated.to_mesh(me);isolated.free()
for mat in shell.data.materials:me.materials.append(mat)
bfront=bpy.data.objects.new('TEMP_front_facade_component',me);bpy.context.scene.collection.objects.link(bfront);bmesh.ops.delete(bm,geom=list(chosen),context='VERTS');bm.to_mesh(shell.data);bm.free()

def cube(name,loc,size,mat):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(loc[0],loc[2],loc[1]));o=bpy.context.object;o.name=name;o.dimensions=(size[0],size[2],size[1]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if mat:o.data.materials.append(bpy.data.materials[mat])
 return o
cut=cube('TEMP_treatment_window',(.9,1.95,-2.5),(1.0,1.10,1),None);bpy.context.view_layer.objects.active=bfront;mod=bfront.modifiers.new('Treatment privacy window','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT');shell.select_set(True);bfront.select_set(True);bpy.context.view_layer.objects.active=shell;bpy.ops.object.join()
new=[cube('Treatment glazing',(.9,1.95,-2.64),(1.0,1.09,.035),'Redesign_Glass')]
for x in [.4,1.4]:new.append(cube('Treatment window frame',(x,1.95,-2.68),(.08,1.26,.13),'Redesign_Timber'))
for y in [1.40,2.50]:new.append(cube('Treatment window frame',(.9,y,-2.68),(1.16,.08,.13),'Redesign_Timber'))
new.append(cube('Treatment window mullion',(.9,1.95,-2.71),(.055,1.1,.10),'Redesign_Timber'))
bpy.ops.object.select_all(action='DESELECT');window=bpy.data.objects['Window'];window.select_set(True)
for o in new:o.select_set(True)
bpy.context.view_layer.objects.active=window;bpy.ops.object.join()
bpy.ops.object.select_all(action='DESELECT');shell.select_set(True);window.select_set(True);bpy.context.view_layer.objects.active=shell
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.003);bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
r=json.loads((out/'geometry_validation.json').read_text());r['parts']=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();assert bad==0 and vol>0,(o.name,bad,vol)
 o.data.calc_loop_triangles();r['parts'].append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles),'nonmanifold':bad,'volume':vol})
r['triangles']=sum(p['triangles'] for p in r['parts']);r['treatment_window']={'centre_x':.9,'sill_y':1.4,'height':1.1,'width':1.0};bpy.context.scene['treatment_window_added']=True
bpy.ops.wm.save_as_mainfile(filepath=str(path));(out/'geometry_validation.json').write_text(json.dumps(r,indent=2));print('TREATMENT_WINDOW_READY',r['triangles'])
