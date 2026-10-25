# Crooked Mortar counter — pipeline experiment 07

One hero asset only. This is a controlled comparison, not a production rollout or a whole-room decoration pass.

Open `Assets/Scenes/CM_CounterWorkflow07_Review.unity`. It is a separate copy of Production02 with only the counter's visible body replaced. The original `Assets/Scenes/CM_CrookedMortar_Production02.unity` is byte-identical to existing Git checkpoint `2dd2625`. Existing architecture, player, camera, door, colliders, furnishing positions and station markers are retained. The original C05 counter remains in the review scene with its renderers disabled, and its original prefab/source are untouched. No additional loose props.

## What changed in the method

The old pipeline chiefly assembled primitive-derived members, reused narrow shared paint-atlas samples and accumulated printed or thin applied ornament. That made file generation reliable, but supplied neither asset-specific surface painting nor enough designed sculptural complexity. More subdivisions or more ornaments would not correct this.

The chosen experiment combines:

1. Reference-led, bespoke Bezier silhouettes and changing profile sections for the worktop, bowed rails, apron, bearing shoulders and cabriole standards. Their dimensions are fitted to the counter's existing use envelope rather than copied from the reference room.
2. An illustrated botanical/mortar design converted to an explicit binary sculpt stencil. A first generated grayscale relief image was rejected: it contained directional shading, not trustworthy depth.
3. Continuous panel substrates inflated from the stencil's interior distance field. Leaf silhouette volumes and shallow vein incisions are separated. The first 3D trial cut veins too deeply; morphological separation and geometric surface fairing corrected that failure. This is numerical sculpture, not albedo brightness displaced into a mesh, and not loose leaves pasted onto a plane.
4. Dense editable sculpt sources retained separately; curvature-adaptive reduction generates the visible game mesh. Hidden backs are flat caps rather than duplicates of the entire dense relief.
5. Dedicated registered gouache-style carving colour and a new quiet walnut surface sheet, generated with the built-in imagegen tool. The first colour trial was rejected for busy grain/high contrast. Structure has physical-scale, grain-aligned UVs; carved fields have their own registered UV regions. Shared old atlas patches and decorative overlays do not supply the new carving.

`MethodAssessment.md` compares alternatives and limitations. No specialized image-to-3D service was configured or used. No packages, software purchases or external paid services.

## Files and recovery

- `CM_CounterWorkflow07.blend`: editable unconverted source, including the hidden `Editable dense sculpt sources - not exported` collection.
- `CounterStencil.png`, `SculptFields.npy`, `PrepareRelief.py`, `ReliefRecipe.json`: reproducible sculpt input and explicit depth recipe.
- `CounterPaint.png` / `WalnutPaint.png`: selected painting sources; rejected trials preserved separately. Images are packed in the Blender file too.
- `build_counter07.py`: bespoke shape/UV/reduction/export implementation, not a rerun of the AF01/C05 furniture recipe.
- Unity outputs under `Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow07/`: one FBX, prefab, two colour maps, three matte URP materials. The prefab supplies visuals and a work-surface datum; existing scene collision and interaction markers stay on the original functional counter root.
- `Prompts.md`: built-in image generation prompt record and selected/rejected outputs.

The interrupted, broader Reconstruction06 pass was superseded by the user before completion. Its Production02 installation was restored to baseline and its sources/recovery snapshot retained in `../Reconstruction06/`. Its unreferenced Unity outputs were hash-verified and archived outside Assets in `AbortedUnityOutputs/`, then removed through AssetDatabase. It is not an approved or installed result.

## Comparison and honest assessment

`Previews/Existing` and `Candidate` are matching Unity Game-view screenshots from the same scene, camera, lighting, exposure and dressing. `GameplayDressed` uses the existing player/orbit camera, pinned to the same pose for the second variant. Front/angled/close/bare/clay views use temporary inspection poses in Game view. Player and loose counter dressing are hidden only for inspection; normal dressing is restored afterward. No paint-over, generated beauty render, lighting trick, bloom/blur change or extra props is presented as a Unity result.

The new carving is substantially more intricate and reads at the tested third-person distance; the bare and clay views establish actual sculptural relief. The asset-specific walnut painting is more cohesive than the previous sparse sage fields and simple leaf strips. This is a promising improvement in the method, not proof of the complete environmental target.

Remaining limitations: the global cabinet remains fairly rectilinear; some illustrated colour shading remains baked into the generated map; image edits are not perfectly pixel-registered; small carved edges need manual cleanup/retopology for final hero quality. It is not a fully hand-sculpted undercut carving. The roughly 92k-triangle review mesh needs an intentional LOD/bake budget before village-wide reuse. No normal-map bake is claimed in this delivery; visible depth is real geometry. No wider propagation is recommended until manual artistic approval.

For maximum control, a trained environment artist can sculpt/paint directly over this editable source, redraw specific contours and create tailored retopology/bakes. Blender already supports that; the actual remaining constraint is authored artistic judgement and precise shape/paint registration, not an FBX export problem. More generic procedural detail is not the recommended next step.

## Validation

`SourceValidation.json`: final source has valid finite coordinates, UVs and normals, no degenerate triangles, metre scale and zero-offset pivots. Dense source panels intentionally remain separate in the hidden authoring collection. An unwanted automatic UV set on converted handle curves was removed rather than weakening the validator.

`IntegrationValidation.json`: final imported mesh/reference checks; all 116 original colliders unchanged, no new colliders, no missing scripts/materials; 43 poses along the unchanged 105-degree outward door arc clear the candidate.

`ClearanceValidation.json`: 190 dense 0.10m capsule-volume probes using unchanged height 2m / radius 0.4m; entry, customer and staff sides, stair and kitchen connections clear the new visible geometry. These are static collision/clearance checks, not a fresh live-input route/E-key test or a manual camera-comfort judgement. Controls/locomotion/door/camera scripts are unchanged.

Final captures run in Play mode. Pipeline incurred an automation timeout during initial review creation and briefly disconnected on Play reload; the operation completed and connection recovered without restarting Unity or launching another Editor. These are automation failures, not compilation/gameplay errors. Final Console: no compilation failure, zero current errors, two retained warnings, and no new captured entries after the initial automation timeout. See `ConsoleValidation.json`.

Nothing committed or pushed. Candidate remains confined to the review scene for manual artistic approval.
