# Entrance Workflow11 — architectural storybook test

Review scene: `Assets/Scenes/CM_CrookedMortar_EntranceWorkflow11_Review.unity`.
Separate derivative of ShopWorkflow10. Production02 and Workflows07–10 are unchanged. Artistic approval pending; no production integration.

## Construction and scope

Only the inside entrance bay (x2.23–5.40m, y0.20–3.30m) is reconstructed. The 2.00m opening, existing door and 105-degree outward swing are preserved. Radially fitted voussoirs, varied jamb course heights, continuous recessed mortar bedding, selected actual chisel chips and curved lime spandrels replace the loose-looking inner ring. Broad chamfered posts, housed knees, flush pegs and a genuine two-part scarfed wall plate establish a restrained structural frame. Broad 2.5mm trowel undulation and one shallow repaired lime coat supply material depth without dense sculpt noise or decorative overlays.

The previous exterior-facing stone and other interior plaster are retained as two exact clipped derivatives of their original meshes. Only the two original renderers listed in Installed.json are disabled; reusable source assets remain intact. No added loose clutter, lights or colliders. Existing posters/stock shown in comparisons are baseline objects, not additions.

Editable source: `CM_EntranceWorkflow11.blend`; separate hidden editable parts and visible joined game exports. Three FBX modules: masonry 10,568 triangles; lime 2,956; timber 4,120. Total new geometry **17,644 triangles**. Retained derivative meshes add 14,874 exterior-stone and 925 other-plaster triangles; they replace corresponding old renderers and are not additional new designs. These costs are modest for the experiment but still need profiling/LOD consideration before wider production use.

## Materials and reproducibility

Metric Blender source; established axis conversion/export (+Y Unity up, existing facade orientation). build_entrance11.py creates the initial candidate using the proven Workflow08 shaping helpers. RefineSurfaces.py operates on that initial source, applies four selected boolean chips, front-face trowel refinement, face-projected stone UVs and rejoins/exports only changed parts. CleanUV.py removes boolean-created unused UV layers. **Do not repeatedly run the refinement on the already-refined source**: it is a one-time recorded operation, not idempotent.

Warm matte walnut is shared unchanged from Workflow09. Existing Workflow10 paint supports plaster. New `PaintedStone.png` is an AI-generated gouache albedo field, not a photograph, render, normal map or baked lighting; packed in the Blender source and imported as a 2048-max sRGB matte URP base map. See Prompts.md. Actual courses, joints and chips are geometry; no painted block-outline trick. Individual face UV regions sample the shared painted field at controlled scale. Source remains editable; the new materials are confined to Workflow11.

## Comparison and honest assessment

Previews/Comparison contains matching DoorGameplay, AngledGameplay, ConstructionClose and SectionClay pairs. Captured from actual Unity Play-mode Game view, with identical light settings and exact before/after camera transforms/FOV. Gameplay cameras are sampled from the existing orbit controller, then pinned across each comparison. Clay temporarily neutralizes affected original/new materials; context remains unchanged. Player/camera/renderers are restored afterward.

The result has appreciably tighter construction, a more coherent arch/frame and warmer illustrated stone. The clay comparison demonstrates actual geometric change. **It does not yet achieve the reference's rich architectural artistry.** At gameplay distance this is a restrained/incremental visual improvement, not a breakthrough. The frame remains fairly straight; mineral paint is still a general surface field rather than individually art-directed stone history. The existing door's straight boards, repeated wood grain, flat cyan glazing and broad unarticulated surrounding surfaces remain visible limitations. No claim of final beauty or artistic approval is made. Further work should use an artist-authored joint/edge paint pass and more purposeful large-form shaping, rather than adding clutter or more microgeometry. Other room work is outside this test.

## Targeted validation

- SourceValidation.json: all 42 editable/export mesh objects have one finite UV layer, valid finite normals/positions, zero degenerate triangles; metric scale retained. Visible game geometry is 17,644 triangles (validation counts source copies too).
- IntegrationValidation.json: imported UV/normal counts correct; no missing scripts/materials; all **116 existing colliders unchanged**, zero additional permanent colliders; **43 door-swing poses** clear against new/retained visible triangle meshes.
- ClearanceValidation.json: **190 static capsule-volume samples** using unchanged 2m height/.4m radius; entry, customer aisle, staff aisle, stair connection and kitchen connection pass.
- ProtectionValidation.json: **291 protected file hashes unchanged**, including Production02 and prior workflow files.
- Current Unity compilation succeeds. Capture arming caused one Pipeline main-thread timeout logged as a tool error; the armed capture subsequently completed and restored state. Two previously retained Console warnings remain. No new observed mesh/import/gameplay exceptions. Console was not cleared to hide history.
- Not performed: fresh real-input E-key interaction, full live stair/exterior regression or manual camera-comfort approval. This is a non-collision-changing art test; static sweep/clearance and Play-mode visual comparison are the proportional checks, not substitutes for manual playtesting.

Review scene is saved, stopped, one loaded scene/AudioListener; player and existing orbit camera enabled. No gameplay, input, camera, lighting or project settings changed. Nothing committed or pushed.
