"""Annotation presentation only. Reuse the unchanged house render; never edit source data."""
import bpy,json,numpy as np,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;file=D/'CM_CrookedMortar_BoundaryMapping01_UNCUT.blend';bpy.ops.wm.open_mainfile(filepath=str(file));s=bpy.context.scene;G=bpy.data.collections['BOUNDARY_MAPPING_ONLY__NO_CUT_NO_EXPORT'];vl=s.view_layers[0]
# Avoid visually misleading through-house diagonals in the three-quarter render.
visible_sides={'Front','Right','Front_Right','Right_Rear','Left_Front'}
for ob in G.all_objects:
 if ob.name.startswith('CONTACT_GUIDE_'):ob.hide_render=ob.get('side') not in visible_sides;ob.show_in_front=False
 elif ob.name.startswith('XY_PROJECTION_'):ob.hide_render=True
 elif ob.name.startswith('REVIEW_'):
  idx=int(ob.name.rsplit('_',1)[-1]);ob.hide_render=idx in [2,4,6]
for ob in G.all_objects:
 if ob.name.startswith('VIEW_'):ob.hide_render=False
bpy.data.objects['VIEW_TITLE'].data.body='OVERVIEW — NEAR-SIDE FOUNDATION BOUNDARY'
bpy.data.objects['VIEW_FOOTNOTE'].data.body='Near-side guides only. See four elevations and underside for the complete proposed loop.'
for mat in bpy.data.materials:
 if mat.name.startswith('GUIDE_ONLY_'):
  em=next(n for n in mat.node_tree.nodes if n.type=='EMISSION');mat.diffuse_color=em.inputs['Color'].default_value
states=[]
for c in vl.layer_collection.children:
 if c.name!=G.name:states.append((c,c.exclude));c.exclude=True
bpy.data.collections['02_XY_Projection_ONLY_Not_UndersideCut'].hide_render=False
s.render.film_transparent=True;s.cycles.samples=4;s.render.filepath=str(D/'Overview_Guides.png');bpy.ops.render.render(write_still=True)
for c,v in states:c.exclude=v
s.render.film_transparent=False;s.cycles.samples=16
for ob in G.all_objects:
 if ob.name.startswith('CONTACT_GUIDE_'):ob.hide_render=False
 elif ob.name.startswith('REVIEW_'):ob.hide_render=False
 elif ob.name.startswith('VIEW_'):ob.hide_render=True
bpy.data.collections['02_XY_Projection_ONLY_Not_UndersideCut'].hide_render=True
# Original geometry / UV / assignments / transforms must still match the recorded baseline.
code=(D/'create_boundary_map.py').read_text();exec(code[code.index('def mesh_hash'):code.index('before=')]);check=json.loads((D/'PreservationValidation.json').read_text());now={n:mesh_hash(bpy.data.objects[n]) for n in check['original_mesh_hashes']};assert now==check['original_mesh_hashes'];assert hashlib.sha256((D.parent/'SeparationInspection_UNCUT.blend').read_bytes()).hexdigest()==check['source_sha256'];bpy.ops.wm.save_as_mainfile(filepath=str(file));print('GUIDE_REFINEMENT_ONLY_GEOMETRY_UNCHANGED')
