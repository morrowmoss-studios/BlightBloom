"""Rough ElderCottage01: compact half-hip home, maintained stoop and lower service addition.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
if (H/'BW_ElderCottage01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Shingle','Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Textures/BW_Inn01_Shingle_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('index=0):','index=0,height=3.0):').replace('[0,3.12]','[0,height]');exec(compile(code,str(H/'wall_helpers.py'),'exec'))



# 5.8 x 8m main house and 1.6 x 5m lower west service addition.
wall('Maintained front',-2.4,3.4,4.5,[(-.7,.7,0,2.4),(-2.0,-1.15,1.2,2.2),(1.4,2.7,1.15,2.25)],index=0)
wall('Main rear',-2.4,3.4,-3.5,[(-.6,.5,1.2,2.2)],index=1)
wall('East home wall',-3.5,4.5,3.4,[(-1.1,.1,1.2,2.2)],True,2)
wall('West return',-3.5,4.5,-2.4,[],True,3)
wall('Service front',-4,-2.4,3.2,[],index=0,height=2.45)
wall('Service rear door',-4,-2.4,-1.8,[(-3.85,-2.55,0,2.3)],index=1,height=2.45)
wall('Service side',-1.8,3.2,-4,[(.65,1.35,1.2,1.95)],True,2,height=2.45)
for x,z,h in [(-2.4,4.5,3),(3.4,4.5,3),(-2.4,-3.5,3),(3.4,-3.5,3),(.7,-3.5,3),(-4,3.2,2.5),(-4,-1.8,2.5)]:native('wooden_post_column_size1.079','Bearing timber',lambda v,x=x,z=z,h=h:(x+v.x*.75,v.y*h/3.4059584,z+v.z*.75),'Timber')
for x in [-2.4,3.4]:box('Eave wall plate',(x,2.94,.5),(.25,.22,8.2),'wood2','Timber',.004)
for z in [-3.5,4.5]:box('Gable tie',(.5,2.94,z),(6.02,.22,.30),'wood2','Timber',.004)
for x,zs in [(-2.4,[(-3.5,-1.8),(3.2,4.5)]),(3.4,[(-3.5,4.5)]),(-4,[(-1.8,3.2)])]:
 for a,b in zs:box('Side sill',(x,.13,(a+b)/2),(.26,.18,b-a),'wood2','Timber',.003)
for z,spans in [(4.5,[(-2.4,-.71),(.71,3.4)]),(-3.5,[(-2.4,3.4)]),(3.2,[(-4,-2.4)])]:
 for a,b in spans:box('Ground sill',((a+b)/2,.13,z),(b-a,.18,.28),'wood2','Timber',.003)
def profile(name,poly,z,role='Plaster',group='Plaster'):
 V=[(x,y,zz) for zz in [z-.11,z+.11] for x,y in poly];n=len(poly);F=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];UV=[((x+4.2)/8.6,y/6) for x,y,zz in V];return create(name,V,F,UV,[role],[0]*len(F),group,True)
for z in [-3.5,4.5]:profile('Clipped gable infill',[(-2.4,3),(3.4,3),(3.4,3.35),(1.55,4.86),(-.55,4.86),(-2.4,3.35)],z)
for z in [-1.8,3.2]:profile('Addition sloped infill',[(-4,2.45),(-2.4,2.45),(-2.4,2.99),(-4,2.51)],z)
for name,cx,z,w,height in [('MainDoor',0,4.56,1.4,2.4),('ServiceDoor',-3.2,-1.86,1.3,2.3)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box('Door jamb',(x,height/2,z),(.15,height,.27),'wood2','Timber',.004)
 box('Door lintel',(cx,height+.10,z),(w+.4,.20,.29),'wood2','Timber',.004)
 native('wall_wood_door1.004',name,lambda v,cx=cx,z=z,w=w,height=height:(cx+(v.x-.38014054)/.685009*(w-.016),.018+v.y/1.83421123*(height-.03),z+(-.12 if z>0 else .12)+v.z),name)
def light(c,w,h,side=False):
 x,y,z=c;box('Small home glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box('Window jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box('Window rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box('Window mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.002)
 box('Projecting sill',(x,y-h/2-.07,z),(.30,.10,w+.35) if side else (w+.35,.10,.30),'wood3','Windows',.004)


for c,w,h,side in [((-1.575,1.7,4.57),.85,1,False),((2.05,1.7,4.57),1.3,1.1,False),((-.05,1.7,-3.57),1.1,1,False),((3.47,1.7,-.5),1.2,1,True),((-4.07,1.575,1),.7,.75,True)]:light(c,w,h,side)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)


for z,spans in [(4.5,[(-2.4,-.71),(.71,3.4)]),(-3.5,[(-2.4,3.4)]),(3.2,[(-4,-2.4)]),(-1.8,[(-4,-3.86),(-2.54,-2.4)])]:
 for a,b in spans:stone('Stone plinth',((a+b)/2,-.07,z),(b-a,.38,.35))
for x,a,b in [(-2.4,-3.5,4.5),(3.4,-3.5,4.5),(-4,-1.8,3.2)]:stone('Side plinth',(x,-.07,(a+b)/2),(.35,.38,b-a))
stone('Main stone stoop',(0,-.075,5.1),(2.35,.15,1.2),'Steps');stone('Main threshold',(0,-.015,4.6),(1.45,.12,.45),'Steps');stone('Service step',(-3.2,-.035,-2.02),(1.42,.17,.6),'Steps')
# Small supported entry roof, no surrounding props.
for x in [-1.08,1.08]:native('wooden_post_column_size1.079','Entry bearing',lambda v,x=x:(x+v.x*.55,v.y*2.55/3.4059584,5.58+v.z*.55),'PorchTimber');stone('Porch pad',(x,-.04,5.58),(.28,.24,.28))
box('Porch ledger',(0,2.83,4.52),(2.55,.18,.20),'wood2','PorchTimber',.003);box('Porch bearing',(0,2.52,5.58),(2.55,.18,.20),'wood2','PorchTimber',.003)
native('chimney_outside_size1.001','Long-used hearth',lambda v:(1.65+v.x*.54,v.y*.96,-1.25+v.z*.54),'Chimney')
# Roof patch/deck and 8-cell painted shingle atlas reuse Inn01's restrained palette.
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
# Half-hipped main roof. Clipped ends, rather than a full cottage gable or tall pyramid.
for side in [-1,1]:
 end=.5+side*3.35
 clips=[lambda p,side=side:3.8+(side*(p.x-.5))/1.05*1.1-p.z,lambda p,side=side:p.z+2.8+(side*(p.x-.5))/1.05*1.1]
 patch('Main half hip',[(.5,5.85,-3.9),(.5,5.85,4.9),(end,3.10,4.9),(end,3.10,-3.9)],10,27,clips)
# Small end hips have a broad lower edge and a narrow ridge meeting.
for front in [True,False]:
 ztip=3.8 if front else -2.8;zbase=4.9 if front else -3.9
 # Rectangular plane clipped to a triangle, with the same layered shingles.
 patch('Clipped end roof',[(-.55,5.85,ztip),(1.55,5.85,ztip),(1.55,4.988,zbase),(-.55,4.988,zbase)],4,7,[lambda p,ztip=ztip,zbase=zbase:1.05*(p.z-ztip)/(zbase-ztip)-(p.x-.5),lambda p,ztip=ztip,zbase=zbase:1.05*(p.z-ztip)/(zbase-ztip)+(p.x-.5)])
patch('Lower service roof',[(-2.3,3.10,-2.05),(-2.3,3.10,3.45),(-4.3,2.49,3.45),(-4.3,2.49,-2.05)],5,17)
patch('Sheltered stoop', [(-1.3,2.96,4.4),(1.3,2.96,4.4),(1.3,2.65,5.82),(-1.3,2.65,5.82)],4,8)
# Ridge cap only; no decorative trusswork.
for side in [-1,1]:
 V=[(.5,5.92,-2.82),(.5,5.92,3.82),(.5+side*.15,5.80,3.82),(.5+side*.15,5.80,-2.82)];create('Ridge cover',V,[(0,1,2,3)],[(.03,.03),(.22,.03),(.22,.42),(.03,.42)],['Shingle'],[0],'Shingles')
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_ElderCottage01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/ElderCottage01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'mainBody':[5.8,8.0],'addition':[1.6,5.0],'floorDatum':FLOOR,'mainDoor':[1.4,2.4],'serviceDoor':[1.3,2.3],'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_ElderCottage01.blend'));print('ELDER_READY',sum(row['triangles'] for row in cat))
