# Counter Workflow09 — focused timber and carving refinement

Open `Assets/Scenes/CM_CounterWorkflow09_Review.unity` (saved, outside Play mode). Workflow09 is visible; Workflow08 remains alongside it in the hierarchy with its renderer disabled. Production02 and the Workflow07/08 scenes, source files and assets are untouched.

## Changes and method

`refine_counter09.py` **opens the existing Workflow08 .blend** and reuses its separate editable construction parts. It does not rerun the complete counter generator. The top, curved rails, stiles, quiet panels, storage floor, end fields, drawers and handles are reused directly. Workflow08 geometry/UV helpers and validated FBX conversion are reused.

- Replaced four swollen formal supports with mildly splayed, chamfered, tapered timber posts. Short bearing knees and shallow drawbore peg ends make the rail/post connections readable. Flat planed faces and narrow bevels replace continuous smooth swelling. Hidden mortise cavities are not fully modeled; this is visual joinery, not an exploded manufacturing model.
- Refined the existing dense central sculpture with a small edge-preserving height correction, slightly stronger relief and a higher curvature-reduction budget (0.12 instead of 0.085). The original Workflow07 stencil is reused; it is not regenerated. The shared curved substrate and single continuous UV domain are retained.
- Reused Workflow08's existing painted walnut image, with restrained saturation/value/warmth tuning baked natively in Blender. No new image generation, artwork request, photographic noise or additional ornament. The central colour bake retains exact mesh registration and adds modest sculpt-derived edge/value articulation. These are emission colour bakes, not AO, normal-map or scene-lighting bakes. Matte URP materials are retained.

Editable file: `CM_CounterWorkflow09.blend`, including separate joinery, dense sculpture, packed painting inputs and final game mesh. Final FBX/prefab/materials/derived colour maps live under `Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow09/`. Reproducible script depends read-only on Workflow07/08 sources. No unrelated geometry or artwork regenerated.

## Result and limits

Final mesh: **77,390 triangles**, 48,170 Unity imported vertices. This is 9,582 more triangles than Workflow08, primarily reserved for the central carving; this is not a mesh-budget optimization pass. One renderer, three shared matte materials. No LOD or normal-map bake delivered.

The clear improvement is a less formal, more appropriate timber construction while retaining the curved outline. In clay, supports, knees and peg relationships are visibly different. Carving crispness improves incrementally; fine leaves remain soft and need authored sculpt cleanup. The warm paint adjustment is intentionally subtle, not a dramatic new texture style. The counter remains bilateral; some grain repetition and the simpler surrounding shelves are still visible. These limitations do not justify adding clutter or remodeling the room during this test.

This is an efficient, reproducible refinement of the existing workflow, not a claim that the complete illustrated-reference quality has been reached. Artistic approval remains pending. No propagation into Production02.

## Matching comparison and validation

Only three paired views were captured in one Play-mode pass: `GameplayDressed`, `ClayBare`, and `CarvingClose`. `Previews/Comparison` labels Workflow08 left / Workflow09 right. Same scene, lighting, exposure, camera and original dressing. Gameplay uses the existing player/orbit camera position, pinned identically for the second version; clay/close views use temporary inspection poses. No extra props or image paint-over. Visibility, materials and player/camera poses restored before leaving Play.

Validation performed once on the completed candidate, using existing targeted utilities:

- Source finite geometry, normals, UVs, degenerate triangles, metre scale and pivot checks passed.
- Unity imported normals/UV/material references complete; no missing scripts/materials.
- Same 2.28 x 0.78m bounds and 1.0525m local flat work-surface datum.
- All 116 scene colliders unchanged, zero new colliders. Existing station markers retained.
- 43 static poses across the unchanged 105-degree outward door swing: no candidate contact.
- 190 static capsule-volume route samples using the unchanged 2m tall / 0.4m radius player: entry, staff/customer sides and nearby stair/kitchen connection clear.
- Console: zero current errors/compilation failure; no new captured entries. Two pre-existing warnings retained.
- Protected source/scene/asset hashes verified; see `ProtectionValidation.json`.

Not performed: fresh live-input walking/sprinting/stairs/E-key route tests, manual camera-comfort approval, broad project regression, room reconstruction or LOD performance benchmarking. Play mode was used for actual visual captures. No gameplay, camera, player rig, architecture or navigation changes. Nothing installed, committed or pushed.
