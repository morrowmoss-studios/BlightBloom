var cam=UnityEngine.GameObject.Find("IntegrationPreviewCamera").GetComponent<UnityEngine.Camera>();
var folder=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/EntryPortal02/IntegrationPreview/Cleaned");System.IO.Directory.CreateDirectory(folder);
var names=new[]{"Front","ThreeQuarter","CloseUp"};var pos=new[]{new UnityEngine.Vector3(.85f,2.6f,-13),new UnityEngine.Vector3(-5.5f,3.4f,-12),new UnityEngine.Vector3(-2.7f,2.8f,-8.5f)};
for(int i=0;i<3;i++){
cam.transform.position=pos[i];cam.fieldOfView=i==2?48:45;cam.transform.LookAt(new UnityEngine.Vector3(.85f,i==2?2.55f:2.4f,-3.8f));
var rt=new UnityEngine.RenderTexture(1600,1200,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;var prior=UnityEngine.RenderTexture.active;cam.targetTexture=rt;cam.Render();UnityEngine.RenderTexture.active=rt;var image=new UnityEngine.Texture2D(1600,1200,UnityEngine.TextureFormat.RGB24,false);image.ReadPixels(new UnityEngine.Rect(0,0,1600,1200),0,0);image.Apply();System.IO.File.WriteAllBytes(folder+"/"+names[i]+".png",image.EncodeToPNG());cam.targetTexture=null;UnityEngine.RenderTexture.active=prior;UnityEngine.Object.DestroyImmediate(image);rt.Release();UnityEngine.Object.DestroyImmediate(rt);
}
cam.fieldOfView=45;cam.transform.position=pos[1];cam.transform.LookAt(new UnityEngine.Vector3(.85f,2.4f,-3.8f));
if(UnityEditor.SceneView.lastActiveSceneView!=null)UnityEditor.SceneView.lastActiveSceneView.LookAt(new UnityEngine.Vector3(.85f,2.4f,-3.8f),cam.transform.rotation,6.5f);
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());

return folder;