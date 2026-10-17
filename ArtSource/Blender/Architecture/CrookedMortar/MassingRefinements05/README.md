# Crooked Mortar — middle-option refinements 05

Scene: Assets/Scenes/CM_CrookedMortar_MassingRefinements05.unity.

All three variants derive exclusively from CM_Massing04_B, the middle "Tucked Corner Apothecary" option in CM_CrookedMortar_MassingStudies04. The BASE dictionary in build_refinements.py records its original configuration and each variant's overrides. Previous A/C options were not used as architectural bases. Primary art reference was inspected directly at /Users/zak/Downloads/Storybook Apothecary by the River.png.

## Variants

A — Conservative Refinement. Keeps the selected footprint and crosswise rear/side roof arrangement closely intact. The hero ridge reduces from 11.1 to 10.65 m, and the front arch becomes a smaller, wider divided domestic window with simple shutter masses, rather than a tall chapel-like opening. The two-part canopy attaches outside the upper facade and shelters the stepped ground-floor entry.

B — Moderate Refinement. Retains the same circulation spine but lowers the main/rear/side ridge hierarchy to 10.40 / 8.55 / 7.55 m. The front feature becomes paired casements under a shared lintel/sill. The side wing narrows and sets back; its leading edge is raked in plan instead of remaining square to the facade. The door recess deepens behind a return cheek and the projecting upper floor. The main roof falls gently toward its lower rear roof.

C — Bold Refinement. Uses the same two-storey arrangement and crosswise rear roofs, with a 10.25 / 8.30 / 7.35 m ridge cascade, a more offset front peak and stronger rearward roof fall. A shallow polygonal oriel is actual extra upper-floor space with paired windows, angled cheeks, support brackets and its own hood. The canopy is notched around it and tied beneath the bay floor, creating an additional architectural layer. The narrow side wing has the strongest setback and plan rake. The entry is the deepest of the three.

These are architecture/shape studies in neutral materials. No texture polishing, foliage, furniture or final decorative dressing was added. Exact rear construction, roof valleys/flashing, final structural joinery and furnished room clearances remain unresolved prototype work. Changes are intentionally incremental from the chosen middle option; these are not replacements with unrelated architectural schemes.

## Function and validation

The original middle option's front shop, rear treatment/preparation, side workroom/study, bedroom/living and rear garden route remain viable. All three retain the same 18-rise straight stair, 0.18 m rises, 0.28 m treads, 1.25 m stair mesh width and actual upper-floor void. Floor levels remain 0.20 and 3.44 m.

Final real CharacterController Play-mode route checks: A 27/27, B 27/27, C 30/30, including C's accessible oriel. Tests check arrival and expected standing height through porch/doorway, stair ascent/descent, upper rooms and study connection, ground treatment/workroom, rear exit and outside return. CharacterController settings remain height 2 m, radius 0.4 m, skin 0.04 m, step offset 0.3 m, slope limit 45 degrees. Reports are Traversal_A.txt, Traversal_B.txt and Traversal_C.txt. This is route validation, not a substitute for manual camera/comfort testing or future furnishing clearance.

Blender reports closed manifold components with positive signed volume. Unity confirms unit scale, UV/normal arrays, colliders, no missing scripts and no material errors. Triangle counts are 4,316 / 4,084 / 4,214 for A/B/C; see UnityValidation.json and individual geometry reports.

## Review

The scene opens all three variants side by side, with common neutral URP materials, daylight and matching review cameras. Previews/ contains A_Front.png, A_ThreeQuarter.png, B_Front.png, B_ThreeQuarter.png, C_Front.png and C_ThreeQuarter.png, plus labeled comparison sheets. Individual captures temporarily hide the other variants and restore all root states before saving.

Press Play to start at A. Existing WASD/sprint/mouse controls are reused. Walk across the plain review site to B/C, or set Study05 Player to the relevant spawn marker before Play: A (-21.15,0.05,-7.5), B (0.85,0.05,-7.5), C (22.85,0.05,-7.5). Select the variant root and press F in Scene view for architectural inspection.

## New outputs and preservation

Editable source: three CM_Refinement05_*.blend files and Blender iteration backups, build_refinements.py, studies.json, geometry/Unity/traversal reports, preview captures, make_review_sheets.py and this note.

Unity assets: Assets/BlightBloom/Art/Architecture/CrookedMortar/MassingRefinements05/Models (three FBXs), Materials (neutral review materials), the new scene and Unity .meta files. External Editor eval utilities are ArtSource/Pipeline/Review/CreateMassingRefinements05.cs, CaptureMassingRefinements05.cs and TestMassingRefinements05.cs; they are outside Assets and do not compile into the game.

Creation refuses an existing scene. Capture/test utilities reject an incorrect active scene. Blender refuses existing output unless explicitly passed --refine-created-study, which affects only this new study's own assets. The prior massing studies, playable apothecary, approved art modules, gameplay scripts, input actions, package files and ProjectSettings were hash-checked unchanged. No software/packages installed and no Git commit made.
