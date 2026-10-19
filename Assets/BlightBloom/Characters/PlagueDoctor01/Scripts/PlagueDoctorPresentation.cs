using UnityEngine;

namespace BlightBloom.Characters
{
    /// <summary>Visual-only first-pass articulation. Never moves the controller or camera.</summary>
    [DisallowMultipleComponent]
    public sealed class PlagueDoctorPresentation : MonoBehaviour
    {
        [SerializeField] private Transform body, leftArm, rightArm, leftLeg, rightLeg, leftCoat, rightCoat;
        [SerializeField, Range(0f, 35f)] private float strideDegrees = 24f;
        private Transform player;
        private Vector3 previousPosition;
        private float phase, blend, speed;

        public void Configure(Transform root, Transform armL, Transform armR, Transform legL,
            Transform legR, Transform coatL, Transform coatR)
        { body = root; leftArm = armL; rightArm = armR; leftLeg = legL; rightLeg = legR; leftCoat = coatL; rightCoat = coatR; }

        private void OnEnable()
        { player = transform.parent; if (player != null) previousPosition = player.position; }

        private void LateUpdate()
        {
            if (player == null)
            {
                player = transform.parent;
                if (player != null) previousPosition = player.position;
            }
            if (player == null || body == null) return;
            float dt = Mathf.Max(Time.deltaTime, .0001f);
            Vector3 delta = player.position - previousPosition; delta.y = 0f;
            previousPosition = player.position;
            float measured = delta.magnitude / dt;
            // Teleports are placement, not locomotion.
            if (measured > 12f) measured = 0f;
            speed = Mathf.Lerp(speed, measured, 1f - Mathf.Exp(-12f * dt));
            blend = Mathf.Lerp(blend, Mathf.Clamp01(speed / 1.2f), 1f - Mathf.Exp(-10f * dt));
            phase += dt * Mathf.Lerp(2f, 9f, Mathf.Clamp01(speed / 3f));
            float stride = Mathf.Sin(phase) * strideDegrees * blend;
            Pose(leftLeg, stride); Pose(rightLeg, -stride);
            Pose(leftArm, -stride * .65f); Pose(rightArm, stride * .65f);
            Pose(leftCoat, stride * .12f); Pose(rightCoat, -stride * .12f);
            body.localPosition = Vector3.up * (.005f * Mathf.Sin(Time.time * 1.7f) * (1f - blend)
                + .012f * (1f - Mathf.Cos(phase * 2f)) * blend);
        }

        private static void Pose(Transform joint, float angle)
        { if (joint != null) joint.localRotation = Quaternion.Euler(angle, 0f, 0f); }
    }
}
