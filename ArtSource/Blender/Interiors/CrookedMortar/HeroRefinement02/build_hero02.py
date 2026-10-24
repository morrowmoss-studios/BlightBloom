"""Scoped hero derivatives. Reuse original AF01 source meshes; preserve originals and all gameplay colliders."""
from pathlib import Path
import sys
D=Path(__file__).resolve().parent;R=D.parents[4]
base=R/'ArtSource/Blender/Interiors/CrookedMortar/ApothecaryFurnishings01'
lib=base/'CM_ApothecaryFurnishings01.blend'
prefix=(base/'build_furnishings01.py').read_text().split('# Counter:')[0]
prefix=prefix.replace("CrookedMortar/ApothecaryFurnishings01'","CrookedMortar/HeroRefinement02'")
prefix=prefix.replace("A/'Textures/CM_AF01_BotanicalLabels.png'","A/'Textures/CM_HR02_InkArtwork.png'")
exec(compile(prefix,str(__file__),'exec'))
heroPaint=bpy.data.images.load(str(A/'Textures/CM_HR02_PaintedSheet.png'));heroPaint.pack()
for node in mats['Walnut'].node_tree.nodes:
 if node.type=='TEX_IMAGE':node.image=heroPaint
# New front-facing ink sheets are viewed from the opposite native UV side after FBX conversion.
base_label=label
def label(*args,**kwargs):
 o=base_label(*args,**kwargs)
 for loop in o.data.uv_layers[0].data:
  mid=(math.floor(loop.uv.x*4)+.5)/4;loop.uv.x=2*mid-loop.uv.x
 return o
# Model helpers operate in metric Unity coordinates; exporter applies established native conversion.
def source(name):
 with bpy.data.libraries.load(str(lib),link=False) as (a,b):b.objects=[name]
 o=b.objects[0];s.collection.objects.link(o);o.name='Recoverable source derivative';parts.append(o)
 for i,m in enumerate(o.data.materials):
  key=m.name.replace('CM_AF01_','').split('.')[0];o.data.materials[i]=mats[key]
 return o
def outline(n,pts,depth,key='Walnut',bevel=.006):
 # Extruded front-facing polygon, not an overlapping solid box.
 count=len(pts);return mesh(n,[(x,y,z) for z in [depth[0],depth[1]] for x,y in pts],[tuple(reversed(range(count))),tuple(range(count,count*2))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)],key,bevel)
def scroll(n,x,y,z,scale=1,key='Walnut'):
 ps=[]
 for i in range(25):
  a=i/24*math.pi*1.7;r=(.12-.075*i/24)*scale;ps.append((x+r*math.cos(a),y+r*math.sin(a),z))
 tube(n,ps,.009*scale,key)
def botanical(x,y,z,h=.25):
 ps=[(x-.01,y-h*.48,z),(x+.015,y-h*.1,z),(x-.007,y+h*.23,z),(x+.012,y+h*.48,z)]
 tube('Carved stem',ps,.004,'Brass')
 for j in range(5):
  yy=y-h*.30+j*h*.15;side=1 if j%2 else -1
  leaf=[(x,yy),(x+side*h*.13,yy+h*.10),(x+side*h*.29,yy+h*.13),(x+side*h*.25,yy+h*.015),(x+side*h*.10,yy-h*.015)]
  outline('Lanceolate carved leaf',leaf,(z-.002,z+.004),'Brass',.001)
def peg(x,y,z,r=.012):rod('Oak drawbore peg',(x,y,z-.015),(x,y,z+.004),r,'Linen',10)
start('CM_HR02_CounterCraft')
source('CM_AF01_SalesCounter')
# Tapered chamfered pilasters with readable collar/base profiles, no footprint growth beyond 25 mm.
for x in [-1.025,1.025]:
 loft('Shaped corner pilaster',[(.12,.067,.052,x,.34),(.20,.075,.06,x,.34),(.24,.048,.045,x,.34),(.72,.045,.044,x,.34),(.79,.070,.055,x,.34),(.88,.063,.05,x,.34)],'Walnut',8)
 for yy in [.23,.77]:box('Collar moulding',(x,yy,.34),(.15,.035,.12),b=.01)
 peg(x,.86,.406)
for x in [-.69,0,.69]:
 pts=[(x-.29,.25),(x+.29,.25),(x+.29,.64),(x+.23,.72),(x,.78),(x-.23,.72),(x-.29,.64)]
 outline('Arch-headed panel moulding',pts,(.399,.418),'Walnut')
 inner=[(x+(px-x)*.86,.5+(py-.5)*.87) for px,py in pts];outline('Painted recessed field',inner,(.418,.423),'Sage',.004)
 if x==0:
  outline('Carved mortar bowl',[(x-.12,.56),(x+.12,.56),(x+.085,.43),(x-.08,.43)],(.43,.438),'Brass',.004)
  rod('Carved pestle',(x-.015,.55,.439),(x+.075,.69,.439),.013,'Brass',10)
 else:botanical(x,.51,.43,.31)
 # Paired inset rosettes frame, distinct from repeated trim strips.
 for side in [-1,1]:scroll('Panel tendril',x+side*.18,.36,.429,.40,'Brass')
for yy in [.18,.88]:box('Ogee lower bead',(0,yy,.38),(2.11,.033,.054),b=.014)
# Side panel construction remains legible from shop entrance and staff side.
for x in [-1.075,1.075]:
 for yy in [.23,.83]:box('Side field rail',(x,yy,0),(.025,.045,.60),b=.009)
# A keyed repair and selected edge wear, not uniformly distributed scratches.
outline('Butterfly repair key',[(-.82,.965),(-.77,.982),(-.72,.965),(-.72,1.005),(-.77,.992),(-.82,1.005)],(-.372,-.361),'Linen',.001)
finish()
start('CM_HR02_ShelvingCraft');o=source('CM_AF01_MedicineShelving')
# Remove the old stepped crown only, replacing it with an actual continuous shaped silhouette.
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.z>2.22],context='VERTS');bm.to_mesh(o.data);bm.free()
pts=[(-.91,2.19),(.91,2.19),(.91,2.26),(.72,2.27),(.55,2.34),(.30,2.38),(0,2.45),(-.30,2.38),(-.55,2.34),(-.72,2.27),(-.91,2.26)]
outline('Continuous swan-neck pediment',pts,(-.18,.15),'Walnut',.012)
# Bracket shoulders and shelf nosings; readable shapes rather than extra subdivisions.
for x in [-.82,.82]:
 for yy in [.92,1.38,1.84]:
  outline('Scalloped shelf corbel',[(x-.035,yy),(x+.035,yy),(x+.035,yy-.17),(x+.01,yy-.14),(x-.025,yy-.06)],(.08,.20),'Walnut',.004)
for yy in [.50,.96,1.42,1.88]:box('Rounded shelf nose',(0,yy-.018,.205),(1.72,.032,.034),b=.012)
for x in [-.56,0,.56]:
 box('Herbarium drawer',(x,.29,.192),(.50,.29,.046),'Walnut',.009);box('Drawer raised field',(x,.29,.221),(.43,.22,.016),'Sage',.006)
 label('Hand-lettered drawer name',(x,.30,.234),.20,.10,[0,1,3][int(round((x+.56)/.56))]);rod('Drop pull',(x,.20,.238),(x,.20,.27),.018,'Iron',12)
for x in [-.74,.74]:botanical(x,2.27,.158,.13)
finish()
# Stock containers: authored differently shaped pottery, bulbous tinctures, tall stoppered bottles.
def vessel(x,y,z,h,r,typ,index):
 profile=([(0,r*.7),(.03,r),(.7*h,r),(.82*h,r*.82),(.86*h,r*.62),(.94*h,r*.62)] if typ==0 else [(0,r*.6),(.05*h,r*.8),(.18*h,r),(.55*h,r),(.70*h,r*.65),(.78*h,r*.36),(.94*h,r*.36)])
 lathe('Apothecary vessel',(x,y,z),profile,'Ceramic' if typ==0 else 'Glass',32)
 rr=r*(.68 if typ==0 else .39);lathe('Cork and neck band',(x,y,z),[(h*.89,rr),(h*.94,rr*1.1),(h,rr*.95)],'Walnut',20)
 label('Botanical ink label',(x,y+h*.40,z+r*1.025),r*1.55,h*.34,index)
 if typ:lathe('Muted tincture',(x,y,z),[(h*.05,r*.75),(h*.43,r*.85)],'Sage',24)
for row in range(4):
 start('CM_HR02_StockCourse'+str(row+1))
 arrangement=[(-.65,.27,.081,0),(-.37,.35,.07,1),(-.09,.30,.095,0),(.25,.38,.072,1),(.63,.25,.088,0)] if row%2==0 else [(-.64,.33,.075,1),(-.30,.26,.082,0),(.06,.32,.095,0),(.45,.35,.067,1),(.67,.22,.06,0)]
 if row==3:
  arrangement=[(-.60,.34,.08,1),(-.18,.29,.09,0),(.66,.27,.08,0)]
  box('Fitted herb caddy',(.28,.09,0),(.32,.18,.22),'Walnut',.008);box('Caddy lid',(.28,.19,0),(.34,.025,.23),'Walnut',.005);label('Caddy inventory',(.28,.09,.116),.23,.12,3)
 for j,(x,h,r,typ) in enumerate(arrangement):vessel(x,0,.015*(j%3-1),h,r,typ,(j+row)%4)
 finish()
start('CM_HR02_CounterJar');vessel(0,0,0,.28,.084,0,0);finish()
start('CM_HR02_RecordsCluster')
# Tied volumes, folded order parcels, quill and ink; surface origin.
for j,(x,w,h,d) in enumerate([(-.16,.25,.045,.31),(-.13,.23,.055,.29)]):
 box('Bound case notes',(x,.03+j*.06,0),(w,h,d),'Walnut' if j==0 else 'Sage',.01)
 box('Ivory page block',(x,.03+j*.06,.005),(w-.016,h-.014,d-.013),'Linen',.003)
 box('Book cover',(x,.03+j*.06+h/2+.004,0),(w+.008,.01,d+.01),'Walnut' if j==0 else 'Sage',.004)
lathe('Ink pot',(.12,0,-.05),[(0,.035),(.05,.045),(.075,.025),(.085,.03)],'Iron',24)
rod('Quill stem',(.12,.07,-.05),(.18,.32,-.04),.003,'Linen',8)
outline('Quill vane',[(.174,.22),(.18,.32),(.17,.39),(.15,.33),(.16,.25)],(-.045,-.038),'Linen',.001)
finish()
start('CM_HR02_ResearchSheet');o=label('Pressed botanical notes',(0,0,0),.36,.44,4)
for v in o.data.vertices:v.co=Vector((v.co.x,v.co.z,v.co.y+.003))
finish()
start('CM_HR02_Parcel');box('Folded herbal order',(0,.055,0),(.25,.11,.18),'Linen',.015)
for x in [-.07,.07]:tube('Linen parcel ties',[(x,.01,-.10),(x,.115,-.10),(x,.115,.10),(x,.01,.10)],.003,'Walnut')
label('Parcel inscription',(0,.057,.098),.13,.065,0);finish()
start('CM_HR02_HerbariumBoard');box('Framed herbarium',(0,0,0),(.72,.90,.04),'Walnut',.015);label('Gathering study',(0,0,.026),.65,.82,7)
for x in [-.30,.30]:peg(x,.36,.034,.009)
finish()
start('CM_HR02_PracticePlaque');outline('Shaped consultation plaque',[(-.26,-.31),(.26,-.31),(.27,.27),(.19,.34),(-.17,.35),(-.27,.26)],(-.025,.025),'Walnut',.012);label('Consultation sign',(0,.005,.030),.46,.59,5)
for x in [-.23,.23]:peg(x,.28,.035,.009)
finish()
# Portal ornaments fit the original +/-1.1m posts and curve; no entrance dimension change.
start('CM_HR02_PortalJoinery')
for x in [-1.1,1.1]:
 for yy in [.43,2.42]:
  box('Post forged collar',(x,yy,.084),(.155,.06,.025),'Iron',.008)
  for xx in [-.048,.048]:peg(x+xx,yy,.106,.008)
 botanical(x,1.85,.082,.31)
 # Curved carved corbel no lower than original arch spring.
 ps=[(x+(-1 if x>0 else 1)*(.02+i*.022),2.40+.17*math.sin(i/15*math.pi/2),.115) for i in range(16)]
 tube('Carved arch bead',ps,.012,'Walnut')
# Delicate incised botanical sweep along the outer arch, following rather than replacing its silhouette.
for side in [-1,1]:
 ps=[(side*(.15+i*.048),2.93-.29*((.15+i*.048)/1.1)**1.5,.091) for i in range(19)]
 tube('Arch bead',ps,.011,'Walnut')
finish()
# Uneven plaster patch and individually jointed stoop-facing stones are fitted visual veneers.
start('CM_HR02_LimeRepair');outline('Old limewash repair',[(-.23,-.22),(.16,-.25),(.25,-.07),(.21,.19),(.07,.23),(-.18,.18),(-.25,.03)],(-.003,.003),'Linen',.001);finish()
start('CM_HR02_StoopFace')
for i,(w,h) in enumerate([(.72,.17),(.83,.18),(.68,.16),(.81,.18),(.75,.17),(.73,.18)]):
 x=-2.26+i*.76;outline('Worn dressed stone',[(x-w/2,-h/2),(x+w/2,-h/2),(x+w/2,h/2-.012),(x+w/2-.04,h/2),(x-w/2+.025,h/2),(x-w/2,h/2-.02)],(-.015,.015),'Ceramic',.012)
finish()
# Export only new authored/derived meshes. Originals on disk never changed.
report={'modules':catalog,'totalTriangles':sum(m['triangles'] for m in catalog),'scaleMetres':1,'axes':'Unity +Y up +Z front','sourceBase':str(lib),'notes':'Purposeful open ink sheets/inlay edges; decorative modules have no colliders.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_HeroRefinement02.blend'))
conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 if '--export-only' in sys.argv and entry['name'] not in sys.argv[sys.argv.index('--export-only')+1:]:continue
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps(report,indent=2));print('HERO02',len(catalog),report['totalTriangles'])
