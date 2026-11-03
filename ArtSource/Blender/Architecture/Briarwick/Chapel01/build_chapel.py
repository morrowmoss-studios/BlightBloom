"""Rough Chapel01: small stone chapel with dominant stained-glass front gable.
No existing buildings or source assets are overwritten.
"""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
if (H/'BW_Chapel01.blend').exists():raise RuntimeError('Candidate exists; inspect before rebuilding')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 m=bpy.data.materials.new(role['name']);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/next(t['path'] for t in role['textures'] if t['property']=='_BaseMap')),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role['name']]=m
for role,path in [('Plaster','Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'),('Thatch','Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures/BW_StableA03_Thatch_BaseColor.png')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'native_helpers.py'),'exec'))
code=(R/'ArtSource/Blender/Architecture/Briarwick/Bakery02/reconstruct_bakery.py').read_text();code=code[code.index('def wall('):code.index("wall('Front continuous")].replace("['Plaster02']","['Plaster']").replace('3.12','3.45');exec(compile(code,str(H/'wall_helpers.py'),'exec'))



# Dedicated low-contrast stone and glass, source artwork packed.
for role,filename in [('Masonry','Masonry'),('StainedGlass','StainedGlass')]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.9 if role=='Masonry' else .65;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Chapel01/Textures'/('BW_Chapel01_'+filename+'.png')));n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[role]=m
for role,color in [('DressStone',(.58,.55,.46,1)),('Lead',(.13,.14,.13,1))]:
 m=bpy.data.materials.new(role);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Roughness'].default_value=.9;mats[role]=m
# Nave: 7.6 x 10.8 m. Street door remains on the original approach axis.
wall('Front masonry',-3.8,3.8,6.5,[(-.8,.8,0,2.5)],index=0)
wall('Rear masonry',-3.8,3.8,-4.3,[],index=1)
wall('West masonry',-4.3,6.5,-3.8,[(-1.6,-.8,1.4,2.7),(2.4,3.2,1.4,2.7)],True,2)
wall('East masonry',-4.3,6.5,3.8,[(-1.6,-.8,1.4,2.7),(2.4,3.2,1.4,2.7)],True,3)
for o in groups.pop('Plaster'):
 side='West' in o.name or 'East' in o.name;o.data.materials.clear();o.data.materials.append(mats['Masonry'])
 for p in o.data.polygons:
  p.material_index=0
  for li in p.loop_indices:
   q=P.inverted()@o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=((q.z if side else q.x)/3,q.y/1.25)
 groups.setdefault('Masonry',[]).append(o)
# Sparse dressed corners, not flying buttresses or ornamental pillars.
for x in [-3.8,3.8]:
 for z in [-4.3,6.5]:box('Dressed corner',(x,1.68,z),(.38,3.36,.38),'DressStone','StoneTrim',.018)
for x in [-.90,.90]:box('Entry jamb',(x,1.25,6.56),(.20,2.5,.40),'DressStone','StoneTrim',.012)
box('Entry lintel',(0,2.64,6.56),(2.10,.28,.40),'DressStone','StoneTrim',.015)
for side in [-1,1]:
 cx=side*.397;native('wall_wood_door1.004','Closed double entry',lambda v,cx=cx,side=side:(cx+(v.x-.38014054)/.685009*.784*side,.018+v.y/1.83421123*2.47,6.40+v.z),'MainDoor',flip=side<0)
def stone(name,pos,size,group='Foundation'):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),group)
for z,spans in [(6.5,[(-3.8,-.81),(.81,3.8)]),(-4.3,[(-3.8,3.8)])]:
 for a,b in spans:stone('Stone footing',((a+b)/2,-.06,z),(b-a,.38,.40))
for x in [-3.8,3.8]:stone('Side foundation',(x,-.06,1.1),(.40,.38,10.8))
stone('Entry threshold',(0,-.025,6.64),(1.7,.15,.60),'Steps');stone('Front stoop',(0,-.075,7.02),(2.4,.15,.80),'Steps')
# Small deep-set side lights, plain surrounds.
for x in [-3.86,3.86]:
 for z in [-1.2,2.8]:
  box('Side leaded light',(x,2.05,z),(.07,1.3,.8),'glass','SideWindows',0)
  for zz in [z-.46,z+.46]:box('Stone light jamb',(x,2.05,zz),(.25,1.5,.14),'DressStone','StoneTrim',.008)
  for y in [1.33,2.77]:box('Stone light rail',(x,y,z),(.25,.14,1.06),'DressStone','StoneTrim',.008)
  box('Simple side mullion',(x,2.05,z),(.10,1.3,.045),'Lead','SideWindows',.001)
# Big pointed window; sun and botanical glass rather than lettering.
right=[(2.35,3.70),(2.35,4.25)]+[(2.35*(1-t)**.85,4.25+2.55*t) for t in [j/16 for j in range(1,17)]]
outline=[(-x,y) for x,y in right]+[(x,y) for x,y in reversed(right[:-1])]
outer=[(x*1.075,5.2+(y-5.2)*1.075) for x,y in outline]
def closed_profile(name,poly,z,thick,role,group):
 V=[(x,y,zz) for zz in [z-thick/2,z+thick/2] for x,y in poly];n=len(poly);F=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];UV=[((x+2.5)/5,(y-3.55)/3.5) for x,y,zz in V];return create(name,V,F,UV,[role],[0]*len(F),group,True)
closed_profile('Village sun and sprig glass',outline,6.54,.045,'StainedGlass','StainedGlass')
# Continuous deep reveal ring (front, rear, outer and inner edges).
V=[(x,y,z) for z,poly in [(6.70,outer),(6.70,outline),(6.46,outer),(6.46,outline)] for x,y in poly];n=len(outline);F=[]
for i in range(n):
 j=(i+1)%n;F.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
create('Pointed dressed stone reveal',V,F,[((x+3)/6,y/4) for x,y,z in V],['DressStone'],[0]*len(F),'StoneTrim',True,.007)
# Physical dark inner lead border, stained-glass lines are painted into the UV.
small=[(x*.984,5.2+(y-5.2)*.984) for x,y in outline];V=[(x,y,6.575) for poly in [outline,small] for x,y in poly];F=[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];create('Lead perimeter',V,F,[(x/5,y/4) for x,y,z in V],['Lead'],[0]*len(F),'Lead')
# Real front gable aperture: bands of plaster only outside the reveal.
rside=[(x*1.075,5.2+(y-5.2)*1.075) for x,y in right]
def inner(y):
 for (x0,y0),(x1,y1) in zip(rside,rside[1:]):
  if y0<=y<=y1:return x0+(x1-x0)*(y-y0)/max(.0001,y1-y0)
 return 0
levels=[3.45]+[y for x,y in rside]+[7.14]
for k,(lo,hi) in enumerate(zip(levels,levels[1:])):
 out0=3.8*(7.14-lo)/(7.14-3.45);out1=3.8*(7.14-hi)/(7.14-3.45)
 if hi<=rside[0][1] or lo>=rside[-1][1]:spans=[(-out0,out0,-out1,out1)]
 else:
  i0=inner(lo);i1=inner(hi);spans=[(-out0,-i0,-out1,-i1),(i0,out0,i1,out1)]
 for a,b,c,d in spans:
  poly=[(a,lo),(b,lo),(d,hi),(c,hi)];closed_profile('Front gable aperture band',poly,6.5,.22,'Plaster','Gables')
closed_profile('Plain rear plaster gable',[(-3.8,3.45),(3.8,3.45),(0,7.14)],-4.3,.22,'Plaster','Gables')
# Two plain timber wall plates support a source-authentic weathered shingle roof.
for x in [-3.8,3.8]:box('Eave wall plate',(x,3.35,1.1),(.24,.20,11.0),'wood2','Timber',.004)
# Read-only package roof modules preserve their original UVs; remove their end infill.
for i in range(6):
 z=-4.7+(i+.5)*11.6/6
 native('roof_wide1_3.002','Weathered shingle roof',lambda v,z=z:(v.x/1.69875622*4.15,3.45+v.y/2.38497162*3.8,z+v.z*11.6/12),'Roof',select=lambda role,vs:role!='wood3')
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Chapel01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Chapel01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
(H/'ModelCatalog.json').write_text(json.dumps({'bodyFootprint':[7.6,10.8],'floorDatum':FLOOR,'mainDoor':[1.6,2.5],'glassWidth':4.7,'glassHeight':3.1,'models':cat},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Chapel01.blend'));print('CHAPEL_READY',sum(row['triangles'] for row in cat))
