"""Focused Production02 visual adapters. Original layout, source and kit exports preserved."""
import bpy,bmesh,json,math,ast
from pathlib import Path
from mathutils import Matrix,Vector
D=Path(__file__).resolve().parent; BASE=D.parent; R=BASE.parents[4]
AS=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/Models'
bpy.ops.wm.open_mainfile(filepath=str(BASE/'CM_CrookedMortar_Production02.blend'))
bpy.context.preferences.filepaths.save_version=0
roofs=json.loads((BASE/'RoofCarrierPlan.json').read_text()); parts=[]; report=[]
def P(p):return(p[0],p[2],p[1])
def normals(me):
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
def uv(o,key):
 while o.data.uv_layers:o.data.uv_layers.remove(o.data.uv_layers[0])
 lay=o.data.uv_layers.new(name='PaintUV0');u0=.515 if key=='Walnut' else .015
 for f in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(f.normal[a]));axes=[a for a in range(3) if a!=axis]
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co
   lay.data[li].uv=(u0+.02+(v[axes[0]]*.11)% .41,.535+(v[axes[1]]*.11)% .41)
 o.data.materials.clear();o.data.materials.append(bpy.data.materials['CM02_'+key])
def cutter(r):
 vv=[P((v[0],v[1]+.12,v[2])) for v in r['vertices']];n=len(vv);vv += [P((v[0],0,v[2])) for v in r['vertices']]
 fs=[tuple(t) for t in r['topTriangles']]+[tuple(i+n for i in reversed(t)) for t in r['topTriangles']]
 edges={}
 for tri in r['topTriangles']:
  for i,j in zip(tri,tri[1:]+tri[:1]):edges.setdefault(tuple(sorted((i,j))),[]).append((i,j))
 for pairs in edges.values():
  if len(pairs)==1:
   i,j=pairs[0];fs.append((i,j,j+n,i+n))
 me=bpy.data.meshes.new('EnvelopeCut');me.from_pydata(vv,[],fs);me.update();normals(me);o=bpy.data.objects.new('EnvelopeCut',me);bpy.context.scene.collection.objects.link(o);return o
cuts={r['name']:cutter(r) for r in roofs}
for o in list(bpy.data.objects):
 if not o.name.startswith('Gable_Roof_'):continue
 before=len(o.data.polygons); own=o.name[len('Gable_'):-2];bpy.context.view_layer.objects.active=o
 for name,c in cuts.items():
  if name==own:continue
  mod=o.modifiers.new('Trim concealed junction against adjacent roof envelope','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c
  bpy.ops.object.modifier_apply(modifier=mod.name)
 normals(o.data);o['replacesSceneMesh']=o.name;parts.append(o);report.append({'name':o.name,'facesBefore':before,'facesAfter':len(o.data.polygons)})
for c in cuts.values():bpy.data.objects.remove(c,do_unlink=True)
def box(name,p,d):
 bpy.ops.mesh.primitive_cube_add(size=1,location=P(p));o=bpy.context.object;o.name=name;o.dimensions=P(d);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 mod=o.modifiers.new('Small crafted edge','BEVEL');mod.width=.004;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name);normals(o.data);uv(o,'Walnut');parts.append(o)
# All finishing remains inside existing guard/wall footprints, outside clear flights.
box('Finish_RearLandingFootJoint',(-.4,1.915,8.84),(3.2,.06,.12))
box('Finish_RearLandingGuardCap',(-.4,3.005,8.85),(3.2,.05,.11))
box('Finish_CentreGuardCap',(-.4,3.305,5.95),(.19,.05,2.7))
box('Finish_UpperGuardCap',(1.3,4.705,6.65),(.19,.05,4.1))
for name,p,d in [('RearLeft',(-1.95,2.45,8.85),(.1,1.1,.1)),('RearRight',(1.25,2.45,8.85),(.1,1.1,.1)),('CentreEnd',(-.4,2.6,7.25),(.19,1.4,.1)),('UpperEntry',(1.3,4.15,4.65),(.19,1.1,.1))]:box('Finish_GuardEnd_'+name,p,d)
# Herb rail meets three ties; two short hangers connect it to the real canopy underside.
box('Finish_HerbRail',(.95,2.94,-1.65),(1.55,.08,.09))
for x in [.3,1.6]:box('Finish_HerbRailSuspension', (x,3.11,-1.65),(.045,.3,.045))
# Back plates rise into the canopy fascia; original curls and light levels retained.
for x,y in [(2.6,2.74),(4.8,2.93)]:box('Finish_LanternMountPlate',(x,(y+3.14)/2,-2.885),(.09,3.14-y,.055))
# Remove only redundant internal verges on the subordinate wing's buried end plane.
for name in ['CM02_Fitted_EaveVergeNetwork_Slate','CM02_Fitted_EaveVergeNetwork_Timber','CM02_Fitted_ValleyNetwork_Slate']:
 o=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(o.data);bm.verts.ensure_lookup_table();unseen=set(bm.verts);remove=[]
 while unseen:
  seen=set();todo=[next(iter(unseen))]
  while todo:
   v=todo.pop()
   if v in seen:continue
   seen.add(v);todo.extend(e.other_vert(v) for e in v.link_edges if e.other_vert(v) not in seen)
  unseen-=seen;xs=[v.co.x for v in seen]
  zs=[v.co.y for v in seen]
  if (name.endswith('ValleyNetwork_Slate') and min(xs)>5.25 and max(xs)<5.95 and min(zs)>1.3 and max(zs)<2.3) or (not name.endswith('ValleyNetwork_Slate') and max(xs)-min(xs)<.20 and abs((max(xs)+min(xs))/2-5.3)<.03):remove.extend(seen)
 bmesh.ops.delete(bm,geom=remove,context='VERTS');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();parts.append(o);o['replacesSceneMesh']=name
 report.append({'name':name,'redundantInternalVergeVerticesRemoved':len(remove)})
# Short fitted continuation of the subordinate roof into the main roof envelope.
# Closes the exposed end at x=5.3, without moving outer eaves, peaks or room volumes.
roofsrc=(R/'ArtSource/Blender/Architecture/CrookedMortar/SlateRoofKit01/build_slate_roof_kit01.py').read_text();tree=ast.parse(roofsrc)
names={'area','clean','clip','intersect','difference','contains','overlap','height','top_at','module','buf','uvpaint','solid_poly','prism_profile','flush','arc_map','tile_patch'}
EPS=1e-7;s=bpy.context.scene;modules={};buffers={};current=None;mats={k:bpy.data.materials['CM02_'+k] for k in ['Walnut','Slate']}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'<existing roof kit helpers>','exec'),globals())
wing=next(r for r in roofs if r['name']=='Roof_SubordinateWing');wing_count=len(wing['vertices'])//2
ret={'name':'Roof_WingJunctionReturn','vertices':[[3.0,v[1],v[2]] for v in wing['vertices'][:wing_count]]+[[5.3,v[1],v[2]] for v in wing['vertices'][wing_count:]],'topTriangles':wing['topTriangles']}
roofs.append(ret);obstacle={'name':'Chimney','vertices':[],'topTriangles':[]};raw={}
exec(roofsrc[roofsrc.index('tris=[]\nfor r in roofs+[obstacle]:'):roofsrc.index('modules={};')],globals())
left=[(v[2],v[1]) for v in wing['vertices'][:wing_count//2+1]]
# Recover the full monotonic front/back profile from the actual authored carrier.
full=[(v[2],v[1]) for v in wing['vertices'][:wing_count]];peak=max(range(wing_count),key=lambda k:full[k][1]);left=full[:peak+1];right=list(reversed(full[peak:]))
def course_coordinates(t):
 profile=left if t['plane'][1]>0 else right
 return (lambda x,z:(x-5.3,arc_map(profile,z))),(lambda u,v:(u+5.3,arc_map(profile,v,True))),1.
module('CM02_FittedWingJunctionReturn','Fitted return closes exposed inner wing roof end',[],kind='FittedAdapter')
for patch in [p for p in visible if p['tri']['name']==ret['name']]:
 tile_patch(patch);solid_poly('Underlay',patch['poly'],lambda x,z:height(patch['tri'],x,z)-.006,.10,1)
flush()
# Conformed valley liners seat on the actual upper envelope, including legacy course cut-outs.
# Replace the old standing segmented cap network; do not stack a second cap on it.
old_segments=json.loads((BASE/'Junctions.json').read_text())
allseg=[dict(a=Vector(j['a']),b=Vector(j['b'])) for j in old_segments if j['role']=='Valley']+[j for j in merged if j['role']=='Valley']
module('CM02_ConformedValleyLiners','Fitted slate valley channels below tile faces',[],kind='FittedAdapter')
covered={}
for seg in allseg:
 a,b=seg['a'],seg['b'];d=Vector((b.x-a.x,b.z-a.z))
 if d.length<.015:continue
 d.normalize();normal=Vector((-d.y,d.x));aa=Vector((a.x,a.z))-.012*d;bb=Vector((b.x,b.z))+.012*d
 corridor=clean([tuple(aa-normal*.045),tuple(bb-normal*.045),tuple(bb+normal*.045),tuple(aa+normal*.045)])
 for patch in visible:
  if not overlap(corridor,patch['poly']):continue
  poly=intersect(corridor,patch['poly'])
  if not poly:continue
  t=patch['tri'];key=t['index'];polys=[poly]
  for prior in covered.get(key,[]):polys=[q for p in polys for q in (difference(p,prior) if overlap(p,prior) else [p])]
  for p in polys:
   if abs(area(p))<1e-7:continue
   solid_poly('Slate',p,lambda x,z,t=t:height(t,x,z)+.012,.014,0,lambda x,z:(x*.25,z*.25));covered.setdefault(key,[]).append(p)
flush()
bpy.ops.object.select_all(action='DESELECT')
checks=[]
for o in parts:
 if not len(o.data.polygons):continue
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-11 for t in o.data.loop_triangles)
 checks.append({'name':o.name,'nonmanifold':bad,'volume':vol,'degenerate':deg,'triangles':len(o.data.loop_triangles)})
 if bad or vol<=0:raise RuntimeError(checks[-1])
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM02_ArchitecturalFinishing.blend'))
bpy.ops.object.select_all(action='DESELECT');export=[o for o in parts if len(o.data.polygons)]
for o in export:o.select_set(True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.context.view_layer.objects.active=export[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(AS/'CM02_ArchitecturalFinishing.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'GeometryValidation.json').write_text(json.dumps({'gables':report,'meshes':checks},indent=2));print('FINISHING_OK',len(export))
