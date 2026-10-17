if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity"||!UnityEditor.EditorApplication.isPlaying)throw new System.Exception("Require study 05 Play mode");
var player=UnityEngine.GameObject.Find("StyledProof Player");player.GetComponent<BlightBloom.Traversal.ThirdPersonMotor>().enabled=false;player.GetComponent<BlightBloom.Traversal.TraversalInput>().enabled=false;UnityEngine.Object.FindFirstObjectByType<BlightBloom.Traversal.ThirdPersonOrbitCamera>().enabled=false;var cc=player.GetComponent<UnityEngine.CharacterController>();
var summaries=new System.Collections.Generic.List<string>();
for(int study=1;study<2;study++){
float ox=0;cc.enabled=false;player.transform.position=new UnityEngine.Vector3(ox+.85f,.07f,-7.5f);cc.enabled=true;UnityEngine.Physics.SyncTransforms();
// Y holds expected standing height; -1 means a transition whose height is checked at the next landing.
var p=new System.Collections.Generic.List<UnityEngine.Vector3>{new(.85f,.04f,-6.4f),new(.85f,.24f,-4.4f),new(.85f,.24f,-1.4f),new(-1.3f,.24f,-1.2f),new(-1.3f,3.48f,5.0f),new(.65f,3.48f,5.0f),new(.65f,3.48f,3.25f)};
if(true){p.Add(new(3.15f,3.48f,3.25f));p.Add(new(3.15f,3.48f,4.1f));p.Add(new(3.15f,3.48f,3.25f));p.Add(new(.65f,3.48f,3.25f));}
p.AddRange(new UnityEngine.Vector3[]{new(.65f,3.48f,-1.6f),new(-1.35f,3.48f,-2.3f),new(.65f,3.48f,-1.6f),new(.65f,3.48f,5.0f),new(-1.3f,3.48f,5.0f),new(-1.3f,.24f,-1.2f),new(.95f,.24f,-1.1f),new(.95f,.24f,3.25f),new(3.15f,.24f,3.25f),new(3.15f,.24f,4.1f),new(3.15f,.24f,3.25f),new(.95f,.24f,3.25f),new(1.05f,.04f,6.7f),new(6.5f,.04f,6.7f),new(6.5f,.04f,-6.7f),new(.85f,.04f,-6.7f)});
if(study==2){int at=p.FindIndex(v=>v.x==-1.35f);p.InsertRange(at+1,new UnityEngine.Vector3[]{new(-.9f,3.48f,-2.3f),new(-.9f,3.48f,-4.25f),new(-.9f,3.48f,-2.3f)});}
var lines=new System.Collections.Generic.List<string>();bool passed=true;int index=0;
foreach(var point in p){var target=new UnityEngine.Vector2(ox+point.x,point.z);int it=0;for(;it<800;it++){var pos=player.transform.position;var d=new UnityEngine.Vector3(target.x-pos.x,0,target.y-pos.z);if(d.magnitude<.10f)break;var prior=pos;cc.Move(UnityEngine.Vector3.ClampMagnitude(d,.055f)+UnityEngine.Vector3.down*.045f);UnityEngine.Physics.SyncTransforms();if(it>20&&(player.transform.position-prior).magnitude<.0001f)break;}
for(int i=0;i<8;i++)cc.Move(UnityEngine.Vector3.down*.045f);
var at=player.transform.position;var err=UnityEngine.Vector2.Distance(new(at.x,at.z),target);var heightErr=System.Math.Abs(at.y-point.y);lines.Add(index+": target="+point.ToString("F3")+" actualLocal="+new UnityEngine.Vector3(at.x-ox,at.y,at.z).ToString("F3")+" planarError="+err.ToString("F3")+" heightError="+heightErr.ToString("F3")+" iterations="+it);if(err>.18f||heightErr>.17f){passed=false;break;}index++;}
var summary=((char)('A'+study))+": passed="+passed+" reached="+index+"/"+p.Count;summaries.Add(summary);System.IO.File.WriteAllText("ArtSource/Blender/Architecture/CrookedMortar/StyledDetails07/Traversal_"+(char)('A'+study)+".txt",summary+"\n"+string.Join("\n",lines));
}
return summaries;
