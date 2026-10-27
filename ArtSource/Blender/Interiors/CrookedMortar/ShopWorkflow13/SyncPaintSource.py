import bpy
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];bpy.ops.wm.open_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'));image=bpy.data.images.load(str(D/'PaintedVesselAtlas.png'));image.pack()
for name,offset in [('Sage',(.53,.53)),('SageVessel',(.53,.53)),('IvoryCeramic',(.02,.53)),('AmberVessel',(.02,.02)),('Paper',(.53,.02))]:
 if 'CM_SW13_'+name not in bpy.data.materials:continue
 m=bpy.data.materials['CM_SW13_'+name];ns=m.node_tree.nodes;lk=m.node_tree.links;bs=ns.get('Principled BSDF');tex=ns.new('ShaderNodeTexImage');tex.image=image;tc=ns.new('ShaderNodeTexCoord');scale=ns.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(.44,.44,1);move=ns.new('ShaderNodeVectorMath');move.operation='ADD';move.inputs[1].default_value=(*offset,0);lk.new(tc.outputs['UV'],scale.inputs[0]);lk.new(scale.outputs[0],move.inputs[0]);lk.new(move.outputs[0],tex.inputs['Vector']);lk.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.95
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_ShopWorkflow13.blend'))
