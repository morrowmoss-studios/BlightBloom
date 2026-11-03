# Briarwick Playable Exploration01

2026-11-03. Integration saved in the existing Briarwick scene. **Implementation and targeted automated Play-mode input validation completed. Ready for manual review; no manual playtesting claim.**

## Inspected and reused

Production02 contains a scene-specific `Crooked Mortar Player` with a 2m/0.4m CharacterController, TraversalInput and ThirdPersonMotor, and the active nested `BB_PlagueDoctor_Locomotion03` prefab at local Y -0.04m. Its 27-bone skinned model, painted material/atlas, `BB_DoctorLocomotion03.controller` and PlagueDoctorLocomotion03 ground-contact driver are reusable. Idle/Walk/Sprint clips are embedded in the existing FBX. Root motion is disabled. The driver reads displacement and Sprint; it does not move the controller.

Read ThirdPersonMotor.cs, TraversalInput.cs, ThirdPersonOrbitCamera.cs, PlagueDoctorLocomotion03.cs, the Production02 stair-camera variant and Locomotion03 documentation/validation utility. Production02 was inspected additively without saving it. Its visual instance has only name/transform overrides; its active Animator matches the reusable prefab.

Briarwick already had the identical motor/input/capsule setup with a visible temporary scale capsule and a general orbit camera. No replacement gameplay implementation was needed. Input uses the existing `Assets/InputSystem_Actions.inputactions`: keyboard WASD/arrows, Shift sprint, pointer look, gamepad left stick/movement, right stick/look and left-stick press/sprint. TraversalInput owns its private action-asset instance and ignores input without application focus. No new action map, PlayerInput or EventSystem is required.

## Integration

Created `Assets/BlightBloom/Characters/PlagueDoctor01/Locomotion03/Prefabs/BB_PlayerExploration_Locomotion03.prefab`. It wraps the copied existing controller/input/motor setup and existing orbit camera with internal references, plus the existing nested Locomotion03 visual. No new movement, animation or camera scripts.

- Root: BB_PlayerExploration_Locomotion03.
- Child: BB_Explorer_Locomotion03 — CharacterController, TraversalInput, ThirdPersonMotor; direct child Locomotion03 visual at -0.04m as in Production02.
- Child: BB_ExplorationCamera — existing ThirdPersonOrbitCamera, URP camera data and AudioListener.
- Spawn near woodland entrance: (-25, 7.1319, 85), facing north. It settles onto the existing road/terrain at runtime.
- Motor remains 3m/s walk, 6m/s sprint; capsule height/radius/skin/step/slope unchanged.
- General orbit uses the existing production exterior control/follow settings with a 4m boom and 65° FOV; outdoors far plane remains 600m. Production02's additional camera contains house-specific world-coordinate stair/interior zones, so those zones were not transplanted outdoors. No camera source code was modified.
- Retained the original Briarwick test player and camera disabled, not deleted. Review camera remains disabled. Runtime checks show one active player, TraversalInput, camera and AudioListener; zero EventSystems, which is appropriate here.
- Fixed a visibility conflict discovered by an actual runtime render: the source skin is layer 2, which Briarwick's camera excludes for planning labels. The new wrapper overrides DoctorSkin to layer 0. Original character prefab, player capsule layer and camera label mask remain unchanged. The avatar is visibly rendered in `Entrance_Preview.png`.

## Validation so far

- **14/14 automated CharacterController.Move collision routes passed** across the full winding woodland route, three lanes, forward/reverse, turns, clearing and edge. Motor/orbit were temporarily paused for this collision probe and restored. This is not a live-input locomotion or camera-comfort test.
- Runtime and Edit configuration checks: all Animator/rig references resolve, expected Animator controller, root motion disabled, no missing scripts, one active input/player/camera/listener. Grey scale capsule is absent from the new rig; only DoctorSkin renders.
- Snapshot comparison of all 696 pre-existing scene objects found zero unexpected component changes; only the two intended original player/camera objects are disabled. Terrain height and alphamap samples are byte-identical.
- Protected-file hash verification finds only the intended Briarwick scene changed. Crooked Mortar Production02, character source prefabs/FBX/controller/painted assets, shared scripts/settings, terrain asset and vegetation assets remain unchanged.
- Final Console check after live-input testing: no compilation failure, **0 errors/0 warnings**. No new entries since the previous Console cursor.

## Completed live-input validation and limitations

`LiveInput.cs` adapts the established Locomotion03 validation approach. It used temporary gamepad/mouse device state events through unchanged TraversalInput, ThirdPersonMotor, ThirdPersonOrbitCamera and Locomotion03 in focused Play mode. It did not invoke motor methods or animation poses directly during the route. Temporary input devices and runtime pose were restored afterward; the Editor is now back in Edit mode with the saved starting placement.

**Passed:** five outward woodland waypoints and seven return waypoints along the road to the village building approach, with alternating walking/sprinting, stopping to Idle, and **92.141° camera orbit through normal look input**. All **213/213 sampled positions were grounded**. Runtime screenshots show distinct walking/sprinting poses and visible articulation; sampled animation phases and elbow/knee rotations change through the route. Idle is confirmed during stops at stages 6/8/10. The automatically named `01_WoodlandEntrance_Idle.png` was captured after movement had already begun on gaining focus; use `Entrance_Preview.png` for the actual idle entrance view instead of treating that filename as an idle assertion.

Distance from the current player pivot to the camera ranged **2.95–4.39 m** along the test (includes follow smoothing, not an exact boom-clearance measurement). Captured views retain player visibility without extreme compression on this route. Ground contact remains the existing approximate solver; this pass does not establish perfect foot planting on every slope. Tree colliders remain approximate trunk capsules, and noncolliding foliage can visually overlap the camera. Manual camera comfort and arbitrary off-path foliage encounters still require review.

Focus was initially unavailable and desktop automation timed out. After the user focused Game view, the final test passed without bypassing the shared focus guard, changing background settings persistently, or modifying input code. This was **automated input-path testing**, not a claim of manual playtesting. Full samples/results are in `LiveInputValidation.json` and `LiveInputSummary.json`; earlier cancelled focus attempts are not the acceptance evidence.

Final Edit-mode preservation check again found zero unexpected changes among 696 prior objects. All rig references resolve and the scene contains exactly one active controller, input handler, camera and AudioListener. No unresolved scene-specific dependency was found. The exploration wrapper references the existing Locomotion03 visual/controller/FBX, shared painted material/atlas, input asset and existing traversal scripts; retain those dependencies.

## Files and recovery

Modified: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
Created: exploration wrapper prefab and its meta; this review folder with snapshots, integration/dependency report, validation scripts/results and entrance preview. Full paths in `ChangedFiles.txt`.

No commits or pushes. No environment expansion or polish. Integration and targeted validation complete. Stop here for review.
