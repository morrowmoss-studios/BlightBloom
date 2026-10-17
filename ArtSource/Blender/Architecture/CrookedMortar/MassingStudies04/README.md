# Crooked Mortar — three architectural massing studies 04

Review scene: Assets/Scenes/CM_CrookedMortar_MassingStudies04.unity. All three studies are present side by side and active. Earlier scenes and assets are preserved. All new architecture is authored in Blender; no texture work, foliage, furniture or decorative prop pass was performed.

## Reference and composition

Primary reference inspected directly: /Users/zak/Downloads/Storybook Apothecary by the River.png. The painting shows a dominant front gable, a long visible roof slope interrupted by a cross-dormer, a much smaller receding parallel wing, a sheltered shop entry, low shop-side roofing and staggered chimneys. The studies explore those relationships with a narrower, taller shop-house envelope rather than a broad residential master box. Hidden rear architecture and exact measurements are inferred; these are alternatives for architectural approval, not exact reconstructions of a single perspective image.

A — Layered Merchant House: closest to the reference's composition. 10.6 m hero ridge with unequal shoulders, a slightly lower roof on the narrower rear stem, cross-dormer, small parallel right-hand gable and a deep continuous shop canopy. The frontage has a real upper projection and the ground-floor shop/display volumes interlock beneath it.

B — Tucked Corner Apothecary: narrower front shop body, left-offset upper gable and 11.1 m ridge. The right-hand door wall is physically recessed 0.70 m behind the shop display wall, beneath a deeper projecting upper floor. Rear stem and secondary-wing roofs run crosswise, creating a more crowded urban-corner silhouette. Two folded canopy planes shelter the stepped frontage. It is a deliberate roof-orientation departure from the reference and is not the closest match.

C — Crooked Shop Cluster: 10.75 m upper shop-house, larger upper overhang and lower single-storey workroom volumes on both sides. A small gabled entrance shelter intersects an offset lean-to shop awning. The right-hand workroom stays subordinate; the private medical study moves into the main upper rear stem rather than occupying a second two-storey house extension. It explores a more additive shop cluster and departs from the reference's simple front canopy.

Recommended architectural starting point: A. B is the more tightly stacked urban alternative; C most strongly reduces the apparent height of the attached workrooms. Final selection remains a visual judgment for the user. Roof junction flashings, final exposed joinery and detailed window/shutter proportions remain outside this silhouette pass.

## Layout and traversal

A/B: public shop and recessed front entry, narrow dispensing bay, rear treatment area, side preparation/storage workroom, main rear garden door; bedroom/living in the upper front and private study in the upper side wing. C: comparable ground-floor flow plus a left shop alcove, with bedroom/living/study retained within the upper main body. Room intentions are empty hierarchy labels and sparse partitions, not fully resolved furnished plans.

Each option has an 18-rise straight shop-house stair and a real upper-floor opening. Ground and upper floor levels: 0.20 / 3.44 m. Rises 0.18 m, treads 0.28 m, clear stair mesh width 1.25 m. Roofs use thin shells and separate gable walls; no solid roof mass blocks the living storey. The final Blender meshes are explicitly triangulated and contain closed manifold components with positive signed volume.

Actual CharacterController Play-mode tests passed separately for A, B and C: 27/27 waypoints each, 81 total. Tests cover approach/porch/entry, stair ascent and descent, upper rooms, A/B upstairs side-study connection, ground-floor treatment/workroom connection, main rear garden exit, exterior return, and C's left alcove. They check both planar arrival and expected standing height. They do not certify future furniture clearance, subjective camera comfort or every possible route. Reports: Traversal_A.txt, Traversal_B.txt, Traversal_C.txt; Unity mesh/reference checks: UnityValidation.json. Existing controller is unchanged: height 2 m, radius 0.4 m, skin 0.04 m, step offset 0.3 m, slope limit 45 degrees.

## Opening and comparing

Open the review scene. Hierarchy roots are Study A / Study B / Study C. Select one and press F in Scene view. All share neutral URP materials, one daylight setup and the same review-camera framing. No postprocessing is used. Previews/ contains six original Unity captures and two labeled comparison contact sheets; during captures other study roots are temporarily hidden and then restored so they cannot intrude in each other's preview.

Press Play to start outside A; use the existing WASD/sprint/mouse controls. You can walk across the plain review site to B and C. For direct Edit-mode placement before Play, move Study04 Player to the corresponding spawn marker: A (-21.15,0.05,-7.5), B (0.85,0.05,-7.5), C (22.85,0.05,-7.5). The existing orbit camera follows its configured target. Spawn markers are under each study root. Review cameras are disabled for Play. Doorways are intentionally open; no interaction system was added.

## New files only

This source directory: build_massing_studies.py; three editable .blend files plus Blender iteration backups; three geometry-validation JSONs; studies.json; UnityValidation.json; three traversal reports; make_review_sheets.py; six full-size previews and two comparison sheets; this README.

Unity assets: Assets/BlightBloom/Art/Architecture/CrookedMortar/MassingStudies04/Models (three FBXs), Materials (neutral review materials), scene CM_CrookedMortar_MassingStudies04.unity, and Unity-generated .meta files.

External Editor eval utilities: ArtSource/Pipeline/Review/CreateMassingStudies04.cs, CaptureMassingStudies04.cs and TestMassingStudies04.cs. These are outside Assets and do not compile into the game. Scene creation refuses an existing scene; capture/tests reject an incorrect active scene. Blender regeneration refuses existing outputs unless --refine-created-study is passed, affecting only this study's own outputs.

No prior scene, gameplay script, approved art asset, package manifest or ProjectSettings file was changed. No packages installed; nothing committed.
