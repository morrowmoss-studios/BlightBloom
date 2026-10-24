"""Fitted artistic composition additions; unchanged architectural envelope and gameplay."""
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4]
text=(R/'ArtSource/Blender/Interiors/CrookedMortar/LivedIn03/build_lived03.py').read_text().split('# Back face is exactly')[0]
text=text.replace("D=Path(__file__).resolve().parent;R=D.parents[4];base=", "D=Path(__file__).resolve().parent;R=D.parents[4];base=").replace("CrookedMortar/LivedIn03'","CrookedMortar/Illustrated04'")
exec(compile(text,str(__file__),'exec'))
art=bpy.data.images.load(str(A/'Textures/CM_Illustrated04_Atlas.png'));art.pack();m=bpy.data.materials.new('CM_IL04_Artwork');m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.95;t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=art;m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);mats['Artwork']=m
# Atlas quadrants, inset to prevent bilinear bleed; +Z surfaces use artist-defined UVs.
def painting(n,p,w,h,q=0):
 x,y,z=p;o=mesh(n,[(x-w/2,y-h/2,z),(x+w/2,y-h/2,z),(x+w/2,y+h/2,z),(x-w/2,y+h/2,z)],[(0,1,2,3)],'Artwork');u,v=[(0,.5),(.5,.5),(0,0),(.5,0)][q]
 for i,(a,b) in enumerate([(0,0),(1,0),(1,1),(0,1)]):o.data.uv_layers[0].data[i].uv=(u+.006+.488*a,v+.006+.488*b)
 
 if n.startswith('Botanical carved panel') or n.startswith('Inset medicinal timber drawer'):
  for loop in o.data.uv_layers[0].data:loop.uv.x=(.345 if x>0 else .006)+(loop.uv.x-.006)*.29
 return o
def inset(n,x,y,z,w,h,q=0):
 box(n+' solid backing',(x,y,z-.014),(w+.035,h+.035,.028),'Walnut',.009);painting(n,(x,y,z+.001),w,h,q)
 for xx in [x-w/2-.017,x+w/2+.017]:box('Shaped panel edge',(xx,y,z+.004),(.03,h+.06,.025),'Walnut',.009)
 for yy in [y-h/2-.017,y+h/2+.017]:box('Moulded panel lip',(x,yy,z+.004),(w+.06,.03,.03),'Walnut',.01)
def scroll(x,y,z,side=1,size=.17):
 pts=[(x+side*size*(.15+.70*i/15)*math.cos(i*math.pi*1.4/15),y+size*(.15+.70*i/15)*math.sin(i*math.pi*1.4/15),z) for i in range(16)];tube('Carved volute',pts,.008,'Walnut')
def foliate(x,y,z,size=.16):
 leaf_inlay(x,y,z,size)
 for sign in [-1,1]:scroll(x+sign*size*.4,y,z,sign,size*.4)
def parcel(x,y,z,w=.26):
 box('Folded prescription packet',(x,y+.04,z),(w,.08,.17),'Linen',.012)
 rod('Hemp wrap',(x-w/2,y+.082,z),(x+w/2,y+.082,z),.004,'Walnut',8);rod('Crossed wrap',(x,y+.082,z-.085),(x,y+.082,z+.085),.004,'Walnut',8)
 lathe('Pressed wax seal',(x+.04,y+.083,z),[(0,.018),(.005,.020)],'Sage',16)
def upright_book(x,y,z,h,w=.08):
 box('Botanical folio paper',(x,y+h/2,z),(w,h,.19),'Linen',.005)
 for side in [-1,1]:box('Shaped leather board',(x+side*w/2,y+h/2,z),( .01,h+.015,.21),'Sage' if x<0 else 'Walnut',.004)
 box('Rounded stitched spine',(x,y+h/2,z+.10),(w+.012,h,.025),'Walnut',.009)
 for yy in [y+.05,y+h-.05]:box('Raised gilt binding',(x,yy,z+.117),(w+.01,.012,.007),'Brass',.002)
 foliate(x,y+h*.52,z+.119,w*.8)
# Fitted over existing customer-facing panel, leaving structure, drawers and footprint intact.
start('CM_IL04_CounterCarving')
inset('Mortar carved panel',0,.56,.437,.67,.54,0)
for x in [-.74,.74]:
 inset('Botanical carved panel',x,.56,.437,.53,.54,0)
for x in [-1.055,-.365,.365,1.055]:
 for y in [.23,.88]:box('Faceted joinery boss',(x,y,.44),(.09,.08,.04),'Walnut',.018);foliate(x,y,.465,.065)
finish()
# Articulated furniture profiles, not a replacement for the existing shelving.
start('CM_IL04_ShelfCarving')
for x in [-.89,.89]:
 for y in [.3,.87,1.5,2.06]:scroll(x,y,.207,1 if x>0 else -1,.085)
 for yy in [.52,.98,1.44,1.9]:
  outline('Scalloped shelf knee',[(x-.04,yy),(x+.04,yy),(x+.04,yy-.12),(x,yy-.18),(x-.04,yy-.10)],(.18,.22),'Walnut',.005)
for y in [.48,.94,1.40,1.86]:box('Rounded shelf front bead',(0,y,.205),(1.7,.025,.028),'Walnut',.009)
finish()
# Two curated replacement shelf courses: stored orders and well-used reference books.
for num in [1,3]:
 start('CM_IL04_WorkingCollection'+str(num))
 if num==1:
  for i,(x,h) in enumerate([(-.66,.31),(-.55,.28),(-.45,.34),(-.34,.30)]):upright_book(x,.005,.005,h,.085)
  for j in range(3):book(.01,.005+j*.05,.005,.30-j*.02,.04,.19,'Sage' if j%2 else 'Walnut')
  parcel(.39,.005,0,.25);parcel(.42,.086,-.01,.21)
  bottle(.67,.005,-.01,.25,.055,1)
 else:
  for j in range(3):book(-.5,.005+j*.055,0,.34-j*.025,.045,.22,'Walnut' if j%2 else 'Sage')
  for x,h in [(-.17,.29),(-.06,.34),(.05,.27),(.16,.32)]:upright_book(x,.005,0,h,.09)
  bottle(.42,.005,.0,.30,.065,2);parcel(.68,.005,0,.19)
 finish()
# A broad botanical drape, with a free hem formed in geometry, and actual tabletop contact.
start('CM_IL04_CounterRunner')
vs=[]
for j,(z,y) in enumerate([(-.22,1.055),(.12,1.055),(.36,1.055),(.405,.98),(.43,.67)]):
 for i,x in enumerate([-.21,0,.21]):vs.append((x+.48,y+.004*math.cos(i*1.6),z))
o=mesh('Woven working runner',vs,[(j*3+i,j*3+i+1,(j+1)*3+i+1,(j+1)*3+i) for j in range(4) for i in range(2)],'Artwork');uv=o.data.uv_layers[0]
for face in o.data.polygons:
 for li in face.loop_indices:
  vi=o.data.loops[li].vertex_index;j,i=divmod(vi,3);uv.data[li].uv=(.006+.488*i/2,.006+.488*(1-j/4))
for i in range(9):rod('Woven hem fringe',(.285+i*.049,.675,.432),(.285+i*.049,.64+.008*(i%3),.435),.0028,'Linen',6)
finish()
# Pinned botanical wall working archive; rear face z=0 seats against verified wall.
start('CM_IL04_BotanicalArchive',None,[['WallBack',[0,0,0]]])
box('Pegged hanging rail',(0,.43,.022),(.76,.065,.044),'Walnut',.012)
for x in [-.32,.32]:rod('Driven wooden peg',(x,.43,-.006),(x,.43,.065),.012,'Walnut',12)
for x,y,w,h in [(-.19,.07,.34,.61),(.18,-.03,.32,.60)]:
 box('Thick handmade botanical paper',(x,y,.024),(w,h,.007),'Linen',.003);painting('Painted herb study',(x,y,.028),w,h,1)
 rod('Paper pin',(x,y+h*.45,.028),(x,y+h*.45,.038),.006,'Brass',10)
finish()
# Three shallow working nooks fitted to existing jambs, not across the stair opening.
start('CM_IL04_JambDetail',None,[['WallBack',[0,0,0]]])
box('Hand planed jamb stile',(0,1.32,.026),(.10,2.64,.052),'Walnut',.013)
for yy in [.06,2.68]:
 box('Jamb foot and cap',(0,yy,.034),(.15,.12,.068),'Walnut',.013);foliate(0,yy,.073,.08)
outline('Carved upper corbel',[(-.05,2.72),(.19,2.72),(.16,2.67),(.10,2.62),(.04,2.49),(-.05,2.46)],(0,.12),'Walnut',.009)
finish()
start('CM_IL04_Header',None,[['WallBack',[0,0,0]]])
box('Moulded lintel',(0,0,.036),(1.92,.12,.072),'Walnut',.015)
for x in [-.84,.84]:foliate(x,0,.078,.085)
inset('Botanical lintel cartouche',0,0,.079,.38,.095,2);finish()
# Cabinet and side table craft: broad profiles and illustrated panels, no new furniture footprint.
start('CM_IL04_PrepTableCraft')
for x in [-.69,.69]:
 outline('Carved knee bracket',[(x,.89),(x-.13*(1 if x>0 else -1),.89),(x-.10*(1 if x>0 else -1),.82),(x,.62)],(.22,.29),'Walnut',.008)
for x in [-.35,.35]:inset('Inset medicinal timber drawer',x,.78,.335,.53,.12,0)
box('Turned table nosing',(0,.91,.346),(1.52,.035,.045),'Walnut',.014);finish()
start('CM_IL04_PreparationRecords')
parcel(-.30,0,0,.28);book(.04,.006,0,.24,.035,.18,'Sage');book(.07,.05,-.01,.23,.035,.17,'Walnut');bottle(.32,.0,0,.24,.048,0);finish()
# One shallow wall-mounted textile with top rod, suspended by its sewn loops.
start('CM_IL04_HerbalBanner',None,[['WallBack',[0,0,0]]])
rod('Banner rail',(-.36,.46,.035),(.36,.46,.035),.017,'Walnut',16)
for x in [-.27,.27]:
 rod('Banner wall peg',(x,.46,-.005),(x,.46,.052),.013,'Iron',12);box('Sewn banner loop',(x,.42,.039),(.035,.12,.012),'Linen',.003)
vs=[(-.30,.40,.04),(.30,.40,.04),(.30,-.33,.048),(.21,-.40,.044),(-.09,-.37,.045),(-.30,-.39,.048)]
o=mesh('Painted botanical hanging',vs,[(0,1,2,3,4,5)],'Artwork');uv=o.data.uv_layers[0]
for face in o.data.polygons:
 for li in face.loop_indices:
  v=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(.506+.488*(v.x+.30)/.60,.506+.488*(v.z+.4)/.8)
finish()
# Flat, shaped woven carpets. No physics added to 4mm floor textiles.
start('CM_IL04_WovenMat',None,[['Floor',[0,0,0]]])
o=mesh('Botanical woven floor runner',[(-.65,.004,-1),(.65,.004,-1),(.67,.004,.85),(.61,.004,1),(-.66,.004,1)],[(0,1,2,3,4)],'Artwork')
for f in o.data.polygons:
 for li in f.loop_indices:
  v=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers[0].data[li].uv=(.006+.488*(v.x+.67)/1.34,.006+.488*(v.y+1)/2)
for sign in [-1,1]:
 for i in range(18):rod('Woven rug fringe',(-.61+i*.07,.004,sign*.98),(-.61+i*.07,.004,sign*1.04),.002,'Linen',6)
finish()
# Exterior fitted cosmetic timber network: all back faces sit on the front gable plane.
start('CM_IL04_FrontCraftwork')
# Queen-post fan echoes the existing hero gable without changing its shape.
for side in [-1,1]:
 rod('Fitted gable fan brace',(2.7,8.42,-.323),(2.7+side*1.30,8.0,-.323),.065,'Walnut',12)
for x in [.12,5.28]:
 pts=[(x-.075,6.66),(x+.075,6.66),(x+.075,6.25),(x-.075,6.40)]
 outline('Carved gable bearing',pts,(-.36,-.294),'Walnut',.009)
 box('Gable bearing cap',(x,6.66,-.33),(.23,.10,.09),'Walnut',.012)
inset('Gable apothecary emblem',2.7,8.50,-.34,1.10,.80,0);painting('Outward painted gable emblem',(2.7,8.50,-.372),1.10,.80,0)
# A pair of front ground-floor corbels seats against the left/right wall timber.
for x,side in [(.10,1),(5.30,-1)]:
 outline('Front carved beam knee',[(x+side*dx,y) for dx,y in [(-.06,3.24),(.34,3.24),(.29,3.16),(.12,3.04),(.06,2.88),(-.06,2.88)]],(-.39,-.203),'Walnut',.012)
 foliate(x,3.11,-.397,.12)
finish()
# Plaster patches are backed, localised and deliberately irregular, not floating decals.
start('CM_IL04_LimewashRepair',None,[['WallBack',[0,0,0]]])
vs=[(-.34,-.27,.003),(.20,-.31,.003),(.32,-.12,.003),(.27,.27,.003),(-.18,.30,.003),(-.32,.11,.003)];o=mesh('Repaired lime field',vs,[tuple(range(6))],'Artwork')
for f in o.data.polygons:
 for li in f.loop_indices:
  v=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers[0].data[li].uv=(.506+.488*(v.x+.34)/.68,.006+.488*(v.z+.31)/.61)
finish()
# Shaped timber architrave for the actual arched preparation window. Back datum at wall.
start('CM_IL04_ArchedWindowLining',None,[['WallBack',[0,0,0]]])
for side in [-1,1]:
 x=side*.855
 box('Window side lining',(x,1.425,.027),(.09,.65,.054),'Walnut',.018)
 box('Lining foot',(x,1.10,.032),(.14,.12,.064),'Walnut',.014)
 foliate(x,1.37,.060,.08)
# Continuous curved band, open centre. Fits outer edge; never a second flat window panel.
N=32;vs=[]
for z in [0,.055]:
 for r in [.81,.90]:
  for i in range(N+1):
   a=math.pi*i/N;vs.append((r*math.cos(a),1.75+r*.81*math.sin(a),z))
K=N+1;fs=[]
for i in range(N):
 fs.extend([(i,i+1,K+i+1,K+i),(2*K+i,3*K+i,3*K+i+1,2*K+i+1),(i,2*K+i,2*K+i+1,i+1),(K+i,K+i+1,3*K+i+1,3*K+i)])
fs.extend([(0,K,3*K,2*K),(N,2*K+N,3*K+N,K+N)])
mesh('Continuous arched window bead',vs,fs,'Walnut',.008)
box('Interior sill nosing',(0,1.04,.045),(1.9,.065,.09),'Walnut',.02)
for x in [-.64,.64]:outline('Sill carved corbel',[(x-.045,1.01),(x+.045,1.01),(x+.04,.86),(x,.81),(x-.045,.91)],(0,.09),'Walnut',.008)
finish()
# Front rectangular window brackets fitted beneath the existing paired sill.
start('CM_IL04_WindowConsole',None,[['WallBack',[0,0,0]]])
outline('Curved window console',[(-.065,0),(.065,0),(.065,-.28),(.025,-.39),(-.025,-.32),(-.065,-.15)],(0,.30),'Walnut',.014)
for y in [-.07,-.2]:foliate(0,y,.308,.09)
box('Window bracket cap',(0,.025,.16),(.20,.05,.35),'Walnut',.012);finish()
report={'modules':catalog,'axes':'Unity +Y up +Z exterior','scaleMetres':1,'notes':'Fitted room composition accents; no collision geometry exported; existing approved material assignments retained outside new additions.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_Illustrated04.blend'));conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 if '--export-only' in sys.argv and entry['name'] not in sys.argv[sys.argv.index('--export-only')+1:]:continue
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps(report,indent=2));print('ILLUSTRATED04_READY',len(catalog))
