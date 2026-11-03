"""Repair only candidate roof end clipping; retain all body groups."""
import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Vector,Matrix
H=Path(__file__).parent;R=H.parents[4];FLOOR=.12
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_ElderCottage01.blend'));bpy.context.preferences.filepaths.save_version=0
s=bpy.context.scene;P=Matrix(((-1,0,0),(0,0,-1),(0,1,0)));mats={m.name:m for m in bpy.data.materials};src={m['name']:m for m in json.loads((R/'ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json').read_text())};helper=(R/'ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py').read_text();exec(compile(helper[helper.index('groups={};collisions=[]'):helper.index('# Main stable:')],str(H/'roof_helpers.py'),'exec'))
for name in ['RoofDeck','Shingles']:bpy.data.objects.remove(bpy.data.objects['BW_ElderCottage01_'+name],do_unlink=True)
def patch(name,corners,rows,cols,clips=()):
 # Each patch is planar in x,z, with y carried by its four corners.
 A,B,C,D=map(Vector,corners)
 def pt(u,t):return A.lerp(B,u).lerp(D.lerp(C,u),t)
 def clip(poly,fn):
  out=[]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   fa,fb=fn(a[0]),fn(b[0]);ia,ib=fa>=0,fb>=0
   if ia:out.append(a)
   if ia!=ib:
    t=fa/(fa-fb);out.append((a[0].lerp(b[0],t),a[1].lerp(b[1],t)))
  return out
 def clipped(points,uv):
  poly=list(zip(points,map(Vector,uv)))
  for fn in clips:poly=clip(poly,fn)
  return poly
 deck=clipped([pt(0,0),pt(1,0),pt(1,1),pt(0,1)],[(0,0),(1,0),(1,1),(0,1)])
 if len(deck)>=3:
  V=[tuple(p-Vector((0,d,0))) for d in [.04,.17] for p,u in deck];n=len(deck);F=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];create(name+' deck',V,F,[tuple(u) for d in [0,1] for p,u in deck],['interior_roof'],[0]*len(F),'RoofDeck',True)
 V=[];F=[];UV=[]
 for row in range(rows):
  t0=max(0,(row-.18)/rows);t1=(row+1)/rows
  for col in range(cols):
   u0=col/cols;u1=(col+1)/cols;idx=(col*3+row*5)%8;uv=[((idx%4+.06+.88*u)/4,(idx//4+.06+.88*t)/2) for u,t in [(0,0),(1,0),(1,1),(0,1)]];points=[pt(u0,t0),pt(u1,t0),pt(u1,t1),pt(u0,t1)]
   for j,p in enumerate(points):p.y+=.012+(rows-row)*.002+.007*math.sin(col*1.7+row*.9)+(j//2)*.012
   poly=clipped(points,uv)
   if len(poly)<3:continue
   k=len(V);V.extend(tuple(p) for p,u in poly);UV.extend(tuple(u) for p,u in poly);F.append(tuple(range(k,len(V))))
   # Thin lower lips carry the overlap at gameplay distance.
   p0,u0v=poly[-2];p1,u1v=poly[-1];k=len(V);V.extend([tuple(p0),tuple(p1),tuple(p1-Vector((0,.013,0))),tuple(p0-Vector((0,.013,0)))]);UV.extend([tuple(u0v),tuple(u1v),tuple(u1v),tuple(u0v)]);F.append((k,k+1,k+2,k+3))
 o=create(name+' laid shingles',V,F,UV,['Shingle'],[0]*len(F),'Shingles');bm=bmesh.new();bm.from_mesh(o.data)
 for f in bm.faces:
  if f.normal.z<0:bmesh.ops.reverse_faces(bm,faces=[f])
 bm.to_mesh(o.data);bm.free()
# Half-hipped main roof. Clipped ends, rather than a full cottage gable or tall pyramid.
for side in [-1,1]:
 end=.5+side*3.35
 clips=[lambda p,side=side:3.8+(side*(p.x-.5))/1.05*1.1-p.z,lambda p,side=side:p.z+2.8+(side*(p.x-.5))/1.05*1.1]
 patch('Main half hip',[(.5,5.85,-3.9),(.5,5.85,4.9),(end,3.10,4.9),(end,3.10,-3.9)],10,27,clips)
# Small end hips have a broad lower edge and a narrow ridge meeting.
for front in [True,False]:
 ztip=3.8 if front else -2.8;zbase=4.9 if front else -3.9
 # Rectangular plane clipped to a triangle, with the same layered shingles.
 patch('Clipped end roof',[(-.55,5.85,ztip),(1.55,5.85,ztip),(1.55,4.988,zbase),(-.55,4.988,zbase)],4,7,[lambda p,ztip=ztip,zbase=zbase:1.05*(p.z-ztip)/(zbase-ztip)-(p.x-.5),lambda p,ztip=ztip,zbase=zbase:1.05*(p.z-ztip)/(zbase-ztip)+(p.x-.5)])
patch('Lower service roof',[(-2.3,3.10,-2.05),(-2.3,3.10,3.45),(-4.3,2.49,3.45),(-4.3,2.49,-2.05)],5,17)
patch('Sheltered stoop', [(-1.3,2.96,4.4),(1.3,2.96,4.4),(1.3,2.65,5.82),(-1.3,2.65,5.82)],4,8)
# Ridge cap only; no decorative trusswork.
for side in [-1,1]:
 V=[(.5,5.92,-2.82),(.5,5.92,3.82),(.5+side*.15,5.80,3.82),(.5+side*.15,5.80,-2.82)];create('Ridge cover',V,[(0,1,2,3)],[(.03,.03),(.22,.03),(.22,.42),(.03,.42)],['Shingle'],[0],'Shingles')
# Export a small family of grouped meshes. Every visible element sits on the raised dry-store datum.
cat=[]
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 if len(objects)>1:bpy.ops.object.join()
 o=bpy.context.object;o.name='BW_ElderCottage01_'+group;o.data.name=o.name
 for v in o.data.vertices:v.co.z+=FLOOR
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<1e-8],context='FACES');bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o.data.calc_loop_triangles();order=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)];path='Assets/BlightBloom/Art/Architecture/Briarwick/ElderCottage01/Models/'+o.name+'.fbx'
 bpy.ops.export_scene.fbx(filepath=str(R/path),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
 cat.append({'group':group,'name':o.name,'assetPath':path,'triangles':len(o.data.loop_triangles),'materialOrder':order})
old=json.loads((H/'ModelCatalog.json').read_text());new={r['group']:r for r in cat};old['models']=[new.get(r['group'],r) for r in old['models']];(H/'ModelCatalog.json').write_text(json.dumps(old,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_ElderCottage01.blend'))
