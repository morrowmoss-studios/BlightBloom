# Shop Workflow12 — crafted room review

Open `Assets/Scenes/CM_CrookedMortar_ShopWorkflow12_Review.unity`. This is a separate derivative of EntranceWorkflow11, retaining its fitted arch and the Workflow09 counter. Production02 and all previous workflow scenes/assets remain protected. No commits or pushes.

## What changed

- Two new reusable cabinet prefabs replace only the medicine and records cabinet renderers. Shouldered end standards, stepped feet, swept crowns, coved bearing edges, segmental shelf aprons, housed shelf supports and recessed sage drawer fields give the furniture a more authored silhouette. Existing stock, records and shelf heights are retained; no loose props were added.
- A fitted paneling module creates a restrained sage/walnut window apron and low wall lining under the records case. It stays within 65mm of existing walls and below openings.
- A fitted joinery module supplies deeper window shoulders/sill, wall plates and curved bearing braces under the existing tie beam. Brace lower edges stay above player head clearance. Existing room boundaries and openings remain unchanged.
- Dedicated painted limewash uses broader pigment groups on the shop's existing interior plaster meshes. The generated source is `PaintedLimewash.png`; prompt/provenance in Prompts.md. Stone and walnut textures are reused unchanged. The new sage material reuses walnut grain with a restrained green tint.
- One existing shop fill is repositioned from (1.55,2.78,1.15) to (1.85,2.55,.55), intensity 1.15 to 1.65, colour (1,.88,.73) to (1,.86,.66); range remains4.6. No lights, bloom, fog or exposure changes were added. This supports a warmer entrance/display emphasis, not a replacement for modeled construction.
- Cabinet feet were corrected to the actual y=.203 visual floor plane during final fitting. No collider or station-marker changes.

## Editable assets and pipeline

`CM_ShopWorkflow12.blend` retains 73 separate editable components plus four joined export meshes. Source scripts reuse the established Workflow08 profile/bevel/UV helpers and Workflow10 cabinet shelf datums and exporters. `build_shop12.py` records initial creation; `SeatCabinetFeet.py` is a one-time final adjustment, not an idempotent repeated utility. Prior Blender sources are read-only.

Four FBX/prefab modules under `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow12/`:

| Module | Triangles |
| --- | ---: |
| MedicineCabinet | 13,324 |
| RecordsCabinet | 5,384 |
| FittedPaneling | 3,968 |
| FittedJoinery | 2,756 |
| Total new modules | 25,432 |

Two former cabinet renderers (13,680 triangles combined) are disabled in this review. Net added geometry is 11,752 triangles. Four new renderers replace two; shared materials and joined meshes avoid individual timber/panel GameObjects. No LOD/GPU profiling was performed. The existing high-detail counter is reused and remains a larger optimization opportunity.

## Comparisons and artistic assessment

`Previews/Comparison/EntranceWide.jpg`, `CounterGameplay.jpg`, `CabinetClose.jpg` and `RoomClay.jpg` show baseline left / candidate right from exact matched camera transforms/FOV. Both versions use the same open-door pose. Colour comparisons include the documented local fill adjustment; clay uses identical original lighting and neutralizes shop geometry. These are actual Unity Play-mode Game-view captures; no AI paint-over of screenshots. The generated bitmap is used as a real material map.

The room is closer to the supplied reference: the cabinet crown and niche rhythm read from player distance, the paneling connects furniture to the window wall, curved braces give the entrance framing more character, and the wall pigment/light hierarchy is warmer. It remains an incremental room improvement rather than a match to the reference's richness. Flat glazing, the empty exterior backdrop, simple existing stock/character forms, repeated wood grain and the still-regular overall architecture limit the illusion. The current herb arrangements are retained, not expanded. The counter was already the strongest constructed element and was preserved rather than decorated again. No claim of final artistic approval is made.

## Validation and limits

- SourceValidation.json: finite UVs/normals/geometry; one UV layer per mesh; no degenerate triangles. Source count includes hidden editable copies. Metric scale and established FBX axis conversion maintained.
- IntegrationValidation.json: imported channels/material references complete; no missing scripts/materials; all116 existing colliders unchanged; no added permanent colliders;43 full outward door-swing poses clear.
- ClearanceValidation.json:190 static capsule samples pass entry/customer/staff/stair connection/kitchen connection routes with unchanged2m height/.4m radius.
- RoomRouteValidation.json: **live input-path smoke test passed**. Temporary Input System keyboard E opened the existing door fully; temporary gamepad events drove normal TraversalInput/ThirdPersonMotor updates through11 waypoints: exterior threshold and return, customer/staff counter approaches, records approach and kitchen doorway/return. No direct route CharacterController.Move calls or route teleports; existing orbit camera stayed enabled. Temporary input devices removed. This is automated live gameplay input, not manual comfort acceptance. Full upstairs/stair/exterior regression was outside the localized scope and was not repeated.
- Final foot correction only seats existing cabinet feet downward37mm against the floor at the same footprint; navigation geometry/colliders are unchanged.
- SavedScopeValidation.json confirms no original script, camera or collider record changes. Expected scene changes are the new prefab instances, two disabled cabinet renderers, two interior plaster material overrides and one local fill transform/light.
- Protected file hashes checked. Unity auto-synchronized the legacy `_MainTex`/`_Color` aliases in an old stone material during import; those incidental changes are restored to the verified pre-task version.
- No compilation failures or observed gameplay exceptions. One read-only Pipeline inspection timed out; subsequent small queries and validation succeeded. Retained Editor warnings are distinguished from new import/gameplay defects in the report.

Review scene is left saved and stopped for manual review. Core player, movement, camera, doors, layout, architecture collisions and Production02 are unchanged.
