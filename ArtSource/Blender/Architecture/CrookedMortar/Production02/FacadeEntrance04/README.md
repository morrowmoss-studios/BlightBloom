# Production02 facade / entrance correction — 2026-10-18

Status: saved candidate for **manual visual approval**, not declared artistically approved. The previous 99° shop-shutter solution was visually rejected and is superseded.

## Installation

- Replaced the awkward single 99° door-side shop shutter with a matched, slightly splayed lower pair: world yaw 9° / 351°, using the original hinges and approved meshes. Hero and secondary front window designs remain intact.
- Rehung the existing entrance on its right jamb at `(4.68, 0.20, -0.75)`, closed yaw 180°, fully open yaw 75°. It still travels **105° outward**, now toward the free right-hand pocket rather than across the shop shutters. No interaction/input source changed.
- Moved the existing stone surround and arched stops forward by 0.49 m; deepened the existing genuine arched timber rebate in Z to 2.8× its original depth. This forms a continuous projecting entrance reveal, rather than a leaf floating ahead of the old doorway. No room, wall opening width, floor, canopy, roof or player dimension changed. Added two scene-local side-return BoxColliders; the clear opening remains 2.0 m.
- Created only `CM02_RightHingedEntranceLeaf.asset` as a derived copy of `CM02_FittedApprovedDoorLeaf.asset`: mirror local Z, transform normals/tangents, reverse triangle winding, preserve UVs and material assignments. With the rehinged root, the approved exterior face stays exterior, the handle is on the free edge and hinge hardware is on the right. Positive unit transforms; 2,444 triangles, same topology count. Original door and approved kit sources unchanged.
- Moved only the right sage planter from `(5.35, .20, -2.45)` to `(5.35, .20, -3.05)` to keep it outside the full opening arc, on the existing porch. Original left planter placement retained.

## Missing left-side shutters

`FinalizeCrookedMortarProduction02.cs` contains a blanket renderer-disable operation for `BedroomRear`, `TreatmentRear`, and `LivingWest`. Inspection confirms the rear paired assets still have their nested shutter Geometry renderers enabled; the operation actually hides the 14 individually named shutter meshes on **LivingWest**. Both of those leaves have been restored. No rear windows changed.

The north leaf would otherwise embed in the stepped nook wall. Its seven existing parts (planks, cross rails and hinge straps) now rotate together by -63° about the original hinge at `(-.32, 3.60, 1.96)` and seat 9 cm toward the front, against the return. The other leaf retains the established open treatment. This is a deliberate corner installation using the existing mesh parts, not a missing leaf or a panel buried inside the building. Shared prefabs were not edited.

## Targeted validation

- `SweepValidation.json`: 211 poses across the 105° outward sweep against 54 nearby visible mesh surfaces, including surrounds, canopy posts and fixtures. Actual fitted door convex envelope: no penetration greater than 2 mm seating tolerance. Separate door envelope expanded by 3 cm: no shutter intersections. Collision-safe player pause/resume tested separately below.
- `LeftWindowValidation.json`: all 14 shutter renderers enabled; no penetration >3 mm against the three adjacent wall colliders, including the nook return.
- `DoorInteractionValidation.json`: all 14 checks passed via temporary Input System keyboard E events and normal live component updates. No animation method invocation used to establish input success. Full opening/closing, player obstruction pause/resume, repeated use, and out-of-range/upper-floor rejection passed. All nine related CharacterController passage checks passed, including shop-to-kitchen circulation with the door both open and closed. The old left-hinge test's standing-clear position was adapted to the new right-hand sweep.
- `MeshValidation.json`: valid UV0 and finite normals, positive unit scene scale, 2,444 triangles. No new material or texture assets.
- Current Unity Console: no errors/warnings, no compilation failure. Historical retained Pipeline messages are not new findings.

## Visual review

All previews are clean Unity observer renders of the **complete facade**, using unchanged scene lighting/materials. Not edited/painted mockups. Door state was set only for captures and restored closed afterward. Player renderer temporarily hidden during capture, then restored.

| View | Closed | Fully open |
| --- | --- | --- |
| Front | `Previews/Front_Closed.png` | `Previews/Front_Open.png` |
| Approved-reference-facing three-quarter | `Previews/ThreeQuarter_Closed.png` | `Previews/ThreeQuarter_Open.png` |
| Left side / restored shutters | `Previews/LeftThreeQuarter_Closed.png` | `Previews/LeftThreeQuarter_Open.png` |

Review the matched lower shutters, projected entry reveal, right-hand door operation and the corner shutter seating. Visual approval remains with the user. The rest of the approved massing/art is unchanged; no broader architectural finishing was attempted.

## Scope

Changed only Production02, its new derived door mesh/meta, the relevant issue tracker and this report/validation/preview folder. No gameplay or camera scripts, input bindings, approved kit prefabs/materials, settings, packages, other scenes or Blender sources changed. Earlier uncommitted stair/camera work and the pre-existing shared slate material edit were preserved. Nothing committed. Exact task files: `ChangedFiles.json`.
