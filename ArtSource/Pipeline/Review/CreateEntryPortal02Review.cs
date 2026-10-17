
var assetDir="Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02";
var scenePath="Assets/Scenes/CM_EntryPortal02_ArtReview.unity";
if(System.IO.File.Exists(scenePath)||System.IO.File.Exists(assetDir+"/Prefabs/CM_EntryPortal02.prefab"))throw new System.Exception("New asset outputs already exist; refusing overwrite");
var approved=UnityEngine.SceneManagement.SceneManager.GetActiveScene();
if(approved.isDirty||approved.path!="Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity")throw new System.Exception("Expected clean approved scene");
System.IO.Directory.CreateDirectory(assetDir+"/Materials");System.IO.Directory.CreateDirectory(assetDir+"/Prefabs");
AssetDatabase.Refresh();
var ti=(TextureImporter)AssetImporter.GetAtPath(assetDir+"/Textures/CM_EntryPortal02_Walnut_BaseColor.png");
ti.sRGBTexture=true;ti.mipmapEnabled=true;ti.maxTextureSize=2048;ti.textureCompression=TextureImporterCompression.Uncompressed;ti.anisoLevel=4;ti.wrapMode=TextureWrapMode.Clamp;ti.SaveAndReimport();
var mat=new Material(Shader.Find("Universal Render Pipeline/Lit")){name="CM_EntryPortal02_PaintedWalnut"};
mat.SetTexture("_BaseMap",AssetDatabase.LoadAssetAtPath<Texture2D>(assetDir+"/Textures/CM_EntryPortal02_Walnut_BaseColor.png"));mat.SetFloat("_Smoothness",0);mat.SetFloat("_Metallic",0);mat.SetFloat("_SpecularHighlights",0);mat.SetFloat("_EnvironmentReflections",0);mat.EnableKeyword("_SPECULARHIGHLIGHTS_OFF");mat.EnableKeyword("_ENVIRONMENTREFLECTIONS_OFF");
AssetDatabase.CreateAsset(mat,assetDir+"/Materials/CM_EntryPortal02_PaintedWalnut.mat");
var review=UnityEditor.SceneManagement.EditorSceneManager.NewScene(UnityEditor.SceneManagement.NewSceneSetup.EmptyScene,UnityEditor.SceneManagement.NewSceneMode.Additive);UnityEngine.SceneManagement.SceneManager.SetActiveScene(review);
var context=new GameObject("Approved07_VisualContext_ONLY_NoScriptsOrColliders");
var excluded=new[]{"Entry portal carved walnut upright","Entry post cap","Entry post shoe","Shallow storybook entry arch","Inner arch trim"};int copied=0;
foreach(var rr in approved.GetRootGameObjects().SelectMany(o=>o.GetComponentsInChildren<MeshRenderer>())){
if(!rr.enabled||!rr.gameObject.activeInHierarchy||excluded.Any(s=>rr.name.StartsWith(s)))continue;
var mf=rr.GetComponent<MeshFilter>();if(mf==null||mf.sharedMesh==null)continue;
var go=new GameObject(rr.name);go.transform.SetPositionAndRotation(rr.transform.position,rr.transform.rotation);go.transform.localScale=rr.transform.lossyScale;go.transform.SetParent(context.transform,true);go.AddComponent<MeshFilter>().sharedMesh=mf.sharedMesh;go.AddComponent<MeshRenderer>().sharedMaterials=rr.sharedMaterials;copied++;
}
context.transform.SetPositionAndRotation(new Vector3(.85f,-.20f,-5.52f),Quaternion.Euler(0,180,0));context.SetActive(false);
var root=new GameObject("CM_EntryPortal02");
var model=(GameObject)PrefabUtility.InstantiatePrefab(AssetDatabase.LoadAssetAtPath<GameObject>(assetDir+"/Models/CM_EntryPortal02.fbx"),review);
PrefabUtility.UnpackPrefabInstance(model,PrefabUnpackMode.Completely,InteractionMode.AutomatedAction);model.name="Geometry";model.transform.SetParent(root.transform,false);
var lod0=new GameObject("LOD0_CraftedParts");lod0.transform.SetParent(model.transform,false);var lod1=new GameObject("LOD1_Distance");lod1.transform.SetParent(model.transform,false);
foreach(var r in model.GetComponentsInChildren<MeshRenderer>()){
r.sharedMaterials=Enumerable.Repeat(mat,r.sharedMaterials.Length).ToArray();r.transform.SetParent(r.name.StartsWith("90_")?lod1.transform:lod0.transform,true);r.enabled=true;
}
var sockets=new GameObject("Attachments_Replaceable_EmptySockets");sockets.transform.SetParent(root.transform,false);
foreach(var j in Newtonsoft.Json.Linq.JArray.Parse(System.IO.File.ReadAllText("ArtSource/Blender/Architecture/CrookedMortar/EntryPortal02/AttachmentPoints.json"))){var s=new GameObject((string)j["name"]);s.transform.SetParent(sockets.transform,false);var p=j["position"].ToObject<float[]>();var r=j["rotation"].ToObject<float[]>();s.transform.localPosition=new Vector3(p[0],p[1],p[2]);s.transform.localEulerAngles=new Vector3(r[0],r[1],r[2]);}
var lg=root.AddComponent<LODGroup>();lg.SetLODs(new[]{new LOD(.18f,lod0.GetComponentsInChildren<Renderer>()),new LOD(.008f,lod1.GetComponentsInChildren<Renderer>())});lg.RecalculateBounds();
var prefab=PrefabUtility.SaveAsPrefabAsset(root,assetDir+"/Prefabs/CM_EntryPortal02.prefab");UnityEngine.Object.DestroyImmediate(root);root=(GameObject)PrefabUtility.InstantiatePrefab(prefab,review);
var stage=GameObject.CreatePrimitive(PrimitiveType.Cube);stage.name="ReviewOnly_Ground";stage.transform.position=new Vector3(0,-.1f,0);stage.transform.localScale=new Vector3(30,.2f,30);
var groundMat=new Material(Shader.Find("Universal Render Pipeline/Lit")){name="CM_EntryPortal02_ReviewGround"};groundMat.SetColor("_BaseColor",new Color(.32f,.34f,.32f));groundMat.SetFloat("_Smoothness",0);AssetDatabase.CreateAsset(groundMat,assetDir+"/Materials/CM_EntryPortal02_ReviewGround.mat");stage.GetComponent<Renderer>().sharedMaterial=groundMat;
RenderSettings.ambientMode=UnityEngine.Rendering.AmbientMode.Trilight;RenderSettings.ambientSkyColor=new Color(.57f,.60f,.66f);RenderSettings.ambientEquatorColor=new Color(.45f,.44f,.41f);RenderSettings.ambientGroundColor=new Color(.25f,.24f,.22f);RenderSettings.fog=false;RenderSettings.skybox=null;
var key=new GameObject("Review_Key").AddComponent<Light>();key.type=LightType.Directional;key.intensity=1.5f;key.color=new Color(1,.94f,.84f);key.transform.rotation=Quaternion.Euler(40,-35,0);key.shadows=LightShadows.Soft;
var fill=new GameObject("Review_Fill").AddComponent<Light>();fill.type=LightType.Directional;fill.intensity=.55f;fill.color=new Color(.83f,.89f,1);fill.transform.rotation=Quaternion.Euler(25,145,0);fill.shadows=LightShadows.None;
var cam=new GameObject("ReviewCamera").AddComponent<Camera>();cam.tag="MainCamera";cam.nearClipPlane=.05f;cam.farClipPlane=100;cam.fieldOfView=42;cam.backgroundColor=new Color(.24f,.27f,.30f);cam.clearFlags=CameraClearFlags.SolidColor;cam.transform.position=new Vector3(4.4f,2.8f,6.2f);cam.transform.LookAt(new Vector3(0,1.5f,0));
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(review,scenePath);UnityEditor.SceneManagement.EditorSceneManager.CloseScene(approved,true);AssetDatabase.SaveAssets();
return new {scene=scenePath,prefab=AssetDatabase.GetAssetPath(prefab),parts=lod0==null?12:12,contextRenderers=copied};