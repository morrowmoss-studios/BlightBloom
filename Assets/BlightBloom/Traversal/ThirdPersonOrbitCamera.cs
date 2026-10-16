using UnityEngine;
using UnityEngine.InputSystem;

namespace BlightBloom.Traversal
{
    [DefaultExecutionOrder(-100)]
    [RequireComponent(typeof(Camera))]
    [DisallowMultipleComponent]
    public sealed class ThirdPersonOrbitCamera : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private TraversalInput input;
        [SerializeField] private Vector3 targetOffset = new Vector3(0f, 1.5f, 0f);
        [SerializeField, Min(0.5f)] private float distance = 5f;
        [SerializeField, Range(0.01f, 1f), InspectorName("Mouse Sensitivity (degrees/pixel)"),
         Tooltip("Degrees per input pixel, on both axes. 0.3 = 1200 pixels for a full turn. Independent of frame rate.")]
        private float mouseSensitivity = 0.3f;
        [SerializeField, Range(0f, 0.1f), Tooltip("Mouse rotation smoothing in seconds. Zero gives direct, responsive mouse look; follow smoothing is separate.")]
        private float mouseRotationSmoothTime = 0f;
        [SerializeField, Min(0f), Tooltip("Angular speed in degrees per second at full stick deflection.")]
        private float stickSensitivity = 120f;
        [SerializeField, Range(-85f, 85f)] private float minimumPitch = -25f;
        [SerializeField, Range(-85f, 85f)] private float maximumPitch = 70f;
        [SerializeField, Min(0f)] private float followSmoothTime = 0.08f;
        [SerializeField, Min(0f), InspectorName("Stick Rotation Smoothing"), Tooltip("Stick rotation smoothing in seconds. Mouse smoothing is configured separately.")]
        private float orbitSmoothTime = 0.04f;
        [SerializeField] private bool invertY = false;
        [SerializeField] private bool captureCursorOnStart = true;
        private Vector3 pivot, followVelocity;
        private float yaw, pitch = 20f, smoothYaw, smoothPitch, yawVelocity, pitchVelocity;
        private bool lastLookWasMouse = true;
        [Header("Optional environment obstruction")]
        [SerializeField] private bool avoidObstacles;
        [SerializeField, Min(0.05f)] private float collisionRadius = 0.18f;
        [SerializeField] private LayerMask obstructionLayers = ~0;
        private bool captured;

        public void ConfigureObstruction(bool enabled, float followDistance)
        { avoidObstacles = enabled; distance = Mathf.Max(0.5f, followDistance); }
        private CursorLockMode previousLock;
        private bool previousVisible;

        public void Configure(Transform followTarget, TraversalInput source)
        { target = followTarget; input = source; }

        private void Start()
        {
            if (target == null || input == null)
            {
                Debug.LogError("Assign a target and TraversalInput to the orbit camera.", this);
                enabled = false;
                return;
            }
            pivot = target.position + targetOffset;
            yaw = smoothYaw = target.eulerAngles.y;
            smoothPitch = pitch;
            if (captureCursorOnStart) CaptureCursor();
            PlaceCamera();
        }

        private void CaptureCursor()
        {
            if (captured) return;
            previousLock = Cursor.lockState;
            previousVisible = Cursor.visible;
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
            captured = true;
        }

        private void ReleaseCursor()
        {
            if (!captured) return;
            Cursor.lockState = previousLock;
            Cursor.visible = previousVisible;
            captured = false;
        }

        private void Update()
        {
            if (!Application.isFocused) return;
            if (Keyboard.current != null && Keyboard.current.escapeKey.wasPressedThisFrame)
            { ReleaseCursor(); return; }
            if (!captured && Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame)
            { CaptureCursor(); return; }
            if (!captured || Cursor.lockState != CursorLockMode.Locked || Time.deltaTime <= 0f) return;
            ApplyLook(input.Look, input.LookUsesMouse, Time.deltaTime);
        }

        private void ApplyLook(Vector2 look, bool usesMouse, float deltaTime)
        {
            if (look.sqrMagnitude > 0f) lastLookWasMouse = usesMouse;
            // Mouse input is accumulated displacement; stick input is an angular rate.
            Vector2 delta = look * (usesMouse ? mouseSensitivity : stickSensitivity * deltaTime);
            yaw += delta.x;
            pitch = Mathf.Clamp(pitch + delta.y * (invertY ? 1f : -1f), minimumPitch, maximumPitch);
        }

        private void LateUpdate()
        {
            if (target == null || Time.deltaTime <= 0f) return;
            pivot = Vector3.SmoothDamp(pivot, target.position + targetOffset, ref followVelocity, followSmoothTime);
            float rotationTime = lastLookWasMouse ? mouseRotationSmoothTime : orbitSmoothTime;
            if (rotationTime <= 0f)
            {
                smoothYaw = yaw;
                smoothPitch = pitch;
                yawVelocity = pitchVelocity = 0f;
            }
            else
            {
                smoothYaw = Mathf.SmoothDampAngle(smoothYaw, yaw, ref yawVelocity, rotationTime);
                smoothPitch = Mathf.SmoothDampAngle(smoothPitch, pitch, ref pitchVelocity, rotationTime);
            }
            PlaceCamera();
        }

        private void PlaceCamera()
        {
            Quaternion rotation = Quaternion.Euler(smoothPitch, smoothYaw, 0f);
            Vector3 backward = -(rotation * Vector3.forward);
            float safeDistance = distance;
            if (avoidObstacles)
            {
                // Ignore the player hierarchy without relying on project-specific layers.
                foreach (RaycastHit hit in Physics.SphereCastAll(pivot, collisionRadius, backward,
                    distance, obstructionLayers, QueryTriggerInteraction.Ignore))
                {
                    if (hit.transform == target || hit.transform.IsChildOf(target)) continue;
                    safeDistance = Mathf.Min(safeDistance, Mathf.Max(0f, hit.distance - 0.05f));
                }
            }
            transform.SetPositionAndRotation(pivot + backward * safeDistance, rotation);
        }

        private void OnApplicationFocus(bool focused) { if (!focused) ReleaseCursor(); }
        private void OnDisable() => ReleaseCursor();
        private void OnValidate() { maximumPitch = Mathf.Max(minimumPitch, maximumPitch); }
    }
}
