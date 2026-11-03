# Briarwick Environment02 — terrain and undergrowth test

2026-11-03. Saved in the existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Awaiting visual approval; no village-wide expansion.

## Implemented area

One feathered, irregular patch around Woodland01, centred near (-29, 101), roughly 42 × 36 m at its soft outer extent. 699 stored alphamap texels have nonzero new-layer contribution (about 1,100 m² at the current 256² control-map resolution). No painting outside the checked x -52 to -6 / z 81 to 121 bounds. Main route is excluded before its endpoint; exposed soil/grass and two localized pebble patches break up the understory without uniform grass carpeting.

The existing 320 × 320 m Unity Terrain already used URP/Terrain Lit and accepts the layers directly. Its TerrainData asset and Terrain object remain in place; no conversion, replacement, second terrain, heightmap import or height modification. Four total layers: a derivative of the original base grass, plus project-owned Grass_Moss, Grass_Soil and Pebbles_A derivatives. The original base layer remains untouched. Its copy disables opacity-as-density blending so local control weights behave predictably; full-weight base grass outside the patch retains its appearance. New layers use softened normals (0.25), muted diffuse remapping, zero metallic/smoothness and no packed mask maps. Grass/soil tile at 4 m; pebbles at 2 m. Height blending and project settings were not changed.

Three loose undergrowth groups combine with the unchanged Woodland01 trees/shrubs:

| Prefab | Instances | Triangles each |
|---|---:|---:|
| Grass_A | 21 | 128 |
| GrassDry_B | 9 | 168 |
| Fern_A | 9 | 360 |
| Fern_C | 9 | 384 |
| Bush_B | 6 | 273 |

Five project-owned static prefab wrappers share four new URP/Lit materials, source meshes and source base-color/normal textures. Foliage is matte, double-sided alpha-clipped at 0.45, with restrained tint/normal strength. No colliders, scripts, wind or new systems were added. Imported package files are unchanged. Woodland01 and all remaining proxies retain their previous states.

## Available package resources and compatibility

Imported pack: `Assets/TerrainSampleAssets/`.

- **16 Terrain Layers:** Grass_A, Grass_B, Grass_Dry, Grass_Moss, Grass_Soil, Heather, Soil_Rocks, Muddy, Rock, Pebbles_A/B/C, Sand, Black_Sand, Snow and Tidal_Pools. Grass_Moss, Grass_Soil and Pebbles_A suit this limited woodland test. Soil_Rocks/Rock are possible later bank/outcrop resources. Muddy needs deliberate wet-location treatment. Sand, snow, black sand and tidal pools are not appropriate for this woodland patch. No dedicated leaf-litter layer was found; none was invented.
- **20 vegetation prefabs:** Fern_A/B/C; Grass_A/B/C/D; GrassDry_A/B/C; Bush_A/B; BushDry_A/B; Heather_A/B; Plant_A/B/C/D. Mesh counts range from 61 to 1,268 triangles. Ferns, sparse Grass_A/dry tufts and small bushes are practical first choices. Larger Grass_B/C/D clusters cost 1,002–1,268 triangles each and should not become a dense default carpet. Heather and other plants are potential restrained accents, not needed for this test. No tree prefabs in this pack; Mini Nature Pack supplies the existing trees.
- **79 texture assets:** 48 terrain maps imported at 2048²; detail maps mostly 1024², with four 512² resources. Terrain base colors use DXT1, normals BC7, masks DXT5. Detail formats include BC7, DXT5 and BC4. Exact paths, importer resolution/type, memory and prefab dependencies are in `PackageInspection.json`.
- The pack's vegetation uses `Shader Graphs/TerrainGrass`. Its shader reports supported, but previous import history includes newer-node warnings in Wind/URPSSS subgraphs and an unknown-property warning in TerrainGrass. That is not proof of production compatibility. This test bypasses those graphs using standard URP/Lit derivatives. Wind, translucency/thickness and terrain-color sampling from the original graph are not reproduced.
- Selected meshes and textures resolve successfully. URP 17.4.0 is already installed. No package installation, dependency upgrade, graph migration, HDRP, pipeline or lighting changes. Full feature compatibility of the original foliage graph remains unverified; no claim that its recorded property warning has been repaired.
- Pack brushes/terrain stamps and settings were not applied. No weather, water, bridge or heightmap systems were imported or integrated.

## Validation

- Existing scene saved and left open in Edit mode, Environment02 group selected.
- **10/10 automated Play-mode routes passed** using the existing CharacterController.Move: three woodland-road lanes, clearing turn and open transition, each forward/reverse. Controller remains 2 m high, radius 0.4 m. All final positions grounded; worst horizontal endpoint error <0.075 m. Motor/orbit were paused only during the collision probe and restored. This is not manual keyboard playtesting or a camera-comfort claim.
- New vegetation has **zero colliders**, so it introduces no blocking road collision. Mesh bounds do not intersect the inspected active building meshes. No changes to entrances or village approaches.
- Terrain height samples are byte-identical to the before snapshot. Alpha weights are nonnegative; maximum sum error is one 8-bit quantization step (1/255), consistent with stored terrain control textures. Painting stays inside the test bounds.
- Integrated meshes have matching UV/normal counts, finite positions, nonzero normals and matching material/submesh counts. Shared materials resolve to supported URP/Lit with assigned textures and correct opaque/cutout settings. Visual review shows no magenta materials or opaque foliage-card rectangles.
- All 497 pre-existing scene objects' serialized components match the before snapshot. No approved buildings, Woodland01, roads, creek, bridge, player or lighting components changed.
- Hash verification of 3,692 baseline files finds only the intended Briarwick scene and existing valley TerrainData asset changed. Imported packs, approved assets, source models, other scenes, scripts, Packages and ProjectSettings are unchanged.
- Final Console: **0 errors, 0 warnings; no compilation failure**. No new warning/error entries since the prior pass's cursor. Earlier recorded package import warnings remain documented above; no Console clearing tool was used.

## Performance and visual limitations

- Added undergrowth: **12,534 triangles, 54 renderers, four shared materials, up to 54 base submesh submissions before batching**. With Woodland01: 24,134 vegetation triangles and 69 renderers. Shadows/depth passes add cost; instancing is enabled, but actual draw calls/frame time were not profiled.
- Four terrain layers fit one four-layer terrain pass; their sampling cost extends beyond the small painted patch. No extra terrain geometry or additional terrain pass was intentionally introduced.
- Selected new source textures: **34.7 MiB estimated compressed GPU mip payload**, versus **69.35 MiB reported Unity texture runtime allocation** (includes copies/overhead, not GPU-only). This excludes old Woodland01 textures, base grass, control maps, frame buffers and meshes. Inspection loaded all pack textures and reported about 467 MiB total texture runtime allocation; that is an Editor inspection footprint, not required scene dependency memory. Selected texture paths and measurements are in `Validation.json`.
- Foliage remains static and card-based with no LOD/distance culling setup. Double-sided alpha clipping still has fill-rate/overdraw cost. Manual camera-comfort testing, target-device GPU profiling and a player build were not performed for this limited material test.
- Ground textures are subdued but retain photographic source structure close up; this is a compatibility/blending test, not final painterly terrain authoring. Soil and pebble accents are intentionally subtle. Existing road meshes still have hard blockout edges; these were preserved rather than repainted or rebuilt. Sparse understory is deliberate. Wider village remains greybox terrain/proxies.

## Recommendation

After visual approval, expand in small ecological patches using the same few shared terrain layers, retaining open path corridors and clear village edges. Prefer inexpensive Grass_A and ferns over repeated large grass clusters. Establish terrain-detail instancing/distance culling, tree LODs and measured overdraw/frame-time budgets before full forest population. Review the original foliage graph's warnings separately if wind/SSS is needed; do not upgrade packages merely to populate this test. Artistic follow-up should target ground-to-road transitions and restrained painterly texture derivatives, not additional clutter or lighting changes.

## Deliverables and recovery

- Project assets: `Assets/BlightBloom/Art/Environment/Briarwick/Environment02/` (five prefabs, four materials, four Terrain Layers and metadata).
- Existing scene and existing `Assets/BlightBloom/Environments/Briarwick/HamletDev01/Terrain/Briarwick_Valley.asset` updated.
- `Environment02_Before_GroundView.png` / `Environment02_After_GroundView.png`: matched woodland-ground comparison.
- Matched `Before`/`After` GroundLevel, Closeup and Context views; additional `Environment02_After_SurfaceDetail.png` for soil/grass/pebble and undergrowth.
- `GroundSourceSheet.png`: diagnostic source swatches, clockwise from top left Grass_Moss, Grass_Soil, Pebbles_A, Soil_Rocks. Not scene lighting.
- `HeightBefore.bin`, `AlphamapsBefore.bin`, original terrain layer reference and snapshots retain the before-state data without creating another Terrain or replacing the valley. `Integrate.cs`, `RefineBlend.cs`, then `NormalizeBaseBlend.cs` document the actual operations; do not rerun over existing integration. Probe and capture scripts are Editor automation outside Assets, not runtime systems.
- Full changed-file inventory: `ChangedFiles.txt`. No commits, pushes, cleanup, LFS work or other building changes.
