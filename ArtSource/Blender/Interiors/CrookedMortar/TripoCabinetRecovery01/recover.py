import bpy,json,math,bmesh
from pathlib import Path
from mathutils import Vector,Matrix
D=Path(__file__).resolve().parent;J=json.loads((D/'Inspection.json').read_text());reports={}
for label,lower,upper,angle in [('CabinetA',.025,.162,-math.pi/2),('CabinetB',-.51,.025,0)]:
 bpy.ops.wm.open_mainfile(filepath=str(D/'ImportedIslands.blend'));s=bpy.context.scene;s.unit_settings.system='METRIC'
 high=bpy.data.collections.new('01_HIGH_DETAIL_preserved');s.collection.children.link(high);opt=bpy.data.collections.new('02_OPTIMIZED_candidate');s.collection.children.link(opt)
 keep=[];excluded=[]
 for r in J['islands']:
  o=bpy.data.objects.get(r['name'])
  if r['min'][2]>.24 and r['min'][0]>lower and r['max'][0]<upper:
   for c in list(o.users_collection):c.objects.unlink(o)
   high.objects.link(o);keep.append(o)
  else:excluded.append(r['name']);bpy.data.objects.remove(o,do_unlink=True)
 # rotate only; uniform metric normalization to 1.94m height, no reshaping.
 R=Matrix.Rotation(angle,4,'Z');pts=[R@o.matrix_world@Vector(v) for o in keep for v in o.bound_box];lo=Vector([min(p[j] for p in pts) for j in range(3)]);hi=Vector([max(p[j] for p in pts) for j in range(3)]);factor=1.94/(hi.z-lo.z);center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));T=Matrix.Scale(factor,4)@Matrix.Translation(-center)@R
 for o in keep:o.matrix_world=T@o.matrix_world
 # join transport fragments, preserving UVs/material; originals still preserved in baseline file.
 bpy.ops.object.select_all(action='DESELECT')
 for o in keep:o.select_set(True)
 bpy.context.view_layer.objects.active=keep[0];bpy.ops.object.join();h=bpy.context.object;h.name=label+'_HighDetail';bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 sourceTris=len(h.data.polygons)
 candidate=h.copy();candidate.data=h.data.copy();opt.objects.link(candidate);candidate.name=label+'_Optimized'
 bpy.context.view_layer.objects.active=candidate;h.select_set(False);candidate.select_set(True)
 # UV seam preservation: decimation is conservative; no welding, hidden-face deletion or semantic guesswork.
 dec=candidate.modifiers.new('Conservative collapse 55 percent','DECIMATE');dec.ratio=.55;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
 high.hide_render=True;high.hide_viewport=True
 stats={}
 for o in [h,candidate]:
  m=o.data;m.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(m)
  stats[o.name]={'triangles':len(m.loop_triangles),'vertices':len(m.vertices),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'uv_layers':[u.name for u in m.uv_layers],'dimensions_m':list(o.dimensions)};bm.free()
 for im in bpy.data.images:
  if im.type=='IMAGE':im.filepath=str(D/'Textures'/im.name)
 out=D/label;out.mkdir(exist_ok=True);(out/'Exports').mkdir(exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(label+'.blend')))
 bpy.ops.object.select_all(action='DESELECT');candidate.select_set(True);bpy.context.view_layer.objects.active=candidate
 bpy.ops.export_scene.gltf(filepath=str(out/'Exports'/(label+'_Optimized.glb')),export_format='GLB',use_selection=True,export_yup=True,export_apply=True)
 reports[label]={'source_triangles':sourceTris,'optimized_triangles':len(candidate.data.polygons),'source_islands':len(keep),'rotation_z_degrees':math.degrees(angle),'uniform_scale_to_1_94m_height':factor,'stats':stats,'excluded_islands':excluded}
 print('RECOVERED',label,sourceTris,len(candidate.data.polygons),flush=True)
(D/'RecoveryReport.json').write_text(json.dumps(reports,indent=2))
