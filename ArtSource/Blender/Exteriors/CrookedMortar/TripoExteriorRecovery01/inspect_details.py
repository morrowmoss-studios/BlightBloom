exec(open(__file__.replace('inspect_details.py','inspect_house.py')).read().split('bpy.ops.wm.read_factory_settings')[0])
bpy.ops.wm.open_mainfile(filepath=str(D/'OriginalReference.blend'));o=next(o for o in bpy.context.scene.objects if o.type=='MESH');co=np.array([v.co[:] for v in o.data.vertices]);lo=co.min(0);hi=co.max(0);center=Vector((lo+hi)/2);span=float(max(hi-lo));s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=True;s.render.resolution_x=1100;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world=bpy.data.worlds.new('World');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.25,.25,1)
for p,e in [((-2,-3,4),500),((3,-1,2),250),((1,3,3),350)]:
 d=bpy.data.lights.new('Area','AREA');d.energy=e*span**2;d.size=span*2;ob=bpy.data.objects.new(d.name,d);s.collection.objects.link(ob);ob.location=center+Vector(p)*span;ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=span*1.48;cam.location=center+Vector((1,-2,1))*span;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
from bpy_extras.object_utils import world_to_camera_view
from bpy_extras import view3d_utils
q=cam.rotation_euler.to_quaternion();hits={}
for name,x,y in [('sign',369,650),('door',438,719),('frontwindow',433,527),('valley',321,550),('frontpost',349,716)]:
 origin=cam.location+q@Vector(((x/1100-.5)*d.ortho_scale,(.5-y/1000)*d.ortho_scale*1000/1100,0));direction=q@Vector((0,0,-1));r=s.ray_cast(bpy.context.evaluated_depsgraph_get(),origin,direction);hits[name]=list(r[1]) if r[0] else None
print('HITS',hits);(D/'DetailTargets.json').write_text(json.dumps(hits,indent=2))
for name in ['sign','valley','door','frontwindow']:
 target=Vector(hits[name] or (-.105,-.29,.31));cam.location=target+Vector((.6,-1.6,.45))*.5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();d.ortho_scale=.18 if name=='sign' else .40;s.render.filepath=str(D/f'Detail_{name}.png');bpy.ops.render.render(write_still=True)
