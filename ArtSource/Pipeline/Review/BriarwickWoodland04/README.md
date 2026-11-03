# Briarwick Woodland04 — village-to-forest integration

2026-11-03. Existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity` saved in Edit mode with **Woodland04 - village to forest transition** selected. Stop for visual approval; no wider expansion.

## Selected area and composition

The previous grove and Locomotion03 exploration rig were inspected in the saved scene. Woodland03 is treated as the user-approved working foundation, not something to replace. The new transition occupies the open northern village approach, approximately x -50 to 2 / z 46 to 90 including canopy edges, south of the existing grove. It stays north of the nearby chapel, elder's cottage and Crooked Mortar, far from the creek and bridge. No changes to those sites, village geography or the transport layout.

Added one organized scene-local group with two children: **Canopy - open village edge to grove** and **Undergrowth - sheltered clusters, clear road**.

- **10 trees**: four Tree 8, three Tree 1 and three Tree 6 instances. Village-side trees are smaller and farther apart; upper clusters connect to the shaded Woodland03 boundary. Deliberately chosen anchor positions, varied scale/yaw and unplanted gaps avoid a regular row or uniform scatter. New roots are seated to the existing slopes.
- **58 low vegetation instances** in eight sheltered groups tied to nearby trees: existing grasses, dry tufts, ferns and small shrubs. More open village-side ground, stronger clustering nearer the grove. New undergrowth avoids a 3.2 m radius around the existing route centreline.
- The established path from (-7,40) through (-17,61) to (-28,95) and the winding Woodland03 continuation remain unchanged. No finished roads, new road meshes or gameplay routes were authored.
- **No existing tree, shrub, undergrowth or placeholder was moved, disabled or deleted.** Woodland01, Environment02, Woodland03 and the exploration rig retain their exact saved component/active states.

## Assets and ground integration

All scene instances reuse approved project-owned Woodland01 tree prefabs, including the already repaired Tree 6 mesh; Woodland03 leaf materials; and Environment02 undergrowth prefabs/materials. Only new tree renderers receive the existing leaf-material overrides. No imported packages, source prefabs, materials, textures or shaders were modified or regenerated.

The existing valley Terrain object, TerrainData, four layers and material remain in place. **677 stored alphamap texels** changed, roughly 1,060 m² of soft, localized transition ground. Painting is restricted to previously unpainted base-grass texels south of the grove, with broad grass/moss/soil blends, a restrained pebble accent and feathered edges. It fades out before z 81; all previously painted texels are byte-for-byte preserved. Tree canopy positions guide soil variation; there is no uniform grass carpet. No height changes, heightmaps, second terrain or terrain replacement.

The existing road mesh remains a blockout with hard edges. Adjacent ground is softer, but this pass does not disguise the road's temporary construction or introduce finished-road art.

## Validation

- **10/10 automated Play-mode route tests passed** with the existing Locomotion03 CharacterController: three main-route lanes at -1.5/0/+1.5 m offsets, each forward/reverse through the full existing woodland route, plus western/eastern transition gaps in both directions. All endpoints grounded; maximum horizontal error <0.075 m. The controller remains 2 m high / 0.4 m radius with unchanged settings.
- **20/20 trunk-blocking tests passed**: approach each new tree capsule from two sides using the existing CharacterController.Move. The player stops outside the trunk axis. Ten inherited trunk capsules are the only added colliders; undergrowth remains noncolliding. These are existing approximate trunk collision shapes, not detailed branch/leaning-trunk reconstruction.
- **40 camera-equivalent sphere casts** at five route positions and eight headings, pitch 20°, radius 0.18 m, retain the full 4 m clearance against colliders. They use the same obstruction radius/distance and hierarchy exclusion as the existing orbit camera. Noncolliding leaves can still occlude the view; this is **not proof of manual camera comfort or collision with every visible foliage surface**.
- Tests temporarily paused motor/orbit only for controlled collision probes, then restored normal state and player pose. No input/controller/camera/animation scripts or parameters changed. No new interactive input-path test or manual walkthrough is claimed for Woodland04; the earlier working integration remains protected.
- No missing scene scripts, missing prefab instances, missing new material/texture references, unsupported new shaders, UV/normal array mismatches or non-finite new vertex positions were found. New vegetation renderer bounds do not intersect the inspected active architectural meshes.
- **735 pre-existing scene objects checked; zero unexpected component or active-state changes.** This includes buildings, roads, creek/bridge, earlier woodland groups, player/camera and lighting. Exactly one active player/input/camera/AudioListener remains, with all rig references resolved.
- Terrain heights are byte-identical to the before snapshot. Previous painted texels changed: **0**. Ground changes outside the selected lower painting area: **0**. `terrainPaintIdentical=false` in Validation.json is expected for the authorized new painting, not a preservation failure.
- SHA-256 checks of **3,741 protected baseline files** found only the intended Briarwick scene and existing valley TerrainData asset changed. Production02, all original/reusable assets, character prefab/controller/model, shared code, settings and package files remain unchanged.
- Final Play-mode Console: **0 errors, 0 warnings; no compilation failure**. No Console clearing or package upgrade performed.

## Cost and performance observations

| Scope | Triangles | Renderers | Base submesh submissions before batching |
|---|---:|---:|---:|
| Added Woodland04 | **22,749** | **68** | **78** |
| Woodland01 + Environment02 + Woodland03 + Woodland04 | **94,892** | **273** | **310** |

Woodland04 uses **10 already-existing materials**, with **zero new unique materials** across the complete composition (still 16 total), **zero new texture dependencies** and **zero additional unique texture-image memory requirement**. Instance/component and runtime batching buffers still add overhead. Counts exclude village buildings, the character and remaining proxy meshes.

All repeated assets retain existing instancing-enabled materials and static flags. Static/SRP batching and GPU instancing eligibility are not a measured draw-call reduction; actual calls depend on visibility, batching and shadow/depth passes. No GPU frame-time, target-device performance or alpha-overdraw profiling was performed. Overlapping double-sided leaf cards remain the main fill-rate concern. Tree spacing and low-plant clumps keep the new section restrained, but the assets still lack a production LOD/distance-culling setup. No optimization overhaul or new foliage system was introduced.

## Visual review and remaining concerns

The new planting bridges the open northern village path and the earlier grove, rather than adding another isolated island. Canopy density increases toward Woodland03 while village-facing gaps preserve road visibility and future village activity space. Materials remain those approved during the working walkthrough; no lighting, fog, skybox or post-processing changes.

Close-up leaf cards, dark leaf clusters, photographic texture structure, hard placeholder-road edges and visible distant cone proxies remain known limitations. They were not redesigned in this composition pass. Manual assessment of the new edge, camera sightlines and perceived density is still required before expansion. No claims of final landscape polish or village-wide performance readiness.

## Screenshots and changed files

Clean 1600×1100 scene-camera renders under identical existing lighting, with matching **Before/After** views:

1. `Woodland04_*_VillageApproach.png` — approaching from the northern village path.
2. `Woodland04_*_OpenToDense.png` — open ground into denser canopy.
3. `Woodland04_*_PlayerHeightEdge.png` — edge at approximately 2.2 m above terrain.
4. `Woodland04_*_Passage.png` — clear corridor into Woodland03, with the saved player visible.
5. `Woodland04_*_VillageContext.png` — village buildings, the transition and untouched outer proxies together.

These are clean review-camera captures, not screenshots proving a new manual walkthrough.

Modified project files:

- `Assets/Scenes/Briarwick_Hamlet_Dev01.unity` — new Woodland04 group and prefab instances only.
- `Assets/BlightBloom/Environments/Briarwick/HamletDev01/Terrain/Briarwick_Valley.asset` — limited new splat weights; heights/layers/previous painting preserved.

Created documentation/evidence only under `ArtSource/Pipeline/Review/BriarwickWoodland04/`: reviewed/adapted Editor automation scripts, baseline snapshots, before-state height/paint arrays, integration/validation/performance reports and screenshots. No new runtime scripts or asset-library derivatives were needed. Exact inventory: `ChangedFiles.txt`. `Integration.json` contains placements; `Validation.json`, `PlayValidation.json`, `TrunkCameraValidation.json`, `Performance.json` and `ProtectedValidation.json` contain evidence. Integration is guarded; do not rerun over the saved group.

**Nothing committed or pushed. Stop here for visual approval.**
