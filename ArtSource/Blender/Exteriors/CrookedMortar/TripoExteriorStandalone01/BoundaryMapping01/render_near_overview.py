import bpy,json,numpy as np,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;f=D/'CM_CrookedMortar_BoundaryMapping01_UNCUT.blend';bpy.ops.wm.open_mainfile(filepath=str(f));s=bpy.context.scene;vl=s.view_layers[0];tmp=bpy.data.collections.new('TEMP_NearSide_RenderSelection');s.collection.children.link(tmp);sides={'Front','Right','Front_Right','Right_Rear','Left_Front'};chosen=[]
for ob in list(bpy.data.objects):
 keep=ob.name.startswith('CONTACT_GUIDE_') and ob.get('side') in sides
 if ob.name.startswith('REVIEW_'):keep=int(ob.name.rsplit('_',1)[-1]) in [0,1,3,5]
 if ob.name.startswith('VIEW_'):keep=True
 if keep:tmp.objects.link(ob);ob.hide_render=False;chosen.append(ob)
bpy.data.objects['VIEW_TITLE'].data.body='OVERVIEW — NEAR-SIDE FOUNDATION BOUNDARY';bpy.data.objects['VIEW_FOOTNOTE'].data.body='Near-side guides only. See elevations and underside for the complete proposed loop.'
states=[]
for c in vl.layer_collection.children:
 if c.name!=tmp.name:states.append((c,c.exclude));c.exclude=True
s.render.film_transparent=True;s.cycles.samples=4;bpy.context.view_layer.update();print('OVERVIEW_SELECTED',[(o.name,o.get('side')) for o in chosen],flush=True);s.render.filepath=str(D/'Overview_Guides.png');bpy.ops.render.render(write_still=True)
for c,v in states:c.exclude=v
bpy.data.collections.remove(tmp)
for ob in list(bpy.data.objects):
 if ob.name.startswith('VIEW_'):ob.hide_render=True
s.render.film_transparent=False;s.cycles.samples=16
code=(D/'create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);check=json.loads((D/'PreservationValidation.json').read_text());assert {n:mesh_hash(bpy.data.objects[n]) for n in check['original_mesh_hashes']}==check['original_mesh_hashes'];bpy.ops.wm.save_as_mainfile(filepath=str(f))
