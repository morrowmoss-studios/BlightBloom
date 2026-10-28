"""Seat rear battens BETWEEN the rear stiles, avoiding coplanar exposed end intersections."""
import bpy
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'));bpy.context.preferences.filepaths.save_version=0
for o in bpy.context.scene.objects:
 if o.type!='MESH' or not o.name.startswith('Rear housed cross batten'):continue
 for v in o.data.vertices:
  v.co.x*=.770/.815;v.co.y=-.232+(v.co.y+.225)/.009*.021
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'))
# Update metrics from final geometry, without rebuilding untouched components.
import json
p=D/'AssetCatalog.json';cat=json.loads(p.read_text());pts=[(v.co.x,v.co.z,v.co.y) for o in bpy.context.scene.objects if o.type=='MESH' for v in o.data.vertices];cat['boundsUnity']={'min':[min(v[i] for v in pts) for i in range(3)],'max':[max(v[i] for v in pts) for i in range(3)]};p.write_text(json.dumps(cat,indent=2))
exec((D/'ExportCabinet.py').read_text())
