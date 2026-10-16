var scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene();
if(scene.path!="Assets/Scenes/CM_WindowBay01_ArtReview.unity"||scene.isDirty)throw new System.Exception("Require clean isolated review scene");
var root="Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01";
var fbx=root+"/Models/CM_WindowBay01_Painted_v02.fbx";
var texturePath=root+"/Textures/CM_WindowBay01_Painted_BaseColor_v02.png";
if(UnityEngine.GameObject.Find("CM_WindowBay01_PaintedReview_v02")!=null)throw new System.Exception("Painted review already exists");
UnityEditor.AssetDatabase.ImportAsset(fbx,UnityEditor.ImportAssetOptions.ForceSynchronousImport);
UnityEditor.AssetDatabase.ImportAsset(texturePath,UnityEditor.ImportAssetOptions.ForceSynchronousImport);
var ti=(UnityEditor.TextureImporter)UnityEditor.AssetImporter.GetAtPath(texturePath);
ti.textureType=UnityEditor.TextureImporterType.Default;ti.sRGBTexture=true;ti.mipmapEnabled=true;ti.maxTextureSize=4096;ti.wrapMode=UnityEngine.TextureWrapMode.Clamp;ti.filterMode=UnityEngine.FilterMode.Trilinear;ti.anisoLevel=4;ti.textureCompression=UnityEditor.TextureImporterCompression.Uncompressed;ti.SaveAndReimport();
var texture=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.Texture2D>(texturePath);
var mats=new System.Collections.Generic.Dictionary<string,UnityEngine.Material>();
foreach(var key in new[]{"Plaster","Timber","Shutters","Slate","Iron","Soil"}){
var path=root+"/Materials/CM_Painted_"+key+"_v02.mat";
if(System.IO.File.Exists(path))throw new System.Exception("Refusing existing material "+path);
var m=new UnityEngine.Material(UnityEngine.Shader.Find("Universal Render Pipeline/Lit"));m.name="CM_Painted_"+key+"_v02";m.SetTexture("_BaseMap",texture);m.SetColor("_BaseColor",UnityEngine.Color.white);m.SetFloat("_Smoothness",0);m.SetFloat("_Metallic",0);m.SetFloat("_SpecularHighlights",0);m.SetFloat("_EnvironmentReflections",0);m.EnableKeyword("_SPECULARHIGHLIGHTS_OFF");m.EnableKeyword("_ENVIRONMENTREFLECTIONS_OFF");UnityEditor.AssetDatabase.CreateAsset(m,path);mats[key]=m;}
var model=UnityEditor.AssetDatabase.LoadAssetAtPath<UnityEngine.GameObject>(fbx);
var go=(UnityEngine.GameObject)UnityEditor.PrefabUtility.InstantiatePrefab(model,scene);go.name="CM_WindowBay01_PaintedReview_v02";
foreach(var r in go.GetComponentsInChildren<UnityEngine.Renderer>()) {var n=r.sharedMaterial.name;var key=mats.Keys.FirstOrDefault(k=>n.Contains(k));if(key==null)throw new System.Exception("Unknown semantic material "+n);r.sharedMaterial=mats[key];}
UnityEditor.PrefabUtility.SaveAsPrefabAsset(go,root+"/Prefabs/CM_WindowBay01_Painted_v02.prefab");
var previous=UnityEngine.GameObject.Find("CM_WindowBay01_PaintedReview_v01");if(previous==null)throw new System.Exception("Previous painted reference missing");previous.SetActive(false);
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene);UnityEditor.AssetDatabase.SaveAssets();UnityEditor.Selection.activeGameObject=go;
return "Painted FBX applied; v01 and neutral references preserved inactive; texture="+texture.width+"x"+texture.height+"; review lighting and cameras untouched.";
