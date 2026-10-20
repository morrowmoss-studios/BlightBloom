# BB_PlagueDoctor01 — Rigged02

Skinned successor to the preserved rigid prototype. Sources, FBX, prefab and script from the original `BB_PlagueDoctor01` remain unchanged and recoverable. Only Production02's visible avatar is replaced; the old avatar instance stays disabled in that scene.

## Source and modeling

`build_rigged_doctor.py` reads the original editable source, preserves the mask/hat/botanicals and accessories, and constructs replacement sleeves, trousers, boots, rounded shoulder mantle and layered coat/linen panels. Added support rings at elbows, knees and ankles; smooth shading and controlled accessory bevels improve curves without global subdivision. The approved painted atlas and matte material are reused. `BB_PlagueDoctor01_Rigged02.blend` contains the editable skin, weights, skeleton and two actions.

27 deformation bones: root, hips/spine/chest/neck/head, shoulders, upper/lower arms and hands, thighs/shins/feet/toes, four coat bones and a satchel bone. Explicit normalized weights (maximum three influences) prevent proximity-weight errors between cloth and limbs. One joined skin / one shared material; 18,524 triangles. FBX metric scale, -Z forward / Y up, established conversion node; armature bind transforms are not baked destructively. Generic rig keeps named bones and original Blender actions available for future interaction clips; this is not a Humanoid retargeting avatar.

## Animation and runtime

Blender `Doctor_Idle` and `Doctor_Walk` actions are baked at 30fps. Idle breathes subtly; walking uses analytical two-bone targets with bent knees, planted stance feet and lifted swing feet, plus elbow bends, arm swing, cloth and satchel motion. Both clips loop. Native source preserves the actions; FBX carries ordinary deform-bone keys, without needing Blender constraints in Unity.

`BB_DoctorLocomotion.controller` uses 180/200ms idle/walk crossfades. The scoped `PlagueDoctorLocomotion` component measures actual player displacement, drives clip cadence, and applies generic two-bone ground contact and bounded stance-foot stabilization. It never writes player/controller/camera transforms, collision dimensions, inputs or root motion. No packages, physics cloth or shared gameplay changes.

Unity folder: `Assets/BlightBloom/Characters/PlagueDoctor01/Rigged02/` contains the FBX, Animator controller, visual prefab and adapter. The existing painted material/atlas are referenced rather than duplicated.

## Limits / future work

This is an initial game rig and locomotion set, not final hero animation. No finger rig, facial animation, physical cloth, interaction clips or bespoke sprint/run clip yet. Sprint reuses faster locomotion. The generic foot adjustment is bounded and cannot replace an authored stair gait on every step. Fine fabric intersections, shoulder tailoring, toe roll and biomechanical polish still need artist review. No camera or environmental lighting changes are used to hide deformation.

## Completed validation

- `RuntimeVisualValidation.json`: passed normal TraversalInput/ThirdPersonMotor testing. Idle, four gait phases, turning and stopping were captured in actual Play mode. Knees bend approximately **22–79 degrees** through gait, compared with approximately **6 degrees** at rest; elbows remain naturally bent and vary across the cycle. These are skinned mesh poses, not empty rigid-joint rotations.
- `StairRouteValidation.json`: **19/19** live-input points passed: ascent/descent, intermediate turn, landing, living/bedroom/study connections and shop/kitchen.
- `EntryExitValidation.json`: **8/8** live points passed, including actual E-key front-door opening/closing and normal entry/exit.
- `GardenRouteValidation.json`: **12/12** live points passed: treatment, kitchen, storage, garden doorway/step and exterior perimeter. No route teleports after each test's initial placement.
- Grounded stance/idle ankle height approximately **15 cm above the ground**, matching the modeled boot sole offset; swing feet rise approximately **11 cm**. Production02 has a **-4 cm visual-only avatar attachment override** to account for the unchanged controller skin width. No gameplay/controller transform change.
- Source vertices normalized/weighted, maximum three influences; Unity Generic Avatar valid; 27 non-null skin bones, complete UVs/normals and assigned existing matte material.
- Console: compilation successful; **one Pipeline /api/exec main-thread timeout** was logged during capture. No new game-script runtime error or warning was observed. This automation error is retained rather than clearing the Console.

`Previews/RuntimeContactSheet.png` shows actual runtime front/side/three-quarter views at idle and several walk phases; the individual PNGs include all four gait phases, turning and stopping. `Previews/DeformationCloseups.png` includes an elbow view and a **clearly labelled garment-hidden knee diagnostic**, because the long coat normally conceals the knee. For that diagnostic only, a temporary copy of the skin's index buffer renders the leg triangles; the original mesh/outfit is restored immediately and no asset is modified. All other views use the complete outfit.

`InstallInUnity.cs` preserves guarded one-time asset setup; `ValidateLiveVisualCycle.cs` is the focused Play-mode capture utility and injects temporary input. It is not read-only. Existing stair/entry route utilities were reused with report paths redirected here.

## Saved scope

Production02 is saved and open in Edit mode. The old avatar, source, FBX, materials and scripts remain untouched. The scene changes only disable the prior visual instance and attach the new rigged prefab with its visual offset. Existing controller, input, camera, door, colliders, room layout and architecture are unchanged. Automated routes do not constitute manual artistic or camera-comfort approval. **Nothing committed.**

### Final coat-weight correction

The first live frames exposed knee penetration through the front coat panel. Final cloth weights now blend the supporting thigh with hips and a secondary coat bone, with compatible weights along panel seams. The corrected FBX was imported **before** the final `RuntimeVisualValidation.json` run and its PNG captures; that final run passed all seven capture groups. Normal-input gameplay and final rendered deformation therefore both have direct runtime evidence. The temporary supplementary posed review was obstructed and was discarded. Three influences are used only where cloth requires them. Source skin validation remains normalized.

Traversal routes preceded this final weight-only cleanup; no controller, clip, collider or architectural change followed them. The final live gait/stopping/turning capture was repeated after the cleanup. Remaining fine shoulder/ankle tailoring and cloth contact at extreme poses still require manual artistic review; no claim of final hero-art polish.
