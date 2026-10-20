using UnityEngine;

namespace BlightBloom.Characters
{
    /// <summary>Visual Animator adapter and generic-rig ground contact. No root motion or controller writes.</summary>
    [DefaultExecutionOrder(100)]
    public sealed class PlagueDoctorLocomotion : MonoBehaviour
    {
        [SerializeField] private Animator animator;
        [SerializeField] private Transform leftThigh, leftShin, leftFoot, rightThigh, rightShin, rightFoot;
        [SerializeField, Min(.1f)] private float cycleDistance = 1.067f;
        [SerializeField, Range(0f, 1f)] private float groundContactWeight = 1f;
        private Transform player;
        private CharacterController controller;
        private Vector3 previous;
        private float speed, previousYaw, turn;
        private readonly Contact left = new Contact(), right = new Contact();
        private static readonly int Moving = Animator.StringToHash("Moving");
        private static readonly int Playback = Animator.StringToHash("Playback");
        private static readonly int Turn = Animator.StringToHash("Turn");

        private sealed class Contact { public bool planted; public Vector3 anchor; }
        public float VisualSpeed => speed;
        public void Configure(Animator source, Transform lt, Transform ls, Transform lf, Transform rt, Transform rs, Transform rf)
        { animator = source; leftThigh = lt; leftShin = ls; leftFoot = lf; rightThigh = rt; rightShin = rs; rightFoot = rf; }

        private void OnEnable() { ResetOwner(); }
        private void ResetOwner()
        {
            player = transform.parent;
            controller = player != null ? player.GetComponent<CharacterController>() : null;
            if (player != null) { previous = player.position; previousYaw = player.eulerAngles.y; }
            speed = 0f; left.planted = right.planted = false;
            if (animator != null) animator.applyRootMotion = false;
        }
        private void Update()
        {
            if (player == null) ResetOwner();
            if (player == null || animator == null) return;
            float dt = Mathf.Max(Time.deltaTime, .0001f);
            Vector3 delta = player.position - previous; delta.y = 0;
            previous = player.position;
            float measured = delta.magnitude / dt;
            if (measured > 12f) { measured = 0f; left.planted = right.planted = false; }
            speed = Mathf.Lerp(speed, measured, 1f - Mathf.Exp(-12f * dt));
            turn = Mathf.Lerp(turn, Mathf.Clamp(Mathf.DeltaAngle(previousYaw, player.eulerAngles.y) / dt / 180f, -1f, 1f), 1f - Mathf.Exp(-8f * dt));
            previousYaw = player.eulerAngles.y;
            animator.SetFloat(Moving, speed, .1f, dt);
            animator.SetFloat(Playback, Mathf.Clamp(speed / cycleDistance, .2f, 5.6f));
            animator.SetFloat(Turn, turn);
        }
        private void LateUpdate()
        {
            if (animator == null || player == null || controller == null) return;
            var state = animator.GetCurrentAnimatorStateInfo(0);
            bool walking = state.IsName("Walk") && speed > .18f && !animator.IsInTransition(0);
            float phase = Mathf.Repeat(state.normalizedTime, 1f);
            float blend = controller.isGrounded ? groundContactWeight : 0f;
            Solve(leftThigh, leftShin, leftFoot, left, walking && phase < .6f, blend);
            Solve(rightThigh, rightShin, rightFoot, right, walking && Mathf.Repeat(phase + .5f, 1f) < .6f, blend);
        }
        private void Solve(Transform thigh, Transform shin, Transform foot, Contact contact, bool stance, float weight)
        {
            if (thigh == null || shin == null || foot == null) return;
            Vector3 original = foot.position;
            Quaternion footRotation = foot.rotation;
            bool hitFound = false; RaycastHit best = default;
            foreach (var hit in Physics.RaycastAll(original + Vector3.up * .30f, Vector3.down, .9f, ~(1 << 2), QueryTriggerInteraction.Ignore))
            {
                if (hit.transform == player || hit.transform.IsChildOf(player)) continue;
                if (!hitFound || hit.distance < best.distance) { best = hit; hitFound = true; }
            }
            if (!hitFound || weight <= 0f) { contact.planted = false; return; }
            Vector3 target = original;
            // Native clip ankle is 15cm above its sole. Preserve swing clearance.
            float correction = Mathf.Clamp(best.point.y + .15f - original.y, -.10f, .14f);
            if (!stance && speed > .18f) correction = Mathf.Max(0f, correction);
            target.y += correction;
            if (stance)
            {
                if (!contact.planted) { contact.anchor = target; contact.planted = true; }
                Vector3 offset = contact.anchor - target; offset.y = 0;
                target += Vector3.ClampMagnitude(offset, .12f);
            }
            else contact.planted = false;
            target = Vector3.Lerp(original, target, weight);
            Vector3 hip = thigh.position;
            float upper = Vector3.Distance(hip, shin.position), lower = Vector3.Distance(shin.position, original);
            Vector3 axis = (target - hip).normalized;
            float distance = Mathf.Clamp(Vector3.Distance(hip, target), .03f, upper + lower - .001f);
            Vector3 pole = player.forward - axis * Vector3.Dot(player.forward, axis);
            if (pole.sqrMagnitude < .001f) pole = player.right;
            pole.Normalize();
            float along = (upper * upper - lower * lower + distance * distance) / (2f * distance);
            Vector3 knee = hip + axis * along + pole * Mathf.Sqrt(Mathf.Max(0f, upper * upper - along * along));
            thigh.rotation = Quaternion.FromToRotation(shin.position - hip, knee - hip) * thigh.rotation;
            shin.rotation = Quaternion.FromToRotation(foot.position - shin.position, target - shin.position) * shin.rotation;
            foot.rotation = footRotation;
        }
    }
}
