// Matched captures. Temporarily positions the existing review camera, then restores every changed value.
if(EditorApplication.isPlaying||UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Briarwick Edit only");
string D="ArtSource/Pipeline/Review/FamilyCottageAOriginalAppearance01";string phase="Restored";
var c=GameObject.Find("Briarwick_ReviewCamera").GetComponent<Camera>();var p=c.transform.localPosition;var q=c.transform.localRotation;var fov=c.fieldOfView;var ortho=c.orthographic;var mask=c.cullingMask;var oldTarget=c.targetTexture;var so=new SerializedObject(c.transform);var hint=so.FindProperty("m_LocalEulerAnglesHint").vector3Value;
var t=GameObject.Find("10 Family cottage A PLACEHOLDER").transform;var m=GameObject.Find("01 The Crooked Mortar ACTUAL PREFAB").transform;
var shots=new System.Collections.Generic.List<object>();
void Shot(string name,Vector3 pos,Vector3 target,float f){c.transform.position=pos;c.transform.LookAt(target);c.orthographic=false;c.fieldOfView=f;c.cullingMask=mask&~(1<<2);var rt=new RenderTexture(1600,1100,24);rt.antiAliasing=2;var old=RenderTexture.active;Texture2D im=null;try{c.targetTexture=rt;c.Render();RenderTexture.active=rt;im=new Texture2D(1600,1100,TextureFormat.RGB24,false);im.ReadPixels(new Rect(0,0,1600,1100),0,0);im.Apply();System.IO.File.WriteAllBytes(D+"/"+phase+"_"+name+".png",im.EncodeToPNG());shots.Add(new{name,position=new[]{pos.x,pos.y,pos.z},target=new[]{target.x,target.y,target.z},fov=f});}finally{c.targetTexture=oldTarget;RenderTexture.active=old;if(im!=null)UnityEngine.Object.DestroyImmediate(im);rt.Release();UnityEngine.Object.DestroyImmediate(rt);}}
try{
Shot("Front",t.TransformPoint(new Vector3(0,4.6f,14)),t.TransformPoint(new Vector3(0,2.9f,.2f)),49);
Shot("ThreeQuarter",t.position+new Vector3(14,7.4f,0),t.position+Vector3.up*3.2f,52);
Shot("Materials",t.TransformPoint(new Vector3(-4,4.5f,7)),t.TransformPoint(new Vector3(-1.9f,3.2f,.3f)),48);
Shot("Entrance",t.TransformPoint(new Vector3(-1,2.4f,5.5f)),t.TransformPoint(new Vector3(-1,1.8f,.95f)),48);
Shot("Cottage20m",t.position+new Vector3(20,9,0),t.position+Vector3.up*3.4f,55);
Shot("CrookedMortar20m",m.position+new Vector3(20,9,0),m.position+Vector3.up*3.4f,55);
}finally{c.transform.localPosition=p;c.transform.localRotation=q;c.fieldOfView=fov;c.orthographic=ortho;c.cullingMask=mask;c.targetTexture=oldTarget;so.Update();so.FindProperty("m_LocalEulerAnglesHint").vector3Value=hint;so.ApplyModifiedPropertiesWithoutUndo();}
System.IO.File.WriteAllText(D+"/"+phase+"_CaptureConditions.json",Newtonsoft.Json.JsonConvert.SerializeObject(shots,Newtonsoft.Json.Formatting.Indented));return new{phase,captures=shots.Count};
