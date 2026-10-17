var output=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/FacadeBay01/Previews");System.IO.Directory.CreateDirectory(output);var cam=UnityEngine.GameObject.Find("FacadeReviewCamera").GetComponent<UnityEngine.Camera>();
var hero=UnityEngine.GameObject.Find("02_ApprovedB_HeroGable_Profile_Reference").transform;hero.GetChild(0).localPosition=new UnityEngine.Vector3(8.2f,0,0);
var names=new[]{"Front","ThreeQuarter","GameplayDistance","KitOverview"};var positions=new[]{new UnityEngine.Vector3(0,4.3f,16),new UnityEngine.Vector3(10.8f,7.2f,15),new UnityEngine.Vector3(4.8f,1.75f,11.5f),new UnityEngine.Vector3(17,10,23)};var targets=new[]{new UnityEngine.Vector3(0,4.25f,0),new UnityEngine.Vector3(0,3.8f,-.5f),new UnityEngine.Vector3(0,3.1f,0),new UnityEngine.Vector3(2.1f,3.5f,0)};
var references=new[]{UnityEngine.GameObject.Find("02_ApprovedB_HeroGable_Profile_Reference"),UnityEngine.GameObject.Find("03_IndependentModuleSamples"),UnityEngine.GameObject.Find("04_ApprovedEntryPortal02_ReferenceOnly")};
for(int i=0;i<names.Length;i++){
foreach(var reference in references)reference.SetActive(i==3);
cam.transform.position=positions[i];cam.transform.LookAt(targets[i]);cam.fieldOfView=i==2?55:45;
var rt=new UnityEngine.RenderTexture(1800,1400,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;var prev=UnityEngine.RenderTexture.active;cam.targetTexture=rt;cam.Render();UnityEngine.RenderTexture.active=rt;var image=new UnityEngine.Texture2D(1800,1400,UnityEngine.TextureFormat.RGB24,false);image.ReadPixels(new UnityEngine.Rect(0,0,1800,1400),0,0);image.Apply();System.IO.File.WriteAllBytes(output+"/"+names[i]+".png",image.EncodeToPNG());cam.targetTexture=null;UnityEngine.RenderTexture.active=prev;UnityEngine.Object.DestroyImmediate(image);rt.Release();UnityEngine.Object.DestroyImmediate(rt);
}
foreach(var reference in references)reference.SetActive(true);
cam.fieldOfView=45;cam.transform.position=positions[3];cam.transform.LookAt(targets[3]);UnityEditor.SceneManagement.EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());return output;
