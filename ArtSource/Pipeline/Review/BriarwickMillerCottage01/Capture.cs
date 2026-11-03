// Matched captures. Temporarily positions the existing review camera, then restores every changed value.
if(EditorApplication.isPlaying||UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Briarwick Edit only");
string D="ArtSource/Pipeline/Review/BriarwickMillerCottage01";string phase="MillerCottage01";
var c=GameObject.Find("Briarwick_ReviewCamera").GetComponent<Camera>();var p=c.transform.localPosition;var q=c.transform.localRotation;var fov=c.fieldOfView;var ortho=c.orthographic;var mask=c.cullingMask;var oldTarget=c.targetTexture;var so=new SerializedObject(c.transform);var hint=so.FindProperty("m_LocalEulerAnglesHint").vector3Value;
var t=GameObject.Find("BW_MillerCottage01").transform;var m=GameObject.Find("01 The Crooked Mortar ACTUAL PREFAB").transform;var cottage=GameObject.Find("10 Family cottage A PLACEHOLDER").transform;
var shots=new System.Collections.Generic.List<object>();
void Shot(string name,Vector3 pos,Vector3 target,float f){c.transform.position=pos;c.transform.LookAt(target);c.orthographic=false;c.fieldOfView=f;c.cullingMask=mask&~(1<<2);var rt=new RenderTexture(1600,1100,24);rt.antiAliasing=2;var old=RenderTexture.active;Texture2D im=null;try{c.targetTexture=rt;c.Render();RenderTexture.active=rt;im=new Texture2D(1600,1100,TextureFormat.RGB24,false);im.ReadPixels(new Rect(0,0,1600,1100),0,0);im.Apply();System.IO.File.WriteAllBytes(D+"/"+phase+"_"+name+".png",im.EncodeToPNG());shots.Add(new{name,position=new[]{pos.x,pos.y,pos.z},target=new[]{target.x,target.y,target.z},fov=f});}finally{c.targetTexture=oldTarget;RenderTexture.active=old;if(im!=null)UnityEngine.Object.DestroyImmediate(im);rt.Release();UnityEngine.Object.DestroyImmediate(rt);}}
try{
Shot("Front",t.TransformPoint(new Vector3(0,3.6f,15)),t.TransformPoint(new Vector3(.5f,2.5f,0)),52);
Shot("ThreeQuarter",t.TransformPoint(new Vector3(11,6.2f,12)),t.TransformPoint(new Vector3(.5f,2.5f,0)),53);
Shot("Side",t.TransformPoint(new Vector3(14,4.5f,0)),t.TransformPoint(new Vector3(.5f,2.6f,0)),52);
Shot("Rear",t.TransformPoint(new Vector3(0,3.8f,-14)),t.TransformPoint(new Vector3(.5f,2.5f,0)),52);
Shot("CreekSide",t.TransformPoint(new Vector3(-10,4,-15)),t.TransformPoint(new Vector3(.5f,2,0)),59);
Shot("VillageContext",t.TransformPoint(new Vector3(-19,16,-20)),t.TransformPoint(new Vector3(0,1.5f,5)),60);
}finally{c.transform.localPosition=p;c.transform.localRotation=q;c.fieldOfView=fov;c.orthographic=ortho;c.cullingMask=mask;c.targetTexture=oldTarget;so.Update();so.FindProperty("m_LocalEulerAnglesHint").vector3Value=hint;so.ApplyModifiedPropertiesWithoutUndo();}
System.IO.File.WriteAllText(D+"/"+phase+"_CaptureConditions.json",Newtonsoft.Json.JsonConvert.SerializeObject(shots,Newtonsoft.Json.Formatting.Indented));return new{phase,captures=shots.Count};
