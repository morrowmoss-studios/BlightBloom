# Briarwick Woodland01 — limited Mini Nature Pack review

2026-11-03. Awaiting visual approval; no wider forest replacement authorized.

## Result and scope

Saved in existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Seven trees and eight shrubs replace seven of 68 proxy tree pairs beside the woodland gathering route, around x -44 to -6, z 90–115 m. Tree heights are 10.2–13.5 m; shrubs 1.4–1.7 m. Spacing, rotation, species and height vary. The open route and village-to-woodland transition remain clear. This is deliberately sparse first-pass integration, not finished landscaping.

Original forest proxies were two combined meshes, not separate trees. Both complete original objects are retained disabled. Exact triangle subsets render the other 61 proxy pairs unchanged; the selected seven pairs are also retained under a disabled reference group. No original mesh was edited or deleted.

New assets: `Assets/BlightBloom/Art/Environment/Briarwick/Woodland01/` contains seven reusable static prefab wrappers, 12 shared URP materials, four proxy subset meshes, and one repaired Tree 6 derivative mesh. Package meshes and diffuse atlases remain dependencies; keep the imported package installed. No new textures were generated.

## Package findings and selection

`Assets/Mini Nature Pack/Models/` contains 10 Tree prefabs and five Bush prefabs, with embedded meshes/materials. The supplied prefabs use legacy Tree Creator optimized shaders and Tree components, not native URP materials. Shader support flags alone do not establish URP compatibility. No LODGroups or colliders are supplied.

| Source prefab | Source triangles | Assessment |
|---|---:|---|
| Tree 1 | 1,392 | Selected: irregular broadleaf silhouette; strong close-up card clustering |
| Tree 2 | 2,320 | Potential fuller canopy; defer wider selection until visual approval |
| Tree 3 | 3,576 | Potential large canopy; highest geometry count in pack |
| Tree 4 | 2,020 | Selected: rounded, substantial canopy; relatively dark clusters |
| Tree 5 | 1,380 | Conditional: negative base bounds require placement inspection |
| Tree 6 | 1,152 | Selected only through repaired derivative: airy multistem silhouette |
| Tree 7 | 3,160 | Conditional distant conifer; darker/sharper silhouette than selected broadleaves |
| Tree 8 | 688 | Selected: lean, irregular sparse silhouette; approximate central trunk collider |
| Tree 9 | 2,344 | Conditional distant conifer; defer near-village use |
| Tree 10 | 988 | Sparse silhouette; less suitable as primary lush woodland canopy |
| Bush1 | 296 | Selected: fern-like understory |
| Bush2 | 200 | Potential branchy shrub; not needed for this small test |
| Bush3 | 168 | Selected: low spreading foliage |
| Bush4 | 212 | Selected sparingly: upright accent |
| Bush5 | 280 | Dark twig-like mass; less useful as primary soft understory |

Grass, gravel, cliff and rock diffuse/normal maps are supplied, plus a demo terrain asset. These were inspected as available resources, not applied: no terrain repaint or geometry changes. See `PackageInspection.json` and `PackageContactSheet.png` for the full package inspection.

## URP conversion and source defect

Project-owned URP/Lit derivatives reuse 1024×1024 diffuse atlases. Bark is opaque/matte; foliage is double-sided alpha-clipped (cutoff 0.45), not transparent blended. Restrained base tint reduces saturation without repainting the source. Metallic is zero; smoothness 0.06 bark / 0.12 foliage. Instancing enabled. Existing scene lighting and pipeline settings unchanged.

Packed legacy normal/specular/translucency maps are not assigned as incompatible URP maps. Static wrappers omit legacy Tree runtime behaviour, wind and billboards. No unsupported shader replacement was performed inside the imported package.

First Play entry exposed NaN vertices in the original Tree 6 mesh, producing abnormal combined-mesh bounds errors. The project-owned derivative removes 10 non-finite vertices and 16 incident triangles, preserves surviving positions, UVs, colors, tangents and submesh assignment, and normalizes its normals. It has 1,136 triangles. Source Tree 6 remains unchanged. Fresh Play entry after repair produced no new errors or warnings. See `Tree6Repair.json`.

## Validation

- **10/10 automated Play-mode CharacterController.Move routes passed**, forward and reverse: three lanes across the woodland road, clearing turn and village transition. Controller remains 2 m high / 0.4 m radius. All endpoints grounded; maximum horizontal endpoint error below 0.075 m. Motor and orbit temporarily paused during the collision probe and restored; normal Edit state restored after Play.
- This is automated collision/traversal validation, **not keyboard playtesting or manual camera-comfort approval**. No input, controller, camera or gameplay scripts changed.
- UV and normal arrays match vertices; no non-finite vertices or zero normals in integrated meshes; material slots match submeshes. All selected materials have supported URP shaders and assigned base textures. No bounds intersection with the inspected active architectural meshes.
- 476 pre-existing scene objects' serialized components match the before snapshot. Only the two original combined proxy objects' active states were intentionally changed; the snapshot compares components, with disabled states checked separately. Remaining proxy vertices and triangle membership match the original precisely.
- SHA-256 verification of 3,229 baseline files found only the intended Briarwick scene changed. Buildings, terrain assets, imported package files, production scenes, source models, settings and scripts in the protected baseline remain unchanged.
- Final fresh Play-mode Console: **0 errors, 0 warnings, no compilation failure**. Earlier captured history includes one Pipeline timeout and three unrelated TerrainSampleAssets import warnings; that pack was not integrated or modified. The Tree 6 bounds errors were reproduced and corrected as above. No Console-clearing tool was used.
- The initial route probe's 700-step budget was too short for the longest segment; increasing the test budget to 2,000 allowed the same route to complete. This was a test limit, not a world geometry adjustment.

## Cost and remaining concerns

Integrated vegetation: **11,600 triangles, 15 renderers, 24 base submesh submissions before batching, 12 shared materials, seven simple trunk capsule colliders**. Shadow/depth passes can add submissions. This is a geometry/material estimate, not a measured GPU frame-time or overdraw benchmark. Bushes are noncolliding; trunk capsules are conservative approximations rather than detailed branch colliders.

Alpha clipping avoids blended sorting but leaf cards remain evident up close, and overlapping double-sided foliage can still cost fill rate. No LODs, billboards, wind or platform profiling yet. Do not scale this setup village-wide without an LOD/culling and GPU-overdraw plan. Proxy subset meshes retain unused original vertices; their bounds remain broad, acceptable for the temporary forest only.

Against the cottage and Crooked Mortar, the varied green silhouettes are a useful woodland direction at landscape distance, but the foliage is less illustrated and has harder/darker card clusters close up than the buildings' soft weathered finish. Existing flat terrain remains a blockout. Do not call this final environment art. Review whether Tree 1/4 card density and shrub scale are acceptable before expansion. No additional foliage, terrain, lighting or material overhaul was attempted.

## Review images

Matched existing-lighting cameras, no editing gizmos, 1600×1100:

- `Woodland01_Before_Overview.png` / `Woodland01_After_Overview.png`
- `Woodland01_Before_GroundLevel.png` / `Woodland01_After_GroundLevel.png`
- `Woodland01_Before_VillageTowardForest.png` / `Woodland01_After_VillageTowardForest.png`
- `Woodland01_Before_FoliageDetail.png` / `Woodland01_After_FoliageDetail.png`
- `Woodland01_After_VillageContext.png`: cottage, Crooked Mortar and woodland in one landscape frame.

Before captures precede integration. After captures include the repaired derivative. `PackageContactSheet.png` is a diagnostic asset-selection sheet, not representative scene lighting. Full exact file inventory is in `ChangedFiles.txt`; machine-readable placement, preservation and validation evidence is alongside this report. The Editor is left in the existing scene with Woodland01 selected. No commits, pushes, cleanup or LFS changes.
