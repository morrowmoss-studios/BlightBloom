if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/CM_CrookedMortar_MassingRefinements05.unity"||UnityEditor.EditorApplication.isPlaying)throw new System.Exception("Require study 05 Edit mode");
var output=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/MassingRefinements05/Previews");System.IO.Directory.CreateDirectory(output);
var visual=UnityEngine.GameObject.Find("Player capsule visual");var active=visual.activeSelf;visual.SetActive(false);
var studies=new[]{UnityEngine.GameObject.Find("Study A - Conservative Refinement"),UnityEngine.GameObject.Find("Study B - Moderate Refinement"),UnityEngine.GameObject.Find("Study C - Bold Refinement")};var states=studies.Select(g=>g.activeSelf).ToArray();
try{
foreach(var id in new[]{"A","B","C"})foreach(var view in new[]{"Front","ThreeQuarter"}){
for(int i=0;i<3;i++)studies[i].SetActive(studies[i].name.StartsWith("Study "+id+" -"));
var c=UnityEngine.GameObject.Find("Study05_"+id+"_"+view).GetComponent<UnityEngine.Camera>();var rt=new UnityEngine.RenderTexture(1400,1200,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;var prior=UnityEngine.RenderTexture.active;c.targetTexture=rt;
try{c.Render();UnityEngine.RenderTexture.active=rt;var tex=new UnityEngine.Texture2D(1400,1200,UnityEngine.TextureFormat.RGB24,false);tex.ReadPixels(new UnityEngine.Rect(0,0,1400,1200),0,0);tex.Apply();System.IO.File.WriteAllBytes(output+"/"+id+"_"+view+".png",tex.EncodeToPNG());UnityEngine.Object.DestroyImmediate(tex);}finally{c.targetTexture=null;UnityEngine.RenderTexture.active=prior;rt.Release();UnityEngine.Object.DestroyImmediate(rt);}
}
}finally{visual.SetActive(active);for(int i=0;i<3;i++)studies[i].SetActive(states[i]);}
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());return "Captured all six neutral Editor previews";
