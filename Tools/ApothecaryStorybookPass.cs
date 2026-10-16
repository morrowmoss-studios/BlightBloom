using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;

// First illustrated exterior style test; generated proxy meshes, not production art.
public static class ApothecaryStorybookPass
{
 const string Dir="Assets/BlightBloom/Locations/StorybookExterior";
 static Transform root;
 static Mesh cube;
 static Dictionary<string,Material> palette;
 static System.Random random;
 static Transform[] before;
 static string collisions;
 public static string Apply()
 {
  var scene=SceneManager.GetActiveScene();
  if(scene.path!="Assets/Scenes/UncleRobertsApothecary.unity"||EditorApplication.isPlayingOrWillChangePlaymode)throw new InvalidOperationException("Open apothecary in Edit mode.");
  if(scene.GetRootGameObjects().Any(g=>g.name=="09 Storybook exterior style test"))throw new InvalidOperationException("Style pass already exists; edit existing assets instead of duplicating it.");
  before=scene.GetRootGameObjects().SelectMany(r=>r.GetComponentsInChildren<Transform>(true)).ToArray();
  collisions=CollisionSignature();
  cube=before.Select(t=>t.GetComponent<MeshFilter>()).First(m=>m!=null&&m.sharedMesh.name=="Cube").sharedMesh;
  if(!AssetDatabase.IsValidFolder(Dir))AssetDatabase.CreateFolder("Assets/BlightBloom/Locations","StorybookExterior");
  foreach(string folder in new[]{"Materials","Textures","Meshes"})if(!AssetDatabase.IsValidFolder(Dir+"/"+folder))AssetDatabase.CreateFolder(Dir,folder);
  random=new System.Random(7124);palette=new Dictionary<string,Material>();
  Painted("Ivory plaster",new Color(.82f,.735f,.57f),0);
  Painted("Weathered walnut",new Color(.255f,.17f,.135f),1);
  Painted("Moss limestone",new Color(.44f,.46f,.37f),2);
  Painted("Charcoal moss slate",new Color(.29f,.32f,.275f),3);
  Painted("Warm carved oak",new Color(.47f,.32f,.19f),1);
  Painted("Sage shutters",new Color(.32f,.43f,.34f),1);
  Painted("Old copper",new Color(.41f,.32f,.20f),4);
  Painted("Soft leaf",new Color(.29f,.43f,.25f),5);
  Solid("Ivory lettering",new Color(.91f,.80f,.57f));
  Solid("Dried lavender",new Color(.40f,.36f,.47f));
  Solid("Wildflower gold",new Color(.77f,.62f,.27f));
  Solid("Amber lantern",new Color(.95f,.58f,.19f));
  palette["Amber lantern"].EnableKeyword("_EMISSION");palette["Amber lantern"].SetColor("_EmissionColor",new Color(1.3f,.57f,.13f));
  Solid("Deep leaf",new Color(.18f,.31f,.235f));
  Solid("Leaf highlight",new Color(.46f,.54f,.29f));
  Undo.SetCurrentGroupName("Apothecary storybook exterior");
  root=Group("09 Storybook exterior style test",null);
  foreach(var t in before)
  {
   var r=t.GetComponent<Renderer>();if(r==null)continue;
   string n=t.name;bool facade=Path(t).Contains("Window apertures and plaster panels");
   if(facade&&(n=="Wall pier"||n=="Window base"||n=="Window header"))Set(r,"Ivory plaster");
   if(Path(t).Contains("Timber structure and stone plinth"))Set(r,n.Contains("Stone")?"Moss limestone":"Weathered walnut");
   if(facade&&(n.Contains("jamb")||n.Contains("sill")||n.Contains("mullion")))Set(r,"Warm carved oak");
   if(n.Contains("Stepped plaster gable"))Set(r,"Ivory plaster");
   if(n.Contains("Gable")||n=="Ridge cap")Set(r,n=="Stepped plaster gable"?"Ivory plaster":"Weathered walnut");
   if(n=="Roof slope")Set(r,"Charcoal moss slate");
   if(n=="Slate course"){Undo.RecordObject(r,"Hide obsolete proxy course renderer");r.enabled=false;}
   if(Path(t).Contains("Storage hearth and exterior chimney")&&n.Contains("Chimney",StringComparison.OrdinalIgnoreCase))Set(r,"Moss limestone");
   if(n=="Front window sill"||n=="Rear window sill")Set(r,"Ivory plaster");
   if(n=="Shop sign block")Set(r,"Weathered walnut");
   if(n.StartsWith("Green apothecary cross")){Undo.RecordObject(r,"Replace cross graphic with mortar emblem");r.enabled=false;}
   if(n.Contains("Open front shutter door")||n.Contains("Open garden door"))Set(r,"Sage shutters");
   if(n.Contains("Main shop entrance")||n.Contains("Garden exit"))Set(r,"Warm carved oak");
  }
  Roof(); Windows(); Joinery(); Greenery(); Lighting(); HandHewnTimber(); Polish(); SignPolish();
  if(CollisionSignature()!=collisions)throw new InvalidOperationException("Collision invariant failed. Do not save.");
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(scene);EditorSceneManager.SaveScene(scene);
  return "Storybook exterior saved; painted materials, shingle meshes, window hoods, joinery, greenery and scene lighting. Existing collider signature unchanged.";
 }
 static string Path(Transform t){return t.parent==null?t.name:Path(t.parent)+"/"+t.name;}
 static string CollisionSignature()
 {
  var s=SceneManager.GetActiveScene();return string.Join("|",s.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Collider>(true)).OrderBy(c=>Path(c.transform)+c.GetType().Name).Select(c=>EditorJsonUtility.ToJson(c)+c.transform.position+c.transform.rotation+c.transform.lossyScale+c.gameObject.activeInHierarchy));
 }
 static void Set(Renderer r,string key){Undo.RecordObject(r,"Exterior material");r.sharedMaterial=palette[key];}
 static Transform Group(string name,Transform p){var g=new GameObject(name);Undo.RegisterCreatedObjectUndo(g,"Storybook group");g.transform.SetParent(p,false);return g.transform;}
 static Transform Shape(Transform p,string name,Vector3 position,Vector3 scale,string material)
 {
  var t=Group(name,p);t.position=position;t.localScale=scale;t.gameObject.AddComponent<MeshFilter>().sharedMesh=cube;t.gameObject.AddComponent<MeshRenderer>().sharedMaterial=palette[material];return t;
 }
 static void Beam(Transform p,string name,Vector3 a,Vector3 b,float width,string mat)
 {var t=Shape(p,name,(a+b)/2,new Vector3(width,(b-a).magnitude,width),mat);t.rotation=Quaternion.FromToRotation(Vector3.up,b-a);}
 static void Solid(string name,Color color)
 {
  var m=new Material(Shader.Find("Universal Render Pipeline/Lit"));m.name=name;m.SetColor("_BaseColor",color);m.SetFloat("_Smoothness",0);m.SetFloat("_Metallic",0);m.SetFloat("_SpecularHighlights",0);m.SetFloat("_EnvironmentReflections",0);m.EnableKeyword("_SPECULARHIGHLIGHTS_OFF");m.EnableKeyword("_ENVIRONMENTREFLECTIONS_OFF");AssetDatabase.CreateAsset(m,Dir+"/Materials/"+name+".mat");palette[name]=m;
 }
 static float Wave(float u,float v,float f,float phase){return Mathf.Sin((u*f+phase)*6.283185f)*Mathf.Cos((v*(f+.5f)+phase)*6.283185f);}
 static void Painted(string name,Color color,int kind)
 {
  const int size=256;var texture=new Texture2D(size,size,TextureFormat.RGBA32,true);texture.name=name+" gouache";var pixels=new Color[size*size];
  for(int y=0;y<size;y++)for(int x=0;x<size;x++)
  {
   float u=x/(float)size,v=y/(float)size;
   float broad=Wave(u,v,2,0.17f)*.032f+Wave(u,v,5,.43f)*.016f;
   float paper=((float)random.NextDouble()-.5f)*.018f;
   float value=broad+paper;
   if(kind==0)value+=Mathf.Sin(u*45+Mathf.Sin(v*19)*1.7f)*.009f;
   if(kind==1)
   {
    float grain=Mathf.Sin((u*22+Mathf.Sin(v*12)*.23f+Mathf.Sin(v*31)*.06f)*6.283185f);
    value+=grain*.027f+Mathf.Pow(Mathf.Abs(Mathf.Sin(u*17+Mathf.Sin(v*4)*.4f)),12)*.032f;
   }
   if(kind==2)
   {
    float row=Mathf.Floor(v*4), a=Mathf.Repeat(u*5+row*.5f,1), b=Mathf.Repeat(v*4,1);
    float edge=Mathf.Min(Mathf.Min(a,1-a),Mathf.Min(b,1-b));
    value+=Mathf.Sin(row*23+Mathf.Floor(u*5+row*.5f)*17)*.033f;
    value-=.065f*(1-Mathf.SmoothStep(0,.075f,edge));value+=.02f*Mathf.Sin(b*3.14f);
   }
   if(kind==3)value+=.035f*Mathf.Sin(v*3.14159f)+.022f*Mathf.Sin(u*20+Mathf.Sin(v*6)*.7f)+.012f*Mathf.Sin(v*40);
   if(kind==4)value+=Mathf.Sin(u*33+v*13)*.012f;
   if(kind==5)value+=.045f*Mathf.Sin(u*3.14f)+.018f*Mathf.Sin(v*22);
   pixels[y*size+x]=new Color(Mathf.Clamp01(color.r+value),Mathf.Clamp01(color.g+value*.87f),Mathf.Clamp01(color.b+value*.72f),1);
  }
  texture.SetPixels(pixels);texture.Apply();string path=Dir+"/Textures/"+name+".png";System.IO.File.WriteAllBytes(path,texture.EncodeToPNG());UnityEngine.Object.DestroyImmediate(texture);AssetDatabase.ImportAsset(path,ImportAssetOptions.ForceSynchronousImport);
  var importer=(TextureImporter)AssetImporter.GetAtPath(path);importer.wrapMode=TextureWrapMode.Repeat;importer.filterMode=FilterMode.Bilinear;importer.mipmapEnabled=true;importer.textureCompression=TextureImporterCompression.Uncompressed;importer.SaveAndReimport();
  Solid(name,Color.white);palette[name].SetTexture("_BaseMap",AssetDatabase.LoadAssetAtPath<Texture2D>(path));
 }
 static void MeshAsset(Transform parent,string name,List<Vector3> verts,List<int> indices,List<Vector2> uv,Material[] materials,List<int>[] sub=null)
 {
  var mesh=new Mesh();mesh.name=name;mesh.SetVertices(verts);mesh.SetUVs(0,uv);
  if(sub==null)mesh.SetTriangles(indices,0);else{mesh.subMeshCount=sub.Length;for(int i=0;i<sub.Length;i++)mesh.SetTriangles(sub[i],i);}
  mesh.RecalculateNormals();
  if(name.Contains("painted shingles"))
  {
   float angle=Mathf.Atan2(3.5f,8.7f);Vector3 n=new Vector3(name.StartsWith("West")?-Mathf.Sin(angle):Mathf.Sin(angle),Mathf.Cos(angle),0);mesh.normals=Enumerable.Repeat(n,verts.Count).ToArray();
  }
  if(name=="Painted ivy leaves")mesh.normals=Enumerable.Repeat(Vector3.back,verts.Count).ToArray();
  mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,Dir+"/Meshes/"+name+".asset");var t=Group(name,parent);t.gameObject.AddComponent<MeshFilter>().sharedMesh=mesh;var renderer=t.gameObject.AddComponent<MeshRenderer>();renderer.sharedMaterials=materials;
  if(name.Contains("painted shingles")){renderer.shadowCastingMode=ShadowCastingMode.Off;renderer.receiveShadows=false;}
 }
 static void Roof()
 {
  var group=Group("Hand-shaped overlapping roof shingles",root);
  for(int side=-1;side<=1;side+=2)
  {
   var verts=new List<Vector3>();var uv=new List<Vector2>();var subs=new[]{new List<int>(),new List<int>(),new List<int>()};
   float angle=Mathf.Atan2(3.5f,8.7f),length=Mathf.Sqrt(3.5f*3.5f+8.7f*8.7f);
   Vector3 normal=new Vector3(side*Mathf.Sin(angle),Mathf.Cos(angle),0);
   for(int row=0;row<15;row++)for(int col=0;col<24;col++)
   {
    float d=row*(length/15), z=-6.7f+col*.65f+(row%2)*.325f;
    if(z>8.5f)continue;
    float width=.63f+((float)random.NextDouble()-.5f)*.05f;
    float tileLength=length/15+.13f;
    // Six-sided painted tile with an uneven softened/scalloped trailing edge.
    Vector2[] shape={new Vector2(0,-width/2),new Vector2(tileLength-.08f,-width/2),new Vector2(tileLength,width*-.3f),new Vector2(tileLength+.025f,width*.25f),new Vector2(tileLength-.06f,width/2),new Vector2(0,width/2)};
    int start=verts.Count;
    for(int k=0;k<shape.Length;k++)
    {
     float distance=Mathf.Min(length+.06f,d+shape[k].x);
     verts.Add(new Vector3(side*distance*Mathf.Cos(angle),10.75f-distance*Mathf.Sin(angle),z+shape[k].y)+normal*(.15f+(15-row)*.008f+Mathf.Pow(shape[k].x/tileLength,2)*.028f));
     uv.Add(new Vector2(shape[k].y/width+.5f,shape[k].x/tileLength));
    }
    int material=random.Next(10)==0?1:random.Next(7)==0?2:0;
    for(int k=1;k<5;k++){subs[material].Add(start);subs[material].Add(start+k);subs[material].Add(start+k+1);subs[material].Add(start);subs[material].Add(start+k+1);subs[material].Add(start+k);}
   }
   // Muted variants use the same painted tile map.
   Material Variant(string name,Color tint){var m=new Material(palette["Charcoal moss slate"]);m.name=name;m.SetColor("_BaseColor",tint);AssetDatabase.CreateAsset(m,Dir+"/Materials/"+name+".mat");return m;}
   var mauve=Variant("Slate mauve variation "+side,new Color(.97f,.94f,.98f));var green=Variant("Slate moss variation "+side,new Color(.93f,1.04f,.87f));
   MeshAsset(group,side<0?"West painted shingles":"East painted shingles",verts,null,uv,new[]{palette["Charcoal moss slate"],mauve,green},subs);
  }
 }
 static void Windows()
 {
  var group=Group("Pointed timber window hoods and shutters",root);
  foreach(var w in before.Where(t=>t.name=="Open framed window"))
  {
   var jamb=w.Cast<Transform>().Where(t=>t.name=="Window jamb").ToArray();if(jamb.Length!=2)continue;
   Vector3 center=(jamb[0].position+jamb[1].position)/2;
   bool side=Mathf.Abs(jamb[0].position.z-jamb[1].position.z)>1;
   Vector3 across=side?Vector3.forward:Vector3.right;
   Vector3 outward=side?new Vector3(Mathf.Sign(center.x),0,0):new Vector3(0,0,Mathf.Sign(center.z-1));
   center+=outward*.22f;
   Vector3 top=center+Vector3.up*.72f;
   Beam(group,"Pointed Gothic hood left",top-across*.89f,top+Vector3.up*.48f,.085f,"Warm carved oak");
   Beam(group,"Pointed Gothic hood right",top+Vector3.up*.48f,top+across*.89f,.085f,"Warm carved oak");
   Beam(group,"Window cross rail",center-across*.74f,center+across*.74f,.055f,"Warm carved oak");
   foreach(int sign in new[]{-1,1})
   {
    var shutter=Shape(group,"Open sage shutter",center+across*(sign*1.02f),side?new Vector3(.10f,1.35f,.28f):new Vector3(.28f,1.35f,.10f),"Sage shutters");
    foreach(float y in new[]{-.4f,.4f})Beam(group,"Shutter brace",center+across*(sign*.9f)+Vector3.up*y+outward*.07f,center+across*(sign*1.14f)+Vector3.up*y+outward*.07f,.06f,"Warm carved oak");
   }
  }
  foreach(float z in new[]{-6.25f,8.25f})
  {
   float x=z<0?0:2;Vector3 center=new Vector3(x,5.55f,z);
   Beam(group,"Upper central window hood",center+new Vector3(-1.1f,.95f,0),center+new Vector3(0,1.35f,0),.09f,"Warm carved oak");
   Beam(group,"Upper central window hood",center+new Vector3(0,1.35f,0),center+new Vector3(1.1f,.95f,0),.09f,"Warm carved oak");
  }
 }
 static void Joinery()
 {
  var group=Group("Eave brackets and apothecary facade details",root);
  foreach(float x in new[]{-8.2f,8.2f})foreach(float z in new[]{-5.5f,-2f,2f,5.5f,7.5f})
   Beam(group,"Carved eave corbel",new Vector3(x,6.6f,z),new Vector3(x*1.055f,7.15f,z),.12f,"Weathered walnut");
  foreach(float z in new[]{-6.28f,8.28f})
  {
   float x=z<0?0:2;
   for(int sign=-1;sign<=1;sign+=2)
    for(int i=0;i<4;i++)Shape(group,"Entrance stone quoin",new Vector3(x+sign*1.4f,.3f+i*.65f,z),new Vector3(.35f,.48f,.16f),"Moss limestone");
   Beam(group,"Entrance carved lintel",new Vector3(x-1.25f,2.9f,z),new Vector3(x+1.25f,2.9f,z),.15f,"Warm carved oak");
  }
  // Text is a temporary readable sign graphic; production needs a bespoke painted mesh/texture.
  var lettering=Group("Robert's apothecary lettering",group);lettering.position=new Vector3(-2.8f,3.1f,-6.48f);
  var text=lettering.gameObject.AddComponent<TextMesh>();text.text="ROBERT'S APOTHECARY";text.font=Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");text.fontSize=64;text.characterSize=.052f;text.anchor=TextAnchor.MiddleCenter;text.color=new Color(.91f,.80f,.57f);lettering.GetComponent<MeshRenderer>().sharedMaterial=text.font.material;
  // Mortar bowl and angled pestle emblem: deliberately readable low-poly signage.
  for(int i=0;i<5;i++)Shape(group,"Mortar bowl emblem",new Vector3(-4.2f,3.04f-i*.024f,-6.49f),new Vector3(.36f-i*.045f,.028f,.025f),"Ivory lettering");
  Beam(group,"Pestle emblem",new Vector3(-4.15f,3.08f,-6.50f),new Vector3(-4.04f,3.26f,-6.50f),.045f,"Ivory lettering");
  // Small steep porch roof stays below the existing upstairs window.
  float slope=Mathf.Atan2(.95f,1.5f)*Mathf.Rad2Deg;
  foreach(int direction in new[]{-1,1})
  {
   var canopy=Shape(group,"Steep entrance canopy",new Vector3(direction*.75f,3.5f,-6.65f),new Vector3(1.78f,.12f,1),"Charcoal moss slate");canopy.rotation=Quaternion.Euler(0,0,-direction*slope);
   Beam(group,"Porch carved verge",new Vector3(0,4.02f,-7.18f),new Vector3(direction*1.55f,3.04f,-7.18f),.09f,"Warm carved oak");
  }
  foreach(float x in new[]{-1.7f,1.7f})
  {
   var lamp=Group("Amber entrance lantern",group);
   Shape(lamp,"Wall bracket",new Vector3(x,2.5f,-6.45f),new Vector3(.06f,.06f,.5f),"Old copper");
   Shape(lamp,"Amber glass proxy",new Vector3(x,2.22f,-6.65f),new Vector3(.19f,.32f,.19f),"Amber lantern");
   foreach(float y in new[]{2.02f,2.42f})Shape(lamp,"Lantern cap",new Vector3(x,y,-6.65f),new Vector3(.3f,.06f,.3f),"Old copper");
   foreach(int corner in new[]{-1,1})foreach(int depth in new[]{-1,1})Shape(lamp,"Lantern frame",new Vector3(x+corner*.11f,2.22f,-6.65f+depth*.11f),new Vector3(.025f,.4f,.025f),"Old copper");
   var glow=Group("Warm lantern glow",lamp);glow.position=new Vector3(x,2.22f,-6.8f);var light=glow.gameObject.AddComponent<Light>();light.type=LightType.Point;light.color=new Color(1,.65f,.28f);light.intensity=.65f;light.range=2.5f;light.shadows=LightShadows.None;
  }
  // Rounded finial silhouette is suggested with simple stacked blocks.
  foreach(float z in new[]{-6.72f,8.72f})
  {
   Shape(group,"Ridge finial stem",new Vector3(0,11.05f,z),new Vector3(.10f,.55f,.10f),"Old copper");
   var diamond=Shape(group,"Ridge finial diamond",new Vector3(0,11.32f,z),new Vector3(.16f,.16f,.16f),"Old copper");diamond.rotation=Quaternion.Euler(0,0,45);
  }
 }
 static void Greenery()
 {
  var group=Group("Restrained ivy and window herbs",root);
  var verts=new List<Vector3>();var indices=new[]{new List<int>(),new List<int>(),new List<int>()};var uv=new List<Vector2>();
  void Leaf(Vector3 p,float size,int shade)
  {
   int a=verts.Count;float tilt=((float)random.NextDouble()-.5f)*.6f;
   verts.Add(p+new Vector3(-size*.6f,tilt*size,0));verts.Add(p+new Vector3(0,-size*.4f,-.025f));verts.Add(p+new Vector3(size*.6f,-tilt*size,0));verts.Add(p+new Vector3(0,size,-.02f));
   uv.AddRange(new[]{new Vector2(0,.3f),new Vector2(.5f,0),new Vector2(1,.3f),new Vector2(.5f,1)});
   foreach(int v in new[]{0,1,3,1,2,3,0,3,1,1,3,2})indices[shade].Add(a+v);
  }
  for(int branch=0;branch<4;branch++)
  {
   float x=-7.55f+branch*.24f;Vector3 previous=new Vector3(x,.05f,-6.33f);
   for(int i=0;i<14-branch*2;i++)
   {
    var next=new Vector3(x+Mathf.Sin(i*.7f+branch)*.18f,.1f+i*.22f,-6.34f);
    Beam(group,"Ivy stem",previous,next,.022f,"Weathered walnut");previous=next;
    Leaf(next+Vector3.right*((i%2==0?1:-1)*.13f),.14f+(float)random.NextDouble()*.08f,random.Next(3));
   }
  }
  foreach(float x in new[]{-4.5f,4.5f})
  {
   Shape(group,"Window herb box",new Vector3(x,.94f,-6.35f),new Vector3(1.5f,.27f,.42f),"Weathered walnut");
   for(int i=0;i<14;i++)Leaf(new Vector3(x-.65f+(float)random.NextDouble()*1.3f,1.06f+(float)random.NextDouble()*.18f,-6.56f),.12f,random.Next(3));
  }
  foreach(float x in new[]{-4.5f,4.5f})for(int i=0;i<5;i++)
  {
   float xx=x-.5f+i*.24f;Beam(group,"Medicinal herb flower stem",new Vector3(xx,1.1f,-6.58f),new Vector3(xx,1.48f,-6.59f),.018f,"Deep leaf");
   for(int petal=0;petal<4;petal++)
   {
    float a=petal*Mathf.PI/2;var blossom=Shape(group,"Small purple and gold wildflower",new Vector3(xx+Mathf.Cos(a)*.045f,1.48f+Mathf.Sin(a)*.045f,-6.6f),new Vector3(.055f,.055f,.025f),i%3==0?"Wildflower gold":"Dried lavender");blossom.rotation=Quaternion.Euler(0,0,petal*90+30);
   }
  }
  MeshAsset(group,"Painted ivy leaves",verts,null,uv,new[]{palette["Soft leaf"],palette["Deep leaf"],palette["Leaf highlight"]},indices);
 }
 public static string SignPolish()
 {
  root=SceneManager.GetActiveScene().GetRootGameObjects().First(g=>g.name=="09 Storybook exterior style test").transform;
  if(palette==null)palette=new Dictionary<string,Material>();palette["Weathered walnut"]=AssetDatabase.LoadAssetAtPath<Material>(Dir+"/Materials/Weathered walnut.mat");
  var nodes=root.GetComponentsInChildren<Transform>(true);var lettering=nodes.First(t=>t.name=="Robert's apothecary lettering");
  Undo.RecordObject(lettering,"Readable apothecary sign");lettering.position=new Vector3(-3,3.1f,-6.6f);
  var text=lettering.GetComponent<TextMesh>();Undo.RecordObject(text,"Readable sign size");text.characterSize=.042f;
  if(!nodes.Any(t=>t.name=="Mortar sign backing"))Shape(root,"Mortar sign backing",new Vector3(-3.25f,3.1f,-6.49f),new Vector3(3.25f,.52f,.09f),"Weathered walnut");
  foreach(var t in nodes.Where(t=>t.name=="Mortar bowl emblem"||t.name=="Pestle emblem"))
  {
   Undo.RecordObject(t,"Mortar emblem alignment");var p=t.position;t.position=new Vector3(p.x> -4.5f?p.x-.4f:p.x,p.y,-6.62f);
  }
  EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());EditorSceneManager.SaveScene(SceneManager.GetActiveScene());return "Sign backing and botanical emblem legibility adjusted.";
 }
 public static string HandHewnTimber()
 {
  var mesh=AssetDatabase.LoadAssetAtPath<Mesh>(Dir+"/Meshes/Hand-hewn timber unit.asset");
  if(mesh==null)
  {
   mesh=new Mesh();mesh.name="Hand-hewn timber unit";var verts=new List<Vector3>();var uv=new List<Vector2>();var triangles=new List<int>();
   var cross=new[]{new Vector2(-.46f,-.31f),new Vector2(-.31f,-.46f),new Vector2(.31f,-.46f),new Vector2(.46f,-.31f),new Vector2(.46f,.31f),new Vector2(.31f,.46f),new Vector2(-.31f,.46f),new Vector2(-.46f,.31f)};
   for(int ring=0;ring<3;ring++)for(int i=0;i<8;i++)
   {
    float scale=ring==1?1.025f:ring==2?.97f:1;verts.Add(new Vector3(cross[i].x*scale+(ring-1)*.012f,ring*.5f-.5f,cross[i].y*scale));uv.Add(new Vector2(i/8f,ring*.5f));
   }
   for(int ring=0;ring<2;ring++)for(int i=0;i<8;i++){int a=ring*8+i,b=ring*8+(i+1)%8;triangles.AddRange(new[]{a,b,b+8,a,b+8,a+8});}
   for(int i=1;i<7;i++){triangles.AddRange(new[]{0,i+1,i,16,16+i,17+i});}
   mesh.SetVertices(verts);mesh.SetUVs(0,uv);mesh.SetTriangles(triangles,0);mesh.RecalculateNormals();mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,Dir+"/Meshes/Hand-hewn timber unit.asset");
  }
  var firstVertex=mesh.vertices[0];var firstNormal=mesh.normals[0];
  if(Vector3.Dot(new Vector3(firstNormal.x,0,firstNormal.z),new Vector3(firstVertex.x,0,firstVertex.z))<0)
  {
   var indices=mesh.triangles;for(int i=0;i<indices.Length;i+=3){int swap=indices[i+1];indices[i+1]=indices[i+2];indices[i+2]=swap;}mesh.triangles=indices;mesh.RecalculateNormals();EditorUtility.SetDirty(mesh);
  }
  foreach(var t in SceneManager.GetActiveScene().GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)))
  {
   if(!(t.name.Contains("timber post")||t.name=="Gable king post"||t.name=="Front diagonal brace"))continue;
   var filter=t.GetComponent<MeshFilter>();if(filter!=null){Undo.RecordObject(filter,"Hand-hewn render mesh");filter.sharedMesh=mesh;}
  }
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());EditorSceneManager.SaveScene(SceneManager.GetActiveScene());return "Bevelled hand-hewn render meshes applied; collision envelopes unchanged.";
 }
 public static string Polish()
 {
  root=SceneManager.GetActiveScene().GetRootGameObjects().First(g=>g.name=="09 Storybook exterior style test").transform;
  before=SceneManager.GetActiveScene().GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>(true)).ToArray();
  if(palette==null)palette=new Dictionary<string,Material>();
  foreach(string name in new[]{"Ivory plaster","Weathered walnut","Charcoal moss slate"})palette[name]=AssetDatabase.LoadAssetAtPath<Material>(Dir+"/Materials/"+name+".mat");
  foreach(var filter in root.GetComponentsInChildren<MeshFilter>())
  {
   var mesh=filter.sharedMesh;
   if(mesh.name.Contains("painted shingles"))
   {
    float angle=Mathf.Atan2(3.5f,8.7f),length=Mathf.Sqrt(3.5f*3.5f+8.7f*8.7f);int side=mesh.name.StartsWith("West")?-1:1;Vector3 normal=new Vector3(side*Mathf.Sin(angle),Mathf.Cos(angle),0);
    var vertices=mesh.vertices;var uv=mesh.uv;
    for(int start=0;start<vertices.Length;start+=6)
    {
     int row=Mathf.Clamp(Mathf.RoundToInt(Mathf.Abs(vertices[start].x)/Mathf.Cos(angle)/(length/15)),0,14);
     for(int k=0;k<6;k++)
     {
      int i=start+k;float d=Mathf.Min(length+.06f,row*(length/15)+uv[i].y*(length/15+.13f));
      vertices[i]=new Vector3(side*d*Mathf.Cos(angle),10.75f-d*Mathf.Sin(angle),vertices[i].z)+normal*(.15f+(15-row)*.008f+uv[i].y*uv[i].y*.028f);
     }
    }
    mesh.vertices=vertices;mesh.normals=Enumerable.Repeat(normal,mesh.vertexCount).ToArray();mesh.RecalculateBounds();EditorUtility.SetDirty(mesh);
    var renderer=filter.GetComponent<Renderer>();renderer.shadowCastingMode=ShadowCastingMode.Off;renderer.receiveShadows=false;
   }
   if(mesh.name=="Painted ivy leaves"){mesh.normals=Enumerable.Repeat(Vector3.back,mesh.vertexCount).ToArray();EditorUtility.SetDirty(mesh);}
  }
  if(!root.Cast<Transform>().Any(t=>t.name=="Smooth painted gable faces"))
  {
   var group=Group("Smooth painted gable faces",root);
   foreach(var t in before.Where(t=>t.name=="Stepped plaster gable")){var renderer=t.GetComponent<Renderer>();Undo.RecordObject(renderer,"Smooth gable proxy surface");renderer.enabled=false;}
   foreach(int side in new[]{-1,1})
   {
    float z=side<0?-6.14f:8.14f;
    var vertices=new List<Vector3>{new Vector3(-8,7.25f,z),new Vector3(8,7.25f,z),new Vector3(0,10.74f,z)};
    var indices=side<0?new List<int>{0,2,1}:new List<int>{0,1,2};
    MeshAsset(group,side<0?"Front painted gable":"Rear painted gable",vertices,indices,new List<Vector2>{new Vector2(0,0),new Vector2(1,0),new Vector2(.5f,1)},new[]{palette["Ivory plaster"]});
   }
  }
  AssetDatabase.SaveAssets();EditorSceneManager.MarkSceneDirty(SceneManager.GetActiveScene());EditorSceneManager.SaveScene(SceneManager.GetActiveScene());return "Shingle and leaf normals corrected; smooth gable proxy faces saved.";
 }
 static void Lighting()
 {
  var sun=before.First(t=>t.name=="Sun").GetComponent<Light>();Undo.RecordObject(sun,"Storybook sun");sun.color=new Color(1,.875f,.70f);sun.intensity=1.65f;sun.shadows=LightShadows.Soft;sun.shadowStrength=.65f;sun.shadowBias=.04f;
  // Existing light transform retained; no project-wide pipeline or quality changes.
  RenderSettings.ambientMode=AmbientMode.Trilight;RenderSettings.ambientSkyColor=new Color(.55f,.63f,.66f);RenderSettings.ambientEquatorColor=new Color(.48f,.46f,.39f);RenderSettings.ambientGroundColor=new Color(.30f,.32f,.25f);
  var sky=new Material(Shader.Find("Skybox/Procedural"));sky.name="Illustrated warm daylight";sky.SetColor("_SkyTint",new Color(.60f,.61f,.59f));sky.SetColor("_GroundColor",new Color(.42f,.43f,.35f));sky.SetFloat("_Exposure",.9f);sky.SetFloat("_SunSize",.02f);AssetDatabase.CreateAsset(sky,Dir+"/Materials/Illustrated daylight.mat");RenderSettings.skybox=sky;
  var fill=Group("Soft cool exterior fill",root);fill.rotation=Quaternion.Euler(35,145,0);var light=fill.gameObject.AddComponent<Light>();light.type=LightType.Directional;light.color=new Color(.71f,.80f,.85f);light.intensity=.28f;light.shadows=LightShadows.None;
 }
}
