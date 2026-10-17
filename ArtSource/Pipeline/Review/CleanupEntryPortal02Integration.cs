var scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene();if(scene.path!="Assets/Scenes/CM_EntryPortal02_IntegrationPreview.unity"||scene.isDirty)throw new System.Exception("Expected clean integration preview");
var roots=scene.GetRootGameObjects();var cols=roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.Collider>(true)).ToArray();var behaviours=roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.MonoBehaviour>(true)).ToArray();
string Snapshot(UnityEngine.Component c){return UnityEditor.EditorJsonUtility.ToJson(c)+c.transform.localToWorldMatrix.ToString();}
var before=cols.Cast<UnityEngine.Component>().Concat(behaviours).ToDictionary(c=>c.GetInstanceID(),Snapshot);
var porch=roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.MeshRenderer>()).Single(r=>r.name=="Porch"&&r.enabled);var mf=porch.GetComponent<UnityEngine.MeshFilter>();var source=mf.sharedMesh;var vs=source.vertices;
var parent=Enumerable.Range(0,vs.Length).ToArray();int Find(int i){while(parent[i]!=i){parent[i]=parent[parent[i]];i=parent[i];}return i;}void Union(int a,int b){parent[Find(a)]=Find(b);}
var weld=new System.Collections.Generic.Dictionary<string,int>();for(int i=0;i<vs.Length;i++){var p=vs[i];var key=$"{p.x:F5},{p.y:F5},{p.z:F5}";if(weld.TryGetValue(key,out var k))Union(i,k);else weld[key]=i;}
var ts=source.triangles;for(int i=0;i<ts.Length;i+=3){Union(ts[i],ts[i+1]);Union(ts[i],ts[i+2]);}
var bounds=new System.Collections.Generic.Dictionary<int,UnityEngine.Bounds>();foreach(var g in Enumerable.Range(0,vs.Length).GroupBy(Find)){var pts=g.Select(i=>porch.transform.TransformPoint(vs[i])).ToArray();var b=new UnityEngine.Bounds(pts[0],UnityEngine.Vector3.zero);foreach(var p in pts)b.Encapsulate(p);bounds[g.Key]=b;}
var removed=bounds.Where(kv=>kv.Value.center.x>1.5f&&kv.Value.size.y>.5f).Select(kv=>kv.Key).ToHashSet();
var beam=bounds.Single(kv=>kv.Value.size.x>4&&kv.Value.min.y>2.8f).Key;
var mesh=UnityEngine.Object.Instantiate(source);mesh.name="CM_EntryPortal02_Preview_CanopyRetained";var changedVerts=mesh.vertices;
foreach(int i in Enumerable.Range(0,vs.Length).Where(i=>Find(i)==beam)){var w=porch.transform.TransformPoint(vs[i]);if(w.x>-.25f){w.x=-.25f;changedVerts[i]=porch.transform.InverseTransformPoint(w);}}
mesh.vertices=changedVerts;
for(int s=0;s<mesh.subMeshCount;s++){var old=source.GetTriangles(s);var keep=new System.Collections.Generic.List<int>();for(int i=0;i<old.Length;i+=3)if(!removed.Contains(Find(old[i]))){keep.Add(old[i]);keep.Add(old[i+1]);keep.Add(old[i+2]);}mesh.SetTriangles(keep,s);}
mesh.RecalculateBounds();
var path="Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/Models/CM_EntryPortal02_IntegrationCanopy.asset";if(System.IO.File.Exists(path))throw new System.Exception("Preview mesh exists");UnityEditor.AssetDatabase.CreateAsset(mesh,path);mf.sharedMesh=mesh;
// Small bearing block connects retained shop beam to new portal post cap; decorative render only.
var bearing=UnityEngine.GameObject.CreatePrimitive(UnityEngine.PrimitiveType.Cube);bearing.name="PreviewOnly_CanopyBearing_LeftPortalCap";UnityEngine.Object.DestroyImmediate(bearing.GetComponent<UnityEngine.Collider>());bearing.transform.position=new UnityEngine.Vector3(-.25f,2.85f,-5.52f);bearing.transform.localScale=new UnityEngine.Vector3(.18f,.12f,.18f);bearing.GetComponent<UnityEngine.Renderer>().sharedMaterial=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.Material>("Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/Materials/CM_EntryPortal02_PaintedWalnut.mat");
foreach(var c in cols.Cast<UnityEngine.Component>().Concat(behaviours))if(Snapshot(c)!=before[c.GetInstanceID()])throw new System.Exception("Collision/behaviour changed: "+c.name);
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene);UnityEditor.AssetDatabase.SaveAssets();return new{components=bounds.Select(k=>new{key=k.Key,center=k.Value.center.ToString(),size=k.Value.size.ToString(),removed=removed.Contains(k.Key)}).ToArray(),collidersUnchanged=cols.Length,behavioursUnchanged=behaviours.Length};
