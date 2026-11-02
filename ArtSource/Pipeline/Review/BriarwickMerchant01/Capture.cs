// Matched captures. Temporarily positions the existing review camera, then restores every changed value.
if(EditorApplication.isPlaying||UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Briarwick Edit only");
string D="ArtSource/Pipeline/Review/BriarwickMerchant01";string phase="Merchant01";
var c=GameObject.Find("Briarwick_ReviewCamera").GetComponent<Camera>();var p=c.transform.localPosition;var q=c.transform.localRotation;var fov=c.fieldOfView;var ortho=c.orthographic;var mask=c.cullingMask;var oldTarget=c.targetTexture;var so=new SerializedObject(c.transform);var hint=so.FindProperty("m_LocalEulerAnglesHint").vector3Value;
var t=GameObject.Find("BW_Merchant01").transform;var m=GameObject.Find("01 The Crooked Mortar ACTUAL PREFAB").transform;var cottage=GameObject.Find("10 Family cottage A PLACEHOLDER").transform;
var shots=new System.Collections.Generic.List<object>();
void Shot(string name,Vector3 pos,Vector3 target,float f){c.transform.position=pos;c.transform.LookAt(target);c.orthographic=false;c.fieldOfView=f;c.cullingMask=mask&~(1<<2);var rt=new RenderTexture(1600,1100,24);rt.antiAliasing=2;var old=RenderTexture.active;Texture2D im=null;try{c.targetTexture=rt;c.Render();RenderTexture.active=rt;im=new Texture2D(1600,1100,TextureFormat.RGB24,false);im.ReadPixels(new Rect(0,0,1600,1100),0,0);im.Apply();System.IO.File.WriteAllBytes(D+"/"+phase+"_"+name+".png",im.EncodeToPNG());shots.Add(new{name,position=new[]{pos.x,pos.y,pos.z},target=new[]{target.x,target.y,target.z},fov=f});}finally{c.targetTexture=oldTarget;RenderTexture.active=old;if(im!=null)UnityEngine.Object.DestroyImmediate(im);rt.Release();UnityEngine.Object.DestroyImmediate(rt);}}
try{
Shot("Front",t.TransformPoint(new Vector3(0,3.6f,15)),t.TransformPoint(new Vector3(0,2.6f,2.5f)),54);
Shot("ThreeQuarter",t.TransformPoint(new Vector3(-10,6.5f,12)),t.TransformPoint(new Vector3(0,2.6f,1.7f)),52);
Shot("Side",t.TransformPoint(new Vector3(12,4.5f,2)),t.TransformPoint(new Vector3(0,2.6f,1.8f)),52);
Shot("Rear",t.TransformPoint(new Vector3(0,4,-12)),t.TransformPoint(new Vector3(0,2.6f,1.8f)),52);
Shot("CounterAwning",t.TransformPoint(new Vector3(-2.05f,1.95f,8.4f)),t.TransformPoint(new Vector3(-2.05f,1.7f,4.6f)),60);
Shot("VillageContext",new Vector3(8,23,-11),new Vector3(-17,8,8),60);
}finally{c.transform.localPosition=p;c.transform.localRotation=q;c.fieldOfView=fov;c.orthographic=ortho;c.cullingMask=mask;c.targetTexture=oldTarget;so.Update();so.FindProperty("m_LocalEulerAnglesHint").vector3Value=hint;so.ApplyModifiedPropertiesWithoutUndo();}
System.IO.File.WriteAllText(D+"/"+phase+"_CaptureConditions.json",Newtonsoft.Json.JsonConvert.SerializeObject(shots,Newtonsoft.Json.Formatting.Indented));return new{phase,captures=shots.Count};
