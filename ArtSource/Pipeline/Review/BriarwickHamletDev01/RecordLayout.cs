var D="ArtSource/Pipeline/Review/BriarwickHamletDev01";
var sites=new[]{
 new{id=1,name="The Crooked Mortar",x=-19f,z=25f,w=7.254f,d=13.756f,h=9.626f,yaw=138f},
 new{id=2,name="Inn and tavern",x=18f,z=16f,w=12f,d=15f,h=9f,yaw=238f},
 new{id=3,name="Blacksmith and forge",x=-26f,z=-25f,w=10f,d=8f,h=5.8f,yaw=70f},
 new{id=4,name="Bakery",x=19f,z=-10f,w=8f,d=9f,h=6.3f,yaw=270f},
 new{id=5,name="General merchant",x=-19f,z=0f,w=9f,d=10f,h=7f,yaw=90f},
 new{id=6,name="Village elders cottage",x=5f,z=42f,w=8f,d=9f,h=6.4f,yaw=190f},
 new{id=7,name="Farmhouse and stable",x=47f,z=-30f,w=10f,d=12f,h=7f,yaw=255f},
 new{id=8,name="Millers cottage",x=38f,z=-47f,w=8f,d=9f,h=6.6f,yaw=5f},
 new{id=9,name="Small chapel",x=-44f,z=30f,w=8f,d=13f,h=8.3f,yaw=135f},
 new{id=10,name="Family cottage A",x=-43f,z=-4f,w=7f,d=9f,h=6f,yaw=115f},
 new{id=11,name="Family cottage B",x=25f,z=43f,w=7.5f,d=9f,h=6.2f,yaw=210f}
};

if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().path!="Assets/Scenes/Briarwick_Hamlet_Dev01.unity")throw new System.Exception("Wrong scene");
var bRoot=GameObject.Find("03 Eleven primary building locations");var rr=new System.Collections.Generic.List<object>();
foreach(var f in GameObject.Find("02 Main road bridge and footpaths").GetComponentsInChildren<MeshFilter>()){if(!(f.name.StartsWith("Path_")||f.name.StartsWith("MainRoad_")))continue;var vs=f.sharedMesh.vertices;var pts=new System.Collections.Generic.List<Vector3>();for(int i=0;i<vs.Length;i+=2)pts.Add((vs[i]+vs[i+1])*.5f);float length=0;for(int i=1;i<pts.Count;i++)length+=Vector3.Distance(pts[i-1],pts[i]);float width=f.name.StartsWith("MainRoad")?5.2f:f.name=="Path_Farm"?3.2f:f.name=="Path_Miller"?2.8f:f.name=="Path_Forge"||f.name=="Path_Inn"?2.6f:f.name=="Path_Graveyard"||f.name=="Path_ApothecaryGarden"?2.2f:2.4f;rr.Add(new{name=f.name,widthMetres=width,mainRoad=f.name.StartsWith("MainRoad"),lengthMetres=length,points=pts.Select(p=>new[]{p.x,p.y,p.z}).ToArray()});}
var records=sites.Select(b=>{var t=bRoot.transform.Cast<Transform>().First(x=>x.name.StartsWith(b.id.ToString("00")+" "));var m=t.Find("Approach_DoorLocation");return new{b.id,b.name,position=new[]{t.position.x,t.position.y,t.position.z},width=b.w,depth=b.d,height=b.h,b.yaw,actualPrefab=b.id==1,approach=new[]{m.position.x,m.position.y,m.position.z}};}).ToArray();
var bridge=GameObject.Find("PedestrianAndHorseBridge_18mSpan_4.8mClear");var house=bRoot.transform.GetChild(0).GetChild(0).gameObject;
var report=new{scene=UnityEngine.SceneManagement.SceneManager.GetActiveScene().path,unityVersion=Application.unityVersion,terrainMetres=new[]{320,48,320},terrainOrigin=new[]{-160,0,-170},coreApproxMetres=new[]{150,110},sites=records,routes=rr,bridge=new{centre=new[]{bridge.transform.position.x,bridge.transform.position.y,bridge.transform.position.z},span=18,clearWidth=4.8f},commonMetres=new[]{26,30},crookedMortarPrefab=PrefabUtility.GetPrefabAssetPathOfNearestInstanceRoot(house),renderTriangles=house.GetComponentsInChildren<MeshFilter>().Sum(x=>x.sharedMesh.triangles.Length/3),buildingScale=new[]{house.transform.lossyScale.x,house.transform.lossyScale.y,house.transform.lossyScale.z},temporaryHorseEnvelope=new[]{1.2f,2.6f,2.8f}};
System.IO.File.WriteAllText(D+"/Layout.json",Newtonsoft.Json.JsonConvert.SerializeObject(report,Newtonsoft.Json.Formatting.Indented));return new{sites=records.Length,routes=rr.Count,triangles=report.renderTriangles};
