import bpy,math,json
from pathlib import Path
from mathutils import Vector
D=Path(__file__).resolve().parent;OUT=D/'Comparisons';OUT.mkdir(exist_ok=True)
views=[('FrontThreeQuarter',(16,-29,17),(0,0,4.8),22,True),('FrontEntrance',(7,-18,5),(0,-4.5,2.5),7,True),('Side',(25,-4,12),(0,0,4.8),22,True),('Rear',(-15,26,15),(0,0,4.8),22,True),('RoofAbove',(14,-16,32),(0,0,5),23,True),('SignClose',(4,-8,4.7),(-.84,-6.38,4.02),2.5,True),('GameplayDistance',(6,-18,1.7),(0,-2.5,4),48,False),('RoofDetail',(7,-10,14),(0,-2,7.3),7,True),('TimberDetail',(4,-11,3),(-1.7,-5.15,2.4),3.5,True),('FoliageDetail',(13,-7,7),(3.0,-1.7,4.1),4.3,True),('WindowsDetail',(6,-12,7.4),(0,-4.2,5.8),5,True)]
for label,file in [('Original','OriginalReference.blend'),('Repaired','CrookedMortar_RepairedHigh.blend'),('Optimized','CrookedMortar_Optimized.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(D/file));s=bpy.context.scene
 if label=='Original':
  for ob in s.objects:ob.scale*=15
 for c in bpy.data.collections:
  if c.name.startswith('ORIGINAL'):c.hide_render=label!='Original'
  if c.name=='REPAIRED_HIGH_DETAIL':c.hide_render=label!='Repaired'
  if c.name=='OPTIMIZED_GAMEPLAY_CANDIDATE':c.hide_render=label!='Optimized'
 s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0;s.view_settings.gamma=1
 s.world=bpy.data.worlds.new('MatchedNeutralWorld');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
 center=Vector((0,0,4.87));span=14.72
 for pos,power in [((-2,-3,4),500),((3,-1,2),250),((1,3,3),350)]:
  ld=bpy.data.lights.new('MatchedArea','AREA');ld.energy=power*span**2;ld.shape='DISK';ld.size=span*2;ob=bpy.data.objects.new(ld.name,ld);s.collection.objects.link(ob);ob.location=center+Vector(pos)*span;ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler()
 cd=bpy.data.cameras.new('MatchedCamera');cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);s.camera=cam;cd.clip_start=.01;cd.clip_end=500
 for name,pos,target,fov,ortho in views:
  path=OUT/f'{label}_{name}.png'
  if path.exists():continue
  cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO' if ortho else 'PERSP'
  if ortho:cd.ortho_scale=fov
  else:cd.lens=36/math.tan(math.radians(fov)/2)/2
  s.render.filepath=str(path);bpy.ops.render.render(write_still=True);print('RENDERED',label,name,flush=True)
 (OUT/'CameraManifest.json').write_text(json.dumps(dict(views=views,samples=16,exposure=0,look='AgX Medium High Contrast',shared_lighting=True),indent=2))
