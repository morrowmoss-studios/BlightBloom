"""Seat frames in real wall reveals and orient roof-deck undersides. New Inn01 only."""
import bpy,bmesh,math
from mathutils import Vector
from pathlib import Path
H=Path(__file__).parent;R=H.parents[4];bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Inn01.blend'));bpy.context.preferences.filepaths.save_version=0
for group in ['Timber','Windows','RoofDeck']:
 o=bpy.data.objects['BW_Inn01_'+group]
 if o.get('RevealAndDeckFinished'):raise RuntimeError('Already finalized')
 bm=bmesh.new();bm.from_mesh(o.data);bm.normal_update()
 if group in ['Timber','Windows']:
  left=set(bm.verts)
  while left:
   v=left.pop();part={v};stack=[v]
   while stack:
    for e in stack.pop().link_edges:
     for q in e.verts:
      if q in left:left.remove(q);part.add(q);stack.append(q)
   pts=[Vector((-q.co.x,q.co.z,-q.co.y)) for q in part];c=sum(pts,Vector())/len(pts);size=Vector([max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)]);move=Vector()
   if group=='Timber':
    if abs(c.z-7.43)<.01 and (abs(c.y-1.25)<.025 or abs(c.y-2.605)<.025):move.z=.13
    if abs(c.z+1.63)<.01 and (abs(c.y-1.15)<.025 or abs(c.y-2.405)<.025):move.z=-.13
   else:
    if .12<size.z<.22 and (abs(c.z-7.52)<.02 or abs(c.z-6.42)<.02):move.z=.06
    if .12<size.z<.22 and abs(c.z+1.72)<.02:move.z=-.06
    if .12<size.x<.22 and abs(c.x+4.52)<.02:move.x=-.06
    if .12<size.x<.22 and abs(c.x-5.02)<.02:move.x=.06
   for q in part:q.co+=Vector((-move.x,-move.z,move.y))
 else:
  flip=[]
  for f in bm.faces:
   if abs(f.normal.z)<.2:continue
   c=f.calc_center_median();x,y,z=-c.x,c.z,-c.y
   if y<4.2:top=3.65-(.85/1.55)*abs(x)
   elif x<1.2:top=8.5+(5.95-8.5)*(x+1.8)/(-4.85+1.8) if x< -1.8 else 8.5+(6.10-8.5)*(x+1.8)/(1.14+1.8)
   else:top=7.25+(6.10-7.25)*(x-3.2)/(1.26-3.2) if x<3.2 else 7.25+(5.45-7.25)*(x-3.2)/(5.35-3.2)
   top+=.014*math.sin(z*.72)+.008*math.sin(x*1.8+z*.7);desired=1 if y>top-.05 else -1
   if f.normal.z*desired<0:flip.append(f)
  bmesh.ops.reverse_faces(bm,faces=flip)
 bm.to_mesh(o.data);bm.free();o.data.normals_split_custom_set([(0,0,0)]*len(o.data.loops));o.data.update();o['RevealAndDeckFinished']=True;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.export_scene.fbx(filepath=str(R/('Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Models/BW_Inn01_'+group+'.fbx')),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Inn01.blend'))
