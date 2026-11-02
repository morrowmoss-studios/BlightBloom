// Scoped corrections to task-created assets only. Not a general scene rebuild.
if(EditorApplication.isPlaying||UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Briarwick Edit mode only");
var terrain=GameObject.Find("Briarwick_Valley_320x320m_EDITABLE").GetComponent<Terrain>();terrain.heightmapPixelError=1;
foreach(var f in GameObject.Find("02 Main road bridge and footpaths").GetComponentsInChildren<MeshFilter>()){
if(!(f.name.StartsWith("Path_")||f.name.StartsWith("MainRoad_")||f.name=="Bridge_ContinuousWalkDeck"))continue;var mesh=f.sharedMesh;var vs=mesh.vertices;for(int i=0;i<vs.Length;i++)vs[i].y+=.03f;
if(f.name=="Path_Merchant"){for(int p=0;p<3;p++){float amount=.6f*(3-p)/3;vs[vs.Length-1-p*2].x+=amount;vs[vs.Length-2-p*2].x+=amount;}}
mesh.vertices=vs;mesh.RecalculateNormals();mesh.RecalculateBounds();var col=f.GetComponent<MeshCollider>();if(col!=null){col.sharedMesh=null;col.sharedMesh=mesh;}EditorUtility.SetDirty(mesh);AssetDatabase.SaveAssetIfDirty(mesh);
}
GameObject.Find("PedestrianAndHorseBridge_18mSpan_4.8mClear").transform.position+=Vector3.up*.03f;
foreach(string n in new[]{"Woodland_CombinedCanopyMasses_PROXY","Woodland_CombinedTrunkMasses_PROXY"}){var m=GameObject.Find(n).GetComponent<MeshFilter>().sharedMesh;var t=m.triangles;for(int i=0;i<t.Length;i+=3){int v=t[i+1];t[i+1]=t[i+2];t[i+2]=v;}m.triangles=t;m.RecalculateNormals();EditorUtility.SetDirty(m);AssetDatabase.SaveAssetIfDirty(m);}
var common=GameObject.Find("Common_26x30m_ActivityReserve").GetComponent<MeshFilter>().sharedMesh;var cv=common.vertices;for(int i=0;i<cv.Length;i++){float u=cv[i].x/13,v=(cv[i].z-5)/15;float x=13*u*Mathf.Sqrt(1-v*v*.5f),z=15*v*Mathf.Sqrt(1-u*u*.5f);float a=Mathf.Atan2(z,x);float scale=1+.035f*Mathf.Sin(a*3)+.025f*Mathf.Cos(a*5);x*=scale;z=5+z*scale;cv[i]=new Vector3(x,terrain.SampleHeight(new Vector3(x,0,z))+.055f,z);}common.vertices=cv;common.RecalculateNormals();common.RecalculateBounds();EditorUtility.SetDirty(common);AssetDatabase.SaveAssetIfDirty(common);
foreach(var t in GameObject.Find("07 Review cameras and planning labels").GetComponentsInChildren<TextMesh>())t.characterSize=t.name=="PlanningLabel"?.23f:.16f;
UnityEditor.SceneManagement.EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());return new{merchantApproachClearanceAddedMetres=.6f,roadVisualOffsetAdded=.03f,forestWindingCorrected=true,common="organic oval",planningLabelsEnlarged=true};
