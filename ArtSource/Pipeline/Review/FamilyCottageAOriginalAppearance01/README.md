# Family Cottage A — original appearance restored

Current candidate: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. The original package's pale weathered timber, subdued plaster, brown shingles, masonry and muted palette are now the preferred visual reference. Style01's walnut/ivory/blue-grey treatment is retained only for comparison. Stop for visual approval.

## Changes

Created twelve project-owned material copies under `Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageA/OriginalAppearance01/Materials/` and assigned them to the cottage's 69 renderers. Copies retain the original URP shaders, colour/normal/roughness/AO/metallic atlas references, texture transforms, shader properties, keywords, pass states, render queues and instancing/GI flags. No tinting, texture editing, contrast cleanup, shader conversion or lighting changes. Unchanged source textures are shared read-only instead of duplicated or regenerated.

Kept all Style01 geometry: corrected leaf and frame, threshold/steps, fitted adjacent window/infill, timber softening, joinery and eave refinements. No meshes, UV coordinates, colliders, transforms, placement, footprint, massing, dormer, chimney or roof volumes changed. Rendered triangles remain **27,920**. The existing Style01 Blender/FBX source remains the editable geometry source; this material-only restoration needs no model regeneration.

## Validation

- All twelve material copies match their source shader properties, texture identities/transforms, keywords and render flags; no missing textures or unsupported shaders.
- Mesh UV0/normal arrays remain valid; no degenerate triangles. Matched detail views show original atlas registration on retained geometry. The larger leaf and narrowed adjacent infill retain Style01's differing local texel density; no new UV deformation was introduced.
- Remeasured minimum frame/rebate opening **1.296 × 2.300 m** across depth/height. Existing controller unchanged: height 2 m, radius 0.4 m, skin 0.04 m. Approximately 0.248 m lateral space per side and 0.300 m headroom at the measured narrowest opening.
- Exact component snapshots confirm all cottage non-renderer components, including transforms, mesh references and colliders, unchanged. All 160 inspected objects outside the cottage also match.
- Prior Style01 Play-mode controller route results remain historical evidence, not a new test. They were not rerun for this material-only change. No interior, interaction or camera-comfort claim. The display door remains closed, solid and noninteractive.
- Final Console: no new errors/warnings, compilationFailed=false. Retained 44 historical import warnings belong to the earlier, repaired Style01 experiment; none occurred during this restoration.
- SHA256 check of 2,171 protected existing files: only the authorized Briarwick scene changed; none missing. Style01 assets, editable source, scripts, reports and captures are byte-identical, as are the imported package, Crooked Mortar and other protected assets/settings.

## Visual comparison

Matches the original's organic grain, mottled plaster and weathered brown shingle finish rather than cleaning or brightening it. Softened geometry and the larger entrance intentionally differ from the original. The cottage remains smaller and less ornate than Crooked Mortar; no attempt was made to copy its slate colour or ornament.

Captures use the existing review camera and unchanged scene lighting/fog. Original reference images are reused from Style01's `Before_*` captures without altering those files. Benchmark views share 20 m horizontal offset, 9 m elevation offset and 55° FOV; the buildings retain different orientations in the same lighting.

- [Original screenshot versus restored cottage](OriginalVsRestored.jpg)
- [Original entrance versus retained corrected doorway](EntranceComparison.jpg)
- [Timber, plaster and roofing comparison](MaterialComparison.jpg)
- [Restored cottage versus unchanged Crooked Mortar](CrookedMortarComparison.jpg)
- [Full front](Restored_Front.png)

## File scope and recovery

Only existing file modified: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
New files: twelve material copies and Unity metadata in `OriginalAppearance01/`, plus this review folder's guarded restoration/validation snippets, records and captures. `ChangedFiles.json` records the task scope.

`Style01RendererAssignments.json` records the prior material assignments for recovery; all referenced Style01 assets are retained. No imported-package, Crooked Mortar, gameplay or project-setting changes. No cleanup, archiving, LFS changes, commits or pushes.
