using UnityEngine;

namespace BlightBloom.Traversal
{
    [RequireComponent(typeof(CharacterController), typeof(TraversalInput))]
    [DisallowMultipleComponent]
    public sealed class ThirdPersonMotor : MonoBehaviour
    {
        [SerializeField] private TraversalInput input;
        [SerializeField] private Transform movementCamera;
        [SerializeField, Min(0f)] private float walkSpeed = 3f;
        [SerializeField, Min(0f)] private float sprintSpeed = 6f;
        [SerializeField, Min(0.01f)] private float rotationSmoothTime = 0.12f;
        [SerializeField, Min(0f)] private float gravity = 25f;
        [SerializeField, Min(0.1f)] private float terminalSpeed = 50f;
        [SerializeField, Min(0.1f)] private float groundStickSpeed = 2f;
        private CharacterController controller;
        private float verticalSpeed, rotationVelocity;
        public bool IsGrounded => controller != null && controller.isGrounded;

        public void Configure(TraversalInput source, Transform cameraTransform)
        { input = source; movementCamera = cameraTransform; }

        private void Awake()
        {
            controller = GetComponent<CharacterController>();
            if (input == null) input = GetComponent<TraversalInput>();
            if (movementCamera == null && Camera.main != null) movementCamera = Camera.main.transform;
            if (movementCamera == null)
            {
                Debug.LogError("Assign a movement camera to ThirdPersonMotor.", this);
                enabled = false;
            }
        }

        private void OnDisable() { verticalSpeed = 0f; rotationVelocity = 0f; }

        private void Update()
        {
            if (!controller.enabled || movementCamera == null) return;
            float dt = Time.deltaTime;
            Vector2 axes = input.Move;
            // Yaw alone keeps movement horizontal even at the camera pitch limits.
            Quaternion yaw = Quaternion.Euler(0f, movementCamera.eulerAngles.y, 0f);
            Vector3 direction = yaw * new Vector3(axes.x, 0f, axes.y);
            if (direction.sqrMagnitude > 0.0001f)
            {
                float angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;
                float heading = Mathf.SmoothDampAngle(transform.eulerAngles.y, angle,
                    ref rotationVelocity, rotationSmoothTime, Mathf.Infinity, dt);
                transform.rotation = Quaternion.Euler(0f, heading, 0f);
            }
            if (controller.isGrounded && verticalSpeed < 0f) verticalSpeed = -groundStickSpeed;
            verticalSpeed = Mathf.Max(verticalSpeed - gravity * dt, -terminalSpeed);
            float speed = input.Sprint ? sprintSpeed : walkSpeed;
            CollisionFlags hits = controller.Move((direction * speed + Vector3.up * verticalSpeed) * dt);
            if ((hits & CollisionFlags.Below) != 0 && verticalSpeed < 0f) verticalSpeed = -groundStickSpeed;
            if ((hits & CollisionFlags.Above) != 0 && verticalSpeed > 0f) verticalSpeed = 0f;
        }
    }
}
