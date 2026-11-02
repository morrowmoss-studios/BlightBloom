"""Bakery01: package-soft timber/plaster plus bespoke hipped pan-and-cover clay roof.
Reuses established native-mesh UV/export helpers without regenerating previous assets.
"""
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4]
helper=R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py'
code=helper.read_text().split('# Main stable:')[0].replace('StableA02OpenFront','Bakery01').replace('BW_StableA02OpenFront.blend','BW_Bakery01.blend')
exec(compile(code,str(helper),'exec'))
# Additional material, wholly project-owned; original package materials stay untouched.
m=bpy.data.materials.new('Clay');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.94
n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures/BW_Bakery01_Clay_BaseColor.png'));n.image.pack();m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats['Clay']=m
# Concrete here is the imported package's soft cream plaster, not modern exposed concrete.
d=src['wall_wood_1m_2.014'];candidates=[]
for si,ts in enumerate(d['submeshes']):
 if d['materials'][si]!='concrete':continue
 for k in range(0,len(ts),3):
  ids=ts[k:k+3];v=[Vector(d['vertices'][j]) for j in ids];normal=(v[1]-v[0]).cross(v[2]-v[0])
  if normal.length>1e-6 and abs(normal.normalized().z)>.95:candidates.append((normal.length,ids,v))
_,ids,v=max(candidates,key=lambda x:x[0]);M=Matrix([(p.x,p.y,1) for p in v]);u=M.inverted()@Vector([d['uv'][j][0] for j in ids]);w=M.inverted()@Vector([d['uv'][j][1] for j in ids]);templates['concrete']=(u,w,min(p.x for p in v),max(p.x for p in v),min(p.y for p in v),max(p.y for p in v))
# Outer wall rings with genuine openings. Main shell 6.6 x 7.4; frontage +Z.
def wall(name,a,b,lo,hi,z,side=False):
 if b-a<.01 or hi-lo<.01:return
 box(name,(z,(lo+hi)/2,(a+b)/2) if side else ((a+b)/2,(lo+hi)/2,z),(.22,hi-lo,b-a) if side else (b-a,hi-lo,.22),'concrete','Plaster',.009)
def wallholes(name,a,b,z,holes,side=False):
 cuts=sorted(set([a,b]+[v for h in holes for v in h[:2]]))
 for i in range(len(cuts)-1):
  l,r=cuts[i:i+2];mid=(l+r)/2;hit=next((h for h in holes if h[0]<mid<h[1]),None)
  if hit:
   wall(name+' sill',l,r,0,hit[2],z,side);wall(name+' head',l,r,hit[3],3.12,z,side)
  else:wall(name,l,r,0,3.12,z,side)
front=4.5;rear=-2.9
wallholes('Front',-3.3,3.3,front,[(-1.6,-.2,0,2.4),(.85,2.45,1.05,2.18),(-2.85,-2.15,1.25,2.18)])
wallholes('Rear',-3.3,3.3,rear,[(-2.45,-1.15,0,2.3),(.9,2.5,.15,3.12)]) # oven masonry occupies this rear-wall opening
wallholes('West',rear,front,-3.3,[(-1.2,.1,1.2,2.2)],True)
wallholes('East',rear,front,3.3,[(.5,1.8,1.2,2.2)],True)
# Simple footed native posts and soft timber framing, no ornate cottage gables.
for x in [-3.3,3.3]:
 for z in [rear,front]:native('wooden_post_column_size1.079','Corner_post',lambda v,x=x,z=z:(v.x*.82+x,v.y*3.18/3.4059584,v.z*.82+z),'Timber')
for z in [rear,front]:
 box('Wall_plate',(0,3.06,z),(6.75,.22,.23),'wood2','Timber',.008)
 for a,b in [(-3.3,-1.7),(-.1,3.3)] if z==front else [(-3.3,-2.55),(-1.05,3.3)]:box('Sill',((a+b)/2,.17,z),(b-a,.17,.23),'wood2','Timber',.006)
for x in [-3.3,3.3]:
 box('Side_plate',(x,3.06,.8),(.23,.22,7.6),'wood2','Timber',.008)
 box('Side_sill',(x,.17,.8),(.23,.17,7.4),'wood2','Timber',.005)
 for z in [-.9,1.4]:box('Side_post',(x,1.57,z),(.17,2.95,.18),'wood2','Timber',.004)
# Window assemblies: modest translucent-looking glass, inset reveals, mullions, sill.
def window(name,c,w,h,side=False):
 x,y,z=c
 box(name+' glazing',c,(.045,h,w) if side else (w,h,.045),'glass','Windows',.003)
 for xx in [-w/2,w/2]:box(name+' jamb',(x,y,z+xx) if side else (x+xx,y,z),(.18,h+.20,.13) if side else (.13,h+.20,.18),'wood2','Windows',.005)
 for yy in [-h/2,h/2]:box(name+' rail',(x,y+yy,z),(.18,.13,w+.26) if side else (w+.26,.13,.18),'wood2','Windows',.005)
 box(name+' mullion',c,(.08,h,.055) if side else (.055,h,.08),'wood2','Windows',.002)
 box(name+' cross',(x,y+.02,z),(.08,.045,w) if side else (w,.045,.08),'wood2','Windows',.002)
 box(name+' sill',(x,y-h/2-.09,z),(.34,.12,w+.32) if side else (w+.32,.12,.34),'wood2','Windows',.006)
window('Shop twinlight',(1.65,1.615,4.48),1.6,1.13)
window('Small frontage light',(-2.5,1.715,4.48),.7,.93)
window('West workroom',(-3.29,1.7,-.55),1.3,1,True);window('East light',(3.29,1.7,1.15),1.3,1,True)
# Distinct customer and service frames; static closed native leaves are separate meshes.
for name,cx,z,width,height in [('Customer',-.9,4.5,1.4,2.4),('Service',-1.8,-2.9,1.3,2.3)]:
 for x in [cx-width/2-.075,cx+width/2+.075]:box(name+' jamb',(x,height/2,z),(.15,height,.25),'wood2','Timber',.007)
 box(name+' lintel',(cx,height+.105,z),(width+.48,.21,.29),'wood2','Timber',.009)
 native('wall_wood_door1.004',name+' door',lambda v,cx=cx,z=z,w=width,h=height:(cx+(v.x-.3612678)/.72605136*(w-.04),v.y/1.83421123*(h-.035)+.015,v.z+z+(-.07 if z>0 else .07)),name+'Door')
# Native rough stone oven/chimney, facing outward at the rear; source UV detail retained.
native('chimney_outside_size1.001','Oven_and_masonry_chimney',lambda v:(v.x+1.7,v.y-.025,-v.z-2.75),'Oven',flip=True)
# Stone perimeter has true door breaks. Original stone mesh/UVs reused.
def stone(name,pos,size):native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),'Foundation')
for a,b in [(-3.3,-1.61),(-.19,3.3)]:stone('Front plinth',((a+b)/2,-.10,4.5),(b-a,.36,.28))
for a,b in [(-3.3,-2.46),(-1.14,3.3)]:stone('Rear plinth',((a+b)/2,-.10,-2.9),(b-a,.36,.28))
for x in [-3.3,3.3]:stone('Side plinth',(x,-.10,.8),(.28,.36,7.4))
stone('Customer flush threshold',(-.9,-.025,4.55),(1.4,.07,.48));stone('Service flush threshold',(-1.8,-.025,-2.95),(1.3,.07,.48))
# No interior: only shallow threshold standing surfaces behind static leaves.
box('Customer vestibule',(-.9,-.055,4.1),(1.4,.11,.8),'floor','Thresholds',0)
box('Service threshold',(-1.8,-.055,-2.6),(1.3,.11,.6),'floor','Thresholds',0)
# Hipped roof underlay: simple closed plaster/wood shelter volume, avoids open gables.
V=[(-3.75,3.1,-3.32),(3.75,3.1,-3.32),(3.75,3.1,4.95),(-3.75,3.1,4.95),(0,4.68,-1.65),(0,4.68,3.1)]
create('Hipped_roof_deck',V,[(0,4,5,3),(4,1,2,5),(0,1,4),(3,5,2),(0,3,2,1)],[(0,0),(1,0),(1,1),(0,1),(.4,.3),(.4,.7)],['interior_roof'],[0]*5,'RoofDeck',True,.01)
# Curved overlapping pan-and-cover tiles. Clay hue comes from eight low-contrast painted swatches.
def tile(name,A,B,C,D,idx,cap=False):
 # Quad ordered along a course: upper left/right then lower right/left.
 n=6 if cap else 4;V=[];UV=[]
 normal=(B-A).cross(D-A).normalized()
 if normal.y<0:normal=-normal
 for row in [0,1]:
  for j in range(n+1):
   u=j/n;top=A.lerp(B,u);bottom=D.lerp(C,u);p=top.lerp(bottom,row)
   bulge=(math.sin(u*math.pi)*.048 if cap else -.019*math.sin(u*math.pi))+.028
   V.append(tuple(p+normal*bulge));UV.append(((idx%4+.07+.86*u)/4,(idx//4+.05+.9*row)/2))
 F=[]
 for j in range(n):F.append((j,j+1,n+2+j,n+1+j))
 o=create(name,V,F,UV,['Clay'],[0]*len(F),'ClayRoof');
 for p in o.data.polygons:p.use_smooth=True
 # Solid undersides matter at eaves and ridges; modest 16 mm thickness.
 mod=o.modifiers.new('Baked clay tile thickness','SOLIDIFY');mod.thickness=.016;mod.offset=-1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
def patch(name,A,B,C,D,rows,cols):
 A,B,C,D=map(Vector,[A,B,C,D])
 for row in range(rows):
  v0=max(0,(row-.12)/rows);v1=min(1,(row+1.0)/rows)
  L0=A.lerp(D,v0);R0=B.lerp(C,v0);L1=A.lerp(D,v1);R1=B.lerp(C,v1)
  for col in range(cols):
   u0=col/cols;u1=(col+1)/cols;idx=(col*3+row*5+(1 if name=='east' else 0))%8
   a=L0.lerp(R0,u0);b=L0.lerp(R0,u1);c=L1.lerp(R1,u1);d=L1.lerp(R1,u0)
   if (b-a).length<.025 and (c-d).length<.025:continue
   # chimney occupies rear plane; keep normal seated overlaps at its penetration.
   cen=(a+b+c+d)/4
   if .98<cen.x<2.42 and -3.5<cen.z<-2.55:continue
   tile(name+' pan',a,b,c,d,idx)
   # A narrow convex cover at each seam gives clay construction rather than flat shingles.
   if col<cols-1:
    half=.16/cols;aa=L0.lerp(R0,u1-half);bb=L0.lerp(R0,u1+half);cc=L1.lerp(R1,u1+half);dd=L1.lerp(R1,u1-half);tile(name+' cover',aa,bb,cc,dd,idx,True)
patch('west',(0,4.68,-1.65),(0,4.68,3.1),(-3.75,3.1,4.95),(-3.75,3.1,-3.32),10,29)
patch('east',(0,4.68,3.1),(0,4.68,-1.65),(3.75,3.1,-3.32),(3.75,3.1,4.95),10,29)
patch('front',(0,4.68,3.1),(0,4.68,3.1),(3.75,3.1,4.95),(-3.75,3.1,4.95),6,26)
patch('rear',(0,4.68,-1.65),(0,4.68,-1.65),(-3.75,3.1,-3.32),(3.75,3.1,-3.32),6,26)
# Ridge/hip capping follows real roof seams, no ornamental crest.
for name,a,b in [('ridge',(0,4.70,-1.65),(0,4.70,3.1)),('hip1',(0,4.70,3.1),(-3.75,3.12,4.95)),('hip2',(0,4.70,3.1),(3.75,3.12,4.95)),('hip3',(0,4.70,-1.65),(-3.75,3.12,-3.32)),('hip4',(0,4.70,-1.65),(3.75,3.12,-3.32))]:
 a,b=Vector(a),Vector(b);vec=b-a;side=vec.cross(Vector((0,1,0))).normalized()*.105;count=math.ceil(vec.length/.38)
 for j in range(count):
  p=a.lerp(b,max(0,(j-.12)/count));q=a.lerp(b,(j+1)/count);tile(name,p-side,p+side,q+side,q-side,j%8,True)
# Plain verges/eaves, no patterned fascia.
for x in [-3.65,3.65]:box('Eave fascia',(x,3.06,.815),(.14,.16,8.22),'wood2','Timber',.006)
for z in [-3.24,4.87]:box('Hip eave',(0,3.06,z),(7.3,.16,.14),'wood2','Timber',.006)
# Keep one reusable mesh per role group and export with established conversion.
catalog=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_Bakery01_'+group;o.data.name=o.name
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.calc_loop_triangles()
 order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
 path='Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 catalog.append({'name':o.name,'group':group,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Bakery01.blend'));(H/'ModelCatalog.json').write_text(json.dumps({'mainFootprint':[6.6,7.4],'roofFootprint':[7.5,8.27],'height':6.4694,'ridgeHeight':4.76,'frontDoor':[1.4,2.4],'serviceDoor':[1.3,2.3],'models':catalog},indent=2));print('BAKERY_READY',sum(m['triangles'] for m in catalog))
