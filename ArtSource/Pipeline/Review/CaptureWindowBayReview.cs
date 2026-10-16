var output=System.IO.Path.GetFullPath("ArtSource/Blender/Architecture/CrookedMortar/WindowBay01/Previews");
foreach(var name in new[]{"Front","ThreeQuarter","GameplayDistance"}){
var c=UnityEngine.GameObject.Find("Review_"+name).GetComponent<UnityEngine.Camera>();
var rt=new UnityEngine.RenderTexture(1440,1080,24,UnityEngine.RenderTextureFormat.ARGB32);rt.antiAliasing=4;
var prior=UnityEngine.RenderTexture.active;c.targetTexture=rt;c.Render();UnityEngine.RenderTexture.active=rt;
var tex=new UnityEngine.Texture2D(1440,1080,UnityEngine.TextureFormat.RGB24,false);tex.ReadPixels(new UnityEngine.Rect(0,0,1440,1080),0,0);tex.Apply();
System.IO.File.WriteAllBytes(output+"/"+name+".png",tex.EncodeToPNG());
c.targetTexture=null;UnityEngine.RenderTexture.active=prior;UnityEngine.Object.DestroyImmediate(tex);rt.Release();UnityEngine.Object.DestroyImmediate(rt);
}
return output;
