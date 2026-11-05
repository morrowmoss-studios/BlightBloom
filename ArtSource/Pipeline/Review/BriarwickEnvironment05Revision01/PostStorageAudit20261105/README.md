# Environment05 Revision01 — post-storage recovery audit

2026-11-05. **PASS: the saved environment is intact; no recovery repair or regeneration was necessary.** Briarwick remains open, saved and in Edit mode. This audit changed no scene, terrain, prefab, material, texture, mesh, script, gameplay or rendering configuration. No Git operations.

## Integrity and completeness

Reloaded `Assets/Scenes/Briarwick_Hamlet_Dev01.unity` from disk in the existing Unity 6000.4.5f1 Editor. It opened successfully with its existing TerrainData. No full reimport, cache deletion or second Editor.

- All **84** prior deliverable-manifest files exist and are non-empty. Four new 1024² PNG sources pass chunk CRC and zlib-decompression checks.
- **912 scene dependencies** checked: no missing files, missing prefab instances, unsupported/error shaders or failed Revision01 main-asset loads. Serialized-reference scan found no broken references; scene missing-script count is zero. Relevant imported meshes have valid UV/normal array lengths and finite positions.
- Editor is neither compiling nor importing; no compilation failure. Final Console has **0 current errors and 0 warnings**, and its captured cursor remains57: no new messages during the audit. Historical captured logs were not cleared. The four earlier default-platform format errors did not recur.
- The corrected ground imports remain alphaSource=None, ordinary compression, AutomaticCompressed default selection, actual DXT1/BC1. Terrain-layer metallic/smoothness remain zero. No renewed sheen or missing-texture appearance in current Play-mode captures.
- All **1,141 pre-Revision01 objects/components** pass the preservation comparison with only the documented intended overrides allowed. Approved Woodland01–04 real placements, buildings, roads, creek/bridge geometry and gameplay setup are preserved. Heights are byte-identical to the recorded baseline; approved grove paint has zero mismatches at control-texture quantization tolerance.
- **4,389 protected/current asset and configuration hashes** were compared before/after this audit: **zero changed files**. This verifies audit preservation; it is not a claim that all files have a pre-storage final hash. Disk-loaded data/count checks establish the saved revision's completeness.

## Reported work independently verified

| Item | Current result |
|---|---|
| Actual native Terrain detail instances | **79,032** |
| Green grass / dry grass / fern / heather | 30,428 / 41,246 / 5,663 / 1,695 |
| VillageCore | 2,948 |
| Meadowland | 14,546 |
| ForestEdges | 23,252 |
| CreekCorridor | 5,610 |
| Hillsides | 32,676 |
| Changed terrain-control texels | **61,112**, matching final layer-weight averages |
| Road/common worn-earth material overrides | **15** |
| Cone positions resolved | **58**: 51 new real trees + seven covered by existing trees within6m |
| Active remainder cone objects | **0**; both combined references remain disabled |

Counts were recomputed from saved density maps and Unity's actual instance-transform output, not assumed from old JSON. Geographic totals were independently reclassified using the existing geographic masks. All match the previous report. New tree positions/types were compared to TreeReplacement.json, all seven existing-tree overlaps were checked, and all original reference objects remain available.

Eight terrain layers, valid normalized painting, all four instanced detail prefabs/materials and the regional ground changes are present. No building/road/water exclusion violations were found among detail map placements. No missing or incorrectly saved environment change was identified.

## Current gameplay validation

- **20 CharacterController.Move route runs passed and grounded**, both directions, including three main-road/bridge lanes, meadow, eastern/western hills, creek banks, farm access and woodland connection.
- **102 trunk blocking checks passed** at the 51 replacement trees. Forty camera-equivalent casts returned4m clearance at sampled woodland positions. These casts do not establish manual camera comfort.
- Focused Play-mode **normal-input** test passed through unchanged TraversalInput, ThirdPersonMotor, Locomotion03 and orbit camera: walking, sprinting, stopping/idle, five outward/seven return waypoints and camera orbit. All stage summaries grounded; **206 runtime samples**. Virtual gamepad/mouse state events were used; no direct animation/motor calls during the route. This is automated runtime validation, not manual playtesting.
- Temporary controller probes, input devices and profiling viewpoints were restored. Play mode exited; motor/input/controller/orbit enabled, one player/camera/listener, scene not dirty. Source controller dimensions, speeds, animation controller, camera and interactions unchanged.

Current idle/sprint PNGs provide two focused visual checks. They show the saved ground coverage and tree materials functioning in Play mode, with existing card silhouettes/repetition still apparent. No new full comparison-render suite was generated.

## Rendering configuration and measured limitations

Unchanged: 512² detail resolution,16 cells/patch (10m), InstanceCountMode, density1, **95m distance**, four validated instanced mesh prototypes using URP/Lit with instancing enabled. No per-clump GameObjects/colliders. No detail mesh LOD chain. Eight terrain layers imply multiple splat passes; exact pass cost was not isolated with Frame Debugger. The far overview remains less lush because details cull at95m and existing atmospheric presentation is unchanged. Card edges/repetition and cutout overdraw remain known quality/performance limitations, not storage corruption.

Available Unity ProfilerRecorder counters captured **360 focused Play-mode frames**,120 per viewpoint after30 warmup frames. Capture duration29.15s. Existing third-person camera was used at temporary woodland, meadow and village positions; all restored. First unfocused profiling attempt collected no frames and was replaced by this successful capture. No global Profiler/rendering setting change.

| View | Main Thread median / p95 (ms) | Editor draw calls | Render triangle counter | SetPass counter |
|---|---:|---:|---:|---:|
| Woodland entrance | 47.44 / 106.77 | 1,955 | 4,556,380 | 70 |
| Open meadow | 48.29 / 162.78 | 2,852 | 8,383,103 | 85 |
| Village approach | 53.22 / 112.45 | 2,138 | 7,034,706 | 78 |

**These are Editor measurements, not standalone performance or vegetation-only counts.** Main Thread includes Editor/tooling/waits; render counters include active Editor views and passes. They do not identify CPU versus GPU bottlenecks or establish target FPS. Elevated costs warrant a separate profiling milestone before density expansion.

Profiler Total Used Memory counter was approximately4.88–4.91GB, reserved5.81–5.83GB, managed0.936–0.937GB during capture. A separate Unity allocator API snapshot afterward reported2.72GB allocated/3.39GB reserved; these have different scopes and must not be treated as interchangeable or GPU memory. Existing terrain-layer texture allocations report100,678,608 bytes including reused sources; four derivative albedos5,596,416 bytes total. No clean-player memory budget was measured.

Frame timing returned **GPU time0**, which is unavailable/invalid for a measured GPU claim. **No GPU performance result is asserted.** Raw per-frame samples and min/median/p95/max summaries are retained.

Existing hierarchy geometry:551,988 triangles,379 renderers,448 submesh submissions and13 materials for Environment05 including earlier work. Replacement trees contribute70,044 triangles/51 renderers. Native details have13,317,052 whole-map potential triangles before culling; this is not the number drawn simultaneously.

## Repairs, changes and next priorities

**Repairs performed: none.** No vegetation placement, baking, recoloring, density change, reimport or environment expansion. A diagnostic C# evaluation initially referenced an unavailable Editor statistics property; corrected in the audit-only utility before sampling, without project compilation or runtime errors.

Recommended next priorities, not begun:

1. Obtain manual exploration/visual approval at village, meadow, banks and forest edges; especially culling transitions and close foliage cards.
2. Profile a representative standalone build on target hardware, including GPU/overdraw, shadows, terrain passes, detail patch submissions and memory. Use evidence to choose LOD/culling/batching changes; do not blindly increase density.
3. With separate authorization, address missing purpose-built rocks/logs/branches/reeds and remaining biome/field composition. Existing blockout bridge/creek/road/terrain-edge geometry remains a distinct later milestone.

Current filesystem free space: **11,853,336,576 bytes (~11.04GiB)** at final check; less than the approximate14GiB estimate but sufficient for this small audit. No storage cleanup performed.

Created only this `PostStorageAudit20261105/` evidence directory (reused audit/probe scripts, JSON, profiler samples and two PNGs); updated the parent ISSUES.md with recovery/performance status. Existing report/source outputs preserved. AssetPreservation.json records zero asset/configuration changes. No commits, pushes, branches or Git commands. **Stop for review.**
