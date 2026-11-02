# Briarwick Bakery01 — first architectural review

Status: review candidate, awaiting visual approval. 2026-11-01 local development session.

## Building and integration

Scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
Prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Prefabs/BW_Bakery01.prefab`.
Scene root: `Bakery - architectural review01` / `BW_Bakery01`.

Original bakery position (19, 5.84169626, -10), yaw 270°, scale 1 is preserved. `04 Bakery PLACEHOLDER` is disabled, retained in its original hierarchy. Existing `Path_Bakery` remains unchanged; its road end leads to the customer frontage. No other locations, terrain, lights or gameplay systems were modified.

The bakery is a modest one-storey timber/plaster structure with a hipped pan-and-cover clay roof, two front lights, small side windows and a prominent rear masonry oven/chimney. It avoids the cottage's tall gable/dormer composition and the stable's open thatched shelter. Plain joinery, soft weathered package timber and subdued plaster remain quieter than the Crooked Mortar landmark. No signs, loose clutter, ovens systems, NPCs or interior furnishing were added.

## Dimensions and cost

- Nominal wall centre-line footprint: **6.6 × 7.4 m** (outer plaster approximately 6.82 × 7.62 m).
- Complete geometry bounds including overhang, hip caps and oven projection: **7.627 × 9.264 m**. Within/near the original approximately 8 × 9 m site.
- Height above placement datum: **6.469 m** to chimney; roof ridge approximately 4.76 m. Underground foundation extends to -0.28 m, so full mesh bound height is 6.749 m.
- Customer opening **1.40 × 2.40 m**; service opening **1.30 × 2.30 m**. With the existing 2 m tall / 0.4 m radius player these leave 0.60/0.50 m total lateral and 0.40/0.30 m overhead clearance respectively. Frame rays measure these dimensions with static leaves excluded.
- Both leaves are **static and closed**. There is no bakery door interaction or complete interior; gameplay tests cover safe approaches, not entry through a closed leaf. Openings, separate leaf objects and named markers support future integration.
- **91,001 triangles**, ten renderers, ten used shared materials. Roof tiles account for 77,069 triangles. This is a first visual/architectural candidate, not a final village performance budget. A roof LOD/bake and simpler overhead collision are recommended after approval.

## Sources and dependencies

- Editable Blender: `ArtSource/Blender/Architecture/Briarwick/Bakery01/BW_Bakery01.blend` (packed working color textures).
- New FBX group exports: `Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Models/`.
- New derivative materials and maps: sibling `Materials/` and `Textures/` folders.
- Painted clay master: `ArtSource/Paint/Architecture/Briarwick/Bakery01/ClayTile_Painting01.svg`, eight muted kiln swatches. Individual curved pans and seam covers provide depth, not a shingle texture recolor. Clay is nonmetallic, very low smoothness and nonemissive.
- Clean plaster derivatives preserve a soft unframed region of the package painting; frame-specific baked AO is deliberately omitted. `PlasterRegion.json` records the crop. The initial atlas reuse produced black diagonal timber shadows, which were identified in Unity and corrected. Original package files and approved cottage materials were never edited.
- Other material derivatives start from the approved restored cottage's original-appearance materials. Native package UVs are retained on posts, stone, door details and oven/chimney. Bakery glazing is opaque/dim, with no emission and muted smoothness, to avoid showing an absent interior through the building.
- Native mesh source catalog: `ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json`; export/UV helper functions reused read-only from `StableA02OpenFront/build_open_stable.py`. Native geometry derives from the installed `Assets/Medieval_house_lite/` package. Its textures and Autodesk Interactive URP shader remain required, plus standard URP Lit for clay/glazing. No new package was installed.
- `Dependencies.json` provides the exact Unity dependency list; `ModelCatalog.json` provides mesh groups/counts. The prefab has no new MonoBehaviours or gameplay-script dependency.

## Targeted validation

- Imported UVs/vertices finite, UV and normal arrays present, unit normals, no zero-area geometry triangles, supported shaders and no missing texture references.
- Correct metric orientation/scale; source +Z frontage maps to original road-facing yaw 270°.
- Main roof slopes, caps, eaves and chimney penetration visually inspected in front, three-quarter, roof and player-height images. No gross uncovered joins were observed; overlapping tile laps are intentional. This does not replace final hand-fitting of every tile.
- Foundation contact checked at nine ground samples: relative ground level approximately -0.000715 to +0.000457 m from placement datum. No terrain edits or floating foundation at these sampled positions.
- **16/16 existing CharacterController.Move Play-mode cases passed**, grounded, in both directions: three customer approach lanes, three service approach lanes, exterior perimeter and road connection. Motor/orbit paused only during probe and restored; player restored after testing. This is automated collision/navigation validation, not keyboard/manual camera-comfort approval. Neither controller dimensions nor shared scripts changed.
- Existing scene component snapshots outside the new review root match the 306-object baseline. The original placeholder's disabled active state is intentional. Protected-file hashes compare 2,364 existing files; only the intended hamlet scene changed.
- No new captured Console warnings/errors after baseline cursor 44; current compilationFailed false. Relevant proof: `StaticValidation.json`, `PlayValidation.json`, `PreservationValidation.json`, `ConsoleValidation.json`.
- No unrelated project-wide regression, interior/door interaction test, horse test or performance benchmark was performed.

## Remaining review items

1. Tile courses/hip convergence are still quite regular and detailed for a village building. Review their scale and restrained clay color before refinement; roof LOD and simplified roof collider are not yet provided.
2. Plaster uses a cropped source region and simple panels; repeated blemishes/panel seams and general architectural plainness remain visible up close. This is not a final artistry pass.
3. Bakery identity relies on the large working chimney, oven mass and entrance composition; there is no dedicated trade sign, smoke or serving counter.
4. Opaque glazing intentionally avoids a view into an unfinished shell. Doors are static architectural representations, not usable entrances yet.

## Images and changed scope

`Bakery01_Front.png`, `Bakery01_ThreeQuarter.png`, `Bakery01_Roof.png`, `Bakery01_VillageContext.png` and `Bakery01_CustomerApproach.png` use the existing unchanged scene lighting with editing gizmos absent. Camera conditions are in `Bakery01_CaptureConditions.json`.

Only the hamlet scene plus new Bakery01 source/paint/Unity/review files changed; see `ChangedFiles.json`. A03, the approved cottage, Crooked Mortar, imported package and production scenes remain intact. Unity is left in Edit mode with the saved Briarwick scene open and bakery selected. No commit or push. Stop for visual review.
