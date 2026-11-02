"""Rough Farmhouse01: rural home, loft, covered stoop and integrated hearth chimney.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
if (H/'BW_Farmhouse01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Thatch','Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures/BW_StableA03_Thatch_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('3.12','3.05');exec(compile(code,str(H/'wall_helpers.py'),'exec'))

# Broad longhouse: 9 x 7.2 m, loft below a plain rural gable.
wall('Front home wall',-4.5,4.5,3.6,[(-.7,.7,0,2.4),(-3.6,-2.3,1.1,2.15),(2.2,3.5,1.1,2.15)],index=0)
wall('Rear working entrance',-4.5,4.5,-3.6,[(1.85,3.15,0,2.3),(-3.4,-2.2,1.15,2.1)],index=1)
wall('West gable lower',-3.6,3.6,-4.5,[(-.75,.55,1.15,2.15)],True,2)
wall('East hearth gable lower',-3.6,3.6,4.5,[(1.05,2.15,1.2,2.15)],True,3)
for x,z in [(-4.5,-3.6),(4.5,-3.6),(-4.5,3.6),(4.5,3.6),(-1.8,3.6),(1.75,3.6),(-.6,-3.6)]:native('wooden_post_column_size1.079','Bearing timber',lambda v,x=x,z=z:(x+v.x*.8,v.y*3.05/3.4059584,z+v.z*.8),'Timber')
for z in [-3.6,3.6]:box('Long wall plate',(0,2.94,z),(9.2,.22,.23),'wood2','Timber',.004)
for x in [-4.5,4.5]:box('Gable tie',(x,3.0,0),(.23,.22,7.35),'wood2','Timber',.004);box('Gable sill',(x,.16,0),(.23,.18,7.2),'wood2','Timber',.004)
for z,intervals in [(3.6,[(-4.5,-.71),(.71,4.5)]),(-3.6,[(-4.5,1.84),(3.16,4.5)])]:
 for a,b in intervals:box('Interrupted sill',((a+b)/2,.16,z),(b-a,.18,.23),'wood2','Timber',.003)
# Modest boarded gable infill avoids ornamental king/A-shaped beams.
gableheight=lambda z:6.15-abs(z)*3.10/4.12
for x in [-4.5,4.5]:
 boardrun('Loft weatherboard',-3.6,3.6,gableheight,x,'side',low=3.05,group='Gables',holes=[(-.42,.42,3.9,4.68)])
 # Frame the loft opening, not a decorative truss.
 for z in [-.48,.48]:box('Loft light jamb',(x,4.29,z),(.17,.94,.12),'wood2','Timber',.003)
 for y in [3.84,4.74]:box('Loft light rail',(x,y,0),(.17,.12,1.08),'wood2','Timber',.003)
 box('Loft dark glazing',(x,4.29,0),(.06,.78,.84),'glass','Windows',0)
# Static doors with generous real openings.
for name,cx,z,w,height in [('MainDoor',0,3.66,1.4,2.4),('ServiceDoor',2.5,-3.66,1.3,2.3)]:
 for x in [cx-w/2-.075,cx+w/2+.075]:box('Entry jamb',(x,height/2,z),(.15,height,.25),'wood2','Timber',.004)
 box('Entry lintel',(cx,height+.105,z),(w+.42,.21,.27),'wood2','Timber',.004)
 native('wall_wood_door1.004',name,lambda v,cx=cx,z=z,w=w,height=height:(cx+(v.x-.38014054)/.685009*(w-.016),.018+v.y/1.83421123*(height-.03),z+(-.12 if z>0 else .12)+v.z),name)
def light(c,w,h,side=False):
 x,y,z=c;box('Small home glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for u in [-w/2,w/2]:box('Window jamb',(x,y,z+u) if side else (x+u,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box('Window rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box('Window mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.002)
 box('Projecting sill',(x,y-h/2-.07,z),(.30,.10,w+.35) if side else (w+.35,.10,.30),'wood3','Windows',.004)
for c,w,h,side in [((-2.95,1.625,3.67),1.3,1.05,False),((2.85,1.625,3.67),1.3,1.05,False),((-2.8,1.625,-3.67),1.2,.95,False),((-4.57,1.65,-.1),1.3,1,True),((4.57,1.675,1.6),1.1,.95,True)]:light(c,w,h,side)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)
for z,intervals in [(3.6,[(-4.5,-.71),(.71,4.5)]),(-3.6,[(-4.5,1.84),(3.16,4.5)])]:
 for a,b in intervals:stone('Local stone plinth',((a+b)/2,-.055,z),(b-a,.38,.32))
for x in [-4.5,4.5]:stone('Side plinth',(x,-.055,0),(.32,.38,7.2))
stone('Covered stoop',(0,-.075,4.25),(2.45,.15,1.38),'Steps');stone('Main threshold',(0,-.015,3.69),(1.43,.10,.45),'Steps');stone('Service step',(2.5,-.045,-3.85),(1.5,.15,.65),'Steps')
# Small board-covered stoop; structurally connected ledger and bearing posts.
for x in [-1.13,1.13]:native('wooden_post_column_size1.079','Porch post',lambda v,x=x:(x+v.x*.58,v.y*2.64/3.4059584,4.88+v.z*.58),'PorchTimber');stone('Porch pad',(x,-.045,4.88),(.28,.26,.28))
box('Porch ledger',(0,2.85,3.65),(2.65,.17,.20),'wood2','PorchTimber',.003);box('Porch bearing',(0,2.59,4.88),(2.65,.18,.20),'wood2','PorchTimber',.003)
def beam(name,a,b,width,depth,group='PorchTimber'):
 a,b=map(Vector,[a,b]);d=b-a;u=Vector((width/2,0,0));v=d.cross(u).normalized()*depth/2;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];return create(name,V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.03,j//4*d.length,width,d.length,'wood3') for j in range(8)],['wood3'],[0]*6,group,True,.003)
for x in [-1.13,1.13]:beam('Porch rafter',(x,2.84,3.54),(x,2.62,5.05),.12,.14)
for i in range(10):
 x=-1.4+(i+.5)*.28;beam('Weathered entry board',(x,2.94,3.50),(x,2.72,5.13),.284,.055,'PorchRoof')
# Source hearth/flue is inside the shell; no exterior fireplace.
native('chimney_outside_size1.001','Hearth chimney',lambda v:(2.65+v.x*.65,v.y*1.025,-1.25+v.z*.65),'Chimney')
# Two continuous, thick thatch slopes with a gentle ridge sag and irregular eave.
V=[];F=[];UV=[];nx=32;ny=18
for side in [-1,1]:
 base=len(V)
 for layer in [0,1]:
  for j in range(ny+1):
   t=j/ny
   for i in range(nx+1):
    u=i/nx;x=-4.88+9.76*u;z=side*4.12*t;y=6.15-3.10*t-.045*math.sin(math.pi*u)+.018*math.sin(x*1.3+z*.6)*t-.24*layer;z+=side*.025*math.sin(x*1.7)*t*t
    V.append((x,y,z));UV.append((.03+.94*u,.03+.94*t))
 N=(nx+1)*(ny+1)
 for j in range(ny):
  for i in range(nx):
   k=base+j*(nx+1)+i;F.append((k,k+1,k+nx+2,k+nx+1));k+=N;F.append((k+nx+1,k+nx+2,k+1,k))
 for i in range(nx):
  k=base+ny*(nx+1)+i;F.append((k,k+N,k+N+1,k+1))
 for i in [0,nx]:
  for j in range(ny):
   k=base+j*(nx+1)+i;F.append((k,k+nx+1,k+nx+1+N,k+N))
o=create('Continuous gable thatch',V,F,UV,['Thatch'],[0]*len(F),'Thatch');bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
for p in o.data.polygons:p.use_smooth=True
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Farmhouse01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Farmhouse01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'bodyFootprint':[9.0,7.2],'floorDatum':FLOOR,'mainDoor':[1.4,2.4],'serviceDoor':[1.3,2.3],'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Farmhouse01.blend'));print('FARMHOUSE_READY',sum(row['triangles'] for row in cat))
