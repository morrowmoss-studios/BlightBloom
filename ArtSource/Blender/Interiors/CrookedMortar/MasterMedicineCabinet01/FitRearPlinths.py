"""Project the two plinth rear faces past rear stiles; remove their coplanar exposed intersections."""
import bpy,json
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));bpy.context.preferences.filepaths.save_version=0
for o in bpy.context.scene.objects:
 if o.type=='MESH' and (o.name.startswith('Broad bearing plinth') or o.name.startswith('Lower shelf seated bearing plinth')):
  for v in o.data.vertices:v.co.y=.222+(v.co.y-.222)*(.454/.445)
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));exec((D/'ExportCabinet.py').read_text())
