"""Local fitted return refinement only; the accepted house reduction is reused unchanged."""
import bpy,numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent
pvs=[(-.171,-.289,.318),(-.100,-.289,.318),(-.100,-.289,.373),(-.103,-.289,.430),(-.138,-.290,.435),(-.171,-.289,.423),(-.175,-.289,.365)]
for file in ['CrookedMortar_RepairedHigh.blend','CrookedMortar_Optimized.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(D/file))
 for ob in bpy.data.objects:
  if ob.type=='MESH' and ob.name.startswith('Fitted_PlasterReturn'):
   for v,co in zip(ob.data.vertices,pvs):v.co=co
   ob.data.update()
 bpy.ops.wm.save_as_mainfile(filepath=str(D/file))
optcol=bpy.data.collections['OPTIMIZED_GAMEPLAY_CANDIDATE'];opt=bpy.data.objects['House_Optimized'];SCALE=15
src=(D/'recover_house.py').read_text();exec(src[src.index('# Export only candidate'):src.index('report=dict')])
