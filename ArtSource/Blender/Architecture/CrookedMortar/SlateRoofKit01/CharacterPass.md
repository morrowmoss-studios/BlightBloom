# SlateRoofKit01 — handcrafted painted refinement

Open the existing Assets/Scenes/CM_SlateRoofKit01_IntegrationPreview.unity. Its roof-kit dependencies carry this update; no scene file was rewritten. The approved StyledDetails07 scene remains unchanged.

## Changes

- Kept corrected roof clipping, local-plane ridges/valleys, measured roof profiles, heights, sockets and fixed junction boundaries. Pitch-cover strips remain disabled.
- Increased controlled tile-width differences with shared boundaries, slightly varied row offsets and overlap lengths, 5–13mm hand-cut toe offsets, asymmetric clipped corners. Shared slope coordinates still continue through carrier triangle boundaries. Variation is deterministic and constrained, not random scatter.
- Existing fascia now has small modeled lower-edge chamfers; seated upper edges remain fixed. Ridge crowns have only 2mm controlled variation. No building-scale curvature or silhouette change.
- New painted slate albedo v04: broad opaque gouache strokes, blue-grey, sage and weathered slate groups. Continuous roof-space UV sampling avoids unrelated rectangular atlas patches; slight per-tile UV shifts reduce cloning. Selected valley channels sample restrained moss/sage regions. This is painted moss coloration, not volumetric moss or extra foliage geometry.
- Reused matte URP Lit and walnut paint. No lighting, bloom, fog or grading changes. v03 is an intermediate paint exploration; v04 is the final material/source reference. Both image-generation sources are retained.

## Verification

29 active modules, 47 mesh parts, 49,768 library triangles (includes all standard examples and fitted adapters, not the installed building alone). Zero non-manifold edges, degenerate geometry or UV triangles. Valid 0–1 UVs with intentional shared painted image reuse. Existing normals recalculated; Unity UV/normal arrays, unit scale, bounds and materials pass. Maximum import bounds discrepancy under 0.000002m. All 1,431 sampled fitted carrier positions still match, no missed samples. Designed overlapping slate courses retain the same positive plane separation. All 53 original collider/behaviour/light components and transforms unchanged, including 37 colliders; no new components. No compilation failure or new Console errors.

All six roofs and previously corrected junctions reviewed in clean Camera.Render previews: hero shoulder, dormer valleys, hero/rear junction, rear/wing step, entry canopy step, display catslide, below eaves, elevated and gameplay distance. No new large gaps, exposed adapter fins or floating slates observed. This visual and sampled check is not an exhaustive all-pairs intersection proof or full traversal playthrough. Intentional tile seams/overlaps remain visible.

## Files and review

Updated build_slate_roof_kit01.py, editable CM_SlateRoofKit01.blend, FBX library exports, shared roof slate material and validation reports. New source/imported paint maps, CharacterPassScope.json, CharacterComponentValidation.json, capture helper ArtSource/Pipeline/Review/CaptureRoofCharacterRefinement.cs and ten previews in Previews/CharacterRefinement. Corrected pre-pass source preserved in Archive/BeforeCharacterRefinement. Exact file inventory is in CharacterPassScope.json.

No gameplay/traversal, colliders, project settings or existing scene files changed. No packages installed, no commit created. Shared roof-kit assets also appear updated anywhere this kit is referenced; the independent approved building assets are untouched.
