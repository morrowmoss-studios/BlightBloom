"""Reads the saved source to record FBX first-face material ordering. No geometry edits."""
import bpy,json
from pathlib import Path
H=Path(__file__).parent
bpy.ops.wm.open_mainfile(filepath=str(H/'BW_FamilyCottageA_Style01.blend'))
M=json.loads((H/'GeometryManifest.json').read_text())
for m in M:
 o=bpy.data.objects[m['replacement']]
 m['exportMaterialOrder']=[o.data.materials[i].name for i in dict.fromkeys(p.material_index for p in o.data.polygons)]
(H/'GeometryManifest.json').write_text(json.dumps(M,indent=2))
print([(m['replacement'],m['exportMaterialOrder']) for m in M])
