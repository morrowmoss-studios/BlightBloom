"""Three independent neutral architectural composition studies. Unity Y-up coordinates.
Only study 04 outputs may be updated with --refine-created-study. Prior assets are read-only.
"""
import bpy,bmesh,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[4]
EXPORT=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/MassingStudies04/Models'
assert (ROOT/'ProjectSettings').is_dir(),ROOT
CONFIGS=[
 dict(id='A',title='Layered Merchant House',half=2.4,heroL=-2.6,heroR=2.45,peakX=-.65,peak=10.6,front=-3.0,entry=-3.0,upper=-3.65,neckRidge=9.15,wingStart=1.8,wingEnd=5.6,wingR=4.5,wingTop=5.95,wingPeak=8.1,wingUpper=True,wingAxis='Z',porch='lean',leftAnnex=False),
 dict(id='B',title='Tucked Corner Apothecary',half=2.1,heroL=-2.7,heroR=1.8,peakX=-.95,peak=11.1,front=-3.15,entry=-2.45,upper=-3.95,neckRidge=8.9,wingStart=1.0,wingEnd=4.9,wingR=4.15,wingTop=5.95,wingPeak=7.9,wingUpper=True,wingAxis='X',porch='folded',leftAnnex=False),
 dict(id='C',title='Crooked Shop Cluster',half=2.3,heroL=-2.65,heroR=2.65,peakX=-.35,peak=10.75,front=-3.25,entry=-2.9,upper=-4.05,neckRidge=8.65,wingStart=1.8,wingEnd=5.6,wingR=4.5,wingTop=3.65,wingPeak=6.1,wingUpper=False,wingAxis='Z',porch='gable',leftAnnex=True)]
REFINE='--refine-created-study' in sys.argv
for c in CONFIGS:
 if ((OUT/f'CM_Massing04_{c["id"]}.blend').exists() or (EXPORT/f'CM_Massing04_{c["id"]}.fbx').exists()) and not REFINE:raise RuntimeError('Study already exists; refusing overwrite')

def build(c):
 for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
 s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='BLENDER_EEVEE'
 mats={}
 for k,col in [('Plaster',(.62,.62,.62,1)),('Roof',(.30,.30,.30,1)),('Timber',(.24,.24,.24,1)),('Stone',(.44,.44,.44,1)),('Glass',(.10,.10,.10,1))]:
  m=bpy.data.materials.get('Study04_'+k) or bpy.data.materials.new('Study04_'+k);m.diffuse_color=col;mats[k]=m
 obs=[]
 def P(x,y,z):return(x,z,y)
 def mesh(n,vs,fs,k):
  me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);s.collection.objects.link(o);o.data.materials.append(mats[k]);obs.append(o)
  bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001);bmesh.ops.dissolve_degenerate(bm,dist=.000001,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();return o
 def box(n,p,d,k='Plaster'):
  x,y,z=p;a,b,h=[v/2 for v in d];vs=[P(x+sx*a,y+sy*b,z+sz*h) for sx,sy,sz in [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)]]
  return mesh(n,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],k)
 def prism(n,axis,poly,a,b,k):
  m=len(poly);vs=[P(u,y,end) if axis=='Z' else P(end,y,u) for end in [a,b] for u,y in poly];fs=[tuple(range(m-1,-1,-1)),tuple(range(m,2*m))]+[(i,(i+1)%m,(i+1)%m+m,i+m) for i in range(m)];return mesh(n,vs,fs,k)
 def boolean(o,cut,operation='DIFFERENCE'):
  bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Architectural aperture/intersection','BOOLEAN');mod.operation=operation;mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);obs.remove(cut);bpy.data.objects.remove(cut,do_unlink=True)
 def wall(n,axis,fixed,a,b,base,top,holes=[]):
  us=sorted(set([a,b]+[x for h in holes for x in h[:2] if a<x<b]));ys=sorted(set([base,top]+[y for h in holes for y in h[2:] if base<y<top]))
  for u,v in zip(us,us[1:]):
   for y,w in zip(ys,ys[1:]):
    if any(h[0]<(u+v)/2<h[1] and h[2]<(y+w)/2<h[3] for h in holes):continue
    box(n,((u+v)/2,(y+w)/2,fixed) if axis=='X' else(fixed,(y+w)/2,(u+v)/2),(v-u,w-y,.22) if axis=='X' else(.22,w-y,v-u))
 def archpoly(center,base,r,spring,rise,segments=20):return[(center-r,base),(center+r,base)]+[(center+r*math.cos(i*math.pi/segments),spring+rise*math.sin(i*math.pi/segments)) for i in range(segments+1)]
 def archhole(o,axis,fixed,center,base,r,spring,rise):boolean(o,prism('TEMP', 'Z' if axis=='X' else 'X',archpoly(center,base,r,spring,rise),fixed-.7,fixed+.7,'Plaster'))
 def beam(n,a,b,w=.14):
  a,b=Vector(P(*a)),Vector(P(*b));v=b-a;bpy.ops.mesh.primitive_cube_add(size=1,location=(a+b)/2);o=bpy.context.object;o.name=n;o.dimensions=(w,w,v.length);o.rotation_euler=v.to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.data.materials.append(mats['Timber']);obs.append(o);return o
 def arched_window(n,axis,fixed,center,base,r,spring,rise):
  # Quiet real recess and frame; no shutters or fine dressing in silhouette studies.
  prism(n+'_Glass','Z' if axis=='X' else 'X',archpoly(center,base,r-.04,spring,rise-.04),fixed-.025,fixed+.025,'Glass')
  curve=[(center-r,base),(center-r,spring)]+[(center+r*math.cos(math.pi-i*math.pi/16),spring+rise*math.sin(math.pi-i*math.pi/16)) for i in range(17)]+[(center+r,base)]
  for (u,y),(v,w) in zip(curve,curve[1:]):
   if (Vector((u,y))-Vector((v,w))).length<1e-4:continue
   beam(n+'_Frame',(u,y,fixed) if axis=='X' else(fixed,y,u),(v,w,fixed) if axis=='X' else(fixed,w,v),.085)
  beam(n+'_Sill',(center-r-.10,base,fixed) if axis=='X' else(fixed,base,center-r-.10),(center+r+.10,base,fixed) if axis=='X' else(fixed,base,center+r+.10),.13)
  beam(n+'_Mullion',(center,base,fixed) if axis=='X' else(fixed,base,center),(center,spring+rise-.06,fixed) if axis=='X' else(fixed,spring+rise-.06,center),.065)
 def simple_window(n,axis,fixed,center,base,width,height):
  arched_window(n,axis,fixed,center,base,width/2,base+height*.68,height*.32)
 def rect_window(n,axis,fixed,center,base,width,height):
  box(n+'_Glass',(center,base+height/2,fixed) if axis=='X' else(fixed,base+height/2,center),(width,height,.035) if axis=='X' else(.035,height,width),'Glass')
  for side in [-1,1]:
   u=center+side*width/2;beam(n+'_Frame',(u,base,fixed) if axis=='X' else(fixed,base,u),(u,base+height,fixed) if axis=='X' else(fixed,base+height,u),.085)
  for y in [base,base+height]:beam(n+'_Frame',(center-width/2,y,fixed) if axis=='X' else(fixed,y,center-width/2),(center+width/2,y,fixed) if axis=='X' else(fixed,y,center+width/2),.09)
  beam(n+'_Mullion',(center,base,fixed) if axis=='X' else(fixed,base,center),(center,base+height,fixed) if axis=='X' else(fixed,base+height,center),.065)
 def roof(n,axis,profile,a,b,capfront=True,capback=True):
  o=prism(n,axis,profile+[(u,y-.16) for u,y in reversed(profile)],a,b,'Roof')
  # Full gable caps start safely above playable headroom; roof is hollow.
  base=min(y for _,y in profile)-.08
  cap=[(profile[0][0],base)]+[(u,y-.17) for u,y in profile[1:-1]]+[(profile[-1][0],base)]
  if capfront:prism(n+'_GableFront',axis,cap,a+.25,a+.46,'Plaster')
  if capback:prism(n+'_GableRear',axis,cap,b-.46,b-.25,'Plaster')
  for (u,y),(v,w) in zip(profile,profile[1:]):beam(n+'_Bargeboard',(u,y,a-.025) if axis=='Z' else(a-.025,y,u),(v,w,a-.025) if axis=='Z' else(a-.025,w,v),.13)
  return o
 def lean(n,vs):
  pts=[P(x,y+dy,z) for dy in [-.14,0] for x,y,z in vs];return mesh(n,pts,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'Roof')
 h=c['half'];hl=c['heroL'];hr=c['heroR'];front=c['front'];entry=c['entry'];upper=c['upper'];ws=c['wingStart'];we=c['wingEnd'];wr=c['wingR'];wt=c['wingTop'];up=3.44
 # Actual connected irregular footprint, not a full rectangular master box.
 box('Floor_FrontShop',(0,.1,(front+.8)/2),(h*2,.2,.8-front),'Timber')
 box('Floor_RearStem',(0,.1,3.2),(4.2,.2,4.8),'Timber')
 box('Floor_WorkWing',((2.1+wr)/2,.1,(ws+we)/2),(wr-2.1,.2,we-ws),'Timber')
 box('Floor_UpperHero',((hl+hr)/2,up-.1,(upper-.9)/2),(hr-hl,.2,-.9-upper),'Timber')
 box('Floor_UpperRightFront',((-.5+hr)/2,up-.1,-.05),(hr+.5,.2,1.7),'Timber') # Z -.9..+.8
 box('Floor_UpperRightRear',(.8,up-.1,2.75),(2.6,.2,3.9),'Timber') # Z .8..4.7
 box('Floor_UpperLanding',(0,up-.1,5.02),(4.2,.2,1.16),'Timber')
 if c['wingUpper']:box('Floor_UpperStudy',((2.1+wr)/2,up-.1,(ws+we)/2),(wr-2.1,.2,we-ws),'Timber')
 # Front wall is physically stepped in B/C; entry sits under a deeper upper projection.
 split=-.05
 left=box('Shell_ShopFrontLeft',((-h+split)/2,1.77,front),((h+split),3.14,.22));boolean(left,box('TEMP',(-1.13,1.80,front),(1.4,1.6,1.2)));rect_window('Window_ShopDisplay','X',front-.14,-1.13,1.0,1.4,1.6)
 right=box('Shell_RecessedEntryRight',((split+h)/2,1.77,entry),(h-split,3.14,.22));archhole(right,'X',entry,.85,.1,.72,2.0,.90)
 if abs(entry-front)>.01:wall('Shell_EntryRecessReturn','Z',split,min(front,entry),max(front,entry),.2,3.34)
 # Door reveal/frame only; open aperture during traversal.
 for x in [.07,1.63]:beam('Entry_Jamb',(x,.2,entry-.13),(x,2.02,entry-.13),.12)
 for i in range(16):
  a=math.pi*i/16;b=math.pi*(i+1)/16;beam('Entry_Arch',(.85+.78*math.cos(a),2.0+.96*math.sin(a),entry-.13),(.85+.78*math.cos(b),2.0+.96*math.sin(b),entry-.13),.12)
 # Upper front projects independently of the shop below; broad plain facade is not the compositional unit.
 fu=box('Shell_UpperHero',((hl+hr)/2,4.84,upper),(hr-hl,2.8,.22))
 archhole(fu,'X',upper,-.40,4.2,.98,6.15,1.1)
 arched_window('Window_Hero','X',upper-.15,-.40,4.2,.98,6.15,1.1)
 wall('Shell_FrontWestGround','Z',-h,front,.8,.2,3.44,[(-2,-.5,.2,2.95)] if c['leftAnnex'] else [])
 wall('Shell_FrontEastGround','Z',h,entry,.8,.2,3.44,[(-1.8,-.35,.2,2.95)])
 wall('Shell_HeroWest','Z',hl,upper,.8,3.44,6.24,[(-1.4,-.1,4.45,5.9)])
 wall('Shell_HeroEast','Z',hr,upper,.8,3.44,6.24,[(-1.6,-.2,4.4,6.0)])
 simple_window('Window_HeroSide','Z',hr+.14,-.9,4.4,1.4,1.6)
 simple_window('Window_HeroWest','Z',hl-.14,-.75,4.45,1.3,1.45)
 # Close steps between wider front and narrower rear body at their actual wall lines.
 for a,b in [(-h,-2.1),(2.1,h)]:
  if b-a>.001:wall('Shell_FootprintShoulder','X',.8,a,b,.2,3.44)
 for a,b in [(hl,-2.1),(2.1,hr)]:
  if b-a>.001:wall('Shell_UpperShoulder','X',.8,a,b,3.44,6.24)
 # Where the right front upper is narrower than the stem, close the rear-facing offset.
 if hr<2.1:wall('Shell_UpperShoulder','X',.8,hr,2.1,3.44,6.24)
 wall('Shell_StemWest','Z',-2.1,.8,5.6,.2,6.24)
 linkZ=max(ws+.85,3.25)
 wall('Shell_StemEastGround','Z',2.1,.8,5.6,.2,3.44,[(linkZ-.8,linkZ+.8,.2,3.1)])
 wall('Shell_StemEastUpper','Z',2.1,.8,5.6,3.44,6.24,[(linkZ-.8,linkZ+.8,3.44,6.05)] if c['wingUpper'] else [])
 wall('Shell_StemRear','X',5.6,-2.1,2.1,.2,6.24,[(.35,1.8,.2,3.05)])
 # Side wing is slender, and C deliberately makes this a single-storey workroom.
 wall('Shell_WingFront','X',ws,2.1,wr,.2,wt)
 wall('Shell_WingRear','X',we,2.1,wr,.2,wt,[(2.55,wr-.3,.2,2.95)] if we>5.3 else [])
 wall('Shell_WingEast','Z',wr,ws,we,.2,wt,[(ws+.65,ws+1.85,1.15,2.65)])
 wall('Shell_WingWestReturn','Z',2.1,5.6,we,.2,wt) if we>5.6 else None
 if we<5.6:wall('Shell_StemAfterWing','Z',2.1,we,5.6,.2,3.44)
 simple_window('Window_WorkWing','Z',wr+.14,ws+1.25,1.15,1.2,1.5)
 if c['wingUpper']:
  # A shallow tall opening makes the little gable read as a stacked workshop/study, not a second normal house.
  wf=next(o for o in obs if o.name=='Shell_WingFront');archhole(wf,'X',ws,(2.1+wr)/2,4.05,.55,5.22,.62);arched_window('Window_Study','X',ws-.14,(2.1+wr)/2,4.05,.55,5.22,.62)
 # Main shop's slender display projection provides a real occupied facade step.
 displayR=h+1.10;dz=ws
 box('Floor_DisplayBay',((h+displayR)/2,.1,(-2.3+dz)/2),(1.1,.2,dz+2.3),'Timber')
 wall('Shell_DisplayFront','X',-2.3,h,displayR,.2,3.35)
 wall('Shell_DisplaySide','Z',displayR,-2.3,dz,.2,3.35,[(-1.7,-.05,1.0,2.6)])
 wall('Shell_DisplayRear','X',dz,h,displayR,.2,3.35)
 rect_window('Window_DispensingBay','Z',displayR+.14,-.875,1.0,1.65,1.6)
 # Sparse functional partitions: rear treatment/preparation; upstairs bed and study/living.
 wall('Interior_Treatment','X',2.25,-.4,2.1,.2,3.24,[(.35,1.8,.2,3.05)])
 wall('Interior_StairScreen','Z',-.5,.1,4.7,.2,3.24)
 wall('Interior_Bedroom','Z',-.25,upper,-.9,up,6.1,[(-2.25,-.95,up,6.1)])
 # Straight shop-house stair: shared viable central circulation, actual void in upper floor.
 for i in range(18):
  z=-.60+i*.28;top=.2+(i+1)*.18
  box('Stairs_StraightFlight',(-1.3,(.2+top)/2,z+.14),(1.25,top-.2,.28),'Timber')
 wall('Stairs_UpperGuard','Z',-.53,-.85,4.65,up,4.55)
 # Primary hero gable and a different, smaller roof behind it: no single practical roof on a master box.
 px=c['peakX'];pk=c['peak'];profile=[(hl-.42,6.03),(hl+.05,6.48),(px-.75,pk-1.15),(px,pk),(px+.65,pk-.77),(hr-.08,6.58),(hr+.48,6.08)]
 hero=roof('Roof_Hero','Z',profile,upper-.35,1.13)
 # Cut true opening through front gable cap if arch crosses the wall-top line.
 for o in list(obs):
  if o.name=='Roof_Hero_GableFront':archhole(o,'X',upper,-.4,4.2,.98,6.15,1.1)
 if c['id']=='B':
  neckprofile=[(.50,6.20),(1.05,6.5),(3.10,c['neckRidge']),(5.5,6.2)]
  roof('Roof_RearCross','X',neckprofile,-2.48,2.48)
 else:
  roof('Roof_SteppedRear','Z',[(-2.5,6.12),(-1.95,6.48),(-.35,c['neckRidge']),(1.95,6.55),(2.5,6.15)],.55,5.98)
 # Cross dormer becomes an actual roof volume, unioned with the hero roof.
 dp=[(-.55,6.55),(-.55,7.30),(.3,8.65 if c['id']!='B' else 8.95),(1.15,7.30),(1.15,6.55)]
 hero.data.materials.append(mats['Plaster'])
 dm=prism('TEMP_Dormer','X',dp,.5,hr+.12,'Plaster');boolean(hero,dm,'UNION')
 for p in hero.data.polygons:p.material_index=1 if abs(p.normal.z)<.04 else 0
 # Dormer face is pierced with a recessed rectangular opening that stays below its pitched shoulders.
 cut=box('TEMP',(hr+.08,7.32,.3),(.65,.85,.68));boolean(hero,cut)
 box('Window_DormerGlass',(hr-.25,7.32,.3),(.03,.78,.61),'Glass')
 for z in [-.08,.68]:beam('Window_DormerFrame',(hr+.145,6.86,z),(hr+.145,7.77,z),.075)
 for y in [6.86,7.77]:beam('Window_DormerFrame',(hr+.145,y,-.08),(hr+.145,y,.68),.075)
 # Subordinate wing roofs differ in orientation and storey count among the three studies.
 if c['wingAxis']=='Z':
  roof('Roof_SubordinateWing','Z',[(1.76,wt+.07),(2.12,wt+.36),((2.1+wr)/2-.12,c['wingPeak']),(wr-.10,wt+.36),(wr+.36,wt+.04)],ws-.32,we+.35)
 else:
  roof('Roof_SubordinateCross','X',[(ws-.35,wt+.07),(ws+.1,wt+.4),((ws+we)/2-.25,c['wingPeak']),(we-.1,wt+.4),(we+.35,wt+.04)],1.80,wr+.35)
 # Porch is deliberately an integrated deep shop shelter; three distinct canopy compositions.
 porchfront=-5.55 if c['id']!='B' else -5.70
 box('Floor_Porch',((hl+hr)/2,.1,(porchfront+entry)/2),(hr-hl+.3,.2,entry-porchfront),'Stone')
 box('Porch_ApproachStep',(.85,.05,porchfront-.2),(1.8,.1,.5),'Stone')
 if c['porch']=='gable':
  roof('Roof_EntranceGable','Z',[(-.28,3.12),(.1,3.4),(.85,5.05),(1.65,3.5),(2.04,3.15)],porchfront-.20,entry+.35)
  lean('Roof_ShopAwning',[(hl-.3,4.0,front+.2),(.0,4.0,front+.2),(.0,3.15,porchfront-.1),(hl-.3,3.15,porchfront-.1)])
 elif c['porch']=='folded':
  lean('Roof_DeepEntryFold',[(-.25,4.7,entry+.3),(hr+.5,4.7,entry+.3),(hr+.5,3.15,porchfront-.1),(-.25,3.15,porchfront-.1)])
  lean('Roof_LeftShopFold',[(hl-.35,4.1,front+.2),(.0,4.1,front+.2),(.0,3.05,porchfront+.35),(hl-.35,3.05,porchfront+.35)])
 else:lean('Roof_FrontCatslide',[(hl-.4,4.25,front+.3),(hr+.4,4.25,front+.3),(hr+.4,3.10,porchfront-.15),(hl-.4,3.10,porchfront-.15)])
 lean('Roof_DisplayCatslide',[(h-.1,4.30,-2.65),(h-.1,4.30,ws+.12),(displayR+.35,3.30,ws+.12),(displayR+.35,3.30,-2.65)])
 for x in [hl+.08,hr-.08]:
  beam('Porch_Post',(x,.2,porchfront+.12),(x,2.95,porchfront+.12),.17)
  beam('Porch_Knee',(x,2.25,porchfront+.12),(x,3.25,porchfront+.85),.13)
 beam('Porch_HeadBeam',(hl-.2,2.98,porchfront+.12),(hr+.2,2.98,porchfront+.12),.19)
 # Visible structural projection and gable tie only; no facade-wide decorative grid.
 beam('Structure_JettyTie',(hl,3.34,upper-.15),(hr,3.34,upper-.15),.18)
 beam('Structure_GableTie',(hl+.8,7.6,upper-.19),(hr-.75,7.6,upper-.19),.16)
 beam('Structure_Kingpost',(px,7.6,upper-.19),(px,pk-.28,upper-.19),.15)
 # Chimneys positioned on rear masonry, not inside the doorway/corridor envelopes.
 top=pk-.15
 box('Chimney_Primary',(2.0,(.2+top)/2,4.90),(.65,top-.2,.78),'Stone')
 box('Chimney_Cap',(2.0,top+.05,4.90),(.95,.18,1.05),'Stone')
 for x in [1.81,2.21]:box('Chimney_Pot',(x,top+.42,4.90),(.19,.55,.23),'Stone')
 box('Chimney_Secondary',(-2.1,pk*.43,2.35),(.42,pk*.80,.46),'Stone')
 if c['leftAnnex']:
  box('Floor_LeftAlcove',(-h-.7,.1,-.8),(1.4,.2,3.2),'Timber')
  wall('Shell_AlcoveWest','Z',-h-1.4,-2.4,.8,.2,3.55)
  wall('Shell_AlcoveFront','X',-2.4,-h-1.4,-h,.2,3.55)
  wall('Shell_AlcoveRear','X',.8,-h-1.4,-h,.2,3.55)
  lean('Roof_LeftAlcove',[(-h+.15,4.65,-2.65),(-h+.15,4.65,1),(-h-1.65,3.55,1),(-h-1.65,3.55,-2.65)])
 # Preserve semantic architectural components rather than hundreds of scene primitives.
 def cat(o):
  n=o.name.split('.')[0]
  for p in ['Shell','Interior','Floor','Stairs','Porch','Structure','Chimney','Window']:
   if n.startswith(p):return p if p in ['Shell','Interior','Porch','Structure','Chimney','Window'] else n
  return n
 by={}
 for o in obs:by.setdefault(cat(o),[]).append(o)
 final=[]
 for name,items in by.items():
  bpy.ops.object.select_all(action='DESELECT')
  for o in items:o.select_set(True)
  bpy.context.view_layer.objects.active=items[0]
  if len(items)>1:bpy.ops.object.join()
  o=bpy.context.object;o.name=name;final.append(o)
  # Explicit triangulation gives consistent Blender/Unity geometry diagnostics.
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=1e-6,edges=list(bm.edges));bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 bpy.ops.object.select_all(action='DESELECT')
 for o in final:o.select_set(True)
 bpy.context.view_layer.objects.active=final[0];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(55),island_margin=.003);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,margin=.002);bpy.ops.object.mode_set(mode='OBJECT')
 report=dict(configuration=c,floor_levels=[.2,up],stairs=dict(risers=18,rise=.18,tread=.28,width=1.25),parts=[])
 for o in final:
  bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);vol=bm.calc_volume(signed=True);bm.free();assert bad==0 and vol>0,(c['id'],o.name,bad,vol)
  report['parts'].append(dict(name=o.name,triangles=len(o.data.polygons),nonmanifold=bad,volume=vol))
 ident=f'CM_Massing04_{c["id"]}'
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(ident+'.blend')))
 conversion=Matrix.Rotation(math.pi,4,'Z')
 for o in final:o.matrix_world=conversion@o.matrix_world
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(EXPORT/(ident+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False)
 (OUT/(ident+'_validation.json')).write_text(json.dumps(report,indent=2));print('STUDY_READY',ident,len(final),sum(x['triangles'] for x in report['parts']))
for c in CONFIGS:build(c)
(OUT/'studies.json').write_text(json.dumps(CONFIGS,indent=2))
