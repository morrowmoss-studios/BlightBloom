# Briarwick Blacksmith & Forge01 — architectural review

Status: first architectural candidate, awaiting visual approval. No new Unity scene, no commits or pushes.

## Design and integration

Existing scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
Prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/Prefabs/BW_Blacksmith01.prefab`.
Scene root: `Blacksmith - architectural review01` / `BW_Blacksmith01`.

Position **(-26, 5.499537, -25)**, yaw **70°**, scale 1 matches the designated placeholder. `03 Blacksmith and forge PLACEHOLDER` remains intact and disabled. `Path_Forge`, terrain, lights, landmarks and other building placements are unchanged. No new scene was created.

The building combines an enclosed rear workshop with an open front work apron under one clay-tiled roof. Its ridge runs across the frontage, giving a long working shelter rather than the bakery's front gable or the cottage's tall dormer composition. Boarded side loft ends and plain perimeter framing remain quiet. Short knee braces support the front bearing beam; no applied ornamental gable pattern was added.

A raised charcoal hearth, thick tapering masonry smoke canopy and continuous stone flue are built into a noncombustible breast replacing part of the workshop wall. This is a covered forge work position, not a detached outdoor fireplace. The hood is open below and overlaps the flue throat; the chimney passes through a fitted roof penetration. No fire particles, dynamic lights, smithing systems or interior dressing were added.

The 2.5 m workshop opening is unobstructed, without a door leaf. A smaller side doorway has a static leaf folded clear against the inner wall. These are architectural access provisions, without interaction scripts. Anvil, quenching trough, horseshoeing and forge work positions have empty named marker transforms for later use; no extra props were placed to fill those areas.

## Dimensions and cost

- Body/covered-floor footprint: **9.2 × 7.4 m**, close to the original 10 × 8 m site.
- Enclosed workshop: **9.2 × 4.2 m**; covered front apron **9.2 × 3.2 m** (nominal wall/post centre lines).
- Complete geometry bounds including overhangs: **10.355 × 8.573 m**.
- Main roof ridge approximately **5.80 m**; chimney **6.586 m** above placement datum. Foundation bottom -0.28 m; complete mesh bound height 6.866 m.
- Wide workshop clear opening **2.50 × 2.65 m**. Side service clear opening **1.30 × 2.30 m**. Existing player is 2 m high, radius 0.4 m, unchanged.
- Front support shifted to local x=-0.8 m so the original approach centre remains clear; outer supports remain at x=±4.6 m. Practical bearing posts and knee braces retain roof support.
- **33,950 triangles**, **12 renderers**, **10 shared materials**, **10 colliders**. Detailed roof/charcoal geometry is visual only; roof deck handles overhead collision. One continuous BoxCollider handles the paving surface, avoiding triangle-edge raycast seams between visual paving modules. No final LOD chain or performance benchmark yet.

## Materials, editable source and dependencies

- Editable Blender: `ArtSource/Blender/Architecture/Briarwick/Blacksmith01/BW_Blacksmith01.blend`, with editable mesh groups, metric units and packed working color images.
- New FBX group exports and prefab/material derivatives: `Assets/BlightBloom/Art/Architecture/Briarwick/Blacksmith01/`.
- Source/export recipe: `build_smithy.py`, then `finalize_local.py`, `clear_road_approach.py`, and `repair_flue.py`. The initial builder refuses an existing candidate. Use saved source for ordinary edits, rather than regenerating approved buildings.
- Read-only native mesh/UV catalog: `ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json`; helper definitions from StableA02OpenFront and Bakery02. No existing builder outputs were regenerated.
- Timber, stone, hardware and door derivatives use the approved cottage's restored native package treatment. Project-owned clay and plaster paintings are reused from Bakery01/02 without editing their sources or materials. Clay has a restrained grey-earth tint; plaster stays soft and low contrast. Glazing is a separate smithy copy. Charcoal is a matte, nonemissive URP material.
- Native assets/textures derive from installed `Assets/Medieval_house_lite/`; standard project URP Lit and Autodesk Interactive shaders are required. No package import or installation. These dependencies remain necessary even though the new mesh exports/prefab are project-owned. `Dependencies.json` contains the exact Unity paths; `ModelCatalog.json` records group counts/material order.
- Source-specific long chimney triangles were clipped at the hood throat with UV interpolation. An initial whole-face filter omitted the shaft; the defect was caught in the first render and repaired before acceptance checks.

## Targeted validation

- Imported vertices/UVs finite, complete UV/normal arrays, normalized normals, zero degenerate triangles, supported materials and no missing texture references/scripts.
- Measured frame clearances as above. The side leaf is fixed open and main opening has no leaf; neither requires an interaction system for this review.
- **396/396 floor probes**, **30/30 roof-deck probes** with upward normals, **22/22 chimney-margin coverage probes** passed. The flue centre is intentionally excluded; tile laps are overlapping visual surfaces, not a claim of watertight roof engineering.
- Nine foundation samples are within approximately 0.3 mm of the existing terrain datum; no terrain edits or placement changes were required.
- Horseshoeing envelope **1.2 × 2.6 × 2.8 m**: **51/51 sampled positions clear** along the left-front approach. This is geometric clearance, not a horse controller/animation test.
- Play mode: **22/22 existing CharacterController.Move route cases passed**, grounded, in both directions. Covered three wide-entry lanes, three side-entry lanes, original road centre/apron, workshop-floor circulation, forge approach, future-station aisle and perimeter. The final test ran after continuous-floor collision was installed. Temporary motor/orbit pauses and player position were restored. This is automated collision/traversal validation, not keyboard-driven manual camera-comfort approval.
- Current Console: zero errors, zero warnings, compilationFailed false; no new captured warnings/errors since baseline cursor 44. An Editor-only floor-collider utility null check was corrected before its successful final run; no gameplay code was introduced.
- Existing scene component snapshots outside the new review root match the **336-object** baseline. Placeholder deactivation is intentional. Protected-file hashes cover **2,469 existing files**, with only the intended hamlet scene differing. A Unity automatic render-state normalization of the historical Bakery01 glass material was restored to its exact baseline hash; no existing material edit remains. Bakery02, Stable A03, cottage, Crooked Mortar, original package, terrain/roads and production scenes remain unchanged.
- No unrelated full-project regression, functional smithing test, NPC/horse simulation, final lighting pass or complete interior production was performed.

Proof: `StaticValidation.json`, `Coverage.json`, `PlayValidation.json`, `FinalIntegration.json`, `PreservationValidation.json`, `ConsoleValidation.json`.

## Remaining issues / artistic review

- First architectural pass only: clay tiles still have an orderly underlying grid, masonry/hood UV scale needs a later dedicated paint/fit pass, and the retained native plank texture is relatively repetitive up close. No final cinematic/environment-art quality is claimed.
- Forge hood/flue are simplified architectural geometry, without simulated draft, bellows, fire, refractory construction or hot-metal equipment. There is no working smithing gameplay.
- Workshop is an accessible empty shell with a floor; tools, anvil, trough and interiors are intentionally pending. Marker locations reserve space but do not establish final animation/NPC clearances.
- No roof LOD or village-wide performance budget was validated. Manual visual/camera review remains pending.

## Screenshots

`Blacksmith01_Front.png`, `Blacksmith01_Side.png`, `Blacksmith01_ThreeQuarter.png`, `Blacksmith01_VillageContext.png`, plus `Blacksmith01_ForgeBay.png`. Captured with the existing unchanged scene lighting, without editing gizmos; camera values are restored. Conditions: `Blacksmith01_CaptureConditions.json`.

Full changed-file scope: `ChangedFiles.json`. The saved Briarwick scene is open in Edit mode with the blacksmith selected. Stop here for visual approval. No commit or push.
