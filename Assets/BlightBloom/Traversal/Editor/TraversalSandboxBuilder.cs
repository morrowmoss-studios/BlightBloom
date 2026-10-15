using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;

namespace BlightBloom.Traversal.Editor
{
    public static class TraversalSandboxBuilder
    {
        private const string ScenePath = "Assets/Scenes/TraversalSandbox.unity";

        [MenuItem("BlightBloom/Create Traversal Sandbox")]
        public static void Create()
        {
            if (EditorApplication.isPlayingOrWillChangePlaymode)
            { Debug.LogWarning("Exit Play mode before creating the sandbox."); return; }
            // Never replace an existing scene or touch SampleScene.
            if (File.Exists(ScenePath))
            {
                EditorUtility.DisplayDialog("Traversal Sandbox exists",
                    "Open Assets/Scenes/TraversalSandbox.unity. The existing scene has not been overwritten.", "OK");
                return;
            }
            var actions = AssetDatabase.LoadAssetAtPath<InputActionAsset>("Assets/InputSystem_Actions.inputactions");
            if (actions == null)
            { Debug.LogError("Existing InputSystem_Actions asset was not found. No scene created."); return; }
            if (!AssetDatabase.IsValidFolder("Assets/Scenes")) AssetDatabase.CreateFolder("Assets", "Scenes");
            Scene previous = SceneManager.GetActiveScene();
            Scene sandbox = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
            SceneManager.SetActiveScene(sandbox);
            try
            {
                var ground = GameObject.CreatePrimitive(PrimitiveType.Cube);
                ground.name = "Ground (60m)";
                ground.transform.position = new Vector3(0f, -0.5f, 0f);
                ground.transform.localScale = new Vector3(60f, 1f, 60f);

                var lightObject = new GameObject("Sun");
                var light = lightObject.AddComponent<Light>();
                light.type = LightType.Directional;
                light.intensity = 2f;
                light.shadows = LightShadows.Soft;
                lightObject.transform.rotation = Quaternion.Euler(50f, -30f, 0f);
                RenderSettings.ambientLight = new Color(0.4f, 0.45f, 0.5f);

                var player = new GameObject("Prototype Player");
                player.transform.position = new Vector3(0f, 0.1f, 0f);
                var controller = player.AddComponent<CharacterController>();
                controller.height = 2f;
                controller.radius = 0.4f;
                controller.center = Vector3.up;
                controller.skinWidth = 0.04f;
                controller.stepOffset = 0.3f;
                controller.slopeLimit = 45f;
                controller.minMoveDistance = 0f;
                var input = player.AddComponent<TraversalInput>();
                input.Configure(actions);
                var motor = player.AddComponent<ThirdPersonMotor>();
                var visual = GameObject.CreatePrimitive(PrimitiveType.Capsule);
                visual.name = "Capsule Visual";
                visual.transform.SetParent(player.transform, false);
                visual.transform.localPosition = Vector3.up;
                Object.DestroyImmediate(visual.GetComponent<Collider>());
                // A visible forward marker makes rotation testable on a symmetric capsule.
                var marker = GameObject.CreatePrimitive(PrimitiveType.Cube);
                marker.name = "Forward Marker";
                marker.transform.SetParent(player.transform, false);
                marker.transform.localPosition = new Vector3(0f, 1.4f, 0.45f);
                marker.transform.localScale = new Vector3(0.18f, 0.18f, 0.3f);
                Object.DestroyImmediate(marker.GetComponent<Collider>());

                var cameraObject = new GameObject("Traversal Camera");
                cameraObject.tag = "MainCamera";
                var camera = cameraObject.AddComponent<Camera>();
                camera.nearClipPlane = 0.1f;
                camera.farClipPlane = 300f;
                camera.fieldOfView = 60f;
                cameraObject.AddComponent<UniversalAdditionalCameraData>();
                cameraObject.AddComponent<AudioListener>();
                cameraObject.transform.SetPositionAndRotation(new Vector3(0f, 3.21f, -4.7f), Quaternion.Euler(20f, 0f, 0f));
                var orbit = cameraObject.AddComponent<ThirdPersonOrbitCamera>();
                orbit.Configure(player.transform, input);
                motor.Configure(input, cameraObject.transform);

                // Primitive colliders exercise wall blocking, steps, and walkable slopes.
                CreateBlock("Wall", new Vector3(4f, 1f, 4f), new Vector3(5f, 2f, 1f), Vector3.zero);
                CreateBlock("Low Step", new Vector3(-3f, 0.1f, 3f), new Vector3(3f, 0.2f, 2f), Vector3.zero);
                CreateBlock("Slope", new Vector3(-6f, 0.3f, 6f), new Vector3(3f, 0.5f, 5f), new Vector3(-15f, 0f, 0f));
                if (!EditorSceneManager.SaveScene(sandbox, ScenePath))
                    throw new IOException("Could not save TraversalSandbox.");
                Debug.Log("Created " + ScenePath + ". Open it alone, then press Play. WASD: move, Left Shift: sprint, mouse: orbit, Escape: release cursor, click: recapture.");
            }
            finally
            {
                if (previous.IsValid() && previous.isLoaded) SceneManager.SetActiveScene(previous);
                EditorSceneManager.CloseScene(sandbox, true);
            }
            EditorGUIUtility.PingObject(AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath));
        }

        private static void CreateBlock(string name, Vector3 position, Vector3 scale, Vector3 angles)
        {
            var block = GameObject.CreatePrimitive(PrimitiveType.Cube);
            block.name = name;
            block.transform.SetPositionAndRotation(position, Quaternion.Euler(angles));
            block.transform.localScale = scale;
        }
    }
}
