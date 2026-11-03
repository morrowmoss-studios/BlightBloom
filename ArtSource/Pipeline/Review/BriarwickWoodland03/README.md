# Briarwick Woodland03 — gathering grove composition

2026-11-03. Saved in the existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, in Edit mode with Woodland03 selected. **Awaiting visual approval; no wider woodland expansion.**

## Composition

A single small grove develops the Woodland01/Environment02 test into an interior, graduated edge and open gathering passage. The locally refined ground has an irregular, feathered extent of approximately 60 × 52 m around (-29,109), under 3% of the 320 × 320 m valley. The actual planted silhouette is irregular and narrower than this bounding rectangle.

- Retained all seven Woodland01 trees, eight shrubs and 54 Environment02 undergrowth placements at their original positions.
- Added **18 trees**: six Tree 6, six Tree 8, four Tree 1 and two Tree 4 instances, using the existing project-owned prefabs and repaired Tree 6 mesh. Larger clusters create overlapping shade; smaller Tree 8 instances loosen the edge. Height, rotation and spacing vary without a grid.
- Added **118 low plants** in loose groups: 50 Grass_A, 26 Fern_C, 17 GrassDry_B, 16 Fern_A and nine Bush_B instances. The new planting excludes a 2.1 m radius around the route centreline and a small interior clearing; existing low planting is retained.
- The winding passage continues about 35 m beyond the existing road endpoint: (-28,95) → (-25,103) → (-24,112) → (-26,120) → (-25,129). It is a vegetation/ground-blend route, not a new road mesh or gameplay system. Sparse ground and a small turn/clearing invite exploration.
- Only **three additional proxy tree pairs**, indices 20, 22 and 30, were replaced in this section. The prior combined remainder objects are disabled, not deleted. New exact triangle subsets display the other **58 proxy pairs** unchanged; the three selected pairs are retained under a disabled reference group. Complete original proxy meshes and the prior Woodland01 subsets are untouched.

## Ground and softness

The existing Terrain object, TerrainData, four terrain layers and terrain material are retained. Local paint refines grass/moss/soil transitions, slightly increases exposed soil near trunks and the walking passage, and retains a restrained pebble accent. Broad masks and feathered boundaries avoid small procedural noise. **1,514 stored alphamap texels changed** (roughly 2,380 m²); none outside x -60 to 2 / z 81 to 137. No height changes or terrain replacement.

Four project-owned leaf-material copies give the grove slightly gentler color, lower smoothness and disabled specular highlights. Alpha-to-coverage is enabled on those copies where the rendering path/MSAA supports it; no project MSAA or URP changes. The seven existing tree renderers receive scene-local leaf overrides, preserving bark, meshes, source prefabs and positions. New trees share those copies. This is a small material refinement, not a shader rewrite or a cure for the source leaf-card construction.

Eight newly placed trees were seated 0.057–0.332 m lower after examining trunk base-ring clearance on the existing slopes. No terrain or earlier tree positions changed. `RootSeating.json` records exact adjustments. No root skirts, replacement foundations or extra decorative objects were used.

## Validation and preservation

- **14/14 automated Play-mode collision/traversal tests passed after final root seating** using the existing CharacterController.Move: three lanes through the road and full winding route, both directions; original clearing turns; village transition; interior clearing turns; graduated outer edge. Endpoints remain grounded; maximum horizontal error <0.075 m. Controller remains 2 m high / 0.4 m radius. Motor and orbit paused only during the probe, then restored. This is not keyboard/manual playtesting or manual camera-comfort approval.
- Terrain height samples are byte-identical to the before snapshot. Existing roads, creek, bridge, buildings, player and camera components match their before values. No new ground-cover colliders. Added trees reuse simple trunk capsules; there are 25 trunk capsules across the complete grove. None obstruct the tested route.
- All integrated mesh UV/normal counts, finite positions, nonzero normals, submesh/material counts and assigned URP materials pass the targeted checks. No bounds intersections with the inspected active architectural meshes. Foliage remains double-sided alpha-clipped, not blended transparent.
- `ScenePreservation.json` checks all **552 pre-existing objects**: only seven intentional leaf-material overrides and disabling the two prior combined remainder objects are accepted; **zero unexpected component/active-state changes**. Proxy vertex data and the union of selected/remainder triangle indices exactly match the previous meshes.
- SHA-256 verification of **3,721 protected baseline files** finds only the intended Briarwick scene and existing valley TerrainData asset changed. Imported assets, approved buildings, Woodland01/Environment02 source assets, other scenes, source models, Packages, settings and gameplay code remain unchanged.
- Alphamap weights remain nonnegative; maximum sum error is 2/255 from four-channel 8-bit storage. No paint changes outside the limited bounds.
- Final Play-mode Console: **0 errors, 0 warnings, no compilation failure**. Pipeline briefly disconnected on one Play entry; UI stop/re-entry restored it and the final route run completed. No Unity restart, second Editor or package/configuration change.

## Geometry, rendering and memory

| Scope | Triangles | Renderers | Base submesh submissions before batching |
|---|---:|---:|---:|
| Added in Woodland03 | 48,009 | 136 | 154 |
| Complete grove, including Woodland01 and Environment02 | **72,143** | **205** | **232** |

Complete grove: **25 trees, 180 low vegetation instances, 16 unique materials**. The visible 58 proxy pairs are excluded from those vegetation totals. Four new leaf materials replace four earlier leaf materials within this grove; all remaining materials are shared. Instancing remains enabled for repeated foliage. Actual submissions depend on static batching/SRP batching/instancing, visibility and shadow/depth passes; these counts are not measured GPU draw calls or frame time.

**No new texture images** were introduced. All grove texture references plus the three added terrain-layer diffuse/normal pairs total approximately **44.0 MiB compressed GPU mip payload**, with **88.0 MiB Unity-reported texture runtime allocation**, including copies/overhead. These totals exclude base grass, control textures, meshes and frame buffers. Memory is shared across repeated instances rather than multiplied per tree. Exact texture measurements are in `Validation.json`.

Double-sided overlapping leaf cards and repeated understory still present fill-rate/alpha-overdraw risks. Static wrappers have no wind, billboards, LODs or tuned distance culling. No large optimization system, GPU profiling session, platform build or village-wide population was attempted. Before expansion, establish measured frame-time/overdraw budgets and LOD/culling strategy; avoid treating these renderer counts as a scalable final forest setup.

## Artistic assessment and remaining issues

The result is substantially more cohesive spatially than the isolated test: canopy shade connects trees, the edge thins irregularly, undergrowth sits in groups, and a navigable interior replaces the earlier scattering. It is **useful as a composition and spacing reference**, pending approval.

It is **not yet the final visual-quality reference for all Briarwick**. Leaf cards and dark foliage clusters remain evident close up, source bark/ground retain photographic structure, some widely retained distant proxies are visible through the boundary, and existing blockout road edges remain abrupt. The ground-cover close-up is intentionally sparse rather than uniformly carpeted. Small material adjustments cannot turn this pack into bespoke illustrated foliage. Lighting and shadows were preserved, so this pass does not claim Kena/Ghibli-level atmospheric finish. Manual walking/camera review and performance profiling are still needed before broader deployment.

## Screenshots and files

Matched existing lighting and cameras, 1600×1100, no editing gizmos. `Before` and `After` versions exist for:

1. `Woodland03_*_PlayerHeight.png` — approximate third-person camera height, 2.2 m above terrain.
2. `Woodland03_*_Route.png` — gathering-route approach.
3. `Woodland03_*_Interior.png` — interior canopy and clustered planting.
4. `Woodland03_*_Edge.png` — transition to open ground.
5. `Woodland03_*_GroundCloseup.png` — ground cover and foliage.
6. `Woodland03_*_BoundaryContext.png` — honest wide view of grove and untouched proxies.

Project-owned additions: `Assets/BlightBloom/Art/Environment/Briarwick/Woodland03/` contains four leaf materials, four proxy subset meshes and metadata. No source meshes or texture assets were regenerated. All other placements are prefab instances in the existing scene. `Integration.json`, `RootSeating.json`, preservation/validation JSON and Editor automation scripts document the work. `HeightBefore.bin`, `AlphamapsBefore.bin` and the snapshots retain the before-state evidence. Do not rerun integration over the saved scene.

Exact file inventory: `ChangedFiles.txt`. No commits, pushes, LFS, storage cleanup, building changes or new scenes. **Stop here for visual approval.**
