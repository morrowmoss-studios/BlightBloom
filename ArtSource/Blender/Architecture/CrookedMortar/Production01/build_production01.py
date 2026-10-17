"""Integration-only fitted building: approved B geometry, approved paint, no source edits."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[5];O=Path(__file__).parent;A=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production01'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.open_mainfile(filepath=str(R/'ArtSource/Blender/Architecture/CrookedMortar/MassingRefinements05/CM_Refinement05_B.blend'))
parts=[];kinds={};furniture=[]
def P(x,y,z):return(x,z,y)
def box(n,p,d,key='Walnut',bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=P(*p));o=bpy.context.object;o.name=n;o.dimensions=P(*d);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 if bevel:
  m=o.modifiers.new('Soft handcrafted edges','BEVEL');m.width=bevel;m.segments=2;bpy.ops.object.modifier_apply(modifier=m.name)
 m=bpy.data.materials.get('FitRole_'+key) or bpy.data.materials.new('FitRole_'+key);o.data.materials.append(m);kinds[o.name]=key;return o
def cut(o,c):
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Fitted rough opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)
# Retain the exact approved occupied envelope, 18-riser stair and roof carriers.
keep=lambda n:n.startswith(('Shell','Interior','Floor','Stairs','Roof_','Chimney','Entry_','Porch','Structure','Window')) and not n.endswith('Bargeboard')
for o in list(bpy.context.scene.objects):
 if o.type!='MESH' or not keep(o.name):bpy.data.objects.remove(o,do_unlink=True);continue
 key='Plaster' if o.name.startswith(('Shell','Interior','Stairs_UpperGuard')) or 'Gable' in o.name else 'Walnut'
 if o.name.startswith('Roof_') and 'Gable' not in o.name:key='RoofBacking'
 if o.name.startswith('Floor_Porch') or o.name=='Chimney':key='Stone'
 kinds[o.name]=key;parts.append(o)
# The paired insert needs .84 x 1.69m rough openings, not the old .76m display holes.
shell=bpy.data.objects.get('Shell')
bpy.ops.object.select_all(action='DESELECT');shell.select_set(True);bpy.context.view_layer.objects.active=shell;bpy.ops.mesh.separate(type='LOOSE')
shell=next(o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Shell') and abs((o.matrix_world@sum((v.co for v in o.data.vertices),Vector())/len(o.data.vertices)).y+4.05)<.01)
for x in [-.95,.03]:cut(shell,box('TEMP',(x,5.355,-4.05),(.84,1.69,1.0)))
# Bedroom partition aligns with the paired central post rather than bisecting a casement.
interior=bpy.data.objects.get('Interior')
for v in interior.data.vertices:
 w=interior.matrix_world@v.co
 if w.z>3.4 and w.y<-.85:w.x-=.21;v.co=interior.matrix_world.inverted()@w
# Remove only the superseded front paired casement components from the old combined window mesh.
win=bpy.data.objects.get('Window');bm=bmesh.new();bm.from_mesh(win.data)
visited=set();kill=[]
for start in bm.verts:
 if start in visited:continue
 stack=[start];group=[];visited.add(start)
 while stack:
  v=stack.pop();group.append(v)
  for e in v.link_edges:
   u=e.other_vert(v)
   if u not in visited:visited.add(u);stack.append(u)
 c=sum((win.matrix_world@v.co for v in group),Vector())/len(group)
 if (c.z>4.35 and c.y< -3.9 and -1.55<c.x<.65) or (1.90<c.x<2.10 and -1.8<c.y<.0 and c.z>4.3):kill.extend(group)
bmesh.ops.delete(bm,geom=kill,context='VERTS');bm.to_mesh(win.data);bm.free()
# Fitted plaster corner infills convert the approved east rectangular rough aperture to an arch.
for side in [-1,1]:
 curve=[]
 for j in range(13):
  a=(math.pi/2)*j/12;curve.append((-.9+side*.7*math.cos(a),5.2+.8*math.sin(a)))
 poly=curve+[(curve[-1][0],6.0),(curve[0][0],6.0)]
 # Drop coincident crown vertices, retain a clean closed extruded polygon.
 poly=[p for i,p in enumerate(poly) if i==0 or (Vector(p)-Vector(poly[i-1])).length>1e-6]
 if (Vector(poly[0])-Vector(poly[-1])).length<1e-6:poly.pop()
 n=len(poly);vs=[(x,z,y) for x in [1.74,1.96] for z,y in poly];fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new('ArchedReveal');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Shell_EastArchedReveal_'+str(side),me);bpy.context.scene.collection.objects.link(o);kinds[o.name]='Plaster'
# Separation yields independently reusable fitted wall / partition components, not a second box shell.
for o in [shell,interior]:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.mesh.separate(type='LOOSE')
parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];
for o in parts:
 if o.name.startswith('Shell'):kinds[o.name]='Plaster'
 if o.name.startswith('Interior'):kinds[o.name]='Plaster'
# Enclosed rear storage, with an aligned 1.45m doorway on the garden circulation line.
for n,p,d in [('StorageLeft',(-.025,1.62,4.30),(.75,2.84,.14)),('StorageRight',(1.95,1.62,4.30),(.30,2.84,.14)),('StorageHeader',(1.075,3.155,4.30),(1.45,.33,.14))]:parts.append(box(n,p,d,'Plaster'))
# Modest functional fixtures: purpose-readable rooms, generous central walking lanes.
def furnishing(name,items,collision):
 objs=[]
 for suffix,p,d,key in items:objs.append(box(name+'_'+suffix,p,d,key,.018))
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name=name;parts.append(o);furniture.append({'name':name,'collision':collision});return o
furnishing('ShopCounter', [('Cabinet',(1.50,.70,-.65),(.65,1.0,1.70),'Walnut'),('Top',(1.48,1.24,-.65),(.78,.08,1.80),'Walnut')],[[1.5,.74,-.65,.78,1.08,1.8]])
furnishing('TreatmentCouch',[('Base',(-.04,.50,3.23),(.62,.60,1.45),'Walnut'),('Cushion',(-.04,.86,3.23),(.65,.15,1.48),'Linen')],[[-.04,.57,3.23,.65,.87,1.48]])
furnishing('PreparationBench',[('Cabinet',(3.54,.67,2.62),(.48,.94,1.65),'Walnut'),('StoneTop',(3.54,1.17,2.62),(.56,.08,1.70),'Stone')],[[3.54,.70,2.62,.56,1.02,1.7]])
furnishing('StorageCabinet',[('Case',(-.12,.94,4.98),(.36,1.48,.72),'Walnut')],[[-.12,.94,4.98,.36,1.48,.72]])
furnishing('BedroomBed',[('Frame',(-1.72,3.69,-3.02),(1.05,.5,1.62),'Walnut'),('Mattress',(-1.72,4.00,-3.02),(1.01,.16,1.58),'Linen'),('Headboard',(-1.72,4.20,-3.87),(1.12,.90,.10),'Walnut')],[[-1.72,3.95,-3.02,1.12,1.02,1.72]])
furnishing('LivingSettle',[('Seat',(1.45,3.71,-3.08),(.55,.52,1.35),'Walnut'),('Cushion',(1.43,4.02,-3.08),(.55,.13,1.31),'Linen'),('Back',(1.73,4.11,-3.08),(.10,1.0,1.40),'Walnut')],[[1.45,3.98,-3.08,.66,1.08,1.4]])
furnishing('StudyWritingDesk',[('Top',(3.55,4.25,2.02),(.50,.08,1.02),'Walnut'),('LeftLeg',(3.55,3.83,1.62),(.32,.78,.10),'Walnut'),('RightLeg',(3.55,3.83,2.42),(.32,.78,.10),'Walnut')],[[3.55,3.85,2.02,.50,.82,1.02]])
furnishing('MedicalLibraryShelves',[('Back',(3.73,4.45,4.0),(.10,2.02,1.12),'Walnut')]+[('Shelf'+str(i),(3.58,3.57+i*.45,4.0),(.38,.06,1.12),'Walnut') for i in range(5)],[[3.58,4.45,4.0,.4,2.02,1.12]])
# Fit the counter beneath the front shop display, clear of the inward-open door leaf.
co=next(o for o in parts if o.name=='ShopCounter')
for v in co.data.vertices:
 w=co.matrix_world@v.co;dx=w.x-1.5;dz=w.y+.65;w.x=-1.2+dz;w.y=-2.65-dx;v.co=co.matrix_world.inverted()@w
next(x for x in furniture if x['name']=='ShopCounter')['collision']=[[-1.2,.74,-2.65,1.8,1.08,.78]]
# Shared approved painting sheet, explicit texture UVs: no new noise or material redesign.
paint=bpy.data.images.load(str(R/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));paint.pack();mats={}
for k in ['Plaster','Walnut','Stone','RoofBacking','Linen','Glass']:
 m=bpy.data.materials.new('CM_Production01_'+k);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1
 if k in ['Plaster','Walnut','Stone','RoofBacking']:
  t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=paint;m.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
 else:bs.inputs['Base Color'].default_value=(.43,.44,.28,1) if k=='Linen' else(.43,.29,.11,1)
 mats[k]=m
for o in parts:
 # Remember face roles before replacing material slots (windows, unioned dormer).
 old=[m.name for m in o.data.materials];roles=[]
 for f in o.data.polygons:
  k=kinds.get(o.name,'Walnut');src=old[f.material_index] if f.material_index<len(old) else ''
  if o.name=='Window':k='Glass' if 'Glass' in src else 'Walnut'
  if o.name=='Roof_Hero' and 'Plaster' in src:k='Plaster'
  if o.name in [x['name'] for x in furniture]:k='Linen' if 'Linen' in src else ('Stone' if 'Stone' in src else 'Walnut')
  roles.append(k)
 o.data.materials.clear()
 for k in mats:o.data.materials.append(mats[k])
 for f,k in zip(o.data.polygons,roles):f.material_index=list(mats).index(k)
 while o.data.uv_layers:o.data.uv_layers.remove(o.data.uv_layers[0])
 uv=o.data.uv_layers.new(name='UVMap')
 coords=[o.matrix_world@v.co for v in o.data.vertices];mins=[min(v[i] for v in coords) for i in range(3)];maxs=[max(v[i] for v in coords) for i in range(3)];dims=[maxs[i]-mins[i] for i in range(3)];long=max(range(3),key=lambda i:dims[i]);across=max([i for i in range(3) if i!=long],key=lambda i:dims[i])
 for f,k in zip(o.data.polygons,roles):
  norm=o.matrix_world.to_3x3()@f.normal
  for li in f.loop_indices:
   p=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   dominant=max(range(3),key=lambda i:abs(norm[i]));axes=[i for i in range(3) if i!=dominant]
   if k in ['Plaster','Stone']:
    vertical=2 if 2 in axes else axes[1];horizontal=next(i for i in axes if i!=vertical)
    u=(p[horizontal]-mins[horizontal])/max(4,dims[horizontal]);v=(p[vertical]-mins[vertical])/max(4,dims[vertical])
   else:
    grain=long if long in axes else axes[1];cross=next(i for i in axes if i!=grain)
    u=(p[cross]-mins[cross])/max(.8,dims[cross]);v=(p[grain]-mins[grain])/max(3.6,dims[grain])
   u=.03+.94*u;v=.03+.94*v
   ox,oy=(.512,.512) if k=='Walnut' else ((.512,.012) if k=='RoofBacking' else(.012,.512));uv.data[li].uv=(ox+.476*u,oy+.476*v)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6) if not o.name.startswith("Stairs_Straight") else None;bmesh.ops.dissolve_degenerate(bm,dist=1e-7,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Stable independent logical pieces grouped in Blender collections and in Unity prefab.
report=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);uv=o.data.uv_layers.active;uvbad=0
 for f in o.data.polygons:
  a,b,c=[Vector(uv.data[li].uv) for li in f.loop_indices];uvbad+=abs((b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x))<1e-13
 pts=[o.matrix_world@v.co for v in o.data.vertices]
 report.append({'name':o.name,'triangles':len(o.data.polygons),'nonmanifold':sum(not e.is_manifold for e in bm.edges),'volume':bm.calc_volume(signed=True),'degenerateUVTriangles':uvbad,'unityBoundsMin':[min(v[i] for v in pts) for i in [0,2,1]],'unityBoundsMax':[max(v[i] for v in pts) for i in [0,2,1]]});bm.free()
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.wm.save_as_mainfile(filepath=str(O/'CM_CrookedMortar_Production01.blend'))
for o in parts:o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);bpy.context.view_layer.update()
bpy.ops.export_scene.fbx(filepath=str(A/'Models/CM_Production01_FittedBuilding.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(O/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(O/'FurnitureCollision.json').write_text(json.dumps(furniture,indent=2));print('PRODUCTION_EXPORT',len(parts),sum(x['triangles'] for x in report))
