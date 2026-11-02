"""A03: preserve A02's shelter, replace roof covering only, add restrained joinery.
Read-only A02 source -> new editable source; no regeneration of unchanged FBXs.
Low roof pitch is an explicit historical compromise, documented in the review.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];A=R/'Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Models'
if (H/'BW_StableA03Rural.blend').exists() and '--refine-own' not in sys.argv:raise RuntimeError('Inspect existing A03 source before rebuilding')
bpy.ops.wm.open_mainfile(filepath=str(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/BW_StableA02OpenFront.blend'))
bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)))
# Preserve the old roof geometry as a hidden, clearly labelled reference in this new source.
old=bpy.data.objects['BW_StableA02_Roofs'];ref=old.copy();ref.data=old.data.copy();col=bpy.data.collections.new('REFERENCE_A02_WoodRoof_NOT_EXPORTED');s.collection.children.link(col);col.objects.link(ref);col.hide_render=True;col.hide_viewport=True
old.name='BW_StableA03_RoofUnderstructure';old.data.name=old.name
bm=bmesh.new();bm.from_mesh(old.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if old.data.materials[f.material_index].name=='roof'],context='FACES');bm.to_mesh(old.data);bm.free()
# Existing ceiling, fascia and structural ridge pieces remain beneath the new coat.
m=bpy.data.materials.new('Thatch');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.91
for kind,file in [('Base Color','BW_StableA03_Thatch_BaseColor.png'),('Normal','BW_StableA03_Thatch_Normal.png')]:
 im=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures'/file));im.pack();n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=im
 if kind=='Base Color':m.node_tree.links.new(n.outputs['Color'],bs.inputs['Base Color'])
 else:
  im.colorspace_settings.name='Non-Color';nm=m.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.30;m.node_tree.links.new(n.outputs['Color'],nm.inputs['Color']);m.node_tree.links.new(nm.outputs['Normal'],bs.inputs['Normal'])
parts=[];joinery=[]
def mesh(name,V,F,UV,material,bevel=0,group=None,face_uv=None):
 me=bpy.data.meshes.new(name);me.from_pydata([P@Vector(v) for v in V],[],F);me.update();me.materials.append(material);uv=me.uv_layers.new(name='UVMap')
 for face in me.polygons:
  for j,li in enumerate(face.loop_indices):uv.data[li].uv=face_uv[face.index][j] if face_uv else UV[me.loops[li].vertex_index]
 o=bpy.data.objects.new(name,me);s.collection.objects.link(o);bpy.context.view_layer.objects.active=o
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 if bevel:
  mod=o.modifiers.new('Soft dressed edges','BEVEL');mod.width=bevel;mod.segments=2;mod.limit_method='ANGLE';mod.angle_limit=.7;bpy.ops.object.modifier_apply(modifier=mod.name)
 for f in o.data.polygons:f.use_smooth=True
 me.set_sharp_from_angle(angle=.9)
 (parts if group is None else group).append(o);return o
def coat_field(x,t):return .265+.014*math.sin(x*1.37)+.008*math.sin(x*3.27-t*2.7)
def mainpoint(u,t,side):
 x=-4.50+9*u;edge=(4.04 if side>0 else 3.03)+.018*math.sin(x*2.2)+.009*math.sin(x*5.1+.7)
 z=side*t*edge;y=4.78-1.74*t+.012*math.sin(t*math.pi)+.010*math.sin(x*1.8+t*3)*math.sin(t*math.pi)
 return x,y,z
def solid_grid(name,nx,ny,point,thickness,uvmap):
 V=[];UV=[]
 for bottom in [False,True]:
  for j in range(ny+1):
   for i in range(nx+1):
    u=i/nx;v=j/ny;x,y,z=point(u,v);d=thickness(u,v)
    V.append((x,y+(0 if bottom else d),z));UV.append(uvmap(u,v,bottom))
 w=nx+1;N=w*(ny+1);F=[];FU=[]
 for j in range(ny):
  for i in range(nx):
   k=j*w+i
   for face in [(k,k+1,k+w+1,k+w),(N+k+w,N+k+w+1,N+k+1,N+k)]:F.append(face);FU.append([UV[a] for a in face])
 boundary=list(range(w))+[j*w+nx for j in range(1,ny+1)]+[ny*w+i for i in range(nx-1,-1,-1)]+[j*w for j in range(ny-1,0,-1)]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):
  F.append((a,b,N+b,N+a));ua,ub=Vector(UV[a]),Vector(UV[b]);d=(ub-ua).normalized();off=Vector((-d.y,d.x))*.018;FU.append([tuple(ua),tuple(ub),tuple(ub+off),tuple(ua+off)])
 return mesh(name,V,F,UV,m,.035,face_uv=FU)
# Each whole slope samples one continuous painting region; there are no repeated strips.
for side,name,rows in [(1,'Main_front_coat',12),(-1,'Main_rear_coat',9)]:
 solid_grid(name,26,rows,lambda u,v,side=side:mainpoint(u,v,side),lambda u,v:coat_field(-4.5+9*u,v),lambda u,v,b,side=side:(.025+.95*u,(.51+.46*(1-v)) if side>0 else (.025+.45*(1-v))))
# Plain folded ridge, not a decorative scroll/crest. It seats into the main coats.
def ridgepoint(u,v):
 x=-4.54+9.08*u;z=(v-.5)*1.30;slope=(1.74/4.04 if z>=0 else 1.74/3.03);smooth=math.sqrt(z*z+.08*.08)-.08
 y=4.78+coat_field(x,0)+.085-slope*smooth-.145
 return x,y,z
solid_grid('Plain_renewed_ridge',26,6,ridgepoint,lambda u,v:.145,lambda u,v,b:(.025+.95*u,.18+.64*v))
# The tack roof remains a lower, modest lean-to; its head is lapped into the gable.
def leanpoint(u,v):
 z=-2.40+4.80*u;x=4.10+2.94*v+.012*math.sin(u*13)*v;y=3.22-.82*v+.010*math.sin(u*8+v*2)
 return x,y,z
solid_grid('Tack_room_coat',14,10,leanpoint,lambda u,v:.23+.012*math.sin(u*10+v*2),lambda u,v,b:(.07+.61*u,.03+.45*(1-v)))
# A few pegs and a small local post-repair cleat; existing beams stay unchanged.
wood=bpy.data.materials['wood2']
def rod(name,a,b,radius=.012):
 aa,bb=Vector(a),Vector(b);axis=(bb-aa).normalized();up=Vector((0,1,0)) if abs(axis.y)<.9 else Vector((1,0,0));u=axis.cross(up).normalized()*radius;v=axis.cross(u).normalized()*radius;V=[];UV=[];n=6
 for layer,end in enumerate([aa,bb]):
  for i in range(n):
   angle=i*2*math.pi/n;V.append(tuple(end+u*math.cos(angle)+v*math.sin(angle)));UV.append((.495+.005*math.cos(angle),.40+.006*math.sin(angle)+layer*.014))
 F=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh(name,V,F,UV,wood,0,joinery)
for x in [-4.2,-1.4,1.4,4.2]:
 for dx in [-.055,.055]:rod('Through_peg',(x+dx,3.35,2.806),(x+dx,3.35,2.85),.013)
# A scarf repair uses a thin fitted wooden cleat touching the corner post, with two pegs.
V=[(-4.31,.38,2.846),(-4.09,.38,2.846),(-4.09,.92,2.846),(-4.31,.88,2.846),(-4.31,.38,2.872),(-4.09,.38,2.872),(-4.09,.92,2.872),(-4.31,.88,2.872)]
F=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];UV=[(.49+(i%2)*.012,.34+(i//2%2)*.05) for i in range(8)]
mesh('Maintained_post_repair',V,F,UV,wood,.004,joinery,face_uv=[[(.49,.34),(.51,.34),(.51,.40),(.49,.40)]]*6)
for y in [.46,.80]:rod('Repair_peg',(-4.20,y,2.864),(-4.20,y,2.894),.010)
# Sparse split-hazel fixings on the renewed ridge. No metal netting or ornamental pattern.
for i in range(8):
 x=-3.95+i*1.12+.025*math.sin(i*2.1);last=None
 for j in range(5):
  z=-.45+j*.225;slope=(1.74/4.04 if z>=0 else 1.74/3.03);y=4.78+coat_field(x,0)+.085-slope*(math.sqrt(z*z+.0064)-.08)+.004
  p=(x,y,z)
  if last:rod('Hazel_ridge_spar',last,p,.008)
  last=p
def combine(objs,name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0]
 if len(objs)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name=name;o.data.name=name
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY');bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free()
 return o
thatch=combine(parts,'BW_StableA03_Thatch');detail=combine(joinery,'BW_StableA03_Joinery')
exports=[old,thatch,detail];rows=[]
for o in exports:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;o.data.calc_loop_triangles()
 if '--texture-fit' not in sys.argv or o!=old:
  bpy.ops.export_scene.fbx(filepath=str(A/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 rows.append({'name':o.name,'group':o.name.replace('BW_StableA03_',''),'assetPath':str((A/(o.name+'.fbx')).relative_to(R)),'triangles':len(o.data.loop_triangles),'materialOrder':[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)],'placement':{'position':[0,0,0],'yaw':0}})
prior=json.loads((R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/ModelCatalog.json').read_text());prior['models']=[r for r in prior['models'] if r['group']!='Roofs']+rows
prior['thatchThicknessMetres']=[.23,.29];prior['nominalRoofPeakMetres']=5.15;prior['roofPitchHistoricalCompromise']='Existing broad low profile retained; shallower than durable traditional thatch practice.'
(H/'ModelCatalog.json').write_text(json.dumps(prior,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_StableA03Rural.blend'))
print('A03_THATCH_READY',[(r['group'],r['triangles']) for r in rows],sum(r['triangles'] for r in prior['models']))
