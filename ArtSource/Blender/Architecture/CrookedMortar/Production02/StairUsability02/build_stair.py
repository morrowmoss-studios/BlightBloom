"""Production02-only open timber stair balustrades; unchanged flights/room envelope."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;R=D.parents[5];A=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/Models'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
im=bpy.data.images.load(str(R/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));im.pack();mat=bpy.data.materials.new('CM02_Walnut');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1;tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=im;mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);parts=[]
def P(p):return Vector((p[0],p[2],p[1]))
def box(n,p,d,collide=True,rotation=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=P(p));o=bpy.context.object;o.name=n;o.dimensions=P(d)
 if rotation:o.rotation_euler=rotation
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);b=o.modifiers.new('Soft joinery edge','BEVEL');b.width=.003 if min(d)<.08 else .006;b.segments=2;bpy.ops.object.modifier_apply(modifier=b.name);o.data.materials.append(mat)
 while o.data.uv_layers:o.data.uv_layers.remove(o.data.uv_layers[0])
 uv=o.data.uv_layers.new(name='PaintUV0')
 for f in o.data.polygons:
  axes=sorted(range(3),key=lambda a:abs(f.normal[a]))[:2];vs=[o.data.vertices[o.data.loops[i].vertex_index].co for i in f.loop_indices];lo=[min(v[a] for v in vs) for a in axes]
  span=max(max(v[a] for v in vs)-lo[j] for j,a in enumerate(axes));scale=min(.13,.44/max(span,.001))
  for li,v in zip(f.loop_indices,vs):uv.data[li].uv=(.53+(v[axes[0]]-lo[0])*scale,.53+(v[axes[1]]-lo[1])*scale)
 parts.append(o)

 return o

def beam(n,a,b,w,h=None):
 a=P(a);b=P(b);o=box(n,((a.x+b.x)/2,(a.z+b.z)/2,(a.y+b.y)/2),(w,(h or w),(b-a).length),False)
 # Local Blender Y is Unity forward. Author beam along local Y then align to slope.
 o.rotation_euler=(b-a).to_track_quat('Y','Z').to_euler()
 return o
# Upper flight centre edge: sloping 1.05 m handrail, not a flat solid partition.
def floor(z):return 3.6-(z-4.6)*(1.7/2.7)
for i,z in enumerate([4.65,5.3,5.95,6.6,7.25]):
 y=floor(z);box('CentreNewel_%02d'%i,(-.4,y+.52,z),(.115,1.10,.115));box('CentrePostCap_%02d'%i,(-.4,y+1.09,z),(.14,.055,.14))
beam('CentreSlopingHandrail',(-.4,4.65,4.6),(-.4,2.95,7.3),.09,.075)
beam('CentreLowRail',(-.4,3.76,4.6),(-.4,2.06,7.3),.065,.065)
for i in range(14):
 z=4.7+i*2.5/13;y=floor(z);box('CentreSpindle_%02d'%i,(-.4,y+.57,z),(.032,.82,.032))
# Wall-side upper-flight railing and rear wall rail removed: full-height walls already protect these edges.
# Protect the previously open upper-floor edge over the LOWER flight; leave the upper-flight entry clear.
for i,x in enumerate([-1.94,-.4]):
 box('OpeningNewel_%02d'%i,(x,4.14,4.55),(.115,1.1,.115));box('OpeningPostCap_%02d'%i,(x,4.71,4.55),(.14,.055,.14))
box('OpeningHandrail',(-1.17,4.65,4.55),(1.65,.075,.09))
box('OpeningLowRail',(-1.17,3.76,4.55),(1.65,.065,.065))
for i in range(10):box('OpeningSpindle_%02d'%i,(-1.88+i*1.42/9,4.18,4.55),(.032,.82,.032))
# Proper stringers finish the exposed upper flight underside, outside the walking faces.
for x in [-.36,1.26]:beam('UpperStringer', (x,3.42,4.6),(x,1.72,7.3),.10,.18)
# Landings extend to the enclosing wall; no room footprint change.
box('FittedTurnLandingFloor',(-.4,1.8,8.15),(3.2,.2,1.7),False)
checks=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume();bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-11 for t in o.data.loop_triangles);checks.append(dict(name=o.name,triangles=len(o.data.loop_triangles),nonmanifold=bad,volume=vol,degenerate=deg))
 if bad or deg or vol<=0:raise RuntimeError(checks[-1])
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM02_OpenTimberStair.blend'))
# Keep editable source parts; export five logical batches, not one renderer per spindle.
groups={}
for o in parts:
 key='LandingFloor' if 'Floor' in o.name else 'Balusters' if 'Spindle' in o.name else 'Newels' if ('Newel' in o.name or 'PostCap' in o.name or 'LandingCap' in o.name) else 'Stringers' if 'Stringer' in o.name else 'Handrails'
 groups.setdefault(key,[]).append(o)
export=[]
for key,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='CM02_Stair_'+key;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);export.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in export:o.select_set(True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.context.view_layer.objects.active=export[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(A/'CM02_OpenTimberStair.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'MeshValidation.json').write_text(json.dumps(checks,indent=2));print('OPEN_STAIR_OK',len(parts),sum(c['triangles'] for c in checks))
