using System.IO;
using BlightBloom.Traversal;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;

namespace BlightBloom.Locations.Editor
{
    /// <summary>All dimensions are metres. Footprint: X -8..8, Z -6..8; upstairs Y 3.6.</summary>
    public static class ApothecaryBlockoutBuilder
    {
        public const string ScenePath = "Assets/Scenes/UncleRobertsApothecary.unity";
        private const float Storey = 3.6f;

        [MenuItem("BlightBloom/Create Uncle Robert's Apothecary")]
        public static void Create()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode) return;
            if (File.Exists(ScenePath))
            {
                EditorUtility.DisplayDialog("Scene already exists", "The existing apothecary was preserved. Open it from Assets/Scenes.", "OK");
                return;
            }
            var actions = AssetDatabase.LoadAssetAtPath<InputActionAsset>("Assets/InputSystem_Actions.inputactions");
            if (actions == null) { Debug.LogError("Existing input actions missing; no scene created."); return; }
            if (!AssetDatabase.IsValidFolder("Assets/Scenes")) AssetDatabase.CreateFolder("Assets", "Scenes");
            Scene previous = SceneManager.GetActiveScene();
            Scene scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            SceneManager.SetActiveScene(scene);
            try
            {
                Transform site = Group("01 Exterior and garden");
                Box(site, "Village ground", new Vector3(0,-0.4f,3), new Vector3(44,0.6f,44));
                Box(site, "Front approach", new Vector3(0,-0.07f,-10), new Vector3(4,0.1f,8));
                Box(site, "Back garden path", new Vector3(2,-0.07f,12), new Vector3(3,0.1f,8));
                for (int row=0; row<2; row++)
                    for (int col=0; col<2; col++)
                    {
                        var bed = Group("Herb bed " + (row*2+col+1), site);
                        float x=-5+col*4, z=11+row*4;
                        Box(bed,"Raised bed",new Vector3(x,0.15f,z),new Vector3(2.8f,0.3f,2.5f));
                        for(int herb=0;herb<3;herb++)
                            Box(bed,"Herb placeholder",new Vector3(x-0.8f+herb*0.8f,0.45f,z),new Vector3(0.35f,0.3f,1.5f));
                    }
                Box(site,"Garden west boundary",new Vector3(-8,0.5f,12.5f),new Vector3(0.2f,1,9));
                Box(site,"Garden rear boundary",new Vector3(-3,0.5f,17),new Vector3(10,1,0.2f));
                Box(site,"Garden east boundary",new Vector3(7,0.5f,12.5f),new Vector3(0.2f,1,9));

                Transform shell=Group("02 Modular shell - open roof for iteration");
                Box(shell,"Ground floor",new Vector3(0,-0.1f,1),new Vector3(16,0.2f,14));
                // Upper floor leaves a real 3m x 9m stairwell opening.
                Box(shell,"Upper floor west",new Vector3(-1.5f,3.5f,1),new Vector3(13,0.2f,14));
                Box(shell,"Upper floor front east",new Vector3(6.5f,3.5f,-5),new Vector3(3,0.2f,2));
                Box(shell,"Upper landing",new Vector3(6.5f,3.5f,6.5f),new Vector3(3,0.2f,3));
                for(int level=0;level<2;level++)
                {
                    float y=level*Storey;
                    var walls=Group(level==0 ? "Ground exterior walls" : "Upper exterior walls",shell);
                    WallX(walls,"Front wall",-8,8,-6,y,0,2.4f);
                    WallX(walls,"Rear garden door",-8,8,8,y,2,2.4f);
                    Box(walls,"West wall",new Vector3(-8,y+1.8f,1),new Vector3(0.2f,3.6f,14));
                    Box(walls,"East wall",new Vector3(8,y+1.8f,1),new Vector3(0.2f,3.6f,14));
                }
                // Upper front/rear openings are windows with solid waist-high sills.
                Box(shell,"Front window sill",new Vector3(0,4.15f,-6),new Vector3(2.4f,1.1f,0.2f));
                Box(shell,"Rear window sill",new Vector3(2,4.15f,8),new Vector3(2.4f,1.1f,0.2f));
                Box(shell,"Shop sign block",new Vector3(-3,3.1f,-6.3f),new Vector3(3,0.5f,0.25f));

                Transform down=Group("03 Ground floor rooms");
                var shop=Group("Shop and front entry",down);
                Box(shop,"Dispensing counter",new Vector3(-4,0.5f,-2.7f),new Vector3(4,1,0.8f));
                Box(shop,"Shop shelf",new Vector3(-7.35f,1,-3.5f),new Vector3(0.7f,2,3));
                // Two wide thresholds connect the public shop to treatment and preparation.
                WallX(down,"Shop to treatment threshold",-8,-0.5f,0,0,-4.3f,2.2f);
                WallX(down,"Shop to preparation threshold",-0.5f,5,0,0,2.2f,2.2f);
                WallZ(down,"Treatment preparation divider",0,4,-0.5f,0,2,2.2f);
                WallX(down,"Treatment to rear storage",-8,-0.5f,4,0,-4.3f,2.2f);
                WallX(down,"Preparation to rear passage",-0.5f,5,4,0,2.2f,2.2f);
                var treatment=Group("Medical examination and treatment",down);
                Box(treatment,"Examination couch",new Vector3(-5,0.4f,2),new Vector3(2.2f,0.8f,0.9f));
                Box(treatment,"Wash stand",new Vector3(-7.25f,0.5f,2),new Vector3(0.8f,1,1));
                var prep=Group("Medicine preparation",down);
                Box(prep,"Preparation bench",new Vector3(4.2f,0.5f,2),new Vector3(0.8f,1,2.5f));
                Box(prep,"Mortar placeholder",new Vector3(4.2f,1.15f,2),new Vector3(0.35f,0.3f,0.35f));
                var storage=Group("Rear storage and garden access",down);
                Box(storage,"Storage shelves",new Vector3(-6.5f,1,6.7f),new Vector3(2,2,0.8f));
                Box(storage,"Crates",new Vector3(-2,0.5f,6.5f),new Vector3(1.2f,1,1.2f));

                Transform stairs=Group("04 Stairs - 18 rises of 0.2m");
                for(int i=0;i<18;i++)
                {
                    float h=(i+1)*0.2f;
                    Box(stairs,"Tread " +(i+1),new Vector3(6.5f,h/2,-3.75f+i*0.5f),new Vector3(2.8f,h,0.5f));
                }
                // Ground-level divider prevents accidental side entry to the solid stair mass.
                Box(stairs,"Stair side partition",new Vector3(5,1.8f,0.5f),new Vector3(0.2f,3.6f,9));
                Box(stairs,"Upper stairwell west guard",new Vector3(5,4.2f,0.5f),new Vector3(0.15f,1.2f,9));
                Box(stairs,"Upper stairwell front guard",new Vector3(6.5f,4.2f,-4),new Vector3(3,1.2f,0.15f));

                Transform up=Group("05 Private upper rooms");
                WallZ(up,"Bedroom east wall",-6,1,-1,Storey,-2,2.2f);
                WallZ(up,"Study east wall",1,8,-1,Storey,4,2.2f);
                WallX(up,"Bedroom study divider",-8,-1,1,Storey,-4,2.2f);
                var bedRoom=Group("Bedroom",up);
                Box(bedRoom,"Bed",new Vector3(-5,4,-3.5f),new Vector3(2.1f,0.8f,3));
                Box(bedRoom,"Personal chest",new Vector3(-7,4,-0.5f),new Vector3(1,0.8f,0.7f));
                var study=Group("Private library and study",up);
                Box(study,"Writing desk",new Vector3(-4.5f,4.1f,5.5f),new Vector3(2.4f,1,1));
                Box(study,"Bookcase west",new Vector3(-7.4f,4.7f,4.5f),new Vector3(0.7f,2.2f,4));
                Box(study,"Bookcase rear",new Vector3(-4.7f,4.7f,7.4f),new Vector3(3,2.2f,0.7f));
                var living=Group("Living space and landing passage",up);
                Box(living,"Table",new Vector3(1.8f,4.1f,-3.5f),new Vector3(1.7f,1,1.2f));
                Box(living,"Bench",new Vector3(1.8f,3.9f,-4.8f),new Vector3(1.7f,0.6f,0.5f));
                CreateTraversal(actions);
                LightScene();
                if(!EditorSceneManager.SaveScene(scene,ScenePath)) throw new IOException("Scene save failed.");
                Debug.Log("Created "+ScenePath+". Open it alone and press Play. Front entry faces -Z; garden is +Z; stairs are east (+X).");
            }
            finally
            {
                if(previous.IsValid() && previous.isLoaded) SceneManager.SetActiveScene(previous);
                EditorSceneManager.CloseScene(scene,true);
            }
            EditorGUIUtility.PingObject(AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath));
        }

        private static Transform Group(string name, Transform parent=null)
        {
            var go=new GameObject(name);
            go.transform.SetParent(parent,false);
            return go.transform;
        }
        private static void Box(Transform parent,string name,Vector3 position,Vector3 scale)
        {
            var go=GameObject.CreatePrimitive(PrimitiveType.Cube);
            go.name=name; go.transform.SetParent(parent,false);
            go.transform.localPosition=position; go.transform.localScale=scale;
        }
        // Split walls around real open thresholds; lintel leaves 2.8m clear height.
        private static void WallX(Transform p,string n,float left,float right,float z,float floor,float door,float width)
        {
            float a=door-width/2,b=door+width/2;
            Box(p,n+" left",new Vector3((left+a)/2,floor+1.8f,z),new Vector3(a-left,3.6f,0.2f));
            Box(p,n+" right",new Vector3((b+right)/2,floor+1.8f,z),new Vector3(right-b,3.6f,0.2f));
            Box(p,n+" lintel",new Vector3(door,floor+3.2f,z),new Vector3(width,0.8f,0.2f));
        }
        private static void WallZ(Transform p,string n,float front,float rear,float x,float floor,float door,float width)
        {
            float a=door-width/2,b=door+width/2;
            Box(p,n+" front",new Vector3(x,floor+1.8f,(front+a)/2),new Vector3(0.2f,3.6f,a-front));
            Box(p,n+" rear",new Vector3(x,floor+1.8f,(b+rear)/2),new Vector3(0.2f,3.6f,rear-b));
            Box(p,n+" lintel",new Vector3(x,floor+3.2f,door),new Vector3(0.2f,0.8f,width));
        }
        private static void CreateTraversal(InputActionAsset actions)
        {
            Transform root=Group("06 Traversal and spawn");
            var spawn=Group("Front entrance spawn",root); spawn.position=new Vector3(0,0.1f,-10);
            var player=new GameObject("Prototype Player"); player.transform.SetParent(root,false); player.transform.position=spawn.position;
            var cc=player.AddComponent<CharacterController>(); cc.height=2; cc.radius=0.4f; cc.center=Vector3.up;
            cc.skinWidth=0.04f; cc.stepOffset=0.3f; cc.slopeLimit=45; cc.minMoveDistance=0;
            var input=player.AddComponent<TraversalInput>(); input.Configure(actions);
            var motor=player.AddComponent<ThirdPersonMotor>();
            var capsule=GameObject.CreatePrimitive(PrimitiveType.Capsule); capsule.name="Capsule visual";
            capsule.transform.SetParent(player.transform,false); capsule.transform.localPosition=Vector3.up;
            Object.DestroyImmediate(capsule.GetComponent<Collider>());
            var cameraObject=new GameObject("Apothecary Camera"); cameraObject.transform.SetParent(root,false); cameraObject.tag="MainCamera";
            var cam=cameraObject.AddComponent<Camera>(); cam.nearClipPlane=0.05f; cam.farClipPlane=200; cam.fieldOfView=65;
            cameraObject.AddComponent<UniversalAdditionalCameraData>(); cameraObject.AddComponent<AudioListener>();
            var orbit=cameraObject.AddComponent<ThirdPersonOrbitCamera>(); orbit.Configure(player.transform,input); orbit.ConfigureObstruction(true,3);
            cameraObject.transform.SetPositionAndRotation(spawn.position+new Vector3(0,2.5f,-3),Quaternion.Euler(20,0,0));
            motor.Configure(input,cameraObject.transform);
        }
        private static void LightScene()
        {
            Transform root=Group("07 Blockout lighting");
            var sun=new GameObject("Sun"); sun.transform.SetParent(root,false);
            var light=sun.AddComponent<Light>(); light.type=LightType.Directional; light.intensity=1.5f; light.shadows=LightShadows.Soft;
            sun.transform.rotation=Quaternion.Euler(50,-35,0);
            for(int level=0;level<2;level++)
                for(int row=0;row<2;row++)
                {
                    var lamp=new GameObject("Interior work light"); lamp.transform.SetParent(root,false);
                    lamp.transform.position=new Vector3(-2,level*Storey+2.8f,-2+row*7);
                    var fill=lamp.AddComponent<Light>(); fill.type=LightType.Point; fill.range=10; fill.intensity=3;
                }
        }
    }
}
