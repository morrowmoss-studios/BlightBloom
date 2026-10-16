using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;

// Concept-directed facade authoring. Existing architecture/physics are retained as proxies.
public static class ApothecaryReferenceFacadePass
{
 const string Dir="Assets/BlightBloom/Locations/ReferenceFacade";
 static Transform root;
 static Mesh cube;
 static Transform[] old;
 static Dictionary<string,Material> mat;
 static System.Random rng;
 public static string Apply()
 {
  var scene=SceneManager.GetActiveScene();
  if(scene.path!="Assets/Scenes/UncleRobertsApothecary.unity"||EditorApplication.isPlayingOrWillChangePlaymode)throw new InvalidOperationException("Apothecary Edit mode required");
  if(scene.GetRootGameObjects().Any(g=>g.name=="10 Concept-directed facade"))throw new InvalidOperationException("Reference pass already applied; edit existing assets.");
  old=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).ToArray();
  string physics=PhysicsState();
  cube=old.Select(t=>t.GetComponent<MeshFilter>()).First(m=>m!=null&&m.sharedMesh.name=="Cube").sharedMesh;
  AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
  foreach(string f in new[]{"Materials","Meshes"})if(!AssetDatabase.IsValidFolder(Dir+"/"+f))AssetDatabase.CreateFolder(Dir,f);
  mat=new Dictionary<string,Material>();rng=new System.Random(10413);
  string atlasPath=Dir+"/Textures/IllustratedSurfaceAtlas.png";
  var importer=(TextureImporter)AssetImporter.GetAtPath(atlasPath);importer.maxTextureSize=2048;importer.textureCompression=TextureImporterCompression.Uncompressed;importer.mipmapEnabled=true;importer.wrapMode=TextureWrapMode.Clamp;importer.SaveAndReimport();
  var atlas=AssetDatabase.LoadAssetAtPath<Texture2D>(atlasPath);
  Atlas("Painted cream plaster",atlas,new Vector2(0,.5f),Color.white);
  Atlas("Painted walnut",atlas,new Vector2(.5f,.5f),new Color(.9f,.92f,.92f));
  Atlas("Painted limestone",atlas,Vector2.zero,new Color(1.03f,1.01f,.95f));
  Atlas("Painted slate",atlas,new Vector2(.5f,0),Color.white);
  Atlas("Cut arch stone",atlas,new Vector2(0,.5f),new Color(.88f,.85f,.76f));
  Flat("Sage shutter",new Color(.31f,.43f,.36f));Flat("Iron",new Color(.16f,.15f,.13f));
  Flat("Leaf shade",new Color(.23f,.34f,.19f));Flat("Leaf mid",new Color(.38f,.45f,.25f));Flat("Leaf light",new Color(.52f,.55f,.29f));
  Flat("Cream bloom",new Color(.92f,.84f,.64f));Flat("Bloom centre",new Color(.73f,.52f,.20f));Flat("Sign parchment",new Color(.75f,.61f,.38f));
  Flat("Quiet amber glazing",new Color(.92f,.68f,.30f,.16f));var glass=mat["Quiet amber glazing"];glass.SetFloat("_Surface",1);glass.SetFloat("_SrcBlend",(float)BlendMode.SrcAlpha);glass.SetFloat("_DstBlend",(float)BlendMode.OneMinusSrcAlpha);glass.SetFloat("_ZWrite",0);glass.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");glass.renderQueue=3000;
  root=Group("10 Concept-directed facade",null);
  Undo.SetCurrentGroupName("Reference-directed apothecary facade");
  // Only renderer materials/visibility change on existing geometry; no collider or transform edits.
  foreach(var t in old)
  {
   var r=t.GetComponent<Renderer>();if(r==null)continue;string path=Path(t),n=t.name;
   if(path.Contains("Window apertures and plaster panels")&&(n=="Wall pier"||n=="Window base"||n=="Window header"))Assign(r,"Painted cream plaster");
   if(path.Contains("Timber structure and stone plinth"))Assign(r,n.Contains("Stone")?"Painted limestone":"Painted walnut");
   if(n=="Front window sill"||n=="Rear window sill")Assign(r,"Painted cream plaster");
   if(n=="Stone chimney stack"||n=="Chimney cap"||n=="Chimney masonry band")Assign(r,"Painted limestone");
   if(n=="Roof slope"||n=="Slate course"||n=="Ridge cap"||n=="Gable verge"||n=="Gable king post"||n=="Front painted gable"||n=="Rear painted gable"||n.Contains("painted shingles")||n=="Steep entrance canopy"||n=="Porch carved verge"||n.StartsWith("Ridge finial")||n=="Shop sign block"||n=="Mortar sign backing"||n=="Robert's apothecary lettering"||n=="Mortar bowl emblem"||n=="Pestle emblem")Hide(r);
   if(path.Contains("09 Storybook")&&(n=="Painted ivy leaves"||n=="Ivy stem"))Hide(r);
   if(path.Contains("09 Storybook")&&t.position.z<-6.05f&&(n.StartsWith("Pointed Gothic hood")||n=="Window cross rail"||n=="Open sage shutter"||n=="Shutter brace"||n=="Upper central window hood"))Hide(r);
  }
  Roof();Windows();Porch();Sign();Botanical();Refine();CentralWindow();
  if(PhysicsState()!=physics)throw new InvalidOperationException("Collision state changed; scene not saved");
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(scene);EditorSceneManager.SaveScene(scene);
  return "Concept facade saved. Existing collision/transform signature unchanged. Roof and window silhouettes are render-only over preserved gameplay architecture.";
 }
 static string Path(Transform t){return t.parent==null?t.name:Path(t.parent)+"/"+t.name;}
 static string PhysicsState(){return string.Join("|",SceneManager.GetActiveScene().GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Collider>(true)).OrderBy(c=>Path(c.transform)+c.GetType().Name).Select(c=>EditorJsonUtility.ToJson(c)+c.transform.position+c.transform.rotation+c.transform.lossyScale+c.gameObject.activeInHierarchy));}
 static void Assign(Renderer r,string name){Undo.RecordObject(r,"Painted facade surface");r.sharedMaterial=mat[name];}
 static void Hide(Renderer r){Undo.RecordObject(r,"Superseded facade renderer");r.enabled=false;}
 static void Flat(string name,Color color){var m=new Material(Shader.Find("Universal Render Pipeline/Lit"));m.name=name;m.SetColor("_BaseColor",color);m.SetFloat("_Smoothness",0);m.SetFloat("_Metallic",0);m.SetFloat("_SpecularHighlights",0);m.SetFloat("_EnvironmentReflections",0);m.EnableKeyword("_SPECULARHIGHLIGHTS_OFF");m.EnableKeyword("_ENVIRONMENTREFLECTIONS_OFF");m.SetFloat("_Cull",0);AssetDatabase.CreateAsset(m,Dir+"/Materials/"+name+".mat");mat[name]=m;}
 static void Atlas(string name,Texture2D atlas,Vector2 offset,Color tint){Flat(name,tint);mat[name].SetTexture("_BaseMap",atlas);mat[name].SetTextureScale("_BaseMap",new Vector2(.488f,.488f));mat[name].SetTextureOffset("_BaseMap",offset+Vector2.one*.006f);}
 static Transform Group(string name,Transform parent){var g=new GameObject(name);Undo.RegisterCreatedObjectUndo(g,"Reference facade art");g.transform.SetParent(parent,false);return g.transform;}
 static Transform Box(Transform p,string name,Vector3 pos,Vector3 size,string material){var t=Group(name,p);t.position=pos;t.localScale=size;t.gameObject.AddComponent<MeshFilter>().sharedMesh=cube;t.gameObject.AddComponent<MeshRenderer>().sharedMaterial=mat[material];return t;}
 static void Beam(Transform p,string name,Vector3 a,Vector3 b,float width,string material){var t=Box(p,name,(a+b)/2,new Vector3(width,(b-a).magnitude,width),material);t.rotation=Quaternion.FromToRotation(Vector3.up,b-a);}
 static Transform Mesh(Transform p,string name,List<Vector3> vertices,List<int> indices,List<Vector2> uv,string material,Vector3? normal=null)
 {
  var mesh=new Mesh();mesh.name=name;mesh.SetVertices(vertices);mesh.SetTriangles(indices,0);mesh.SetUVs(0,uv);mesh.RecalculateNormals();if(normal.HasValue)mesh.normals=Enumerable.Repeat(normal.Value,vertices.Count).ToArray();mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,Dir+"/Meshes/"+name+".asset");var t=Group(name,p);t.gameObject.AddComponent<MeshFilter>().sharedMesh=mesh;var r=t.gameObject.AddComponent<MeshRenderer>();r.sharedMaterial=mat[material];return t;
 }
 static Vector3 RoofPoint(float x,float z)
 {
  float span=x< -3.4f?5.3f:12.1f,u=Mathf.Abs(x+3.4f)/span;
  return new Vector3(x,13.4f-6.2f*u-.4f*Mathf.Sin(u*Mathf.PI)+.12f*Mathf.Sin(u*Mathf.PI*2),z);
 }
 static void Roof()
 {
  var group=Group("Steeper off-centre curved roof silhouette",root);
  for(int side=-1;side<=1;side+=2)
  {
   float span=side<0?5.3f:12.1f;int rows=side<0?14:20;
   var verts=new List<Vector3>();var uv=new List<Vector2>();var triangles=new List<int>();
   for(int row=0;row<rows;row++)for(int col=0;col<24;col++)
   {
    float u0=row/(float)rows,u1=Mathf.Min(1.01f,(row+1.09f)/rows);float z0=-6.72f+col*.65f+(row%2)*.19f,z1=Mathf.Min(8.72f,z0+.64f);
    if(z0>8.65f)continue;
    int a=verts.Count;float lift=.09f+(rows-row)*.006f;
    foreach(var v in new[]{RoofPoint(-3.4f+side*span*u0,z0),RoofPoint(-3.4f+side*span*u1,z0+.025f),RoofPoint(-3.4f+side*span*u1,z1-.02f),RoofPoint(-3.4f+side*span*u0,z1)})verts.Add(v+Vector3.up*lift);
    float tu=(float)rng.NextDouble()*.68f,tv=(float)rng.NextDouble()*.68f;uv.AddRange(new[]{new Vector2(tu,tv),new Vector2(tu,tv+.3f),new Vector2(tu+.3f,tv+.3f),new Vector2(tu+.3f,tv)});
    if(side>0)triangles.AddRange(new[]{a,a+2,a+1,a,a+3,a+2});else triangles.AddRange(new[]{a,a+1,a+2,a,a+2,a+3});
   }
   var t=Mesh(group,side<0?"Curved steep west roof tiles":"Curved sweeping east roof tiles",verts,triangles,uv,"Painted slate");t.GetComponent<Renderer>().receiveShadows=false;
  }
  foreach(float z in new[]{-6.19f,8.19f})
  {
   Mesh(group,z<0?"Tall front plaster gable":"Tall rear plaster gable",new List<Vector3>{new Vector3(-8.7f,7.12f,z),new Vector3(8.7f,7.12f,z),new Vector3(-3.4f,13.4f,z)},new List<int>{0,2,1},new List<Vector2>{new Vector2(0,0),new Vector2(1,0),new Vector2(.3f,1)},"Painted cream plaster",z<0?Vector3.back:Vector3.forward);
   for(int side=-1;side<=1;side+=2)
   {
    float span=side<0?5.3f:12.1f;
    for(int i=0;i<10;i++)Beam(group,"Curved gable bargeboard",RoofPoint(-3.4f+side*span*i/10,z+(z<0?-.16f:.16f)),RoofPoint(-3.4f+side*span*(i+1)/10,z+(z<0?-.16f:.16f)),.20f,"Painted walnut");
   }
  }
  Beam(group,"Off-centre ridge cap",new Vector3(-3.4f,13.58f,-6.9f),new Vector3(-3.4f,13.58f,8.9f),.22f,"Painted walnut");
  Beam(group,"Attic king post",new Vector3(-3.4f,7.22f,-6.37f),new Vector3(-3.4f,13.2f,-6.37f),.2f,"Painted walnut");
  Beam(group,"Attic collar beam",new Vector3(-6.7f,9.05f,-6.37f),new Vector3(4.8f,9.05f,-6.37f),.18f,"Painted walnut");
  Beam(group,"Gable left brace",new Vector3(-6.6f,7.25f,-6.37f),new Vector3(-3.4f,10.6f,-6.37f),.15f,"Painted walnut");
  Beam(group,"Gable right brace",new Vector3(-.2f,7.25f,-6.37f),new Vector3(-3.4f,10.6f,-6.37f),.15f,"Painted walnut");
  Box(group,"Visual chimney extension",new Vector3(-8.55f,12.65f,5.15f),new Vector3(1.1f,1.3f,1.3f),"Painted limestone");
  Box(group,"Chimney crown",new Vector3(-8.55f,13.4f,5.15f),new Vector3(1.5f,.25f,1.7f),"Cut arch stone");
  // Render-only gabled attic feature, no new floor or accessible room.
  var dormer=Group("Small east attic dormer proxy",group);float x=4.8f;
  Mesh(dormer,"Dormer plaster triangle",new List<Vector3>{new Vector3(x-1,9,-6.55f),new Vector3(x+1,9,-6.55f),new Vector3(x,11,-6.55f)},new List<int>{0,2,1},new List<Vector2>{Vector2.zero,Vector2.right,new Vector2(.5f,1)},"Painted cream plaster",Vector3.back);
  foreach(int side in new[]{-1,1})
  {
   Mesh(dormer,"Dormer roof "+side,new List<Vector3>{new Vector3(x,11.1f,-6.8f),new Vector3(x+side*1.2f,9,-6.8f),new Vector3(x+side*1.2f,9,-4.9f),new Vector3(x,11.1f,-4.9f)},new List<int>{0,2,1,0,3,2},new List<Vector2>{Vector2.zero,Vector2.up,Vector2.one,Vector2.right},"Painted slate",new Vector3(side*.87f,.5f,0));
   Beam(dormer,"Dormer verge",new Vector3(x,11.14f,-6.88f),new Vector3(x+side*1.2f,9,-6.88f),.14f,"Painted walnut");
  }
 }
 static void Arc(Transform p,string name,Vector3 center,float inner,float outer,string material,bool joints)
 {
  var v=new List<Vector3>();var uv=new List<Vector2>();var tris=new List<int>();int segments=16;
  for(int i=0;i<segments;i++)
  {
   float a=i*Mathf.PI/segments+(joints?.01f:0),b=(i+1)*Mathf.PI/segments-(joints?.01f:0);int start=v.Count;
   foreach(var pt in new[]{new Vector2(Mathf.Cos(a)*inner,Mathf.Sin(a)*inner),new Vector2(Mathf.Cos(a)*outer,Mathf.Sin(a)*outer),new Vector2(Mathf.Cos(b)*outer,Mathf.Sin(b)*outer),new Vector2(Mathf.Cos(b)*inner,Mathf.Sin(b)*inner)}){v.Add(center+new Vector3(pt.x,pt.y,0));uv.Add(new Vector2(pt.x/(outer*2)+.5f,pt.y/outer));}
   tris.AddRange(new[]{start,start+2,start+1,start,start+3,start+2});
  }
  Mesh(p,name,v,tris,uv,material,Vector3.back).GetComponent<Renderer>().shadowCastingMode=ShadowCastingMode.Off;
 }
 static void Windows()
 {
  var group=Group("Arched front windows with real retained apertures",root);int index=0;
  foreach(var w in old.Where(t=>t.name=="Open framed window"))
  {
   var jamb=w.Cast<Transform>().Where(t=>t.name=="Window jamb").ToArray();if(jamb.Length!=2)continue;Vector3 c=(jamb[0].position+jamb[1].position)/2;
   if(c.z> -5.9f)continue;
   foreach(var r in w.GetComponentsInChildren<Renderer>())Hide(r);
   float floor=c.y-1.75f;var g=Group("Arched facade window "+(++index),group);
   Arc(g,"Window limestone arch "+index,new Vector3(c.x,floor+1.6f,-6.29f),.81f,1,"Cut arch stone",true);
   Arc(g,"Inner wooden arch "+index,new Vector3(c.x,floor+1.6f,-6.34f),.74f,.83f,"Painted walnut",false);
   foreach(int side in new[]{-1,1})
   {
    Box(g,"Window stone upright",new Vector3(c.x+side*.9f,floor+1.35f,-6.25f),new Vector3(.2f,.5f,.19f),"Cut arch stone");
    Box(g,"Window timber upright",new Vector3(c.x+side*.78f,floor+1.35f,-6.34f),new Vector3(.09f,.5f,.13f),"Painted walnut");
    var shutter=Box(g,"Curved-top sage shutter proxy",new Vector3(c.x+side*1.16f,floor+1.67f,-6.33f),new Vector3(.42f,1.23f,.12f),"Sage shutter");shutter.rotation=Quaternion.Euler(0,side*12,0);
    foreach(float y in new[]{floor+1.25f,floor+1.95f})Box(g,"Shutter hinge",new Vector3(c.x+side*1.16f,y,-6.42f),new Vector3(.43f,.055f,.045f),"Iron");
   }
   Beam(g,"Window centre mullion",new Vector3(c.x,floor+1.1f,-6.35f),new Vector3(c.x,floor+2.36f,-6.35f),.065f,"Painted walnut");
   Beam(g,"Window transom",new Vector3(c.x-.76f,floor+1.6f,-6.35f),new Vector3(c.x+.76f,floor+1.6f,-6.35f),.055f,"Painted walnut");
   foreach(int side in new[]{-1,1})Beam(g,"Gothic fan tracery",new Vector3(c.x,floor+1.61f,-6.35f),new Vector3(c.x+side*.53f,floor+2.16f,-6.35f),.045f,"Painted walnut");
   // Arched pane and opaque corner masks sit entirely in the existing rectangular opening.
   var pane=new List<Vector3>{new Vector3(c.x-.75f,floor+1.1f,-6.12f),new Vector3(c.x+.75f,floor+1.1f,-6.12f)};
   for(int i=0;i<=16;i++){float angle=i*Mathf.PI/16;pane.Add(new Vector3(c.x+Mathf.Cos(angle)*.75f,floor+1.6f+Mathf.Sin(angle)*.75f,-6.12f));}
   var triangles=new List<int>();for(int i=1;i<pane.Count-1;i++)triangles.AddRange(new[]{0,i+1,i});
   Mesh(g,"Quiet amber arched pane "+index,pane,triangles,pane.Select(p=>new Vector2((p.x-c.x)/1.6f+.5f,(p.y-floor-1.1f)/1.3f)).ToList(),"Quiet amber glazing",Vector3.back);
   var masks=new List<Vector3>();var mu=new List<Vector2>();var mt=new List<int>();
   for(int i=0;i<20;i++)
   {
    float a=-.8f+i*.08f,b=a+.08f,ya=1.6f+Mathf.Sqrt(Mathf.Max(0,.64f-a*a)),yb=1.6f+Mathf.Sqrt(Mathf.Max(0,.64f-b*b));int st=masks.Count;
    masks.AddRange(new[]{new Vector3(c.x+a,floor+ya,-6.15f),new Vector3(c.x+b,floor+yb,-6.15f),new Vector3(c.x+b,floor+2.4f,-6.15f),new Vector3(c.x+a,floor+2.4f,-6.15f)});mu.AddRange(new[]{Vector2.zero,Vector2.right,Vector2.one,Vector2.up});mt.AddRange(new[]{st,st+2,st+1,st,st+3,st+2});
   }
   Mesh(g,"Plaster arched aperture infill "+index,masks,mt,mu,"Painted cream plaster",Vector3.back);
  }
  // Central upper opening remains timber-framed, preserving the mixed window vocabulary.
  foreach(int side in new[]{-1,1})Beam(group,"Central upper window post",new Vector3(side*1.12f,4.7f,-6.27f),new Vector3(side*1.12f,6.4f,-6.27f),.12f,"Painted walnut");
  Beam(group,"Central upper transom",new Vector3(-1.12f,5.5f,-6.27f),new Vector3(1.12f,5.5f,-6.27f),.08f,"Painted walnut");
 }
 static void Porch()
 {
  var g=Group("Broad shop canopy and stone entrance",root);
  Mesh(g,"Lean-to painted shop canopy",new List<Vector3>{new Vector3(-7.4f,3.95f,-6.2f),new Vector3(1.6f,3.95f,-6.2f),new Vector3(1.7f,3.18f,-7.5f),new Vector3(-7.5f,3.18f,-7.5f)},new List<int>{0,2,1,0,3,2},new List<Vector2>{Vector2.zero,new Vector2(1,0),Vector2.one,Vector2.up},"Painted slate",new Vector3(0,.86f,-.5f));
  Beam(g,"Porch eave fascia",new Vector3(-7.55f,3.16f,-7.52f),new Vector3(1.75f,3.16f,-7.52f),.16f,"Painted walnut");
  foreach(float x in new[]{-7.1f,-4.8f,-2.4f,1.35f})
  {
   Beam(g,"Porch rafter",new Vector3(x,3.9f,-6.18f),new Vector3(x,3.13f,-7.58f),.11f,"Painted walnut");
   Beam(g,"Porch carved support",new Vector3(x,2.7f,-6.25f),new Vector3(x,3.12f,-7.35f),.10f,"Painted walnut");
  }
  Arc(g,"Segmented entrance arch",new Vector3(0,1.6f,-6.46f),1.22f,1.48f,"Cut arch stone",true);
  foreach(int side in new[]{-1,1})for(int i=0;i<4;i++)Box(g,"Entrance cut-stone jamb",new Vector3(side*1.35f,.2f+i*.4f,-6.37f),new Vector3(.27f,.37f,.22f),"Cut arch stone");
  // Nothing is placed across the original 2.4m-wide entry or its floor.
 }
 static void Sign()
 {
  var g=Group("Hanging mortar-and-botanical apothecary sign",root);
  Beam(g,"Forged sign bracket",new Vector3(-7,5.2f,-6.25f),new Vector3(-7,5.2f,-7.7f),.07f,"Iron");
  Beam(g,"Sign hanging crossbar",new Vector3(-7.95f,5.2f,-7.7f),new Vector3(-5.85f,5.2f,-7.7f),.065f,"Iron");
  foreach(float x in new[]{-7.75f,-6.05f})Beam(g,"Sign hanger",new Vector3(x,5.2f,-7.7f),new Vector3(x,4.87f,-7.7f),.035f,"Iron");
  Box(g,"Carved sign wooden rim",new Vector3(-6.9f,4.2f,-7.68f),new Vector3(2.3f,1.45f,.14f),"Painted walnut");
  Box(g,"Painted sign field",new Vector3(-6.9f,4.2f,-7.77f),new Vector3(2.1f,1.25f,.035f),"Sign parchment");
  Text(g,"Uncle Robert's",new Vector3(-6.9f,4.58f,-7.81f),.053f);Text(g,"Apothecary",new Vector3(-6.9f,3.78f,-7.81f),.06f);
  for(int i=0;i<7;i++)Box(g,"Painted mortar emblem",new Vector3(-6.9f,4.28f-i*.055f,-7.82f),new Vector3(.7f-i*.07f,.055f,.02f),"Cut arch stone");
  Beam(g,"Pestle emblem",new Vector3(-6.83f,4.31f,-7.84f),new Vector3(-6.63f,4.61f,-7.84f),.08f,"Painted walnut");
  // Scrolls are small segmented curves, not an unrelated hero asset.
  foreach(int side in new[]{-1,1})for(int i=0;i<20;i++)
  {
   float a=i*.20f,b=(i+1)*.20f;Vector3 Point(float t){float r=.28f*(1-t/5);return new Vector3(-6.9f+side*(.8f+Mathf.Cos(t)*r),5.2f+Mathf.Sin(t)*r,-7.7f);}
   Beam(g,"Forged bracket scroll",Point(a),Point(b),.035f,"Iron");
  }
 }
 static void Text(Transform p,string value,Vector3 position,float size){var t=Group(value,p);t.position=position;var text=t.gameObject.AddComponent<TextMesh>();text.text=value;text.font=Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");text.fontSize=64;text.characterSize=size;text.anchor=TextAnchor.MiddleCenter;text.color=new Color(.17f,.16f,.12f);t.GetComponent<MeshRenderer>().sharedMaterial=text.font.material;}
 public static string CentralWindow()
 {
  var scene=SceneManager.GetActiveScene();root=scene.GetRootGameObjects().First(g=>g.name=="10 Concept-directed facade").transform;
  if(root.Cast<Transform>().Any(t=>t.name=="Central traditional timber window"))return "Central window already detailed";
  cube=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<MeshFilter>(true)).First(m=>m.sharedMesh!=null&&m.sharedMesh.name=="Cube").sharedMesh;
  if(mat==null)mat=new Dictionary<string,Material>();foreach(string n in new[]{"Painted walnut","Quiet amber glazing","Sage shutter","Iron"})mat[n]=AssetDatabase.LoadAssetAtPath<Material>(Dir+"/Materials/"+n+".mat");
  var group=Group("Central traditional timber window",root);
  Beam(group,"Central window lintel",new Vector3(-1.14f,6.4f,-6.3f),new Vector3(1.14f,6.4f,-6.3f),.11f,"Painted walnut");
  foreach(float x in new[]{-.38f,.38f})Beam(group,"Central window mullion",new Vector3(x,4.72f,-6.31f),new Vector3(x,6.35f,-6.31f),.065f,"Painted walnut");
  Mesh(group,"Central quiet glass",new List<Vector3>{new Vector3(-1.1f,4.73f,-6.12f),new Vector3(1.1f,4.73f,-6.12f),new Vector3(1.1f,6.34f,-6.12f),new Vector3(-1.1f,6.34f,-6.12f)},new List<int>{0,2,1,0,3,2},new List<Vector2>{Vector2.zero,Vector2.right,Vector2.one,Vector2.up},"Quiet amber glazing",Vector3.back);
  foreach(int side in new[]{-1,1})
  {
   Box(group,"Central sage shutter",new Vector3(side*1.39f,5.55f,-6.31f),new Vector3(.34f,1.6f,.11f),"Sage shutter");
   foreach(float y in new[]{5.05f,6.05f})Box(group,"Central shutter hinge",new Vector3(side*1.39f,y,-6.39f),new Vector3(.35f,.055f,.035f),"Iron");
  }
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(scene);EditorSceneManager.SaveScene(scene);return "Central upper opening detailed as a traditional timber window, preserving the aperture.";
 }
 public static string Refine()
 {
  var scene=SceneManager.GetActiveScene();root=scene.GetRootGameObjects().First(g=>g.name=="10 Concept-directed facade").transform;
  if(root.Cast<Transform>().Any(t=>t.name=="Refined facade accents"))return "Refinement already present";
  cube=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<MeshFilter>(true)).First(m=>m.sharedMesh!=null&&m.sharedMesh.name=="Cube").sharedMesh;
  if(mat==null)mat=new Dictionary<string,Material>();foreach(string name in new[]{"Painted cream plaster","Painted walnut","Painted limestone","Painted slate","Cut arch stone","Iron","Leaf mid","Leaf shade","Leaf light","Cream bloom","Sign parchment"})mat[name]=AssetDatabase.LoadAssetAtPath<Material>(Dir+"/Materials/"+name+".mat");
  var g=Group("Refined facade accents",root);var nodes=root.GetComponentsInChildren<Transform>(true);
  mat["Painted slate"].SetColor("_BaseColor",new Color(.78f,.87f,.90f));EditorUtility.SetDirty(mat["Painted slate"]);
  // Proper curved shutter silhouettes, retaining each authored transform and hinge.
  var outline=new List<Vector3>{new Vector3(-.5f,-.5f,-.5f),new Vector3(.5f,-.5f,-.5f)};
  for(int i=0;i<=12;i++){float a=i*Mathf.PI/12;outline.Add(new Vector3(Mathf.Cos(a)*.5f,.2f+Mathf.Sin(a)*.3f,-.5f));}
  var tri=new List<int>();for(int i=1;i<outline.Count-1;i++)tri.AddRange(new[]{0,i+1,i});
  var shutter=Mesh(g,"Shared round-top shutter mesh",outline,tri,outline.Select(v=>new Vector2(v.x+.5f,v.y+.5f)).ToList(),"Painted walnut",Vector3.back);shutter.gameObject.SetActive(false);
  foreach(var t in nodes.Where(t=>t.name=="Curved-top sage shutter proxy"))t.GetComponent<MeshFilter>().sharedMesh=shutter.GetComponent<MeshFilter>().sharedMesh;
  // A tile silhouette replaces the large stretched canopy plane; no new collision.
  Hide(nodes.First(t=>t.name=="Lean-to painted shop canopy").GetComponent<Renderer>());
  var vertices=new List<Vector3>();var uv=new List<Vector2>();var triangles=new List<int>();
  for(int row=0;row<3;row++)for(int col=0;col<16;col++)
  {
   float x=-7.4f+col*.565f,z=-6.2f-row*.44f;float y=3.95f-row*.257f;int st=vertices.Count;
   vertices.AddRange(new[]{new Vector3(x,y+.05f,z),new Vector3(x+.55f,y+.05f,z),new Vector3(x+.54f,y-.247f,z-.5f),new Vector3(x+.01f,y-.247f,z-.5f)});
   uv.AddRange(new[]{new Vector2(.1f,.1f),new Vector2(.35f,.1f),new Vector2(.35f,.4f),new Vector2(.1f,.4f)});triangles.AddRange(new[]{st,st+2,st+1,st,st+3,st+2});
  }
  Mesh(g,"Painted canopy tile courses",vertices,triangles,uv,"Painted slate",new Vector3(0,.86f,-.5f)).GetComponent<Renderer>().receiveShadows=false;
  // Chimney is extended only above the retained collision stack; no hearth/layout changes.
  Box(g,"Taller visual chimney shaft",new Vector3(-8.55f,14.3f,5.15f),new Vector3(1.1f,2.0f,1.3f),"Painted limestone");
  Box(g,"Chimney cream coping",new Vector3(-8.55f,15.4f,5.15f),new Vector3(1.5f,.25f,1.7f),"Cut arch stone");
  foreach(float x in new[]{-8.85f,-8.25f})Box(g,"Terracotta flue pot proxy",new Vector3(x,15.8f,5.15f),new Vector3(.28f,.65f,.3f),"Painted walnut");
  // Louvred attic vents explain the higher roof without inventing usable rooms.
  foreach(var point in new[]{new Vector3(-3.4f,10.0f,-6.45f),new Vector3(4.8f,9.55f,-6.7f)})
  {
   float radius=point.x<0?.42f:.27f;
   Arc(g,"Arched attic vent surround "+point.x,point,radius,radius+.1f,"Painted walnut",false);
   Box(g,"Dark attic vent backing",point+new Vector3(0,-.12f,.03f),new Vector3(radius*2,.65f,.05f),"Iron");
   for(int i=0;i<4;i++)Box(g,"Attic louvre",point+new Vector3(0,-.4f+i*.13f,-.025f),new Vector3(radius*1.9f,.055f,.06f),"Painted walnut");
  }
  // Shade variation is grouped by leaf, not random noisy per-pixel colour.
  var ivy=nodes.First(t=>t.name=="Lobed ivy leaf clusters");var ivyMesh=ivy.GetComponent<MeshFilter>().sharedMesh;var allTriangles=ivyMesh.triangles;var parts=new[]{new List<int>(),new List<int>(),new List<int>()};
  for(int leaf=0;leaf<70;leaf++)parts[leaf%3].AddRange(allTriangles.Skip(leaf*24).Take(24));
  ivyMesh.subMeshCount=3;for(int i=0;i<3;i++)ivyMesh.SetTriangles(parts[i],i);ivy.GetComponent<MeshRenderer>().sharedMaterials=new[]{mat["Leaf mid"],mat["Leaf shade"],mat["Leaf light"]};EditorUtility.SetDirty(ivyMesh);
  // The sign uses the painted plaster surface as a parchment-like field.
  nodes.First(t=>t.name=="Painted sign field").GetComponent<Renderer>().sharedMaterial=mat["Painted cream plaster"];
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(scene);EditorSceneManager.SaveScene(scene);return "Curved shutters, tiled canopy, visible chimney and louvred attic vents refined.";
 }
 static void Botanical()
 {
  var g=Group("Grouped climbing leaves and cream blossoms",root);var v=new List<Vector3>();var uv=new List<Vector2>();var triangles=new List<int>();
  for(int i=0;i<70;i++)
  {
   float y=.25f+(float)rng.NextDouble()*5.5f,x=2.02f+Mathf.Sin(y*1.4f)*.22f+((float)rng.NextDouble()-.5f)*.55f,size=.12f+(float)rng.NextDouble()*.12f;Vector3 p=new Vector3(x,y,-6.40f-(float)rng.NextDouble()*.06f);int st=v.Count;
   Vector2[] outline={new Vector2(0,-.7f),new Vector2(-.5f,-.15f),new Vector2(-.6f,.25f),new Vector2(-.25f,.55f),new Vector2(0,.35f),new Vector2(.25f,.55f),new Vector2(.6f,.25f),new Vector2(.5f,-.15f)};
   v.Add(p);uv.Add(new Vector2(.5f,.5f));float angle=(float)rng.NextDouble()*2;
   foreach(var q in outline){v.Add(p+new Vector3((q.x*Mathf.Cos(angle)-q.y*Mathf.Sin(angle))*size,(q.x*Mathf.Sin(angle)+q.y*Mathf.Cos(angle))*size,0));uv.Add(q+Vector2.one*.5f);}
   for(int k=0;k<8;k++)triangles.AddRange(new[]{st,st+1+(k+1)%8,st+1+k});
  }
  Mesh(g,"Lobed ivy leaf clusters",v,triangles,uv,"Leaf mid",Vector3.back);
  for(int i=0;i<10;i++)
  {
   float y=1.3f+i*.37f,x=2.2f+Mathf.Sin(i)*.3f;
   for(int petal=0;petal<5;petal++){float a=petal*Mathf.PI*2/5;var t=Box(g,"Small cream climbing blossom",new Vector3(x+Mathf.Cos(a)*.065f,y+Mathf.Sin(a)*.065f,-6.53f),new Vector3(.095f,.075f,.035f),"Cream bloom");t.rotation=Quaternion.Euler(0,0,petal*72);}
   Box(g,"Blossom ochre centre",new Vector3(x,y,-6.56f),new Vector3(.04f,.04f,.025f),"Bloom centre");
  }
  foreach(float x in new[]{-6.4f,-5.8f,-3.7f})
  {
   Beam(g,"Herb drying cord",new Vector3(x,3.15f,-7.38f),new Vector3(x,2.88f,-7.38f),.02f,"Iron");
   for(int i=0;i<5;i++)Beam(g,"Hanging medicinal herb",new Vector3(x,2.88f,-7.38f),new Vector3(x+(i-2)*.06f,2.42f+(i%2)*.08f,-7.4f),.055f,"Leaf shade");
  }
 }
}
