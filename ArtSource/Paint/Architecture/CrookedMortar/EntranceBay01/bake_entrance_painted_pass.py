"""Transfer generated gouache source painting to the approved UV atlas; no mesh edits.
Creates sibling painted source + FBX. Requires --source-sheet ABSOLUTE_PATH.
"""
import bpy,json,math,hashlib,sys
import numpy as np
from pathlib import Path
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'ArtSource/Blender/Architecture/CrookedMortar/EntranceBay01'
PAINT=Path(__file__).parent
ASSET=ROOT/'Assets/BlightBloom/Art/Architecture/CrookedMortar/EntranceBay01'
source=ROOT/'ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png'
blend=BASE/'CM_EntranceBay01_Painted_v01.blend';fbx=ASSET/'Models/CM_EntranceBay01_Painted_v01.fbx'
textures=ASSET/'Textures';textures.mkdir(exist_ok=True)
atlaspath=textures/'CM_EntranceBay01_Painted_BaseColor_v01.png'
if any(p.exists() for p in [blend,fbx,atlaspath]) and '--refine-this-new-asset' not in sys.argv:raise RuntimeError('Refusing to overwrite painted assets')
bpy.ops.wm.open_mainfile(filepath=str(BASE/'CM_EntranceBay01_Geometry_v01.blend'))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
def fingerprint(o):
 payload={'vertices':[tuple(v.co) for v in o.data.vertices],'faces':[tuple(p.vertices) for p in o.data.polygons],'uv':[tuple(d.uv) for d in o.data.uv_layers[0].data],'matrix':[list(row) for row in o.matrix_world]}
 return hashlib.sha256(json.dumps(payload).encode()).hexdigest()
before={o.name:fingerprint(o) for o in objects}
image=bpy.data.images.load(str(source));image.colorspace_settings.name='sRGB'
# Quadrant coordinates in Blender's bottom-left UV convention.
rects={'Plaster':(0,.5),'Timber':(.5,.5),'Sage':(0,0),'Stone':(0,.5),'Slate':(.5,0)}
original_materials=list(bpy.data.materials)
for mat in original_materials:
 key=mat.name.replace('Entrance_','');nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');mat.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 if key in rects:
  uvnode=nodes.new('ShaderNodeUVMap');uvnode.uv_map='PaintProjection';tex=nodes.new('ShaderNodeTexImage');tex.image=image;tex.extension='EXTEND';mat.node_tree.links.new(uvnode.outputs[0],tex.inputs['Vector']);mat.node_tree.links.new(tex.outputs['Color'],em.inputs['Color'])
  if key=='Stone':
   tint=nodes.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.66,.70,.69,1);mat.node_tree.links.new(tex.outputs['Color'],tint.inputs[1]);mat.node_tree.links.new(tint.outputs[0],em.inputs['Color'])
 else:em.inputs['Color'].default_value=(.045,.04,.032,1) if key=='Soil' else (.065,.072,.066,1)
# Project actual painted brushwork along each wooden part's principal length.
# Only a TEMPORARY UV layer is used for transfer. The approved atlas is not edited.
for oi,o in enumerate(objects):
 m=o.data;key=o.data.materials[0].name.replace('Entrance_','');uv=m.uv_layers.new(name='PaintProjection')
 coords=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);centre=coords.mean(axis=0)
 _,axes=np.linalg.eigh(np.cov(coords.T));long=axes[:,-1];across=axes[:,-2];depth=axes[:,0]
 if long[np.argmax(np.abs(long))]<0:long=-long
 if across[np.argmax(np.abs(across))]<0:across=-across
 if 'Door_Leaf' in o.name:long=np.array([0.,0.,1.]);across=np.array([1.,0.,0.]);depth=np.array([0.,1.,0.])
 # Deterministic patch selection only, not generated noise or simulated grain.
 ox=((oi*7)%13)/13*.13;oy=((oi*11)%17)/17*.1
 for p in m.polygons:
  key=m.materials[p.material_index].name.replace('Entrance_','')
  if key not in rects:continue
  normal=np.array(tuple(o.matrix_world.to_3x3()@p.normal))
  cross=depth if abs(np.dot(normal,across))>abs(np.dot(normal,depth)) else across
  for li in p.loop_indices:
   v=coords[m.loops[li].vertex_index];rel=v-centre
   if key in ['Plaster','Stone']:
    u=(v[0]+1.7)/3.4 if abs(normal[1])>=abs(normal[0]) or abs(normal[2])>.7 else .5+v[1]/3.4
    w=v[2]/3.7 if abs(normal[2])<.7 else .3+v[1]/3.4
   elif key=='Slate':u=(v[0]+1.86)/3.72;w=(v[1]+.5)/1.9
   elif key=='Timber' and 'Curved_Timber_Stop' in o.name:
    u=(math.sqrt((v[0]/.9)**2+((v[2]-1.70)/.95)**2)-.88)*2+.2
    w=math.atan2((v[2]-1.70)/.95,v[0]/.9)/math.pi
   else:
    u=.5+float(np.dot(rel,cross))/.85;w=.5+float(np.dot(rel,long))/3.6
   u=max(.025,min(.975,.08+u*.78+ox));w=max(.025,min(.975,.06+w*.80+oy))
   x,y=rects[key];uv.data[li].uv=(x+.012+u*.476,y+.012+w*.476)
 m.uv_layers.active_index=0;m.uv_layers[0].active_render=True
# Join temporary copies into a single bake receiver; preserve every approved mesh.
bpy.ops.object.select_all(action='DESELECT');copies=[]
for o in objects:
 c=o.copy();c.data=o.data.copy();bpy.context.scene.collection.objects.link(c);c.select_set(True);copies.append(c)
bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();receiver=bpy.context.object
atlas=bpy.data.images.new('CM_EntranceBay01_Painted_BaseColor_v01',width=4096,height=4096,alpha=False);atlas.colorspace_settings.name='sRGB';atlas.filepath_raw=str(atlaspath);atlas.file_format='PNG'
for mat in receiver.data.materials:
 node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=atlas;node.select=True;mat.node_tree.nodes.active=node
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;s.render.bake.margin=16;s.render.bake.use_clear=True
bpy.ops.object.bake(type='EMIT');atlas.save()
bpy.data.objects.remove(receiver,do_unlink=True)
for o in objects:
 o.data.uv_layers.remove(o.data.uv_layers['PaintProjection']);o.data.uv_layers.active_index=0
assert before=={o.name:fingerprint(o) for o in objects},'Geometry or UV0 changed'
for mat in original_materials:
 nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');bs=nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.95;bs.inputs['Metallic'].default_value=0
 tex=nodes.new('ShaderNodeTexImage');tex.image=atlas;tex.label='Painted albedo on approved unique UV atlas';mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color']);mat.node_tree.links.new(bs.outputs[0],out.inputs['Surface'])
 mat.name=mat.name.replace('Entrance_','Painted_')
# Pack both the original painting and baked atlas for portable editable source.
image.pack();atlas.pack()
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
conversion=Matrix.Rotation(math.pi,4,'Z')
for o in objects:o.matrix_world=conversion@o.matrix_world
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH'},global_scale=1,apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Z',axis_up='Y',use_space_transform=True,bake_space_transform=True,use_mesh_modifiers=True,mesh_smooth_type='FACE',bake_anim=False,add_leaf_bones=False,path_mode='STRIP')
report={'geometry_and_uv0_unchanged':True,'meshes':len(objects),'source_painting':str(source),'atlas':str(atlaspath),'atlas_size':[4096,4096],'color_space':'sRGB','bake':'emission/albedo only; no lighting, AO, blur, or noise','padding_pixels':16,'geometry_hashes':before}
(PAINT/'texture_validation.json').write_text(json.dumps(report,indent=2));print('PAINT_BAKE_SUCCESS',json.dumps({k:v for k,v in report.items() if k!='geometry_hashes'}))
