"""Refresh only this candidate's packed painting after atlas-crop correction."""
import bpy
from pathlib import Path
H=Path(__file__).parent;bpy.ops.wm.open_mainfile(filepath=str(H/'BW_Chapel01.blend'));bpy.context.preferences.filepaths.save_version=0
for image in bpy.data.images:
 if image.source=='FILE' and 'BW_Chapel01_' in image.name:
  if image.packed_file:image.unpack(method='REMOVE')
  image.reload();image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(H/'BW_Chapel01.blend'))
