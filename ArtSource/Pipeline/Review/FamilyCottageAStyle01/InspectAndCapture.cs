// Read-only geometry export and baseline, followed by captures with all camera state restored.
var scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene();
if(EditorApplication.isPlaying||scene.path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Briarwick Edit mode required");
string D="ArtSource/Pipeline/Review/FamilyCottageAStyle01",S="ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01";
var root=GameObject.Find("10 Family cottage A PLACEHOLDER");
string H(Transform t){string s=t.name;while(t.parent!=null){t=t.parent;s=t.name+"/"+s;}return s;}
var untouched=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).Where(t=>t!=root.transform&&!t.IsChildOf(root.transform)).Select(t=>new{path=H(t),components=t.GetComponents<Component>().Where(c=>c!=null).Select(c=>new{type=c.GetType().FullName,json=EditorJsonUtility.ToJson(c)}).ToArray()}).ToArray();
System.IO.File.WriteAllText(D+"/UnrelatedBefore.json",Newtonsoft.Json.JsonConvert.SerializeObject(untouched));
var meshes=root.GetComponentsInChildren<MeshFilter>(false).Select(f=>f.sharedMesh).Distinct().Select(m=>new{name=m.name,vertices=m.vertices.Select(v=>new[]{v.x,v.y,v.z}).ToArray(),normals=m.normals.Select(v=>new[]{v.x,v.y,v.z}).ToArray(),uv=m.uv.Select(v=>new[]{v.x,v.y}).ToArray(),submeshes=Enumerable.Range(0,m.subMeshCount).Select(i=>m.GetTriangles(i)).ToArray(),materials=root.GetComponentsInChildren<MeshFilter>(false).First(f=>f.sharedMesh==m).GetComponent<Renderer>().sharedMaterials.Select(a=>a.name).ToArray()}).ToArray();
System.IO.File.WriteAllText(S+"/SourceMeshReadOnly.json",Newtonsoft.Json.JsonConvert.SerializeObject(meshes));
var mats=root.GetComponentsInChildren<Renderer>(false).SelectMany(r=>r.sharedMaterials).Distinct().Select(m=>new{name=m.name,path=AssetDatabase.GetAssetPath(m),shader=m.shader.name,textures=m.GetTexturePropertyNames().Where(n=>m.GetTexture(n)!=null).Select(n=>new{property=n,path=AssetDatabase.GetAssetPath(m.GetTexture(n))}).ToArray()}).ToArray();
System.IO.File.WriteAllText(S+"/SourceMaterials.json",Newtonsoft.Json.JsonConvert.SerializeObject(mats,Newtonsoft.Json.Formatting.Indented));
return new{meshes=meshes.Length,materials=mats.Length,triangles=root.GetComponentsInChildren<MeshFilter>(false).Sum(f=>f.sharedMesh.triangles.Length/3),dirty=scene.isDirty};
