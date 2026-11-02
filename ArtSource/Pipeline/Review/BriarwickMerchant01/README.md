# Briarwick General Merchant01 — architectural review

Built 2026-11-02 in the existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Only location05 was replaced. Its original greybox remains disabled at its original transform; roads and terrain were not edited. Candidate selected in the running Editor, Edit mode, scene saved.

## Building

A small enclosed storehouse volume with a steep hipped thatch roof, offset customer door, timber-framed street counter and shallow supported board canopy. Rear double delivery doors and small windows/louver provide practical service elevations. Empty timber sign bracket only; no invented signage, merchandise clutter, interior gameplay or trading system.

- Enclosed footprint: **6.8 × 6.4 m (43.52 m²)**. Roof/awning envelope approximately **7.52 m wide × 8.14 m deep**.
- Roof peak: **6.658 m above placement datum**, approximately **6.51 m above planned shop floor**. Foundation extends 0.13 m below datum.
- Customer opening: **1.40 × 2.40 m**. Delivery opening: **1.60 × 2.40 m**.
- Both entrances have static closed leaves; no new door interaction or playable interior. Doorway dimensions exclude frames, while walk tests stop outside the leaves.
- Counter: **2.40 m wide × 0.65 m deep**, top **1.00 m above shop floor / 1.03 m above customer apron**. Selling hatch: **2.30 × 1.25 m**.
- Minimum sampled canopy clearance above apron: **2.41 m**.
- **21,336 triangles**, **14 mesh renderers**, **9 shared materials**. Static mesh colliders; no dynamic/gameplay components. No LODs yet.

## Sources and dependencies

Editable `ArtSource/Blender/Architecture/Briarwick/Merchant01/BW_Merchant01.blend`; fourteen grouped FBX exports and reusable `Assets/BlightBloom/Art/Architecture/Briarwick/Merchant01/Prefabs/BW_Merchant01.prefab`.

Project-owned materials reuse the cottage package's original weathered wood/stone/door atlases, Bakery02 plaster and StableA03 thatch textures. All source/package assets remain unchanged. No new package dependency. Exact transitive Unity dependencies are recorded in `FinalIntegration.json`.

## Validation completed

- Inspected final front, three-quarter, side, rear, counter and village-context captures. Corrected initial ground exposure underneath the serving recess by extending its local lining to floor level and closing its floor/ceiling. Changed only that lining to matte wood.
- All fourteen meshes: finite UVs and valid normals; zero degenerate triangles. Supported shaders, no missing texture references.
- Static roof coverage: 25/25 rays, correct upward-facing surfaces. Customer paving: 20/20 samples. Canopy: 12/12 overhead samples. Measured door frames and counter.
- Existing 2 m-high, 0.4 m-radius CharacterController: **24/24 automated Play-mode cases passed grounded**, forward/reverse customer lanes, counter lanes/turn, rear delivery lanes, road approach and perimeter. Tests use CharacterController.Move, temporarily pause motor/orbit and restore all state. They are collision smoke checks, not manual keyboard, sprint-animation or camera-comfort approval.
- No new warnings/errors; current Unity Console 0 errors/0 warnings, compilation not failed. Historical captured warning cursor remained44.
- **2,592 baseline file hashes checked**: only the authorized Briarwick scene changed. **377 existing scene objects' component snapshots unchanged** outside the new merchant root. Original placeholder intentionally disabled. No existing approved building, package, production scene, terrain, road, controller or camera asset changed.

## Remaining limitations / visual review

This is a rough architectural candidate, not final approved art. The steep hipped roof gives a distinct silhouette but dominates the small shop; its simple pyramidal form needs manual artistic review. The continuous thatch coat reads combed and its eave grain is regular at close range. The board canopy is repetitive, and the small windows remain dark. No claim of final craftsmanship or photoreal detail. Storage is represented by enclosed exterior volume with a locally closed serving recess, not a completed interior. No NPC, stock, sign graphic, trading or opening-door behavior added. Manual camera comfort and gameplay interactions were not tested because no such systems changed.

## Captures

`Merchant01_Front.png`, `Merchant01_ThreeQuarter.png`, `Merchant01_Side.png`, `Merchant01_Rear.png`, `Merchant01_CounterAwning.png`, `Merchant01_VillageContext.png`. Existing lighting, no editing gizmos; temporary review camera restored after capture.

Changed-file inventory: `ChangedFiles.json`. No commit or push. Stop for visual review before extending construction.
