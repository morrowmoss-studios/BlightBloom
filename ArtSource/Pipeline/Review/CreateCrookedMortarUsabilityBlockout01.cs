var path="Assets/Scenes/CM_CrookedMortar_UsabilityBlockout01.unity";
var dir="Assets/BlightBloom/Prototypes/CrookedMortarUsability01";
if(EditorApplication.isPlaying || EditorApplication.isCompiling || System.IO.File.Exists(path)) throw new System.Exception("Busy or destination exists");
var old=UnityEngine.SceneManagement.SceneManager.GetActiveScene(); if(old.isDirty)throw new System.Exception("Unsaved scene");
var source=old.GetRootGameObjects().First(g=>g.name=="06 Existing Third Person Player and Camera");
var scene=UnityEditor.SceneManagement.EditorSceneManager.NewScene(UnityEditor.SceneManagement.NewSceneSetup.EmptyScene,UnityEditor.SceneManagement.NewSceneMode.Additive);
UnityEngine.SceneManagement.SceneManager.SetActiveScene(scene);
Transform Group(string n){return new GameObject(n).transform;}
var shell=Group("01 Wall shell - clear dimensions in metres");var floors=Group("02 Continuous floors and ceilings");var stairs=Group("03 U stair - 18 risers 1.5m flights");var furniture=Group("04 Representative furniture - solid footprints");var roof=Group("05 Silhouette guides - no finished art");var markers=Group("06 Room and route datums");
var colors=new[]{new Color(.70f,.66f,.56f),new Color(.27f,.34f,.34f),new Color(.35f,.27f,.22f),new Color(.48f,.57f,.46f),new Color(.48f,.43f,.56f),new Color(.62f,.48f,.34f)};
var mats=new Material[colors.Length];for(int i=0;i<mats.Length;i++){mats[i]=new Material(Shader.Find("Universal Render Pipeline/Lit"));mats[i].name="Layout01_"+i;mats[i].SetColor("_BaseColor",colors[i]);mats[i].SetFloat("_Smoothness",0);AssetDatabase.CreateAsset(mats[i],dir+"/"+mats[i].name+".mat");}
GameObject Box(string n,Transform par,float x,float y,float z,float sx,float sy,float sz,int mat=0,bool collision=true){var g=GameObject.CreatePrimitive(PrimitiveType.Cube);g.name=n;g.transform.SetParent(par,false);g.transform.position=new Vector3(x,y,z);g.transform.localScale=new Vector3(sx,sy,sz);g.GetComponent<Renderer>().sharedMaterial=mats[mat];if(!collision)UnityEngine.Object.DestroyImmediate(g.GetComponent<Collider>());return g;}
void Slab(string n,float x0,float x1,float z0,float z1,float top,float thick,int mat=1){Box(n,floors,(x0+x1)/2,top-thick/2,(z0+z1)/2,x1-x0,thick,z1-z0,mat);}
void Wall(string n,bool alongX,float fixedAt,float a,float b,float bottom,float top,int mat=0){if(b-a<.001f)return;Box(n,shell,alongX?(a+b)/2:fixedAt,(bottom+top)/2,alongX?fixedAt:(a+b)/2,alongX?b-a:.2f,top-bottom,alongX?.2f:b-a,mat);}
void DoorWall(string n,bool alongX,float at,float a,float b,float center,float width,float baseY){Wall(n+" jamb A",alongX,at,a,center-width/2,baseY,baseY+3.1f);Wall(n+" jamb B",alongX,at,center+width/2,b,baseY,baseY+3.1f);Wall(n+" lintel 2.75m clear",alongX,at,center-width/2,center+width/2,baseY+2.75f,baseY+3.1f);}
// Union of three offset volumes plus a stair-access nook. Top surfaces are 0.2m and 3.6m.
Slab("Site / garden - 30m",-10,20,-8,18,0,.25f,3);
Slab("Shop floor 5.4 x 4.4",-.2f,5.6f,-.2f,4.6f,.2f,.2f);
Slab("Rear body floor",-2.2f,5.6f,4.6f,9.2f,.2f,.2f);
Slab("Stair lobby floor 2.0 x 2.4",-2.2f,0,2.2f,4.6f,.2f,.2f);
Slab("Wing floor",5.6f,9.2f,1.8f,9,.2f,.2f);
Slab("Upper living and open landing",-.2f,5.6f,-.2f,4.6f,3.6f,.3f);
Slab("Upper landing west return",-2.2f,-.2f,2.2f,4.6f,3.6f,.3f);
Slab("Bedroom full floor",1.4f,5.6f,4.6f,9.2f,3.6f,.3f);
Slab("Study full floor",5.6f,9.2f,1.8f,6.4f,3.6f,.3f);
// Ceilings cover rooms but never the stairwell. 3.10m clear throughout.
Slab("Living ceiling",-.2f,5.6f,-.2f,4.6f,6.85f,.15f,0);
Slab("Landing nook ceiling",-2.2f,-.2f,2.2f,4.6f,6.85f,.15f,0);
Slab("Rear bedroom and stair ceiling",-2.2f,5.6f,4.6f,9.2f,6.85f,.15f,0);
Slab("Study ceiling",5.6f,9.2f,1.8f,6.4f,6.85f,.15f,0);
Slab("Storage ceiling",5.6f,9.2f,6.4f,9,3.45f,.15f,0);
// Ground perimeter; side-wing access is independent of treatment.
DoorWall("Front entrance 2.0",true,-.1f,-.2f,5.6f,3.7f,2,.2f);
Wall("West shop front",false,-.1f,0,2.2f,.2f,3.3f);
Wall("Lobby south return",true,2.1f,-2.2f,0,.2f,3.3f);Wall("West lobby and stair",false,-2.1f,2.2f,9.2f,.2f,6.7f);
Wall("Rear body north",true,9.1f,-2.2f,5.6f,.2f,6.7f);
DoorWall("Shop to kitchen 1.8",false,5.5f,0,4.4f,3,1.8f,.2f);
DoorWall("Shop to treatment 2.0",true,4.5f,1.8f,5.4f,3.6f,2,.2f);
Wall("Treatment west partition",false,1.7f,4.6f,9,.2f,3.3f);
Wall("Treatment to wing",false,5.5f,4.6f,9,.2f,3.3f);
Wall("Wing front ground",true,1.9f,5.6f,9.2f,.2f,3.3f);Wall("Wing east ground",false,9.1f,2,9,.2f,3.3f);
DoorWall("Kitchen to storage 1.8",true,6.3f,5.6f,9,7.7f,1.8f,.2f);DoorWall("Storage garden exit 1.8",true,8.9f,5.6f,9,7.7f,1.8f,.2f);
// Upper plan: no partition between landing and living.
Wall("Upper front",true,-.1f,-.2f,5.6f,3.6f,6.7f);Wall("Upper shop west front",false,-.1f,0,2.2f,3.6f,6.7f);Wall("Upper nook south",true,2.1f,-2.2f,0,3.6f,6.7f);
DoorWall("Living to study 1.8",false,5.5f,0,4.4f,3,1.8f,3.6f);
DoorWall("Landing to bedroom 2.0",true,4.5f,1.8f,5.4f,3.6f,2,3.6f);
Wall("Bedroom west partition",false,1.7f,4.6f,9,3.6f,6.7f);Wall("Bedroom east",false,5.5f,4.6f,9,3.6f,6.7f);
Wall("Study front",true,1.9f,5.6f,9.2f,3.6f,6.7f);Wall("Study east",false,9.1f,2,6.4f,3.6f,6.7f);Wall("Study rear",true,6.3f,5.6f,9.2f,3.6f,6.7f);
// Actual solid steps, 0.1889m risers, 0.30m goings. No ramp cheat.
for(int i=0;i<9;i++){float h=.2f+(i+1)*3.4f/18;Box("Lower tread "+(i+1),stairs,-1.25f,(h+.2f)/2,4.6f+(i+.5f)*.3f,1.5f,h-.2f,.3f,2);}
Box("Intermediate landing 3.2 x 1.5",stairs,-.4f,1.8f,8.05f,3.2f,.2f,1.5f,2);
for(int i=0;i<9;i++){float h=1.9f+(i+1)*3.4f/18;Box("Upper tread "+(i+1),stairs,.45f,h-.10f,7.3f-(i+.5f)*.3f,1.5f,.2f,.3f,2);}
// Guard screens prevent falling, but stay out of the 1.5m clear flights.
Box("Centre stair guard",stairs,-.4f,2.6f,5.95f,.2f,1.4f,2.7f,2);
Box("Upper east stairwell guard",stairs,1.3f,4.15f,6.65f,.2f,1.1f,4.1f,2);
Box("Rear landing guard",stairs,-.4f,2.45f,8.85f,3.2f,1.1f,.1f,2);
// Furniture footprints have full colliders. Nothing is scaled down to fake circulation.
Box("Shop counter 2.2 x .75",furniture,1.1f,.7f,1.25f,2.2f,1,.75f,5);
Box("Shop shelf .35 deep",furniture,.18f,1.1f,2.25f,.35f,1.8f,1.4f,5);
Box("Examination bed .9 x 2.0",furniture,4.75f,.65f,7.6f,.9f,.9f,2,4);
Box("Treatment cabinet .40 deep",furniture,2.05f,1.1f,8.1f,.4f,1.8f,1.5f,5);
Box("Kitchen east workbench .65 x 3.4",furniture,8.675f,.7f,4.1f,.65f,1,3.4f,5);
Box("Kitchen front preparation 1.5 x .65",furniture,7.1f,.7f,2.325f,1.5f,1,.65f,5);
Box("Storage west shelf .45",furniture,5.825f,1.1f,7.6f,.45f,1.8f,1.8f,5);
Box("Storage east shelf .45",furniture,8.775f,1.1f,7.6f,.45f,1.8f,1.8f,5);
Box("Bedroom bed 1.6 x 2.1",furniture,3.6f,3.95f,7.85f,1.6f,.7f,2.1f,4);
Box("Bedroom wardrobe .5 x 1.2",furniture,2.05f,4.6f,5.2f,.5f,2,1.2f,5);
Box("Study east desk .7 x 1.8",furniture,8.65f,4.1f,4.4f,.7f,1,1.8f,5);
Box("Study rear bookcase 1.9 x .35",furniture,7.25f,4.6f,6.025f,1.9f,2,.35f,5);
Box("Living bench 2 x .8",furniture,1.1f,4.05f,.6f,2,.9f,.8f,4);
Box("Living low table 1.2 x .65",furniture,2.9f,3.9f,1.2f,1.2f,.6f,.65f,5);
// Reserved porch: door sweep is left of the straight approach lane.
Slab("Porch flush approach",1.5f,6,-2.8f,0,.2f,.2f,1);
Box("Door swing pocket - visual datum only",markers,2.7f,.207f,-1.05f,2.1f,.012f,2.1f,4,false);
Slab("Garden step",6.5f,8.9f,9,10,.2f,.2f,1);
void Datum(string n,float x,float y,float z){var g=new GameObject(n);g.transform.SetParent(markers,false);g.transform.position=new Vector3(x,y,z);}
Datum("Shop 5.4 x 4.4",2.7f,.2f,2.2f);Datum("Treatment 3.6 x 4.4",3.6f,.2f,6.8f);Datum("Kitchen 3.4 x 4.2",7.3f,.2f,4.1f);Datum("Storage 3.4 x 2.4",7.3f,.2f,7.6f);Datum("Bedroom 3.6 x 4.4",3.6f,3.6f,6.8f);Datum("Study 3.4 x 4.2",7.3f,3.6f,4.1f);Datum("Open landing reserve 2.4 x 2.4",.2f,3.6f,3.4f);
// Simple closed gabled volumes keep the eventual architectural hierarchy legible.
void Gable(string n,float x0,float x1,float z0,float z1,float eave,float ridge,bool rotate=false){var g=new GameObject(n);g.transform.SetParent(roof,false);var mesh=new Mesh();float mid=(x0+x1)/2;var v=new[]{new Vector3(x0,eave,z0),new Vector3(x1,eave,z0),new Vector3(mid,ridge,z0),new Vector3(x0,eave,z1),new Vector3(x1,eave,z1),new Vector3(mid,ridge,z1)};mesh.vertices=v;mesh.triangles=new[]{0,2,1,3,4,5,0,3,5,0,5,2,2,5,4,2,4,1,0,1,4,0,4,3};var faceVertices=mesh.triangles.Select(i=>mesh.vertices[i]).ToArray();mesh.Clear();mesh.vertices=faceVertices;mesh.triangles=Enumerable.Range(0,faceVertices.Length).ToArray();mesh.RecalculateNormals();mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,dir+"/"+n+".asset");g.AddComponent<MeshFilter>().sharedMesh=mesh;g.AddComponent<MeshRenderer>().sharedMaterial=mats[1];if(rotate){g.transform.position=new Vector3(-.4f,0,6.9f);g.transform.rotation=Quaternion.Euler(0,90,0);}}
Gable("Hero front gable",-.5f,5.9f,-.5f,5.0f,6.85f,11.2f);
// Cross-roof uses local coordinates, with ridge along X.
Gable("Lower rear crossroof",-2.65f,2.65f,-4.8f,2.2f,6.85f,9.65f,true);
Gable("Recessed study wing",5.3f,9.5f,1.5f,6.65f,6.85f,8.8f);
Gable("Low storage extension",5.3f,9.5f,6.3f,9.4f,3.45f,5.1f);
Box("Deep porch canopy - silhouette guide",roof,3.7f,3.22f,-1.35f,3.2f,.2f,2.7f,1,false).transform.rotation=Quaternion.Euler(-12,0,0);
var traversal=UnityEngine.Object.Instantiate(source);traversal.name="07 Existing unchanged third-person traversal";UnityEngine.SceneManagement.SceneManager.MoveGameObjectToScene(traversal,scene);var cc=traversal.GetComponentInChildren<CharacterController>();cc.transform.position=new Vector3(4,.24f,-3.8f);cc.transform.rotation=Quaternion.identity;var spawn=traversal.GetComponentsInChildren<Transform>().First(t=>t.name=="Front approach spawn");spawn.position=cc.transform.position;
var hinge=new GameObject("08 Front door - E toggle outward into reserved pocket");hinge.transform.position=new Vector3(2.72f,.2f,-.26f);var door=hinge.AddComponent<BlightBloom.Prototypes.BlockoutDoor>();door.player=cc.transform;door.interactionActions=AssetDatabase.LoadAssetAtPath<UnityEngine.InputSystem.InputActionAsset>("Assets/InputSystem_Actions.inputactions");
var leaf=Box("Door leaf - 1.96m",hinge.transform,3.7f,1.55f,-.1f,1.96f,2.7f,.10f,2);leaf.transform.localPosition=new Vector3(.98f,1.35f,0);
var sun=new GameObject("Neutral daylight");sun.transform.rotation=Quaternion.Euler(50,-30,0);var light=sun.AddComponent<Light>();light.type=LightType.Directional;light.intensity=1.4f;light.shadows=LightShadows.Soft;
RenderSettings.ambientMode=UnityEngine.Rendering.AmbientMode.Flat;RenderSettings.ambientLight=new Color(.65f,.65f,.65f);RenderSettings.skybox=null;
var fills=Group("09 Neutral interior fill - no shadows");foreach(var p in new[]{new Vector3(2.7f,2.8f,2.2f),new Vector3(3.6f,2.8f,6.8f),new Vector3(7.3f,2.8f,4.1f),new Vector3(7.5f,2.8f,7.6f),new Vector3(-.4f,5.8f,6.8f),new Vector3(2.7f,6.2f,2.2f),new Vector3(3.6f,6.2f,6.8f),new Vector3(7.3f,6.2f,4.1f)}){var g=new GameObject("Room fill");g.transform.SetParent(fills,false);g.transform.position=p;var l=g.AddComponent<Light>();l.type=LightType.Point;l.range=6;l.intensity=1.3f;l.shadows=LightShadows.None;}
AssetDatabase.SaveAssets();UnityEditor.SceneManagement.EditorSceneManager.SaveScene(scene,path);UnityEditor.SceneManagement.EditorSceneManager.CloseScene(old,true);Selection.activeGameObject=cc.gameObject;return new{path,roots=scene.rootCount,cc.height,cc.radius,cc.stepOffset};
