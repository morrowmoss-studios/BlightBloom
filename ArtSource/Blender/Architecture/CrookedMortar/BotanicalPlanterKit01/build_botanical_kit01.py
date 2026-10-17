"""Shaped-leaf storybook botanical library; new outputs only. Metres, Unity Y up/Z exterior."""
import bpy,bmesh,math,json,sys,shutil
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/BotanicalPlanterKit01';PAINT=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/BotanicalPlanterKit01'
if (OUT/'CM_BotanicalPlanterKit01.blend').exists() and '--refine-own-kit' not in sys.argv:raise RuntimeError('Refusing existing source')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
atlas=bpy.data.images.load(str(PAINT/'CM_BotanicalElements01.png'));atlas.pack();atlas.colorspace_settings.name='sRGB'
paint=bpy.data.images.load(str(ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'));paint.pack();paint.colorspace_settings.name='sRGB'
shutil.copyfile(ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png',ASSET/'Textures/CM_BotanicalContainerPaint01.png')
mats={}
for key,col in {'Foliage':(1,1,1,1),'FoliageDry':(.95,.90,.83,1),'Timber':(1,1,1,1),'Clay':(.56,.37,.28,1),'Soil':(.075,.052,.032,1),'Stem':(.19,.25,.10,1),'Twine':(.42,.33,.19,1)}.items():
 m=bpy.data.materials.new('CM_Botanical_'+key);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=1;bs.inputs['Base Color'].default_value=col
 if key in ['Foliage','FoliageDry','Timber','Clay']:
  im=m.node_tree.nodes.new('ShaderNodeTexImage');im.image=atlas if key.startswith('Foliage') else paint;mix=m.node_tree.nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;mix.inputs[2].default_value=col;m.node_tree.links.new(im.outputs['Color'],mix.inputs[1]);m.node_tree.links.new(mix.outputs[0],bs.inputs['Base Color'])
  if key.startswith('Foliage'):m.node_tree.links.new(im.outputs['Alpha'],bs.inputs['Alpha']);m.surface_render_method='DITHERED'
 mats[key]=m
# Nonuniform rectangles follow actual generated sprite extents; pixels use bottom-up image coordinates.
regions=[(.016,.535,.326,.951),(.333,.537,.532,.95),(.565,.531,.746,.95),(.79,.526,.954,.95),(.030,.055,.304,.48),(.298,.062,.563,.408),(.59,.045,.717,.49),(.794,.045,.960,.485)]
pixels=list(atlas.pixels);W,H=atlas.size;profiles=[]
for x0,y0,x1,y1 in regions:
 rows=[]
 for j in range(7):
  v=y0+(y1-y0)*j/6;yy=min(H-1,max(0,int(v*H)));xs=[]
  for dy in range(-3,4):
   y=min(H-1,max(0,yy+dy))
   xs += [x for x in range(int(x0*W),int(x1*W)) if pixels[(y*W+x)*4+3]>.40]
  if not xs:
   for radius in [8,16,32]:
    for y in [max(0,yy-radius),min(H-1,yy+radius)]:xs += [x for x in range(int(x0*W),int(x1*W)) if pixels[(y*W+x)*4+3]>.40]
    if xs:break
  lo=max(x0,min(xs)/W-.003) if xs else (x0+x1)/2-.007;hi=min(x1,max(xs)/W+.003) if xs else (x0+x1)/2+.007
  if hi-lo<.008:lo-=.004;hi+=.004
  rows.append((v,lo,hi))
 profiles.append(rows)
parts=[];modules={};current='';leaf_serial=0

def P(p):return(p[0],p[2],p[1])
def module(name,kind,notes='',soil=0,sockets=None):
 global current
 current='CM_BotanicalPlanterKit01_'+name;modules[current]={'name':current,'kind':kind,'notes':notes,'soilHeight':soil,'sockets':sockets or [{'name':'Attach','position':[0,0,0]}],'parts':[]}
def obj(name,vs,fs,role,uvs=None,solid=True,bevel=0,leaf=False):
 raw_role=role
 if role=='Stem':role='FoliageDry' if modules[current]['kind']=='Hanging' else 'Foliage'
 me=bpy.data.meshes.new(current+'_'+name);me.from_pydata([P(v) for v in vs],[],fs);me.update();o=bpy.data.objects.new(me.name,me);s.collection.objects.link(o);me.materials.append(mats[role]);o['module']=current;o['role']=role;o['solid']=solid;o['leaf']=leaf
 if solid:
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if bevel:
  bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Soft handmade edge','BEVEL');mod.width=bevel;mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 me=o.data;uv=me.uv_layers.new(name='PaintUV0')
 for face in me.polygons:
  for li in face.loop_indices:
   idx=me.loops[li].vertex_index;v=me.vertices[idx].co
   if uvs:uv.data[li].uv=uvs[idx]
   elif role=='Timber':uv.data[li].uv=(.745+.08*v.x,.55+.12*v.z+.04*v.y)
   elif role=='Clay':uv.data[li].uv=(.27+.11*v.x,.60+.30*v.z+.04*v.y)
   else:uv.data[li].uv=(.1+v.x*.08,.1+v.z*.08+v.y*.02)
 # Opaque stem tubes sample a fully opaque small painted patch and share the leaf draw.
 if raw_role=='Stem':
  centre=(.87,.25) if role=='FoliageDry' else (.44,.75)
  for face in me.polygons:
   ids=list(face.loop_indices);ps=[me.vertices[me.loops[i].vertex_index].co for i in ids];drop=max(range(3),key=lambda i:abs(face.normal[i]));axes=[i for i in range(3) if i!=drop];lo=[min(p[k] for p in ps) for k in axes];span=[max(p[k] for p in ps)-lo[j] for j,k in enumerate(axes)]
   for li,p in zip(ids,ps):uv.data[li].uv=(centre[0]+.006*((p[axes[0]]-lo[0])/max(span[0],1e-8)-.5),centre[1]+.006*((p[axes[1]]-lo[1])/max(span[1],1e-8)-.5))
 if role.startswith('Foliage'):
  for face in me.polygons:face.use_smooth=True
 elif role in ['Clay','Stem','Twine']:
  for face in me.polygons:face.use_smooth=len(face.vertices)==4
 parts.append(o);modules[current]['parts'].append(o.name);return o

def box(n,p,d,role='Timber'):
 x,y,z=p;a,b,c=[q/2 for q in d];vs=[(x+sx*a,y+sy*b,z+sz*c) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]];return obj(n,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],role,bevel=.004)
def tube(n,points,r=.006,role='Stem',sides=5):
 points=[Vector(p) for p in points];vs=[]
 for i,p in enumerate(points):
  tangent=(points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized();ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0));a=tangent.cross(ref).normalized();b=tangent.cross(a);radius=r*(1-.35*i/(len(points)-1))
  for j in range(sides):vs.append(tuple(p+(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides))*radius))
 fs=[tuple(range(sides-1,-1,-1)),tuple(range(len(vs)-sides,len(vs)))]+[(k*sides+j,k*sides+(j+1)%sides,(k+1)*sides+(j+1)%sides,(k+1)*sides+j) for k in range(len(points)-1) for j in range(sides)]
 return obj(n,vs,fs,role)
def leaf(n,a,b,width,sprite=1,front=(0,0,1),dry=False):
 global leaf_serial
 a,b=Vector(a),Vector(b);up=(b-a).normalized();normal=Vector(front);right=up.cross(normal)
 if right.length<.01:right=up.cross(Vector((1,0,0)))
 right.normalize();normal=right.cross(up).normalized();vs=[];uv=[];x0,y0,x1,y1=regions[sprite]
 for j,(v,lo,hi) in enumerate(profiles[sprite]):
  t=j/6
  for k,u in enumerate([lo,(lo+hi)/2,hi]):
   x=(u-(x0+x1)/2)/(x1-x0);p=a.lerp(b,t)+right*x*width+normal*(math.sin(t*math.pi)*width*.10+(width*.065 if k==1 else 0)*math.sin(t*math.pi));vs.append(tuple(p));uv.append((u,v))
 fs=[(j*3+k,j*3+k+1,(j+1)*3+k+1,(j+1)*3+k) for j in range(6) for k in range(2)]
 o=obj(n,vs,fs,'FoliageDry' if dry else 'Foliage',uv,False,leaf=True);o['lod_keep']=leaf_serial%2==0 or sprite in [3,5,6];leaf_serial+=1;return o

def plant(species,base=(0,0,0),scale=1,seed=0,dry=False,down=False):
 origin=Vector(base);height={'Lavender':.53,'Sage':.36,'Rosemary':.55,'Thyme':.23,'Chamomile':.44}[species]*scale
 def T(p):p=Vector(p);return origin+Vector((p.x,-p.y if down else p.y,p.z))
 count=5 if species!='Thyme' else 6
 for j in range(count):
  angle=j*2.399+seed*.53;spread=(.11 if species!='Thyme' else .16)*scale;h=height*(.78+.22*(.5+.5*math.sin(j*1.87+seed)));tip=Vector((math.cos(angle)*spread,h,math.sin(angle)*spread));tube(species+'_Stem',[T((0,0,0)),T(tip*.45+Vector((-.015*scale,0,.005*scale))),T(tip)],.004*scale)
  if species in ['Rosemary','Thyme']:
   front=(math.sin(angle+.8),.12,math.cos(angle+.8));leaf(species+'_ShapedSprig',T(tip*.06),T(tip),(.16 if species=='Rosemary' else .23)*scale,2 if species=='Rosemary' else 4,front,dry)
  else:
   for level in [0.28,.56]:
    for side in [-1,1]:
     a=tip*level;theta=angle+side*1.2+level*2;length=(.17 if species=='Sage' else .11)*scale;b=a+Vector((math.cos(theta)*length,(.10 if species=='Sage' else .055)*scale,math.sin(theta)*length));leaf(species+'_Leaf',T(a),T(b),(.12 if species=='Sage' else .029)*scale,7 if dry and species=='Sage' else 1,(-math.sin(theta),.3,math.cos(theta)),dry)
   if species in ['Lavender','Chamomile']:
    length=(.16 if species=='Lavender' else .115)*scale;leaf(species+'_Flower',T(tip-Vector((0,length*.6,0))),T(tip+Vector((.012*scale,length*.4,0))),(.07 if species=='Lavender' else .13)*scale,6 if dry else (3 if species=='Lavender' else 5),(math.sin(angle),.2,math.cos(angle)),dry)

# Containers: closed hollow vessels, separate soil; base-centre pivots.
def lathe(n,profile,role='Clay',sides=16):
 vs=[]
 for y,r in profile:
  for i in range(sides):
   a=i*math.tau/sides;rr=r*(1+.013*math.sin(i*2.1)+.008*math.sin(i*.7));vs.append((math.cos(a)*rr,y,math.sin(a)*rr))
 fs=[tuple(range(sides-1,-1,-1)),tuple(range(len(vs)-sides,len(vs)))]+[(j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i) for j in range(len(profile)-1) for i in range(sides)];return obj(n,vs,fs,role)
for suffix,diam,h in [('Small',.32,.32),('Medium',.47,.46),('Large',.64,.62)]:
 module('Pot_'+suffix,'Container','Hollow hand-shaped terracotta; plant root socket at soil surface.',h*.84,[{'name':'PlantRoot','position':[0,h*.84,0]}]);r=diam/2
 lathe('HollowTerracotta',[(0,r*.59),(.035*h,r*.66),(.73*h,r*.93),(.84*h,r*.93),(.87*h,r*1.025),(h,r*1.025),(h,r*.88),(.84*h,r*.84),(.17*h,r*.55)])
 lathe('RecessedSoil',[(h*.81,r*.82),(h*.84,r*.82)],'Soil',16)
module('WoodBucket','Container','Open hollow walnut bucket, two restrained hoops.',.32,[{'name':'PlantRoot','position':[0,.32,0]}]);lathe('OpenWoodenContainer',[(0,.14),(.02,.15),(.37,.205),(.40,.205),(.40,.181),(.08,.125)],'Timber',12)
for y,r in [(.075,.163),(.33,.203)]:lathe('TimberHoop',[(y-.012,r),(y+.012,r),(y+.012,r-.012),(y-.012,r-.012)],'Twine',12)
lathe('Soil',[(.30,.165),(.32,.165)],'Soil',12)
for suffix,w,d,h in [('HerbTray',.65,.38,.24),('WindowBox_1p76m',1.76,.38,.30),('WindowBox_2p10m',2.10,.39,.28)]:
 module(suffix,'Container','Independent walnut window box or herb tray; soil/root socket at top interior.',h*.80,[{'name':'PlantRoot','position':[0,h*.80,0]},{'name':'WallMount','position':[0,h*.45,-d/2]}]);box('Bottom',(0,.025,0),(w-.07,.05,d-.03));box('Front',(0,h/2,d/2-.025),(w,h,.05));box('Back',(0,h/2,-d/2+.025),(w,h,.05))
 for x in [-w/2+.025,w/2-.025]:box('End',(x,h/2,0),(.05,h,d-.10))
 box('Soil',(0,h*.78,0),(w-.11,.025,d-.11),'Soil')
 for x in [-w*.32,w*.32]:box('BoxAttachmentBackCleat',(x,h*.35,-d/2-.018),(.065,h*.50,.04))
for species in ['Lavender','Sage','Rosemary','Thyme','Chamomile']:
 for version in ['A','B']:
  module('Plant_'+species+'_'+version,'Plant','Root pivot; shaped bent individual foliage, no crossed whole-plant planes.');plant(species,scale=1 if version=='A' else .88,seed=2 if version=='A' else 7)
for suffix,w in [('Small',1.55),('Paired',1.91)]:
 for style in ['Flowering','Greenery']:
  module('WindowInsert_'+style+'_'+suffix,'Plant','Centred root datum; fits existing approved window-box soil footprints without replacing architecture.')
  for j in range(9):plant((['Chamomile','Lavender','Thyme','Sage','Lavender'] if style=='Flowering' else ['Thyme','Sage','Rosemary','Sage','Thyme'])[j%5],((j-4)*w/9,0,.065*math.sin(j*2)),.71 if j%2==0 else .76,seed=j+4)
  for side in [-1,1]:
   root=Vector((side*w*.29,0,.14));crest=root+Vector((side*.025,.11,.11));end=root+Vector((side*.08,-.34,.17));tube('TrailingBoxStem',[root,crest,end],.006)
   for k in range(7):
    a=crest.lerp(end,(k+.25)/7);b=a+Vector(((-1 if k%2 else 1)*.08,-.09,.012));leaf('TrailingBoxIvy',a,b,.13,0,(0,.12,1))

def vine(name,points,count,width=.15,corner=False):
 points=[Vector(p) for p in points];tube(name+'_Stem',points,.008)
 for j in range(count):
  t=(j+.3)/count*(len(points)-1);i=min(len(points)-2,int(t));p=points[i].lerp(points[i+1],t-i);side=-1 if j%2 else 1;end=p+Vector((side*width*.66,-.11,.015*math.sin(j)));normal=(0,.12,1) if not corner or j%3 else (1,.12,0);leaf(name+'_IvyLeaf',p,end,width*(.75+.22*math.sin(j*1.7)**2),0,normal)
for suffix,pts,count,width in [('Wall_A',[(0,0,.025),(.12,.45,.04),(-.10,.9,.05),(.09,1.4,.03)],18,.22),('Wall_B',[(0,0,.03),(-.18,.35,.08),(.02,.80,.03),(-.22,1.28,.06)],16,.20),('Corner90',[(0,0,.04),(.10,.5,.07),(.01,.9,.12),(.06,1.45,.04)],18,.21),('BeamDrape',[(-.65,0,.04),(-.25,-.16,.06),(.25,-.10,.04),(.68,-.35,.09)],16,.18),('Trailing',[(0,0,0),(.12,-.33,.08),(-.08,-.7,.12),(.10,-1.03,.14)],14,.16)]:
 module('Ivy_'+suffix,'Vine','Mount datum follows stem start, +Z stand-off; asymmetric shaped ivy leaves.',sockets=[{'name':'Mount','position':[0,0,0]},{'name':'End','position':pts[-1]}]);vine(suffix,pts,count,width,suffix=='Corner90')
for species in ['Lavender','Rosemary','Sage','Mixed']:
 module('Hanging_'+species,'Hanging','Top rope socket; hangs downward. Dried foliage separately tinted; no collider.',sockets=[{'name':'Hang','position':[0,0,0]}]);tube('HangingLoop',[(0,0,0),(-.028,-.05,0),(0,-.11,0),(.028,-.05,0),(0,0,0)],.006,'Twine',6)
 for j,sp in enumerate([species,species] if species!='Mixed' else ['Lavender','Rosemary','Sage']):plant(sp,((j-.5)*.055 if species!='Mixed' else (j-1)*.025,-.095,.022*math.sin(j*2)),.76 if species!='Mixed' else .60,seed=j+9,dry=True,down=True)
 tube('Binding', [(-.06,-.17,-.025),(.06,-.18,-.025),(.06,-.18,.025),(-.06,-.17,.025),(-.06,-.17,-.025)],.008,'Twine',5)
for suffix,species,positions in [('HerbBed_A',['Lavender','Sage','Thyme','Rosemary'],[(-.29,0,-.18),(.26,0,-.1),(-.25,0,.22),(.25,0,.23)]),('HerbBed_B',['Chamomile','Thyme','Sage','Lavender'],[(-.26,0,-.23),(.25,0,-.15),(-.20,0,.19),(.24,0,.23)]),('FlowerBorder',['Chamomile','Thyme','Lavender'],[(-.40,0,0),(0,0,.07),(.4,0,-.02)]),('Groundcover',['Thyme','Thyme','Thyme'],[(-.19,0,-.12),(.16,0,-.08),(0,0,.17)])]:
 module('Garden_'+suffix,'Garden','Soil-level pivot; patch remains within existing beds, never adds physics.')
 for j,(sp,p) in enumerate(zip(species,positions)):plant(sp,p,.65 if suffix!='Groundcover' else .52,seed=j+11)
# Validate source; leaf strips are intentionally open single surfaces, all opaque pieces closed solids.
report={'modules':len(modules),'parts':[],'foliageTopology':'Bent silhouette-cut open surfaces; double-sided alpha clip in Unity, not closed volumes.','spriteRegions':regions,'atlasSize':[W,H]};dims={}
for o in parts:
 me=o.data;me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();deg=sum(t.area<1e-12 for t in me.loop_triangles)
 if deg or (o['solid'] and (bad or vol<=0)):raise RuntimeError((o.name,bad,vol,deg))
 uv=me.uv_layers[0];uvbad=0
 for t in me.loop_triangles:
  a,b,c=[uv.data[i].uv for i in t.loops];uvbad+=abs((b-a).cross(c-a))<1e-13
 # Opaque cap UVs need face-planar projections when the long-axis trim projection collapses.
 if uvbad and o['solid']:
  for face in me.polygons:
   ids=list(face.loop_indices);pts=[me.vertices[me.loops[i].vertex_index].co for i in ids];n=face.normal;drop=max(range(3),key=lambda i:abs(n[i]));axes=[i for i in range(3) if i!=drop]
   for li,p in zip(ids,pts):uv.data[li].uv=(max(.53,min(.97,.75+.07*p[axes[0]])),max(.53,min(.97,.61+.07*p[axes[1]]))) if o['role']=='Timber' else (.18+.1*p[axes[0]],.60+.1*p[axes[1]])
 uvbad=sum(abs((uv.data[t.loops[1]].uv-uv.data[t.loops[0]].uv).cross(uv.data[t.loops[2]].uv-uv.data[t.loops[0]].uv))<1e-13 for t in me.loop_triangles)
 if uvbad:raise RuntimeError(('UV',o.name,uvbad))
 if not all(0<=p.uv.x<=1 and 0<=p.uv.y<=1 for p in uv.data):raise RuntimeError(('UV bounds',o.name))
 report['parts'].append({'name':o.name,'module':o['module'],'triangles':len(me.loop_triangles),'solid':bool(o['solid']),'nonmanifoldEdges':bad,'degenerateTriangles':deg,'degenerateUVs':uvbad})
for idx,(name,meta) in enumerate(modules.items()):
 col=bpy.data.collections.new(name);s.collection.children.link(col);loc=Vector((idx%7*2.6,idx//7*-2.5,0))
 for o in [p for p in parts if p['module']==name]:s.collection.objects.unlink(o);col.objects.link(o);o.location=loc
 for sock in meta['sockets']:e=bpy.data.objects.new('Socket_'+sock['name'],None);col.objects.link(e);e.location=Vector(P(sock['position']))+loc;e.empty_display_type='ARROWS';e.empty_display_size=.08
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CM_BotanicalPlanterKit01.blend'))
for name,meta in modules.items():
 selected=[p for p in parts if p['module']==name];pts=[(v.co.x,v.co.z,v.co.y) for o in selected for v in o.data.vertices];dims[name]={'min':[min(p[i] for p in pts) for i in range(3)],'max':[max(p[i] for p in pts) for i in range(3)]};meta['lods']=[]
 for lod in range(2 if meta['kind']!='Container' else 1):
  bpy.ops.object.select_all(action='DESELECT');exports=[]
  for role in sorted(set(o['role'] for o in selected)):
   copies=[]
   for o in selected:
    if o['role']!=role or (lod==1 and o.get('leaf') and not o.get('lod_keep')):continue
    c=o.copy();c.data=o.data.copy();s.collection.objects.link(c);c.location=(0,0,0);c.select_set(True);copies.append(c)
   if not copies:continue
   bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();joined=bpy.context.object;joined.name=name+'_'+role;joined.data.materials.clear();joined.data.materials.append(mats[role])
   for face in joined.data.polygons:face.material_index=0
   joined.select_set(False);exports.append(joined)
  for o in exports:o.select_set(True)
  bpy.context.view_layer.update()
  for o in exports:o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
  bpy.context.view_layer.objects.active=exports[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
  fn=name+('_Reduced' if lod else '')
  bpy.ops.export_scene.fbx(filepath=str(ASSET/'Models'/f'{fn}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
  tris=0
  for o in exports:o.data.calc_loop_triangles();tris+=len(o.data.loop_triangles);bpy.data.objects.remove(o,do_unlink=True)
  meta['lods'].append({'file':fn+'.fbx','triangles':tris})
(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(OUT/'ModuleCatalog.json').write_text(json.dumps(list(modules.values()),indent=2));(OUT/'SourceDimensions.json').write_text(json.dumps(dims,indent=2));print('BOTANICAL_READY',len(modules),len(parts),sum(x['lods'][0]['triangles'] for x in modules.values()))
