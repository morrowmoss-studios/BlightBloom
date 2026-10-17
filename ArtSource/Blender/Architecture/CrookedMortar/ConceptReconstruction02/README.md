# Crooked Mortar — concept reconstruction 02

This separate, neutral architectural study was built from the supplied Storybook Apothecary by the River image after preparing Analysis/MassingDiagram.png. The playable apothecary and ArchitecturalRedesign01 scenes are preserved.

## Reference interpretation

A: dominant steep longitudinal roof, prominent front gable, slightly jettied upper frontage. B: a cross-dormer cut into its visible roof slope, rather than a full-height transverse house wing. C: a narrower, lower parallel-gabled wing set back on the right. P: a 2.2 m deep open porch across the front, with the entrance recessed behind its beam. D: a low side-shop extension beneath the upper windows. Two staggered chimney stacks complete the roof silhouette. Roof profiles have flared lower slopes and deliberately staggered ridges.

The visible roof relationships follow the illustration; exact metric dimensions, unseen rear elevations and interiors are design inferences. This is an architectural approval study, not a claim of exact perspective reconstruction.

## Functional adaptation

The main ground-floor frontage and low side extension form the public shop. Rear-right is treatment, connected to the right wing's preparation room, rear storage and garden door. An 18-rise U stair occupies the main rear-left volume. Upstairs contains front-left bedroom, front-right living space, rear reading nook and the lower parallel wing's library/study. Floors are 0.20 and 3.35 m. Stair rises are 0.175 m, treads 0.29 m and flights 1.25 m wide.

The new mesh contains real door/window apertures and a Boolean-unioned cross-dormer. Attic roof volumes are solid massing proxies, not accessible roof interiors or finished roof construction. Roofing thickness, valley flashing, final joinery and final window-to-gable composition remain for the next architectural/art review. Interior purposes are hierarchy labels; no decorative furniture was added.

## Assets and tools

Editable source: CM_ConceptReconstruction02.blend; its .blend1 is Blender's iteration backup. Reproducible construction source: build_concept_reconstruction.py. New FBX and neutral matte URP materials live in Assets/BlightBloom/Art/Architecture/CrookedMortar/ConceptReconstruction02. Approved window and entrance prefab instances are reused with scene-only neutral material overrides, selective parts enabled and independent proportions. Their source assets are unchanged. The door is held open in the playable scene; preview capture temporarily closes it and restores it.

Review scene: Assets/Scenes/CM_CrookedMortar_ConceptReconstruction02.unity. Open it and press Play. Existing WASD/sprint/mouse traversal scripts and input actions are reused without code changes. Escape releases cursor as configured by the existing system. Three disabled review cameras and Previews/*.png provide front, concept-side three-quarter and right elevation views. No postprocessing is used to hide geometry.

New Editor eval utilities, kept outside Assets: ArtSource/Pipeline/Review/CreateConceptReconstruction02.cs, CaptureConceptReconstruction02.cs and TestConceptReconstruction02.cs. The creation utility refuses an existing scene. Blender regeneration similarly refuses overwrite unless explicitly passed --refine-created-study, which applies only to this new study.

## Validation

25 authored mesh parts, 2,932 triangles excluding approved modules. Blender reports closed manifold components and positive signed volumes; Unity confirms UV and normal arrays, unit root scale, assigned colliders and no missing scripts/material errors. A real CharacterController was driven through 35 waypoints in Play mode: approach, entrance, both flights up/down, bedroom/living/study, treatment, preparation/storage, rear garden exit, outside return and side shop. All passed; see traversal_validation.txt. This checks collision routes, not subjective camera comfort or final furniture clearance. Manual Play review is still recommended.

No existing scene, gameplay script, package or project setting was changed. No packages were installed and no commit was made.
