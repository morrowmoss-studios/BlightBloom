# Production02 entry / shop composition 05

**Candidate for manual visual approval. Previous shutter arrangements are rejected, not approved.**

## Assessment before construction

The approach view (`Previews/Before_Approach.png`) showed a shop opening, wide single-leaf shutters, porch post, lantern and door surround competing for the same narrow strip. The near shutter was partly hidden by the post/lantern, and moving the doorway forward made its stone arch dominate independently of the shop bay. A left-opening door also hid the display when open. This needed a composed frontage, not another isolated shutter angle.

## One fitted solution

- The existing paired shop insert is fitted to **80% of its former horizontal span**, keeping height, central division, glazing and craftsmanship. Its lintel is about 1.63 m wide. The original wide shop shutters are inactive only in this scene; source assets remain intact.
- New matching **bi-fold sage shutters**: two .36 m leaves per side, folding into a .36 m stack instead of swinging a broad panel toward the door. Their approx. 1.63 m height covers the casement glass with a rebate margin. Twelve-degree splay, a deliberate gap between folded leaves, matching hinge plates/knuckles and softened painted edges provide believable attachment. Both sides share proportions and opening logic.
- Fitted ivory plaster returns close the former wider rough openings; a quiet walnut lintel shoulder completes the narrower bay. Existing planter and planting fit the same width. No interior room dimensions or routes changed.
- The stone/arched timber surround returns to its original shallow plane. The reused right-handed door at `(4.68, .20, -.31)` travels **180° closed → 75° open: 105° outward**, away from the display. This removes the previous .49 m surround projection. The 5 cm outboard leaf seating is for its rebate/stop, not a substitute for shutter fitting. No gameplay source changed.
- A pre-existing continuous base timber crossed the doorway. It is replaced in this scene by two fitted instances of the approved beam, ending at the stone surround shoulders. The porch finish now butts into the shop floor at z=-.20 rather than overlapping it. Existing floor colliders remain continuous and unchanged.
- The right porch planter returns to its original position. Portal, lanterns, sign, herbs, roof hierarchy, upper windows and all unrelated facade/room systems remain unchanged from this task's starting scene.

## Assets / editability

`CM02_EntryShopComposition05.blend` and `build_entry_shop.py` retain 43 editable solids, reusing approved modeling/UV/export helpers. New FBX: `Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/Models/CM02_EntryShopComposition05.fbx`. Four material groups / **4,788 triangles**; two reused plinth-beam instances add 216 triangles. Scene root: `16 Fitted entrance and shop composition` (six renderers, not one GameObject per plank).

Walnut and plaster materials are reused. Two new matte URP materials provide sage (using the existing approved paint sheet) and restrained dark iron; no texture images, packages or approved kits were regenerated. Original and earlier rejected assets/scenes remain preserved.

## Validation

- `MeshValidation.json`: source solids manifold, positive volume, no degenerate triangles. `UnityImportValidation.json`: UV0 complete, no inverted normals or collapsed UV triangles, correct orientation/material assignments; new FBX groups at unit scale. Reused beams vary in length with unchanged cross-section.
- `SweepValidation.json`: 211 poses across the full 105° swing against 58 nearby visible mesh surfaces. No penetration >2 mm seating tolerance; no shutter intersection with a separate door envelope expanded 3 cm. Includes surround, framing, lanterns and nearby objects. Foliage alpha planes/glazing are excluded from the solid-envelope test.
- `DoorInteractionValidation.json`: **14/14 live E-key checks and 9/9 related passage checks passed**, including player obstruction pause/resume and kitchen access with the door open/closed. Temporary Input System events used the existing action path; no animation method invocation established input success.
- `EntryExitValidation.json`: **8/8 continuous route connections passed** using temporary Gamepad move events → existing TraversalInput → normal motor Update: approach, enter, shop, kitchen, return, exit. One initial placement only; no route teleports or test-driven CharacterController.Move. Camera-relative steering compensates for camera heading, so this is function evidence rather than manual-feel acceptance.
- Scene-local collision changes: **only the two redundant projecting-return colliders from rejected pass 04 were disabled**. Original room, floor, stair, wall and player colliders unchanged; no new collision geometry. See `ScopeValidation.json`.
- Compilation passes; current Unity Console has zero errors/warnings. The earlier Pipeline main-thread timeout is an automation connection event, resolved by restarting Pipeline in the existing Editor, not a new gameplay error.

## Visual review

Clean Unity observer renders with unchanged lighting, no editing gizmos, filters or image paint-over. Player renderer temporarily hidden for clarity and restored. Approach camera at `(4.8, 2.2, -9.5)` evaluates gameplay-distance readability; it is an observer view, not a claim that the shared player camera was changed.

| View | Door closed | Fully open |
| --- | --- | --- |
| Front / complete facade | `Previews/Front_Closed.png` | `Previews/Front_Open.png` |
| Three-quarter / complete facade | `Previews/ThreeQuarter_Closed.png` | `Previews/ThreeQuarter_Open.png` |
| Player approach distance | `Previews/Approach_Closed.png` | `Previews/Approach_Open.png` |

Review judgement: the smaller folding leaves establish equal jamb margins; the doorway remains the focal point, the open leaf moves away from the shop, and the base timber/threshold now read as intentional construction. Other canopies/upper shutters still carry the approved StyledDetails07 identity. **These are design observations, not user approval.** Review the new narrow, taller shop-shutter proportions in Unity before accepting this candidate. No further decoration or unrelated architectural redesign was attempted.

## Scope

Production02 only, its new fitted FBX/materials/source, and the relevant issue tracker/review artifacts. No shared gameplay or camera source, project settings, packages, approved kits, building dimensions, roof hierarchy, other rooms or other scenes changed. Prior uncommitted work was preserved. Nothing committed. Exact task paths: `ChangedFiles.json`.
