# Briarwick Environment06 Revision01 — landscape refinement candidate

2026-11-05. Existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`; no new scene. **Candidate for visual review, not approved final landscaping.** No Git operations, commits, pushes, branches, new packages, build or global render-setting changes.

## What changed

- Reduced native instanced Terrain detail maps from **84,204 to 22,914** (−72.8%). Every retained cell is a subset of the prior map; no vegetation expansion or tree regeneration.
- Replaced only this terrain's first two prototype references with owned **18-triangle short-grass meshes**, versus128/168 triangles for the old grass prototypes. Three offset curved strips reuse the lower blade portions of existing GrassFlowersFREE grass01/02 textures; no custom framework, new shader or wind system. Physical height approximately0.15–0.31m after prototype variation. Upward shading normals avoid dark upright-card faces. Existing larger fern/heather/flower prototypes remain in smaller, coherent patches.
- Disabled **199 of310** coarse Environment05 filler chunks, retaining111 and all source mesh assets. Removed258,405 submitted mesh triangles from those chunks (463,352→204,947 across these low-plant chunks). These are separate from native detail counts. Every disabled path is in Integration.json. WoodlandSkirts and CreekBanks retain a higher share; all trees, trunk colliders and approved Woodland01–04 objects are untouched.
- Two owned TerrainLayer derivatives share a new opaque painted short-turf diffuse.7.5m tiling, muted green/dry remaps, no glossy alpha, normal or mask texture. Existing moss/soil/pebble/rock/mud layers retained.62377 of65536 alphamap texels blended to distinguish yards, broad meadow/dry communities, woodland ground, creek earth and slope rock, and soften worn road margins. Terrain heights and road meshes unchanged.
- Native detail distance95→80m on this Terrain component only; density multiplier remains1. The continuous ground material supplies the far surface; vegetation culling is still visible at some high views.

## Counts

| Native detail type | Before | Revision01 |
|---|---:|---:|
|Grass_A → short grass|30,428|9,627|
|GrassDry_B → dry short grass|41,246|11,858|
|Fern_A|5,663|750|
|Heather|1,695|184|
|Low flowers|971|92|
|Meadow flowers|4,201|403|

|Region (mutually exclusive reporting masks)|Before|Revision01|
|---|---:|---:|
|DistantCountryside|20,784|3,460|
|Hillsides|29,376|7,494|
|Meadows|14,024|4,863|
|CreekBanks|5,145|2,360|
|VillageMargins|6,118|816|
|WoodlandSkirts|8,757|3,921|

Exact regional/type breakdown and chunk removals: [Integration.json](Integration.json). Region labels are geographic reporting masks; not newly created vegetation groups. Ferns are retained principally in woodland and damp creek areas, heather reduced to a few suitable patches, flowers retained in fewer existing noise-defined colonies. Large-scale shorter grass distribution has open intervals rather than uniform coverage. Native potential geometry across every placement fell13,441,180→717,922 triangles (not per-frame rendering, excludes trees/buildings/coarse chunks/shadow passes).

## Local grass/material test and source

Before widespread assignment, TestShortGrass.cs rendered a small meadow subset on a disposable TerrainData clone and restored all original references in finally. ShortGrass_LocalTest.png records that experiment, not the exact final broad composition. It exposed an inappropriate sheen with automatic high-quality BC7 import; switching only the owned diffuse to the project's opaque RGB BC1/DXT1 convention removed the sheen. Runtime paired profiling then checks the deployed candidate against the original, with the final references/maps/distance/chunk states.

One built-in ImageGen short-turf source is preserved under `ArtSource/Paint/Environment/Briarwick/Environment06_Revision01/ShortTurf_Painted_Source.png`; import1024² opaque BC1 with mipmaps, approximately0.67MiB GPU storage. Generated source1254². Source prompt in TextureSource.md. This is an opaque diffuse/albedo illustration, not generated geometry or a global grass shader. It is conceptually tileable; artistic edge/repetition approval remains necessary. Two mesh materials use unchanged imported alpha textures and URP/Lit cutout, double-sided, no cast shadows. No imported originals edited. Persistent new project assets are under `Assets/BlightBloom/Art/Environment/Briarwick/Environment06_Revision01/`.

## Matched measurements

|View|PlayerLoop ms|Render thread ms|GPU counter ms|Draw calls|Triangles|
|---|---:|---:|---:|---:|---:|
|Village common|13.89 → 10.69|16.50 → 12.75|25.88 → 20.70|2,249 → 1,453|7.75M → 4.17M|
|Woodland interior|13.20 → 10.51|17.02 → 12.74|24.58 → 20.39|2,056 → 1,415|4.63M → 1.15M|
|Meadow|13.51 → 7.82|14.54 → 11.35|31.18 → 21.59|2,968 → 1,981|8.28M → 2.62M|
|Creek bridge|13.11 → 10.06|13.93 → 13.08|26.07 → 19.40|2,840 → 1,934|6.06M → 2.68M|
|Open hillside|12.86 → 10.64|14.74 → 12.91|28.50 → 19.54|2,751 → 1,809|7.30M → 2.54M|
|Building approach|12.72 → 7.80|15.93 → 9.34|23.23 → 20.28|2,253 → 1,469|5.07M → 2.77M|

Values are medians of50 sampled frames after20 warmup frames per view/phase,600 samples total. All six before/after positions use the same camera, lighting, Editor settings and background/focus conditions. ProfilePaired.cs swaps only a disposable runtime TerrainData clone plus the199 filler active states and detail distance, then restores normal runtime state. No source asset is restored/rewritten for profiling. An earlier independent baseline/after capture also records120 frames per view in ProfileBefore.json/ProfileAfter.json and agrees on the rendering reduction.

**Limits:** counters include the running Editor, open views, shadow/depth passes, background scheduling and profiling overhead; they are not isolated single-camera draw counts or standalone-game FPS. Main Thread median remains around100ms in both states under background Editor scheduling, so that total is not evidence of a CPU workload improvement. PlayerLoop and CPU Render Thread Frame Time are separately sampled nonzero counters. GPU Frame Time also returns valid, nonzero samples; these are actual Unity profiler counter readings in this Editor session, not inferred GPU performance or a standalone GPU capture. WaitForTargetFPS returns0, so it does not isolate the background idle time. Batch count is not independently exposed by this sampler. Transparency pixel coverage/overdraw is not instrumented: fewer/smaller strips and patches suggest lower risk but do not quantify overdraw.

The terrain clone keeps both before/after maps/resources resident, and Editor memory includes both views/assets. Memory counters are in PerformanceSummary.json; do not interpret them as a clean player-build memory delta. No repeat standalone build: the prior baseline is outdated, its build took~33minutes and triggers writes to protected configuration files. A new build is inappropriate without resolving that protection/approval first. Existing world/building and tree costs remain substantial despite lower grass cost.

## Error investigation

[NullReferenceTrace.txt](NullReferenceTrace.txt) contains the actual historical Editor.log stack: UnityEditor.WindowLayout.FindRootSplitView→MaximizePrepare→Maximize→MaximizeKeyHandler→MaximizeGestureHandler. No Locomotion03, imported foliage or project gameplay frame appears. This explains the available exception as an Editor layout/maximization failure; it does not prove every past NullReference has that cause. It has not reappeared in the current normal Play-mode/collision/profiling tests. No speculative gameplay repair, Editor layout reset or settings normalization was performed. If it recurs, capture that instance's full stack separately.

## Validation and preservation

- Automated Play-mode existing CharacterController.Move:20 route runs pass, including three bridge/main-road lanes in both directions, creek banks, hills, meadow, farm and woodland.22 building approaches pass, stopping before static doors (not playable interiors).
-102 trunk blocking tests pass;40 camera-equivalent sphere casts along the woodland route found4m clearance at sampled headings. These checks do not establish manual camera comfort throughout the landscape.
- Normal-input Locomotion03 validation and final integrity/hash results: see final verification section below; not to be inferred from route probes.
- Before-state scene and TerrainData are preserved as `.before` files in this review directory; six complete detail maps, alphamaps, heightmap, prototype/layer configuration, scene-component snapshot and protected hashes are also saved. No source assets deleted. To roll back, explicitly restore the saved scene/TerrainData with Unity safely unloaded from those assets; preserve their existing .meta/GUIDs. Do not overwrite loaded assets blindly. The separate detail/alpha snapshots and disabled-path list permit narrower restoration.
- Protected five settings files, Production02, player/scripts/controller/camera/animation, all eleven building placements, roads, creek, bridge, approved trees and imported/source assets are subject to final hash/component checks. Earlier uncommitted work is retained, never reverted.

## Artistic assessment and remaining limitations

The counterexample to the prior clump blanket is now visible: much clearer negative space, lower plants near buildings, fewer unsuitable isolated ferns and flower specks, with a continuous painted turf surface beneath them. This is a measurable clutter/cost reduction, **not a claim of finished storybook art**. Broad ground still reads too uniform in some views; the generated leaf/grass stroke pattern repeats, dry tint is olive, and short mesh strips remain identifiable up close. Sparse flowers and retained older heather/bush chunks need manual composition review. Hard road-mesh outlines cannot be fully removed by painting the underlying Terrain; road geometry/material redesign was not part of this pass. Terrain horizon, sky/background, forest edge density and tree-card appearance remain prior limitations. No global lighting or atmosphere overhaul was used to hide them.

Review matched screenshots in [GALLERY.md](GALLERY.md), including woodland interior, meadow, creek, hills, building surroundings and four static third-person pairs. Review in the saved scene at player height before approving density/material direction. Next work should follow that review, plus a separately authorized standalone performance capture; no expansion is proposed now.

## Final verification / handoff

- `Validation.json`: saved scene, **zero unexpected changes** among prior scene objects/components; the200 allowed changes are199 filler active flags plus Terrain detail distance. New root is a revision identifier only. Existing buildings, terrain transform, roads, creek, bridge, tree objects, colliders, player/camera/input/animation component data match the start snapshot. All active mesh UV/normal counts and finite vertex checks pass; no unsupported/missing material or missing script found. All six native prototypes validate and use instancing; eight terrain diffuse references resolve.
- `ActualDetailTransforms.json`: actual native instance transforms across all1024 patches total22,914, exactly matching the six revised detail maps. No cell increased over its before map. Detail density remains1, resolution512,16cells per patch.
- Heights are byte-identical. Terrain weights contain no NaN, negative or out-of-range values. Stored eight-channel UNorm8 weight sums span0.988235–1.011765, within the expected±8/(2×255) quantization tolerance. Baseline span was0.988235–1.015686; a too-strict initial0.002 sum test was corrected after checking actual baseline/after quantization, not by hiding invalid samples or rewriting the surface.
- `ProtectedVerification.json`: refreshed hashes of4430 existing scoped source/asset/config files find **only the intended Briarwick scene and TerrainData changed**; none missing. All five explicitly protected settings files and Production02 are byte-identical. Existing source/imported libraries are not modified. Review documentation updates are listed separately.
- Current Unity Console:0errors/0warnings, compilation not failed/in progress. Captured log cursor64 remains unchanged from the beginning of this task; its older retained11error/50warning entries were not cleared or counted as new. Historical WindowLayout exception did not recur in this run.
- **Normal-input follow-up passed:** after the Mac was unlocked and Game view retained focus, the reused LiveInput.cs probe completed all5outbound and7return waypoints through unchanged TraversalInput, ThirdPersonMotor, orbit camera and Locomotion03.207samples:207grounded; Idle/Walk/Sprint observed, speeds reaching3/6m/s,91.96°orbit response, minimum sampled camera distance3.85m.188distinct left-elbow and187left-knee rotation samples support active articulated animation. Runtime idle/sprint screenshots are saved and the sprint capture was visually inspected. This is automated input-path validation, not manual playtesting or a general camera-comfort approval. Previous focus-timeout/interrupted attempts are retained separately; no focus guard bypass or gameplay edit. Final test restored normal devices/player state and Play mode was stopped safely.
- `InputResumeVerification.json`: scene, TerrainData, Production02 and all five settings hashes remain identical to their pre-input-test values. Console remains0errors/0warnings with no new captured entries or compilation failure.
- Scene remains open, saved, in Edit mode for review. About9.5GiB free at the final disk check. No Git operations performed.

Changed-file scope: [ChangedFiles.txt](ChangedFiles.txt). Comparison gallery includes12matched regional pairs plus4static third-person pairs; no unrecorded layout/lighting changes are used for the comparison.
