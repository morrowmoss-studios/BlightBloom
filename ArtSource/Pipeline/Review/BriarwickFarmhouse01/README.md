# Briarwick Farmhouse01 — rough architectural review

2026-11-02. Integrated into the EXISTING `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, location07. Original `07 Farmhouse and stable PLACEHOLDER` disabled, not deleted. Saved in Edit mode; `BW_Farmhouse01` selected for review.

## Form and scale

Modest broad farmhouse with a loft, continuous gabled thatch coat, muted plaster and pale weathered timber, local stone plinth, integrated hearth chimney, small covered front stoop and rear service entrance. No clutter or ornamental trusses; deliberately simpler than the inn and Crooked Mortar. Roof pitch approximately37 degrees, no regular individual tile strips. Lower-normal-strength project-owned thatch derivative preserves the StableA03 palette.

- Main footprint **9.0 × 7.2 m = 64.8 m²**; roof about9.76 ×8.29m and porch extends to localz5.13m.
- Highest chimney point **6.777 m above placement datum**; roof ridge about6.27m. Planned floor +0.12m above placement datum.
- Main clear opening **1.40 × 2.40 m**, rear service **1.30 × 2.30 m**. Static closed leaves, no interactive doors or playable interior.
- Sampled porch headroom minimum **2.50 m**.
- **22,588 triangles**, **12 mesh renderers**, **9 shared materials**; static mesh colliders. No LODs yet.
- Original placeholder position (47,5.669026,-30), yaw255°, unit scale; no terrain adjustment. Farmhouse remains separate from StableA03.

## Deliverables and dependencies

Editable source `ArtSource/Blender/Architecture/Briarwick/Farmhouse01/BW_Farmhouse01.blend` with packed source color images. Twelve FBX groups, project-owned materials and reusable `Assets/BlightBloom/Art/Architecture/Briarwick/Farmhouse01/Prefabs/BW_Farmhouse01.prefab`.

Uses read-only original cottage/package timber, stone, door, hardware, firewood and glass maps, existing Bakery02 plaster map and StableA03 thatch maps. No imported package asset or approved building edits. Exact Unity dependencies listed in `FinalIntegration.json`.

## Validation

- **18/18 grounded Play-mode CharacterController.Move tests passed**, forward/reverse main-door approach lanes, rear service lanes, road connection, front frontage and full perimeter. Existing controller2mhigh/.4mradius; motor/camera paused temporarily and restored, player transform restored. This is automated collision validation, not manual keyboard or camera-comfort approval.
- All12 meshes finite UVs and valid normals, zero degenerate triangles; supported materials and no missing texture references.
- Structural opening ray measurements match sizes above, with static door leaves excluded. No passage through closed doors claimed.
- 25/25 roof coverage rays hit with upward-facing normals; 12/12 porch overhead samples, >=2.50m headroom. Foundation contacts sampled against unchanged terrain.
- Initial gable board tips penetrated the roof and joints exposed sky. Corrected only the new farmhouse by trimming tips beneath the thatch and adding recessed backing. Final front/side/rear/three-quarter/context views inspected.
- Current Console **0 errors/0 warnings**, compilation not failed. Pipeline generated an automation API/thread-abort error during Play-mode reload; restored the existing connection via UI and completed the tests. No new asset/gameplay warnings/errors observed. No Console clearing performed.
- **399 pre-existing scene component snapshots unchanged**, excluding the new farmhouse root; original placeholder intentionally disabled. **2,649 baseline file hashes checked**, only authorized Briarwick scene changed. Roads, creek, bridge, terrain, stable, completed buildings, gameplay and production scenes unchanged.

## Future refinement

Rough-build candidate, not final art. Thatch remains a simple textured continuous coat with a regular end-grain eave band, and the porch boards/gable cladding remain repetitive. Small glazing reads dark and loft glazing uses a closed backing; interior views are not supported. Chimney junction is visually intersected cleanly but does not yet have bespoke flashing. Fine joinery, richer restrained material variation, roof dressing/UV refinement and LOD/collider optimization belong to a future approved pass. No interior, NPC, farming, dialogue or door systems added.

## Review images

`Farmhouse01_Front.png`, `Farmhouse01_ThreeQuarter.png`, `Farmhouse01_Side.png`, `Farmhouse01_Rear.png`, `Farmhouse01_VillageContext.png`. Clean existing-scene lighting/camera renders with no editing gizmos. Neighboring buildings retained; farmhouse roof/stoop framing unobstructed in final individual views. Context shows the relationship with StableA03 and farm plots.

`ChangedFiles.json` lists this task's modified/additional files. Merchant01 files were already untracked before this task and remain untouched. No new scene, commit or push. Stop for manual visual approval.
