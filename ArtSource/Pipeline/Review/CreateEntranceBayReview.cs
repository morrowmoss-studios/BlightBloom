var scenePath="Assets/Scenes/CM_EntranceBay01_ArtReview.unity";
var assetRoot="Assets/BlightBloom/Art/Architecture/CrookedMortar/EntranceBay01";
if(System.IO.File.Exists(scenePath)) throw new System.Exception("Review scene already exists; refusing overwrite");
var original=UnityEngine.SceneManagement.SceneManager.GetActiveScene();
if(original.isDirty) throw new System.Exception("Current scene has unsaved edits; leaving it untouched");
UnityEditor.AssetDatabase.ImportAsset(assetRoot+"/Models/CM_EntranceBay01_Painted_v01.fbx",UnityEditor.ImportAssetOptions.ForceSynchronousImport);
var model=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.GameObject>(assetRoot+"/Models/CM_EntranceBay01_Painted_v01.fbx");
if(model==null)throw new System.Exception("FBX model missing");
System.IO.Directory.CreateDirectory(assetRoot+"/Materials");
System.IO.Directory.CreateDirectory(assetRoot+"/Prefabs");
UnityEditor.AssetDatabase.Refresh();
var palette=new System.Collections.Generic.Dictionary<string,UnityEngine.Color>{
{"Plaster",new UnityEngine.Color(.66f,.63f,.57f)}, {"Timber",new UnityEngine.Color(.23f,.20f,.17f)},
{"Sage",new UnityEngine.Color(.39f,.41f,.38f)}, {"Slate",new UnityEngine.Color(.29f,.31f,.32f)},
{"Iron",new UnityEngine.Color(.16f,.17f,.17f)}, {"Stone",new UnityEngine.Color(.57f,.55f,.49f)}};
var texturePath=assetRoot+"/Textures/CM_EntranceBay01_Painted_BaseColor_v01.png";
UnityEditor.AssetDatabase.ImportAsset(texturePath,UnityEditor.ImportAssetOptions.ForceSynchronousImport);
var ti=(UnityEditor.TextureImporter)UnityEditor.AssetImporter.GetAtPath(texturePath);ti.sRGBTexture=true;ti.maxTextureSize=4096;ti.mipmapEnabled=true;ti.filterMode=UnityEngine.FilterMode.Trilinear;ti.anisoLevel=4;ti.wrapMode=UnityEngine.TextureWrapMode.Clamp;ti.textureCompression=UnityEditor.TextureImporterCompression.Uncompressed;ti.SaveAndReimport();
var texture=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.Texture2D>(texturePath);
var materials=new System.Collections.Generic.Dictionary<string,UnityEngine.Material>();
foreach(var kv in palette){var m=new UnityEngine.Material(UnityEngine.Shader.Find("Universal Render Pipeline/Lit"));m.name="CM_Entrance_Painted_"+kv.Key;m.SetColor("_BaseColor",UnityEngine.Color.white);m.SetTexture("_BaseMap",texture);m.SetFloat("_Smoothness",0);m.SetFloat("_Metallic",0);m.SetFloat("_SpecularHighlights",0);m.SetFloat("_EnvironmentReflections",0);m.EnableKeyword("_SPECULARHIGHLIGHTS_OFF");m.EnableKeyword("_ENVIRONMENTREFLECTIONS_OFF");UnityEditor.AssetDatabase.CreateAsset(m,assetRoot+"/Materials/"+m.name+".mat");materials[kv.Key]=m;}
var review=UnityEditor.SceneManagement.EditorSceneManager.NewScene(UnityEditor.SceneManagement.NewSceneSetup.EmptyScene,UnityEditor.SceneManagement.NewSceneMode.Additive);
UnityEngine.SceneManagement.SceneManager.SetActiveScene(review);
var go=(UnityEngine.GameObject)UnityEditor.PrefabUtility.InstantiatePrefab(model,review);go.name="CM_EntranceBay01_PaintedReview_v01";
foreach(var r in go.GetComponentsInChildren<UnityEngine.Renderer>()) {r.sharedMaterials=r.sharedMaterials.Select(source=>{var key=palette.Keys.FirstOrDefault(k=>source!=null&&source.name.Contains(k));if(key==null)throw new System.Exception("Unknown material slot");return materials[key];}).ToArray();}
// Keep imported model connection and names; wrapper prefab retains a clear module root.
UnityEditor.PrefabUtility.SaveAsPrefabAsset(go,assetRoot+"/Prefabs/CM_EntranceBay01_Painted_v01.prefab");
// Review-only lighting: no project quality, renderer, or postprocessing changes.
UnityEngine.RenderSettings.ambientMode=UnityEngine.Rendering.AmbientMode.Trilight;
UnityEngine.RenderSettings.ambientSkyColor=new UnityEngine.Color(.61f,.64f,.68f);
UnityEngine.RenderSettings.ambientEquatorColor=new UnityEngine.Color(.48f,.49f,.51f);
UnityEngine.RenderSettings.ambientGroundColor=new UnityEngine.Color(.28f,.27f,.25f);
var lightGo=new UnityEngine.GameObject("Review_Key");var light=lightGo.AddComponent<UnityEngine.Light>();light.type=UnityEngine.LightType.Directional;light.intensity=1.5f;light.shadows=UnityEngine.LightShadows.Soft;lightGo.transform.rotation=UnityEngine.Quaternion.Euler(38,210,0);
var fillGo=new UnityEngine.GameObject("Review_Fill");var fill=fillGo.AddComponent<UnityEngine.Light>();fill.type=UnityEngine.LightType.Directional;fill.intensity=.55f;fill.shadows=UnityEngine.LightShadows.None;fillGo.transform.rotation=UnityEngine.Quaternion.Euler(20,335,0);
var names=new[]{"Front","ThreeQuarter","GameplayDistance"};
var positions=new[]{new UnityEngine.Vector3(0,1.85f,7),new UnityEngine.Vector3(4.6f,3.25f,6.7f),new UnityEngine.Vector3(1.8f,1.7f,8)};
for(int i=0;i<3;i++){var cgo=new UnityEngine.GameObject("Review_"+names[i]);var c=cgo.AddComponent<UnityEngine.Camera>();c.clearFlags=UnityEngine.CameraClearFlags.SolidColor;c.backgroundColor=new UnityEngine.Color(.30f,.32f,.34f);c.fieldOfView=i==2?55:40;c.nearClipPlane=.05f;c.farClipPlane=100;cgo.transform.position=positions[i];cgo.transform.LookAt(new UnityEngine.Vector3(0,1.8f,.1f));c.enabled=i==1;if(i==1)cgo.tag="MainCamera";}
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(review,scenePath);
UnityEditor.AssetDatabase.SaveAssets();
if(!original.isDirty)UnityEditor.SceneManagement.EditorSceneManager.CloseScene(original,true);
UnityEditor.Selection.activeGameObject=go;
if(UnityEditor.SceneView.lastActiveSceneView!=null)UnityEditor.SceneView.lastActiveSceneView.FrameSelected();
var importer=(UnityEditor.ModelImporter)UnityEditor.AssetImporter.GetAtPath(assetRoot+"/Models/CM_EntranceBay01_Painted_v01.fbx");
return "Created "+scenePath+"; model meshes="+go.GetComponentsInChildren<UnityEngine.MeshFilter>().Length+"; root scale="+go.transform.localScale+"; root rotation="+go.transform.eulerAngles+"; importer scale="+importer.globalScale+"; original scene dirty="+original.isDirty;
