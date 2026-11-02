# Family Cottage A — Style Refinement 01

Review candidate in `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Saved, left in Edit mode with Cottage A selected. Stop for artistic approval before applying this treatment to another building. No commit, push, package import, cleanup or LFS work.

## Changes

- Nine project-owned URP/Lit material derivatives and eighteen 2048² textures: warm walnut timber/door/steps, warm cream plaster, muted blue-grey slate, quieter warm-grey masonry, muted iron and non-emissive glazing. Three existing low-visibility material roles remain shared from the package. Original package files are untouched.
- Timber uses a multi-tone palette and retained, softened directional grain. Plaster retains registered panel staining with reduced damaged-surface contrast. Roof courses are painted in mesh-derived surface coordinates, preserving rotated UV islands and reducing the original fine striping. Stone contrast and normal strength are reduced. These are reproducible atlas-paint derivatives, not newly sculpted individual roof tiles.
- URP metallic/smoothness maps explicitly pack metallic into red and inverted/controlled roughness into alpha, imported as linear data. Wood, plaster, stone, roof and glass are dielectric; glass has no emission. Original normal/AO textures are shared read-only with reduced strengths.
- Selective 2.5–7 mm timber bevels, softened prominent posts and beams, small eave-edge refinement, two entrance lintel pegs, a wider fitted leaf/frame and wider steps. Existing gable surfaces retain their original topology: experimental bevels produced import defects and were withdrawn.
- The entrance centre stays fixed. Its adjacent window panel is 84% of its former width and the narrow infill is 68%, each shifted 0.16 m to meet the wider frame. Total facade width, 7 × 6 m wall footprint, placement/yaw, dormer, chimney and roof volumes remain unchanged. Atlas registration is retained; these local width changes alter texel density slightly.
- Scene-local overrides use nine FBX mesh derivatives across 27 existing instances; no source prefab was applied or overwritten. Existing colliders follow the affected mesh/transform changes. No controller, camera, input or other gameplay script changed.

## Doorway and collision validation

Minimum measured frame/rebate clearance approximately **1.296 × 2.300 m**, sampled across depth and height, including the narrower back rebate. Door leaf is 1.27 × 2.27 m. Widened steps are approximately 1.55 m across.

The unchanged CharacterController is 2 m high, radius 0.4 m, step offset 0.3 m, skin width 0.04 m. Ten Play-mode CharacterController.Move checks passed with grounded endpoints: left/centre/right entrance lanes forward and reverse, local approach forward/reverse, and exterior perimeter forward/reverse. This is collision-path validation using the real capsule, not keyboard/manual playtesting or a camera-comfort certification.

The closed display door remains noninteractive and correctly blocks movement. Its collider was disabled only during the opening-clearance probe, then restored in `finally`, along with the normal motor, camera, player position and rotation. No new interior or door system was created; the short throat test does not establish a playable interior.

## Geometry/material checks

- Rendered cottage plus approach: **20,210 → 27,920 triangles**. Still 69 renderers and 12 shared material roles; this is not a batched village-production prefab or LOD pass.
- All sampled active meshes have finite vertices, complete UV0/normal arrays and unit-length normals. Final scan reports no degenerate triangles, missing materials or unsupported used shaders. UV/material registration inspected in matched front, angled and detail renders. New bevel strips and locally resized panels are not a complete texel-density reauthoring.
- Final FBX reimports and Play-mode validation produced no new Console warnings/errors; compilationFailed=false. Earlier in this pass, 44 import warnings identified self-intersecting polygons in experimental gable bevels. Those were resolved by retaining original gable topology and restricting/triangulating doorway bevels. `ConsoleValidation.json` distinguishes the retained historical messages from the final clean result.
- 160 scene objects outside the Cottage A hierarchy match the live pre-change component snapshot exactly. SHA256 comparison of 2,050 pre-existing protected files found only the authorized Briarwick scene changed; no files missing. Crooked Mortar, original package, production/interior scenes, gameplay/settings and tracking configuration remain byte-identical.
- No project-wide regression, build, horse-control test, interior traversal or manual camera-comfort test was run.

## Visual assessment and remaining issues

The first pass improves warm/cool balance, separates timber from plaster, softens photographic surface contrast and gives the entrance a believable human scale. It remains noticeably simpler and more regular than Crooked Mortar; it is a supporting cottage, not an ornate landmark. This is a cohesion improvement, not approval as final storybook environment art.

Roof tiles are mainly painted/normal-mapped over simple slopes. Some straight framing, repeated panel layouts and uniform glazing remain evident. Stone apron edges are still rectangular; no terrain or path layout was changed. No loose clutter was added to disguise these limitations. Further silhouette irregularity, unique painted wear, glazing depth or placement blending should await visual review. Repeated-village draw calls/LODs are future work.

## Matched visual review

Lighting, exposure/fog and camera conditions are identical before/after each paired view. No editing gizmos, depth of field or image grading. Source PNGs are retained. The benchmark pair uses the same 20 m horizontal offset, 9 m elevation offset, 55° FOV and 3.4 m target height; building orientations remain as placed, so their incident light angles differ.

- [Front](FrontComparison.jpg)
- [Three-quarter](ThreeQuarterComparison.jpg)
- [Timber, plaster and roof](MaterialsComparison.jpg)
- [Entrance](EntranceComparison.jpg)
- [Cottage versus unchanged Crooked Mortar](BenchmarkComparison.jpg)

## Files and reproduction

- Changed existing scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
- New project-owned assets: `Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageA/Style01/` — Models, Materials, Textures and Unity metadata. Ancestor-folder metadata is also new.
- Editable Blender source/scripts: `ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/`.
- Captures, guarded Editor snippets and validation records: this directory. `ChangedFiles.json` lists the full task file scope; existing unrelated working-tree changes were not staged or altered.

Read the source README before rerunning anything. The integration snippet refuses to run twice, because blindly reapplying the adjacent-panel changes would be destructive. Original modular assets remain available for recovery; scene changes are overrides only.
