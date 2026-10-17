var source="Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity";
var dest="Assets/Scenes/CM_EntryPortal02_IntegrationPreview.unity";
if(UnityEditor.EditorApplication.isPlaying||UnityEditor.EditorApplication.isCompiling)throw new System.Exception("Editor busy");
for(int i=0;i<UnityEngine.SceneManagement.SceneManager.sceneCount;i++)if(UnityEngine.SceneManagement.SceneManager.GetSceneAt(i).isDirty)throw new System.Exception("Unsaved scene; refusing switch");
if(System.IO.File.Exists(dest))throw new System.Exception("Preview already exists; refusing overwrite");
if(!UnityEditor.AssetDatabase.CopyAsset(source,dest))throw new System.Exception("Scene copy failed");
var scene=UnityEditor.SceneManagement.EditorSceneManager.OpenScene(dest,UnityEditor.SceneManagement.OpenSceneMode.Single);
var roots=scene.GetRootGameObjects();
var collidersBefore=roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.Collider>(true)).Count();
var scriptsBefore=roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.MonoBehaviour>(true)).Count();
var prefixes=new[]{"Entry portal carved walnut upright","Entry post cap","Entry post shoe","Shallow storybook entry arch","Inner arch trim"};
var disabled=new System.Collections.Generic.List<string>();
foreach(var r in roots.SelectMany(o=>o.GetComponentsInChildren<UnityEngine.MeshRenderer>(true)))if(prefixes.Any(p=>r.name.StartsWith(p))&&r.enabled){r.enabled=false;disabled.Add(r.name);}
if(disabled.Count!=34)throw new System.Exception("Expected 34 measured proxy renderers, got "+disabled.Count);
var prefab=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.GameObject>("Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/Prefabs/CM_EntryPortal02.prefab");
var portal=(UnityEngine.GameObject)UnityEditor.PrefabUtility.InstantiatePrefab(prefab,scene);portal.name="CM_EntryPortal02_PreviewOnly";portal.transform.SetPositionAndRotation(new UnityEngine.Vector3(.85f,.20f,-5.52f),UnityEngine.Quaternion.Euler(0,180,0));portal.transform.localScale=UnityEngine.Vector3.one;
var cam=new UnityEngine.GameObject("IntegrationPreviewCamera").AddComponent<UnityEngine.Camera>();cam.enabled=false;cam.nearClipPlane=.05f;cam.farClipPlane=200;cam.fieldOfView=45;cam.clearFlags=UnityEngine.CameraClearFlags.Skybox;cam.transform.position=new UnityEngine.Vector3(-5.5f,3.4f,-12f);cam.transform.LookAt(new UnityEngine.Vector3(.85f,2.3f,-3.3f));
var collidersAfter=scene.GetRootGameObjects().SelectMany(o=>o.GetComponentsInChildren<UnityEngine.Collider>(true)).Count();
var scriptsAfter=scene.GetRootGameObjects().SelectMany(o=>o.GetComponentsInChildren<UnityEngine.MonoBehaviour>(true)).Count();
if(collidersAfter!=collidersBefore||scriptsAfter!=scriptsBefore)throw new System.Exception("Existing collision or script counts changed");
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene,dest);
var folder=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/EntryPortal02/IntegrationPreview");System.IO.Directory.CreateDirectory(folder);
var names=new[]{"Front","ThreeQuarter","GameplayDistance"};var pos=new[]{new UnityEngine.Vector3(.85f,2.6f,-13),new UnityEngine.Vector3(-5.5f,3.4f,-12),new UnityEngine.Vector3(-2.3f,1.85f,-11)};
for(int i=0;i<3;i++){
cam.transform.position=pos[i];cam.fieldOfView=i==2?55:45;cam.transform.LookAt(new UnityEngine.Vector3(.85f,i==2?1.95f:2.4f,-3.8f));
var rt=new UnityEngine.RenderTexture(1600,1200,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;var prior=UnityEngine.RenderTexture.active;cam.targetTexture=rt;cam.Render();UnityEngine.RenderTexture.active=rt;var image=new UnityEngine.Texture2D(1600,1200,UnityEngine.TextureFormat.RGB24,false);image.ReadPixels(new UnityEngine.Rect(0,0,1600,1200),0,0);image.Apply();System.IO.File.WriteAllBytes(folder+"/"+names[i]+".png",image.EncodeToPNG());cam.targetTexture=null;UnityEngine.RenderTexture.active=prior;UnityEngine.Object.DestroyImmediate(image);rt.Release();UnityEngine.Object.DestroyImmediate(rt);
}
cam.fieldOfView=45;cam.transform.position=pos[1];cam.transform.LookAt(new UnityEngine.Vector3(.85f,2.4f,-3.8f));
UnityEditor.Selection.activeGameObject=portal;if(UnityEditor.SceneView.lastActiveSceneView!=null)UnityEditor.SceneView.lastActiveSceneView.LookAt(new UnityEngine.Vector3(.85f,2.4f,-3.8f),cam.transform.rotation,6.5f);
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene,dest);
var report=new{scene=dest,disabledProxyRenderers=disabled,collidersBefore,collidersAfter,scriptsBefore,scriptsAfter,portalScale=portal.transform.localScale.ToString(),sourceSceneUnmodified=true,notes="Only old proxy renderers hidden in duplicate; original GameObjects and colliders retained. Existing door, sign, lanterns and plants remain in approved positions."};
System.IO.File.WriteAllText(folder+"/IntegrationValidation.json",Newtonsoft.Json.JsonConvert.SerializeObject(report,Newtonsoft.Json.Formatting.Indented));return report;
