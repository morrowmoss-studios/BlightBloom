# The Crooked Mortar — painted window refinement v02

## Roof diagnosis and correction

The two visible blocks were the tops of `04_Left_Structural_Post` and `04_Right_Edge_Post`, not the eave rafters. In the v01 Blender source their vertices rose about 13.84cm and 12.25cm above the nominal slate underside respectively. Rafters already lay below the roof.

Opened the existing editable `CM_WindowBay01_Painted_v01.blend`. Reshaped only the top portions of those two posts to follow the roof boarding underside, leaving at least 1.5cm clearance below it. Post meshes remain closed solids with the same topology; they integrate into the beam/roof zone. No pieces were deleted. Shingles, rafters, roof boarding, roof silhouette, window, shutters, planter and all other geometry remain unchanged. The source was saved as `ArtSource/Blender/Architecture/CrookedMortar/WindowBay01/CM_WindowBay01_Painted_v02.blend`.

## Painting refinement

`Sources/GouacheMaterialSheet_v02.png` is a new image-generation edit of the v01 painting, using the selected concept as a style/palette reference. `Sources/prompt_v02.txt` records the exact built-in image-generation prompt. Native returned resolution is 1254×1254. Grain now uses fewer broad, lower-contrast ribbons; shutters have quiet sage strokes rather than distressed stripes; slate has larger calm moss/blue-grey color groups; plaster has broader, cleaner ivory planes. No blur, procedural noise, shader noise, bloom, fog, exposure, grading or lighting adjustments were used.

The new painting is transferred into `Textures/CM_WindowBay01_Painted_BaseColor_v02.png`, a 4096×4096 sRGB atlas with 16px padding. 4K is the bake/UV target, not a claim of native 4K painting detail. Temporary projection coordinates are removed before saving; the original unique UV0 layout is retained. Reveal projection was corrected to give side surfaces a two-dimensional paint sample instead of stretching a single texture column. Painted source and atlas are packed into the editable v02 .blend.

## Unity review and files

Under `Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01/`:

- `Models/CM_WindowBay01_Painted_v02.fbx`
- `Textures/CM_WindowBay01_Painted_BaseColor_v02.png`
- `Materials/CM_Painted_*_v02.mat` (six semantic matte URP Lit materials)
- `Prefabs/CM_WindowBay01_Painted_v02.prefab`

`Assets/Scenes/CM_WindowBay01_ArtReview.unity` now displays `CM_WindowBay01_PaintedReview_v02`. Neutral and v01 instances remain inactive for comparison; their source assets are untouched. Enable only one instance at a time when comparing. The original review camera and lighting snapshots compare identically. Front, ThreeQuarter and GameplayDistance previews are saved in `ArtSource/Blender/Architecture/CrookedMortar/WindowBay01/Previews/Painted_v02/`. Both protrusions are absent in the inspected updated views.

Authoring utilities: `refine_painted_pass_v02.py` here, and `ArtSource/Pipeline/Review/ApplyWindowBayPaintedPassV02.cs` / `CaptureWindowBayPaintedPassV02.cs`. These create sibling assets and refuse existing v02 output. No gameplay scripts were introduced.

## Validation

`texture_validation_v02.json` records post clearances and source fingerprints. Blender checks manifold edges, positive signed volume and absence of degenerate faces on all 82 meshes. An independent source comparison confirmed UV coordinates and topology counts remain unchanged, including the two post meshes. Other 80 mesh fingerprints are unchanged.

`unity_texture_validation_v02.txt`: 82 meshes, 13,424 triangles, correct original overall bounds, unit root scale, zero root rotation, valid normals, UV coordinates in 0–1. The two deformed posts have two additional split rendering vertices each in Unity due to recomputed normals; this does not add source geometry or triangles. Imported UV coordinate sets match. All other mesh vertex streams remain unchanged. No colliders were introduced.

No new Console warnings/errors were observed and compilation failure is false. Existing playable scenes, traversal scripts, package configuration, ProjectSettings, neutral source and v01 source/export/material/texture/prefab assets retain their pre-task hashes. No software installed or Git commits created.

## Art review limits

This is a quieter AI-painted prototype, not a final artist-painted master. Broad color groups intentionally replace detailed grain and stone texture. Per-joint wear, end-grain painting and localized edge accents could still benefit from an artist painting directly on the retained UV atlas. No additional decoration or foliage was added.
