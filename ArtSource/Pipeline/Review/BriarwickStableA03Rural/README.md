# Briarwick Stable A03 — rural thatch review

Status: saved review candidate, awaiting visual approval. 2026-11-01.

## Scope and preservation

`Assets/Scenes/Briarwick_Hamlet_Dev01.unity` now displays `Stable A - rural thatch review03` / `BW_StableA03_Rural` at the A02 location: (46, 5.98, -12), yaw 255°, scale 1. A02 remains intact in its inactive review root; A01 remains inactive. Toggle review roots exclusively to compare. No approved cottage, Crooked Mortar, imported package, gameplay, camera, terrain or production-scene assets were edited.

The 10.7 × 5.4 m body footprint, three bays, low partitions, enclosed tack room, fixed-open side service door, posts and separate approach remain. Original timber/material variation is reused. There are no main-front doors and no new loose props.

## Changes and editable sources

- Replaced only the old roof-covering faces with closed, subtly uneven thatch volumes, approximately 23–29 cm thick, softly rounded drip edges and a plain folded ridge. Existing timber understructure remains. The main front drip edge is approximately 1.34 m beyond the bearing posts; coverage is preserved.
- Added sparse timber through-pegs, ridge fixings and a fitted small corner-post repair. Body construction and floor/partition collision geometry are reused unchanged.
- Added one project-owned matte URP thatch material with dedicated 2048 px color, restrained normal and packed metallic/smoothness maps. No emission or metallic straw treatment. Broad slopes use continuous UV regions rather than repeated narrow texture strips.
- Source: `ArtSource/Blender/Architecture/Briarwick/StableA03Rural/BW_StableA03Rural.blend`. Hidden `REFERENCE_A02_WoodRoof_NOT_EXPORTED` collection retains the previous roof. `refine_thatch.py` documents construction/export; only three changed/new mesh groups were exported. Metric scale, FBX -Z forward / Y up, Unity +Z frontage.
- Painting source: `ArtSource/Paint/Architecture/Briarwick/StableA03Rural/Thatch_Painting01.ora`, with original generated painting and editable soft-finish layers. Built-in imagegen created the initial straw painting; `GenerationPrompt.txt` preserves its exact prompt. `prepare_material.py` performs controlled softening/color adjustment and map preparation. It does not replace the original generated source.
- Prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Prefabs/BW_StableA03_Rural.prefab`. New exports are under the sibling `Models/` folder, new material and maps under `Materials/` and `Textures/`. Unchanged body FBXs and materials remain referenced from A01/A02.

## Visual assessment and rural economy

The straw covering removes the regular shingle-course appearance, adds a thicker organic eave and makes this shelter materially distinct from the cottage and ornate apothecary. Muted oatmeal/taupe straw sits beside pale weathered timber without a walnut recolor or extra clutter. Plain ridge repair, sparse pegs and one local timber repair suggest practical maintenance and local labor rather than neglect. Agricultural straw and hazel fixings offer an economical local alternative to a landmark building's slate and ornamental work.

The candidate is visibly a thatched open shelter at gameplay scale. It remains a prototype: close-up fibers are rather evenly combed, ridge ends are simple, and the retained package gable/infill junctions remain more mechanical than the Crooked Mortar. It does not establish final cinematic lighting or final village landscaping.

**Historical limitation:** preserving the approved broad, low roof also preserves shallow pitches (approximately 23° front, 30° rear, 16° tack roof). Traditional thatch generally needs considerably steeper pitches for durable water shedding. This pass is a visual material/construction candidate, not a claim of historically weather-resolved thatch. A future pitch revision needs explicit architectural approval; it was not silently introduced here. Local material use and plain ridge maintenance follow the conservation guidance in [Historic Environment Scotland](https://www.engineshed.scot/building-advice/building-components/roofs/thatched-roofs/) and [SPAB](https://www.spab.org.uk/advice/thatched-roofs).

## Targeted validation

- A03 building: **22,088 triangles**, versus A02 **14,956** (+7,132). Ten mesh renderers; eight shared materials. Separate approach: 52 triangles, excluded from building total. New thatch 6,204; joinery 948; retained roof understructure 276 triangles. No dense grass cards, transparency or foliage overdraw were introduced.
- Mesh arrays: UVs present, finite vertices/UVs, unit normals and no zero-area geometry triangles in Unity's imported meshes. Twenty roof downward rays hit upward-facing covering. Visual inspection of front, main slopes, ridge, eaves and tack junction found no gross gaps or lost roof coverage; intentional layer seating is retained.
- Three front bays: approximately **2.491 m clear width × 3.23 m height**. Side service entry **1.30 × 2.30 m**.
- Horse-envelope box **1.2 × 2.6 × 2.8 m**: 369 sampled positions, none blocked. This is geometric clearance, not an animated horse or mounted movement test.
- Floor coverage: 377 samples, zero misses. Front access: 27 probes, zero obstructions.
- Play-mode existing CharacterController.Move: **26/26 forward/reverse route cases passed**, grounded throughout. Covered all bay lanes, side entry, tack connection/cross aisle, perimeter and approach spur. Existing 2 m height / 0.4 m radius controller unchanged. Probe temporarily paused motor/orbit, then restored all normal runtime state. This is automated controller/collision validation, not keyboard-driven manual camera-comfort approval.
- Console after import and Play test: no new warnings/errors after starting cursor 44; current Editor counts zero warnings and zero errors, compilationFailed false. Pipeline briefly disconnected at Play reload and reconnected without project changes; route test then completed.
- Compared 2,334 protected existing files by SHA-256: only the intended hamlet scene changed. Existing scene component snapshots outside the A03 review root match the baseline; A02's known active-state change is intentional. All A02 files, approved buildings, imported assets and production scenes remain unchanged. See `PreservationValidation.json`, `StaticValidation.json` and `PlayValidation.json`.
- No project-wide regression, performance benchmark, actual horse simulation or manual artistic approval was performed. No commits or pushes.

## Review images

- `Front_BeforeAfter.png`: A02 and A03, matching camera/lighting.
- `RuralA03_ThreeQuarter.png`: roof and open bays.
- `RuralA03_ThatchEavesAndTimber.png`: close-up.
- `RuralA03_RoofAndLeanTo.png`: tack roof and junction.
- `RuralA03_GameplayApproach.png`: human approach height.
- `VillageMaterialComparison.png`: A03, approved cottage and Crooked Mortar in unchanged scene lighting, approximately matched 20 m camera offsets. Different orientations/aspects remain visible; no materials were adjusted to force identical color.
- Camera data: `RuralA03_CaptureConditions.json`.

Unity is left in Edit mode with the saved Briarwick scene open and A03 selected. Stop here for visual approval.
