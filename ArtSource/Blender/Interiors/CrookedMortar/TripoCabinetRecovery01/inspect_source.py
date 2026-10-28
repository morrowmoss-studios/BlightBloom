import bpy,json,hashlib,time
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;src=D.parent/'TripoImports/rustic wooden cabinet 3d model.glb'
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(src))
original=list(bpy.context.scene.objects)
for o in original:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True)
  bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.separate(type='LOOSE');bpy.ops.object.mode_set(mode='OBJECT')
report=[]
for i,o in enumerate(list(bpy.context.scene.objects)):
 if o.type!='MESH':continue
 o.name=f'Island_{i:04d}';pts=[o.matrix_world@Vector(v) for v in o.bound_box];lo=[min(p[j] for p in pts) for j in range(3)];hi=[max(p[j] for p in pts) for j in range(3)]
 report.append(dict(name=o.name,vertices=len(o.data.vertices),triangles=len(o.data.polygons),min=lo,max=hi))
report.sort(key=lambda x:-x['triangles'])
(D/'Inspection.json').write_text(json.dumps({'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'islands':report},indent=2))
for im in bpy.data.images:
 if im.type=='IMAGE':
  (D/'Textures').mkdir(exist_ok=True);im.filepath_raw=str(D/'Textures'/im.name);im.save();print('TEXTURE',im.name,tuple(im.size))
bpy.ops.wm.save_as_mainfile(filepath=str(D/'ImportedIslands.blend'))
print('ISLANDS',len(report));print(json.dumps(report[:30],indent=2))
# quick overview: imported glTF Y-up becomes Blender Z-up
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
for p,e in [((1,-2,3),140),((-2,-1,1),90)]:
 d=bpy.data.lights.new('Studio','AREA');d.energy=e;d.size=3;o=bpy.data.objects.new('Studio',d);s.collection.objects.link(o);o.location=p;o.rotation_euler=(Vector((0,0,.35))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Camera');o=bpy.data.objects.new('Camera',d);s.collection.objects.link(o);o.location=(1.1,-2.5,1.1);o.rotation_euler=(Vector((0,0,.37))-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=1.25;s.camera=o;s.render.filepath=str(D/'InspectionOverview.png');bpy.ops.render.render(write_still=True)
