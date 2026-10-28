import bpy,json,hashlib
import numpy as np
from pathlib import Path
D=Path(__file__).resolve().parent;src=D.parent/'TripoCabinetRecovery01/CabinetB/CabinetB.blend'
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1
# A new asset-only scene, neither source collection is modified on disk.
for ob in list(bpy.data.objects):
 if ob.name!='CabinetB_Optimized':bpy.data.objects.remove(ob,do_unlink=True)
o=bpy.data.objects['CabinetB_Optimized'];o.name='CM_BotanicalCabinet_Style02'
for c in list(o.users_collection):c.objects.unlink(o)
c=bpy.data.collections.new('STYLE02_ASSET');s.collection.children.link(c);c.objects.link(o);c.hide_render=False;c.hide_viewport=False
bpy.context.view_layer.objects.active=o;o.select_set(True)
old=o.data.materials[0];m=old.copy();m.name='CM_Cabinet_WalnutPaint_Style02_Working';o.data.materials[0]=m;n=m.node_tree.nodes;l=m.node_tree.links
bs=n.get('Principled BSDF');base=next(x for x in n if x.type=='TEX_IMAGE' and 'basecolor' in x.image.name);normal=next(x for x in n if x.type=='NORMAL_MAP');rm=next(x for x in n if x.type=='TEX_IMAGE' and '_rm' in x.image.name)
# Keep original source artwork packed for recoverability in the editable working material.
def node(t,name):x=n.new(t);x.label=name;return x
def math(op,a,b=None):
 x=node('ShaderNodeMath',op);x.operation=op
 if hasattr(a,'node'):l.new(a,x.inputs[0])
 else:x.inputs[0].default_value=a
 if b is not None:
  if hasattr(b,'node'):l.new(b,x.inputs[1])
  else:x.inputs[1].default_value=b
 return x.outputs[0]
def mix(a,b,f,name):
 x=node('ShaderNodeMixRGB',name)
 for val,i in [(f,0),(a,1),(b,2)]:
  if hasattr(val,'node'):l.new(val,x.inputs[i])
  else:x.inputs[i].default_value=val
 return x.outputs[0]
sep=node('ShaderNodeSeparateColor','Original palette masks');sep.mode='HSV';l.new(base.outputs['Color'],sep.inputs[0]);h,sat,val=sep.outputs[:]
wood=math('MULTIPLY',math('LESS_THAN',h,.115),math('GREATER_THAN',h,.006));wood=math('MULTIPLY',wood,math('GREATER_THAN',sat,.30));wood=math('MULTIPLY',wood,.52)
# Object-space hand-painted grain: broad directional strokes, not noise. Long stroke direction follows timber roles.
texco=node('ShaderNodeTexCoord','Metre-scale material coordinates');sepp=node('ShaderNodeSeparateXYZ','Grain direction by construction zone');l.new(texco.outputs['Object'],sepp.inputs[0]);x,y,z=sepp.outputs[:]
absx=math('ABSOLUTE',x);post=math('GREATER_THAN',absx,.86);high=math('GREATER_THAN',z,1.60);shelfzone=math('GREATER_THAN',z,.70);horizontal=math('MAXIMUM',high,math('MULTIPLY',shelfzone,math('SUBTRACT',1,post)))
# A vertical grain texture uses image Y for long strokes: fronts/rails horizontal, stiles vertical.
cv=node('ShaderNodeCombineXYZ','Post grain X/Z');l.new(math('MULTIPLY',x,1.8),cv.inputs[0]);l.new(math('MULTIPLY',z,.8),cv.inputs[1])
ch=node('ShaderNodeCombineXYZ','Rail grain Z/X');l.new(math('MULTIPLY',z,1.8),ch.inputs[0]);l.new(math('MULTIPLY',x,.8),ch.inputs[1])
vect=node('ShaderNodeMixRGB','Structural grain direction');l.new(horizontal,vect.inputs[0]);l.new(cv.outputs[0],vect.inputs[1]);l.new(ch.outputs[0],vect.inputs[2])
grain=node('ShaderNodeTexImage','Hand-painted walnut source');grain.image=bpy.data.images.load(str(D/'Textures/Walnut_Painted_Source.png'));grain.extension='REPEAT';l.new(vect.outputs[0],grain.inputs[0])
# Tonal modulation retains the old construction shadows and relief without the original brittle scratch contrast.
bw=node('ShaderNodeRGBToBW','Existing construction values');l.new(base.outputs['Color'],bw.inputs[0]);fac=math('ADD',.32,math('MULTIPLY',bw.outputs[0],2.8));multi=node('ShaderNodeMixRGB','Painted grain with retained construction values');multi.blend_type='MULTIPLY';multi.inputs[0].default_value=1;l.new(grain.outputs[0],multi.inputs[1]);l.new(fac,multi.inputs[2])
paint=mix(base.outputs[0],multi.outputs[0],wood,'Walnut painted layer over registered atlas')
hsv=node('ShaderNodeHueSaturation','Restrained storybook saturation');hsv.inputs['Saturation'].default_value=.84;hsv.inputs['Value'].default_value=1.03;l.new(paint,hsv.inputs['Color'])
color=hsv.outputs[0]
# Compact sage harmony only in existing green pixels; no new plants or stock.
green=math('MULTIPLY',math('GREATER_THAN',h,.15),math('LESS_THAN',h,.43));green=math('MULTIPLY',green,.12)
color=mix(color,(.075,.115,.038,1),green,'Restrained sage botanical tint')
l.new(color,bs.inputs['Base Color']);normal.inputs['Strength'].default_value=.32
bs.inputs['Roughness'].default_value=.82
for link in list(bs.inputs['Roughness'].links):l.remove(link)
for link in list(bs.inputs['Metallic'].links):l.remove(link)
bs.inputs['Metallic'].default_value=.08;bs.inputs['Specular IOR Level'].default_value=.25
# Two-stage bake: geometry contributes only broad grain. Original registered color
# is graded in a flat UV-domain pass, avoiding reprojection drift on fragmented UVs.
out=next(x for x in n if x.type=='OUTPUT_MATERIAL');emit=node('ShaderNodeEmission','Bake color without illumination');l.new(grain.outputs[0],emit.inputs['Color']);l.new(emit.outputs[0],out.inputs['Surface'])
gimg=bpy.data.images.new('CM_Cabinet_Style02_GrainUV',width=4096,height=4096,alpha=False);gimg.colorspace_settings.name='sRGB';gimg.generated_color=(.16,.08,.035,1)
gtarget=node('ShaderNodeTexImage','GRAIN_BAKE_TARGET');gtarget.image=gimg
for nd in n:nd.select=False
gtarget.select=True;n.active=gtarget;s.render.bake.margin=0;s.render.bake.use_clear=False;bpy.ops.object.bake(type='EMIT')
gimg.filepath_raw=str(D/'Textures/CM_Cabinet_Style02_GrainUV.png');gimg.file_format='PNG';gimg.save();gimg.pack()
glookup=node('ShaderNodeTexImage','Registered broad grain layer');glookup.image=gimg;l.new(glookup.outputs[0],multi.inputs[1]);l.new(color,emit.inputs['Color'])
atlas=bpy.data.images.new('CM_Cabinet_Style02_BaseColor',width=4096,height=4096,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(D/'Textures/CM_Cabinet_Style02_BaseColor.png')
target=node('ShaderNodeTexImage','ALBEDO_BAKE_TARGET');target.image=atlas
for nd in n:nd.select=False
target.select=True;n.active=target
# A full 0..1 UV quad evaluates the color grade per atlas pixel, not through tiny
# overlapping cabinet triangles. The temporary quad is not saved or exported.
o.select_set(False);bpy.ops.mesh.primitive_plane_add(size=2);quad=bpy.context.object;quad.name='TEMP_UV_DOMAIN_BAKE';quad.data.materials.append(m)
s.render.bake.use_clear=True;s.render.bake.margin=0;bpy.ops.object.bake(type='EMIT');bpy.data.objects.remove(quad,do_unlink=True)
o.select_set(True);bpy.context.view_layer.objects.active=o
atlas.file_format='PNG';atlas.save();atlas.reload();atlas.pack();l.new(bs.outputs[0],out.inputs['Surface']);m.use_fake_user=True
# Export material stays glTF-compatible. Working layer graph retained as unused editable material.
export=bpy.data.materials.new('CM_Cabinet_Style02_MattePaint');export.use_nodes=True;nn=export.node_tree.nodes;ll=export.node_tree.links;b=nn.get('Principled BSDF');bc=nn.new('ShaderNodeTexImage');bc.image=atlas;ll.new(bc.outputs[0],b.inputs['Base Color'])
nt=nn.new('ShaderNodeTexImage');nt.image=next(i for i in bpy.data.images if '_normal' in i.name);norm=nn.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.32;ll.new(nt.outputs[0],norm.inputs['Color']);ll.new(norm.outputs[0],b.inputs['Normal']);b.inputs['Roughness'].default_value=.82;b.inputs['Metallic'].default_value=.08;b.inputs['Specular IOR Level'].default_value=.25
o.data.materials[0]=export
for im in bpy.data.images:
 if im.type=='IMAGE':im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(D/'CM_BotanicalCabinet_Style02.blend'),compress=True)
bpy.ops.export_scene.gltf(filepath=str(D/'Exports/CM_BotanicalCabinet_Style02.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
(D/'BuildReport.json').write_text(json.dumps({'base_source':str(src),'base_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'triangles':len(o.data.polygons),'dimensions_m':list(o.dimensions),'geometry_changed':False,'uvs_changed':False,'normal_strength':.32,'roughness':.82,'metallic':.08,'texture_size':[4096,4096],'working_material':m.name},indent=2));print('STYLE02_READY',flush=True)
