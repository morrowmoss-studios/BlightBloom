using UnityEngine;
using UnityEngine.InputSystem;

namespace BlightBloom.Prototypes
{
    // Scene-local fixture: reuse the existing binding without enabling unrelated player actions.
    public sealed class BlockoutDoor : MonoBehaviour
    {
        public Transform player;
        public InputActionAsset interactionActions;
        public bool IsOpen { get; private set; }
        public bool IsBlocked { get; private set; }
        public float closedAngle;
        public float openAngle = 105f;
        public float interactionDistance = 3.2f;
        private float angle;
        private InputAction interact;
        private BoxCollider leaf;
        private CharacterController controller;

        private void Awake()
        {
            angle = closedAngle;
            leaf = GetComponentInChildren<BoxCollider>();
            controller = player != null ? player.GetComponent<CharacterController>() : null;
        }

        private void OnEnable()
        {
            if (interactionActions == null)
            {
                Debug.LogError("Assign the existing Player/Interact action asset to this blockout door.", this);
                return;
            }
            // Shared Interact uses Hold. This temporary door explicitly uses a single press,
            // copying its existing bindings without modifying the source asset.
            var source = interactionActions.FindAction("Player/Interact", true);
            interact = new InputAction("BlockoutDoorInteract", InputActionType.Button, interactions: "Press");
            foreach (var binding in source.bindings) interact.AddBinding(binding);
            interact.performed += OnInteract;
            interact.Enable();
        }

        private void OnDisable()
        {
            if (interact == null) return;
            interact.performed -= OnInteract;
            interact.Dispose();
            interact = null;
        }

        private bool InRange()
        {
            if (player == null) return false;
            Vector3 delta = player.position - transform.position;
            return new Vector2(delta.x, delta.z).magnitude <= interactionDistance &&
                Mathf.Abs(delta.y) < 2f;
        }

        private void OnInteract(InputAction.CallbackContext context)
        {
            if (InRange()) SetOpen(!IsOpen);
        }

        private void Update()
        {
            float next = Mathf.MoveTowardsAngle(angle, IsOpen ? openAngle : closedAngle, 150f * Time.deltaTime);
            IsBlocked = SweepHitsPlayer(angle, next);
            if (IsBlocked) return; // Keep the request: movement resumes when the player steps clear.
            angle = next;
            transform.localRotation = Quaternion.Euler(0f, angle, 0f);
        }

        private bool SweepHitsPlayer(float from, float to)
        {
            if (leaf == null || controller == null || !controller.enabled ||
                Mathf.Abs(Mathf.DeltaAngle(from, to)) < .001f) return false;
            int samples = Mathf.Max(1, Mathf.CeilToInt(Mathf.Abs(Mathf.DeltaAngle(from, to)) / 2f));
            for (int i = 1; i <= samples; i++)
            {
                Quaternion rotation = (transform.parent != null ? transform.parent.rotation : Quaternion.identity) *
                    Quaternion.Euler(0, Mathf.LerpAngle(from, to, (float)i / samples), 0);
                Vector3 position = transform.position + rotation * Vector3.Scale(transform.lossyScale, leaf.transform.localPosition);
                // The leaf stays upright: the closest capsule-axis point has its Y clamped
                // to the box centre. Query the box at the proposed pose, without moving it.
                Vector3 centre = controller.transform.TransformPoint(controller.center);
                Vector3 axis = controller.transform.up;
                float halfSegment = Mathf.Max(0, controller.height * .5f - controller.radius);
                Vector3 point = centre + axis * Mathf.Clamp(Vector3.Dot(position - centre, axis), -halfSegment, halfSegment);
                Vector3 nearest = Physics.ClosestPoint(point, leaf, position, rotation * leaf.transform.localRotation);
                float safeRadius = controller.radius + .02f;
                if ((point - nearest).sqrMagnitude < safeRadius * safeRadius) return true;
            }
            return false;
        }

        public bool SetOpen(bool open, bool immediately = false)
        {
            // Immediate placement is for setup/probes; live input always follows the checked animation.
            if (immediately && SweepHitsPlayer(angle, open ? openAngle : closedAngle)) return false;
            IsOpen = open;
            if (immediately)
            {
                angle = open ? openAngle : closedAngle;
                transform.localRotation = Quaternion.Euler(0, angle, 0);
                IsBlocked = false;
            }
            return true;
        }

        private void OnGUI()
        {
            if (!InRange()) return;
            GUI.Label(new Rect(18,18,760,32), IsBlocked
                ? "Door swing blocked — step back or to the side; the door will resume. E: reverse."
                : "E / gamepad north: open or close front door (swings outward).");
        }
    }
}
