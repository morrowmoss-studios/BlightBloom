# Briarwick Inn & Tavern01 — architectural review

2026-11-02. Status: first exterior candidate, awaiting visual approval. No new scene; no commit or push.

## Building and site

Scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
Prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Prefabs/BW_Inn01.prefab`.
Root: `Inn - architectural review01` / `BW_Inn01`.

Position **(18, 5.941107, 16)**, yaw **238°**, scale 1 retains location02 and the original road-facing entrance line. `02 Inn and tavern PLACEHOLDER` remains complete and disabled. `Path_Inn`, terrain, roads, lights, landmarks and other locations were not moved or edited. No other scene was created or modified.

A two-storey main block is paired with a lower, recessed right wing. Unequal parallel gables, their fitted valley and the small entrance porch establish character through massing instead of applied timber ornament. The sign provision is a plain supported timber arm with an empty attachment marker; no lettering, signboard graphic or invented inn name.

The hearth/fireplace geometry is internal to the right wing, with only the masonry flue emerging through its roof. It is not a detached outdoor fireplace. No fire, smoke, tavern interactions, furniture, NPCs or complete interior were constructed.

## Dimensions and architectural allowance

- Main block **5.7 × 9.2 m**; recessed wing **3.8 × 8.1 m**; combined ground footprint **83.22 m²**, within a 9.5 × 9.2 m bounding rectangle with the front corner recessed. Ground-wall thickness approximately 0.22 m.
- Overall model extents including roof overhangs and porch: **10.273 × 11.185 m**.
- Roof height above placement datum **8.569 m**; chimney approximately **8.378 m**. Foundation bottom -0.30 m; full mesh-bound height 8.869 m.
- Nominal storey rise **3.10 m**. Main upper wall/eave zone about 6.0–6.17 m, lower wing 5.45–5.68 m before its rising roof. The main block gives roughly 52 m² gross per storey, and the wing adds about 31 m² gross at ground level. This permits a small public room/circulation, cooking/service accommodation and a few modest upstairs sleeping spaces in a future layout. This is an architectural allowance, not a validated room/stair plan.
- Main door frame clear opening **1.50 × 2.50 m**. Rear service opening **1.30 × 2.30 m**. Existing player **2.0 m high, radius 0.4 m**, unchanged.
- Main doorway has a shallow stone threshold and approximately 3.0 × 1.5 m porch standing surface. Ground sill beams are interrupted at both entrances rather than crossing their openings.
- Door leaves are **static and closed**. Tests cover approaches and standing clearances, not passage through closed leaves or an interior. There is no new interaction system.

## Geometry and materials

**31,272 triangles**, **14 renderers**, **9 used shared materials**, **13 static mesh colliders**. Individual shingles are visual geometry; the roof deck and small valley collider provide the collision envelope. No LOD chain or runtime performance benchmark was produced in this architectural pass.

Timber/stone/door derivatives preserve the approved cottage's pale weathered native package character. Inn plaster has a restrained warm greige adjustment to the existing project-owned soft plaster map. Glazing stays dim and opaque to conceal the unbuilt interior; no uniform emission or glossy-window treatment. No new lighting or contrast/sharpening pass was applied.

The roof uses individually modeled overlapping wooden shingles with small course variation and eight restrained grain swatches derived from clean regions of the original package roof painting. The native atlas's baked course shadows are not copied as broad repeating strips. Roof/deck spacing, fitted ridge covers, soffit UVs and frame reveals were corrected after close-up inspection. The subdued valley is a narrow practical weathering channel rather than applied ornament. Regularity of the underlying course layout remains visible up close.

## Editable source and dependencies

- Blender source: `ArtSource/Blender/Architecture/Briarwick/Inn01/BW_Inn01.blend`, editable mesh groups with packed working color images.
- Source recipe: `build_inn.py`, `finish_frames_and_deck.py`, `seat_roof_cover.py`, `clear_door_sills.py`, in that order. Initial builder refuses an existing candidate; local corrections guard against repeated application. Prefer editing the saved source for routine changes, without rebuilding completed village assets.
- FBX exports: `Assets/BlightBloom/Art/Architecture/Briarwick/Inn01/Models/`; metric conversion follows the established Blender -Z-forward/Y-up export and Unity +Z frontage convention. Imported mesh transforms are identity/scale1.
- Shingle painting: `ArtSource/Paint/Architecture/Briarwick/Inn01/Shingle_GrainAtlas01.png`, `prepare_shingles.py`, and exact normalized source crops in `SourceRegions.json`. Color map sRGB with mipmaps, nonmetallic, smoothness .06. No new generated concept artwork, paid service or package was used.
- Read-only source catalog: FamilyCottageA `Style01/SourceMeshReadOnly.json`; native UV/export helpers from StableA02OpenFront and wall/roof-clipping helpers from Bakery02. Installed `Assets/Medieval_house_lite/` supplies native texture/mesh source. Project-owned plaster painting from Bakery02 is reused unchanged. Material derivatives belong to Inn01; no existing material was edited.
- Standard project URP Lit and Autodesk Interactive shaders remain dependencies. `Dependencies.json` contains exact Unity asset paths; `ModelCatalog.json` records mesh-group counts and material order.
- Historical Bakery01 glass baseline bytes were captured as a safeguard against Unity's previously observed automatic render-state serialization. This task did not need to restore or alter it; all existing material hashes remain unchanged.

## Targeted validation

- Imported meshes: finite vertices/UVs, UV and normal arrays present, normalized normals, no zero-area geometry triangles. Supported shaders, material slot assignments and texture references checked. No missing scripts.
- Entrances measured by structural ray checks with static door leaves excluded: main **1.50 × 2.50 m**, service **1.30 × 2.30 m**. Doorframes and sill interruptions checked in the close entrance view.
- Roof deck: **45/45 coverage probes**, upward normals. Chimney margins **24/24** covered, valley **5/5**, porch standing surface **49/49**. Lower hearth geometry lies within the wing. Flue centre intentionally excluded from margin checks. Deck/covers overlap as intentional architectural seating, not a claim of complete watertight roof engineering.
- Terrain near the footprint is within approximately 4 mm of placement datum. Foundation/threshold placement required no terrain or road changes. One outer ground sample is beyond the recessed wing frontage and is a terrain-level reference only.
- Play mode: **18/18 existing CharacterController.Move cases passed**, grounded in both directions. Three main approach lanes, three service approach lanes, porch approach/turn, perimeter and recessed-wing frontage. Motor/orbit temporarily paused during the automated probe and then restored, along with the player transform. No movement speed, capsule, camera or input changes.
- This is automated collision/traversal testing, **not** keyboard-driven manual camera-comfort approval, and not an interior or door-interaction test.
- Existing scene component snapshots outside the new review root match the **356-object** baseline. Placeholder deactivation is intentional. **2,525 protected existing files** were hash-compared: only the intended Briarwick scene differs. All completed buildings, imported package, terrain/roads, production scenes and shared scripts/settings remain unchanged.
- Console: zero current errors/warnings, compilationFailed false; no newly captured warnings/errors after baseline cursor44. A missing Python helper import was corrected before its successful export; no gameplay scripts were added.
- No unrelated full-project regression, interior/stair validation, tavern gameplay, performance benchmark or final lighting pass.

Proof: `StaticValidation.json`, `Coverage.json`, `PlayValidation.json`, `FinalIntegration.json`, `PreservationValidation.json`, `ConsoleValidation.json`.

## Remaining limitations and artistic review

1. This is a restrained first architectural pass. Plaster is still broad/simple, roof courses retain an underlying regular grid, and fine edge aliasing/texture scale at oblique roof views needs later art/LOD review.
2. Windows are deliberately dark/opaque; no interior furnishing, stair or guest-room construction is hidden behind a claim of playability. The 3.1 m storey datum and future-stair marker are planning references only. Interior layout/camera comfort needs its own authorized milestone.
3. Main and service doors are static closed architectural leaves. Inn entry, scene transitions and interactions remain unimplemented.
4. The hearth is simplified hidden source-derived geometry; no fire/draft simulation or detailed flue engineering. Final historical construction accuracy and weatherproofing are not asserted.
5. No LODs or final batching/performance budget. Crooked Mortar remains visibly more ornate and materially rich; the new inn does not claim that landmark's finished artwork quality.

## Review screenshots

`Inn01_Front.png`, `Inn01_Entrance.png`, `Inn01_ThreeQuarter.png`, `Inn01_Side.png`, `Inn01_Rear.png`, `Inn01_RoofChimney.png`, `Inn01_VillageContext.png`. The context image includes Crooked Mortar for scale. Existing scene lighting/exposure is unchanged and editing gizmos are absent. Capture camera values are restored; see `Inn01_CaptureConditions.json`.

Changed scope: one existing scene plus new Inn01 source, grain derivative, exports, materials, prefab and review outputs. Exact inventory: `ChangedFiles.json`. The saved Briarwick scene is open in Edit mode with the inn selected. Stop for visual review before any next building. **No commit or push.**
