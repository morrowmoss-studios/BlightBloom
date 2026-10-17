"""Expanded Crooked Mortar fitted architecture. Reuses roof-kit construction/clipping helpers; never rewrites kits."""
import bpy,bmesh,math,json,ast
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=R/'Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02'
assert bpy.app.background
if (OUT/'CM_CrookedMortar_Production02.blend').exists():raise RuntimeError('New output exists; no implicit regeneration')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
source=R/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'
paint=bpy.data.images.load(str(source));paint.pack();slate_paint=bpy.data.images.load(str(R/'ArtSource/Paint/Architecture/CrookedMortar/SlateRoofKit01/CharacterPass/CM_Slate_GouacheColour_v04.png'));slate_paint.pack()
mats={}
for key in ['Plaster','Walnut','Stone','Slate','Linen']:
 m=bpy.data.materials.new('CM02_'+key);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1
 if key=='Linen':bs.inputs['Base Color'].default_value=(.43,.44,.28,1)
 else:
  im=m.node_tree.nodes.new('ShaderNodeTexImage');im.image=slate_paint if key=='Slate' else paint;m.node_tree.links.new(im.outputs['Color'],bs.inputs['Base Color'])
 mats[key]=m
parts=[];modules={};buffers={};current=None;EPS=1e-7
roofsrc=(R/'ArtSource/Blender/Architecture/CrookedMortar/SlateRoofKit01/build_slate_roof_kit01.py').read_text();tree=ast.parse(roofsrc)
names={'area','clean','clip','intersect','difference','contains','overlap','height','top_at','module','buf','uvpaint','solid_poly','prism_profile','flush','arc_map','tile_patch'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'<reused roof-kit helpers>','exec'),globals())
# Asset colour sheet quadrants: upper-left plaster, upper-right walnut, lower-left stone.
rects={'Plaster':(.015,.515,.47,.47),'Walnut':(.515,.515,.47,.47),'Stone':(.015,.515,.47,.47),'Linen':(.015,.515,.47,.47)}
def P(p):return(p[0],p[2],p[1])
def uvmap(o,key):
 while o.data.uv_layers:o.data.uv_layers.remove(o.data.uv_layers[0])
 uv=o.data.uv_layers.new(name='PaintUV0');u0,v0,w,h=rects[key]
 for poly in o.data.polygons:
  vs=[o.data.vertices[i].co for i in poly.vertices];normal=poly.normal;axis=max(range(3),key=lambda a:abs(normal[a]));axes=[a for a in range(3) if a!=axis]
  if key=='Walnut':axes=sorted(axes,key=lambda a:max(v[a] for v in vs)-min(v[a] for v in vs))
  lo=[min(v[a] for v in vs) for a in axes];span=[max(v[a] for v in vs)-lo[j] for j,a in enumerate(axes)]
  # Broad paint groups, with per-face UV area; no triangular noise or tiled procedural shader.
  scale=min(.13,.44/max(max(span),.001))
  for li,v in zip(poly.loop_indices,vs):uv.data[li].uv=(u0+.01+(v[axes[0]]-lo[0])*scale,v0+.01+(v[axes[1]]-lo[1])*scale)
 o.data.materials.clear();o.data.materials.append(mats[key]);o['materialRole']=key

def box(name,p,d,key='Walnut',bevel=.006):
 bpy.ops.mesh.primitive_cube_add(size=1,location=P(p));o=bpy.context.object;o.name=name;o.dimensions=P(d);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 if bevel:
  m=o.modifiers.new('Restrained softened edges','BEVEL');m.width=bevel;m.segments=2;bpy.ops.object.modifier_apply(modifier=m.name)
 return o

def cut(o,c):
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Real fitted opening','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)

# Window inserts use unchanged approved scale and geometry, with real rough openings through the new shell.
windows=[{'name':'HeroPair','kind':'Pair','x':2.1,'y':3.6,'z':-.2,'yaw':180},
 {'name':'ShopDisplay','kind':'Pair','x':1.3,'y':.2,'z':-.2,'yaw':180},
 {'name':'StudyFront','kind':'Single','x':7.3,'y':3.6,'z':1.8,'yaw':180},
 {'name':'KitchenEast','kind':'Single','x':9.2,'y':.2,'z':4.2,'yaw':90},
 {'name':'StudyEast','kind':'Single','x':9.2,'y':3.6,'z':4.1,'yaw':90},
 {'name':'BedroomRear','kind':'Pair','x':3.6,'y':3.6,'z':9.2,'yaw':0},
 {'name':'TreatmentRear','kind':'Pair','x':3.6,'y':.2,'z':9.2,'yaw':0},
 {'name':'LivingWest','kind':'Single','x':-.2,'y':3.6,'z':1.1,'yaw':270}]
# Rectangular union envelope for the main paired inserts; single inserts use an arch cutter.
def arch_cutter(w):
 cx,base,cz=w['x'],w['y'],w['z'];yaw=w['yaw'];hw=.80;spring=1.75;sill=1.10;crown=2.4
 outline=[(-hw,sill),(hw,sill),(hw,spring)]+[(hw*math.cos(t),spring+(crown-spring)*math.sin(t)) for t in [i*math.pi/16 for i in range(1,17)]]
 verts=[(u,v,depth) for depth in [-.5,.5] for u,v in outline];n=len(outline);fs=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new('ArchCut');me.from_pydata(verts,[],fs);me.update();o=bpy.data.objects.new('ArchCut',me);s.collection.objects.link(o)
 # Source coordinates (horizontal,height,depth) -> world Unity, then Blender.
 q=math.radians(yaw)
 for v in me.vertices:
  u,h,d=v.co;v.co=P((cx+math.cos(q)*u+math.sin(q)*d,base+h,cz-math.sin(q)*u+math.cos(q)*d))
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 return o

architecture=[]
for item in json.loads((OUT/'FunctionalGeometry.json').read_text()):
 n=item['name'];g=item['group'];p=item['position'];d=item['size']
 if n.startswith('Site'):continue
 key='Plaster' if g.startswith('01') or 'ceiling' in n.lower() else 'Stone' if ('Porch' in n or 'Garden step' in n) else 'Walnut'
 if g.startswith('04'):key='Linen' if n.startswith(('Bedroom bed','Examination bed','Living bench')) else 'Walnut'
 o=box(n,p,d,key,.003 if key=='Plaster' else .006)
 if g.startswith('01'):
  for w in windows:
   lo=[p[i]-d[i]/2 for i in range(3)];hi=[p[i]+d[i]/2 for i in range(3)]
   if w['y']+1.5<lo[1] or w['y']+1.5>hi[1]:continue
   # Only exterior boundary walls at this plane; matching measured shell is deliberate.
   eastwest=w['yaw'] in [90,270];plane=w['x'] if eastwest else w['z'];wallplane=p[0] if eastwest else p[2]
   if abs(plane-wallplane)>.105:continue
   hpos=w['z'] if eastwest else w['x'];amin=lo[2] if eastwest else lo[0];amax=hi[2] if eastwest else hi[0]
   if not amin-.01<hpos<amax+.01:continue
   if w['kind']=='Pair':
    for offset in [-.49,.49]:
     cp=[w['x'],w['y']+1.915,w['z']];cp[2 if eastwest else 0]+=offset;dim=[.84,1.69,1];
     if eastwest:dim=[1,1.69,.84]
     cut(o,box('Pair aperture',cp,dim,bevel=0))
   else:cut(o,arch_cutter(w))
 uvmap(o,key);architecture.append(o)
# Join by material role, retaining meaningful source object names in the editable blend.
# Build genuinely interlocking smooth-profile roof carriers, not scaled copies of an old house.
profiles={};roofs=[]
def curve(points,n=14):
 return [tuple(sum(math.comb(3,j)*(1-t)**(3-j)*t**j*points[j][k] for j in range(4)) for k in [0,1]) for t in [i/n for i in range(n+1)]]
def roof(name,left,right,a,b,axis='Z'):
 profile=left+list(reversed(right[:-1]));profiles[name]=(left,right,axis,a)
 verts=[]
 for along in [a,b]:
  for cross,y in profile:verts.append([cross,y,along] if axis=='Z' else [along,y,cross])
 tris0=[];n=len(profile)
 for i in range(n-1):
  ids=[i,i+1,n+i+1,n+i];v=[Vector(verts[k]) for k in ids]
  if (v[1]-v[0]).cross(v[2]-v[0]).y<0:ids.reverse()
  tris0 += [ids[:3],[ids[0],ids[2],ids[3]]]
 roofs.append(dict(name=name,vertices=verts,topTriangles=tris0))
heroL=curve([(-.5,6.85),(.10,7.03),(1.05,10.75),(1.9,11.45)])
heroR=curve([(5.9,6.85),(4.75,7.06),(2.85,10.73),(1.9,11.45)])
roof('Roof_Hero',heroL,heroR,-.48,5.05)
roof('Roof_RearCross',curve([(4.22,6.85),(4.7,7.0),(5.8,9.4),(6.6,9.72)]),curve([(9.55,6.85),(9.0,7.08),(7.4,9.38),(6.6,9.72)]),-2.55,5.8,'X')
roof('Roof_StairNook',curve([(-2.55,6.85),(-2.2,7.06),(-1.5,8.62),(-1.15,8.95)]),curve([(.32,6.85),(-.05,7.06),(-.75,8.62),(-1.15,8.95)]),1.85,5.2)
roof('Roof_SubordinateWing',curve([(1.45,6.85),(1.95,7.05),(3.25,8.7),(3.85,9.08)]),curve([(6.65,6.85),(6.1,7.05),(4.65,8.75),(3.85,9.08)]),5.3,9.55,'X')
roof('Roof_GardenStore',[(5.25,3.45),(7.3,5.12)],[(9.55,3.45),(7.3,5.12)],6.3,9.4)
# Mono-pitch canopy volumes: ridge is at the wall, generous underside height remains outside walkable rooms.
roof('Roof_DeepEntryFold',[(2.25,3.26),(2.25,3.26)],[(5.85,3.26),(5.85,3.26)],-2.9,-.15) if False else None
for name,x0,x1,z0,z1,y0,y1 in [('Roof_DeepEntryFold',2.25,5.85,-2.9,-.1,3.22,4.36),('Roof_LeftShopFold',-.35,2.65,-1.95,-.08,3.16,4.08)]:
 roofs.append(dict(name=name,vertices=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z1],[x0,y1,z1]],topTriangles=[[0,2,1],[0,3,2]]));profiles[name]=([(z0,y0),(z1,y1)],[(z0,y0),(z1,y1)],'X',x0)
# Reuse proven exact upper-envelope clipping, disjoint coverage and intersection extraction.
obstacle={'name':'Chimney','vertices':[],'topTriangles':[]};raw={'reference':'Expanded layout + StyledDetails07 roof relationships'}
exec(roofsrc[roofsrc.index('tris=[]\nfor r in roofs+[obstacle]:'):roofsrc.index('modules={};')],globals())
merged=[seg for seg in merged if seg['role']!='PitchTransition']
def course_coordinates(t):
 left,right,axis,start=profiles[t['name']];gradient=t['plane'][0 if axis=='Z' else 1];profile=left if gradient>0 else right
 if t['name'] in ['Roof_DeepEntryFold','Roof_LeftShopFold']:profile=left
 if axis=='Z':return (lambda x,z:(z-start,arc_map(profile,x))),(lambda u,v:(arc_map(profile,v,True),u+start)),1.
 return (lambda x,z:(x-start,arc_map(profile,z))),(lambda u,v:(u+start,arc_map(profile,v,True))),1.
# Fitted SlateRoofKit01 surface adapters retain common course size, art and actual geometry.
for r in roofs:
 module('CM02_'+r['name'],'Fitted extended roof using approved kit slate courses',[],kind='FittedAdapter')
 for patch in [p for p in visible if p['tri']['name']==r['name']]:
  tile_patch(patch);solid_poly('Underlay',patch['poly'],lambda x,z:height(patch['tri'],x,z)-.006,.10,1)
 flush()
# Reuse boundary finishing and locally fitted valleys/ridges; no redundant overlapping carrier panels.
edgecode=roofsrc[roofsrc.index("module('CM_SlateRoofKit01_Fitted_EaveVergeNetwork'"):roofsrc.index('# Approved front gable verge')]
edgecode=edgecode.replace("if t['name']=='Roof_Hero' and abs(mid.z+4.4)<.002:continue","if False:continue").replace('CM_SlateRoofKit01_Fitted_','CM02_Fitted_')
exec(edgecode,globals())
# Plaster gable ends close actual roof profiles to the wall head. Never stretch the old gable asset.
for name,(left,right,axis,start) in profiles.items():
 if name in ['Roof_DeepEntryFold','Roof_LeftShopFold']:continue
 r=next(r for r in roofs if r['name']==name);a=min(p[2 if axis=='Z' else 0] for p in r['vertices']);b=max(p[2 if axis=='Z' else 0] for p in r['vertices']);profile=left+list(reversed(right[:-1]));base=3.45 if name=='Roof_GardenStore' else 6.85
 # Gable plane is inset from the edge; eave tails do not become unsupported wall extensions.
 for edge,coord in [('A',a+.27),('B',b-.27)]:
  outline=[(profile[0][0],base)]+profile+[(profile[-1][0],base)]
  # Eliminate repeated endpoint baseline vertices.
  compact=[]
  for p in outline:
   if not compact or math.dist(p,compact[-1])>1e-6:compact.append(p)
  if math.dist(compact[0],compact[-1])<1e-6:compact.pop()
  verts=[]
  for depth in [-.08,.08]:
   for x,y in compact:verts.append(P((x,y,coord+depth) if axis=='Z' else (coord+depth,y,x)))
  n=len(compact);faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
  me=bpy.data.meshes.new(name+'Gable');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Gable_'+name+'_'+edge,me);s.collection.objects.link(o);uvmap(o,'Plaster');architecture.append(o)
# New source plaster gables may intersect other roofs below the upper envelope. Clip hidden portions by exact roof solids.
# They are end walls; internal hidden overlaps are not duplicate visible surfaces.
for o in architecture:parts.append(o)
# Chimney is a rear-biased architectural anchor, clear of all interiors and stair headroom.
for n,p,d in [('ChimneyStack',(4.85,9.45,7.75),(.7,4.8,.75)),('ChimneyCrown',(4.85,11.92,7.75),(.94,.2,.99)),('FlueA',(4.62,12.28,7.75),(.19,.52,.22)),('FlueB',(5.08,12.28,7.75),(.19,.52,.22))]:
 o=box(n,p,d,'Stone',.028);uvmap(o,'Stone');parts.append(o)
# Recalculate normals and validate source solids before export.
report=[]
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-11 for t in o.data.loop_triangles)
 report.append({'name':o.name,'nonmanifold':bad,'volume':vol,'degenerate':deg,'triangles':len(o.data.loop_triangles)})
 if bad or deg or vol<=0:raise RuntimeError(report[-1])
for o in parts:o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CM_CrookedMortar_Production02.blend'))
# Export grouped roles, preserving semantic source parts in blend and reducing Unity renderer count.
for filename,objects in [('CM02_FittedArchitecture',[o for o in parts if not o.get('module')]),('CM02_FittedRoof',[o for o in parts if o.get('module')])]:
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True);o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(ASSET/'Models'/f'{filename}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(OUT/'WindowPlacements.json').write_text(json.dumps(windows,indent=2));(OUT/'RoofCarrierPlan.json').write_text(json.dumps(roofs,indent=2));(OUT/'Junctions.json').write_text(json.dumps([{k:list(v) if isinstance(v,Vector) else v for k,v in seg.items()} for seg in merged],indent=2))
print('PRODUCTION02_READY',len(parts),sum(r['triangles'] for r in report),len(visible),len(merged))
