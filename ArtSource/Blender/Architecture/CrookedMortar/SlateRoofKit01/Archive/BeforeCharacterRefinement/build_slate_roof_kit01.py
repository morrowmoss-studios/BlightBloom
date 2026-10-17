"""CM_SlateRoofKit01. Measured upper-envelope roof fit, reusable grid panels, approved paint."""
import bpy,bmesh,math,json,sys,shutil
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent;ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/SlateRoofKit01'
if not bpy.app.background:raise RuntimeError('Background only')
if (OUT/'CM_SlateRoofKit01.blend').exists() and '--refine-own-kit' not in sys.argv:raise RuntimeError('Refusing existing output')
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;bpy.context.preferences.filepaths.save_version=0
source=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png';texture=ASSET/'Textures/CM_SlateRoofKit01_ApprovedPaintSheet.png';shutil.copyfile(source,texture);paint=bpy.data.images.load(str(source));paint.colorspace_settings.name='sRGB';paint.pack();mats={}
for key in ['Slate','Walnut']:
 m=bpy.data.materials.new('CM_Roof_'+key);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=1;bs.inputs['Metallic'].default_value=0;im=n.new('ShaderNodeTexImage');im.image=paint;m.node_tree.links.new(im.outputs['Color'],bs.inputs['Base Color']);m.node_tree.links.new(bs.outputs[0],out.inputs[0]);mats[key]=m
EPS=1e-7

def area(poly):return sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))*.5

def clean(poly):
 out=[]
 for p in poly:
  if not out or math.dist(p,out[-1])>1e-7:out.append(tuple(p))
 if len(out)>1 and math.dist(out[0],out[-1])<1e-7:out.pop()
 changed=True
 while changed and len(out)>3:
  changed=False
  for i in range(len(out)):
   a=out[i-1];b=out[i];c=out[(i+1)%len(out)];cross=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
   if abs(cross)<1e-8 or math.dist(a,b)<1e-6:out.pop(i);changed=True;break
 if len(out)<3 or abs(area(out))<1e-9:return []
 if area(out)<0:out.reverse()
 return out

def clip(poly,a,b,c):
 if not poly:return []
 result=[];prev=poly[-1];dp=a*prev[0]+b*prev[1]+c
 for cur in poly:
  dc=a*cur[0]+b*cur[1]+c
  if (dc>=-EPS)!=(dp>=-EPS):
   t=dp/(dp-dc);result.append((prev[0]+t*(cur[0]-prev[0]),prev[1]+t*(cur[1]-prev[1])))
  if dc>=-EPS:result.append(cur)
  prev=cur;dp=dc
 return clean(result)

def intersect(poly,other):
 for q,r in zip(other,other[1:]+other[:1]):poly=clip(poly,-(r[1]-q[1]),r[0]-q[0],(r[1]-q[1])*q[0]-(r[0]-q[0])*q[1])
 return poly

def difference(poly,other):
 # Disjoint convex fragments partition A minus convex B.
 remaining=poly;result=[]
 for q,r in zip(other,other[1:]+other[:1]):
  a=-(r[1]-q[1]);b=r[0]-q[0];c=-a*q[0]-b*q[1]
  outside=clip(remaining,-a,-b,-c)
  if outside:result.append(outside)
  remaining=clip(remaining,a,b,c)
  if not remaining:break
 return result

def contains(poly,x,z,tol=1e-5):return all((r[0]-q[0])*(z-q[1])-(r[1]-q[1])*(x-q[0])>=-tol for q,r in zip(poly,poly[1:]+poly[:1]))

def overlap(a,b):return not(max(p[0] for p in a)<min(p[0] for p in b)-EPS or max(p[0] for p in b)<min(p[0] for p in a)-EPS or max(p[1] for p in a)<min(p[1] for p in b)-EPS or max(p[1] for p in b)<min(p[1] for p in a)-EPS)

raw=json.loads((OUT/'ApprovedRoofMeasurement.json').read_text());roofs=raw['roofs'];obstacle=json.loads((OUT/'ApprovedChimneyGeometry.json').read_text());tris=[]
for r in roofs+[obstacle]:
 for ids in r['topTriangles']:
  pts=[Vector(r['vertices'][i]) for i in ids];n=(pts[1]-pts[0]).cross(pts[2]-pts[0]).normalized()
  if abs(n.y)<.06:continue
  poly=clean([(p.x,p.z) for p in pts])
  if not poly:continue
  A=-n.x/n.y;B=-n.z/n.y;C=pts[0].y-A*pts[0].x-B*pts[0].z
  tris.append(dict(name=r['name'],poly=poly,plane=(A,B,C),normal=n,index=len(tris)))
def height(t,x,z):a,b,c=t['plane'];return a*x+b*z+c

def top_at(x,z,include_chimney=False):
 candidates=[(height(t,x,z),t) for t in tris if (include_chimney or t['name']!='Chimney') and contains(t['poly'],x,z)]
 return max(candidates,key=lambda q:q[0]) if candidates else None

visible=[]
for t in tris:
 if t['name']=='Chimney':continue
 polys=[t['poly']]
 for other in tris:
  if other is t or not overlap(t['poly'],other['poly']):continue
  delta=[other['plane'][i]-t['plane'][i] for i in range(3)]
  if max(abs(x) for x in delta)<1e-6:
   if other['index']>t['index']:continue
   removal=other['poly']
  else:removal=clip(other['poly'],delta[0],delta[1],delta[2]-1e-5)
  if not removal:continue
  new=[]
  for p in polys:new+=difference(p,removal) if overlap(p,removal) else [p]
  polys=new
  if not polys:break
 for p in polys:
  if abs(area(p))>1e-7:visible.append(dict(tri=t,poly=p))
# Locate visible roof junctions and same-roof creases using exact clipped boundaries.
segments={}
for patch in visible:
 t=patch['tri'];p=patch['poly']
 for q,r in zip(p,p[1:]+p[:1]):
  if math.dist(q,r)<.07:continue
  x,z=(q[0]+r[0])/2,(q[1]+r[1])/2
  for other in tris:
   if other is t or other['name']=='Chimney' or t['normal'].dot(other['normal'])>.99027:continue
   if not contains(other['poly'],x,z,.00002) or abs(height(t,x,z)-height(other,x,z))>.0001:continue
   direction=Vector((r[0]-q[0],0,r[1]-q[1])).normalized();perp=Vector((-direction.z,0,direction.x));g1=Vector((t['plane'][0],0,t['plane'][1])).dot(perp);g2=Vector((other['plane'][0],0,other['plane'][1])).dot(perp)
   crosssamples=[top_at(x+perp.x*k,z+perp.z*k) for k in [-.025,.025]]
   crest=sum(v[0] if v else height(t,x,z) for v in crosssamples)/2-height(t,x,z)
   role='Valley' if t['name']!=other['name'] or (g1*g2<-.001 and crest>.001) else ('Ridge' if g1*g2<-.001 else 'PitchTransition')
   a3=Vector((q[0],height(t,*q),q[1]));b3=Vector((r[0],height(t,*r),r[1]));key=(role,tuple(sorted([tuple(round(v,4) for v in a3),tuple(round(v,4) for v in b3)])))
   segments[key]=dict(a=a3,b=b3,role=role,roofA=t['name'],roofB=other['name'])
# Exact plane-plane valleys between distinct roof volumes; clip intervals against all higher carriers.
for ti,t in enumerate(tris):
 if t['name']=='Chimney':continue
 for other in tris[ti+1:]:
  if other['name']=='Chimney' or other['name']==t['name'] or not overlap(t['poly'],other['poly']):continue
  region=intersect(t['poly'],other['poly'])
  if not region:continue
  da,db,dc=[t['plane'][i]-other['plane'][i] for i in range(3)]
  if math.hypot(da,db)<1e-5:continue
  hits=[]
  for q,r in zip(region,region[1:]+region[:1]):
   fq=da*q[0]+db*q[1]+dc;fr=da*r[0]+db*r[1]+dc
   if abs(fq)<1e-5:hits.append(q)
   if fq*fr<0:
    u=fq/(fq-fr);hits.append((q[0]+u*(r[0]-q[0]),q[1]+u*(r[1]-q[1])))
  if len(hits)<2:continue
  q,r=max(((a,b) for a in hits for b in hits),key=lambda pair:math.dist(*pair))
  if math.dist(q,r)<.08:continue
  intervals=[(0,1)]
  for third in tris:
   if third is t or third is other:continue
   lo,hi=0.,1.;dx=r[0]-q[0];dz=r[1]-q[1];conditions=[]
   for u,v in zip(third['poly'],third['poly'][1:]+third['poly'][:1]):
    aa=-(v[1]-u[1]);bb=v[0]-u[0];cc=-aa*u[0]-bb*u[1];conditions.append((aa*dx+bb*dz,aa*q[0]+bb*q[1]+cc))
   dA,dB,dC=[third['plane'][i]-t['plane'][i] for i in range(3)];conditions.append((dA*dx+dB*dz,dA*q[0]+dB*q[1]+dC-.0001))
   for aa,bb in conditions:
    if abs(aa)<1e-10:
     if bb<0:lo=2;break
    elif aa>0:lo=max(lo,-bb/aa)
    else:hi=min(hi,-bb/aa)
   if hi<=lo:continue
   new=[]
   for a,b in intervals:
    if lo>a:new.append((a,min(b,lo)))
    if hi<b:new.append((max(a,hi),b))
   intervals=[(a,b) for a,b in new if b-a>1e-5]
  for a,b in intervals:
   p0=(q[0]+a*(r[0]-q[0]),q[1]+a*(r[1]-q[1]));p1=(q[0]+b*(r[0]-q[0]),q[1]+b*(r[1]-q[1]));a3=Vector((p0[0],height(t,*p0),p0[1]));b3=Vector((p1[0],height(t,*p1),p1[1]));key=('Valley',tuple(sorted([tuple(round(v,4) for v in a3),tuple(round(v,4) for v in b3)])));segments[key]=dict(a=a3,b=b3,role='Valley',roofA=t['name'],roofB=other['name'])
# Merge overlapping collinear pieces, including segmentation from triangulated carriers.
merged=[]
for seg in sorted(segments.values(),key=lambda t:(t['role'],t['roofA'],tuple(t['a']))):
 a,b=seg['a'],seg['b'];d=(b-a).normalized()
 if next((v for v in d if abs(v)>1e-5),1)<0:a,b=b,a;d=-d
 absorbed=False
 for m in merged:
  md=(m['b']-m['a']).normalized()
  if m['role']!=seg['role'] or set([m['roofA'],m['roofB']])!=set([seg['roofA'],seg['roofB']]) or abs(md.dot(d))<.9999:continue
  if (a-m['a']).cross(md).length>.002:continue
  vals=[(a-m['a']).dot(md),(b-m['a']).dot(md)];length=(m['b']-m['a']).length
  if min(vals)>length+.003 or max(vals)<-.003:continue
  base=m['a'].copy();m['a']=base+md*min(0,*vals);m['b']=base+md*max(length,*vals);absorbed=True;break
 if not absorbed:merged.append(dict(seg,a=a,b=b))

modules={};parts=[];current=None;buffers={}
def module(name,description,sockets,placement=(0,0,0),kind='Reusable'):
 global current,buffers
 current=name;buffers={};modules[name]=dict(name=name,description=description,kind=kind,placement=list(placement),sockets=sockets,parts=[])

def buf(key):return buffers.setdefault(key,{'v':[],'f':[],'uv':[],'paint':'Walnut' if key in ['Timber','Underlay'] else 'Slate'})
def uvpaint(key,u,v,seed):
 # Trim-sheet reuse is intentional; stable scale and shifts, no shader noise or per-tile materials.
 if key in ['Timber','Underlay']:return (.512+.476*max(.025,min(.975,.5+u/.85)),.512+.476*max(.025,min(.975,.08+v/3.6)))
 u0=.902+((seed*37)%31)*.0003;v0=.108+((seed*19)%23)*.0003
 # All tile patches stay in the approved grouped blue-grey paint region; no isolated sage rectangles.
 return (min(.98,u0+u*.06),min(.48,v0+v*.06))

def solid_poly(key,poly,fn,thick=.018,seed=0,uvfn=None):
 poly=clean(poly)
 if not poly or abs(area(poly))<1e-7:return
 # poly is (x,z); height can be authored or measured. Each patch is a closed watertight shell.
 data=buf(key);n=len(poly);off=len(data['v'])
 pts=[Vector((x,fn(x,z),z)) for x,z in poly]
 for lower in [True,False]:
  for p in pts:data['v'].append((p.x,p.z,p.y-(thick if lower else 0)))
 faces=[tuple(range(off+n-1,off-1,-1)),tuple(range(off+n,off+2*n))]+[(off+i,off+(i+1)%n,off+(i+1)%n+n,off+i+n) for i in range(n)]
 for f in faces:
  data['f'].append(f);uv=[]
  for idx in f:
   p=data['v'][idx];u,v=uvfn(p[0],p[1]) if uvfn else (p[0]-poly[0][0],p[1]-poly[0][1]);uv.append(uvpaint(key,u,v,seed))
  data['uv'].append(uv)

def prism_profile(key,profile,a,b,axis='X',seed=0):
 # Cross section coordinates across horizontal / height; extrude along ridge or fascia.
 n=len(profile);data=buf(key);off=len(data['v']);vs=[]
 for along in [a,b]:
  for across,h in profile:vs.append((along,across,h) if axis=='X' else (across,along,h))
 data['v']+=vs;faces=[tuple(range(off+n-1,off-1,-1)),tuple(range(off+n,off+2*n))]+[(off+i,off+(i+1)%n,off+(i+1)%n+n,off+i+n) for i in range(n)]
 for f in faces:
  data['f'].append(f);data['uv'].append([uvpaint(key,vs[idx-off][1 if axis=='X' else 0],vs[idx-off][0 if axis=='X' else 1],seed) for idx in f])

def flush():
 for key,data in buffers.items():
  if not data['f']:continue
  me=bpy.data.meshes.new(current+'_'+key);me.from_pydata(data['v'],[],data['f']);me.update();o=bpy.data.objects.new(current+'_'+key,me);s.collection.objects.link(o);me.materials.append(mats[data['paint']]);o['module']=current;o['role']=key
  uv=me.uv_layers.new(name='PaintUV0')
  for p,uvs in zip(me.polygons,data['uv']):
   uvarea=abs(sum(uvs[i][0]*uvs[(i+1)%len(uvs)][1]-uvs[(i+1)%len(uvs)][0]*uvs[i][1] for i in range(len(uvs))))*.5
   vbase=.512 if data['paint']=='Walnut' else .012
   if uvarea<1e-10 or any(not (.512<=u<=.988 and vbase<=v<=vbase+.476) for u,v in uvs):
    pts=[Vector(data['v'][i]) for i in p.vertices];edges=[pts[(i+1)%len(pts)]-pts[i] for i in range(len(pts))];tangent=max(edges,key=lambda e:e.length).normalized();normal=next((edges[0].cross(e).normalized() for e in edges[1:] if edges[0].cross(e).length>1e-10),Vector((0,0,1)));across=normal.cross(tangent).normalized();xy=[((q-pts[0]).dot(across),(q-pts[0]).dot(tangent)) for q in pts];lo=[min(q[i] for q in xy) for i in range(2)];span=[max(q[i] for q in xy)-lo[i] for i in range(2)];scale=min(.22,.44/max(max(span),1e-6));uvs=[(.524+(q[0]-lo[0])*scale,vbase+.012+(q[1]-lo[1])*scale) for q in xy]
   for li,val in zip(p.loop_indices,uvs):uv.data[li].uv=val
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
  if key=='Underlay':bmesh.ops.triangulate(bm,faces=list(bm.faces))
  bm.to_mesh(me);bm.free()
  uv=me.uv_layers[0]
  for p in me.polygons:
   vals=[uv.data[i].uv.copy() for i in p.loop_indices];ua=abs(sum(vals[i].x*vals[(i+1)%len(vals)].y-vals[(i+1)%len(vals)].x*vals[i].y for i in range(len(vals))))*.5
   if ua<1e-12:
    pts=[me.vertices[i].co.copy() for i in p.vertices];tangent=(pts[1]-pts[0]).normalized();normal=(pts[1]-pts[0]).cross(pts[2]-pts[0]).normalized();across=normal.cross(tangent);xy=[((q-pts[0]).dot(across),(q-pts[0]).dot(tangent)) for q in pts];lo=[min(q[i] for q in xy) for i in range(2)];span=[max(q[i] for q in xy)-lo[i] for i in range(2)];scale=min(.22,.44/max(max(span),1e-6));vb=.524 if data['paint']=='Walnut' else .024
    for li,q in zip(p.loop_indices,xy):uv.data[li].uv=(.524+(q[0]-lo[0])*scale,vb+(q[1]-lo[1])*scale)
  # Low-profile slate silhouette, flat surfaces; deliberate edge chamfers encoded as solid thickness.
  parts.append(o);modules[current]['parts'].append(o.name)

# One continuous physical course coordinate per roof side, never per triangle.
HERO_LEFT=[(-3.22,6.03),(-2.75,6.48),(-1.8,9.25),(-1.05,10.4)]
HERO_RIGHT=[(2.33,6.08),(1.77,6.58),(-.4,9.63),(-1.05,10.4)]
def arc_map(points,value,inverse=False):
 lengths=[0]
 for a,b in zip(points,points[1:]):lengths.append(lengths[-1]+math.dist(a,b))
 if inverse:
  i=next((i for i in range(len(lengths)-1) if value<=lengths[i+1]),len(lengths)-2);f=(value-lengths[i])/(lengths[i+1]-lengths[i]);return points[i][0]+f*(points[i+1][0]-points[i][0])
 increasing=points[-1][0]>points[0][0]
 i=next((i for i in range(len(points)-1) if (value<=points[i+1][0] if increasing else value>=points[i+1][0])),len(points)-2)
 f=(value-points[i][0])/(points[i+1][0]-points[i][0]);return lengths[i]+f*(lengths[i+1]-lengths[i])
def native_z(x,z,inverse=False):
 amount=.2*max(0,min(1,(x-2.1)/1.85));k=amount/3.55
 if inverse:
  return z+amount*max(0,min(1,(4.9-z)/3.55)) if z>.85 else z
 if z<=.85:return z
 if z<1.35+amount:return z-amount
 if z>=4.9:return z
 return (z-k*4.9)/(1-k)
def course_coordinates(t):
 A,B,C=t['plane'];name=t['name']
 if name=='Roof_Hero' and abs(A)>abs(B):
  profile=HERO_LEFT if A>0 else HERO_RIGHT
  return (lambda x,z:(z+4.4,arc_map(profile,x))), (lambda u,v:(arc_map(profile,v,True),u-4.4)),1.
 if name in ['Roof_RearCross','Roof_SubordinateCross']:
  profile=[(.5,6.2),(1.05,6.5),(3.1,8.55)] if name=='Roof_RearCross' else [(1.,6.02),(1.45,6.35),(2.875,7.55)]
  if B<0:profile=[(5.5,6.2),(3.1,8.55)] if name=='Roof_RearCross' else [(5.25,5.99),(4.8,6.35),(2.875,7.55)]
  return (lambda x,z:(x,arc_map(profile,native_z(x,z)))), (lambda u,v:(u,native_z(u,arc_map(profile,v,True),True))),1.
 if name in ['Roof_DeepEntryFold','Roof_LeftShopFold']:
  front=-5.8 if name=='Roof_DeepEntryFold' else -5.35;g=1.14/1.8 if name=='Roof_DeepEntryFold' else .995/1.35;factor=math.sqrt(1+g*g)
  return (lambda x,z:(x,(z-front)*factor)),(lambda u,v:(u,front+v/factor)),1.
 if name=='Roof_DisplayCatslide':
  factor=math.sqrt(1+(1/1.55)**2)
  return (lambda x,z:(z,(3.55-x)*factor)),(lambda u,v:(3.55-v/factor,u)),1.
 course_axis='Z' if abs(A)>abs(B) else 'X';gradient=A if course_axis=='Z' else B;sign=1 if gradient>=0 else -1;cos=1/math.sqrt(1+gradient*gradient)
 return (lambda x,z:(z,x*sign) if course_axis=='Z' else (x,z*sign)),(lambda u,v:(v*sign,u) if course_axis=='Z' else (u,v*sign)),cos

def tile_patch(patch,width=.3333333,advance=.30):
 t=patch['tri'];poly=patch['poly'];uvcoords,world,cos=course_coordinates(t);step=advance*cos
 polyuv=clean([uvcoords(x,z) for x,z in poly]);umin,umax=min(p[0] for p in polyuv),max(p[0] for p in polyuv);vmin,vmax=min(p[1] for p in polyuv),max(p[1] for p in polyuv)
 # Area-preserving visible polygon clipping, not accepting/rejecting whole tiles at intersections.
 for row in ([0] if t.get("single_course") else range(math.floor(vmin/step)-1,math.ceil(vmax/step)+1)):
  shift=.5*width if row%2 else 0;v0=row*step;v1=v0+.43*cos
  for col in range(math.floor((umin-shift)/width)-1,math.ceil((umax-shift)/width)+1):
   seed=(row*71+col*43+len(t['name'])*11)%997
   def boundary(k):return k*width+shift+.012*math.sin(k*2.17+row*.73)+.006*math.sin(k*.67+row*2.1)
   u0=boundary(col)+.0015;u1=boundary(col+1)-.0015
   # Restrained hand-cut toe: 1.5-3mm deterministic shape changes, never random surface noise.
   toe=((seed%5)-2)*.0007
   clipped=intersect(polyuv,[(u0,v0+toe),(u1,v0+toe),(u1,v1),(u0,v1)])
   if not clipped or abs(area(clipped))<.00005:continue
   wpoly=clean([world(u,v) for u,v in clipped])
   def hf(x,z):u,v=uvcoords(x,z);return height(t,x,z)+.048-.026*(v-v0)/(.43*cos)
   cutpolys=[wpoly]
   for valley in merged:
    if valley['role']!='Valley' or t['name'] not in [valley['roofA'],valley['roofB']]:continue
    aa,bb=valley['a'],valley['b'];d=Vector((bb.x-aa.x,bb.z-aa.z))
    if d.length<.01:continue
    d.normalize();n=Vector((-d.y,d.x));qa=Vector((aa.x,aa.z))-.005*d;qb=Vector((bb.x,bb.z))+.005*d;corridor=clean([tuple(qa-n*.038),tuple(qb-n*.038),tuple(qb+n*.038),tuple(qa+n*.038)])
    cutpolys=[fragment for poly0 in cutpolys for fragment in (difference(poly0,corridor) if overlap(poly0,corridor) else [poly0])]
   for poly0 in cutpolys:
    if abs(area(poly0))>.00005:solid_poly('Slate',poly0,hf,.018,seed,lambda x,z:(uvcoords(x,z)[0]-u0,(uvcoords(x,z)[1]-v0)/cos))

def standard_panel(name,width,length,pitch,course=False):
 theta=math.radians(pitch);run=length*math.cos(theta);rise=length*math.sin(theta);module(name,f'{width}m course width, {length}m on-slope length, measured-family pitch {pitch} degrees. Bottom-left eave pivot.',[{'name':'EaveStart','position':[0,0,0]},{'name':'EaveEnd','position':[width,0,0]},{'name':'UpSlopeStart','position':[0,rise,run]},{'name':'UpSlopeEnd','position':[width,rise,run]}])
 t=dict(name=name,plane=(0,math.tan(theta),0),single_course=course);poly=[(0,0),(width,0),(width,run),(0,run)];patch={'tri':t,'poly':poly};tile_patch(patch)
 if not course:solid_poly('Underlay',poly,lambda x,z:z*math.tan(theta)-.006,.10,0)
 else:modules[name]['sockets'].append({'name':'NextCourse','position':[0,.30*math.sin(theta),.30*math.cos(theta)]})
 flush()

# Pitch values selected from measured hero/wing/canopy slope families, not a uniform generic roof.
for pitch in [35,56.9,71.1]:standard_panel('CM_SlateRoofKit01_Panel2x2p4_'+str(pitch).replace('.','p'),2,2.4,pitch)
standard_panel('CM_SlateRoofKit01_Panel4x2p4_56p9',4,2.4,56.9)
standard_panel('CM_SlateRoofKit01_SecondaryGablePanel2m_52p43',2,math.hypot(1.5,1.95),math.degrees(math.atan2(1.95,1.5)))
standard_panel('CM_SlateRoofKit01_Panel2x1p2_56p9',2,1.2,56.9)
for pitch in [35,56.9]:standard_panel('CM_SlateRoofKit01_Course2m_'+str(pitch).replace('.','p'),2,.43,pitch,True)
# Timber eave and fascia, with concealed raised bearing and a defined drip overhang.
for pitch in [35,56.9]:
 name='CM_SlateRoofKit01_EaveFascia2m_'+str(pitch).replace('.','p');module(name,'Walnut fascia with seated supporting ledger. Align to panel EaveStart.',[{'name':'Start','position':[0,0,0]},{'name':'End','position':[2,0,0]}]);prism_profile('Timber',[(-.055,-.18),(.09,-.18),(.09,-.025),(-.055,-.025)],0,2);flush()
# Ridge caps with restrained, faceted slate profiles; finish the peak without modern metalwork.
for suffix,left,right in [('Hero',56.9,49.8),('Wing',40.1,31.9),('Secondary',52.43,52.43)]:
 name='CM_SlateRoofKit01_Ridge2m_'+suffix;module(name,'Low, asymmetric slate cap fitted to adjacent slope families; ridge-centre start pivot.',[{'name':'Start','position':[0,0,0]},{'name':'End','position':[2,0,0]}]);L=.16*math.tan(math.radians(left));R=.16*math.tan(math.radians(right));profile=[(-.16,-L+.035),(-.08,-L*.5+.055),(0,.07),(.08,-R*.5+.055),(.16,-R+.035),(.16,-R+.017),(.08,-R*.5+.037),(0,.052),(-.08,-L*.5+.037),(-.16,-L+.017)];prism_profile('Slate',profile,0,2);flush()
# Straight verge: canonical pitched 2m length, on-slope sockets; walnut barge and overlapping slate lip.
for pitch in [35,52.43,56.9,71.1]:
 th=math.radians(pitch);verge_length=math.hypot(1.5,1.95) if pitch==52.43 else 2;run=verge_length*math.cos(th);rise=verge_length*math.sin(th);name='CM_SlateRoofKit01_Verge2m_'+str(pitch).replace('.','p');module(name,'Walnut sloping edge and slate overcloak. Match panel outside edge, no duplicate bargeboard.',[{'name':'Eave','position':[0,0,0]},{'name':'Upper','position':[0,rise,run]}]);solid_poly('Timber',[(-.065,0),(.065,0),(.065,run),(-.065,run)],lambda x,z:z*math.tan(th)-.012,.13,1,lambda x,z:(x,z/math.cos(th)));solid_poly('Slate',[(-.085,0),(.025,0),(.025,run),(-.085,run)],lambda x,z:z*math.tan(th)+.025,.018,4,lambda x,z:(x,z/math.cos(th)));flush()
# Reusable internal valley for equal 35-degree intersecting roofs, 2m centre line.
module('CM_SlateRoofKit01_Valley2m_35','Slate-lined open valley, roof edges terminate at channel. Rotate/seat using intersection sockets.',[{'name':'Start','position':[0,0,0]},{'name':'End','position':[2,0,0]}]);profile=[(-.14,.14*math.tan(math.radians(35))+.015),(-.04,.04*math.tan(math.radians(35))+.012),(0,.012),(.04,.04*math.tan(math.radians(35))+.012),(.14,.14*math.tan(math.radians(35))+.015),(.14,.14*math.tan(math.radians(35))),(.04,.04*math.tan(math.radians(35))-.003),(0,-.003),(-.04,.04*math.tan(math.radians(35))-.003),(-.14,.14*math.tan(math.radians(35)))];prism_profile('Slate',profile,0,2);flush()
# Explicit change-of-pitch apron: usable at the measured steeper-to-hero shoulder relationship.
module('CM_SlateRoofKit01_PitchBreak2m_71to57','Bent slate apron across 71.1 to56.9 degree shoulder. Centre crease pivot; ends are along course axis.',[{'name':'CreaseStart','position':[0,0,0]},{'name':'CreaseEnd','position':[2,0,0]}]);profile=[(-.16,-.16*math.tan(math.radians(71.1))+.035),(0,.035),(.16,.16*math.tan(math.radians(56.9))+.035),(.16,.16*math.tan(math.radians(56.9))+.017),(0,.017),(-.16,-.16*math.tan(math.radians(71.1))+.017)];prism_profile('Slate',profile,0,2);flush()
# Surface fit is stored per named approved roof, retaining the unioned dormer and original deformation.
for r in roofs:
 name='CM_SlateRoofKit01_Fitted_'+r['name'].replace('Roof_','');points=r['vertices'];origin=(min(p[0] for p in points),min(p[1] for p in points)+.16,min(p[2] for p in points));module(name,'Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation.',[{'name':'MeasuredOrigin','position':[0,0,0]}],origin,'FittedAdapter')
 for patch in [p for p in visible if p['tri']['name']==r['name']]:
  tile_patch(patch);solid_poly('Underlay',patch['poly'],lambda x,z:height(patch['tri'],x,z)-.006,.10,1)
 # Fitted buffers are built in measured world coordinates then canonicalized at a metric reference pivot.
 for data in buffers.values():data['v']=[(p[0]-origin[0],p[1]-origin[2],p[2]-origin[1]) for p in data['v']]
 flush()
# Exposed eave/verge boundaries, excluding the separately authored full hero front rake.
module('CM_SlateRoofKit01_Fitted_EaveVergeNetwork','Measured boundary fascia/barge pieces, merged in one reusable adapter mesh. Excludes the HeroB front rake supplied separately.',[{'name':'WorldDatum','position':[0,0,0]}],(0,0,0),'FittedAdapter')
edgekeys=set();edgecount=0
for patch in visible:
 t=patch['tri'];p=patch['poly']
 for q,r in zip(p,p[1:]+p[:1]):
  if math.dist(q,r)<.08:continue
  a=Vector((q[0],height(t,*q),q[1]));b=Vector((r[0],height(t,*r),r[1]));d=Vector((b.x-a.x,0,b.z-a.z))
  if d.length<.08:continue
  d.normalize();perp=Vector((-d.z,0,d.x));mid=(a+b)/2;side=[top_at(mid.x+perp.x*k,mid.z+perp.z*k) for k in [-.004,.004]]
  if all(v is not None for v in side):
   if abs(side[0][0]-side[1][0])<.10:continue
   # Only the high external lip gets a seated fascia. Lower abutments end beneath it.
   if mid.y<max(v[0] for v in side)-.04:continue
   if max(v[0] for v in side)-min(v[0] for v in side)<.60:
    # Replace this edge with a fitted vertical step apron, not diagonal cross-roof ribbons.
    low=min(v[0] for v in side)-.018;data=buf('Slate');off=len(data['v'])
    for p0 in [a,b]:
     delta=p0.y-mid.y
     for across,yy in [(-.008,low+delta),(.008,low+delta),(.008,p0.y+.015),(-.008,p0.y+.015)]:
      vv=p0+perp*across;data['v'].append((vv.x,vv.z,yy))
    fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    for f in fs:data['f'].append(tuple(off+i for i in f));data['uv'].append([uvpaint('Slate',(i%4)*.02,(i//4)*(b-a).length,0) for i in f])
    continue
  if t['name']=='Roof_Hero' and abs(mid.z+4.4)<.002:continue
  key=tuple(sorted([tuple(round(v,4) for v in a),tuple(round(v,4) for v in b)]))
  if key in edgekeys:continue
  edgekeys.add(key);edgecount+=1;data=buf('Timber');off=len(data['v'])
  for base in [a,b]:
   for across,drop in [(-.055,-.18),(.055,-.18),(.055,-.025),(-.055,-.025)]:
    v=base+perp*across+Vector((0,drop,0));data['v'].append((v.x,v.z,v.y))
  fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
  for f in fs:data['f'].append(tuple(off+i for i in f));data['uv'].append([uvpaint('Timber',(i%4)*.04,(i//4)*(b-a).length,edgecount) for i in f])
flush()
# Fitted ridge, valley and pitch-change finishing strips share exact intersection lines.
for role in ['Ridge','Valley']:
 module('CM_SlateRoofKit01_Fitted_'+role+'Network','Measured '+role.lower()+' adapters for the approved interlocking roofs. Not a generic substitute for a different intersection.',[{'name':'WorldDatum','position':[0,0,0]}],(0,0,0),'FittedAdapter')
 for index,seg in enumerate(m for m in merged if m['role']==role):
  a,b=seg['a'],seg['b'];length=(b-a).length
  d=Vector((b.x-a.x,0,b.z-a.z));horizontal=d.length
  if horizontal<.08:continue
  d.normalize();perp=Vector((-d.z,0,d.x));width=.09 if role=='Ridge' else .095
  mid=(a+b)/2;slopes=[]
  for side in [-1,1]:
   q=mid+perp*side*.025;candidates=[t for t in tris if t['name'] in [seg['roofA'],seg['roofB']] and contains(t['poly'],q.x,q.z,.0001) and abs(height(t,mid.x,mid.z)-mid.y)<.12]
   if not candidates:candidates=sorted([t for t in tris if t['name'] in [seg['roofA'],seg['roofB']]],key=lambda t:abs(height(t,mid.x,mid.z)-mid.y))[:1]
   t=min(candidates,key=lambda t:abs(height(t,q.x,q.z)-mid.y));slopes.append(t['plane'][0]*perp.x+t['plane'][1]*perp.z)
  # Split at .65m for caps/transition slates; valleys remain continuous channel pieces.
  count=max(1,math.ceil(length/(.65 if role!='Valley' else 3)))
  for k in range(count):
   t0=k/count;t1=(k+1)/count;aa=a.lerp(b,t0);bb=a.lerp(b,t1)
   # A closed five-point bent strip, with surface heights sampled from the actual envelope.
   cross=[-width,-width*.4,0,width*.4,width];top=[]
   for p in [aa,bb]:
    for v in cross:
     q=p+perp*v;yy=p.y+slopes[0 if v<0 else 1]*v
     lift=(.055 if abs(v)<width*.1 else .035) if role=='Ridge' else (.014 if role=='Valley' else .034)
     top.append(Vector((q.x,yy+lift,q.z)))
   data=buf('Slate');off=len(data['v']);n=5
   for down in [.016,0]:
    for p in top:data['v'].append((p.x,p.z,p.y-down))
   # Two longitudinal surfaces, side/end caps. All faces form one closed strip shell.
   fs=[]
   for j in range(n-1):fs += [(off+j,off+j+1,off+n+j+1,off+n+j),(off+2*n+j,off+3*n+j,off+3*n+j+1,off+2*n+j+1)]
   fs += [(off,off+n,off+3*n,off+2*n),(off+n-1,off+2*n-1,off+4*n-1,off+3*n-1)]
   for j in range(n-1):fs += [(off+j,off+2*n+j,off+2*n+j+1,off+j+1),(off+n+j,off+n+j+1,off+3*n+j+1,off+3*n+j)]
   for f in fs:data['f'].append(f);data['uv'].append([uvpaint('Slate',(i%5)*width/2,(i//5%2)*(bb-aa).length,index+3) for i in f])
 flush()
# Approved front gable verge, matching FacadeBay01 HeroB without changing the roof profile.
profile=[(-3.22,6.03),(-2.75,6.48),(-1.8,9.25),(-1.05,10.40),(-.4,9.63),(1.77,6.58),(2.33,6.08)];module('CM_SlateRoofKit01_HeroB_GableVerge','Full measured front rake with one continuous walnut band and slate overcloak. FacadeBay01 HeroB profile equivalent, placed at original roof face.',[{'name':'LeftEave','position':[-3.22,6.03,-4.4]},{'name':'Apex','position':[-1.05,10.4,-4.4]},{'name':'RightEave','position':[2.33,6.08,-4.4]}],(0,0,0),'FittedAdapter')
# Here prism axis Z extrudes profile x/y along world z.
prism_profile('Timber',profile+[(x,y-.13) for x,y in reversed(profile)],-4.48,-4.36,'Z',2);prism_profile('Slate',[(x,y+.025) for x,y in profile]+[(x,y+.007) for x,y in reversed(profile)],-4.50,-4.36,'Z',3);flush()
# Record and validate each closed mesh shell; intentional UV0 sharing is a paint trim-sheet workflow.
report={'reference':raw['reference'],'modules':len(modules),'parts':[],'visibleRoofPolygons':len(visible),'junctionSegments':len(merged),'uv0':'Approved paint-sheet patches intentionally reused; no procedural surface noise.','sourcePaint':str(source),'topology':'Closed individual solids grouped per mesh; no per-shingle GameObjects.'};dims={}
for o in parts:
 bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);volume=bm.calc_volume(signed=True);bm.free();o.data.calc_loop_triangles();deg=sum(t.area<1e-11 for t in o.data.loop_triangles)
 if bad or volume<=0 or deg:raise RuntimeError((o.name,bad,volume,deg))
 assert all(math.isfinite(u.uv.x) and 0<=u.uv.x<=1 and 0<=u.uv.y<=1 for u in o.data.uv_layers[0].data)
 report['parts'].append(dict(name=o.name,module=o['module'],triangles=len(o.data.loop_triangles),nonmanifold_edges=bad,degenerate_triangles=deg,volume=volume))
 pts=[(v.co.x,v.co.z,v.co.y) for v in o.data.vertices];entry=dims.setdefault(o['module'],{'points':[],'triangles':0});entry['points']+=pts;entry['triangles']+=len(o.data.loop_triangles)
for key,entry in dims.items():pts=entry.pop('points');entry['min']=[min(p[i] for p in pts) for i in range(3)];entry['max']=[max(p[i] for p in pts) for i in range(3)]
# Source collections separate module families; display layout affects only standard source inspection.
for idx,(name,meta) in enumerate(modules.items()):
 col=bpy.data.collections.new(name);s.collection.children.link(col)
 loc=Vector((idx%6*6,idx//6*-7,0)) if meta['kind']=='Reusable' else Vector((0,0,0))
 for o in [p for p in parts if p['module']==name]:
  s.collection.objects.unlink(o);col.objects.link(o);o.location=loc if meta['kind']=='Reusable' else Vector((meta['placement'][0],meta['placement'][2],meta['placement'][1]))
 for sock in meta['sockets']:
  e=bpy.data.objects.new('Socket_'+sock['name'],None);col.objects.link(e);p=sock['position'];e.location=Vector((p[0],p[2],p[1]))+loc if meta['kind']=='Reusable' else Vector((p[0]+meta['placement'][0],p[2]+meta['placement'][2],p[1]+meta['placement'][1]));e.empty_display_type='ARROWS';e.empty_display_size=.14
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'CM_SlateRoofKit01.blend'))
for name,meta in modules.items():
 bpy.ops.object.select_all(action='DESELECT');selected=[o for o in parts if o['module']==name]
 if not selected:continue
 for o in selected:o.location=(0,0,0);o.select_set(True)
 bpy.context.view_layer.update()
 for o in selected:o.matrix_world=Matrix.Rotation(math.pi,4,'Z')@o.matrix_world
 bpy.context.view_layer.objects.active=selected[0];bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(ASSET/'Models'/f'{name}.fbx'),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(OUT/'ModuleCatalog.json').write_text(json.dumps(list(modules.values()),indent=2));(OUT/'GeometryValidation.json').write_text(json.dumps(report,indent=2));(OUT/'SourceDimensions.json').write_text(json.dumps(dims,indent=2));(OUT/'MeasuredJunctions.json').write_text(json.dumps([{k:list(v) if isinstance(v,Vector) else v for k,v in m.items()} for m in merged],indent=2));print('ROOF_KIT_READY',len(modules),len(parts),sum(p['triangles'] for p in report['parts']))
