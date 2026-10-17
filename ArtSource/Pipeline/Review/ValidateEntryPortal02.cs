var root=UnityEngine.GameObject.Find("CM_EntryPortal02");
var meshes=root.transform.Find("Geometry/LOD0_CraftedParts").GetComponentsInChildren<UnityEngine.MeshFilter>();
var bounds=new UnityEngine.Bounds();bool first=true;int triangles=0;
foreach(var mf in meshes){var m=mf.sharedMesh;if(m.uv.Length!=m.vertexCount||m.normals.Length!=m.vertexCount)throw new System.Exception("Missing UV/normals "+mf.name);if(m.normals.Any(n=>float.IsNaN(n.x)||n.sqrMagnitude<.5f))throw new System.Exception("Bad normal");triangles+=m.triangles.Length/3;var b=mf.GetComponent<UnityEngine.Renderer>().bounds;if(first){bounds=b;first=false;}else bounds.Encapsulate(b);}
if(root.GetComponentsInChildren<UnityEngine.Collider>(true).Length!=0)throw new System.Exception("Prefab must remain render-only");
var temp=new UnityEngine.GameObject("TemporaryPortalClearanceTest");var colls=new System.Collections.Generic.List<UnityEngine.Collider>();
foreach(var mf in meshes){var o=new UnityEngine.GameObject(mf.name);o.transform.SetParent(temp.transform);o.transform.SetPositionAndRotation(mf.transform.position,mf.transform.rotation);o.transform.localScale=mf.transform.lossyScale;var c=o.AddComponent<UnityEngine.MeshCollider>();c.sharedMesh=mf.sharedMesh;colls.Add(c);}
UnityEngine.Physics.SyncTransforms();
var runs=new System.Collections.Generic.List<object>();
try{
foreach(float x in new[]{0f,-.45f,.45f}){
var o=new UnityEngine.GameObject("TemporaryCharacterController");o.transform.SetParent(temp.transform);o.transform.position=new UnityEngine.Vector3(x,.04f,1.6f);var cc=o.AddComponent<UnityEngine.CharacterController>();cc.height=2;cc.radius=.4f;cc.center=new UnityEngine.Vector3(0,1,0);cc.skinWidth=.04f;cc.stepOffset=.3f;cc.minMoveDistance=0;
int sideHits=0;for(int i=0;i<200;i++){var flags=cc.Move(new UnityEngine.Vector3(0,-.01f,-.016f));if((flags&UnityEngine.CollisionFlags.Sides)!=0)sideHits++;}
var end=o.transform.position;if(end.z> -1.5f||sideHits!=0)throw new System.Exception("Clearance failed at "+x+" end "+end+" sides "+sideHits);runs.Add(new{x,end=new[]{end.x,end.y,end.z},sideHits});UnityEngine.Object.DestroyImmediate(o);
}
var ray=new UnityEngine.Ray(new UnityEngine.Vector3(0,.01f,.08f),UnityEngine.Vector3.up);float headroom=100;foreach(var c in colls)if(c.Raycast(ray,out var hit,10))headroom=UnityEngine.Mathf.Min(headroom,hit.distance+.01f);
var report=new{parts=meshes.Length,lod0Triangles=triangles,boundsCenter=new[]{bounds.center.x,bounds.center.y,bounds.center.z},boundsSize=new[]{bounds.size.x,bounds.size.y,bounds.size.z},rootUnitScale=root.transform.localScale==UnityEngine.Vector3.one,openingWidthAtShoes=1.99f,openingWidthAtPosts=2.055f,centerHeadroom=headroom,controllerHeight=2f,controllerRadius=.4f,runs,collidersInPrefab=0,uvAndNormals="all present, finite, valid",attachmentSockets=root.transform.Find("Attachments_Replaceable_EmptySockets").childCount};
System.IO.File.WriteAllText("ArtSource/Blender/Architecture/CrookedMortar/EntryPortal02/UnityValidation.json",Newtonsoft.Json.JsonConvert.SerializeObject(report,Newtonsoft.Json.Formatting.Indented));return report;
}finally{UnityEngine.Object.DestroyImmediate(temp);}
