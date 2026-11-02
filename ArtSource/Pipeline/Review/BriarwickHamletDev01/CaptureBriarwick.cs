// Adapted from the existing standalone test capture: new scene only, no asset/material edits.
if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Wrong scene");
var D="ArtSource/Pipeline/Review/BriarwickHamletDev01";var c=GameObject.Find("Briarwick_ReviewCamera").GetComponent<Camera>();var terrain=GameObject.Find("Briarwick_Valley_320x320m_EDITABLE").GetComponent<Terrain>();
var originalPosition=c.transform.position;var originalRotation=c.transform.rotation;var originalOrtho=c.orthographic;var originalSize=c.orthographicSize;var originalFov=c.fieldOfView;var originalMask=c.cullingMask;
void Shot(string name,Vector3 position,Vector3 target,bool ortho=false,float size=100,float fov=55){c.transform.position=position;c.transform.LookAt(target);c.orthographic=ortho;c.orthographicSize=size;c.fieldOfView=fov;c.cullingMask=ortho?~0:(~0&~(1<<2));var rt=new RenderTexture(1800,1200,24,RenderTextureFormat.ARGB32);rt.antiAliasing=2;var prior=RenderTexture.active;Texture2D image=null;try{c.targetTexture=rt;c.Render();RenderTexture.active=rt;image=new Texture2D(1800,1200,TextureFormat.RGB24,false);image.ReadPixels(new Rect(0,0,1800,1200),0,0);image.Apply();System.IO.File.WriteAllBytes(D+"/"+name+".png",image.EncodeToPNG());}finally{c.targetTexture=null;RenderTexture.active=prior;if(image!=null)UnityEngine.Object.DestroyImmediate(image);rt.Release();UnityEngine.Object.DestroyImmediate(rt);}}
try{
Shot("01_BirdsEye",new Vector3(0,185,-88),new Vector3(0,5,-14),true,115);
Shot("02_MainRoadApproach",new Vector3(8,terrain.SampleHeight(new Vector3(8,0,-96))+1.7f,-96),new Vector3(1,8,-4),false,100,65);
Shot("03_CommonAndCrookedMortar",new Vector3(12,8.5f,-5),new Vector3(-13,9,23),false,100,68);
Shot("04_CreekAndBridge",new Vector3(-8,13,-80),new Vector3(6,4.8f,-66),false,100,62);
Shot("05_CrookedMortarTerrainPlacement",new Vector3(-4,8.5f,11),new Vector3(-19,9,25),false,100,62);
}finally{c.transform.SetPositionAndRotation(originalPosition,originalRotation);c.orthographic=originalOrtho;c.orthographicSize=originalSize;c.fieldOfView=originalFov;c.cullingMask=originalMask;}
return new{images=5,scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene().path,gizmos=false,postProcessing=false};
