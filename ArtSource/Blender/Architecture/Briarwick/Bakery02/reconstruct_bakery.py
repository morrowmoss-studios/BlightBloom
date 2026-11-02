"""Bakery02 scoped architectural correction. Reads Bakery01; writes only Bakery02.
Retains native door/window/foundation groups, replaces wall/roof, internalizes oven.
"""
import bpy,bmesh,json,math
from mathutils import Vector,Matrix
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models'
if (H/'BW_Bakery02.blend').exists():raise RuntimeError('Existing Bakery02: inspect before regenerating')
bpy.ops.wm.open_mainfile(filepath=str(R/'ArtSource/Blender/Architecture/Briarwick/Bakery01/BW_Bakery01.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};mats={m.name:m for m in bpy.data.materials};groups={}
# Reuse only helper definitions and native timber UV templates; no old builder execution.
helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'helpers_from_A02.py'),'exec'))
for name in ['Plaster','RoofDeck','ClayRoof']:
 bpy.data.objects.remove(bpy.data.objects['BW_Bakery01_'+name],do_unlink=True)
# Preserve body timber except old hip-roof fascia islands outside the wall plates.
o=bpy.data.objects['BW_Bakery01_Timber'];bm=bmesh.new();bm.from_mesh(o.data);remaining=set(bm.verts)
while remaining:
 start=next(iter(remaining));component={start};stack=[start];remaining.remove(start)
 while stack:
  for edge in stack.pop().link_edges:
   v=edge.other_vert(edge.verts[0]) if False else None
   for v in edge.verts:
    if v in remaining:remaining.remove(v);component.add(v);stack.append(v)
 pts=[P.inverted()@v.co for v in component];centre=sum(pts,Vector())/len(pts)
 if abs(centre.x)>3.5 or centre.z>4.7 or centre.z<-3.1:bmesh.ops.delete(bm,geom=list(component),context='VERTS')
bm.to_mesh(o.data);bm.free();o.name='BW_Bakery02_Timber';groups['Timber']=[o]
# Move and turn the whole chamber into the building. Old rear wall opening is removed below.
o=bpy.data.objects['BW_Bakery01_Oven']
for v in o.data.vertices:
 q=P.inverted()@v.co;q=Vector((q.x-.45,q.y,-4.15-q.z));v.co=P@q
o.data.update();o.name='BW_Bakery02_InternalOven';groups['InternalOven']=[o]
# Dedicated subdued plaster, no old baked framework shadows.
m=bpy.data.materials.new('Plaster02');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.95;n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Textures/BW_Bakery02_Plaster_BaseColor.png'));n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats['Plaster02']=m
# Continuous closed wall surfaces, no seams between infill rectangles.
def wall(name,a,b,fixed,holes,side=False,index=0):
 xs=sorted(set([a,b]+[v for h in holes for v in h[:2]]));ys=sorted(set([0,3.12]+[v for h in holes for v in h[2:]]));cells={}
 for i in range(len(xs)-1):
  for j in range(len(ys)-1):
   x=(xs[i]+xs[i+1])/2;y=(ys[j]+ys[j+1])/2
   if not any(h[0]<x<h[1] and h[2]<y<h[3] for h in holes):cells[i,j]=True
 V=[];F=[];UV=[]
 def face(coords):
  start=len(V)
  for x,y,d in coords:V.append((fixed+d,y,x) if side else (x,y,fixed+d));UV.append(((index%2+.06+.88*(x-a)/(b-a))/2,(index//2+.06+.88*y/5.7)/2))
  F.append(tuple(range(start,len(V))))
 for i,j in cells:
  x0,x1=xs[i:i+2];y0,y1=ys[j:j+2]
  for d in [-.11,.11]:face([(x0,y0,d),(x1,y0,d),(x1,y1,d),(x0,y1,d)])
  if (i-1,j) not in cells:face([(x0,y0,-.11),(x0,y0,.11),(x0,y1,.11),(x0,y1,-.11)])
  if (i+1,j) not in cells:face([(x1,y0,-.11),(x1,y1,-.11),(x1,y1,.11),(x1,y0,.11)])
  if (i,j-1) not in cells:face([(x0,y0,-.11),(x1,y0,-.11),(x1,y0,.11),(x0,y0,.11)])
  if (i,j+1) not in cells:face([(x0,y1,-.11),(x0,y1,.11),(x1,y1,.11),(x1,y1,-.11)])
 o=create(name,V,F,UV,['Plaster02'],[0]*len(F),'Plaster')
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
wall('Front continuous infill',-3.3,3.3,4.5,[(-1.6,-.2,0,2.4),(.85,2.45,1.05,2.18),(-2.85,-2.15,1.25,2.18)],index=0)
wall('Rear restored masonry wall',-3.3,3.3,-2.9,[(-2.45,-1.15,0,2.3)],index=1)
wall('West infill',-2.9,4.5,-3.3,[(-1.2,.1,1.2,2.2)],True,2)
wall('East infill',-2.9,4.5,3.3,[(.5,1.8,1.2,2.2)],True,3)
# Ridge offset subtly toward the customer side; low eaves retained, useful loft volume above.
ridge=-.35;peak=5.58
for z,index in [(4.5,0),(-2.9,1)]:
 V=[(-3.3,3.12,z-.11),(3.3,3.12,z-.11),(ridge,peak-.12,z-.11),(-3.3,3.12,z+.11),(3.3,3.12,z+.11),(ridge,peak-.12,z+.11)]
 UV=[((index+.06+.88*(x+3.3)/6.6)/2,(.06+.88*y/5.7)/2) for x,y,z0 in V]
 create('Gable infill',V,[(0,2,1),(3,4,5),(0,3,5,2),(2,5,4,1),(0,1,4,3)],UV,['Plaster02'],[0]*5,'Plaster',True)
 # Modest king-post construction, with slightly shaped supported verges.
 box('Gable king post',(ridge,4.27,z),(.15,2.35,.19),'wood2','Timber',.004)
 for left in [True,False]:
  a=Vector((-3.63 if left else 3.63,3.06,z+.03));b=Vector((ridge,peak-.01,z+.03));delta=b-a;u=Vector((delta.y,-delta.x,0)).normalized()*.085;v=Vector((0,0,.10));V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]]
  create('Gable verge',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],[timberUV((j%4-1.5)*.055,(j//4)*delta.length,.17,delta.length,'wood2') for j in range(8)],['wood2'],[0]*6,'Timber',True,.003)
for x in [-3.65,3.65]:box('Side eave fascia',(x,3.06,.8),(.14,.17,8.15),'wood2','Timber',.004)
# Tile/deck hole sits inside the masonry shaft silhouette, preventing visible roof intrusions.
rect=(.72,1.78,-1.31,-.68)
def clip(poly,axis,value,keepLess):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=a[0][axis]-value;db=b[0][axis]-value;ia=da<=0 if keepLess else da>=0;ib=db<=0 if keepLess else db>=0
  if ia:out.append(a)
  if ia!=ib:
   t=da/(da-db);out.append((a[0].lerp(b[0],t),a[1].lerp(b[1],t)))
 return out
planes=[(0,rect[0],False),(0,rect[1],True),(2,rect[2],False),(2,rect[3],True)]
def outside(poly):
 pieces=[];remaining=poly
 for axis,value,less in planes:
  part=clip(remaining,axis,value,not less)
  if len(part)>2:pieces.append(part)
  remaining=clip(remaining,axis,value,less)
  if not remaining:break
 return pieces
RV=[];RF=[];RU=[]
def addface(coords,uvs):
 for poly in outside(list(zip(map(Vector,coords),map(Vector,uvs)))):
  start=len(RV);RV.extend(tuple(p) for p,u in poly);RU.extend(tuple(u) for p,u in poly);RF.append(tuple(range(start,len(RV))))
def point(x,z):
 y=peak-(peak-3.13)*(abs(x-ridge)/(3.72+ridge if x<ridge else 3.72-ridge));y+=.016*math.sin(z*.8)+.008*math.sin(x*2+z)
 return Vector((x,y,z))
# Closed roof underdeck (upper/bottom faces clipped at the shaft).
DV=[];DF=[];DU=[]
for end in [-3.72,3.72]:
 pts=[point(ridge,-3.25),point(ridge,4.87),point(end,4.87),point(end,-3.25)]
 for shift in [0,-.13]:
  poly=[p+Vector((0,shift,0)) for p in pts]
  for piece in outside([(p,Vector((i%2,i//2))) for i,p in enumerate(poly)]):
   k=len(DV);DV.extend(tuple(p) for p,u in piece);DU.extend(tuple(u) for p,u in piece);DF.append(tuple(range(k,len(DV))))
 for a,b in zip(pts,pts[1:]+pts[:1]):
  k=len(DV);DV.extend([tuple(a),tuple(b),tuple(b-Vector((0,.13,0))),tuple(a-Vector((0,.13,0)))]);DU.extend([(0,0),(1,0),(1,1),(0,1)]);DF.append(tuple(range(k,k+4)))
create('Roof deck',DV,DF,DU,['interior_roof'],[0]*len(DF),'RoofDeck')
# Fewer, fuller tiles than 01; millimetric lap/width changes avoid stamping identical strips.
for slope,end in enumerate([-3.72,3.72]):
 rows=12;cols=27
 for row in range(rows):
  v0=max(0,(row-.18)/rows);v1=(row+1)/rows
  for col in range(cols):
   z0=-3.25+8.12*(col/cols)+(.018*math.sin(col*1.7+row*.6) if col else 0);z1=-3.25+8.12*((col+1)/cols)+(.018*math.sin((col+1)*1.7+row*.6) if col<cols-1 else 0)
   x0=ridge+(end-ridge)*v0;x1=ridge+(end-ridge)*v1;idx=(col*3+row*5+slope*2)%8
   for cap in [False,True]:
    n=4 if cap else 3;a=z0 if not cap else z1-.042;b=z1 if not cap else z1+.042
    if cap and col==cols-1:continue
    verts=[];uv=[]
    for t,x in [(0,x0),(1,x1)]:
     for j in range(n+1):
      u=j/n;z=a+(b-a)*u;p=point(x,z);p.y+=.022+(rows-row)*.002+(.058*math.sin(u*math.pi) if cap else -.017*math.sin(u*math.pi));p.y+=.004*math.sin(row+col*.7)
      verts.append(p);uv.append(Vector(((idx%4+.07+.86*u)/4,(idx//4+.05+.90*t)/2)))
    for j in range(n):
     ids=[j,j+1,n+2+j,n+1+j];addface([verts[i] for i in ids],[uv[i] for i in ids])
     # Only the visible tile nose receives thickness; hidden tile bottoms are omitted.
     ids=[n+1+j,n+2+j];top=[verts[i] for i in ids];bottom=[p-Vector((0,.018,0)) for p in top];uv0=[uv[i] for i in ids];addface(top+bottom[::-1],uv0+[u+Vector((0,-.008)) for u in uv0[::-1]])
# Plain rounded overlapping ridge caps, no oversized crest.
for col in range(24):
 z0=-3.26+col*8.14/24;z1=z0+8.14/24+.045;verts=[];uv=[]
 for t,z in [(0,z0),(1,z1)]:
  for j in range(7):
   angle=math.pi*j/6;x=ridge+.14*math.cos(angle);y=peak+.035+.11*math.sin(angle)+.016*math.sin(z*.8);verts.append(Vector((x,y,z)));uv.append(Vector((((col%4)+.06+.88*j/6)/4,((col%2)+.05+.9*t)/2)))
 for j in range(6):addface([verts[i] for i in [j,j+1,8+j,7+j]],[uv[i] for i in [j,j+1,8+j,7+j]])
o=create('Soft laid clay tile courses',RV,RF,RU,['Clay'],[0]*len(RF),'ClayRoof')
for p in o.data.polygons:p.use_smooth=True
# Retain source data/UVs and separate leaves for unchanged groups; export only changed meshes.
oldcat=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/Bakery01/ModelCatalog.json').read_text());catalog=[]
for row in oldcat['models']:
 if row['group'] in ['Plaster','Timber','RoofDeck','ClayRoof','Oven']:continue
 o=bpy.data.objects[row['name']];o.name=row['name'].replace('Bakery01','Bakery02');catalog.append(row)
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Bakery02_'+group;o.data.name=o.name
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free()
 if group=='Plaster':
  for p in o.data.polygons:p.use_smooth=False
 o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 catalog.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery02.blend'));(H/'ModelCatalog.json').write_text(json.dumps({'mainFootprint':[6.6,7.4],'ridgeHeight':peak+.16,'height':6.4694,'frontDoor':[1.4,2.4],'serviceDoor':[1.3,2.3],'ovenChamberInside':True,'roofPenetrationInnerBoundary':rect,'models':catalog},indent=2));print('BAKERY02_READY',sum(m['triangles'] for m in catalog))
