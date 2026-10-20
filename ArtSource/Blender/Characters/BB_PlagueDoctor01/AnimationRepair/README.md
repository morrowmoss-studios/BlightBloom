# Plague doctor visible-animation repair

## Confirmed root cause

The saved avatar prefab contained six animated joint objects with **zero renderer descendants**. The arms, legs and coat panels were still siblings beneath the nested FBX model root. Reparenting imported model children during the original installation did not survive saving/reloading the nested prefab. Thus movement detection and numeric joint-angle checks succeeded, but rotated empty transforms. Only the parent body's bob affected the visible character. The original `AnimationValidation.json` is historical and does not establish visible animation.

## Repair

- Unpacked the nested FBX instance **inside the avatar prefab only**, preserving its shared FBX mesh and material references. Reparented the six articulated mesh objects to the corresponding shoulder, hip and coat joints, retaining their rest positions. The reusable FBX and Blender geometry are unchanged.
- Verified the saved/reloaded prefab and runtime instance each have one renderer under every articulated joint.
- Avatar-only presentation script: travel-paced phase, coordinated opposing arms/legs, stronger but restrained coat motion, smoothed movement transitions. Removed walking body bob; retained only 3mm idle breathing. Visual boot contact compensation follows ground under the rotating boot, with a small swing-foot lift. No root motion, motor/input/controller/camera modification, or colliders added.
- Existing dimensions, silhouette, painted materials and architectural scene objects unchanged. Production02 inherits the fixed visual prefab.

## Visual evidence

`VisualCycleValidation.json`: actual Play-mode normal input path, temporary gamepad → TraversalInput → existing motor. Captures at idle and opposite stride phases show renderer-centre changes and the visible model in front, side and three-quarter views. No methods set the captured poses directly. `Previews/RuntimeContactSheet.png` arranges those unaltered Unity renders; source PNGs remain available individually.

## Limitations

This is segmented prototype articulation, not a skinned humanoid animation set. Boots still rotate with straight legs; heel/toe roll, bending knees/elbows, full foot locking and tailored cloth deformation need a proper rig. Cloth can intersect limbs at extreme poses. Ground compensation improves contact but is not production foot IK; manual review on uneven ground remains appropriate. No claim of final locomotion polish.

## Targeted regression results

- Runtime visual cycle passed: idle plus opposing gait phases, nine clear observer captures. Each animated joint contains a visible mesh.
- Live-input stair route **19/19** passed, including ascent/descent, turning landing and adjacent rooms.
- Live E-key/front-door entry/exit route **8/8** passed.
- Current Console zero errors/warnings; compilation successful.
- Stopped Play mode and verified all six mesh/joint connections persist in the saved prefab instance. Production02 remains open.
