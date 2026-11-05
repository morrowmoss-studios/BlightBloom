# Briarwick Environment05 — full landscape coverage

2026-11-03. Existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity` saved in Edit mode with **Environment05 - countryside coverage** selected. This is a landscape-wide first coverage pass, not an isolated patch. Stop for visual approval.

## Coverage and regional work

Surveyed the existing 320 × 320 m valley, its road records, land-use reserves, architecture, creek/bridge, approved woodland and exploration rig. `PLAN.md` records the pre-implementation plan. No new scene, terrain or gameplay system.

**60,133 control-map texels changed: 91.76% of the complete terrain control map**, approximately 94,000 m². Earlier painted woodland ground is retained exactly. The remaining unchanged surface includes previous work, building footprints, land-use reserves and road surfaces. Existing four terrain layers provide broad grass/moss/soil/pebble blends guided by slope, creek proximity, road wear and large-scale variation. No extra terrain layer/pass was introduced. Heights and all existing layers/materials remain unchanged.

The Environment05 hierarchy has six regional subdivisions. Open countryside is intentionally not converted into forest.

| Region | Low plant instances | New renderers including trees | New triangles | Treatment |
|---|---:|---:|---:|---|
| Meadows | 390 | 51 | 67,899 | Open grass/dry-tuft clusters, occasional small shrubs/heather, varied ground |
| Hillsides | 551 | 104 | 110,368 | Sparser dry vegetation, soil/pebble exposure, occasional outer trees |
| VillageMargins | 486 | 55 | 83,148 | Low growth in unused margins, worn ground near routes; footprints, approaches, common and plots kept clear |
| CreekBanks | 425 | 24 | 113,307 | Fern-rich clusters and damp soil/pebble blends on both banks, outside water and crossing corridors |
| WoodlandSkirts | 148 | 19 | 38,498 | Sheltered fern/grass groups outside the approved grove, blending into open countryside |
| DistantCountryside | 372 | 75 | 68,724 | Restrained low growth and scattered trees; broad ground treatment rather than dense forest |

Total **2,372 low plants** plus **18 sparse outer trees**. Low plants: 945 Grass_A, 705 GrassDry_B, 360 Bush_B, 140 Fern_A, 136 Fern_C and 86 Heather_A. There are 195 general cluster anchors plus additional creek-bank clusters. Anchor placement uses irregular separation and ecological exclusions; individual plants vary in size/rotation within clumps, leaving gaps. The entire prior northwestern grove/transition footprint is excluded from new planting. Existing proxies are retained unchanged.

## Assets, implementation and editability

Reused approved Woodland01 tree prefabs (including the repaired Tree 6 mesh), Woodland03 leaf materials, Environment02 grasses/ferns/shrub meshes and materials, and the existing four terrain layers. Original packages, shared assets and existing prefabs are not modified.

The already imported Terrain Asset Pack's Heather_A mesh/base-color/normal maps support restrained flowers. One project-owned standard URP/Lit heather material is derived from the existing fern material, using the imported heather maps. It retains matte, muted, double-sided alpha-clipped treatment. No Shader Graph migration or package installation.

Low vegetation is **combined by region, 40 m spatial cell and material into 310 mesh chunks**, rather than creating 2,372 individual renderer components. Source vertex data, UVs, normals and source silhouettes are retained by mesh combination. Chunks have local origins/bounds and no colliders. Existing prefab instances supply the 18 trees and inherited trunk capsules. Roots are seated on the existing terrain; terrain is not reshaped.

`Integrate.cs` and `Integration.json` retain exact source types, placements, scales, rotations, region grouping and chunk generation. Original editable/source assets remain intact. Unity mesh assets are the baked output; this pass did not author new Blender geometry or regenerate approved models. The guarded integration script must not be rerun over the saved group.

No suitable loose rock, log, fallen-branch or exposed-root models were found in the available model/prefab inventory. Architectural rock-floor pieces are not appropriate substitutes. Rock/pebble ground detail is provided by the existing terrain layer; **no invented 3D debris or stretched unrelated meshes** were added. Bespoke natural-debris assets remain a gap.

## Geometry, rendering and memory

| Scope | Triangles | Renderers | Base submesh submissions before batching |
|---|---:|---:|---:|
| Added Environment05 | **481,944** | **328** | **346** |
| All current environment vegetation, including earlier passes | **576,836** | **601** | **656** |

Environment05 uses 11 materials, 10 reused plus one new heather derivative. All environment vegetation now uses 17 unique materials. Counts exclude buildings, character, terrain, roads and proxy cones.

Combining reduces low-plant renderer components by approximately 87% compared with one renderer per plant. It does not reduce triangle count or prove a frame-time gain. Spatial chunks trade some culling precision for lower component/submission overhead; chunks crossing empty village space are not filled with geometry there. Combined unique meshes are not GPU-instanced copies; repeated trees remain instancing-eligible, and shared materials support SRP/static batching. Shadow/depth passes add cost. No global settings or rendering systems changed.

- New unique texture dependencies: **two existing imported 1024² heather maps**. Estimated compressed GPU mip payload **2.67 MiB**; Unity-reported texture runtime allocation **5.34 MiB** including copies/overhead. No image files duplicated.
- Environment05's referenced meshes report approximately **76.7 MiB runtime allocation**, including the reused tree meshes. New baked mesh/material folder occupies approximately **68 MiB on disk**. Additional static-batch/runtime buffers can increase memory further.
- Low plant geometry remains double-sided cutout foliage: alpha overdraw, shadow cost and card visibility remain concerns. Existing assets have no production LOD/billboard/distance-culling setup. Hundreds of landscape chunks require actual target-device profiling before further density increases. **No final GPU performance claim**, player build or optimization overhaul was performed.

## Validation

- **20/20 automated Play-mode CharacterController.Move route tests passed**, all endpoints grounded, horizontal endpoint error <0.075 m. Includes three lanes through the southern approach, bridge, main village road and woodland, forward/reverse; southern meadow; east/west hillsides; both creek banks; farm access; and the winding woodland continuation.
- **36/36 new-tree collision tests passed** approaching the 18 inherited capsule colliders from two sides. Low plants have no colliders. Existing character dimensions, motor, camera, input, animations and interactions were not changed.
- **40 camera-equivalent sphere casts** retained a 4 m obstruction clearance at the sampled woodland/approach positions. They do not establish manual camera comfort or account for visual occlusion by noncolliding leaves. The landscape-wide collision routes, rather than these casts, cover the wider regions.
- Placement checks for all 2,372 low plants found **zero building/plot, water, road, old-grove or slope-exclusion violations**. Conservative plant-footprint radii leave at least **1.54 m from the water edge** and **1.22 m from road edges** in the checked samples. New trees were separately screened with a larger footprint and creek setback. Water/bridge geometry, channel positions and existing travel corridors remain intact.
- Large combined chunk AABBs can overlap empty space near buildings, so those AABBs are not used as false-positive clipping tests. `PlacementPerformance.json` checks the individual source placements/radii against architecture and route exclusions. No claim of exhaustive triangle-to-triangle intersection testing.
- New mesh/material checks pass: UV/normal arrays match vertices, positions finite, base textures present, supported URP shaders. No missing scene scripts or new missing prefab references were found.
- **806 pre-existing objects checked: zero unexpected serialized-component or active-state changes.** All previous vegetation placements, player/camera, lighting, buildings, roads, creek, bridge and land-use markers remain unchanged. There is still exactly one active player/input/camera/AudioListener; rig references resolve.
- Terrain height samples are byte-identical. Previously painted texels changed: **0**. Only new splat weights were written; `terrainPaintIdentical=false` is expected for this authorized landscape painting.
- Hash checks of **3,741 protected files** identify only the intended Briarwick scene and valley TerrainData as changed. Original packages, Production02, all approved source assets, prefabs, scripts, settings and input/animation assets are unchanged.
- Final Play-mode Console: **0 errors, 0 warnings; no compilation failure**. No Console clearing performed.

Collision probes temporarily paused motor/orbit and restored the player and normal state afterward. These are **automated collision/traversal checks**, not a new normal-input animation regression or manual playtest. No manual visual/camera-comfort approval is claimed.

## Visual review, unfinished areas and next decisions

This pass replaces the largely flat-color landscape surface with connected ground treatment and low growth in every region. Bank vegetation is denser, village circulation remains readable, and meadows/hills remain open. Existing lighting/fog/skybox/post-processing are preserved; the far elevated image consequently retains the scene's atmospheric fade.

It remains a **first broad coverage candidate**, not a finished richly illustrated countryside. Low plants are deliberately sparse at landscape scale. Distant cone proxies, temporary roads, water strip, bridge and land-use surfaces are still visibly blockout assets. Natural 3D rocks/logs/branches are missing. Source ground/bark retain some photographic detail and foliage cards remain visible close up. Outer slopes/terrain edges keep their original shape and are not all validated as playable routes. Further bespoke art, regional composition review and profiling are needed; do not equate broad paint coverage with final artistic quality.

No additional expansion beyond the existing terrain. No weather, water, lighting, gameplay or foliage runtime systems. No package changes. **No Git commands, commits, pushes, branches, cleanup or LFS work.**

## Screenshots and files

Matched existing-lighting, gizmo-free 1600×1100 **Before/After** views:

- `Environment05_*_Overall.png` — complete existing terrain from elevated angle.
- `Environment05_*_Village.png` — village surroundings.
- `Environment05_*_Meadow.png` and `Environment05_*_Hillside.png` — open land and height variation.
- `Environment05_*_Roadside.png` — southern player-height approach.
- `Environment05_*_CreekBridge.png` — bank growth and preserved crossing.
- `Environment05_*_WoodlandEdge.png` — landscape into approved woodland.
- `Environment05_After_CoverageSurvey.png` — additional near-vertical survey to inspect coverage; not a matched before/after pair.

Review cameras are approximately player height for the ground-level views. They are not evidence of manual gameplay. The player remains at its approved saved woodland spawn.

Modified: existing Briarwick scene and `Assets/BlightBloom/Environments/Briarwick/HamletDev01/Terrain/Briarwick_Valley.asset` (paint only).

Created: `Assets/BlightBloom/Art/Environment/Briarwick/Environment05/` (310 combined mesh assets, one heather material and metadata) and this review directory (plan, scripts, placement JSON, preservation evidence and captures). Exact inventory: `ChangedFiles.txt`. Baseline height/alpha arrays and scene snapshot preserve before-state evidence. All reusable source assets remain available for future editing.

**Scene saved; Environment05 selected. Stop for visual approval.**
