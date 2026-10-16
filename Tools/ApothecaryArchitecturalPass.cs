using System;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;

// Editor-only authoring utility, compiled on demand with Unity Pipeline run_script.
// The original greybox generator is deliberately left intact.
public static class ApothecaryArchitecturalPass
{
    static Transform root;
    static Transform[] original;
    static Dictionary<string,Material> mats;
    const string MatPath="Assets/BlightBloom/Locations/ProxyMaterials";
    public static string Apply()
    {
        var scene=SceneManager.GetActiveScene();
        if(scene.path!="Assets/Scenes/UncleRobertsApothecary.unity" || EditorApplication.isPlayingOrWillChangePlaymode)
            throw new InvalidOperationException("Open the apothecary in Edit mode first.");
        if(scene.GetRootGameObjects().Any(g=>g.name=="08 Architectural proxy pass"))
            throw new InvalidOperationException("Proxy pass already exists; edit it in the hierarchy rather than duplicating it.");
        original=scene.GetRootGameObjects().SelectMany(g=>g.GetComponentsInChildren<Transform>()).ToArray();
        if(!AssetDatabase.IsValidFolder(MatPath)) AssetDatabase.CreateFolder("Assets/BlightBloom/Locations","ProxyMaterials");
        mats=new Dictionary<string,Material>();
        Material("Timber",new Color(.19f,.105f,.065f)); Material("Oak",new Color(.43f,.28f,.14f));
        Material("Plaster",new Color(.76f,.69f,.53f)); Material("Limewash",new Color(.88f,.82f,.67f));
        Material("Stone",new Color(.38f,.40f,.37f)); Material("Roof",new Color(.19f,.25f,.29f));
        Material("Shop",new Color(.48f,.40f,.27f)); Material("Treatment",new Color(.55f,.68f,.63f));
        Material("Preparation",new Color(.42f,.51f,.31f)); Material("Storage",new Color(.42f,.35f,.27f));
        Material("Bedroom",new Color(.53f,.37f,.34f)); Material("Study",new Color(.29f,.40f,.44f));
        Material("Living",new Color(.63f,.52f,.34f)); Material("Linen",new Color(.80f,.78f,.65f));
        Material("Earth",new Color(.28f,.23f,.16f)); Material("Herb",new Color(.28f,.41f,.20f));
        Material("Iron",new Color(.14f,.16f,.16f)); Material("Hearth",new Color(.12f,.105f,.09f));
        Undo.SetCurrentGroupName("Apothecary architectural proxy pass");
        root=Group("08 Architectural proxy pass",null);
        // Shared proxy palette on original geometry; no original collider or transform changes here.
        foreach(var t in original)
        {
            var r=t.GetComponent<Renderer>(); if(r==null) continue;
            string key="Limewash";
            if(t.name.Contains("floor")||t.name=="Upper landing"||t.name.StartsWith("Tread")||t.name.Contains("guard"))key="Oak";
            if(t.name=="Village ground")key="Herb";
            if(t.name.Contains("approach")||t.name.Contains("path")||t.name.Contains("boundary"))key="Stone";
            if(t.name=="Raised bed")key="Earth";
            if(t.name=="Herb placeholder")key="Herb";
            if(t.name=="Dispensing counter"||t.name=="Crates"||t.name=="Personal chest"||t.name=="Bench"||t.name.Contains("shelf")||t.name.Contains("Bookcase")||t.name.Contains("desk")||t.name.Contains("bench")||t.name=="Table")key="Oak";
            if(t.name=="Examination couch"||t.name=="Bed")key="Linen";
            if(t.name=="Mortar placeholder"||t.name=="Wash stand")key="Stone";
            Undo.RecordObject(r,"Proxy palette"); r.sharedMaterial=mats[key];
        }
        var windows=Group("Window apertures and plaster panels",root);
        foreach(var t in original.Where(t=>t.parent!=null && (t.parent.name=="Ground exterior walls"||t.parent.name=="Upper exterior walls")))
        {
            if(t.name.Contains("lintel"))continue;
            bool side=t.name=="West wall"||t.name=="East wall";
            bool front=t.name.StartsWith("Front wall");
            bool rear=t.name.StartsWith("Rear garden door");
            if(!side&&!front&&!rear)continue;
            // Retain the originals, disabled, as reversible blockout references.
            Undo.RecordObject(t.gameObject,"Retain original wall backup"); t.gameObject.SetActive(false);
            float floor=t.position.y-1.8f;
            float start=side?-6:t.position.x-t.localScale.x/2;
            float end=side?8:t.position.x+t.localScale.x/2;
            float plane=side?t.position.x:t.position.z;
            float[] centers=side?new[]{-3f,2f,6f}:new[]{front?(t.position.x<0?-4.5f:4.5f):(t.position.x<0?-4f:5.8f)};
            float cursor=start;
            var group=Group(t.parent.name+" / "+t.name,windows);
            foreach(float c in centers)
            {
                float a=c-.8f,b=c+.8f;
                Panel(group,side,plane,cursor,a,floor+1.8f,3.6f,"Wall pier");
                Panel(group,side,plane,a,b,floor+.55f,1.1f,"Window base");
                Panel(group,side,plane,a,b,floor+3f,1.2f,"Window header");
                Window(group,side,plane,c,floor);
                cursor=b;
            }
            Panel(group,side,plane,cursor,end,floor+1.8f,3.6f,"Wall pier");
        }
        var frame=Group("Timber structure and stone plinth",root);
        for(int level=0;level<2;level++)
        {
            float y=level*3.6f;
            foreach(float x in new[]{-8f,-1.2f,1.2f,8f})
                Box(frame,"Front timber post",new Vector3(x,y+1.8f,-6.15f),new Vector3(.18f,3.6f,.18f),"Timber");
            foreach(float x in new[]{-8f,.8f,3.2f,8f})
                Box(frame,"Rear timber post",new Vector3(x,y+1.8f,8.15f),new Vector3(.18f,3.6f,.18f),"Timber");
            foreach(float x in new[]{-8.15f,8.15f})
                foreach(float z in new[]{-6f,-.5f,4f,8f})
                    Box(frame,"Side timber post",new Vector3(x,y+1.8f,z),new Vector3(.18f,3.6f,.18f),"Timber");
            foreach(float z in new[]{-6.15f,8.15f})
                Box(frame,"Storey belt beam",new Vector3(0,y+3.5f,z),new Vector3(16.4f,.22f,.22f),"Timber");
            foreach(float x in new[]{-8.15f,8.15f})
                Box(frame,"Side belt beam",new Vector3(x,y+3.5f,1),new Vector3(.22f,.22f,14.4f),"Timber");
            for(int side=-1;side<=1;side+=2)
                Beam(frame,"Front diagonal brace",new Vector3(side*6.8f,y+2.55f,-6.19f),new Vector3(side*5.7f,y+3.35f,-6.19f),.14f,"Timber");
        }
        foreach(float x in new[]{-8.16f,8.16f})
            Box(frame,"Stone foundation",new Vector3(x,.3f,1),new Vector3(.32f,.6f,14.4f),"Stone",true);
        foreach(float z in new[]{-6.16f,8.16f})
        {
            float door=z<0?0:2;
            Box(frame,"Stone foundation left",new Vector3((-8+door-1.2f)/2,.3f,z),new Vector3(door-1.2f+8,.6f,.32f),"Stone",true);
            Box(frame,"Stone foundation right",new Vector3((door+1.2f+8)/2,.3f,z),new Vector3(8-door-1.2f,.6f,.32f),"Stone",true);
        }
        var roof=Group("Pitched slate proxy roof",root);
        float rise=3.5f,half=8.7f,len=Mathf.Sqrt(rise*rise+half*half),angle=Mathf.Atan2(rise,half)*Mathf.Rad2Deg;
        for(int side=-1;side<=1;side+=2)
        {
            var panel=Box(roof,"Roof slope",new Vector3(side*half/2,7.25f+rise/2,1),new Vector3(len,.22f,15.4f),"Roof",true);
            panel.localRotation=Quaternion.Euler(0,0,-side*angle);
            for(int row=1;row<=5;row++)
            {
                float x=side*half*row/6;
                Box(roof,"Slate course",new Vector3(x,10.75f-Mathf.Abs(x)*rise/half+.13f,1),new Vector3(.07f,.06f,15.4f),"Stone");
            }
            foreach(float z in new[]{-6.65f,8.65f})
                Beam(roof,"Gable verge",new Vector3(0,10.8f,z),new Vector3(side*8.75f,7.27f,z),.22f,"Timber");
        }
        Box(roof,"Ridge cap",new Vector3(0,10.9f,1),new Vector3(.3f,.25f,15.6f),"Roof");
        foreach(float z in new[]{-6f,8f})
        {
            for(int row=0;row<10;row++)
            {
                float y=7.2f+(row+.5f)*.35f;
                Box(roof,"Stepped plaster gable",new Vector3(0,y,z),new Vector3(16*(1-(row+.5f)/10),.35f,.2f),"Plaster");
            }
            Box(roof,"Gable king post",new Vector3(0,8.9f,z+(z<0?-.14f:.14f)),new Vector3(.2f,3.4f,.2f),"Timber");
        }
        var entries=Group("Entrance surrounds and apothecary sign",root);
        Portal(entries,new Vector3(0,0,-6.25f),2.4f,"Main shop entrance");
        Portal(entries,new Vector3(2,0,8.25f),2.4f,"Garden exit");
        // Open door leaves sit against the outside wall, never across the walkable openings.
        Box(entries,"Open front shutter door",new Vector3(1.5f,1.25f,-6.32f),new Vector3(.5f,2.5f,.12f),"Oak");
        Box(entries,"Open garden door",new Vector3(3.55f,1.25f,8.32f),new Vector3(.5f,2.5f,.12f),"Oak");
        var oldSign=original.First(t=>t.name=="Shop sign block"); oldSign.GetComponent<Renderer>().sharedMaterial=mats["Timber"];
        Box(entries,"Green apothecary cross vertical",new Vector3(-3,3.1f,-6.46f),new Vector3(.18f,.39f,.06f),"Herb");
        Box(entries,"Green apothecary cross horizontal",new Vector3(-3,3.1f,-6.46f),new Vector3(.55f,.14f,.06f),"Herb");
        var structure=Group("Interior beams and stair joinery",root);
        foreach(float y in new[]{3.22f,6.85f})
            foreach(float z in new[]{-4.7f,.2f,4.2f,7.1f})
                Box(structure,"Exposed ceiling beam",new Vector3(-1.5f,y,z),new Vector3(12.8f,.22f,.2f),"Timber");
        foreach(float x in new[]{5.16f,7.78f})
        {
            for(int i=0;i<7;i++)
            {
                float z=-3.6f+i*1.35f, h=.2f+(z+3.75f)*.4f;
                Box(structure,"Stair baluster",new Vector3(x,h+.45f,z),new Vector3(.09f,.9f,.09f),"Timber");
            }
            Beam(structure,"Sloped stair handrail",new Vector3(x,1.12f,-3.75f),new Vector3(x,4.52f,4.75f),.11f,"Timber");
        }
        foreach(float z in new[]{-4f,5f}) Box(structure,"Stair newel",new Vector3(5.08f,4.25f,z),new Vector3(.2f,1.3f,.2f),"Timber");
        var hearth=Group("Storage hearth and exterior chimney",root);
        Box(hearth,"Hearth slab",new Vector3(-7.23f,.08f,5.15f),new Vector3(1.5f,.16f,1.7f),"Stone",true);
        foreach(float z in new[]{4.5f,5.8f}) Box(hearth,"Fireplace stone jamb",new Vector3(-7.55f,.7f,z),new Vector3(.85f,1.4f,.3f),"Stone",true);
        Box(hearth,"Fireplace lintel",new Vector3(-7.55f,1.45f,5.15f),new Vector3(1,.25f,1.7f),"Stone",true);
        Box(hearth,"Firebox back",new Vector3(-7.92f,.7f,5.15f),new Vector3(.08f,1.2f,1.1f),"Hearth");
        Box(hearth,"Stone chimney stack",new Vector3(-8.55f,6,5.15f),new Vector3(1.1f,12,1.3f),"Stone",true);
        Box(hearth,"Chimney cap",new Vector3(-8.55f,12.1f,5.15f),new Vector3(1.5f,.25f,1.7f),"Stone",true);
        for(int row=0;row<18;row++) Box(hearth,"Chimney masonry band",new Vector3(-8.55f,.6f+row*.63f,5.15f),new Vector3(1.15f,.055f,1.35f),"Plaster");
        RoomsAndProps();
        AssetDatabase.SaveAssets();
        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene);
        return "Architectural pass saved. Existing layout and traversal retained; additions grouped under 08 Architectural proxy pass.";
    }
    static void RoomsAndProps()
    {
        var rooms=Group("Room finishes and furniture proxies",root);
        Floor(rooms,"Shop floor",new Vector3(-1.5f,.012f,-3),new Vector3(12.8f,.016f,5.8f),"Shop");
        Floor(rooms,"Treatment floor",new Vector3(-4.25f,.012f,2),new Vector3(7.25f,.016f,3.8f),"Treatment");
        Floor(rooms,"Medicine preparation floor",new Vector3(2.25f,.012f,2),new Vector3(5.25f,.016f,3.8f),"Preparation");
        Floor(rooms,"Storage floor",new Vector3(-1.5f,.012f,6),new Vector3(12.8f,.016f,3.8f),"Storage");
        Floor(rooms,"Bedroom floor",new Vector3(-4.5f,3.612f,-2.5f),new Vector3(6.8f,.016f,6.8f),"Bedroom");
        Floor(rooms,"Study floor",new Vector3(-4.5f,3.612f,4.5f),new Vector3(6.8f,.016f,6.8f),"Study");
        Floor(rooms,"Living floor",new Vector3(2,3.612f,1),new Vector3(5.8f,.016f,13.8f),"Living");
        foreach(string name in new[]{"Dispensing counter","Preparation bench","Writing desk","Table"})
        {
            var t=original.First(x=>x.name==name); var size=t.localScale; var pos=t.position;
            Box(rooms,name+" oak worktop",pos+Vector3.up*(size.y/2+.04f),new Vector3(size.x+.1f,.08f,size.z+.1f),"Oak");
            for(int i=0;i<4;i++) Box(rooms,name+" face joinery",pos+new Vector3((i-1.5f)*size.x/4,0,-size.z/2-.015f),new Vector3(.045f,size.y,.04f),"Timber");
        }
        foreach(string name in new[]{"Shop shelf","Storage shelves","Bookcase west","Bookcase rear"})
        {
            var t=original.First(x=>x.name==name); var size=t.localScale; var pos=t.position;
            Undo.RecordObject(t.GetComponent<Renderer>(),"Proxy shelving face"); t.GetComponent<Renderer>().enabled=false;
            var group=Group(name+" joinery (original collision envelope)",rooms);
            bool side=size.x<size.z;
            for(int i=0;i<4;i++) Box(group,"Shelf board",new Vector3(pos.x,pos.y-size.y/2+i*size.y/3,pos.z),new Vector3(size.x,.08f,size.z),"Oak");
            foreach(int sign in new[]{-1,1})
                Box(group,"Shelf upright",pos+(side?new Vector3(0,0,sign*(size.z/2-.05f)):new Vector3(sign*(size.x/2-.05f),0,0)),side?new Vector3(size.x,size.y,.1f):new Vector3(.1f,size.y,size.z),"Timber");
            for(int shelf=0;shelf<3;shelf++) for(int item=0;item<5;item++)
            {
                Vector3 v=side?new Vector3(0,0,(item-2)*size.z/6):new Vector3((item-2)*size.x/6,0,0);
                v+=pos+Vector3.up*(-size.y/2+shelf*size.y/3+.22f);
                Box(group,name.StartsWith("Bookcase")?"Book spine":"Medicine jar proxy",v,side?new Vector3(size.x*.65f,.3f,.14f):new Vector3(.14f,.3f,size.z*.65f),shelf%2==0?"Preparation":"Linen");
            }
        }
        foreach(string n in new[]{"Bed","Examination couch"})
        {
            var t=original.First(x=>x.name==n); var p=t.position;var s=t.localScale;
            Box(rooms,n+" padded surface",p+Vector3.up*(s.y/2+.07f),new Vector3(s.x,.14f,s.z),"Linen");
            Box(rooms,n+" cover",p+new Vector3(0,s.y/2+.15f,s.z*.15f),new Vector3(s.x*.96f,.03f,s.z*.6f),n=="Bed"?"Bedroom":"Treatment");
            Box(rooms,n+" pillow",p+new Vector3(0,s.y/2+.18f,-s.z*.35f),new Vector3(s.x*.65f,.16f,s.z*.2f),"Linen");
            Box(rooms,n+" headboard",p+new Vector3(0,.2f,-s.z/2),new Vector3(s.x+.1f,s.y+.4f,.12f),"Timber");
        }
        foreach(string n in new[]{"Crates","Personal chest"})
        {
            var t=original.First(x=>x.name==n);
            foreach(float ratio in new[]{-.3f,.3f}) Box(rooms,n+" iron band",t.position+new Vector3(ratio*t.localScale.x,0,0),new Vector3(.08f,t.localScale.y+.03f,t.localScale.z+.03f),"Iron");
        }
        var drying=Group("Herb drying rack above preparation bench",rooms);
        foreach(float z in new[]{1f,3f}) Box(drying,"Suspension",new Vector3(4.2f,2.85f,z),new Vector3(.06f,.55f,.06f),"Iron");
        Box(drying,"Rack rail",new Vector3(4.2f,2.57f,2),new Vector3(.55f,.1f,2.3f),"Timber");
        for(int i=0;i<6;i++) Box(drying,"Hanging herb bundle",new Vector3(4.2f,2.3f,1.2f+i*.3f),new Vector3(.18f,.45f,.16f),"Herb");
    }
    static void Material(string name,Color color)
    {
        string path=MatPath+"/"+name+".mat";
        var m=AssetDatabase.LoadAssetAtPath<Material>(path);
        if(m==null){m=new Material(Shader.Find("Universal Render Pipeline/Lit"));m.name=name;AssetDatabase.CreateAsset(m,path);}
        m.SetColor("_BaseColor",color);m.SetFloat("_Smoothness",.12f);mats[name]=m;
    }
    static Transform Group(string n,Transform p){var g=new GameObject(n);Undo.RegisterCreatedObjectUndo(g,"Proxy group");g.transform.SetParent(p,false);return g.transform;}
    static Transform Box(Transform p,string n,Vector3 pos,Vector3 size,string mat,bool solid=false)
    {
        var g=GameObject.CreatePrimitive(PrimitiveType.Cube);Undo.RegisterCreatedObjectUndo(g,"Proxy geometry");
        g.name=n;g.transform.SetParent(p,false);g.transform.position=pos;g.transform.localScale=size;
        g.GetComponent<Renderer>().sharedMaterial=mats[mat];g.GetComponent<Collider>().enabled=solid;return g.transform;
    }
    static void Floor(Transform p,string n,Vector3 pos,Vector3 size,string mat){Box(p,n,pos,size,mat);}
    static void Beam(Transform p,string n,Vector3 a,Vector3 b,float w,string mat){var t=Box(p,n,(a+b)/2,new Vector3(w,(b-a).magnitude,w),mat);t.rotation=Quaternion.FromToRotation(Vector3.up,b-a);}
    static void Panel(Transform p,bool side,float plane,float a,float b,float y,float h,string n)
    {if(b-a<.001f)return;Box(p,n,side?new Vector3(plane,y,(a+b)/2):new Vector3((a+b)/2,y,plane),side?new Vector3(.2f,h,b-a):new Vector3(b-a,h,.2f),y>3.6f?"Limewash":"Plaster",true);}
    static void Window(Transform p,bool side,float plane,float c,float floor)
    {
        var w=Group("Open framed window",p);
        foreach(float edge in new[]{-.8f,.8f})
            Box(w,"Window jamb",side?new Vector3(plane,floor+1.75f,c+edge):new Vector3(c+edge,floor+1.75f,plane),side?new Vector3(.34f,1.5f,.1f):new Vector3(.1f,1.5f,.34f),"Timber");
        foreach(float y in new[]{floor+1.1f,floor+2.4f})
            Box(w,"Window sill and lintel",side?new Vector3(plane,y,c):new Vector3(c,y,plane),side?new Vector3(.4f,.12f,1.85f):new Vector3(1.85f,.12f,.4f),"Timber");
        Box(w,"Window mullion",side?new Vector3(plane,floor+1.75f,c):new Vector3(c,floor+1.75f,plane),side?new Vector3(.12f,1.3f,.065f):new Vector3(.065f,1.3f,.12f),"Oak");
    }
    static void Portal(Transform p,Vector3 center,float width,string name)
    {
        foreach(int side in new[]{-1,1})Box(p,name+" post",center+new Vector3(side*(width/2+.1f),1.4f,0),new Vector3(.16f,2.8f,.3f),"Timber");
        Box(p,name+" lintel",center+Vector3.up*2.85f,new Vector3(width+.5f,.2f,.35f),"Timber");
    }
}
