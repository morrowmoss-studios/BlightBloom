# CM_WindowBay01 — painted texture pass v01

## Result and review

The existing isolated scene `Assets/Scenes/CM_WindowBay01_ArtReview.unity` now shows `CM_WindowBay01_PaintedReview_v01`. The neutral reference remains present but inactive as `CM_WindowBay01_GeometryReview`; enable only one version at a time for an A/B comparison. Lighting, camera transforms, field of view, ambient colors and background are identical to the geometry review. The playable apothecary scene was not touched.

Previews are in `ArtSource/Blender/Architecture/CrookedMortar/WindowBay01/Previews/Painted_v01/`: Front, ThreeQuarter and GameplayDistance.

## Painting sources and published assets

- `Sources/GouacheMaterialSheet_v01.png`: original AI-generated gouache-style source painting, made with the built-in image-generation tool using the user's selected apothecary image as a palette/style reference. It is not a human-painted or layered PSD source. Native resolution is **1254 × 1254**; each material quadrant is approximately 627 × 627. Generation requested a larger image but this is the actual returned size.
- `Sources/prompt.txt`: exact generation prompt. Quadrants: upper-left ivory plaster; upper-right walnut; lower-left sage painted wood; lower-right mossy blue-grey slate. No reference-image pixels are directly projected onto the asset.
- `bake_painted_pass.py`: reproducible Blender transfer/bake script. No noise textures, generated grain functions, AO, directional illumination, or postprocessing are used.
- `ArtSource/Blender/Architecture/CrookedMortar/WindowBay01/CM_WindowBay01_Painted_v01.blend`: sibling editable Blender source with the painting and baked atlas packed. Original neutral `.blend` is preserved. Use Material Preview or Rendered viewport shading to inspect textures; the model has no review lights/cameras in Blender.
- `Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01/Textures/CM_WindowBay01_Painted_BaseColor_v01.png`: **4096 × 4096 sRGB** albedo atlas, shared by the semantic materials. The four surfaces are atlas regions rather than four separate full-size runtime images. Iron and recessed soil use simple flat matte colors in their atlas regions.
- Sibling FBX: `Models/CM_WindowBay01_Painted_v01.fbx`; prefab: `Prefabs/CM_WindowBay01_Painted_v01.prefab`; six semantic URP materials: `Materials/CM_Painted_*_v01.mat`, all under the asset folder above.
- New Unity authoring/capture utilities: `ArtSource/Pipeline/Review/ApplyWindowBayPaintedPass.cs` and `CaptureWindowBayPaintedPass.cs`. These are Editor-evaluated utilities, not compiled gameplay scripts.

## Mapping and color treatment

The approved unique UV0 atlas remains bit-for-bit unchanged. A temporary paint-projection UV layer transfers the source paintings to UV0 using a color-only emission bake; the temporary layer is removed before saving/export. Timber projections follow each part's principal length; the curved frame uses angular coordinates to follow the arch. Slates use consistent building-space scale and restrained source-patch offsets. The plaster receives broad painted cream/ochre/cool planes; shutters use vertical sage strokes. No geometry, normals or object transforms are changed.

The atlas has 16-pixel bake padding. Imported resolution is 4096, with sRGB color, mipmaps, trilinear filtering, clamp wrapping and no texture compression for this review. The existing atlas's median density is about 337 atlas pixels/metre at 4K, with some projection/stretch variation around bevels and reveals. A 4K atlas preserves UV islands and gutters; it does **not** imply the 1254-pixel source painting contains native 4K detail. Source brushwork is deliberately broad and supports a prototype review; bespoke hero close-ups should receive higher-resolution artist paint-over.

URP Lit materials have white albedo tint, zero metallic, zero smoothness, and disabled specular highlights/environment reflections. There are no normal, height, emission or AO maps. The painted surface is carried by actual image albedo, not a shader noise substitute. No bloom, blur, fog or grading changes were made.

## Validation

`texture_validation.json` records exact pre/post Blender vertex, polygon, UV0 and transform fingerprints for all 82 meshes. `unity_texture_validation.txt` confirms the neutral and painted FBX imports have identical vertices, normals, UVs, triangle indices and transforms: 82 meshes, 13,424 triangles. Review camera and lighting snapshots compare equal. No new Unity warnings/errors were observed and compilation failure is false.

## Remaining artistic refinement

This is the first **AI-painted texture prototype**, not final human-authored texture art. The source sheet is retained for repainting, and the editable .blend can be texture-painted directly on the packed atlas. Next review should assess whether the walnut is too warm, plaster patches too assertive, or slate variation too continuous between tiles. A dedicated artist pass should place wear deliberately at corners/joints, refine reveal transitions and end grain, reduce repeated brush rhythms and author per-tile accents. No extra geometry or foliage was added. Geometry approval, painted-surface approval and eventual facade installation remain separate decisions.
