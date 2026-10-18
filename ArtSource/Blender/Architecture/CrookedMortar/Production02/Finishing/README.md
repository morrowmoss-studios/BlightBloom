# Production02 architectural finishing — 2026-10-17

Scene: `Assets/Scenes/CM_CrookedMortar_Production02.unity`. Existing 11.4 × 9.4 m functional envelope, floor levels, rooms, stair flights, entrances and all 90 original colliders preserved. No gameplay, camera/input source, original kits, project settings or protected scenes changed. Nothing committed.

## Corrected

- Trimmed concealed gable ends against adjacent roof envelopes and removed buried wing verges. The wing's exposed inner end required a short continuation of its existing pitch into the main roof. Fitted slate valley liners replace standing segmented caps and exposed brown backing in course cut-outs. Outer eaves, roof peaks and overall front silhouette retained; no footprint/room redesign.
- Added small landing-guard foot joint, guard caps and end trim within existing guard/wall footprints. This closes the visible landing seam and finishes exposed guard ends without narrowing the 1.5 m flights.
- Added a real rail at the three existing herb ties, with two canopy suspensions. Added lantern mounting plates and seated the left curl against its crown. Light components and intensities unchanged. Same ivy instance seated against the plaster/post transition; no botanical density increase.
- Reworked the existing arched door rebate rather than stacking another overlay. Inner lip seats against the actual wood silhouette, with a recessed outer arch perimeter. Closed-door daylight gap no longer visible in the tested oblique interior view. Physical door opening/collider unchanged; finished visual aperture approximately 1.81 m (target minimum 1.8 m).
- Shared scene-local glazing now softly tinted and translucent, with restrained emission, no glossy highlights or environment reflections. Paired and single windows retain their architecture, shutters and existing pane geometry. Opaque frame submeshes still cast shadows; the glass material's shadow pass is disabled. No light leak found around the reviewed window reveals.
- Legacy single-window host braces/eaves were already disabled; no need to alter approved window kits. Unidentified diagonal wall geometry was not reproduced in the current room/exterior captures. Painted plaster brush strokes and intentional structural bracing retained.

## Sources and scope

`build_finishing.py` reads the unchanged original Production02 blend and reuses the existing roof-kit geometry helpers. `CM02_ArchitecturalFinishing.blend` preserves editable local adapters; `CM02_ArchitecturalFinishing.fbx` is the only new Unity model. Original architecture/roof FBXs and all original kit exports preserved. The new model uses explicit approved material remaps and unit scale; relevant original renderer instances are disabled by scene overrides where a fitted adapter replaces them.

Editor installation is recorded in `ArtSource/Pipeline/Review/FinishCrookedMortarProduction02Integration.cs`. It refuses to run over an existing finishing installation. It is a one-time baseline migration, not a request to regenerate an already finished scene.

## Targeted validation

- `GeometryValidation.json`: 28 exported source meshes, 17,740 triangles; all checked solids manifold with positive volume, no degenerate triangles. Existing source UVs retained on gables; new trim uses UV0 and approved painted materials.
- `SurfaceValidation.json`: enabled current scene render meshes probed independently of gameplay colliders: 2,028 floor and ceiling samples, no holes; 4,732 roof-envelope samples including the fitted wing return, no misses. No invalid UV/normal attributes or missing scripts. Reused the established surface utility with temporary Edit-mode layer-31 probes, removed afterward.
- `TraversalValidation.json`: 56/56 actual CharacterController.Move routes, including both stair directions, all principal rooms, bedroom bed aisles, kitchen benches, garden and exterior circuit; 2,028 collision floor samples without holes; 64 existing-camera obstruction samples. Test-only motor/input/camera disabling ends on leaving Play mode.
- `DoorInteractionValidation.json`: 14/14 live input/safety checks, 9/9 associated route checks. Six E press/release events passed through a temporary Input System keyboard and the existing bound action, with normal MonoBehaviour updates and normal player systems enabled. Includes 105° outward sweep, pause/resume when obstructed, inside/outside opening/closing, out-of-range rejection and kitchen access. No direct animation method used as input proof.
- `SceneValidation.json`: exact pre/post comparison of 90 static colliders; CC, motor, input and camera enabled afterward; door closed. Current compilation successful; Unity Console zero current errors/warnings during the final Play session. Historical Pipeline logs were not cleared or treated as current faults.

Existing traversal/surface/input utilities were adapted transiently for this scene/report folder; no new shared validation framework or gameplay scripts were created.

## Remaining issues

- Manual indoor camera comfort still requires acceptance, especially the U-stair turn. Camera settings and behavior intentionally unchanged; automated obstruction samples do not prove comfort.
- The two originally reported diagonal-wall locations remain unidentified. If seen in Production02, record the room/view before choosing a material or geometry fix.
- Historical shadow-atlas warning did not reproduce; still deferred for diagnosis, not claimed fixed. No rendering budgets/settings were changed.
- This is focused architectural finishing. Production furniture, a finished hearth and broader garden/path art remain outside scope.
- Close-up roofing still reveals some polygonal course transitions. The exposed brown strips and standing fin are removed; this is not a new roof-style iteration.

## Review

Scene left open in Edit mode, saved, ready for normal Play testing. Updated clean images in `../Previews/`: Front, ElevatedThreeQuarter, Side, GameplayDistance, Shop, Kitchen, Bedroom, Staircase and Finishing_Entry / Finishing_DoorInside / Finishing_RoofJunction / Finishing_KitchenWindow. `ActualGameViewExterior.png` is the earlier reconstruction capture, not refreshed by this finishing pass.

Full changed-file inventory: `ChangedFiles.json`. Existing issue tracker updated at `../../Production01/ISSUES.md` with explicitly Production02-scoped statuses, preserving historical Production01 issues.
