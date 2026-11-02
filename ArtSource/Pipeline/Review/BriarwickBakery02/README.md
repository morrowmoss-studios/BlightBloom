# Briarwick Bakery02 — architectural correction review

Status: new separate candidate, awaiting visual approval. Bakery01 has NOT been treated as approved. No commit or push.

## Latest update — applied gable timber removed

Removed four disconnected timber pieces: one central vertical at each gable and the two front diagonal pieces. No rear diagonals existed. Structural sloping verges, horizontal plates, roof tiles, plaster, entrances and internal oven/chimney are unchanged. Previous timber is preserved in a hidden, non-exported Blender reference collection. The existing prefab updates through its unchanged timber FBX reference; the scene file itself did not require editing.

Current total **32,046 triangles**. Imported UVs/normals and matching timber collider checked; both ends visually inspected. No new Console errors/warnings. All other source meshes and all protected existing files match the pre-cleanup baseline, except the intentionally updated Bakery02 Blender source, timber FBX and model catalog. No movement regression was rerun: removal is entirely above the entrance clearances and floor/navigation geometry is byte-identical. Latest images: `GableCleanup_Front.png` and `GableCleanup_Rear.png`; earlier comparisons below show the pre-cleanup candidate. Proof: `GableCleanupGeometry.json`, `GableCleanupUnity.json`, `GableCleanupPreservation.json`. No commits or pushes.

## Changes

- Repositioned and turned the source-derived oven chamber into the building. The former rear-wall fireplace opening is now continuous plaster construction. The chamber/firebox no longer projects outside as a barbecue; only the masonry chimney emerges through the roof. Simplified internal oven geometry is sufficient for this exterior pass; it is not a finished bread-oven interior or functional baking system.
- Replaced the shallow hipped roof with a pitched gable, ridge offset 0.35 m toward one side, approximately 5.74 m high including capping. Kept the wall/eave levels, body dimensions, customer/service openings and existing placement. Retained fitted verge boards; the later gable cleanup removed the applied king posts and diagonal pieces. No replacement ornament.
- Reworked clay tile coverage with more legible curved tile noses, controlled 45 mm course irregularity, small width/height differences and restrained existing painted clay swatches. Removed hidden tile bottoms, and use the roof deck for collision instead of detailed tile colliders.
- Rebuilt continuous plaster wall surfaces with proper window/door reveals, eliminating Bakery01's beveled rectangular panel seams. Four broad soft plaster atlas regions replace the repeated cropped blemishes. Original pale weathered timber, stone, door, window and hardware treatment is retained. No harsh contrast/noise treatment or approved-building repaint.
- A final preservation check caught Unity normalizing three render-state fields on the reused Bakery01 glass material. Restored the exact original SHA-256 and isolated Bakery02 glazing in its own derivative. No Bakery01 file change remains.

## Placement, footprint and counts

Scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
Root: `Bakery - architectural review02` / `BW_Bakery02`.
Prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Prefabs/BW_Bakery02.prefab`.

Position **(19, 5.84169626, -10)**, yaw **270°**, scale 1, unchanged from Bakery01. Existing road approach `Path_Bakery` unchanged. Bakery01 remains complete in inactive `Bakery - architectural review01`; the original placeholder remains inactive. Toggle review roots exclusively for comparison.

- Nominal wall-centre footprint **6.6 × 7.4 m**; complete geometry extent **7.44 × 8.20 m**, including roof overhangs.
- Chimney height above placement datum **6.469 m**, unchanged. Foundation bottom -0.28 m; full mesh bound height 6.749 m.
- **32,046 triangles**, versus Bakery01 **91,001** (58,955 fewer, approximately 65% reduction). **10 renderers, 10 used shared materials, 9 mesh colliders**. Detailed tile covering is visual only; the roof deck retains overhead collision. No LOD chain/performance benchmark in this pass.
- Customer frame opening **1.40 × 2.40 m**, service **1.30 × 2.30 m**. Existing 2 m tall, radius 0.4 m controller unchanged. Both static closed leaves, their placement, glazing, foundation, thresholds and marker intent are retained; no new entrance interaction or complete interior is provided.

## Editable source and dependencies

- Blender: `ArtSource/Blender/Architecture/Briarwick/Bakery02/BW_Bakery02.blend`, with packed working color textures and editable mesh groups.
- `reconstruct_bakery.py` reads Bakery01 and established read-only stable/native UV helpers, exports only changed body/roof groups. It refuses an existing Bakery02 source.
- `refine_tiles_and_joinery.py` performs the inspected local tile-lap and gable joinery adjustment. Apply once after initial reconstruction, not as a general regeneration tool.
- `finish_winding.py` finalizes reflected oven/roof outward normals. It protects oven winding against repeated reversal.
- `ModelCatalog.json` records reused Bakery01 FBXs and new Bakery02 exports/counts. New exports reside in `Assets/BlightBloom/Art/Architecture/Briarwick/Bakery02/Models/`.
- Painting: `ArtSource/Paint/Architecture/Briarwick/Bakery02/Plaster_PaintedAtlas02.png`, editable wash-layout guide `Plaster_Washes02.svg` and reproducible `prepare_plaster.py`. The SVG describes wash shapes; the source-region image and Python recipe provide the complete raster treatment. No AI-generated artwork or external service was needed for this correction.
- New plaster/glazing materials are project-owned. Other unchanged materials and models intentionally reference Bakery01 and installed `Assets/Medieval_house_lite/` texture dependencies, without editing them. Source UV catalog and stable helper remain read-only pipeline dependencies. `Dependencies.json` is the exact Unity dependency list. Existing URP/Autodesk Interactive shaders, no new packages or scripts in gameplay.

## Targeted validation

- Existing scene components outside the new review root match the **321-object** pre-task snapshot; original Bakery01 active-state change is intentional. Hash verification covers **2,436 existing files**: only the hamlet scene differs. Approved cottage, Stable A03, Crooked Mortar, Bakery01, imported package and production scenes remain unchanged.
- Imported geometry: finite UVs, UV/normal arrays complete, normalized normals, no zero-area triangles, supported materials and no missing texture references. No missing scripts.
- Frame ray clearances measured as above, excluding static leaves. These are architectural opening clearances, not a claim the closed doors are interactive.
- Oven containment: all **1,050 lower-chamber vertices** lie within the wall envelope. Lower chamber bounds x=0.322–2.174 m, z=-1.400–0.055 m; the original exterior firebox projection is gone.
- Roof coverage: **30/30** roof-deck samples hit upward-facing surfaces; **24/24** chimney-margin samples hit roof/masonry coverage. Flue centre is intentionally excluded. The tile/deck penetration is trimmed within the masonry shaft footprint; overlapping seating is intentional. Visual inspection of the rear/roof view shows no gross roof holes or exposed outdoor chamber.
- Nine foundation ground samples retain contact within approximately 1 mm of datum; terrain was not modified.
- Play mode: **16/16 existing CharacterController.Move route cases passed**, grounded, through customer/service approach lanes, road connection and perimeter in both directions. Temporary motor/orbit pause and player position were restored. This is automated collision testing, not keyboard-driven manual camera review or entry into an absent interior.
- No new Console warnings/errors after baseline cursor 44; current errors/warnings zero, compilationFailed false. No shared systems or unrelated scenes changed. No unrelated full-project validation.

## Visual assessment and limitations

The simple gable produces a clearer rural building silhouette than Bakery01's bungalow-like hip. Integrated chimney placement removes the external fireplace reading. Continuous plaster is quieter and less repetitive; revised tile laps read as individual clay pieces rather than continuous corrugation. The result remains modest beside Crooked Mortar.

This remains an architectural candidate, not final illustrative art. Tiles retain an orderly underlying grid, plaster is deliberately simple and lacks unique final wear painting, and glazing is dark/opaque to conceal the absent interior. Internal oven construction is simplified, without a finished refractory vault/flue engineering study. There are no functional doors, baking features, NPCs or furnishings. Final artistic approval is pending; technical checks do not establish it.

## Matched comparisons

`Comparison_Front.png`, `Comparison_Side.png`, `Comparison_ThreeQuarter.png`, `Comparison_VillageContext.png` show Bakery01/Bakery02 from identical cameras and unchanged scene lighting. Original individual renders are also retained. `Bakery02_RoofChimney.png` shows the new roof penetration and closed rear elevation. Camera records: `Bakery02_CaptureConditions.json`.

Full changed-file inventory: `ChangedFiles.json`. Unity is left in Edit mode with the saved Briarwick scene open and Bakery02 selected. Stop here for visual approval.
