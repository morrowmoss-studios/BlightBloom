# Briarwick Environment06 — botanical and village-wide landscape review candidate

2026-11-05. Saved in existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, Edit mode, Environment06 selected. **NOT VISUALLY APPROVED. User review identifies excessive vegetation clutter, artificial ground and rendering performance requiring improvement. No further vegetation/expansion is authorized. All five settings/profile files are to remain unchanged pending explicit approval.** No new scene, buildings, architecture changes, trees, gameplay mechanics, commits or Git operations.

## Important preservation exception

Scene-object preservation passes, but **file-level preservation is not fully clean**. Of4,430 protected files, seven differ: intended Briarwick scene/TerrainData plus these five settings/profile files:

- `Assets/Settings/DefaultVolumeProfile.asset`
- `Assets/Settings/PC_RPAsset.asset`
- `Assets/Settings/UniversalRenderPipelineGlobalSettings.asset`
- `ProjectSettings/ProjectSettings.asset`
- `ProjectSettings/UnityConnectSettings.asset`

Their timestamps align with the optional standalone build/its aftermath. No explicit API call edited rendering/player/cloud settings, but the pre-task baseline contains hashes rather than contents, so **whether these differences are serialization-only or contain value changes is unverified**. They have not been blindly reverted. Current copies are retained in SettingsReview; ProtectedVerification.json lists exact differences. User has now supplied the GitHub Desktop comparison and explicitly instructed retaining all five files unchanged. The subsequent installed-source review is documented in SettingsReview/TechnicalReview.md; specific setting changes still require approval. Do not claim all project settings are unchanged or automatically approve these differences. No Git operations were used to inspect/recover them.

## Survey, scope and art assessment

Reviewed the full320×320m landscape, eleven sites plus stable/farmstead, roads/common, creek/bridge, meadows, slopes and approved Woodland01–04/Environment02–05. PLAN.md records the pre-placement priorities. Existing Environment05 baseline remained79,032 details/four instanced prototypes. Existing nature/terrain libraries were checked again: trees/shrubs/grasses/ferns are available; no suitable standalone loose rocks/logs/roots or dedicated reeds were identified. Tree-branch textures are not standalone debris assets. No architectural rock-floor substitutes.

The new `Assets/ALP_Assets/GrassFlowersFREE` pack contains twelve alpha-textured grass/flower images, demo terrain and a post-processing preset, not a ready URP foliage-prefab library. PackageInspection.json/contact sheet cover resolution, alpha coverage and import settings. The demo and post-processing preset were not applied. Four restrained pale-blue/white/pink images were chosen; vivid red/violet variants deferred. These are decorative designs, not researched medicinal species or gameplay plants.

A24-clump temporary test rendered successfully in existing scene lighting and was removed. FlowerCompatibility.png shows the suitability assessment. Flowers provide readable small accents at third-person scale; close inspection can still reveal source-card construction. This is not bespoke hero botanical art.

## Created assets and integration

Under `Assets/BlightBloom/Art/Environment/Briarwick/Environment06/`:

- One1024² RGBA atlas copied/downsampled from original grassFlower01,06,10,02 textures, without modifying source imports.
- One shared matte, double-sided, alpha-clipped URP/Lit material: cutoff0.45, metallic/smoothness0, instancing enabled; atlas mips preserve alpha coverage. BC7 alpha is intentional for foliage, unlike opaque terrain albedos.
- Two editable Unity mesh assets/prefabs, **24 triangles /30 vertices each**: LowFlowers and MeadowFlowers. Three offset bowed, alpha-fitted four-section strips reduce full rectangular card area. Curvature/offsets, scale and rotation provide volume; no claim that cards are eliminated from every close angle.
- Native Terrain detail layers4/5; no per-clump GameObjects, colliders or runtime gameplay scripts. Existing four detail maps remain **byte-identical**. Generator/source scripts provide editable geometry/UV construction; no new Blender source was needed for these lightweight detail meshes.

**79,032 →84,204 native instances: +5,172 flowers.** Original30,428 green grass,41,246 dry grass,5,663 ferns,1,695 heather retained. New971 low and4,201 meadow clumps. **4,983/5,172 (96.35%) lie outside the original grove rectangle**, so development is not concentrated in the original quadrant.

| Region | New clumps | Treatment |
|---|---:|---|
| Village yards | 666 | Differentiated maintained access, working yards and residential side/rear colonies |
| Common/path margins | 200 | Small irregular low colonies outside road/approach buffers; open common retained |
| Meadows | 1,510 | Loosely grouped flowering accents among unchanged mixed grasses |
| Hillsides | 2,285 | Lower-rate colonies across the larger slope/boundary area, soil/dry surface variation retained |
| Creek banks | 227 | Restrained flowers outside water, with damp-ground blends; no false reed substitution |
| Woodland transitions | 284 | Sparse clearing/edge accents, no extra trees or relocation of undergrowth |

Existing eight terrain layers reused, no ninth layer/pass. **10,372 control texels measurably differ** from the immediate baseline at0.004 weight tolerance;10,440 were processed by integration. Worn access gradients, working-yard earth, greener dwelling margins, damp banks and route-side dry blends refine the previously painted terrain. Heights unchanged; original grove ground paint preserved. Common/plots, water and practical approach areas remain open. Every planned building area received surface treatment and modest flowers:

| Site | Yard flower clumps | Processed nearby control texels |
|---|---:|---:|
| Crooked Mortar | 42 | 503 |
| Inn | 62 | 507 |
| Blacksmith | 74 | 474 |
| Bakery | 65 | 610 |
| Merchant | 8 | 462 |
| Elder cottage | 59 | 289 |
| Farmhouse/stable area | 76 | 649 |
| Miller's cottage | 33 | 420 |
| Chapel | 39 | 527 |
| Family Cottage A | 145 | 427 |
| Family Cottage B | 63 | 405 |

These are disjoint nearest-site yard masks, not species labels or identical garden designs. Stable/farm circulation and cultivated plot reserves are excluded. Village and countryside markers are organized under `Environment06 - botanical village landscape`; actual vegetation maps live in the existing TerrainData, not renderer children that can be toggled individually.

## Performance assessment

Before placement, existing instancing/materials,95m distance, density1 and the prior47–53ms Editor audit were reviewed. A standalone baseline **build succeeded** on the unchanged macOS/Mono target, explicit Briarwick scene, Development/DetailedBuildReport, output outside the repository:

`/private/tmp/BlightBloomEnvironment06Baseline/BriarwickBaseline.app`

1,211,758,377 bytes; build time1,995.06s, largely first Metal shader compilation;0 errors,3 warnings: no runtime Pipeline config, imported LightFlickerEffect CS0109, and Unity native-symbol upload403. No settings/target/build-list API change was requested; see unresolved automatic settings differences above. Desktop launch hung and was interrupted. **No standalone runtime FPS/CPU/GPU measurement is claimed.** Build success alone is not a performance baseline measurement. No repeat build was performed.

Bounded additions use24tri clumps versus existing128–360tri sources. Entire-map new potential geometry **124,128 triangles**, approximately0.93% of the old13,317,052 whole-map detail potential. This is NOT a simultaneously rendered count. One new material/atlas, two prototypes,0 new scene renderers/colliders. Atlas Editor runtime-memory allocation2,797,232 bytes; existing terrain-layer texture allocation100,678,608 bytes unchanged. Distance95m, density1 and patch resolution512/16 unchanged. No mesh LOD chain added; culling remains distance/patch based. Small silhouettes and alpha fitting help, but clipping/overdraw and patch submissions still cost rendering work.

A successful **720-frame matched Editor Play-mode comparison** used runtime-only TerrainData clone: immediate baseline paint with new maps empty versus new paint/maps, same player/camera poses,120 samples per view after30 warmup frames. Original asset never modified by profiling; clone removed and all references/background flag restored. Early profiling attempts collected zero frames while the application was not advancing; they are not used for conclusions. Final sample duration25.0s, all720 samples focused.

| View | Editor draw calls before→after | Triangle counter before→after | Main Thread median before→after(ms) | Main Thread p95 before→after(ms) |
|---|---:|---:|---:|---:|
| Woodland | 1,817→1,998 | 5,663,162→5,686,490 | 28.86→28.16 | 47.19→44.81 |
| Meadow | 1,248→1,402 | 5,368,783→5,385,775 | 29.69→29.40 | 49.66→45.90 |
| Village | 1,584→1,773 | 5,192,564→5,235,140 | 22.94→23.18 | 36.30→38.54 |

**Editor/tooling/view/pass/wait overhead is included.** Do not infer a speedup or standalone FPS from small timing variation. Added draw submissions154–189 are real reported overhead despite small geometry. Baseline/after both have candidate assets loaded and a runtime clone; memory counters include allocations/cache/GC effects. Approximately5.02–5.14GB Total Used Memory and5.92GB reserved were observed; not standalone player memory or VRAM. No GPU timing was collected. Current data supports bounded first-pass integration, **not production performance sign-off**. A controlled target-build/GPU profile remains necessary before density/distance expansion. No approved vegetation was removed to hit arbitrary counters.

## Validation results

- Saved scene contains84,204 actual computed native instances. Original four maps byte-identical; all six prototypes valid/instanced; no missing references/imports/new mesh UV/normal defects; supported URP material.
- **1,198 pre-existing scene objects/components: zero unexpected changes.** Buildings, roads, creek, bridge, approved woodland, colliders, controller/camera/input/animation setup preserved. Terrain heights byte-identical; protected grove paint mismatches0.
- **20 main-route/bridge/meadow/hill/bank/farm/woodland CharacterController.Move runs passed/grounded**, both directions.
- **22 approach runs passed/grounded**, both directions for all eleven sites; stop before static village doors. No claim of opening static village doors or exploring unfinished interiors.
- **102 replacement-tree blocking tests passed**,40 sampled camera-equivalent casts retained4m clearance. Scene collider preservation also checked. Not a manual camera-comfort claim or exhaustive building-triangle sweep.
- **Normal-input Play-mode Locomotion03 route passed**: virtual gamepad/mouse events, walking/sprinting/idle/stopping/orbit, five outward/seven return waypoints,202 runtime samples. No direct clip/motor method calls during that route. Automated runtime validation, not manual playtesting. All temporary devices/probe state restored.
- All5,172 new source-cell placements pass building/plot, path, water and slope masks. Minimum cell-center distances:1.405m outside road edge,4.218m from creek axis. Buffers allow source radius/jitter. This is conservative mask validation, not exhaustive triangle intersection testing; natural plant overlap is allowed. No new solid obstacles.
- Final Console **0 current errors /0 warnings**, no compilation failure. Captured cursor64 unchanged during final tests. Build warnings above remain in the historical log, not hidden or fixed by editing third-party code. No Console-clear command used.
- File check:4,430 protected files, only scene/TerrainData plus five settings exceptions differ. Original imported pack, all original building/woodland/player assets and source scripts unchanged. This exception is unresolved and prevents a fully clean preservation sign-off.

## Visual review and unfinished work

GALLERY.md links eleven matched before/after landscape views: full overview, village core, meadow, hills, roadside, creek/bridge, woodland edge, east/west village, farmstead and northern homes. Four additional static third-person composition views cover meadow, west/east village and creek approach. Two actual normal-input runtime captures plus pack contact/compatibility views retained. Same review cameras/lighting, no editing gizmos or dramatic reframing to conceal sparse areas.

Improvement is visible at player height in modest flower colonies, dwelling/working-yard differences and connected road/meadow margins across the whole village. **It is not a finished richly illustrated landscape.** The high overview remains comparatively simple because of95m detail culling, unchanged fog and blockout geography. Existing road/bridge/creek/plot edges remain rigid; they were not redesigned. Close foliage-card artifacts/repetition remain possible. Suitable loose rocks/logs/roots/branches and dedicated reeds remain missing. No medicinal gathering/crafting/species labeling, NPCs or unrelated systems were added.

Next priorities, not begun: resolve settings discrepancy against pre-task versions; manual visual/traversal review; controlled standalone/GPU/overdraw profile; approved biome-specific debris/reed assets and later village geography/architecture refinement. Do not expand plant density or detail distance until those reviews.

## Files and state

Intentional Unity edits: Briarwick scene and its existing TerrainData. New owned assets: Environment06 texture/material/two meshes/two prefabs and metadata. Reports, snapshots, guarded tools, profiler data and captures: this directory. Unexpected settings files are listed at top and included in ChangedFiles.txt; current copies preserved for review. No destructive recovery attempted.

Scene saved/open in Edit mode, Environment06 selected. Normal gameplay components enabled. Guarded Integrate.cs must not be reapplied over the saved scene. Original source/prototypes/maps and source-pack assets remain available. Baseline development build is temporary outside repository; no cleanup/archiving performed. Disk headroom approximately10.9GiB at final check. **No commits, pushes, branches or Git commands. Environment06 is not visually approved; stop for explicit approval before settings or landscape corrections.**

## Subsequent technical review

User supplied GitHub Desktop findings for all five files and instructed retention without blind reversion. See [Settings technical review](SettingsReview/TechnicalReview.md) for installed URP17.4 source evidence, required-versus-derived distinctions, unexplained UnityConnect enable, and unreferenced Editor-test subassets in the default profile. Earlier candidate assessments are superseded by the user’s **not visually approved** decision. No settings or landscape change was made during that documentation review.
