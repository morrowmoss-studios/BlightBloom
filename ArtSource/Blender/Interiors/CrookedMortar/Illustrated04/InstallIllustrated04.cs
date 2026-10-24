if(EditorApplication.isPlaying||UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/CM_CrookedMortar_Production02.unity"||UnityEngine.SceneManagement.SceneManager.GetActiveScene().isDirty)throw new System.Exception("Clean Production02 Edit required");if(GameObject.Find("20 Illustrated apothecary composition 04")!=null)throw new System.Exception("Already installed");
string dir="Assets/BlightBloom/Art/Interiors/CrookedMortar/Illustrated04/",af="Assets/BlightBloom/Art/Interiors/CrookedMortar/ApothecaryFurnishings01/",hr="Assets/BlightBloom/Art/Interiors/CrookedMortar/HeroRefinement02/";AssetDatabase.Refresh();var cat=Newtonsoft.Json.Linq.JObject.Parse(System.IO.File.ReadAllText("ArtSource/Blender/Interiors/CrookedMortar/Illustrated04/AssetCatalog.json"));
var texture=AssetDatabase.LoadAssetAtPath<Texture2D>(dir+"Textures/CM_Illustrated04_Atlas.png");var painted=new Material(Shader.Find("Universal Render Pipeline/Lit")){name="CM_IL04_PaintedArtwork"};painted.SetTexture("_BaseMap",texture);painted.SetColor("_BaseColor",Color.white);painted.SetFloat("_Smoothness",0);painted.SetFloat("_Metallic",0);painted.SetFloat("_Cull",0);painted.doubleSidedGI=true;AssetDatabase.CreateAsset(painted,dir+"Materials/CM_IL04_PaintedArtwork.mat");foreach(var row in cat["modules"]){var n=(string)row["name"];var path=dir+"Models/"+n+".fbx";var mi=(ModelImporter)AssetImporter.GetAtPath(path);mi.materialImportMode=ModelImporterMaterialImportMode.None;mi.importAnimation=false;mi.importNormals=ModelImporterNormals.Import;mi.isReadable=true;mi.SaveAndReimport();var g=new GameObject(n);var model=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(path));model.transform.SetParent(g.transform,false);foreach(var r in model.GetComponentsInChildren<MeshRenderer>()){r.gameObject.layer=2;r.sharedMaterials=row["materials"].Select(t=>{string k=((string)t).Replace("CM_AF01_","").Split('.')[0];if(k=="CM_IL04_Artwork")return painted;return AssetDatabase.LoadAssetAtPath<Material>(k=="Labels"?hr+"Materials/CM_HR02_InkArtwork.mat":k=="Walnut"?hr+"Materials/CM_HR02_PaintedWalnut.mat":af+"Materials/CM_AF01_"+k+".mat");}).ToArray();}var c=row["collider"];Vector3 V(Newtonsoft.Json.Linq.JToken t)=>new Vector3((float)t[0],(float)t[1],(float)t[2]);if(c!=null&&c.Type!=Newtonsoft.Json.Linq.JTokenType.Null){var box=g.AddComponent<BoxCollider>();box.center=V(c[0]);box.size=V(c[1]);}var sockets=new GameObject("Verified attachment datums").transform;sockets.SetParent(g.transform,false);foreach(var socket in row["sockets"]){var t=new GameObject((string)socket[0]).transform;t.SetParent(sockets,false);t.localPosition=V(socket[1]);}PrefabUtility.SaveAsPrefabAsset(g,dir+"Prefabs/"+n+".prefab");UnityEngine.Object.DestroyImmediate(g);}
var scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene();var ts=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).ToArray();var root=new GameObject("20 Illustrated apothecary composition 04");
GameObject Spawn(string n,Transform parent,Vector3 p,float yaw=0){var g=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(dir+"Prefabs/"+n+".prefab"));g.transform.SetParent(parent,false);g.transform.localPosition=p;g.transform.localRotation=Quaternion.Euler(0,yaw,0);PrefabUtility.RecordPrefabInstancePropertyModifications(g.transform);return g;}
Transform Obj(string n)=>ts.Single(t=>t.name==n);
var counter=Obj("CM_AF01_SalesCounter");Spawn("CM_IL04_CounterCarving",counter,Vector3.zero);Spawn("CM_IL04_CounterRunner",counter,Vector3.zero);
var shelf=Obj("CM_AF01_MedicineShelving");Spawn("CM_IL04_ShelfCarving",shelf,Vector3.zero);
foreach(int i in new[]{1,3}){var old=shelf.Find("CM_HR02_StockCourse"+i);old.gameObject.SetActive(false);PrefabUtility.RecordPrefabInstancePropertyModifications(old.gameObject);Spawn("CM_IL04_WorkingCollection"+i,shelf,new Vector3(0,i==1?.53f:1.45f,.02f));}
var table=Obj("CM_AF01_SideWorktable");Spawn("CM_IL04_PrepTableCraft",table,Vector3.zero);Spawn("CM_IL04_PreparationRecords",table,new Vector3(0,.976f,0));
// Verified existing wall faces, not implied extensions across open routes.
var placements=new[]{
("CM_IL04_BotanicalArchive",new Vector3(2.19f,1.98f,4.397f),180f,new Vector3(.82f,1,1)),
("CM_IL04_BotanicalArchive",new Vector3(5.00f,1.98f,4.397f),180f,new Vector3(.82f,1,1)),
("CM_IL04_BotanicalArchive",new Vector3(5.397f,2.03f,.31f),270f,new Vector3(.45f,.76f,1)),
("CM_IL04_BotanicalArchive",new Vector3(5.397f,2.03f,1.89f),270f,new Vector3(.45f,.76f,1)),
("CM_IL04_BotanicalArchive",new Vector3(5.603f,2.65f,5.37f),90f,Vector3.one),
("CM_IL04_HerbalBanner",new Vector3(8.45f,2.30f,2.003f),0f,Vector3.one),
("CM_IL04_JambDetail",new Vector3(2.47f,.20f,4.397f),180f,Vector3.one),
("CM_IL04_JambDetail",new Vector3(4.73f,.20f,4.397f),180f,Vector3.one),
("CM_IL04_Header",new Vector3(3.6f,3.12f,4.397f),180f,Vector3.one),
("CM_IL04_JambDetail",new Vector3(5.397f,.20f,1.96f),270f,Vector3.one),
("CM_IL04_JambDetail",new Vector3(5.397f,.20f,4.04f),270f,Vector3.one),
("CM_IL04_Header",new Vector3(5.397f,3.12f,3.0f),270f,Vector3.one),
("CM_IL04_WovenMat",new Vector3(3.60f,.201f,1.30f),0f,Vector3.one),
("CM_IL04_WovenMat",new Vector3(7.35f,.201f,4.15f),0f,new Vector3(.85f,1,.9f)),
("CM_IL04_FrontCraftwork",Vector3.zero,0f,Vector3.one),
("CM_IL04_LimewashRepair",new Vector3(5.12f,2.0f,-.203f),180f,new Vector3(.6f,.7f,1)),
("CM_IL04_LimewashRepair",new Vector3(-.203f,2.4f,1.35f),270f,Vector3.one),
("CM_IL04_HerbalBanner",new Vector3(-.203f,1.90f,1.15f),270f,new Vector3(1.2f,1.7f,1))
};
foreach(var p in placements){var g=Spawn(p.Item1,root.transform,p.Item2,p.Item3);g.transform.localScale=p.Item4;PrefabUtility.RecordPrefabInstancePropertyModifications(g.transform);}
// Reuse approved botanical meshes. Seated vines stay outside windows and doorway travel.
string botanical="Assets/BlightBloom/Art/Architecture/CrookedMortar/BotanicalPlanterKit01/Prefabs/";
var ivyPath=AssetDatabase.FindAssets("t:Prefab",new[]{botanical.TrimEnd('/')}).Select(g=>AssetDatabase.GUIDToAssetPath(g)).First(p=>p.Contains("Ivy_Wall"));
foreach(var p in new[]{new Vector3(.10f,1.25f,-.18f),new Vector3(.10f,3.45f,-.18f),new Vector3(5.27f,3.55f,-.18f)}){var g=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(ivyPath));g.name="Attached botanical trail 04";g.transform.SetParent(root.transform,false);g.transform.SetPositionAndRotation(p,Quaternion.Euler(0,180,0));g.transform.localScale=new Vector3(.75f,1.2f,.8f);PrefabUtility.RecordPrefabInstancePropertyModifications(g.transform);}
System.IO.File.WriteAllText("ArtSource/Blender/Interiors/CrookedMortar/Illustrated04/Installed.json","{\"installed\":true}");UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(scene);UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene);AssetDatabase.SaveAssets();return new{root=root.name,fixtures=placements.Length};
