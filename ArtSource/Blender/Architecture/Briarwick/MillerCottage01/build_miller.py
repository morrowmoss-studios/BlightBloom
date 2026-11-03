"""Rough MillerCottage01: narrow gabled home, low side grain store and integrated hearth chimney.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
if (H/'BW_MillerCottage01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Thatch','Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures/BW_StableA03_Thatch_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('3.12','3.0');exec(compile(code,str(H/'wall_helpers.py'),'exec'))


# Main 6.6 x 7.8 m home, plus 1.4 x 3.8 m low grain store.
wall('Road front',-3.3,3.3,3.9,[(-.30,1.10,0,2.4),(-2.55,-1.45,1.15,2.15),(2.0,2.65,1.35,2.15)],index=0)
wall('Creek rear',-3.3,3.3,-3.9,[(.95,2.25,0,2.3),(-2.55,-1.45,1.15,2.1)],index=1)
wall('West home wall',-3.9,3.9,-3.3,[(-1.6,-.5,1.15,2.15)],True,2)
wall('East home wall',-3.9,3.9,3.3,[],True,3)
for x,z in [(-3.3,-3.9),(3.3,-3.9),(-3.3,3.9),(3.3,3.9),(-.9,3.9),(.2,-3.9)]:native('wooden_post_column_size1.079','Wall bearing',lambda v,x=x,z=z:(x+v.x*.8,v.y*3.0/3.4059584,z+v.z*.8),'Timber')
for z in [-3.9,3.9]:box('Gable tie',(0,2.9,z),(6.78,.20,.22),'wood2','Timber',.004)
for x in [-3.3,3.3]:box('Side wall plate',(x,2.9,0),(.22,.20,8.0),'wood2','Timber',.004);box('Side sill',(x,.13,0),(.22,.18,7.8),'wood2','Timber',.003)
for z,spans in [(3.9,[(-3.3,-.31),(1.11,3.3)]),(-3.9,[(-3.3,.94),(2.26,3.3)])]:
 for a,b in spans:box('Interrupted sill',((a+b)/2,.13,z),(b-a,.18,.22),'wood2','Timber',.003)
# Full closed plaster gables, no arbitrary decorative triangles or upper false windows.
ridge=-.42;peak=5.6
for z,index in [(3.9,0),(-3.9,1)]:
 V=[(-3.3,3,z-.11),(3.3,3,z-.11),(ridge,5.35,z-.11),(-3.3,3,z+.11),(3.3,3,z+.11),(ridge,5.35,z+.11)]
 UV=[((index+.06+.88*(x+3.3)/6.6)/2,(.06+.88*y/5.7)/2) for x,y,zz in V]
 create('Plain plaster gable',V,[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(0,1,4,3)],UV,['Plaster'],[0]*5,'Plaster',True)
# Static usable-scale door frames; no interaction components.
for name,cx,z,w,height in [('MainDoor',.4,3.96,1.4,2.4),('ServiceDoor',1.6,-3.96,1.3,2.3)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box('Door jamb',(x,height/2,z),(.15,height,.25),'wood2','Timber',.004)
 box('Door lintel',(cx,height+.10,z),(w+.42,.20,.27),'wood2','Timber',.004)
 native('wall_wood_door1.004',name,lambda v,cx=cx,z=z,w=w,height=height:(cx+(v.x-.38014054)/.685009*(w-.016),.018+v.y/1.83421123*(height-.03),z+(-.12 if z>0 else .12)+v.z),name)
def light(c,w,h,side=False):
 x,y,z=c;box('Small home glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box('Window jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box('Window rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box('Window mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.002)
 box('Projecting sill',(x,y-h/2-.07,z),(.30,.10,w+.35) if side else (w+.35,.10,.30),'wood3','Windows',.004)

for c,w,h,side in [((-2,1.65,3.97),1.1,1,False),((2.325,1.75,3.97),.65,.8,False),((-2,1.625,-3.97),1.1,.95,False),((-3.37,1.65,-1.05),1.1,1,True)]:light(c,w,h,side)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)

for z,spans in [(3.9,[(-3.3,-.31),(1.11,3.3)]),(-3.9,[(-3.3,.94),(2.26,3.3)])]:
 for a,b in spans:stone('Stone footing',((a+b)/2,-.07,z),(b-a,.38,.32))
for x in [-3.3,3.3]:stone('Side footing',(x,-.07,0),(.32,.38,7.8))
stone('Main threshold',(.4,-.035,4.1),(1.6,.17,.68),'Steps');stone('Service threshold',(1.6,-.035,-4.1),(1.5,.17,.68),'Steps')
# Low sealed board grain/tool store; no displayed goods or machinery.
storeheight=lambda x:2.8-(x-3.3)*.38
boardrun('Store front',3.3,4.7,storeheight,1.9,low=0,group='Store')
boardrun('Store rear',3.3,4.7,storeheight,-1.9,low=0,group='Store')
boardrun('Store end',-1.9,1.9,2.268,4.7,'side',low=0,group='Store')
for z in [-1.9,1.9]:native('wooden_post_column_size1.079','Store corner',lambda v,z=z:(4.7+v.x*.65,v.y*2.27/3.4059584,z+v.z*.65),'Timber');stone('Store foundation',(4.0,-.07,z),(1.4,.38,.28))
stone('Store end foundation',(4.7,-.07,0),(.28,.38,3.8))
# Closed backing stops daylight between store planks without creating a playable interior.
box('Store backing',(4.66,1.13,0),(.045,2.26,3.8),'wood3','Store',.002)
for z in [-1.87,1.87]:box('Store front backing',(4.0,1.13,z),(1.4,2.26,.045),'wood3','Store',.002)
# Hearth/flue remains inside the home below its emergence through the roof.
native('chimney_outside_size1.001','Integrated hearth',lambda v:(1.7+v.x*.51,v.y*.9,-1.55+v.z*.51),'Chimney')
# Simple continuous thatch: offset ridge, two unequal slopes, restrained sag.
def roofcoat(name,x0,x1,z0,z1,height,group='Thatch',nx=18,nz=26):
 V=[];F=[];UV=[]
 for layer in [0,1]:
  for j in range(nz+1):
   z=z0+(z1-z0)*j/nz
   for i in range(nx+1):
    x=x0+(x1-x0)*i/nx;y=height(x,z)-.22*layer;V.append((x,y,z));UV.append((.03+.94*j/nz,.03+.94*i/nx))
 N=(nx+1)*(nz+1)
 for j in range(nz):
  for i in range(nx):
   k=j*(nx+1)+i;F.append((k,k+1,k+nx+2,k+nx+1));k+=N;F.append((k+nx+1,k+nx+2,k+1,k))
 for j in range(nz):
  for i in [0,nx]:k=j*(nx+1)+i;F.append((k,k+nx+1,k+nx+1+N,k+N))
 for j in [0,nz]:
  for i in range(nx):k=j*(nx+1)+i;F.append((k,k+N,k+N+1,k+1))
 o=create(name,V,F,UV,['Thatch'],[0]*len(F),group);bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 for p in o.data.polygons:p.use_smooth=True
for end in [-3.72,3.72]:
 def ht(x,z,end=end):return peak-(peak-2.94)*abs(x-ridge)/abs(end-ridge)-.022*math.sin(math.pi*(z+4.25)/8.5)+.012*math.sin(z*1.6)*abs(x-ridge)/abs(end-ridge)
 roofcoat('Unequal main thatch slope',min(ridge,end),max(ridge,end),-4.25,4.25,ht)
roofcoat('Low store thatch',3.27,4.98,-2.15,2.15,lambda x,z:3.01-(x-3.27)*.38+.012*math.sin(z*1.5),nx=8,nz=12)
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_MillerCottage01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/MillerCottage01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'mainBody':[6.6,7.8],'store':[1.4,3.8],'floorDatum':FLOOR,'mainDoor':[1.4,2.4],'serviceDoor':[1.3,2.3],'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_MillerCottage01.blend'));print('MILLER_READY',sum(row['triangles'] for row in cat))
