using UnityEngine;
using UnityEngine.InputSystem;

namespace BlightBloom.Traversal
{
    // Each player owns a private action asset; enabling this never enables combat/UI actions.
    [DefaultExecutionOrder(-200)]
    [DisallowMultipleComponent]
    public sealed class TraversalInput : MonoBehaviour
    {
        [SerializeField] private InputActionAsset actions;
        private InputActionAsset instance;
        private InputAction move, look, sprint;
        public Vector2 Move { get; private set; }
        public Vector2 Look { get; private set; }
        public bool Sprint { get; private set; }
        public bool LookUsesMouse { get; private set; }

        public void Configure(InputActionAsset source) => actions = source;

        private void OnEnable()
        {
            if (actions == null)
            {
                Debug.LogError("Assign the existing InputSystem_Actions asset to TraversalInput.", this);
                enabled = false;
                return;
            }
            instance = Instantiate(actions);
            move = instance.FindAction("Player/Move", true);
            look = instance.FindAction("Player/Look", true);
            sprint = instance.FindAction("Player/Sprint", true);
            move.Enable();
            look.Enable();
            sprint.Enable();
        }

        private void Update()
        {
            if (!Application.isFocused)
            {
                Clear();
                return;
            }
            Move = Vector2.ClampMagnitude(move.ReadValue<Vector2>(), 1f);
            Look = look.ReadValue<Vector2>();
            LookUsesMouse = look.activeControl != null && look.activeControl.device is Pointer;
            Sprint = sprint.IsPressed();
        }

        private void Clear() { Move = Look = Vector2.zero; Sprint = false; }
        private void OnDisable()
        {
            Clear();
            if (instance == null) return;
            instance.Disable();
            Destroy(instance);
            instance = null;
        }
    }
}
