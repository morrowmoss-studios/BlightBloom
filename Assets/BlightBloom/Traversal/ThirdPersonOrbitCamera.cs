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
        [SerializeField, Min(0f), Tooltip("Degrees per pixel; mouse delta must not be multiplied by deltaTime.")]
        private float mouseSensitivity = 0.12f;
        [SerializeField, Min(0f)] private float stickSensitivity = 120f;
        [SerializeField, Range(-85f, 85f)] private float minimumPitch = -25f;
        [SerializeField, Range(-85f, 85f)] private float maximumPitch = 70f;
        [SerializeField, Min(0f)] private float followSmoothTime = 0.08f;
        [SerializeField, Min(0f)] private float orbitSmoothTime = 0.04f;
        [SerializeField] private bool invertY = false;
        [SerializeField] private bool captureCursorOnStart = true;
        private Vector3 pivot, followVelocity;
        private float yaw, pitch = 20f, smoothYaw, smoothPitch, yawVelocity, pitchVelocity;
        private bool captured;
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
            Vector2 delta = input.Look * (input.LookUsesMouse ? mouseSensitivity : stickSensitivity * Time.deltaTime);
            yaw += delta.x;
            pitch = Mathf.Clamp(pitch + delta.y * (invertY ? 1f : -1f), minimumPitch, maximumPitch);
        }

        private void LateUpdate()
        {
            if (target == null || Time.deltaTime <= 0f) return;
            pivot = Vector3.SmoothDamp(pivot, target.position + targetOffset, ref followVelocity, followSmoothTime);
            smoothYaw = Mathf.SmoothDampAngle(smoothYaw, yaw, ref yawVelocity, orbitSmoothTime);
            smoothPitch = Mathf.SmoothDampAngle(smoothPitch, pitch, ref pitchVelocity, orbitSmoothTime);
            PlaceCamera();
        }

        private void PlaceCamera()
        {
            Quaternion rotation = Quaternion.Euler(smoothPitch, smoothYaw, 0f);
            transform.SetPositionAndRotation(pivot - rotation * Vector3.forward * distance, rotation);
        }

        private void OnApplicationFocus(bool focused) { if (!focused) ReleaseCursor(); }
        private void OnDisable() => ReleaseCursor();
        private void OnValidate() { maximumPitch = Mathf.Max(minimumPitch, maximumPitch); }
    }
}
