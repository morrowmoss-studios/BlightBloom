"""Blacksmith01: enclosed rear workshop and open front work apron. New assets only."""
import bpy,bmesh,json,math
from mathutils import Vector,Matrix
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4]
if (H/'BW_Blacksmith01.blend').exists():raise RuntimeError('Existing candidate; inspect before rebuild')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.87;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Clay','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures/BW_Bakery01_Clay_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
m=bpy.data.materials.new('Charcoal');m.diffuse_color=(.055,.045,.035,1);mats['Charcoal']=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
# Real shaft-facing stone UVs, not arbitrary wood-atlas coordinates.
d=src['chimney_outside_size1.001'];best=None
for si,ts in enumerate(d['submeshes']):
 if d['materials'][si]!='rock2':continue
 for k in range(0,len(ts),3):
  ids=ts[k:k+3];v=[Vector(d['vertices'][j]) for j in ids];n=(v[1]-v[0]).cross(v[2]-v[0])
  if n.length<1e-7 or abs(n.normalized().z)<.9 or max(p.y for p in v)-min(p.y for p in v)<3:continue
  if best is None or n.length>best[0]:best=(n.length,ids,v)
_,ids,v=best;M=Matrix([(p.x,p.y,1) for p in v]);u=M.inverted()@Vector([d['uv'][j][0] for j in ids]);w=M.inverted()@Vector([d['uv'][j][1] for j in ids]);templates['rock2']=(u,w,min(p.x for p in v),max(p.x for p in v),min(p.y for p in v),max(p.y for p in v))
# Reuse continuous wall/reveal construction, with a lower 3.10 m workshop wall.
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('3.12','3.10')
exec(compile(code,str(H/'wall_helpers.py'),'exec'))
wall('Workshop front',-4.6,4.6,.5,[(-3.45,-.95,0,2.65),(-.2,1.1,1.15,2.25),(1.65,3.85,0,3.1)],index=0)
wall('Workshop rear',-4.6,4.6,-3.7,[],index=1)
wall('Workshop west',-3.7,.5,-4.6,[(-2.55,-1.25,0,2.3)],True,2)
wall('Workshop east',-3.7,.5,4.6,[(-2.3,-1.1,1.2,2.2)],True,3)
# Fireproof breast replaces the wall, rather than an arbitrary exterior fireplace.
box('Stone fire breast',(2.75,1.57,.48),(2.2,3.14,.42),'rock2','ForgeMasonry',.008)
# Footed corners and front bearings, no applied gable ornaments.
for i,(x,z) in enumerate([(-4.6,-3.7),(4.6,-3.7),(-4.6,.5),(4.6,.5),(-4.6,3.7),(-.35,3.7),(4.6,3.7)]):
 native('wooden_post_column_size1.079','Bearing post '+str(i),lambda v,x=x,z=z:(v.x*.88+x,v.y*3.18/3.4059584,v.z*.88+z),'Timber')
for z in [-3.7,.5,3.7]:box('Bearing plate',(0,3.12,z),(9.45,.24,.25),'wood2','Timber',.005)
for x in [-4.6,4.6]:box('Side plate',(x,3.12,0),(.23,.22,7.65),'wood2','Timber',.005)
# Purposeful short knee braces carry the front beam into posts.
for x,dx in [(-4.6,.48),(-.35,-.45),(-.35,.45),(4.6,-.48)]:
 a=Vector((x,2.64,3.7));b=Vector((x+dx,3.02,3.7));delta=b-a;u=Vector((delta.y,-delta.x,0)).normalized()*.055;v=Vector((0,0,.07));V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]]
 create('Load bearing knee brace',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.035,j//4*delta.length,.11,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'Timber',True,.003)
# Workshop opening/frame, no leaf blocking the main work approach.
for x in [-3.53,-.87]:box('Wide opening jamb',(x,1.34,.5),(.16,2.68,.28),'wood2','Timber',.005)
box('Wide opening head',(-2.2,2.76,.5),(2.95,.22,.30),'wood2','Timber',.006)
for z in [-2.63,-1.17]:box('Service jamb',(-4.6,1.17,z),(.28,2.34,.16),'wood2','Timber',.005)
box('Service head',(-4.6,2.41,-1.9),(.30,.22,1.75),'wood2','Timber',.006)
# Fixed-open human leaf lies against workshop's inner west wall; no interaction script.
o=native('wall_wood_door1.004','Side service leaf',lambda v:(-4.43+v.z, v.y/1.83421123*2.25+.025,-1.22-(v.x-.03763604)/.685009*1.25),'ServiceDoor',flip=True)
# Two small practical lights. Dim opaque glazing avoids promising a finished interior.
def light(name,c,w,h,side=False):
 x,y,z=c;box(name+' glazing',c,(.05,h,w) if side else (w,h,.05),'glass','Windows',0)
 for v in [-w/2,w/2]:box(name+' jamb',(x,y,z+v) if side else (x+v,y,z),(.18,h+.16,.12) if side else (.12,h+.16,.18),'wood2','Windows',.003)
 for v in [-h/2,h/2]:box(name+' rail',(x,y+v,z),(.18,.12,w+.24) if side else (w+.24,.12,.18),'wood2','Windows',.003)
 box(name+' mullion',c,(.08,h,.05) if side else (.05,h,.08),'wood2','Windows',.001)
light('Front shop light',(.45,1.7,.55),1.3,1.1);light('East side light',(4.65,1.7,-1.7),1.2,1.0,True)
# Native stone floor/plinth modules preserve weathered material alignment.
def stone(name,pos,size,group='Foundation'):
 native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)
for x in [-4.6,4.6]:stone('Wall plinth',(x,-.10,-1.6),(.28,.36,4.2))
stone('Rear plinth',(0,-.10,-3.7),(9.2,.36,.28))
for a,b in [(-4.6,-3.45),(-.95,4.6)]:stone('Front wall plinth',((a+b)/2,-.10,.5),(b-a,.36,.28))
# Broad floor tiles at ground level; no raised slab blocking access.
for i in range(4):
 for j in range(3):stone('Working floor',( -3.45+i*2.3,-.075,-2.47+j*2.47),(2.3,.15,2.47),'Floor')
for x in [-4.6,-.35,4.6]:stone('Front post pad',(x,-.055,3.7),(.40,.25,.40))
stone('Service threshold',(-4.6,-.015,-1.9),(.42,.06,1.3),'Floor')
# Raised masonry forge bed, hollow tapering smoke canopy and a shaft tied into the breast.
box('Forge hearth base',(2.75,.40,1.05),(1.72,.80,1.3),'rock2','ForgeMasonry',.018)
box('Hearth slab',(2.75,.86,1.05),(1.88,.12,1.42),'rock2','ForgeMasonry',.012)
box('Charcoal bed',(2.75,.935,1.0),(1.28,.05,.88),'Charcoal','ForgeCore',.012)
for x in [1.9,3.6]:box('Hearth curb',(x,.99,1.05),(.16,.22,1.3),'rock2','ForgeMasonry',.007)
# Tapered canopy wall shells, open below and connected to the chimney throat.
lo=[(1.8,1.95,.34),(3.7,1.95,.34),(3.7,1.95,1.83),(1.8,1.95,1.83)];hi=[(2.26,3.05,.50),(3.24,3.05,.50),(3.24,3.05,1.23),(2.26,3.05,1.23)]
for k in range(4):
 V=[lo[k],lo[(k+1)%4],hi[(k+1)%4],hi[k]];uv=[timberUV((i%2-.5)*1.4,i//2*1.2,1.4,1.2,'rock2') for i in range(4)];o=create('Tapered forge hood',V,[(0,1,2,3)],uv,['rock2'],[0],'ForgeMasonry');mod=o.modifiers.new('Masonry hood thickness','SOLIDIFY');mod.thickness=.1;mod.offset=-1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
native('chimney_outside_size1.001','Stone flue',lambda v:(2.75+v.x*.75,3.0+(v.y-1.713)*.75,.55+v.z*.75),'Chimney',select=lambda role,V:role=='rock2' and min(p[1] for p in V)>1.68)
# Side gables are quiet boarded loft ends, supported on the posts/plates.
peak=5.65;ridgeZ=-.4
def roofY(z):return peak-(peak-3.15)*abs(z-ridgeZ)/(3.8 if z<ridgeZ else 4.7)+.012*math.sin(z*1.1)
for x in [-4.6,4.6]:boardrun('Side loft boarding',-3.7,3.7,lambda z:roofY(z)-.14,x,'side',low=3.12,group='UpperTimber')
# Tiled slopes and collision deck reuse Bakery02 clipping/lap logic with a new plan.
# Hole boundary stays inside the masonry shaft footprint.
rect=(2.38,3.12,.61,1.06)
lib=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();exec(compile(lib[lib.index('def clip('):lib.index('RV=[];RF=[];RU=[]')],str(H/'roof_helpers.py'),'exec'))
RV=[];RF=[];RU=[]
def addface(coords,uvs):
 for poly in outside(list(zip(map(Vector,coords),map(Vector,uvs)))):
  start=len(RV);RV.extend(tuple(p) for p,u in poly);RU.extend(tuple(u) for p,u in poly);RF.append(tuple(range(start,len(RV))))
DV=[];DF=[];DU=[]
for end in [-4.2,4.3]:
 pts=[Vector((-5.15,roofY(ridgeZ),ridgeZ)),Vector((5.15,roofY(ridgeZ),ridgeZ)),Vector((5.15,roofY(end),end)),Vector((-5.15,roofY(end),end))]
 for shift in [0,-.13]:
  for piece in outside([(p+Vector((0,shift,0)),Vector((i%2,i//2))) for i,p in enumerate(pts)]):
   k=len(DV);DV.extend(tuple(p) for p,u in piece);DU.extend(tuple(u) for p,u in piece);DF.append(tuple(range(k,len(DV))))
 for a,b in zip(pts,pts[1:]+pts[:1]):
  k=len(DV);DV.extend([tuple(a),tuple(b),tuple(b-Vector((0,.13,0))),tuple(a-Vector((0,.13,0)))]);DU.extend([(0,0),(1,0),(1,1),(0,1)]);DF.append(tuple(range(k,k+4)))
create('Tile bearing deck',DV,DF,DU,['interior_roof'],[0]*len(DF),'RoofDeck')
for slope,end in enumerate([-4.2,4.3]):
 for row in range(13):
  for col in range(32):
   offset=.04*math.sin(col*1.6+row*.9);z0=ridgeZ+(end-ridgeZ)*max(0,(row-.18)/13)+(offset if row else 0);z1=ridgeZ+(end-ridgeZ)*(row+1)/13+(offset if row<12 else 0);x0=-5.15+10.3*col/32;x1=-5.15+10.3*(col+1)/32;idx=(col*3+row*5+slope)%8
   for cap in [False,True]:
    n=4 if cap else 3;a=x1-.043 if cap else x0;b=x1+.043 if cap else x1
    if cap and col==31:continue
    vs=[];uv=[]
    for t,z in [(0,z0),(1,z1)]:
     for j in range(n+1):
      u=j/n;x=a+(b-a)*u;y=roofY(z)+.02+(13-row)*.003+.035*t*t+(.055*math.sin(u*math.pi) if cap else -.017*math.sin(u*math.pi));vs.append((x,y,z));uv.append(((idx%4+.07+.86*u)/4,(idx//4+.05+.9*t)/2))
    for j in range(n):
     ids=[j,j+1,n+2+j,n+1+j];addface([vs[i] for i in ids],[uv[i] for i in ids]);ids=[n+1+j,n+2+j];top=[Vector(vs[i]) for i in ids];addface(top+[p-Vector((0,.018,0)) for p in top[::-1]],[uv[i] for i in ids]+[(uv[i][0],uv[i][1]-.008) for i in ids[::-1]])
for k in range(29):
 x0=-5.16+k*10.32/29;x1=x0+10.32/29+.035;vs=[];uv=[]
 for t,x in [(0,x0),(1,x1)]:
  for j in range(7):
   a=math.pi*j/6;vs.append((x,roofY(ridgeZ)+.04+.11*math.sin(a),ridgeZ+.14*math.cos(a)));uv.append(((k%4+.06+.88*j/6)/4,(k%2+.05+.9*t)/2))
 for j in range(6):addface([vs[i] for i in [j,j+1,j+8,j+7]],[uv[i] for i in [j,j+1,j+8,j+7]])
o=create('Weathered clay covering',RV,RF,RU,['Clay'],[0]*len(RF),'ClayRoof')
for p in o.data.polygons:p.use_smooth=True
# Structural edge boards follow slopes; no applied triangle ornaments.
for x in [-5.04,5.04]:
 for z in [-4.2,4.3]:
  a=Vector((x,roofY(z)-.09,z));b=Vector((x,roofY(ridgeZ)-.09,ridgeZ));delta=b-a;u=Vector((.065,0,0));v=delta.cross(u).normalized()*.075;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];create('Structural verge',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.04,j//4*delta.length,.14,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'Timber',True,.003)
for z in [-4.15,4.25]:box('Eave fascia',(0,roofY(z)-.09,z),(10.3,.17,.14),'wood2','Timber',.004)
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Blacksmith01_'+group;o.data.name=o.name;bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.normal_update()
 if group=='ClayRoof':bmesh.ops.reverse_faces(bm,faces=[f for f in bm.faces if f.normal.z<-.01])
 if group=='RoofDeck':
  flip=[]
  for f in bm.faces:
   c=f.calc_center_median();top=roofY(-c.y);desired=1 if c.z>top-.05 else -1
   if f.normal.z*desired<-.01:flip.append(f)
  bmesh.ops.reverse_faces(bm,faces=flip)
 bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'bodyFootprint':[9.2,7.4],'enclosedWorkshop':[9.2,4.2],'coveredFrontApron':[9.2,3.2],'wideOpening':[2.5,2.65],'serviceOpening':[1.3,2.3],'ridgeHeight':5.8,'chimneyHeight':6.59,'chimneyHole':rect,'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Blacksmith01.blend'));print('SMITHY_READY',sum(r['triangles'] for r in cat))
