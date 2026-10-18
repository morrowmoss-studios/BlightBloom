using UnityEngine;
using UnityEngine.InputSystem;
using BlightBloom.Traversal;

namespace BlightBloom.Prototypes
{
    [DefaultExecutionOrder(-100)]
    [RequireComponent(typeof(Camera))]
    [DisallowMultipleComponent]
    public sealed class Production02StairOrbitCamera : MonoBehaviour
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
        [Header("Production02 stairwell only")]
        [SerializeField] private Bounds stairZone = new Bounds(new Vector3(-0.4f, 2f, 6.25f), new Vector3(3.8f, 5f, 6.5f));
        [SerializeField, Min(1f)] private float usefulDistance = 3.0f;
        [SerializeField, Range(60f, 240f)] private float assistDegreesPerSecond = 240f;
        private float assistYaw, assistPitch, nextProbe;
        private Vector3 lastTargetPosition, targetVelocity;
        public int EmergencyCorrections { get; private set; }
        private bool assistActive;
        private readonly RaycastHit[] hits = new RaycastHit[64];
        public float CurrentDistance { get; private set; }
        public bool StairAssistActive { get; private set; }
        // A scene-local camera variant: original input/cursor/follow behavior is retained below.
        // Layer 2 contains only the new invisible player-safety guards. Real timber and walls
        // remain camera obstacles; the camera does not treat empty balustrade air as a wall.
        private bool Blocks(Collider c) => c.gameObject.layer != 2 && c.transform != target && !c.transform.IsChildOf(target);
        private float Clearance(float heading, float elevation, Vector3? from = null)
        {
            var back = -(Quaternion.Euler(elevation, heading, 0f) * Vector3.forward);
            float clear = distance;
            int count = Physics.SphereCastNonAlloc(from ?? pivot, collisionRadius, back, hits, distance,
                obstructionLayers, QueryTriggerInteraction.Ignore);
            for (int i = 0; i < count; i++) if (Blocks(hits[i].collider))
                clear = Mathf.Min(clear, Mathf.Max(0f, hits[i].distance - 0.05f));
            return clear;
        }
        private float PlanningClearance(float heading, float elevation, Vector3? from = null)
        {
            Vector3 origin=from ?? pivot;
            float clear=Clearance(heading,elevation,origin);
            Vector3 at=origin-Quaternion.Euler(elevation,heading,0)*Vector3.forward*clear;
            // The front landing floor divides the lower lobby from the living room above.
            // While downstairs, avoid parking above that floor and then having to cross
            // the slab during descent. This is a planning preference, never a new collider
            // or an instruction to force the final boom inward.
            float footHeight=origin.y-targetOffset.y;
            if(footHeight<2.05f && at.z<4.8f && at.y>3.05f)
                return Mathf.Min(clear,1f);
            return clear;
        }
        private int VisibleBodyPoints(Vector3 from)
        {
            int visible = 0;
            for (int point = 0; point < 4; point++)
            {
                Vector3 to = target.position + Vector3.up * (point == 0 ? 1.8f : point == 1 ? 1.2f : point == 2 ? .65f : .25f);
                Vector3 delta = to - from;
                int count = Physics.RaycastNonAlloc(from, delta.normalized, hits, Mathf.Max(0, delta.magnitude-.04f),
                    obstructionLayers, QueryTriggerInteraction.Ignore);
                bool blocked = false;
                for (int i=0; i<count; i++) if (Blocks(hits[i].collider)) { blocked=true; break; }
                if (!blocked) visible++;
            }
            return visible;
        }
        private void AssistStairOrbit()
        {
            StairAssistActive = stairZone.Contains(target.position);
            if (!StairAssistActive) { assistActive=false; return; }
            float clear = PlanningClearance(smoothYaw, smoothPitch);
            Vector3 at = pivot - Quaternion.Euler(smoothPitch,smoothYaw,0) * Vector3.forward * clear;
            int visible = VisibleBodyPoints(at);
            if (Time.unscaledTime >= nextProbe)
            {
                nextProbe = Time.unscaledTime + .05f;
                if (clear < usefulDistance || PlanningClearance(smoothYaw,smoothPitch,pivot+targetVelocity*.35f) < usefulDistance || visible < 3)
                {
                    float best = Mathf.Min(Mathf.Min(clear,PlanningClearance(smoothYaw,smoothPitch,pivot+targetVelocity*.35f)),2.6f) + .65f*visible;
                    float bestYaw=smoothYaw, bestPitch=smoothPitch;
                    for (int offset = -180; offset <= 180; offset += 30)
                    for (int p = 0; p < 4; p++)
                    {
                        float elevation = p==0 ? Mathf.Clamp(smoothPitch,0,30) : p==1 ? 0 : p==2 ? 10 : 25;
                        float heading = smoothYaw + offset;
                        float space = PlanningClearance(heading,elevation);
                        Vector3 candidate = pivot - Quaternion.Euler(elevation,heading,0)*Vector3.forward*space;
                        int seen = VisibleBodyPoints(candidate);
                        float score = Mathf.Min(Mathf.Min(space,PlanningClearance(heading,elevation,pivot+targetVelocity*.35f)),2.6f) + .65f*seen - .0055f*Mathf.Abs(offset)
                            - .008f*Mathf.Abs(elevation-smoothPitch);
                        if (score > best + .18f) { best=score; bestYaw=heading; bestPitch=elevation; }
                    }
                    if (Mathf.Abs(Mathf.DeltaAngle(bestYaw,smoothYaw))>.5f || Mathf.Abs(bestPitch-smoothPitch)>.5f)
                    { assistYaw=bestYaw; assistPitch=bestPitch; assistActive=true; }
                }
            }
            if (!assistActive) return;
            yaw = smoothYaw = Mathf.MoveTowardsAngle(smoothYaw,assistYaw,assistDegreesPerSecond*Time.deltaTime);
            pitch = smoothPitch = Mathf.MoveTowards(smoothPitch,assistPitch,60f*Time.deltaTime);
            if (Mathf.Abs(Mathf.DeltaAngle(smoothYaw,assistYaw))<.1f && Mathf.Abs(smoothPitch-assistPitch)<.1f)
                assistActive=false;
        }

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
            lastTargetPosition = target.position;
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
            if (look.sqrMagnitude > 0f)
            {
                lastLookWasMouse = usesMouse;
                nextProbe = 0f;
            }
            // Mouse input is accumulated displacement; stick input is an angular rate.
            Vector2 delta = look * (usesMouse ? mouseSensitivity : stickSensitivity * deltaTime);
            yaw += delta.x;
            if (assistActive) { assistYaw += delta.x; assistPitch = Mathf.Clamp(assistPitch + delta.y * (invertY ? 1f : -1f), minimumPitch, maximumPitch); }
            pitch = Mathf.Clamp(pitch + delta.y * (invertY ? 1f : -1f), minimumPitch, maximumPitch);
        }

        private void LateUpdate()
        {
            if (target == null || Time.deltaTime <= 0f) return;
            targetVelocity = Vector3.ClampMagnitude((target.position-lastTargetPosition)/Time.deltaTime,6f);
            lastTargetPosition=target.position;
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
            if (avoidObstacles) AssistStairOrbit();
            Quaternion rotation = Quaternion.Euler(smoothPitch, smoothYaw, 0f);
            Vector3 backward = -(rotation * Vector3.forward);
            float safeDistance = distance;
            if (avoidObstacles)
            {
                // Ignore the player hierarchy without relying on project-specific layers.
                foreach (RaycastHit hit in Physics.SphereCastAll(pivot, collisionRadius, backward,
                    distance, obstructionLayers, QueryTriggerInteraction.Ignore))
                {
                    if (!Blocks(hit.collider)) continue;
                    safeDistance = Mathf.Min(safeDistance, Mathf.Max(0f, hit.distance - 0.05f));
                }
            }
            // Emergency escape for abrupt user-orbit changes; normal movement should be handled
            // predictively above, before the boom collapses. Never push through an obstacle.
            if (StairAssistActive && avoidObstacles && safeDistance < 1.65f)
            {
                float best=-1000f, heading=smoothYaw, elevation=smoothPitch, bestDistance=safeDistance;
                for(int offset=-180;offset<=180;offset+=15)
                for(int p=0;p<4;p++)
                {
                    float candidatePitch=p*10f;
                    float candidateYaw=smoothYaw+offset;
                    float space=Clearance(candidateYaw,candidatePitch);
                    if(PlanningClearance(candidateYaw,candidatePitch)<1.8f)continue;
                    if(space<1.8f)continue;
                    Vector3 at=pivot-Quaternion.Euler(candidatePitch,candidateYaw,0)*Vector3.forward*space;
                    int seen=VisibleBodyPoints(at);
                    float score=Mathf.Min(space,2.6f)+.65f*seen-.006f*Mathf.Abs(offset)-.008f*Mathf.Abs(candidatePitch-smoothPitch);
                    if(score>best){best=score;heading=candidateYaw;elevation=candidatePitch;bestDistance=space;}
                }
                if(best>-999f)
                {
                    yaw=smoothYaw=heading;pitch=smoothPitch=elevation;assistActive=false;
                    rotation=Quaternion.Euler(elevation,heading,0);backward=-(rotation*Vector3.forward);
                    safeDistance=bestDistance;EmergencyCorrections++;
                }
            }
            CurrentDistance = safeDistance;
            transform.SetPositionAndRotation(pivot + backward * safeDistance, rotation);
        }

        private void OnApplicationFocus(bool focused) { if (!focused) ReleaseCursor(); }
        private void OnDisable() => ReleaseCursor();
        private void OnValidate() { maximumPitch = Mathf.Max(minimumPitch, maximumPitch); }
    }
}
