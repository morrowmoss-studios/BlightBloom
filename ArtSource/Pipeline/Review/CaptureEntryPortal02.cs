var output=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/EntryPortal02/Previews");System.IO.Directory.CreateDirectory(output);
var cam=UnityEngine.GameObject.Find("ReviewCamera").GetComponent<UnityEngine.Camera>();var context=UnityEngine.Resources.FindObjectsOfTypeAll<UnityEngine.GameObject>().First(o=>o.name=="Approved07_VisualContext_ONLY_NoScriptsOrColliders"&&o.scene.IsValid());
var root=UnityEngine.GameObject.Find("CM_EntryPortal02");root.GetComponent<UnityEngine.LODGroup>().ForceLOD(0);
var positions=new[]{new UnityEngine.Vector3(0,1.5f,6.3f),new UnityEngine.Vector3(4.4f,2.8f,6.2f),new UnityEngine.Vector3(-3.1f,1.85f,6.5f),new UnityEngine.Vector3(7.8f,5.2f,11f)};
var names=new[]{"Front","ThreeQuarter","GameplayDistance","ApprovedContextFit"};
for(int i=0;i<4;i++){
context.SetActive(i==3);cam.transform.position=positions[i];cam.fieldOfView=i==2?55:42;cam.transform.LookAt(new UnityEngine.Vector3(0,i==3?2.8f:1.5f,0));
var rt=new UnityEngine.RenderTexture(1440,1440,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;var prior=UnityEngine.RenderTexture.active;cam.targetTexture=rt;cam.Render();UnityEngine.RenderTexture.active=rt;var tex=new UnityEngine.Texture2D(1440,1440,UnityEngine.TextureFormat.RGB24,false);tex.ReadPixels(new UnityEngine.Rect(0,0,1440,1440),0,0);tex.Apply();System.IO.File.WriteAllBytes(output+"/"+names[i]+".png",tex.EncodeToPNG());cam.targetTexture=null;UnityEngine.RenderTexture.active=prior;UnityEngine.Object.DestroyImmediate(tex);rt.Release();UnityEngine.Object.DestroyImmediate(rt);
}
context.SetActive(false);root.GetComponent<UnityEngine.LODGroup>().ForceLOD(-1);cam.fieldOfView=42;cam.transform.position=positions[1];cam.transform.LookAt(new UnityEngine.Vector3(0,1.5f,0));UnityEditor.SceneManagement.EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());return output;
