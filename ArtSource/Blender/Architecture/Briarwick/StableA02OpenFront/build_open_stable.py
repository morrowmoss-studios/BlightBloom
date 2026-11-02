"""Briarwick Stable A open-front Review02. Native package maps are read-only.
Open-front three-bay shelter, side-entry tack room, deeper front cover.
Uses established metric Blender -> FBX -> Unity conversion; no texture repainting.
"""
import bpy,bmesh,json,math,sys
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4]
assert (R/'AGENTS.md').exists()
A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/StableA02OpenFront/Models'
if (H/'BW_StableA02OpenFront.blend').exists() and '--refine-own' not in sys.argv:raise RuntimeError('Inspect existing stable source before regeneration')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())}
roles=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMaterials.json').read_text());mats={}
for role in roles:
 name=role['name'];mat=bpy.data.materials.new(name);mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.83
 path=next(t['path'] for t in role['textures'] if t['property']=='_BaseMap');n=mat.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(R/path),check_existing=True);n.image.pack();mat.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color']);mats[name]=mat
mat=bpy.data.materials.new('PackedEarth_Routes');mat.diffuse_color=(.26,.22,.16,1);mats['PackedEarth_Routes']=mat
groups={};collisions=[]
def create(name,V,F,UV,materials,slot,group,closed=False,bevel=0,face_uv=None):
 me=bpy.data.meshes.new(name);me.from_pydata([P@Vector(v) for v in V],[],F);me.update();uv=me.uv_layers.new(name='UVMap')
 for role in materials:me.materials.append(mats[role])
 for p,idx in zip(me.polygons,slot):
  p.material_index=idx
  for j,li in enumerate(p.loop_indices):uv.data[li].uv=face_uv[p.index][j] if face_uv else UV[me.loops[li].vertex_index]
 o=bpy.data.objects.new(name,me);s.collection.objects.link(o);bpy.context.view_layer.objects.active=o
 if closed:
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if bevel:
  mod=o.modifiers.new('Small softened board edges','BEVEL');mod.width=bevel;mod.segments=1;mod.limit_method='ANGLE';mod.angle_limit=.65;bpy.ops.object.modifier_apply(modifier=mod.name)
 if closed:
  for p in me.polygons:p.use_smooth=True
  me.set_sharp_from_angle(angle=.65);wn=o.modifiers.new('Soft weighted timber normals','WEIGHTED_NORMAL');wn.keep_sharp=True;bpy.ops.object.modifier_apply(modifier=wn.name)
 groups.setdefault(group,[]).append(o);return o
def native(key,name,fn,group,flip=False,select=None):
 d=src[key];F=[];slots=[]
 for i,ts in enumerate(d['submeshes']):
  for k in range(0,len(ts),3):
   f=ts[k:k+3]
   if select and not select(d['materials'][i],[d['vertices'][j] for j in f]):continue
   # Native Unity triangle normals must survive the handedness reflection P.
   F.append(f if flip else f[::-1]);slots.append(i)
 return create(name,[fn(Vector(v)) for v in d['vertices']],F,d['uv'],d['materials'],slots,group)
# Select real long timber UV faces rather than sampling arbitrary atlas rectangles.
templates={}
for role,key in [('wood2','wooden_post_column_size1.079'),('wood3','wall_wood_1m_2.014')]:
 d=src[key];best=None
 for i,ts in enumerate(d['submeshes']):
  if d['materials'][i]!=role:continue
  for k in range(0,len(ts),3):
   ids=ts[k:k+3];v=[Vector(d['vertices'][j]) for j in ids];n=(v[1]-v[0]).cross(v[2]-v[0]);ys=[p.y for p in v];xs=[p.x for p in v]
   if n.length<1e-8 or abs(n.normalized().z)<.9 or max(ys)-min(ys)<2:continue
   if best is None or n.length>best[0]:best=(n.length,ids,v)
 assert best,role
 _,ids,v=best;M=Matrix([(p.x,p.y,1) for p in v]);u=M.inverted()@Vector([d['uv'][j][0] for j in ids]);w=M.inverted()@Vector([d['uv'][j][1] for j in ids]);templates[role]=(u,w,min(p.x for p in v),max(p.x for p in v),min(p.y for p in v),max(p.y for p in v))
def timberUV(x,y,w,h,role,variation=0):
 u,v,x0,x1,y0,y1=templates[role];xx=(x/w+.5)*.85*(x1-x0)+x0+.075*(x1-x0);yy=y0+(y/max(h,.001))*.94*(y1-y0)+.02*(y1-y0)+variation*.015
 p=Vector((xx,yy,1));return (u.dot(p),v.dot(p))
def box(name,pos,size,role='wood2',group='Structure',bevel=.003,yaw=0):
 w,h,d=size;V=[];UV=[];local=[];rot=Matrix.Rotation(math.radians(yaw),3,'Y')
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]:
  q=Vector((x*w/2,y*h/2,z*d/2));local.append(q);V.append(tuple(Vector(pos)+rot@q));UV.append(timberUV(q.x,q.y+h/2,w,h,role if role in templates else 'wood2'))
 F=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 grain=max(range(3),key=lambda i:size[i]);face_uv=[]
 for face in F:
  n=(local[face[1]]-local[face[0]]).cross(local[face[2]]-local[face[0]]);normal=max(range(3),key=lambda i:abs(n[i]));va=grain if grain!=normal else next(i for i in range(3) if i!=normal);ua=next(i for i in range(3) if i not in [normal,va]);face_uv.append([timberUV(local[j][ua],local[j][va]+size[va]/2,size[ua],size[va],role if role in templates else 'wood2') for j in face])
 return create(name,V,F,UV,[role],[0]*6,group,closed=True,bevel=bevel,face_uv=face_uv)
def board(name,centre,width,low,high,axis='front',group='Shell',variation=0):
 # Physical plank thickness and a very small bow; irregularity stays millimetric.
 h=high-low
 if h<.04:return
 o=box(name,(centre[0],low+h/2,centre[1]),(width,h,.045),'wood3',group,.0015,yaw=90 if axis=='side' else 0)
def boardrun(prefix,a,b,height,fixed,axis='front',low=.15,group='Shell',holes=()):
 count=max(1,round((b-a)/.235));step=(b-a)/count
 for i in range(count):
  c=a+(i+.5)*step;h=height(c) if callable(height) else height;segments=[(low,h)]
  for h0,h1,y0,y1 in holes:
   if c+step/2>h0+.002 and c-step/2<h1-.002:
    new=[]
    for l,t in segments:
     if y0>l:new.append((l,min(t,y0)))
     if y1<t:new.append((max(l,y1),t))
    segments=new
  for j,(l,t) in enumerate(segments):board(prefix+f'_{i:02}_{j}',(fixed,c) if axis=='side' else (c,fixed),step-.004,l,t,axis,group,(i%5-2)*.25)
# Main stable: 8.4 x 5.4 m, three front-facing stall bays.
boardrun('Rear_board',-4.2,4.2,3.16,-2.7)
gable=lambda z:4.61-abs(z)*(.574 if z<0 else .43)
boardrun('West_gable',-2.7,2.7,gable,-4.2,'side',holes=[(-.64,.64,3.4,4.22)])
boardrun('East_gable',-2.7,2.7,gable,4.2,'side',holes=[(.3,1.8,0,2.3)])
# Tack lean-to, recessed front and lower eaves.
tackheight=lambda x:3.13-(x-4.2)*.28
boardrun('Tack_front',4.2,6.5,tackheight,2.1)
boardrun('Tack_rear',4.2,6.5,tackheight,-2.1)
boardrun('Tack_end',-2.1,2.1,2.486,6.5,'side',holes=[(-.66,.66,0,2.30)])
# Native carved/footed posts keep the package's weathered construction language.
for i,(x,z,height) in enumerate([(-4.2,-2.7,3.18),(0,-2.7,3.18),(4.2,-2.7,3.18),(-4.2,2.7,3.47),(-1.4,2.7,3.47),(1.4,2.7,3.47),(4.2,2.7,3.47),(6.5,2.1,2.52),(6.5,-2.1,2.52),(4.2,2.1,3.18)]):
 native('wooden_post_column_size1.079','Pegged_post_'+str(i),lambda v,x=x,z=z,h=height:(v.x+x,v.y*h/3.4059584,v.z+z),'Structure')
box('Rear_wall_plate',(0,3.03,-2.7),(8.7,.26,.23))
box('Open_front_bearing_beam',(0,3.36,2.7),(8.7,.26,.23))
for z in [-.75,.75]:box('Side_service_jamb',(6.52,1.22,z),(.18,2.44,.20))
box('Side_service_lintel',(6.52,2.40,0),(.20,.20,1.70))
box('Connecting_portal_head',(4.20,2.42,1.05),(.20,.24,1.7))
for z in [.20,1.90]:box('Connecting_portal_post',(4.20,1.2,z),(.20,2.40,.20))
for z in [-2.7,2.7]:box('Low_sill',(0,.16,z),(8.4,.18,.16)) if z<0 else None
box('West_sill',(-4.2,.16,0),(.16,.18,5.4));box('East_rear_sill',(4.2,.16,-1.2),(.16,.18,3));box('East_front_sill',(4.2,.16,2.25),(.16,.18,.9))
for a,b in [(-2.1,-.65),(.65,2.1)]:box('Tack_side_sill',(6.5,.16,(a+b)/2),(.16,.18,b-a))
box('Tack_rear_sill',(5.35,.16,-2.1),(2.3,.18,.16))
box('Tack_front_sill',(5.35,.16,2.1),(2.3,.18,.16))
# A few integrated diagonal braces, not decorative overlays.
for x in [-3.8,-1.4,1.4,3.8]:
 a=Vector((x,2.76,2.75));b=Vector((x+(.45 if x<0 else -.45),3.27,2.75));mid=(a+b)/2;delta=b-a
 # Create in world coordinates using a closed rectangular prism between endpoints.
 u=Vector((delta.y,-delta.x,0)).normalized()*.055;v=Vector((0,0,.055));V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];UV=[timberUV((j%4-1.5)*.03,(j//4)*delta.length,.12,delta.length,'wood2') for j in range(8)]
 create('Mortised_brace',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],UV,['wood2'],[0]*6,'Structure',True,.002)
# Continuous native roof sections: no invented slate material or repainting.
for i,x in enumerate([-3.3,-1.1,1.1,3.3]):
 native('roof_wide2_3.001','Main_roof_'+str(i),lambda v,x=x:(v.x*1.1+x,3.06+v.y*.76,v.z*(1.8 if v.z>0 else 1.35)),'Roofs')
for i,z in enumerate([-1.15,1.15]):
 native('roof_wide2_3.001','Lean_to_roof_'+str(i),lambda v,z=z:(4.0+v.z*1.35,2.48+(v.y-.2021)*(.72/2.044),v.x*1.15+z),'Roofs',flip=True,select=lambda role,V:all(p[2]>=-.001 for p in V) and sum(p[2] for p in V)/3>.01)
# Gable verges and loft hatch framing follow the existing roof profile.
for z in [-2.30,2.30]:
 a=Vector((4.19,3.10,z));b=Vector((6.95,2.34,z));delta=b-a;u=Vector((delta.y,-delta.x,0)).normalized()*.09;v=Vector((0,0,.07));V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];UV=[timberUV((j%4-1.5)*.04,(j//4)*delta.length,.16,delta.length,'wood2') for j in range(8)]
 create('Lean_to_edge_board',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],UV,['wood2'],[0]*6,'Structure',True,.002)
for x in [-4.35,4.35]:
 for sign in [-1,1]:
  a=Vector((x,3.10,sign*(3.90 if sign>0 else 2.90)));b=Vector((x,4.82,0));delta=b-a;u=Vector((.07,0,0));v=delta.cross(u).normalized()*.075;V=[tuple(p+su*u+sv*v) for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]];UV=[timberUV((j%4-1.5)*.04,(j//4)*delta.length,.16,delta.length,'wood2') for j in range(8)]
  create('Gable_verge',V,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],UV,['wood2'],[0]*6,'Structure',True,.002)
for z in [-.72,.72]:box('Loft_jamb',(-4.24,3.81,z),(.17,.94,.16))
for y in [3.34,4.29]:box('Loft_rail',(-4.24,y,0),(.18,.15,1.60))
# Closed loft loading hatch, no loose hay or clutter.
for i in range(5):board('Loft_hatch_board_'+str(i),(-4.30,-.52+i*.26),.25,3.43,4.17,'side','LoftHatch')
# Floor and low stone returns; all portals are free of a stone upstand.
box('Main_packed_earth',(0,-.055,0),(8.4,.11,5.4),'PackedEarth_Routes','Floor',0)
box('Tack_floor',(5.35,-.055,0),(2.30,.11,4.2),'PackedEarth_Routes','Floor',0)
def stone(name,pos,size):
 native('floor_rock_2x3m.001',name,lambda v:(pos[0]+v.x/3*size[0],pos[1]+(v.y/.338265836-.5)*size[1],pos[2]+v.z/2*size[2]),'Foundation')
stone('Rear_plinth',(0,-.10,-2.7),(8.4,.40,.23))
for x in [-4.2,-1.4,1.4,4.2]:stone('Front_post_pad',(x,-.04,2.7),(.38,.28,.38))
stone('West_plinth',(-4.2,-.10,0),(.24,.40,5.4));stone('East_plinth',(4.2,-.10,-1.2),(.24,.40,3))
stone('East_front_return',(4.2,-.10,2.25),(.24,.40,.9));stone('Tack_rear_plinth',(5.35,-.10,-2.1),(2.3,.40,.24))
stone('Tack_front_return',(5.35,-.10,2.1),(2.3,.40,.24))
for a,b in [(-2.1,-.65),(.65,2.1)]:stone('Tack_side_return',(6.5,-.10,(a+b)/2),(.24,.40,b-a))
stone('Side_human_flush_threshold',(6.53,-.025,0),(.36,.07,1.30))
# Three front-facing bays, low kickboards and rails; no gates across the frontage.
for x in [-1.4,1.4]:
 for z in [-2.5,1.2]:box('Stall_post',(x,.70,z),(.16,1.4,.16),group='Partitions')
 for y in [.75,1.15]:box('Stall_rail',(x,y,-.65),(.10,.12,3.7),group='Partitions')
 boardrun('Stall_kickboards',-2.5,1.2,.62,x,'side',low=.12,group='Partitions')
# No horse/front doors. The sole service door is on the outer tack-room side.
door_specs=[('HumanDoor',1.27,2.27,True,(6.60,.02,.635),165)]
door_meta={}
for name,w,h,mirror,pos,yaw in door_specs:
 o=native('wall_wood_door1.004',name,lambda v,w=w,h=h,mirror=mirror:((v.x+.00175786018)/.72605136*w*(-1 if mirror else 1),v.y/1.83421123*h,v.z),name,flip=mirror)
 door_meta[name]={'position':list(pos),'yaw':yaw,'width':w,'height':h}
catalog=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_StableA02_'+group;o.data.name=o.name
 # Explicit triangles prevent importer ambiguity on bevel caps.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free()
 o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
 reused={'Floor','LoftHatch','HumanDoor'}
 asset_path=('Assets/BlightBloom/Art/Architecture/Briarwick/StableA01/Models/BW_StableA01_'+group+'.fbx') if group in reused else ('Assets/BlightBloom/Art/Architecture/Briarwick/StableA02OpenFront/Models/'+o.name+'.fbx')
 if group not in reused:
  bpy.ops.export_scene.fbx(filepath=str(R/asset_path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 catalog.append({'name':o.name,'group':group,'assetPath':asset_path,'triangles':len(o.data.loop_triangles),'materialOrder':order,'placement':door_meta.get(group,{'position':[0,0,0],'yaw':0})})
 if group in door_meta:o.location=P@Vector(door_meta[group]['position']);o.rotation_euler.z=math.radians(-door_meta[group]['yaw'])
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_StableA02OpenFront.blend'))
(H/'ModelCatalog.json').write_text(json.dumps({'mainFootprint':[8.4,5.4],'totalFootprint':[10.7,5.4],'ridgeHeight':4.875,'openBayNominalWidth':2.8,'frontOverhang':1.26,'frontBearingBeamClearHeight':3.23,'humanOpening':[1.3,2.3],'horseReferenceEnvelope':[1.2,2.6,2.8],'models':catalog},indent=2))
print('OPEN_STABLE_READY',len(catalog),sum(m['triangles'] for m in catalog))
