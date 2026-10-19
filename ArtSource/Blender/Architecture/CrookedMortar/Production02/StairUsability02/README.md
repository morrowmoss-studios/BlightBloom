> Latest: `../FocusedRepair03/README.md` supersedes the guard/camera results below after further manual findings. This document describes the prior revision.

# Production02 stair usability correction

Current scene: `Assets/Scenes/CM_CrookedMortar_Production02.unity`. This supersedes the earlier guard-cap finishing pass for the staircase. Manual acceptance of the new camera feel remains necessary.

## Cause and correction

The old centre guard was a solid 0.2 m thick panel with a flat top, regardless of tread level. The upper stairwell had another long solid guard and the intermediate landing had a redundant guard in front of a full-height wall. These obscured the flights and turn. The original camera could only retract a straight boom; at the rear wall it reached approximately **0.77 m**, despite remaining collision-free. The lower-flight settled sample reached **1.18 m**.

- Replaced the visible guards with a sloping centre balustrade, slim upper balustrade, newels, caps, handrails, spindles and properly fitted upper stringers. Five exported mesh batches use the approved painted walnut material; 64 editable source pieces total 6,912 triangles.
- Extended only the intermediate landing from **3.2 × 1.5 m to 3.2 × 1.7 m**, meeting its existing enclosing wall. A wall-mounted turning rail replaces the redundant rear guard. The 1.5 m flights, 18 risers, room dimensions, exterior, floor rise and existing treads remain unchanged.
- Disabled the three superseded guard colliders and old guard/landing renderers in this scene. Retained them for reversibility. Extended the existing landing collider to match its floor. Added four static visible-timber MeshColliders and two continuous non-trigger player-safety guard boxes. Enabled static colliders: 90 before, **93 now**. CharacterController height 2 m, radius 0.4 m and step offset 0.3 m unchanged.
- The two invisible safety boxes use the existing Ignore Raycast layer; the player still collides with them. The scene-local camera ignores that layer so empty balustrade air does not behave like an opaque panel. An audit confirmed those are the only two colliders on that layer in this scene. Visible timber, walls, treads, floors and ceilings remain camera obstacles. No project layer settings or collision matrix changed.

## Camera scope

`Assets/BlightBloom/Prototypes/CrookedMortarProduction02/Production02StairOrbitCamera.cs` is a **Production02-only variant** of the existing orbit camera. The original shared script is unchanged and its component is disabled only on this scene's camera; it remains available for comparison. Existing target/input references, mouse sensitivity, follow smoothing, pitch limits, cursor handling, FOV and requested 4 m follow distance were copied unchanged.

Inside the serialized stair bounds, the variant searches for a useful nearby orbit, predicts clearance ahead of movement, and avoids leaving the downstairs camera stranded above the front landing floor during descent. Final placement always uses real obstacle clearance. An emergency clear-orbit fallback handles abrupt placement/orbit changes rather than pushing through geometry. Outside the stair area, the original follow/orbit logic applies (with the deliberate invisible-guard filtering described above).

The first live route exposed transient compression that settled screenshots missed. The current predictive version was rerun; see the final reports below. This is not a claim that every possible mouse gesture or camera preference has been manually accepted.

## Validation

- **LiveRouteValidation.json / CameraQualityValidation.json:** temporary gamepad left-stick events followed the existing Player/Move action, TraversalInput and normal ThirdPersonMotor.Update, with the real camera LateUpdate enabled. Both flights, both directions, the turn and 19 room/route connections passed. Steering compensated for rendered camera yaw to follow repeatable waypoints; this is real input-path testing, not a human-operated WASD feel test.
- Final continuous stair run: **minimum 1.95 m, median 3.18 m**, at least 3/4 body samples visible, head and torso visible throughout, maximum sampled body height 56.3% of the viewport, **zero camera/geometry overlaps**. One correction followed the test's initial placement; **zero emergency corrections during walking**. Those framing criteria are recorded separately from mere route completion.
- **BeforePoseValidation.json / AfterPoseValidation.json:** seven settled normal-controller/camera poses at the bottom, lower flight, turn and upper landing. Final representative distances **2.66–3.08 m around the turn**, versus 0.77 m on the rear-facing before views. These are comparison views, not manual acceptance.
- **GuardAndLandingValidation.json:** 32/32 edge-protection penetration samples; player/guard layer collision enabled; 220 landing-floor samples with no holes. No controller shrinking or disabled player collision.
- **ConnectedTraversalValidation.json:** reused the established utility with the scene-local camera type: 56/56 connected routes including stairs, bedrooms, study, kitchen and garden; 2,028 floor samples without holes. This deterministic test is supplementary, not the camera-comfort verdict.
- **MeshValidation.json:** all 64 source solids manifold with positive volume, no degenerate triangles; UV-mapped, unit-scale FBX. Final Unity compilation succeeds and current Console errors/warnings are zero.

## Sources, screenshots and review

Editable `CM02_OpenTimberStair.blend` and `build_stair.py` live here. Unity model: `Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/Models/CM02_OpenTimberStair.fbx`. No original kits or shared prefabs were regenerated.

`Previews/After_*.png` and `Game_Bottom.png`, `Game_Turn.png`, `Game_UpperLanding.png` capture the **actual Game-view render target**, with no editing gizmos. Representative poses use normal follow/collision updates; mouse look was temporarily paused only to keep capture headings stable, then restored. The live input route was a separate uninterrupted test. `Before_Turn*.png` retain the compressed comparison. The existing main `../Previews/Staircase.png` was refreshed to show the new construction.

The scene is saved in Edit mode with normal player systems and the new local camera enabled. Enter Play and manually check walking, turning, deliberate orbiting and descent. Final acceptance should focus on whether the orbit assistance feels natural, not solely whether the automated quality thresholds passed.

See `ChangedFiles.json` for this task's file inventory. Earlier uncommitted finishing work was preserved. Protected scenes, expanded rooms, exterior assets, shared camera/movement/input scripts, packages and project settings are unchanged. **Nothing committed.**
