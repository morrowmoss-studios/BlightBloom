"""Inn01: two-storey main hall, recessed lower guest/service wing and sheltered entry.
Only project-owned outputs; existing village assets and native helpers are read-only.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4]
if (H/'BW_Inn01.blend').exists():raise RuntimeError('Existing inn candidate; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.88;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Shingle','Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Textures/BW_Inn01_Shingle_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path));n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
m=bpy.data.materials.new('DullMetal');m.diffuse_color=(.16,.15,.13,1);mats['DullMetal']=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
# Continuous wall surfaces and real reveals; no pseudo-infill panel seams.
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace('index=0):','index=0,height=6.0):').replace('[0,3.12]','[0,height]').replace("['Plaster02']","['Plaster']").replace('/5.7','/8.6');exec(compile(code,str(H/'wall_helpers.py'),'exec'))
# Main room allows common room below and three modest guest spaces above (interior not built).
wall('Main frontage',-4.5,1.2,7.5,[(-.75,.75,0,2.5),(-3.85,-2.35,1.1,2.3),(-3.75,-2.55,4.05,5.35),(-.70,.50,4.05,5.35)],index=0)
wall('Main rear',-4.5,1.2,-1.7,[(-3.55,-2.15,1.2,2.3),(-2.9,-1.7,4.1,5.35)],index=1)
wall('Main west',-1.7,7.5,-4.5,[(.3,1.7,1.2,2.3),(.05,1.15,4.1,5.4),(4.65,5.85,4.1,5.4)],True,2,height=6.17)
wall('Main east setback return',6.4,7.5,1.2,[],True,3)
wall('Recessed wing frontage',1.2,5.0,6.4,[(2.5,3.9,1.2,2.3),(2.65,3.85,3.95,5.15)],index=3,height=5.45)
wall('Wing rear service',1.2,5.0,-1.7,[(2.55,3.85,0,2.3),(2.65,3.75,3.95,5.15)],index=1,height=5.45)
wall('Wing east',-1.7,6.4,5.0,[(.4,1.6,1.2,2.3),(4.2,5.3,3.95,5.2)],True,2,height=5.68)
# Gable ends follow the roof profile without decorative applied members.
mainProfile=[(-4.85,5.95),(-1.8,8.5),(1.2,6.05)];wingProfile=[(1.2,6.05),(3.2,7.25),(5.35,5.45)]
def gable(name,pts,z,index):
 V=[(x,y,z+d) for d in [-.11,.11] for x,y in pts];n=len(pts);F=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];UV=[((index%2+.05+.9*(x+4.5)/9.5)/2,(index//2+.05+.9*y/8.6)/2) for x,y,z0 in V];create(name,V,F,UV,['Plaster'],[0]*len(F),'Plaster',True)
for z,index in [(7.5,0),(-1.7,1)]:gable('Main gable',[(-4.5,6),(1.2,6),(-1.8,8.44),(-4.5,6.18)],z,index)
for z,index in [(6.4,3),(-1.7,1)]:gable('Wing gable',[(1.2,5.45),(5,5.45),(5,5.68),(3.2,7.19),(1.2,5.99)],z,index)
# Story posts remain at real storey scale and seat into continuous floor/plate beams.
posts=[(-4.5,-1.7),(-4.5,7.5),(1.2,7.5),(-1.8,7.5),(-1.25,-1.7),(-4.5,2.9),(5,-1.7),(5,6.4),(1.2,6.4),(5,2.9)]
for x,z in posts:
 top=5.68 if x>4 else 6.0
 for low,h in [(0,3.1),(3.1,top-3.1)]:native('wooden_post_column_size1.079','Story bearing post',lambda v,x=x,z=z,low=low,h=h:(x+v.x*.78,low+v.y*h/3.4059584,z+v.z*.78),'Timber')
for y in [.16,3.08,5.90]:
 for z in [-1.7,7.5]:box('Main floor/plate beam',(-1.65,y,z),(5.85,.20,.24),'wood2','Timber',.004)
 box('Main west floor/plate',(-4.5,y,2.9),(.24,.20,9.4),'wood2','Timber',.004)
for y in [.16,3.08,5.36]:
 for z in [-1.7,6.4]:box('Wing floor/plate',(3.1,y,z),(3.94,.20,.24),'wood2','Timber',.004)
 box('Wing east floor/plate',(5,y,2.35),(.24,.20,8.3),'wood2','Timber',.004)
# Frames are modest mullioned lights, not elaborate merchant-house bays.
def light(name,c,w,h,side=False):
 x,y,z=c;box(name+' glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box(name+' jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.004)
 for v in [-h/2,h/2]:box(name+' rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.004)
 box(name+' mullion',c,(.08,h,.055) if side else (.055,h,.08),'wood2','Windows',.002)
 box(name+' transom',(x,y+.05,z),(.08,.05,w) if side else (w,.05,.08),'wood2','Windows',.001)
 box(name+' sill',(x,y-h/2-.09,z),(.32,.12,w+.30) if side else (w+.30,.12,.32),'wood2','Windows',.005)
for c,w,h in [((-3.1,1.7,7.52),1.5,1.2),((-3.15,4.7,7.52),1.2,1.3),((-.1,4.7,7.52),1.2,1.3),((3.2,1.75,6.42),1.4,1.1),((3.25,4.55,6.42),1.2,1.2),((-2.85,1.75,-1.72),1.4,1.1),((-2.3,4.725,-1.72),1.2,1.25),((3.2,4.55,-1.72),1.1,1.2)]:light('Modest front/rear casement',c,w,h)
for c,w,h in [((-4.52,1.75,1),1.4,1.1),((-4.52,4.75,.6),1.1,1.3),((-4.52,4.75,5.25),1.2,1.3),((5.02,1.75,1),1.2,1.1),((5.02,4.575,4.75),1.1,1.25)]:light('Side casement',c,w,h,True)
# Clear static architectural doors; no tavern interaction or interior system.
for name,cx,z,w,h,base in [('MainDoor',0,7.43,1.5,2.5,.055),('ServiceDoor',3.2,-1.63,1.3,2.3,.02)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box('Door jamb',(x,h/2,z),(.15,h,.26),'wood2','Timber',.005)
 box('Door lintel',(cx,h+.105,z),(w+.44,.21,.29),'wood2','Timber',.005)
 native('wall_wood_door1.004',name,lambda v,cx=cx,z=z,w=w,h=h,base=base:(cx+(v.x-.38014054)/.685009*(w-.016),base+v.y/1.83421123*(h-base-.015),z+v.z),name)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)
for z in [-1.7,7.5]:
 intervals=[(-4.5,1.2)] if z<0 else [(-4.5,-.76),(.76,1.2)]
 for a,b in intervals:stone('Main stone footing',((a+b)/2,-.11,z),(b-a,.38,.28))
stone('West footing',(-4.5,-.11,2.9),(.28,.38,9.2));stone('Setback return footing',(1.2,-.11,6.95),(.28,.38,1.1))
for z in [-1.7,6.4]:
 for a,b in ([(1.2,2.54),(3.86,5)] if z<0 else [(1.2,5)]):stone('Wing stone footing',((a+b)/2,-.11,z),(b-a,.38,.28))
stone('East footing',(5,-.11,2.35),(.28,.38,8.1));stone('Service threshold',(3.2,-.015,-1.76),(1.3,.07,.48),'EntranceStone')
stone('Porch standing surface',(0,-.015,8.25),(3.0,.13,1.5),'EntranceStone');stone('Main sill',(0,.025,7.56),(1.5,.07,.42),'EntranceStone')
# Porch posts support a small gabled shelter; no applied ornamental gable truss.
for x in [-1.35,1.35]:native('wooden_post_column_size1.079','Porch bearing',lambda v,x=x:(x+v.x*.66,v.y*2.82/3.4059584,8.6+v.z*.66),'PorchTimber')
box('Porch front bearing',(0,2.76,8.6),(2.98,.18,.20),'wood2','PorchTimber',.004)
for x in [-1.4,1.4]:box('Porch side plate',(x,2.8,8.05),(.17,.17,1.65),'wood2','PorchTimber',.004)
# Plain timber sign arm and its supporting strut, without board, lettering or graphic.
box('Sign wall mount',(1.03,2.55,7.64),(.13,.65,.15),'wood2','SignBracket',.003);box('Sign arm',(1.03,2.78,8.0),(.13,.13,.85),'wood2','SignBracket',.003)
a=Vector((1.03,2.40,7.67));b=Vector((1.03,2.72,8.27));delta=b-a;u=Vector((.045,0,0));v=delta.cross(u).normalized()*.045;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Sign arm strut',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.03,j//4*delta.length,.09,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'SignBracket',True,.003)
# Hearth chimney stays wholly within the service wing below the roof.
native('chimney_outside_size1.001','Integrated hearth and flue',lambda v:(3.35+v.x*.8,v.y*1.29,-.4+v.z*.8),'Chimney')
# Use the proven clipping helper for an exact hidden penetration inside the masonry footprint.
rect=(2.96,3.72,-.32,.15);lib=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();exec(compile(lib[lib.index('def clip('):lib.index('RV=[];RF=[];RU=[]')],str(H/'roof_helpers.py'),'exec'))
RV=[];RF=[];RU=[];DV=[];DF=[];DU=[]
def addface(V,UV,target='roof'):
 for poly in outside(list(zip(map(Vector,V),map(Vector,UV)))):
  vs,fs,us=(RV,RF,RU) if target=='roof' else (DV,DF,DU);k=len(vs);vs.extend(tuple(p) for p,u in poly);us.extend(tuple(u) for p,u in poly);fs.append(tuple(range(k,len(vs))))
def roofstrip(name,x0,y0,x1,y1,z0,z1,cols,rows):
 def point(t,z):
  x=x0+(x1-x0)*t;y=y0+(y1-y0)*t+.014*math.sin(z*.72)+.008*math.sin(x*1.8+z*.7);return Vector((x,y,z))
 corners=[point(0,z0),point(0,z1),point(1,z1),point(1,z0)]
 for shift in [0,-.11]:addface([p+Vector((0,shift,0)) for p in corners],[(0,0),(1,0),(1,1),(0,1)],'deck')
 for a,b in zip(corners,corners[1:]+corners[:1]):addface([a,b,b-Vector((0,.11,0)),a-Vector((0,.11,0))],[(0,0),(1,0),(1,1),(0,1)],'deck')
 for row in range(rows):
  for col in range(cols):
   offset=.025*math.sin(col*1.7+row*.91);t0=max(0,(row-.22)/rows)+(offset/abs(x1-x0) if row else 0);t1=(row+1)/rows+(offset/abs(x1-x0) if row<rows-1 else 0);zz0=z0+(z1-z0)*col/cols;zz1=z0+(z1-z0)*(col+1)/cols;idx=(col*3+row*5+(2 if name=='wing' else 0))%8
   vs=[];uv=[]
   for t,tt in [(t0,0),(t1,1)]:
    for j in range(3):
     u=j/2;z=zz0+(zz1-zz0)*u;p=point(t,z);p.y+=.018+(rows-row)*.0025+.022*tt*tt+.005*math.sin(u*math.pi);vs.append(p);uv.append(((idx%4+.08+.84*u)/4,(idx//4+.06+.88*tt)/2))
   for j in range(2):
    ids=[j,j+1,4+j,3+j];addface([vs[i] for i in ids],[uv[i] for i in ids]);ids=[3+j,4+j];top=[vs[i] for i in ids];addface(top+[p-Vector((0,.012,0)) for p in top[::-1]],[uv[i] for i in ids]+[(uv[i][0],uv[i][1]-.008) for i in ids[::-1]])
 # Edge framing tracks the real sloping profile, with no internal triangular ornaments.
 for z in [z0+.04,z1-.04]:
  a=Vector((x0,y0-.08,z));b=Vector((x1,y1-.08,z));delta=b-a;u=Vector((delta.y,-delta.x,0)).normalized()*.06;v=Vector((0,0,.075));VV=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Fitted structural verge',VV,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.04,j//4*delta.length,.13,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'RoofTrim',True,.003)
roofstrip('main',-1.8,8.5,-4.85,5.95,-2.15,7.95,34,12);roofstrip('main',-1.8,8.5,1.14,6.10,-2.15,7.95,34,12)
roofstrip('wing',3.2,7.25,1.26,6.10,-2.15,6.8,30,8);roofstrip('wing',3.2,7.25,5.35,5.45,-2.15,6.8,30,9)
roofstrip('porch',0,3.65,-1.55,2.8,7.30,8.95,6,6);roofstrip('porch',0,3.65,1.55,2.8,7.30,8.95,6,6)
# Split timber ridge covers are quiet, useful weather protection.
for x,y,z0,z1 in [(-1.8,8.55,-2.17,7.97),(3.2,7.30,-2.17,6.82),(0,3.70,7.29,8.97)]:
 for side in [-1,1]:
  VV=[(x,y+.035,z0),(x,y+.035,z1),(x+side*.16,y-.06,z1),(x+side*.16,y-.06,z0)];addface(VV,[(0,0),(0,1),(1,1),(1,0)])
create('Irregular laid wooden shingles',RV,RF,RU,['Shingle'],[0]*len(RF),'Shingles');create('Continuous roof deck',DV,DF,DU,['interior_roof'],[0]*len(DF),'RoofDeck')
# Modest open valley gutter seats within both meeting roof edges.
VV=[(1.10,6.14,-2.15),(1.2,6.055,-2.15),(1.30,6.14,-2.15),(1.10,6.14,6.8),(1.2,6.055,6.8),(1.30,6.14,6.8)];create('Roof valley weathering',VV,[(0,1,4,3),(1,2,5,4)],[(0,0),(.5,0),(1,0),(0,1),(.5,1),(1,1)],['DullMetal'],[0,0],'RoofValley')
# Export only new Inn01 groups. No native package or approved asset is overwritten.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Inn01_'+group;o.data.name=o.name;bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.normal_update()
 if group in ['Shingles','RoofValley']:bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<-.01])
 # Deck is a collision envelope: duplicate underside is retained, top normals face up.
 if group=='RoofDeck':
  for f in bm.faces:
   if f.normal.z<-.1:bmesh.ops.reverse_faces(bm,faces=[f])
 bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'mainBody':[5.7,9.2],'wing':[3.8,8.1],'bodyArea':5.7*9.2+3.8*8.1,'floorRise':3.1,'mainDoor':[1.5,2.5],'serviceDoor':[1.3,2.3],'chimneyHole':rect,'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Inn01.blend'));print('INN_READY',sum(m['triangles'] for m in cat))
