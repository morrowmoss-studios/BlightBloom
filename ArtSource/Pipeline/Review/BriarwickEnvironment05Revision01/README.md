# Environment05 Revision01 — landscape-wide review candidate

2026-11-04. Existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, saved/open in Edit mode. Revision01 selected inside Environment05. **Stop for visual approval.** No new scene, terrain, packages, gameplay, lighting/settings or Git operations.

## Changes and coverage

The prior pass had zero Terrain details, 2,372 clustered plants across 102,400 m² and 58 visible cone pairs. `AUDIT.md` records the full regional survey before planting. This revision substantially improves player-height coverage throughout the existing valley; it is not final landscape art.

- 61,112 / 65,536 control texels revised (93.25%). That measures painting, not artistic completion. Original approved grove weights remain unchanged within texture quantization tolerance.
- Four project-owned softened 1024² grass/dry/rock/damp-soil albedos and layers supplement the original four unchanged layers. Broad green/dry mosaics, slope exposure, creek moisture, tree shade and worn route margins distinguish land uses.
- **79,032 native Terrain detail instances**, verified via ComputeDetailInstanceTransforms: 30,428 green grass, 41,246 dry grass, 5,663 ferns, 1,695 heather. No per-clump GameObjects or colliders. Final grass scale ranges are in FinalTerrain.json.
- **All 58 remaining visible cone pairs addressed:** 51 real trees; seven positions already covered by an existing real tree within 6 m. Two combined proxy objects disabled, not deleted. Types 1/4/6/8 use varied yaw/scale, inherited trunk colliders and existing muted leaf materials.
- Earlier Environment05's 2,372 batched plants and 18 trees retained. Approved Woodland01–04 real placements preserved.
- Roads/common receive a scene-only matte textured-earth material override. Meshes, transforms, colliders and original material preserved. No building, creek, bridge or plot geometry changes.

| Regional detail mask | Native clumps | Treatment |
|---|---:|---|
| Maintained village core | 2,948 | Lower density; common, plots, footprints and approaches excluded; worn ground margins |
| Meadowland | 14,546 | Mixed-height green/dry grass and sparse heather, open sightlines |
| Forest edges / outer woodland | 23,252 | Ferns, shaded ground and real-tree replacement |
| Creek corridor | 5,610 | Damp soil/pebbles and irregular grass/fern clusters outside water and crossings |
| Hillsides | 32,676 | Dry/green mosaics, rock-ground exposure, sparser steeper slopes |

Counts are disjoint ecological masks. Fields, maintained routes, water and unsafe slopes intentionally remain open. Existing regional subgroups remain; Revision01 contains VillageCore, Meadowland, ForestEdges, CreekCorridor and Hillsides guides, with replacement trees under ForestEdges. Detail maps reside in the existing TerrainData, not scene-object vegetation groups.

## Performance and rendering

512² detail map, 16 cells per patch (10 m patches), InstanceCountMode, four instanced mesh prototypes, density 1, **95 m culling distance**. Existing prefabs' URP materials render correctly; no imported legacy Shader Graph migration. Unity documents instanced details using prefab materials and range culling: https://docs.unity.com/en-us/engine/6000.6/manual/creating-environments/script-terrain/terrain-grass and https://unity.com/blog/games/experience-the-new-unity-terrain-demo-scenes-for-hdrp-and-urp . Installed 6000.4 API/render test confirmed compatibility here.

- New trees: **70,044 triangles / 51 renderers**, two submeshes each. Existing meshes/materials reused.
- Full Environment05 hierarchy, including earlier work: **551,988 mesh triangles / 379 renderers / 448 submesh submissions / 13 materials**. Excludes native details, terrain and other scene assets. Component/submesh counts are not measured GPU draw calls.
- Detail prototypes: 128 / 168 / 360 / 268 triangles. Entire-map potential **13,317,052 triangles** if all details were drawn, NOT simultaneous gameplay cost. Visibility depends on range and patches. Cutout overdraw/shadow cost needs profiling.
- Eight layers require approximately **two terrain splat passes** instead of one; original grove layers retained. No detail mesh LOD chain exists; patch/range culling used.
- Four new albedos report ~5.34 MiB combined Editor runtime-memory allocation. All referenced layer textures report ~96 MiB including reused normals/old maps; not all new allocation. TerrainData reports ~1.36 MiB, which does not fully account for native detail buffers.
- **No GPU timing, built-player profile or target-hardware FPS claim.** Profile the approved density in a standalone build before production acceptance.

## Validation

- **20 automated CharacterController.Move route runs passed and grounded**, both directions: main-road/bridge three lanes, meadow, hills, creek banks, farm access and woodland connection.
- **102 new-trunk blocking tests passed**. Forty camera-equivalent casts retained 4 m sampled clearance. This does not establish manual comfort or foliage visibility.
- **Focused Play-mode normal-input test passed** through unchanged TraversalInput → ThirdPersonMotor → Locomotion03/camera: five outward/seven return waypoints, idle/walk/sprint/stopping, grounding and ~93.65° orbit. 179 runtime samples and five screenshots. Virtual gamepad/mouse input; no direct gait/clip/motor calls during the route. Automated interactive-runtime validation, **not manual playtesting**. Normal state/devices restored.
- **1,141 pre-existing objects/components compared: zero unexpected changes**, permitting intended road/common material slots, detail distance and two proxy active states. Existing building entrances, geometry, colliders, real-tree placements, lighting and gameplay setup unchanged.
- Heights byte-identical; zero approved-grove paint mismatches at control-texture tolerance.
- All native detail placements satisfy conservative building/plot/road/water masks: zero violations. Tree footprints screened against routes/buildings/banks. Static detail vegetation has no collision. Door/approach protection is based on unchanged buildings and exclusion masks; static village doors were not opened and unfinished interiors were not entered.
- No missing scene scripts, serialized references, new mesh UV/normal defects or unsupported new materials. One active player/input/camera/listener. Controller h2/r0.4, speeds 3/6 m/s, camera 4 m/65° preserved.
- **4,365 protected hashes checked:** only the authorized Briarwick scene and TerrainData differ. Production02, original packages, architectural/character sources, prefabs, scripts, settings and earlier Environment05 assets unchanged.
- Final Console **0 current errors / 0 warnings**, no compilation failure. Four transient conversion errors came from an explicit default-platform DXT1 setting; corrected to Automatic/ordinary compression with alpha disabled, resolving to DXT1. Earlier BC7 alpha caused unwanted ground sheen and was corrected. Historical Pipeline errors remain in captured logs. No Console-clear command used. No new buffered messages after cursor57 during final checks.

## Visual assessment and unfinished work

Seven matched overview/ground camera pairs plus three matched static third-person pairs demonstrate improvement. Separate runtime captures show the animated player. Same cameras/lighting, no gizmos or flattering lighting changes. Third-person static pairs temporarily restored baseline paint/material/proxy state, then restored and revalidated the saved candidate.

The player-height result is substantially fuller: meadow heights vary, cones are gone, banks connect into woodland and circulation stays readable. However, **unchanged fog and 95 m detail culling make the high overview much less lush than ground views**. Broad ground regions remain relatively simple at distance.

Outstanding:

1. Suitable loose rock/log/branch/root meshes and dedicated reeds were unavailable in relevant inspected assets. Rock/pebble layers and grass/fern cover are used honestly; no unrelated architectural substitutes. These requested 3D features remain unfinished.
2. Road, creek, bridge, plots and terrain-edge/channel cutoffs retain their blockout geometry. Protected from changes in this task.
3. Source leaf/grass cards and some bark detail remain visible close up. No new wind/LOD system or source-art overhaul. Alpha overdraw requires profiling.
4. This is **not final richly illustrated Kena/Ghibli-quality countryside**. Biome-specific art, field-management composition, approved debris assets and distant presentation need further work/approval. Village gaps are intentionally maintained, not all filled with vegetation.
5. No manual camera-comfort approval, exhaustive outer-slope traversal or actual GPU timing.

All five major regions received terrain/detail treatment. The gaps above are explicit; ready for visual review, not automatic artistic approval.

## Files and recovery

Modified: existing Briarwick scene; `Assets/BlightBloom/Environments/Briarwick/HamletDev01/Terrain/Briarwick_Valley.asset`.

Created: `Assets/BlightBloom/Art/Environment/Briarwick/Environment05/Revision01/` (four textures/layers, road material, heather detail prefab and metadata), this review directory (audit, guarded tooling, snapshots, validation and comparisons). Exact inventory: ChangedFiles.txt. No Blender mesh generation necessary; existing owned vegetation reused.

GroundPass/Details/Trees/GroundEdges are guarded baseline integration tools: **do not reapply over saved work**. Final tuning recorded in FinalTerrain.json. Texture imports: alphaSource=None, ordinary compression, Automatic default format. Capture/GameplayComparison restore review state; probes restore normal runtime state.

A transient filesystem-full error interrupted the first report write after scene/validation saves. Disk then reported ~2.5 GiB available. Only two newly created disposable diagnostic PNGs were removed (DetailCompatibility.png and Revision01_FourLayerTest_Meadow.png, 3,457,985 bytes total) to leave report-writing headroom. All required comparisons retained. No existing caches/sources/history removed. Avoid further bulk imports until disk headroom is reviewed separately.

**No Git commands, commits, pushes, branches, LFS, archiving or unrelated cleanup. Scene saved/open; stop for approval.**
