"""Non-destructive material reconstruction. Geometry and original UVs are unchanged."""
import bpy,math,json,hashlib,numpy as np
from pathlib import Path
D=Path(__file__).resolve().parent;src=D.parent/'TripoCabinetStyle02/CM_BotanicalCabinet_Style02.blend';bpy.ops.wm.open_mainfile(filepath=str(src));o=bpy.data.objects['CM_BotanicalCabinet_Style02'];o.name='CabinetB_Style03_SameGeometry'
style02=o.data.materials[0];style02.use_fake_user=True
with bpy.data.libraries.load(str(D.parent/'TripoCabinetRecovery01/CabinetB/CabinetB.blend'),link=False) as (a,b):b.materials=[x for x in a.materials if x.startswith('tripo_material')]
original=b.materials[0];original.name='COMPARE_01_RecoveredTripo';original.use_fake_user=True;style02.name='COMPARE_02_Style02'
base=next(im for im in bpy.data.images if im.name=='rustic_wooden_cabinet_3d_model_basecolor.jpg');normal=next(im for im in bpy.data.images if im.name=='rustic_wooden_cabinet_3d_model_normal.png');grain=next(im for im in bpy.data.images if im.name=='Walnut_Painted_Source.png')
report={}
for variant in ['A','B']:
 expressive=variant=='B';mat=bpy.data.materials.new('COMPARE_03_PrototypeA' if not expressive else 'COMPARE_04_PrototypeB');mat.use_nodes=True;mat.use_fake_user=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear()
 def node(t,label):p=n.new(t);p.label=label;p.name=label;return p
 def wire(val,sock):
  if hasattr(val,'node'):l.new(val,sock)
  else:sock.default_value=val
 def mathn(op,a,b=None):
  p=node('ShaderNodeMath',op);p.operation=op;wire(a,p.inputs[0]);
  if b is not None:wire(b,p.inputs[1])
  return p.outputs[0]
 def smooth(v,a,b):
  p=node('ShaderNodeMapRange','Soft material region');p.interpolation_type='SMOOTHSTEP';p.clamp=True;wire(v,p.inputs[0]);p.inputs[1].default_value=a;p.inputs[2].default_value=b;return p.outputs[0]
 def invert(v):return mathn('SUBTRACT',1,v)
 def band(v,a,b,w=.01):return mathn('MULTIPLY',smooth(v,a,a+w),invert(smooth(v,b-w,b)))
 def product(*a):
  out=a[0]
  for q in a[1:]:out=mathn('MULTIPLY',out,q)
  return out
 def maximum(*a):
  out=a[0]
  for q in a[1:]:out=mathn('MAXIMUM',out,q)
  return out
 def mix(a,b,f,label):
  p=node('ShaderNodeMixRGB',label)
  for v,i in [(f,0),(a,1),(b,2)]:wire(v,p.inputs[i])
  return p.outputs[0]
 def ramp(v,points,label):
  p=node('ShaderNodeValToRGB',label);p.color_ramp.interpolation='B_SPLINE';cr=p.color_ramp
  while len(cr.elements)>2:cr.elements.remove(cr.elements[-1])
  for i,(pos,col) in enumerate(points):
   e=cr.elements[i] if i<2 else cr.elements.new(pos);e.position=pos;e.color=(*col,1)
  wire(v,p.inputs[0]);return p.outputs['Color']
 tc=node('ShaderNodeTexCoord','Metre-space paint coordinates');sep=node('ShaderNodeSeparateXYZ','Construction zones');l.new(tc.outputs['Object'],sep.inputs[0]);x,y,z=sep.outputs[:];absx=mathn('ABSOLUTE',x)
 raw=node('ShaderNodeTexImage','Original atlas — selectors and protected markings only');raw.image=base
 hsv=node('ShaderNodeSeparateColor','Source hue/saturation selectors — discard baked luminance');hsv.mode='HSV';l.new(raw.outputs[0],hsv.inputs[0]);h,sat,value=hsv.outputs[:]
 # Object mapping is independent of damaged inherited UVs for reconstructed materials.
 mapping=node('ShaderNodeVectorMath','Hand-painted grain physical scale');mapping.operation='MULTIPLY';l.new(tc.outputs['Object'],mapping.inputs[0]);mapping.inputs[1].default_value=(1.4,1.4,.65) if not expressive else (.48,.48,.28)
 # Horizontal grain on drawer/crown rails, vertical grain on full-height stiles.
 orient=product(invert(smooth(absx,.76,.84)),maximum(invert(smooth(z,.61,.65)),smooth(z,1.70,1.76)))
 swapped=node('ShaderNodeCombineXYZ','Horizontal rail coordinate frame');wire(z,swapped.inputs[0]);wire(y,swapped.inputs[1]);wire(x,swapped.inputs[2]);oriented=mix(tc.outputs['Object'],swapped.outputs[0],orient,'Structural grain orientation');l.new(oriented,mapping.inputs[0])
 paint=node('ShaderNodeTexImage','Painted walnut — replacement diffuse, not old-albedo overlay');paint.image=grain;paint.projection='BOX';paint.projection_blend=.22;l.new(mapping.outputs[0],paint.inputs[0])
 bw=node('ShaderNodeRGBToBW','Painted value groups');l.new(paint.outputs[0],bw.inputs[0]);g=bw.outputs[0]
 woodcolor=ramp(g,[(.025,(.038,.017,.009)),(.10,(.080,.032,.012)),(.26,(.19,.085,.032))] if not expressive else [(.025,(.014,.006,.003)),(.10,(.065,.027,.012)),(.26,(.24,.12,.045))],'Walnut interpreted color groups')
 # A deliberate low-frequency paint field in B, retaining real geometric shading.
 if expressive:
  map2=node('ShaderNodeVectorMath','Broad paint field');map2.operation='MULTIPLY';l.new(tc.outputs['Object'],map2.inputs[0]);map2.inputs[1].default_value=(.19,.19,.16)
  broad=node('ShaderNodeTexImage','Broad organic paint variation');broad.image=grain;broad.projection='BOX';broad.projection_blend=.35;l.new(map2.outputs[0],broad.inputs[0]);bb=node('ShaderNodeRGBToBW','Broad material value');l.new(broad.outputs[0],bb.inputs[0]);field=ramp(bb.outputs[0],[(.02,(.018,.008,.004)),(.12,(.075,.032,.014)),(.25,(.24,.13,.05))],'Large authored walnut regions');woodcolor=mix(woodcolor,field,.42,'Expressive paint variation')
 nt=node('ShaderNodeTexImage','Original geometric-detail normal');nt.image=normal
 def principled(label,color,rough=.7,metal=0,strength=.25,sheen=0,coat=0):
  p=node('ShaderNodeBsdfPrincipled',label);wire(color,p.inputs['Base Color']);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;p.inputs['Specular IOR Level'].default_value=.38;p.inputs['Sheen Weight'].default_value=sheen;p.inputs['Coat Weight'].default_value=coat
  nm=node('ShaderNodeNormalMap',label+' normal detail');nm.inputs['Strength'].default_value=strength;l.new(nt.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],p.inputs['Normal']);return p.outputs[0]
 ao=node('ShaderNodeAmbientOcclusion','Local carving and joinery crevice tone');ao.inputs['Distance'].default_value=.035;ao.samples=8;crevice=mix((1,1,1,1),ao.outputs['Color'],.23 if not expressive else .29,'Restrained physical crevice accent');mul=node('ShaderNodeMixRGB','Paint and modeled crevice tone');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;wire(woodcolor,mul.inputs[1]);wire(crevice,mul.inputs[2]);woodcolor=mul.outputs[0]
 wood=principled('01 Reconstructed walnut',woodcolor,.66 if not expressive else .73,0,.22 if not expressive else .10)
 backingcolor=mix((.028,.055,.036,1),(.095,.16,.105,1),.36 if not expressive else .82,'Sage backing pigment');back=principled('02 Sage backing',backingcolor,.82,0,.12)
 # Preserve fine book/label/pot imagery where no reliable de-lighted source exists.
 stockcolor=mix(raw.outputs[0],(.15,.085,.04,1),.16 if not expressive else .38,'Bounded stock treatment — inherited artwork retained');stock=principled('03 Books leather ceramic stock',stockcolor,.50 if not expressive else .62,0,.35,0,.10)
 leafvalue=g if expressive else mathn('ADD',mathn('MULTIPLY',g,.65),mathn('MULTIPLY',h,.20))
 leafcolor=ramp(leafvalue,[(.02,(.025,.065,.015)),(.11,(.065,.14,.025)),(.27,(.20,.30,.070))] if not expressive else [(.02,(.025,.065,.015)),(.11,(.085,.175,.032)),(.27,(.22,.32,.085))],'Layered botanical pigments without old specular or AO')
 leaf=principled('04 Matte layered foliage',leafcolor,.75 if not expressive else .84,0,.45 if not expressive else .25,.04 if not expressive else .07)
 mosscolor=ramp(g,[(.02,(.025,.06,.012)),(.11,(.09,.16,.025)),(.27,(.20,.28,.06))],'Velvety moss pigments');moss=principled('05 Velvety moss',mosscolor,.92,0,.32,.25)
 brasscolor=mix((.16,.09,.025,1),(.32,.21,.075,1),smooth(g,.03,.22),'Aged brass pigment');brass=principled('06 Aged brass — actual metallic response',brasscolor,.50 if not expressive else .60,.72,.15)
 glasscolor=mix((.018,.045,.028,1),(.075,.15,.095,1),smooth(g,.03,.22),'Bottle tint independent of baked white glints');glass=principled('07 Restrained bottle glass finish',glasscolor,.24 if not expressive else .30,0,.10,0,.32)
 papercolor=mix(raw.outputs[0],(.46,.35,.19,1),.06 if not expressive else .16,'Protected labels botanical print and bone');paper=principled('08 Protected printed details and bone',papercolor,.72,0,.24)
 def box(xa,xb,za,zb,ya=-.25,yb=.20,w=.012):return product(band(x,xa,xb,w),band(z,za,zb,w),band(y,ya,yb,w))
 contents=maximum(box(-.78,.78,.65,.99),box(-.78,.78,1.04,1.34),box(-.78,.78,1.40,1.68))
 glassmask=maximum(box(-.68,-.25,1.055,1.31),box(-.32,.10,1.43,1.65),box(.26,.52,.67,.98),box(-.43,-.23,.67,.97))
 # Glass tint is deliberately opaque: fused bottles have no dependable separate inner shell.
 green=product(band(h,.125,.46,.025),smooth(sat,.20,.36));green=product(green,maximum(invert(contents),smooth(value,.12,.24)))
 geom=node('ShaderNodeNewGeometry','Physical surface orientation');normsep=node('ShaderNodeSeparateXYZ','Up-facing moss selection');l.new(geom.outputs['Normal'],normsep.inputs[0]);mossmask=product(band(h,.12,.19,.015),smooth(sat,.32,.55),smooth(normsep.outputs[2],.25,.65),invert(contents))
 backmask=product(smooth(y,.20,.24),band(z,.58,1.75,.02),invert(smooth(absx,.78,.84)))
 # Drawer hardware is selected by its actual protrusion as well as the eight local centres.
 hardware=[];labelareas=[]
 for xc in [-.66,-.22,.22,.66]:
  for zc in [.225,.465]:
   dx=mathn('DIVIDE',mathn('SUBTRACT',x,xc),.115);dz=mathn('DIVIDE',mathn('SUBTRACT',z,zc),.07);dist=mathn('ADD',mathn('MULTIPLY',dx,dx),mathn('MULTIPLY',dz,dz));hardware.append(product(invert(smooth(dist,.65,1.25)),invert(smooth(y,-.125,-.108))))
   labelareas.append(box(xc-.12,xc+.12,zc+.030,zc+.150,-.16,-.07,.008))
 brassmask=maximum(*hardware);ivory=product(invert(smooth(sat,.65,.85)),smooth(value,.15,.30));glasslabels=maximum(box(-.68,-.25,1.075,1.19),box(-.32,.10,1.46,1.555),box(.30,.52,.72,.835),box(-.43,-.23,.72,.81))
 papermask=product(ivory,maximum(product(contents,invert(glassmask)),glasslabels,maximum(*labelareas)))
 # Blend material parameters, not eight complete layered Principled closures.
 # This keeps all roles available without exceeding Cycles' closure limit.
 layers=[(backmask,back,'Sage panel'),(contents,stock,'Stock'),(glassmask,glass,'Bottle glass'),(green,leaf,'Foliage'),(mossmask,moss,'Moss'),(brassmask,brass,'Brass'),(papermask,paper,'Protected inscriptions')]
 wood.node.inputs['Specular IOR Level'].default_value=.25;leaf.node.inputs['Specular IOR Level'].default_value=.16;moss.node.inputs['Specular IOR Level'].default_value=.10;glass.node.inputs['Specular IOR Level'].default_value=.50
 keys=['Base Color','Roughness','Metallic','Sheen Weight','Coat Weight','Specular IOR Level']
 def read_input(bs,k):
  sk=bs.node.inputs[k];return sk.links[0].from_socket if sk.is_linked else sk.default_value
 params={k:read_input(wood,k) for k in keys};strength=wood.node.inputs['Normal'].links[0].from_node.inputs['Strength'].default_value
 for mask,bs,label in layers:
  for k in keys:
   value=read_input(bs,k)
   if k=='Base Color':params[k]=mix(params[k],value,mask,label+' color')
   else:params[k]=mathn('ADD',mathn('MULTIPLY',params[k],invert(mask)),mathn('MULTIPLY',value,mask))
  st=bs.node.inputs['Normal'].links[0].from_node.inputs['Strength'].default_value;strength=mathn('ADD',mathn('MULTIPLY',strength,invert(mask)),mathn('MULTIPLY',st,mask))
 final=node('ShaderNodeBsdfPrincipled','Single efficient illustrated surface')
 for k,v in params.items():wire(v,final.inputs[k])
 final.inputs['Specular IOR Level'].default_value=.38
 nm=node('ShaderNodeNormalMap','Material-aware preserved normal detail');wire(strength,nm.inputs['Strength']);l.new(nt.outputs[0],nm.inputs['Color']);l.new(nm.outputs[0],final.inputs['Normal'])
 for nd in list(n):
  if nd.type=='BSDF_PRINCIPLED' and nd!=final:n.remove(nd)
  elif nd.type=='NORMAL_MAP' and nd!=nm:n.remove(nd)
 out=node('ShaderNodeOutputMaterial','Illustrated material output');l.new(final.outputs[0],out.inputs['Surface'])
 # Arrange editable nodes by dependency rather than leaving a stack at origin.
 depths={}
 def depth(p,visited=None):
  if p in depths:return depths[p]
  deps=[q.from_node for i in p.inputs for q in i.links];depths[p]=0 if not deps else 1+max(depth(q) for q in deps);return depths[p]
 rows={}
 for nd in n:
  d=depth(nd);r=rows.get(d,0);rows[d]=r+1;nd.location=(d*235,-r*210);nd.width=205
 o.data.materials[0]=mat
 for im in bpy.data.images:
  if im.type=='IMAGE':im.pack()
 bpy.ops.wm.save_as_mainfile(filepath=str(D/f'CabinetB_Style03_Prototype{variant}.blend'),compress=True)
 report[variant]={'material':mat.name,'wood_uses_old_albedo':False,'material_roles':8,'wood_normal_strength':.22 if not expressive else .10,'wood_roughness':.66 if not expressive else .73,'glass_roughness':.24 if not expressive else .30,'brass_metallic':.72,'brass_roughness':.50 if not expressive else .60,'geometry_changed':False,'original_uv_changed':False,'source_artwork_retained_for':'Stock imagery, labels, botanical picture, bone; hue/saturation used for mask selection, not wood illumination','limitation':'Glass is tinted opaque reflective finish, not reconstructed hollow/transmissive bottles; semantic masks are soft spatial and source-hue approximations.'}
 print('SAVED PROTOTYPE',variant,flush=True)
(D/'BuildReport.json').write_text(json.dumps(report,indent=2))
