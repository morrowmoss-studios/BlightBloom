# The Crooked Mortar — CM_EntranceBay01

First isolated entrance-bay art prototype, using the approved `CM_WindowBay01_Painted_v02` as the material/shape benchmark. No playable facade installation has occurred.

## Open and review

- Unity: `Assets/Scenes/CM_EntranceBay01_ArtReview.unity` (currently open in the existing Editor).
- Prefab: `Assets/BlightBloom/Art/Architecture/CrookedMortar/EntranceBay01/Prefabs/CM_EntranceBay01_Painted_v01.prefab`.
- Editable source: `CM_EntranceBay01_Painted_v01.blend` beside this README. Paint source and baked atlas are packed. Use Material Preview to view textures.
- Geometry-only editable source: `CM_EntranceBay01_Geometry_v01.blend`.
- Previews: `Previews/Painted_v01/Front.png`, `ThreeQuarter.png`, `GameplayDistance.png`.
- Review is static; no Play mode, player or runtime script is required. The 8m gameplay-distance camera is at 1.7m above ground, with a 55-degree vertical field of view.

The review uses the same neutral directional-light/ambient values, matte URP setup, background and front/three-quarter camera positions as the approved window review. No bloom, fog, blur, grading or renderer changes were made.

## Architecture and scale

Nominal wall: **3.4m wide × 3.6m storey height × 0.32m thick**. Full decorative bounds are approximately **3.7196m wide × 3.7574m tall × 1.3949m deep**.

The rough arched opening is 1.8m wide, springing at 1.7m and reaching 2.65m. The fitted leaf is approximately 1.75m wide, built from five planks with separate curved timber stops/jambs and a true thick wall opening. Its bottom is 0.22m, with a 0.20m stone threshold and a 0.09m lower step. A 2cm gap avoids the leaf intersecting the threshold.

The existing gameplay opening is 2.4m wide. The new 1.8m entrance is an isolated visual design choice, not an approved change to that clearance. Future installation must resolve jamb infill, door swing, camera/head clearance and collision proxies explicitly. Do not drop this closed door into the playable route without an integration pass.

Parts include:

- Through-cut plaster shell and a hewn stone surround with 11 curved voussoirs and four jamb blocks per side.
- Curved timber door stop, jambs, rear bracing, forged strap hinges, ring pull and a small sage diamond inlay.
- Slightly bowed walnut posts/header, knee braces, continuous canopy boarding, rafters/fascia and five staggered slate courses.
- Wide threshold/lower step, small hanging mortar-and-pestle emblem board, and two sparse authored herb bundles.

The ring, straps, plank and rear-brace meshes are combined into one logical `03_Door_Leaf_Hinged` mesh with three material slots. Its Blender pivot is (-0.89,-0.03,0.20), mapping to Unity (-0.89,0.20,-0.03), ready for a future hinge hierarchy. It has no interaction code, animation or colliders. Other mesh parts have semantic numbered prefixes, consistent with the window module.

## Palette and painting

The exact approved source `ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png` is reused without modifying it: warm ivory, restrained walnut grain, sage accents and mossy blue-grey slate. Warm stone derives from the ivory painting with a restrained neutral tint, rather than a new realistic noise material. Iron uses a simple matte dark color.

`Assets/BlightBloom/Art/Architecture/CrookedMortar/EntranceBay01/Textures/CM_EntranceBay01_Painted_BaseColor_v01.png` is a unique 4096×4096 sRGB atlas with 16px bake padding. Six semantic URP Lit materials are under `Materials/CM_Entrance_Painted_*.mat`; metallic/smoothness are zero and specular/environment highlights are disabled. No normal, displacement, AO or emission maps are added.

Brushwork follows timber length, with an explicit vertical door projection so dense handle/hinge geometry cannot skew its grain direction. Horizontal stone step surfaces have a proper two-dimensional paint sample. This uses actual approved image brushwork, not shader noise or a lighting filter. The source painting's native resolution remains 1254×1254; the atlas is a 4K bake target, not native 4K painted detail.

## Validation

95 mesh parts, **20,040 triangles**. Blender checks closed manifold edges, positive signed volumes and absence of degenerate faces. Shell ray probes confirm a real opening. Both structural posts have more than 2cm roof-boarding clearance; no post tops pierce the canopy. The imported root has scale (1,1,1), zero rotation and the expected bounds/axis mapping. All material slots have valid URP textures and normals/UV arrays pass checks. No new Console warnings/errors; compilation failure is false.

The initial UV audit found four sub-pixel intersections around one plaster-shell bevel face. `repair_shell_uv.py` isolates that face as its own UV island and repacks the unique atlas without mesh edits. The final layout has zero positive-area overlaps at the audit tolerance (1e-9 UV area), and all UVs are in 0–1. Median density is about 265 atlas pixels/metre at 4K, with 5th/95th percentiles around 242/279. This is lower than the smaller window's 337px/m but uses the same physical brush projection scale; prioritize higher atlas density only if close-up review warrants it.

Reports: `geometry_validation.json`, `uv_repair.json`, `uv_validation.json`, `unity_validation.txt`; UV guide: `CM_EntranceBay01_UV.svg`. Painting-transfer fingerprints are under `ArtSource/Paint/Architecture/CrookedMortar/EntranceBay01/texture_validation.json`.

Existing scenes (including the approved window review), approved window source/export/textures/materials, traversal scripts, Packages and ProjectSettings retain their pre-task hashes. No commits or package installations.

## Authoring and remaining work

Reproduction order: `build_entrance_bay.py`, `repair_shell_uv.py`, then `ArtSource/Paint/Architecture/CrookedMortar/EntranceBay01/bake_entrance_painted_pass.py`. Run in headless Blender. Creation normally refuses existing output; the bake's `--refine-this-new-asset` flag is explicit iteration support. Unity creation/capture/validation utilities are in `ArtSource/Pipeline/Review/` with EntranceBay in their names; they are not runtime scripts. The scene creator refuses existing scene output.

This is a review prototype, not finished production art. The sign is an emblem without finalized lettering; herb bundles are sparse low-poly silhouettes. Door swing/rebate joinery, unique edge/end-grain painting, final stone wear and optional render batching/LODs remain review decisions. Static parts are separate for reuse, not yet optimized into a final shipping draw-call budget. No gameplay behaviour or collisions were introduced.
