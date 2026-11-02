"""Selective derivatives, in metres. Original package meshes are retained read-only.
Established FBX convention: Unity(x,y,z) -> Blender(-x,-z,y), -Z forward/+Y up.
UV loops retained through local deformation, welding and small angle-limited bevels.
"""
import bpy,bmesh,json,math
import sys
from pathlib import Path
from mathutils import Vector,Matrix
HERE=Path(__file__).parent;ROOT=HERE.parents[5]
OUT=ROOT/'Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageA/Style01/Models'
assert (ROOT/'AGENTS.md').exists()
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
bpy.context.preferences.filepaths.save_version=0
source=bpy.data.collections.new('READ_ONLY_original_mesh_reference');s.collection.children.link(source);source.hide_render=True;source.hide_viewport=True
edits=bpy.data.collections.new('EDITABLE_derivative_meshes_at_native_pivots');s.collection.children.link(edits);edits.hide_render=True;edits.hide_viewport=True
preview=bpy.data.collections.new('ASSEMBLED_CottageA_Style01');s.collection.children.link(preview)
P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
def pt(v):return P@Vector(v)
paint=json.loads((HERE/'PaintManifest.json').read_text());mats={}
for role in json.loads((HERE/'SourceMaterials.json').read_text()):
 key=role['name'];p=next((p for p in paint if p['sourceRole']==key),None)
 path=ROOT/(p['baseMap'] if p else next(t['path'] for t in role['textures'] if t['property']=='_BaseMap'))
 mat=bpy.data.materials.new(key);mat.use_nodes=True;n=mat.node_tree.nodes;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.8
 tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True);tex.image.pack();mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);mats[key]=mat
orig={};data=json.loads((HERE/'SourceMeshReadOnly.json').read_text())
for d in data:
 me=bpy.data.meshes.new(d['name']);faces=[];slots=[]
 for i,tri in enumerate(d['submeshes']):
  for j in range(0,len(tri),3):faces.append(tri[j:j+3]);slots.append(i)
 me.from_pydata([pt(v) for v in d['vertices']],[],faces);me.update();uv=me.uv_layers.new(name='UVMap')
 for poly,slot in zip(me.polygons,slots):
  poly.material_index=slot
  for li in poly.loop_indices:uv.data[li].uv=d['uv'][me.loops[li].vertex_index]
 for name in d['materials']:me.materials.append(mats[name])
 obj=bpy.data.objects.new(d['name'],me);source.objects.link(obj);orig[d['name']]=obj
def newmesh(src,name,fn=None,bevel=.005):
 o=orig[src].copy();o.data=o.data.copy();o.name=name;o.data.name=name;edits.objects.link(o)
 if not fn and not bevel:return o
 if fn:
  for v in o.data.vertices:v.co=pt(fn(P.inverted()@v.co))
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000015);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 bpy.context.view_layer.objects.active=o;o.hide_set(False)
 # Modifier application does not require the collection to be visible.
 if bevel:
  b=o.modifiers.new('Selective worn arris, millimetres','BEVEL');b.width=bevel;b.segments=2;b.limit_method='ANGLE';b.angle_limit=.60;b.affect='EDGES'
  if name in ['BW_Cottage01_EntryFrame','BW_Cottage01_DoorLeaf']:
   # Preserve detailed original ironwork. Bevel only structural timber edges.
   bm=bmesh.new();bm.from_mesh(o.data);layer=bm.edges.layers.float.new('bevel_weight_edge')
   for e in bm.edges:e[layer]=1.0 if e.is_manifold and e.calc_face_angle()>.60 and all(o.data.materials[f.material_index].name in ['wood1','wood2','wood3','doors'] for f in e.link_faces) else 0.0
   bm.to_mesh(o.data);bm.free();b.limit_method='WEIGHT'
  bpy.ops.object.modifier_apply(modifier=b.name)
 for f in o.data.polygons:f.use_smooth=True
 o.data.set_sharp_from_angle(angle=.65)
 wn=o.modifiers.new('Weighted joinery normals','WEIGHTED_NORMAL');wn.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=wn.name)
 if name in ['BW_Cottage01_EntryFrame','BW_Cottage01_DoorLeaf']:
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free()
 return o
def xmap(x):
 a=abs(x)
 return math.copysign(a*.65/.34 if a<=.34 else .65+(a-.34)*(.17/.16),x)
def ymap(y):
 if y<=.11268:return y
 if y<=1.948:return .11268+(y-.11268)*(2.30/(1.948-.11268))
 return 2.41268+(y-1.948)*((3-2.41268)/(3-1.948))
def frame(v):return (xmap(v.x),ymap(v.y),v.z)
def door(v):
 offx=-.38378906;offy=.112680376
 return ((v.x+.00175786018)/.72605136*1.27-.635-offx,v.y/1.83421123*2.27,v.z)
specs=[('wall_wood_entry_1m_1.001','BW_Cottage01_EntryFrame',frame,.004),('wall_wood_door1.004','BW_Cottage01_DoorLeaf',door,.0025),('steps2.002','BW_Cottage01_EntranceSteps',lambda v:(v.x*1.55,v.y,v.z),.006),('wooden_post_column_size1.079','BW_Cottage01_SoftenedPost',None,.007),('wooden_post_horizontal_long.100','BW_Cottage01_SoftenedBeam',None,.005),('roof_wide1_end.005','BW_Cottage01_GableEndNarrow',None,0),('roof_wide2_end.001','BW_Cottage01_GableEndWide',None,0),('roof_wide1_3.002','BW_Cottage01_EaveNarrow',None,.006),('roof_wide2_3.001','BW_Cottage01_EaveWide',None,.006)]
modified={src:newmesh(src,name,fn,bev) for src,name,fn,bev in specs}
# Gable infill is intentionally unchanged: the imported thin surfaces do not benefit
# from a global bevel. Preserve their original topology, winding and UV registration.
# Two small through-pegs at the entrance lintel joints: joinery, not loose dressing.
entry=modified['wall_wood_entry_1m_1.001'];pegs=[]
for x in [-.727,.727]:
 bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.014,depth=.025,location=pt((x,2.50,.075)),rotation=(math.pi/2,0,0))
 p=bpy.context.object;p.data.materials.append(mats['wood2'])
 for uv in p.data.uv_layers.active.data:uv.uv=(.5+uv.uv.x*.01,.4+uv.uv.y*.01)
 pegs.append(p)
edits.hide_viewport=False
bpy.ops.object.select_all(action='DESELECT');entry.select_set(True)
for p in pegs:p.select_set(True)
bpy.context.view_layer.objects.active=entry;bpy.ops.object.join()
records=json.loads((ROOT/'ArtSource/Pipeline/Review/BriarwickFirstHouseTest01/Assembly.json').read_text())['modules']
def keyfor(name):return max((k for k in orig if name.startswith(k.split('.')[0])),key=lambda k:len(k.split('.')[0]))
for r in records:
 src=keyfor(r['name']);template=modified.get(src,orig[src]);o=bpy.data.objects.new(r['name'],template.data);preview.objects.link(o)
 pos=list(r['position']);scale=list(r['scale'])
 if r['name']=='wall_wood_2m_window.004':pos[0]-=.16;scale[0]*=.84
 if r['name']=='wall_wood_1m_2':pos[0]+=.16;scale[0]*=.68
 o.location=pt(pos)
 x,y,z=[math.radians(v) for v in r['rotation']]
 rot=Matrix.Rotation(y,3,'Y')@Matrix.Rotation(x,3,'X')@Matrix.Rotation(z,3,'Z')
 o.rotation_euler=(P@rot@P.inverted()).to_euler();o.scale=scale[0],scale[2],scale[1]
for o in modified.values():
 if '--entrance-only' in sys.argv and o.name not in ['BW_Cottage01_EntryFrame','BW_Cottage01_DoorLeaf','BW_Cottage01_GableEndNarrow','BW_Cottage01_GableEndWide']:continue
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(OUT/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
edits.hide_viewport=True
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'BW_FamilyCottageA_Style01.blend'))
report=[]
for src,o in modified.items():
 o.data.calc_loop_triangles();report.append({'sourceMesh':src,'replacement':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'uvLoops':len(o.data.uv_layers.active.data),'materials':[m.name for m in o.data.materials],'exportMaterialOrder':[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]})
(HERE/'GeometryManifest.json').write_text(json.dumps(report,indent=2));print('COTTAGE_REFINEMENT_READY',len(report),sum(m['triangles'] for m in report))
