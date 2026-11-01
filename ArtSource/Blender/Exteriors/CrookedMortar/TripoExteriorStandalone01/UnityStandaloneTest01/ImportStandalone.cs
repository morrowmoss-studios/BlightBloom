var D="ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/UnityStandaloneTest01";
var A="Assets/BlightBloom/Art/Exteriors/CrookedMortar/Standalone01";
if(EditorApplication.isPlaying||EditorApplication.isCompiling)throw new System.Exception("Require Edit mode, no compilation.");
if(new System.IO.DriveInfo("/").AvailableFreeSpace<3000000000L)throw new System.Exception("Disk reserve <3GB");
if(System.IO.Directory.Exists(A))throw new System.Exception("Existing standalone output: inspect before continuing");
void Folder(string p){if(AssetDatabase.IsValidFolder(p))return;Folder(System.IO.Path.GetDirectoryName(p).Replace('\\','/'));AssetDatabase.CreateFolder(System.IO.Path.GetDirectoryName(p).Replace('\\','/'),System.IO.Path.GetFileName(p));}
foreach(var p in new[]{A+"/Models",A+"/Textures",A+"/Materials",A+"/Prefabs",A+"/TestTerrain"})Folder(p);
var watch=System.Diagnostics.Stopwatch.StartNew();var freeBefore=new System.IO.DriveInfo("/").AvailableFreeSpace;
var fbx=A+"/Models/CM_CrookedMortar_Standalone01.fbx";
AssetDatabase.StartAssetEditing();try{
 var meta=System.IO.File.ReadAllText("Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Models/CM_CrookedMortar_ExteriorRecovery01.fbx.meta");meta=System.Text.RegularExpressions.Regex.Replace(meta,@"(?m)^guid: .*$","guid: "+System.Guid.NewGuid().ToString("N"));
 System.IO.File.WriteAllText(fbx+".meta",meta);System.IO.File.Copy(D+"/Exports/CM_CrookedMortar_Standalone01.fbx",fbx,false);
 foreach(var n in new[]{"FoundationReturn_MatchedStone.png","FoundationReturn_Normal.png"})System.IO.File.Copy("ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/"+n,A+"/Textures/"+n,false);
}finally{AssetDatabase.StopAssetEditing();}
AssetDatabase.ImportAsset(fbx,ImportAssetOptions.ForceSynchronousImport);
foreach(var n in new[]{"FoundationReturn_MatchedStone.png","FoundationReturn_Normal.png"}){var p=A+"/Textures/"+n;AssetDatabase.ImportAsset(p,ImportAssetOptions.ForceSynchronousImport);var ti=(TextureImporter)AssetImporter.GetAtPath(p);bool normal=n.Contains("Normal");ti.textureType=normal?TextureImporterType.NormalMap:TextureImporterType.Default;ti.sRGBTexture=!normal;ti.maxTextureSize=1024;ti.npotScale=TextureImporterNPOTScale.None;ti.mipmapEnabled=true;ti.anisoLevel=4;ti.wrapMode=TextureWrapMode.Clamp;ti.textureCompression=TextureImporterCompression.CompressedHQ;ti.SaveAndReimport();}
var m=new Material(Shader.Find("Universal Render Pipeline/Lit"));m.name="CM_Standalone_LocalFoundationReturns";m.SetTexture("_BaseMap",AssetDatabase.LoadAssetAtPath<Texture2D>(A+"/Textures/FoundationReturn_MatchedStone.png"));m.SetColor("_BaseColor",Color.white);m.SetFloat("_Smoothness",.13f);m.SetTexture("_BumpMap",AssetDatabase.LoadAssetAtPath<Texture2D>(A+"/Textures/FoundationReturn_Normal.png"));m.SetFloat("_BumpScale",.18f);m.EnableKeyword("_NORMALMAP");AssetDatabase.CreateAsset(m,A+"/Materials/CM_Standalone_LocalFoundationReturns.mat");AssetDatabase.SaveAssetIfDirty(m);
watch.Stop();var model=AssetDatabase.LoadAssetAtPath<GameObject>(fbx);if(model==null)throw new System.Exception("Model import failed");
var report=new{importAndTextureSetupSeconds=watch.Elapsed.TotalSeconds,freeBytesBefore=freeBefore,freeBytesAfter=new System.IO.DriveInfo("/").AvailableFreeSpace,fbxBytes=new System.IO.FileInfo(fbx).Length,meshCount=model.GetComponentsInChildren<MeshFilter>().Length,triangles=model.GetComponentsInChildren<MeshFilter>().Sum(x=>x.sharedMesh.triangles.Length/3),meshes=model.GetComponentsInChildren<MeshFilter>().Select(x=>new{name=x.name,vertices=x.sharedMesh.vertexCount,submeshes=x.sharedMesh.subMeshCount,uvs=x.sharedMesh.uv.Length,normals=x.sharedMesh.normals.Length}).ToArray()};
System.IO.File.WriteAllText(D+"/UnityImport.json",Newtonsoft.Json.JsonConvert.SerializeObject(report,Newtonsoft.Json.Formatting.Indented));return report;
