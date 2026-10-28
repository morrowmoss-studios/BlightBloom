# Botanical Cabinet Style02 — painterly material upgrade

Separate, non-destructive style candidate based on **recovered Cabinet B**, the eight-drawer cabinet with the skull and botanical picture. Cabinet A, both recovery sources, the original Tripo GLB, all prior workflows and Unity scenes remain unchanged. No commits or pushes.

## Review and files

- `CM_BotanicalCabinet_Style02.blend` — editable asset-only source. Original 478,613-triangle geometry and UVs retained exactly; no studio objects in exports.
- `CM_Cabinet_Style02_RenderReview.blend` — separate Blender review studio with soft lighting, physical cyclorama, camera and both before/after materials. Not a Unity scene.
- `Exports/CM_BotanicalCabinet_Style02.glb` — self-contained material and textures, Y up / front +Z.
- `Exports/CM_BotanicalCabinet_Style02.fbx` — established metric, -Z-forward/Y-up FBX conversion, embedded textures. FBX is provided for native Unity import; Unity URP material settings still need application on integration.
- `Textures/CM_Cabinet_Style02_GrainUV.png` — intermediate broad grain layer for editable/reproducible baking.
- `Textures/CM_Cabinet_Style02_BaseColor.png` — baked 4096² registered atlas.
- `Textures/CM_Cabinet_Original_Normal.png` — unchanged original 4096² normal map; used at strength **0.32**.
- `Textures/Walnut_Painted_Source.png` — generated 1254² directional painted wood source, preserved separately and packed into editable source.
- `Previews/Style02_{Front,ThreeQuarter,Side,Gameplay,FinishDetail}.png` — actual Blender renders, not AI-generated beauty shots. Matching `Before_*.png` renders use identical lighting/cameras.
- `Comparisons/` — labelled before/after pairs; `Validation.json`, `BuildReport.json`, `ReviewLighting.json` — targeted measurements/settings.

## What changed

The existing form, crown, carving, shelves, drawer arrangement, planter, vines and stock are preserved. No extra clutter, replacement furniture, reshaping or added ornaments.

A **new painted walnut image layer** is mixed with the registered original color atlas through an editable Blender material graph. Original brown/saturation masks limit the treatment largely to walnut/leather-toned areas. Object-space directional sampling gives broad painted grain while retaining original joinery shadows and carving placement. A restrained saturation grade and green-pixel sage tint bring the plants and stock into a closer palette relationship. Existing UVs are reused, not regenerated; the result is baked to an ordinary exportable albedo image. A two-stage transfer bakes only broad grain through the fragmented cabinet UVs, then grades original color in a full-quad UV-domain pass. This avoids reprojecting and shifting the original fine drawer/hardware artwork.

The original normal map is attenuated to 0.32; roughness is 0.82 and metallic 0.08. This deliberately unified matte response reduces plastic/metallic glare while retaining the painted brass appearance. Brass is **not** a newly isolated semantic material: furniture, props and hardware are still fused into the recovered asset. Original baked glints are reduced by the color treatment but not completely removed.

The material `CM_Cabinet_WalnutPaint_Style02_Working` is retained with fake-user protection for editing/rebaking; the visible asset uses the simple export material `CM_Cabinet_Style02_MattePaint`. Original material maps remain packed in the working source. `prepare_style.py` records the exact layer construction.

## Artistic assessment

The candidate has quieter grain contrast, a more muted walnut/sage palette, broader paint variation and a softer surface response, while retaining the rich original cabinet identity. The matched renders separate material changes from the effect of cinematic lighting. There is no bloom, fog, depth-of-field blur, smoothed image filter or invented new dressing.

**This is a finish upgrade, not a rebuilt or newly hand-sculpted mesh.** Rounded/worn shapes come from the existing recovered geometry; softer normal shading does not change silhouettes. It moves toward Wicket's warm, tactile rendered finish but does not reproduce fur-like softness or certify a complete artistic match. Source texture artifacts, baked illumination/highlights, fused props and irregular generated leaf shapes remain visible in close-up. A future exact semantic repaint or structural modularization would require clean region masks/UV reconstruction, not more loose props.

The painted grain layer is image-generated; color layering, UV baking and review lighting are Blender operations. The grain is not photorealistic procedural noise. Color masks are an approximation and also touch some brown leather/book surfaces; this should be judged in the supplied close-ups.

## Preserved dimensions and technical limits

- 478,613 triangles, one mesh and one export material.
- Dressed bounds unchanged: **2.1927 m wide × 0.6082 m deep × 1.9399 m high**.
- Vertex-coordinate and UV hashes identical to recovered B.
- This retains the recovery's temporary review scale; no new fit test in The Crooked Mortar was performed. No claim that it is already installed or clearance-approved in Unity.
- Original high-detail B (870,208 triangles) remains recoverable in the untouched Recovery01 source.
- Existing 8,994 collapsed UV triangles and seam fragmentation are inherited; no speculative UV repair or topology change. The final atlas pass processes the original map across the complete UV domain, retaining registered data even at collapsed UV coordinates. Zero bake dilation avoids bleeding neighbouring patches in the dense atlas. A preliminary direct surface-color bake was rejected after close-up review exposed shifted hardware artifacts; it is not the delivered atlas.
- Still a heavy hero candidate, not a low-budget repeated village prop. No new LOD or retopology was requested/performed.

## Validation

`validate_export.py` confirms baseline source hash unchanged, identical mesh/UV hashes, finite coordinates/UVs, expected triangle counts, and fresh empty-scene GLB and FBX reimports with material and both 4096² maps. FBX returns a Y-up transport mesh (height on Y), GLB reimport restores Blender Z up; these differing bounds-axis orders are expected, not a nonuniform scale change.

Geometry/normals were not altered. The original recovery's topology and degenerate-UV limitations persist. Current validation is asset-only; **no Unity import, runtime performance, collisions, gameplay, room fit or URP screenshot validation** was performed. No gameplay or Unity Console claim is made for this isolated Blender pass.

For eventual URP Lit setup: Base Map = new albedo; Normal Map = original map imported as Normal, strength 0.32; Metallic 0.08; Smoothness approximately 0.18; opaque, no emission. FBX material conversion is not a guarantee Unity will reproduce Blender settings automatically. GLB encodes normal scale/roughness/metallic directly. Studio lights are review-only and not baked into the color texture.

## Reproduction

1. `prepare_style.py`: load unchanged Recovery01 B, build painted working material, bake a new atlas, save isolated source and GLB. New outputs only.
2. `validate_export.py`: explicitly reload/repack the saved atlas, save exports, compare hashes and reimport. The reload guards against Blender retaining a stale inherited packed image.
3. `render_review.py`: render both materials from identical views; save separate studio. `-- --quick` limits to three-quarter; `-- --rest` excludes three-quarter.
4. `make_comparisons.py`: pair actual renders without editing their appearance.

`ImageGenerationPrompt.md` records the built-in image-generation prompt and reference interpretation. All project-consumed artwork is copied into this folder, not left only in the tool's generated-image storage.
