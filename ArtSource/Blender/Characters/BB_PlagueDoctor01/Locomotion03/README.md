# BB Plague Doctor — Locomotion03

Character-only successor to Rigged02. Original Blender, FBX, prefab, Animator and runtime adapter remain unchanged; Production02 retains the older avatar disabled for recovery.

## Diagnosis and implementation

Rigged02 animated the forearms through only a small range, barely used the pelvis/torso, and accelerated one short-stride walk for both speeds. Its visual ground solver also replaced the authored knee plane. Successful input routing did not establish convincing motion.

`build_locomotion03.py` opens the existing editable Rigged02 model. It preserves topology, UVs, painted material, proportions and the 27-bone skeleton. The overlapping inner linen edges are locally tailored into narrow walking vents to avoid opposite-boot penetration. It authors baked 60 fps idle/walk/sprint clips with wrist/foot trajectories, two-bone joint solutions, opposing shoulder/hip motion, coordinated hand relaxation, heel/toe roll and delayed coat/satchel motion. Supporting-leg coat influence is increased with a soft waist blend; existing toe bones receive boot-front weights.

The scoped `PlagueDoctorLocomotion03` reads actual player displacement and existing sprint input. Walk is authored for 1.4 m per cycle, sprint 2.5 m, matching the unchanged 3/6 m/s controls. Transitions preserve support-foot phase. Sole markers and the authored knee plane support terrain contact; flight feet are not pulled down. No root motion or controller writes.

## Assets and recovery

- Editable source: `BB_PlagueDoctor_Locomotion03.blend`.
- Unity folder: `Assets/BlightBloom/Characters/PlagueDoctor01/Locomotion03/` (model, controller, prefab, character-only script).
- Shared original painted material/atlas; no texture regeneration.
- `InstallInUnity.cs` is a guarded one-time installer. Do not rerun over an existing controller/prefab.
- Restore Rigged02 by disabling Locomotion03 and enabling the retained Rigged02 scene instance. Never enable both.

## Validation

Source: 27 bones, 9,376 native vertices, 18,524 triangles, one UV layer, normalized weights with at most three influences. Full source samples in `SourceValidation.json`.

Runtime visual and targeted route validation passed in the existing focused Editor. Full W recorded 2.996–3.000 m/s and W+LeftShift 5.994–6.000 m/s, using distinct Animator states. Four live phases per gait, idle, turning and stopped poses were captured front/side/three-quarter; elbow and garment-hidden knee diagnostics are explicitly labelled. Live elbows sampled about 27–67° walking and 71–101° sprinting. Source loops match exactly; UVs/normals are finite and valid.

The existing input-route utilities passed 19 stair/connected-room waypoints, eight E-key entry/exit/shop/kitchen points, and 12 treatment/storage/garden/exterior points. The stair test was repeated after the final cloth update, with normal camera Game-view captures. No route teleports or direct motor calls occur between waypoints. Source contact trajectories counter world movement; foot planting remains an approximate generic-rig solve, especially on stairs.

Unity compilation passes, with no new gameplay exceptions or warnings observed. Console retains the Pipeline `/api/exec` 5000 ms timeout error from automation calls during reload; it is not a character exception. No Console clearing was performed.

 `ValidateFullSpeedVisual.cs` uses full W and LeftShift through the existing input path, captures live skin poses and records speed, phases and joint angles. It creates only temporary observer/input objects in Play mode and restores them afterward. Reuse existing Rigged02 route utilities with report paths redirected here. Preview-only posed clips are not acceptance evidence.

## Limitations to review

This is hand-authored first-pass in-place locomotion, not motion capture or physical cloth. Long coat panels have a limited secondary rig; fast recovery and sharp turns require visual inspection. Stairs use the existing movement controller and limited foot-contact correction, not a dedicated stair gait. Manual animation feel approval remains necessary.

Nothing committed. No shared movement/input/camera, architecture, collision, package or project-setting changes.
