"""Rough Merchant01: enclosed dry store, open serving recess and integrated shallow canopy.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.15
if (H/'BW_Merchant01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Thatch','Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures/BW_StableA03_Thatch_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('3.12','3.15');exec(compile(code,str(H/'wall_helpers.py'),'exec'))
wall('Shopfront',-3.4,3.4,5,[(-3.2,-.9,1.0,2.25),(.75,2.15,0,2.4),(2.45,3.15,1.4,2.25)],index=0)
wall('Storage rear',-3.4,3.4,-1.4,[(0,1.6,0,2.4),(-2.5,-1.9,2.25,2.8)],index=1)
wall('West storage wall',-1.4,5,-3.4,[],True,2);wall('East storage light',-1.4,5,3.4,[(.65,1.75,1.3,2.25)],True,3)
for x,z in [(-3.4,-1.4),(-3.4,5),(3.4,-1.4),(3.4,5),(.35,5),(-.8,-1.4)]:native('wooden_post_column_size1.079','Bearing post',lambda v,x=x,z=z:(x+v.x*.8,v.y*3.15/3.4059584,z+v.z*.8),'Timber')
for z in [-1.4,5]:box('Wall plate',(0,3.03,z),(6.98,.22,.23),'wood2','Timber',.004)
for x in [-3.4,3.4]:box('Side wall plate',(x,3.03,1.8),(.23,.22,6.6),'wood2','Timber',.004);box('Side sill',(x,.16,1.8),(.23,.18,6.4),'wood2','Timber',.004)
for z,intervals in [(5,[(-3.4,.74),(2.16,3.4)]),(-1.4,[(-3.4,-.01),(1.61,3.4)])]:
 for a,b in intervals:box('Interrupted ground sill',((a+b)/2,.16,z),(b-a,.18,.23),'wood2','Timber',.004)
# Shop hatch frame carries the shallow canopy and the counter.
for x in [-3.26,-.84]:box('Serving jamb',(x,1.65,5.04),(.12,1.5,.24),'wood2','Shopfront',.004)
box('Serving lintel',(-2.05,2.34,5.04),(2.60,.18,.25),'wood2','Shopfront',.005)
# Broad usable countertop made from three restrained fitted planks.
for j in range(3):box('Counter plank',(-2.05,.96,4.93+j*.215),(2.40,.08,.22),'wood3','Counter',.006)
for x in [-3.08,-1.02]:
 a=Vector((x,.62,5.06));b=Vector((x,.92,5.45));d=b-a;u=Vector((.045,0,0));v=d.cross(u).normalized()*.045;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Counter support',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.03,j//4*d.length,.09,d.length,'wood2') for j in range(8)],['wood2'],[0]*6,'Counter',True,.003)
# Empty shadowed service recess; no goods, inventory or complete shop interior.
box('Service recess rear',(-2.05,1.62,3.60),(2.42,1.40,.05),'wood3','ServingRecess',.002)
for x in [-3.22,-.88]:box('Service recess side',(x,1.62,4.30),(.05,1.40,1.4),'wood3','ServingRecess',.002)
box('Service recess ceiling',(-2.05,2.30,4.30),(2.4,.05,1.4),'wood3','ServingRecess',.002)
# Customer and delivery frames have generous true apertures; static leaves, no gameplay.
for name,cx,z,w in [('Customer',1.45,5.06,1.4),('Delivery',.8,-1.46,1.6)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box(name+' door jamb',(x,1.2,z),(.15,2.4,.26),'wood2','Timber',.004)
 box(name+' lintel',(cx,2.51,z),(w+.44,.22,.28),'wood2','Timber',.005)
native('wall_wood_door1.004','Customer closed leaf',lambda v:(1.45+(v.x-.38014054)/.685009*1.384,.02+v.y/1.83421123*2.36,4.94+v.z),'CustomerDoor')
for cx,mirror in [(.396,False),(1.204,True)]:native('wall_wood_door1.004','Delivery double leaf',lambda v,cx=cx,mirror=mirror:(cx+(v.x-.38014054)/.685009*.792*(-1 if mirror else 1),.02+v.y/1.83421123*2.36,-1.34+v.z),'DeliveryDoors',flip=mirror)
# Modest lights; no large glass retail frontage.
def light(c,w,h,side=False):
 x,y,z=c;box('Small glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box('Light jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box('Light rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box('Light mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.001)
light((2.8,1.825,5.06),.7,.85);light((3.46,1.775,1.2),1.1,.95,True)
# Rear storage vent, understated wooden louvers rather than another display window.
for i in range(5):box('Storage vent slat',(-2.2,2.29+i*.105,-1.45),(.62,.085,.08),'wood3','Windows',.001)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)
for z,intervals in [(5,[(-3.4,.74),(2.16,3.4)]),(-1.4,[(-3.4,-.01),(1.61,3.4)])]:
 for a,b in intervals:stone('Stone footings',((a+b)/2,-.1,z),(b-a,.36,.28))
for x in [-3.4,3.4]:stone('Side footings',(x,-.1,1.8),(.28,.36,6.4))
stone('Customer step',(1.45,-.025,5.18),(1.45,.09,.52),'ApproachStone');stone('Delivery step',(.8,-.025,-1.53),(1.65,.09,.52),'ApproachStone');stone('Selling apron',(-2.05,-.09,5.93),(2.9,.12,.8),'ApproachStone')
# Canopy posts are outside the serving opening and clear of the original path centre.
for x in [-3.45,-.65]:native('wooden_post_column_size1.079','Canopy bearing',lambda v,x=x:(x+v.x*.6,v.y*2.52/3.4059584,6.15+v.z*.6),'CanopyTimber');stone('Canopy pad',(x,-.09,6.15),(.30,.24,.30))
box('Front canopy bearing',(-2.05,2.47,6.15),(3.08,.18,.19),'wood2','CanopyTimber',.004)
box('Canopy wall ledger',(-2.05,2.76,4.99),(3.20,.18,.22),'wood2','CanopyTimber',.004)
# Actual plank canopy, shallow, no decorative valance or extra market structure.
for i in range(12):
 x=-3.64+(i+.5)*3.19/12;a=Vector((x,2.83,4.88));b=Vector((x,2.54,6.35));delta=b-a;u=Vector((.134,0,0));v=delta.cross(u).normalized()*.022;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Canopy weatherboard',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.08,j//4*delta.length,.27,delta.length,'wood3') for j in range(8)],['wood3'],[0]*6,'CanopyBoards',True,.003)
for x in [-3.45,-.65]:
 a=Vector((x,2.76,5.0));b=Vector((x,2.49,6.15));d=b-a;u=Vector((.05,0,0));v=d.cross(u).normalized()*.06;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Canopy rafter',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.035,j//4*d.length,.11,d.length,'wood2') for j in range(8)],['wood2'],[0]*6,'CanopyTimber',True,.003)
# Small supported sign bracket at the doorway, without name or graphic.
box('Sign fixing',(2.23,2.49,5.15),(.12,.5,.16),'wood2','SignBracket',.003);box('Sign arm',(2.23,2.70,5.52),(.12,.12,.85),'wood2','SignBracket',.003)
# Steep hipped thatch differs from the stable's broad low gable; each slope has continuous UVs.
V=[];F=[];UV=[];peak=6.5
patches=[((-.4,peak,1.8),(.4,peak,1.8),(3.75,2.95,5.35),(-3.75,2.95,5.35)),((.4,peak,1.8),(-.4,peak,1.8),(-3.75,2.95,-1.75),(3.75,2.95,-1.75)),((-.4,peak,1.8),(-.4,peak,1.8),(-3.75,2.95,5.35),(-3.75,2.95,-1.75)),((.4,peak,1.8),(.4,peak,1.8),(3.75,2.95,-1.75),(3.75,2.95,5.35))]
for patch in patches:
 A,B,C,D=map(Vector,patch);nx=18;ny=12;base=len(V)
 for layer in [0,1]:
  for j in range(ny+1):
   t=j/ny
   for i in range(nx+1):
    u=i/nx;p=A.lerp(B,u).lerp(D.lerp(C,u),t);p.y+=.012*math.sin(p.x*1.4+p.z*.9)+.009*math.sin(p.z*2)-layer*.22;p.x+=.012*math.sin(p.z*1.7);p.z+=.012*math.sin(p.x*1.2);V.append(tuple(p));UV.append((.03+.94*u,.03+.94*t))
 N=(nx+1)*(ny+1)
 for j in range(ny):
  for i in range(nx):
   k=base+j*(nx+1)+i;F.append((k,k+1,k+nx+2,k+nx+1));k+=N;F.append((k+nx+1,k+nx+2,k+1,k))
 # Only exterior eaves connect layers; hips/ridge share vertices with adjacent patches.
 for i in range(nx):
  k=base+ny*(nx+1)+i;F.append((k,k+N,k+N+1,k+1))
o=create('Hipped continuous thatch coat',V,F,UV,['Thatch'],[0]*len(F),'Thatch');bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
for p in o.data.polygons:p.use_smooth=True
# Plain thick ridge dressing; no shaggy exaggeration or botanical clutter.
V=[];UV=[];F=[]
for x in [-.62,.62]:
 for j in range(9):
  a=math.pi*j/8;V.append((x,peak+.04+.12*math.sin(a),1.8+.24*math.cos(a)));UV.append(((x+.62)/1.24,j/8))
for j in range(8):F.append((j,j+1,j+10,j+9))
o=create('Plain straw ridge dressing',V,F,UV,['Thatch'],[0]*len(F),'Thatch');mod=o.modifiers.new('Ridge coat thickness','SOLIDIFY');mod.thickness=.07;mod.offset=-1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Merchant01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Merchant01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'bodyFootprint':[6.8,6.4],'floorDatum':FLOOR,'customerDoor':[1.4,2.4],'deliveryDoor':[1.6,2.4],'counterHeightAboveFloor':1.0,'counterWidth':2.4,'counterUsableDepth':.65,'sellingHatch':[2.3,1.25],'roofPitchNote':'Nominal main thatch slopes approximately 45 degrees; end hips slightly steeper.','models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Merchant01.blend'));print('MERCHANT_READY',sum(row['triangles'] for row in cat))
