"""Rough FamilyCottageB01: single-storey offset-ridge cottage with rear catslide and sheltered entry.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
if (H/'BW_FamilyCottageB01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Shingle','Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Textures/BW_Inn01_Shingle_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('index=0):','index=0,height=3.0):').replace('[0,3.12]','[0,height]');exec(compile(code,str(H/'wall_helpers.py'),'exec'))




# Compact single-story 6.8 x 7.2 m home; asymmetric roof carries a modest entry cover.
wall('Front home wall',-3.4,3.4,4,[(-.70, .70,0,2.4),(-2.55,-1.25,1.1,2.2),(1.9,2.7,1.3,2.15)],index=0,height=3.05)
wall('Rear working door',-3.4,3.4,-3.2,[(.95,2.25,0,2.2),(-2.35,-1.25,1.1,2.0)],index=1,height=2.5)
wall('West home wall',-3.2,4,-3.4,[(-.6,.5,1.1,2.1)],True,2,height=2.5)
wall('East home wall',-3.2,4,3.4,[(1.3,2.3,1.15,2.15)],True,3,height=2.5)
for x,z,height in [(-3.4,-3.2,2.5),(3.4,-3.2,2.5),(-3.4,4,3.05),(3.4,4,3.05),(-.9,4,3.05),(-.25,-3.2,2.5)]:native('wooden_post_column_size1.079','Bearing post',lambda v,x=x,z=z,h=height:(x+v.x*.75,v.y*h/3.4059584,z+v.z*.75),'Timber')
for z,y in [(4,2.95),(-3.2,2.4)]:box('Wall bearing plate',(0,y,z),(7.02,.22,.29),'wood2','Timber',.004)
for x in [-3.4,3.4]:box('Low side sill',(x,.13,.4),(.26,.18,7.2),'wood2','Timber',.003)
for z,spans in [(4,[(-3.4,-.71),(.71,3.4)]),(-3.2,[(-3.4,.94),(2.26,3.4)])]:
 for a,b in spans:box('Interrupted sill',((a+b)/2,.13,z),(b-a,.18,.29),'wood2','Timber',.003)
# Side infill follows the actual unequal roof pitches and closes wall-to-roof transitions.
for x in [-3.4,3.4]:
 poly=[(-3.2,2.5),(4,2.5),(4,3.61),(1.6,5.47),(-3.2,2.79)];n=len(poly);V=[(xx,y,z) for xx in [x-.11,x+.11] for z,y in poly];F=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];UV=[((z+3.65)/8.7,y/6) for xx,y,z in V];create('Catslide gable infill',V,F,UV,['Plaster'],[0]*len(F),'Plaster',True)
# Small front upper strip meets the roof underside; no decorative timber patterns.
box('Front upper closure',(0,3.32,4),(6.8,.55,.22),'Plaster','Plaster',0)
# Keep original road axis for main entry; service door faces rear.
for name,cx,z,w,height in [('MainDoor',0,4.06,1.4,2.4),('ServiceDoor',1.6,-3.26,1.3,2.2)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box('Entry jamb',(x,height/2,z),(.15,height,.27),'wood2','Timber',.004)
 box('Entry lintel',(cx,height+.10,z),(w+.42,.20,.29),'wood2','Timber',.004)
 native('wall_wood_door1.004',name,lambda v,cx=cx,z=z,w=w,height=height:(cx+(v.x-.38014054)/.685009*(w-.016),.018+v.y/1.83421123*(height-.03),z+(-.12 if z>0 else .12)+v.z),name)
def light(c,w,h,side=False):
 x,y,z=c;box('Small home glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box('Window jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box('Window rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box('Window mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.002)
 box('Projecting sill',(x,y-h/2-.07,z),(.30,.10,w+.35) if side else (w+.35,.10,.30),'wood3','Windows',.004)



for c,w,h,side in [((-1.9,1.65,4.07),1.3,1.1,False),((2.3,1.725,4.07),.8,.85,False),((-1.8,1.55,-3.27),1.1,.9,False),((-3.47,1.6,-.05),1.1,1,True),((3.47,1.65,1.8),1,1,True)]:light(c,w,h,side)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)



for z,spans in [(4,[(-3.4,-.71),(.71,3.4)]),(-3.2,[(-3.4,.94),(2.26,3.4)])]:
 for a,b in spans:stone('Foundation footing',((a+b)/2,-.07,z),(b-a,.38,.35))
for x in [-3.4,3.4]:stone('Side footing',(x,-.07,.4),(.35,.38,7.2))
stone('Sheltered entry stoop',(0,-.075,4.55),(2.35,.15,1.1),'Steps');stone('Front threshold',(0,-.015,4.08),(1.45,.12,.45),'Steps');stone('Service threshold',(1.6,-.035,-3.4),(1.45,.15,.6),'Steps')
# Posts support the modest extended front cover rather than a second decorative roof.
for x in [-1.08,1.08]:native('wooden_post_column_size1.079','Front cover post',lambda v,x=x:(x+v.x*.55,v.y*2.97/3.4059584,4.84+v.z*.55),'PorchTimber');stone('Post pad',(x,-.04,4.84),(.28,.24,.28))
box('Covered entry bearing',(0,2.88,4.84),(2.48,.20,.22),'wood2','PorchTimber',.003)
native('chimney_outside_size1.001','Integrated household hearth',lambda v:(-1.5+v.x*.52,v.y*.90,-.7+v.z*.52),'Chimney')
def patch(name,corners,rows,cols,clips=()):
 # Each patch is planar in x,z, with y carried by its four corners.
 A,B,C,D=map(Vector,corners)
 def pt(u,t):return A.lerp(B,u).lerp(D.lerp(C,u),t)
 def clip(poly,fn):
  out=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   fa,fb=fn(a[0]),fn(b[0]);ia,ib=fa>=0,fb>=0
   if ia:out.append(a)
   if ia!=ib:
    t=fa/(fa-fb);out.append((a[0].lerp(b[0],t),a[1].lerp(b[1],t)))
  return out
 def clipped(points,uv):
  poly=list(zip(points,map(Vector,uv)))
  for fn in clips:poly=clip(poly,fn)
  return poly
 deck=clipped([pt(0,0),pt(1,0),pt(1,1),pt(0,1)],[(0,0),(1,0),(1,1),(0,1)])
 if len(deck)>=3:
  V=[tuple(p-Vector((0,d,0))) for d in [.04,.17] for p,u in deck];n=len(deck);F=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];create(name+' deck',V,F,[tuple(u) for d in [0,1] for p,u in deck],['interior_roof'],[0]*len(F),'RoofDeck',True)
 V=[];F=[];UV=[]
 for row in range(rows):
  t0=max(0,(row-.18)/rows);t1=(row+1)/rows
  for col in range(cols):
   u0=col/cols;u1=(col+1)/cols;idx=(col*3+row*5)%8;uv=[((idx%4+.06+.88*u)/4,(idx//4+.06+.88*t)/2) for u,t in [(0,0),(1,0),(1,1),(0,1)]];points=[pt(u0,t0),pt(u1,t0),pt(u1,t1),pt(u0,t1)]
   for j,p in enumerate(points):p.y+=.012+(rows-row)*.002+.007*math.sin(col*1.7+row*.9)+(j//2)*.012
   poly=clipped(points,uv)
   if len(poly)<3:continue
   k=len(V);V.extend(tuple(p) for p,u in poly);UV.extend(tuple(u) for p,u in poly);F.append(tuple(range(k,len(V))))
   # Thin lower lips carry the overlap at gameplay distance.
   p0,u0v=poly[-2];p1,u1v=poly[-1];k=len(V);V.extend([tuple(p0),tuple(p1),tuple(p1-Vector((0,.013,0))),tuple(p0-Vector((0,.013,0)))]);UV.extend([tuple(u0v),tuple(u1v),tuple(u1v),tuple(u0v)]);F.append((k,k+1,k+2,k+3))
 o=create(name+' laid shingles',V,F,UV,['Shingle'],[0]*len(F),'Shingles');bm=bmesh.new();bm.from_mesh(o.data)
 for f in bm.faces:
  if f.normal.z<0:bmesh.ops.reverse_faces(bm,faces=[f])
 bm.to_mesh(o.data);bm.free()

# Main roof: short front pitch and longer sheltered rear catslide, no dormer or extra gable.
patch('Front pitch',[(-3.8,5.6,1.6),(3.8,5.6,1.6),(3.8,2.95,5.05),(-3.8,2.95,5.05)],10,24)
patch('Rear catslide',[(3.8,5.6,1.6),(-3.8,5.6,1.6),(-3.8,2.65,-3.65),(3.8,2.65,-3.65)],15,24)
for side in [-1,1]:
 V=[(-3.82,5.67,1.6),(3.82,5.67,1.6),(3.82,5.56,1.6+side*.15),(-3.82,5.56,1.6+side*.15)];create('Plain ridge cover',V,[(0,1,2,3)],[(.03,.03),(.22,.03),(.22,.42),(.03,.42)],['Shingle'],[0],'Shingles')
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_FamilyCottageB01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageB01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'bodyFootprint':[6.8,7.2],'floorDatum':FLOOR,'mainDoor':[1.4,2.4],'serviceDoor':[1.3,2.2],'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_FamilyCottageB01.blend'));print('COTTAGE_B_READY',sum(row['triangles'] for row in cat))
