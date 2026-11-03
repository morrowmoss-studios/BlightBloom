# Briarwick Family Cottage B01 — rough architectural review

2026-11-03. Saved in EXISTING `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, location11. Original `11 Family cottage B PLACEHOLDER` retained disabled. Placement(25,6.037371,43), yaw210°, unit scale unchanged. No new Unity scene. Cottage selected in saved Edit mode for review.

## Architectural draft

Single-story rural home with an offset transverse ridge, a long rear catslide, unequal roof pitches and small asymmetrically sized windows. The front overhang is structurally supported over a stone entry stoop instead of carrying an extra ornamental porch roof. Modest rear service entrance and integrated hearth chimney. No dormer, decorative truss pattern, wing copied from another cottage, clutter or luxurious treatment.

- **Footprint6.8 ×7.2m =48.96m²**; roof envelope approximately7.6 ×8.7m including sheltered front cover.
- **Height5.965m including chimney** above placement datum; ridge cap around5.79m. Planned floor+0.12m.
- Main clear doorway **1.4 ×2.4m**, rear service **1.3 ×2.2m**. Static leaves; no door interactions or playable interior. Dimensions measured between framing with closed leaf colliders excluded.
- Minimum sampled covered-entry headroom **2.4m** above planned floor datum.
- **15,900 triangles**, **11 mesh renderers**, **10 shared materials**, static mesh colliders. No LODs or final optimization pass.

## Sources and dependencies

Editable packed `ArtSource/Blender/Architecture/Briarwick/FamilyCottageB01/BW_FamilyCottageB01.blend`, eleven grouped FBX models, project-owned material derivatives and reusable `Assets/BlightBloom/Art/Architecture/Briarwick/FamilyCottageB01/Prefabs/BW_FamilyCottageB01.prefab`.

Reuses original cottage/package weathered wood, stone, doors, metal, firewood and roof-underdeck maps; existing muted plaster/small-window material sources and Inn01’s eight-cell painted shingle atlas. No new texture regeneration, asset installation or original package changes. Exact Unity dependencies in `GeometryValidation.json`.

## Targeted validation

- **16/16 grounded automated Play-mode CharacterController.Move checks passed**: three main-entry lanes, three rear-entry lanes, original road connection and full perimeter, forward/reverse. Existing controller2m high/.4m radius. Motor/orbit temporarily paused/restored and player transform restored. Collision smoke checks only, not manual keyboard or camera-comfort approval.
- **30/30 roof-deck samples passed**, correct upward-facing normals; covered-entry clearance>=2.4m. Roof/chimney, side-gable closure, entry support and rear threshold inspected visually.
- Eleven meshes: finite UVs, valid normals, zero degenerate triangles; supported materials with no missing texture references. Front/rear doorway dimensions verified.
- Terrain samples under foundation within1mm of original datum. Original road/path, terrain, bridge, creek, buildings and landmarks unchanged.
- **461 pre-existing scene objects’ component snapshots unchanged** outside new root; original placeholder intentionally disabled. **2,869 baseline file hashes checked**, only authorized Briarwick scene changed.
- Unity Console final**0 errors/0 warnings**, compilation not failed. Historical captured cursor44 unchanged; no Console clearing.

## Remaining refinement

Rough candidate, not final art approval. Roof courses retain atlas repetition; eave/verge edge treatment is simple and can show small shingle lips. Side plaster gables are intentionally plain; glazing remains dark. Fine joinery, local chimney flashing, more restrained material variation and future collider/LOD tuning belong to a separately approved pass. No furnishing, landscaping, NPCs, interior, dialogue or other gameplay implemented. No village-wide polish started.

## Review

`FamilyCottageB01_Front.png`, `FamilyCottageB01_ThreeQuarter.png`, `FamilyCottageB01_Side.png`, `FamilyCottageB01_Rear.png`, `FamilyCottageB01_VillageContext.png`. Clean existing-scene lighting/camera renders without gizmos; camera restored after capture. Context includes unchanged ElderCottage01.

Exact file inventory: `ChangedFiles.json`. No commit or push. Stop for manual visual approval.
