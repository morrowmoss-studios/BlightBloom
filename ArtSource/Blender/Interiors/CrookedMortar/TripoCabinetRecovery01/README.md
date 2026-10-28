# Tripo Botanical Cabinet Recovery 01

Recovered assets for artistic approval; **no Unity integration**. Original GLB, Production02, previous workflows, prefabs and gameplay remain untouched. No commit or push.

## Deliverables

- `CabinetA/CabinetA.blend`, `CabinetB/CabinetB.blend`: independent editable sources. Each contains `01_HIGH_DETAIL_preserved` (hidden) and `02_OPTIMIZED_candidate` (visible). Toggle collection visibility to compare; do not enable both simultaneously.
- Each cabinet's `Exports/*_Optimized.glb`: one mesh, one shared original material, all three original 4096×4096 maps embedded. No external texture dependency.
- `Textures/`: original embedded base color JPG, packed roughness/metallic JPG, normal PNG, extracted **byte-for-byte**, not repainted or recompressed. `TextureManifest.json` records checksums. The Blender sources also pack these maps.
- `ImportedIslands.blend`: complete imported assembly before cabinet extraction, with all 2,775 topological islands retained, including excluded material.
- `InspectionOverview.png`: full assembly overview. `Inspection.json` records source SHA256 and every island's bounds/counts. `RecoveryReport.json` records retained counts, transforms and excluded island IDs.
- `Cabinet*/Previews/`: matched high-detail/optimized front, three-quarter, side, crown, drawer and gameplay-distance views. `Comparisons/`: side-by-side sheets, high-detail left / optimized right.
- `Validation.json`, `SurfaceDetails.json`, `ExportMaterialAudit.json`: measured results and limitations.

## What the source actually contains

The supplied GLB has **one node, one mesh, one material, 1,914,846 triangles**, and three embedded 4K images. Loose-part separation yields 2,775 islands; most are UV-seam fragments rather than semantic objects.

Cabinet B is the large front-facing cabinet on the left of the imported assembly (skull and botanical picture on the upper shelf). Cabinet A is the second full-size cabinet in the middle, initially facing sideways (bottles and flower pots above a row of books). Both contain eight drawer fronts in the generated geometry. A is **not markedly narrower/taller** in the actual export; its dressed normalized width is slightly greater. No narrow/tall design was invented or substituted. The minis below are excluded.

Safe extraction uses genuine empty spatial gaps. In imported Blender coordinates:

- A: all island bounds above Z=0.24 and inside X=(0.025, 0.162).
- B: all island bounds above Z=0.24 and inside X=(-0.51, 0.025).
- There are no islands crossing those cabinet boundaries. Miniatures occupy a separate lower band; right-hand incomplete frame/fragments lie beyond X=0.1685. All exclusions survive in `ImportedIslands.blend` and the original GLB.

A retains 773 islands; B retains 1,029. 336,774 triangles / 973 islands from miniature variants and the disconnected incomplete frame are excluded from the two assets. **No detail inside either recovered cabinet was pruned.**

## Scale, orientation, pivots

Source import dimensions are not trustworthy real-world measurements. Both cabinets are uniformly normalized to a **temporary 1.94 m dressed height for review**; no nonuniform reshaping. A is rotated -90° around Blender Z to share B's front direction. Original arrangement and scale survive in the baseline. The exact transforms are recorded.

| Cabinet | High triangles | Optimized triangles | Reduction | Dressed W × D × H, metres |
|---|---:|---:|---:|---|
| A | 707,864 | 389,324 | 45.0% | 2.2273 × 0.5432 × 1.9400 |
| B | 870,208 | 478,613 | 45.0% | 2.1927 × 0.6082 × 1.9400 |

Blender Z-up / front -Y; glTF export Y-up / front +Z. Origin is centred in X/depth at the high-detail lowest foot plane. Optimized feet differ by less than 0.1 mm. Final gameplay placement/scale needs approval; no claim of a measured Unity fit.

## Optimization and visual judgement

Conservative collapse decimation at 0.55 retains original UVs/materials and the original normal map. No remesh, voxel conversion, indiscriminate weld, hidden-face deletion, or replacement geometry. No new normal bake was necessary for this conservative candidate. No lower-resolution source textures were substituted. Stronger reduction was not chased merely to reach a number.

The broad silhouettes, crowns, brass handles, botanical carvings, plants, hanging planter, and existing shelf stock remain recognizable. Compare exact matched views, including details; close inspection still shows the original generated softness, uneven leaves and painted/baked highlights. This is faithful recovery, not an artistic redesign or proof of clean handcrafted topology.

These are **heavy hero-asset LOD0 candidates**, not village-wide repeated-instance budgets. A subsequent approved production pass could develop a clean retopology and baked LODs. They are export-ready for evaluation, not certified final Unity production assets.

## Modularity limitations

After merging coincident coordinates at 1 micrometre **in analysis only**, each cabinet is one connected geometric component. The many import islands do not isolate furniture, plants, bottles or drawers. Joining transport fragments does not destroy a useful semantic hierarchy: none existed. Loose-part editability can be recovered from the baseline or Blender Separate by Loose Parts.

No drawer movement, interchangeable stock, independent foliage or detachable planter is claimed. Those need deliberate cutting, reconstruction of hidden contact surfaces, new UVs and texture transfer/baking. Automatically deleting uncertain islands would remove legitimate details. That operation was not attempted. Existing moss/stock/planters remain in place.

## Validation and inherited defects

- Original GLB SHA256 unchanged.
- Raw extracted texture checksums and both export texture checksums match exactly.
- Fresh empty-scene GLB reimports: one mesh, expected triangle counts, all three 4K images and normal/base-color/metallic-roughness assignments preserved.
- Finite geometry, UVs and vertex normals; no zero vertex normals or zero-area geometric triangles at 1e-16 m² threshold.
- Deterministic bidirectional nearest-surface sampling (~12,000 face centroids per cabinet): max A 0.214 mm, B 0.191 mm; 95th percentile A 0.076 mm, B 0.081 mm. This is a sample, not a guaranteed global Hausdorff bound.
- Source topological boundaries: A 60,216; B 76,638, largely coincident UV seam fragments. Optimized A 59,564; B 75,593. Not watertight manufacturing/collision meshes.
- **Inherited collapsed UV triangles:** A 82,042 high / 21,727 optimized; B 31,351 high / 8,994 optimized (UV area <1e-20). Finite UVs alone do not establish a clean unwrap. Preserved appearance was prioritized; these regions require UV reconstruction/texture transfer before independent repainting. Some additional tiny optimized triangles cover less than half a texel; see `SurfaceDetails.json`.
- No semantic cuts or speculative hole fills. Original generation defects and baked illumination remain.
- Blender exporter warns that multiple texture nodes share a sampler for packed roughness/metallic; material audit and roundtrip verify correct maps. Blender 5.2 reports a `World.use_nodes` deprecation in the render-only studio, not an asset fault.
- No Unity import, gameplay, collision, runtime performance, or lighting validation performed, per requested approval boundary. No Unity scenes/assets/settings/scripts changed.

## Reproducible scripts

Read before running. Outputs are limited to this folder. Run Blender scripts with the existing Blender executable; do not open another Unity Editor.

1. `inspect_source.py`: imports original without writing it, separates loose parts, records baseline and overview.
2. `extract_original_textures.py`: stdlib Python, extracts unchanged embedded bytes (run after inspection's preliminary image saves).
3. `recover.py`: extracts full cabinet regions, preserves high collection, builds separate conservative candidates and exports.
4. `validate_recovery.py`: restores and packs raw original images, reexports, measures connectivity/surface deviation, reimports GLBs in empty scenes, verifies original hash.
5. `validate_surface_details.py`: read-only source checks for normals, degenerate geometry and UVs.
6. `render_comparisons.py`: unsaved neutral Cycles studio, identical cameras/lighting per state; no reference projection, bloom, fog or invented beauty renders.
7. `make_comparisons.py`: labels and pairs actual renders; reports image differences as supporting evidence only.

**Approval boundary:** inspect the recovered designs and matched comparisons before any Unity integration or further destructive modularization.
