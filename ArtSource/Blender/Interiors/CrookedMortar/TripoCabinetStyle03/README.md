# Cabinet B / Style03 — two material reconstruction tests

Separate Blender prototypes from `TripoCabinetStyle02/CM_BotanicalCabinet_Style02.blend`. No geometry redesign, object movement, optimisation, Unity integration, commits or pushes. Prior versions remain unchanged.

## Review files

- `CabinetB_Style03_PrototypeA.blend`: reconstructed walnut/material response.
- `CabinetB_Style03_PrototypeB.blend`: broader interpreted paint and wood-only curvature pigment glaze.
- `FourWay_Neutral_Review.blend`: shared mesh; switch its material slot between the four `COMPARE_01…04` materials.
- `Comparisons/*_FourWay.png`: original / Style02 / A / B, left to right. Five views: three-quarter, crown/wood, foliage/planter, contents/brass/drawers and gameplay distance.
- `Previews/`: 20 individual full-resolution renders, including separate close-ups.
- `ASSESSMENT.md`: visual judgement and remaining problems.
- Diagnostic/validation JSON files record measurements; `RenderConditions.json` records the locked rig.

All dependencies are packed. `Textures/Walnut_Painted_Source_Reused.png` preserves the unmodified painted grain reused from Style02. No new image-generation service or new raster atlas was used; the new materials are editable Blender graphs. These are not Unity shader exports.

## Diagnosis, before editing

`Diagnostics/Original_BaseColor_Emission.png` displays the original base color **without lighting or specular shading**. Brass-handle glints, bottle streaks, dark shelf recesses and highlighted timber wear remain visible: illumination is already baked into the image. Roughness cannot remove it. `Geometry_Only.png` confirms that crown, carved relief, leaves, rope and stock silhouettes also contain real geometry.

The active Style02 asset has one material and one inherited UV set: **8,994 collapsed triangles**, **19,067 triangles below half a 4K texel**. At 1e-7 UV quantisation, 28 repeated nonzero UV triangles were found; 26 map to surface centres over 1 mm apart. This establishes some overlapping coverage, not a complete overlap count. The source is fused; apparent loose islands do not provide reliable semantic parts.

Wicket is accessible: the supplied GIF is **192 × 208 pixels / 57 frames**. Its first frame is preserved in `Diagnostics/Wicket_ReferenceFrame.png`. It guides tactile dimensional finish, not anatomy; this small reference cannot establish fine wood-material fidelity.

## What changed

**A:** Replaces the wood diffuse image entirely with metre-space painted walnut, structural grain direction, interpreted color groups and restrained physical crevice tone. Old wood luminance/highlights are not blended back in. Drawer/crown rails receive horizontal grain, stiles vertical grain. Separate parameter fields control sage backing, layered foliage, moss, metallic brass, reflective bottle finish, ceramics/books and protected paper/bone artwork.

**B:** Starts with A's region system, testing darker/coarser broad walnut color groups, reduced micro-normal strength, more unified greens and stronger sage backing. A wood-only pigment glaze follows convex modelled relief. It comes from virtual coincident-coordinate grouping and neighbourhood curvature, saved as a point attribute; **no actual welding or vertex movement** occurs. Warm transitions are anchored to carvings/corners, not screen outlines or photographed highlights. B uses this interpretation and real lighting rather than A's additional AO multiplier.

Material roles feed parameters into **one Principled surface**. An initial eight-shader mix hit Cycles' closure limit and was rejected; the final renders use the corrected graph. Original normals retain bounded vein/relief detail. Glass/wood/foliage/brass have different roughness/specular/metallic responses, rather than one global matte setting.

## Limits and verification

- Exact vertex-coordinate/UV hashes, 478,613 triangles and **2.1927 × 0.6082 × 1.9399 m** bounds are preserved. No content is removed or moved.
- No claim of clean new UVs: object-space wood bypasses their defects. Original UVs remain for normals, selectors and protected markings.
- This is replacement of selected illumination-bearing materials, **not exact inverse de-lighting**. Some baked illumination remains on labels, books, ceramics and other protected stock artwork.
- Soft spatial/source-hue masks approximate semantic regions. Small fused details can be misclassified. Individual close-ups are essential.
- Glass is an **opaque tinted reflective approximation**, not hollow/transmissive bottles with reconstructed liquid. Existing generated shells do not support that claim.
- Source text is already partly illegible; it was retained, not blurred or invented. Removing photographed edge contrast can also weaken fine ornament that exists mainly in paint.
- No new unwrapped/baked production atlas, Unity material port, runtime or gameplay validation is claimed.

All four versions use the same **478,613-triangle mesh**; “original” means recovered Tripo material on that mesh. Fixed 55 mm cameras, neutral-white lights/background, exposure 0, gamma 1, AgX Medium High Contrast, 24 samples and seed 41. No bloom, fog, DOF or image blur; denoising treats sampling noise only. No cabinet beauty images are AI-generated.

## Reproduction

Run in order: `inspect_materials.py`, `build_prototypes.py`, `add_expressive_glaze.py` (once after fresh build), `validate_prototypes.py`, `render_fourway.py`, `make_comparisons.py`. Read scripts first. `-- --b-only` refreshes B only when all other states and rig settings are unchanged. Pixel differences support change detection, not artistic approval.

Stop here for artistic selection. No further cabinet edits or integration are authorised by this test.
