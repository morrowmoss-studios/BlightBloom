# The Crooked Mortar — architectural reconstruction 03

New scene: Assets/Scenes/CM_CrookedMortar_ConceptReconstruction03.unity. Open and press Play; uses the existing traversal/input/camera scripts and a 2 m high, 0.4 m radius CharacterController with its existing 0.3 m step offset. The main door is held open in the playable scene. Review capture temporarily closes it, hides the player capsule, then restores both.

## Reference-driven reconstruction

Primary reference inspected directly: /Users/zak/Downloads/Storybook Apothecary by the River.png.

The painting's form is a dominant narrow front gable carrying one long steep roof, a cross-dormer on the visible roof slope, a smaller receding parallel gable to the right, a deep sheltered shop frontage, a low side extension, and two staggered chimneys. The roof hierarchy and sheltered doorway are the architectural reference. Hidden rear elevations, exact measurements and internal partitions remain design inferences.

Compared with study 02:

- Rebuilt the main roof as a thin shell with separate front/rear gable walls, rather than an opaque solid triangular attic mass. The front arched opening now crosses into the gable itself. The approved window is proportioned taller to fit the illustration's lancet-like opening; it no longer dictates a squat wall panel below a large blank triangle.
- Main roof profile has an offset ridge, steep left shoulder, longer right slope, flared eaves and a slight fall toward the rear. Front ridge height is 9.30 m; major chimney pots reach 9.925 m. Roof and chimney heights now form a closer group.
- Narrowed the entire side wing, including floors, openings and roof, by 18 percent. Its smaller roof remains below the main ridge, with a visible intersecting dormer between the two gables.
- Extended the low side shop volume forward to the main shop front wall. Its sloping roof now meets the deep entrance canopy, rather than reading as an isolated rectangular attachment. The actual enclosed footprint and circulation change with that extension.
- Added only the principal gable tie/kingpost/brace and porch supports. No foliage, prop dressing, textures or material polish. All materials are matte neutral review colours.
- Trimmed the buried main eave inside the secondary wing connection and raised its ceiling to preserve CharacterController headroom. Fitted the dormer window beneath the roof slopes.

This is a reviewable interpretation, not an exact camera solve or a claim that all architectural proportions are final. The roof valley junctions and unseen rear construction remain prototype geometry. The secondary roof retains a closed attic mass; the main roof is hollow. Final timber joints, tile layers and detailed architecture are deliberately outside this pass.

## Functional layout

Front ground floor: public shop, dispensing side bay and recessed entry under the 2.2 m deep porch. Rear main volume: treatment to the right, U stair to the left. Narrow side wing: preparation room, rear storage and garden exit. Upper floor: bedroom, living area, reading nook and side-wing medical library/study. Functional rooms are represented by partitions and hierarchy labels, without decorative furniture.

Floor levels remain 0.20 m and 3.35 m to reuse the tested U-stair circulation: 18 rises of 0.175 m, 0.29 m treads and 1.25 m wide flights. Footprint/roof/upper-front architecture were changed around this circulation. No gameplay code changed.

## Files and verification

Editable Blender source and reproducible build script are in this folder, with Blender's .blend1 iteration backup. Exported FBX and neutral URP materials are in Assets/BlightBloom/Art/Architecture/CrookedMortar/ConceptReconstruction03. Approved window/entrance prefabs are reused with scene-only transforms, selective parts disabled and neutral material overrides; their original assets were not changed.

New eval utilities outside Assets: CreateConceptReconstruction03.cs, CaptureConceptReconstruction03.cs, TestConceptReconstruction03.cs and ValidateConceptReconstruction03.cs in ArtSource/Pipeline/Review. Scene creation refuses overwrite. Capture/test/validation reject the wrong active scene.

Previews/ contains Front.png, ThreeQuarter.png and Side.png captured from the running Unity Editor. The three-quarter camera sees front and right elevation at a low elevation comparable to the concept, without postprocessing.

Blender reports 25 closed-manifold authored mesh parts with positive signed volume. Unity imports 3,128 triangles, complete UV/normal arrays, unit root scale and assigned mesh colliders. No missing scripts or material errors. Final Play-mode CharacterController test passed all 35 waypoints, covering approach, entry, stair ascent/descent, bedroom/living/study, treatment, preparation/storage, garden exit, exterior return and side shop. See traversal_validation.txt and unity_validation.json. This verifies route collision traversal, not subjective camera comfort or future furniture clearance.

Existing scenes, gameplay scripts, packages and ProjectSettings were hash-checked unchanged. No packages installed or Git commits made. Manual visual and Play review is the next step.
