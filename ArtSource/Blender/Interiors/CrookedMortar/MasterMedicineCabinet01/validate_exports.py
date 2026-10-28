"""Targeted export round-trip and material manifest. No Unity import/scene operations."""
import bpy,json,math
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'CM_MasterMedicineCabinet01.blend'))
cat=json.loads((D/'AssetCatalog.json').read_text());manifest=[]
for m in bpy.data.materials:
 if not m.name.startswith('CM_MMC01'):continue
 bs=m.node_tree.nodes.get('Principled BSDF');im=[n.image for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];mix=next((n for n in m.node_tree.nodes if n.type=='MIX_RGB'),None);alpha='Ivy' in m.name or 'Moss' in m.name
 manifest.append({'name':m.name,'albedoFile':('Textures/'+Path(im[0].filepath).name) if im else None,'albedoSize':list(im[0].size) if im else None,'tintLinear':list(mix.inputs[2].default_value) if mix else list(bs.inputs['Base Color'].default_value),'roughness':bs.inputs['Roughness'].default_value,'metallic':bs.inputs['Metallic'].default_value,'alphaMode':'MASK' if alpha else 'OPAQUE','cutoff':.4 if alpha else None,'doubleSided':alpha,'unityRecommendation':'URP/Lit; BaseMap and BaseColor from manifest; Smoothness=1-roughness, Metallic as listed. Alpha clipping/cull off only for ivy/moss.'})
(D/'MaterialManifest.json').write_text(json.dumps(manifest,indent=2))
source=[]
for c in bpy.context.scene.collection.children:
 for o in c.objects:
  if o.type=='MESH':source.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
core=[]
for c in bpy.context.scene.collection.children:
 if not c.name.startswith(('01_','02_','03_','04_','05_')):continue
 for o in c.objects:
  if o.type=='MESH':core.extend(tuple(o.matrix_world@v.co) for v in o.data.vertices)
coreLo=[min(p[i] for p in core) for i in range(3)];coreHi=[max(p[i] for p in core) for i in range(3)]
fitting={'existingMeasuredBayMetres':{'width':1.846,'height':2.926,'maxVisualDepth':.759},'woodAndHardwareDimensionsMetres':{'width':coreHi[0]-coreLo[0],'height':coreHi[2]-coreLo[2],'depth':coreHi[1]-coreLo[1]},'wholeAssetDimensionsMetres':{'width':max(p[0] for p in source)-min(p[0] for p in source),'height':max(p[2] for p in source)-min(p[2] for p in source),'depth':max(p[1] for p in source)-min(p[1] for p in source)},'footBearingOffsetFromOriginMetres':coreLo[2],'installation':'Not installed. Core fits measured width/height. Leaf tips slightly exceed measured cabinet width; removable/repositionable vegetation must be checked against actual beam/window returns before any integration. No claim of scene collision validation.'}
(D/'FittingReport.json').write_text(json.dumps(fitting,indent=2))
lo=[min(p[i] for p in source) for i in range(3)];hi=[max(p[i] for p in source) for i in range(3)];expectedMin=[-hi[0],-hi[1],lo[2]];expectedMax=[-lo[0],-lo[1],hi[2]]
# The established FBX transport turns native Blender +Y front into -Y for Unity +Z exterior.
def stats():
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[tuple(o.matrix_world@v.co) for o in objects for v in o.data.vertices];mins=[min(p[i] for p in pts) for i in range(3)];maxs=[max(p[i] for p in pts) for i in range(3)];tri=0
 for o in objects:o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles)
 return {'meshes':len(objects),'triangles':tri,'minBlenderNative':mins,'maxBlenderNative':maxs,'dimensionsMetres':[maxs[i]-mins[i] for i in range(3)],'boundsMatchTransport':max(abs(mins[i]-expectedMin[i]) for i in range(3))<.0002 and max(abs(maxs[i]-expectedMax[i]) for i in range(3))<.0002,'missingUVs':sum(not o.data.uv_layers for o in objects),'emptyMaterialSlots':sum(any(m is None for m in o.data.materials) for o in objects)}
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(D/'Exports/CM_MasterMedicineCabinet01.fbx'));fbx=stats();bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(D/'Exports/CM_MasterMedicineCabinet01.glb'));glb=stats()
r={'passed':all(x['boundsMatchTransport'] and x['meshes']==8 and x['triangles']==cat['triangles'] and not x['missingUVs'] and not x['emptyMaterialSlots'] for x in [fbx,glb]),'FBX':fbx,'GLB':glb,'method':'Reimport both final exports into separate empty Blender states; compare actual world bounds to the documented Unity-axis transport and source triangle count. Not a Unity import or gameplay test.','materialCount':len(manifest)};(D/'ExportValidation.json').write_text(json.dumps(r,indent=2));print('EXPORT_ROUNDTRIP',r)
