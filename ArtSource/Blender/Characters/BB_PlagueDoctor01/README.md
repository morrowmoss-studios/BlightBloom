# BB_PlagueDoctor01 — first playable avatar

First-pass interpretation of `BlightBloom Apothecary Character Sheet.png`: moss hood/cape and open coat, ivory beaked mask, aged-gold lens rims, dark leather broad-brim hat, cream sleeves/underskirt, gloves, boots, belt vials and satchel. This is an intentionally simplified playable prototype, not final hero art or an exact reproduction of the painting.

## Editable sources and export

- `BB_PlagueDoctor01.blend`: editable individual parts, packed painted atlas, metric coordinates.
- `build_doctor.py`: reproducible Blender construction/export using the established FBX axis conversion. Exports only this avatar.
- `paint_atlas.py`: editable brush-shape/botanical painting source. Uses broad colour ribbons and drawn sprigs, without photographic noise.
- Unity asset folder: `Assets/BlightBloom/Characters/PlagueDoctor01/` — FBX, 1024px painted atlas, shared matte URP material, reusable visual prefab and `PlagueDoctorPresentation.cs`.

11 articulated mesh groups, **5,060 triangles**, approximately **1.99 m tall** at unit scale. Source solids manifold, positive volumes, complete UV0; imported meshes have UVs, normals and assigned material. One shared material, no transparency, no new lights, no colliders, no root motion.

## Integration

Only `Assets/Scenes/CM_CrookedMortar_Production02.unity` is changed among existing scene/gameplay assets. `Plague Doctor Avatar` is a child of `Crooked Mortar Player`. Existing `Player capsule visual` Renderer is disabled; the CharacterController remains enabled with its original 2 m height / .4 m radius. Avatar renderers use Ignore Raycast so the existing obstruction camera does not mistake the player's hat for architecture. No shared controller, input, camera, collision, architecture, material or project-setting changes.

`PlagueDoctorPresentation` measures actual horizontal displacement and applies visual-only idle breathing, opposing arm/leg swings, coat sway and small walking bob. Direction comes from the existing motor's player rotation. No Animator/humanoid rig, physics cloth or gameplay/input logic is added. Prefab may be reused beneath the same kind of player root.

## Future art work

This is low-poly prototype craftsmanship: smooth/skinned shoulders and elbows, proper fingers, tailored cape folds, asymmetric hat sculpt, deeper hand-painted texturing, mask seams, richer leather accessories and fine botanical embroidery remain future work. The simple segmented gait is included now; a properly skinned locomotion rig, foot placement and stair-aware animation should replace it later. Coat/limb self-intersections at extreme poses can occur; these visual meshes do not change traversal collision.

## Review

`Previews/` contains Unity renders. `Front`, `ThreeQuarter` and `BackGameplay` are observer renders; `Play_*` images use the existing gameplay camera in Play mode. Machine-readable mesh/route/animation results accompany this file. Automated input-route checks are functional evidence, not manual camera-comfort approval.

## Validation results

- Live normal-input route: **19/19** stair/landing/living/bedroom/study/shop/kitchen points passed, both stair directions.
- Live E and move route: **8/8** front entry/shop/kitchen/exit points passed.
- Separate collision-walk probe: **12/12** treatment/storage/rear exit/garden/perimeter points passed using a temporary identical CharacterController. This additional garden check is not a live-input/camera-comfort test.
- Runtime animation monitor: opposing leg swing approximately **-24 to +24 degrees**, capsule hidden, no avatar colliders, original 2m height/.4m radius. Actual gameplay-camera screenshots captured at stairs, upstairs and entrance.
- Current Console: zero errors/warnings, compilation successful. Historical Pipeline tool errors remain distinguishable from game/runtime errors.
- Existing serialized gameplay/collider records unchanged. Only the existing capsule renderer and player child hierarchy changed, plus the new visual prefab instance. Other scenes/assets were preserved.
