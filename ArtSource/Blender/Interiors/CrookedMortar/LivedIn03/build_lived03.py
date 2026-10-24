"""Room-specific authored details with wall-back and surface datums. No architecture regeneration."""
from pathlib import Path
import sys
D=Path(__file__).resolve().parent;R=D.parents[4];base=R/'ArtSource/Blender/Interiors/CrookedMortar/ApothecaryFurnishings01'
text=(base/'build_furnishings01.py').read_text().split('# Counter:')[0].replace("CrookedMortar/ApothecaryFurnishings01'","CrookedMortar/LivedIn03'").replace("A/'Textures/CM_AF01_BotanicalLabels.png'","R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/HeroRefinement02/Textures/CM_HR02_InkArtwork.png'")
exec(compile(text,str(__file__),'exec'))
paint2=bpy.data.images.load(str(R/'Assets/BlightBloom/Art/Interiors/CrookedMortar/HeroRefinement02/Textures/CM_HR02_PaintedSheet.png'));paint2.pack()
for node in mats['Walnut'].node_tree.nodes:
 if node.type=='TEX_IMAGE':node.image=paint2
old_label=label
def label(*a,**k):
 o=old_label(*a,**k)
 for l in o.data.uv_layers[0].data:
  mid=(math.floor(l.uv.x*4)+.5)/4;l.uv.x=2*mid-l.uv.x
 return o
def outline(n,pts,depth,k='Walnut',b=.006):
 N=len(pts);return mesh(n,[(x,y,z) for z in depth for x,y in pts],[tuple(reversed(range(N))),tuple(range(N,N*2))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)],k,b)
def book(x,y,z,w,h,d,k='Sage'):
 box('Hand stitched binding',(x,y+h/2,z),(w,h,d),k,.006);box('Paper fore-edge',(x,y+h/2,z+.006),(w-.014,h-.014,d-.015),'Linen',.002)
 for yy in [y+.005,y+h-.005]:box('Cover board',(x,yy,z),(w+.008,.010,d+.009),k,.003)
 for xx in [x-w*.3,x+w*.3]:box('Binding raised band',(xx,y+h/2,z-d/2-.005),(.018,h,.01),'Walnut',.002)
def bottle(x,y,z,h,r,i):
 lathe('Infusion vessel',(x,y,z),[(0,r*.65),(.06*h,r),(.60*h,r),(.73*h,r*.70),(.80*h,r*.4),(.95*h,r*.4)],'Glass',28);lathe('Cork',(x,y,z),[(h*.92,r*.44),(h,r*.40)],'Walnut',16);lathe('Infusion',(x,y,z),[(.025,r*.8),(.47*h,r*.85)],'Sage',24);label('Recorded contents',(x,y+h*.4,z+r*1.02),r*1.4,h*.3,i)
# Back face is exactly z=0; all modules use an explicit wall/surface datum.
start('CM_LI03_RecordShelf',[[0,.38,.14],[1.28,.76,.28]],[['WallBack',[0,.38,0]]])
box('Backboard',(0,.38,.02),(1.28,.76,.04),'Sage',.009)
for x in [-.62,.62]:
 outline('Shaped console cheek',[(x-.025,0),(x+.025,0),(x+.025,.65),(x,.75),(x-.025,.65)],(0,.26),'Walnut',.006)
for y in [.08,.40,.74]:box('Lipped ledge',(0,y,.14),(1.28,.04,.28),b=.012);box('Shelf retaining bead',(0,y+.035,.278),(1.22,.04,.025),b=.009)
for i,(x,w,h) in enumerate([(-.43,.22,.055),(-.41,.24,.045),(-.39,.25,.05)]):book(x,.105+i*.06,.14,w,h,.22,'Walnut' if i==0 else 'Sage')
for x in [-.12,.06,.22]:
 box('Bound patient case',(x,.24,.15),(.11,.25,.19),'Sage' if x<.1 else 'Walnut',.006);label('Case index',(x,.25,.25),.075,.13,6)
bottle(.47,.105,.14,.23,.055,2)
label('Robert case ledger',(0,.58,.048),1.06,.23,4)
# Pegs seat through the board, not floating at a guessed world position.
for x in [-.5,.5]:rod('Wall fixing peg',(x,.66,.0),(x,.66,.052),.012,'Iron',10)
finish()
start('CM_LI03_ReagentCabinet',[[0,.70,.16],[1.18,1.40,.32]],[['WallBack',[0,.7,0]]])
box('Cabinet planked back',(0,.72,.025),(1.16,1.40,.05),'Sage',.012)
for x in [-.56,.56]:box('Carved upright',(x,.7,.16),(.07,1.40,.30),b=.012)
for y in [.08,.52,.96,1.38]:box('Shelf nosing',(0,y,.16),(1.18,.06,.32),b=.015)
outline('Raised curved crown',[(-.60,1.38),(.60,1.38),(.60,1.44),(.42,1.45),(.22,1.52),(0,1.56),(-.22,1.52),(-.42,1.45),(-.60,1.44)],(0,.29),'Walnut',.009)
for i,(x,y,h) in enumerate([(-.36,.115,.31),(0,.115,.24),(.35,.115,.33),(-.38,.555,.28),(.0,.555,.32),(.37,.555,.26),(-.33,.995,.30),(.13,.995,.24),(.40,.995,.32)]):bottle(x,y,.16,h,.07 if i%3 else .085,i%4)
# Differing fitted cubby divisions and a drawer: related but deliberately not a perfect grid.
for x,y,h in [(-.15,.29,.38),(.22,.74,.38),(-.03,1.18,.34)]:box('Fitted partition',(x,y,.15),(.025,h,.28),b=.005)
for x in [-.51,.51]:rod('Drawbore anchor',(x,1.31,0),(x,1.31,.32),.012,'Linen',10)
finish()
start('CM_LI03_ToolRail',None,[['WallBack',[0,0,0]]])
box('Beaded instrument rail',(0,0,.025),(1.12,.11,.05),'Walnut',.015)
for j,(x,length) in enumerate([(-.42,.28),(-.08,.35),(.29,.23)]):
 tube('Forged hook',[(x,0,.03),(x,0,.10),(x,-.035,.12),(x,-.065,.10)],.009,'Iron')
 rod('Tool suspension',(x,-.045,.10),(x,-length,.10),.006,'Iron',10)
 if j==0:lathe('Hanging measure',(x,-length-.08,.10),[(0,.04),(.07,.055),(.08,.05),(.02,.025)],'Brass',24)
 elif j==1:
  rod('Pestle grip',(x,-length+.03,.10),(x,-length-.12,.10),.018,'Walnut',16)
 else:
  outline('Wide herb knife',[(x-.01,-length+.06),(x+.025,-length+.06),(x+.07,-length-.08),(x-.04,-length-.08)],(.088,.107),'Iron',.002)
for x in [-.5,.5]:rod('Anchored fixing',(x,0,0),(x,0,.06),.012,'Iron',10)
finish()
for name,L in [('CM_LI03_ShopBeam',5.4),('CM_LI03_PrepBeam',3.4)]:
 start(name,None,[['CeilingTop',[0,.08,0]],['WallL',[-L/2,0,0]],['WallR',[L/2,0,0]]])
 box('Continuous hand planed beam',(0,0,0),(L,.16,.17),'Walnut',.015)
 for sign in [-1,1]:
  x=sign*(L/2-.06)
  box('Wall bearing pad',(x,-.13,0),(.10,.40,.22),'Walnut',.015)
  pts=[(x-.05,-.07),(x+.05,-.07),(x+.05,-.32),(x,-.29),(x-.05,-.16)]
  outline('Scalloped bearing corbel',pts,(-.12,.12),'Walnut',.009)
  for z in [-.095,.095]:rod('Timber peg',(x,-.13,z-.004),(x,-.13,z+.004),.012,'Linen',10)
 finish()
start('CM_LI03_WorkSurfaceStory',None,[['Surface',[0,0,0]]])
# At workbench scale: a cloth lies on the surface and drapes only over its front lip.
vs=[];xs=[-.35,-.15,.15,.35];zs=[-.22,0,.25,.35,.38]
for j,z in enumerate(zs):
 for i,x in enumerate(xs):vs.append((x,.003+(0 if j<3 else -.10*(j-2))+.003*math.sin(i*1.5),z))
fs=[(j*4+i,j*4+i+1,(j+1)*4+i+1,(j+1)*4+i) for j in range(4) for i in range(3)];o=mesh('Working linen',vs,fs,'Linen');bpy.context.view_layer.objects.active=o;mod=o.modifiers.new('Woven thickness','SOLIDIFY');mod.thickness=.003;bpy.ops.object.modifier_apply(modifier=mod.name)
box('Herb pressing board',(-.05,.035,-.03),(.42,.055,.31),'Walnut',.012)
# Pressed medicinal leaves have broad useful silhouettes; they rest on the board.
for j,(x,z) in enumerate([(-.17,-.07),(-.08,-.02),(.04,.02),(.12,-.05)]):
 rod('Laid herb stem',(x,.065,z-.07),(x+.015,.065,z+.08),.003,'Sage',8)
 for sign in [-1,1]:mesh('Prepared sage leaf',[(x,.066,z),(x+sign*.05,.071,z+.03),(x+sign*.08,.065,z+.07),(x+sign*.02,.065,z+.065)],[(0,1,2,3)],'Sage')
# Portable herb press: readable upper frame, a wooden screw and an offset hand lever.
for x in [-.24,.14]:box('Herb press upright',(x,.20,-.03),(.035,.34,.045),'Walnut',.007)
box('Bow-edged press crossbar',(-.05,.37,-.03),(.48,.055,.08),'Walnut',.014)
rod('Wooden press screw',(-.05,.13,-.03),(-.05,.44,-.03),.014,'Walnut',16)
for y in [.25,.29,.33,.40]:lathe('Screw thread suggestion',(-.05,y,-.03),[(0,.018),(.008,.018)],'Walnut',16)
box('Pressing plate',(-.05,.15,-.03),(.33,.025,.24),'Walnut',.007);rod('Cross handle',(-.14,.44,-.03),(.06,.44,-.03),.009,'Walnut',12)
book(.22,.008,-.11,.12,.025,.15,'Walnut');finish()
start('CM_LI03_WorkbenchJoinery',None,[['BenchDatum',[0,0,0]]])
for sign in [-1,1]:
 x=sign*1.47
 outline('Carved knee brace',[(x,.87),(x-sign*.26,.87),(x-sign*.22,.82),(x-sign*.11,.76),(x-sign*.04,.63),(x,.57)],(.20,.27),'Walnut',.008)
 for y in [.28,.60]:box('Side joinery rail',(sign*1.52,y,0),(.025,.035,.49),'Walnut',.006)
 rod('End pin',(x,.83,.275),(x,.83,.30),.012,'Linen',10)
box('Under-drawer beading',(0,.655,.30),(2.98,.027,.035),'Walnut',.010)
for x in [-1.38,1.38]:leaf_inlay(x,.765,.346,.10)
finish()
start('CM_LI03_FieldNotebook',None,[['Surface',[0,0,0]]]);box('Worn cover',(0,.018,0),(.31,.036,.24),'Walnut',.008);o=label('Preparation notes',(0,0,0),.28,.21,4)
for v in o.data.vertices:v.co=Vector((v.co.x,v.co.z,v.co.y+.039))
rod('Wax pencil',(-.09,.045,.13),(.11,.045,.12),.007,'Walnut',10);finish()
start('CM_LI03_FormularyBoard',None,[['WallBack',[0,0,0]]]);box('Framed working formulary',(0,0,.022),(.84,.50,.044),'Walnut',.009);label('Robert preparation notes',(0,0,.047),.78,.44,4)
for x in [-.37,.37]:rod('Driven fixing',(x,.20,0),(x,.20,.053),.009,'Iron',10)
finish()
start('CM_LI03_BeamHook',None,[['CeilingMount',[0,0,0]],['HerbLoop',[0,-.08,0]]]);tube('Forged beam hook',[(0,.028,0),(0,-.045,0),(.025,-.068,0),(.023,-.086,0),(0,-.089,0),(-.012,-.073,0)],.007,'Iron');lathe('Driven washer',(0,-.003,0),[(0,.022),(.005,.022)],'Iron',16);finish()
report={'modules':catalog,'totalTriangles':sum(m['triangles'] for m in catalog),'scaleMetres':1,'axes':'Unity +Y up +Z front','notes':'WallBack and Surface datums are explicit. New fixed wall furniture gets simple purposeful colliders; small dressing does not.'}
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_LivedIn03.blend'));conversion=Matrix.Rotation(math.pi,4,'Z')
for entry in catalog:
 if '--export-only' in sys.argv and entry['name'] not in sys.argv[sys.argv.index('--export-only')+1:]:continue
 o=bpy.data.objects[entry['name']];o.matrix_world=conversion@o.matrix_world;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(A/'Models'/(entry['name']+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
(D/'AssetCatalog.json').write_text(json.dumps(report,indent=2));print('LIVED03_READY',len(catalog))
