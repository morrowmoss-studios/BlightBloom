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
        private Vector3 leftLegRest, rightLegRest;
        private Vector3[] leftFootVertices, rightFootVertices;
        private CharacterController controller;

        public void Configure(Transform root, Transform armL, Transform armR, Transform legL,
            Transform legR, Transform coatL, Transform coatR)
        { body = root; leftArm = armL; rightArm = armR; leftLeg = legL; rightLeg = legR; leftCoat = coatL; rightCoat = coatR; }

        private void OnEnable()
        {
            player = transform.parent;
            if (player != null) previousPosition = player.position;
            if (leftLeg != null) leftLegRest = leftLeg.localPosition;
            if (rightLeg != null) rightLegRest = rightLeg.localPosition;
            leftFootVertices = LegVertices(leftLeg);
            rightFootVertices = LegVertices(rightLeg);
            controller = GetComponentInParent<CharacterController>();
        }

        private static Vector3[] LegVertices(Transform joint)
        {
            var mesh = joint != null ? joint.GetComponentInChildren<MeshFilter>() : null;
            if (mesh == null) return null;
            var vertices = mesh.sharedMesh.vertices;
            for (int i = 0; i < vertices.Length; i++)
                vertices[i] = joint.InverseTransformPoint(mesh.transform.TransformPoint(vertices[i]));
            return vertices;
        }

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
            // One full left/right cycle per 1.5 metres, independent of frame rate.
            phase += dt * speed * (Mathf.PI * 2f / 1.5f);
            float stride = Mathf.Sin(phase) * strideDegrees * blend;
            Pose(leftLeg, stride); Pose(rightLeg, -stride);
            Pose(leftArm, -stride * .85f); Pose(rightArm, stride * .85f);
            Pose(leftCoat, stride * .22f); Pose(rightCoat, -stride * .22f);
            body.localPosition = Vector3.up * (.003f * Mathf.Sin(Time.time * 1.7f) * (1f - blend));
            GroundLeg(leftLeg, leftLegRest, leftFootVertices, Mathf.Max(0f, Mathf.Cos(phase)) * .065f * blend);
            GroundLeg(rightLeg, rightLegRest, rightFootVertices, Mathf.Max(0f, -Mathf.Cos(phase)) * .065f * blend);
        }

        private void GroundLeg(Transform joint, Vector3 rest, Vector3[] vertices, float lift)
        {
            if (joint == null || vertices == null) return;
            joint.localPosition = rest;
            if (controller == null || !controller.isGrounded) return;
            float lowest = float.PositiveInfinity;
            Vector3 foot = joint.position;
            foreach (var vertex in vertices)
            {
                Vector3 point = joint.TransformPoint(vertex);
                if (point.y < lowest) { lowest = point.y; foot = point; }
            }
            // Visual-only boot contact. Ignore the player layer and all triggers.
            if (Physics.Raycast(foot + Vector3.up * .4f, Vector3.down, out var hit,
                .9f, ~(1 << 2), QueryTriggerInteraction.Ignore))
            {
                float offset = Mathf.Clamp(hit.point.y + .008f + lift - lowest, -.18f, .18f);
                joint.position += Vector3.up * offset;
            }
        }

        private static void Pose(Transform joint, float angle)
        { if (joint != null) joint.localRotation = Quaternion.Euler(angle, 0f, 0f); }
    }
}
