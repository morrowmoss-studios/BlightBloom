# The Crooked Mortar — Production01 integration candidate

Scene: `Assets/Scenes/CM_CrookedMortar_Production01.unity`.
Benchmark: `CM_CrookedMortar_B_StyledDetails07`, preserved unchanged.
This is the first playable integrated candidate, not a final furnished interior or a release-ready environment.

## Installed production assets

- EntryPortal02: unchanged approved portal at (.85, .20, -5.52), yaw180. Uses the previously cleaned canopy-support mesh; redundant original right upright/knee and crossing header are omitted. A small bearing supports the retained shop-side beam. Sign, lanterns and hanging botanicals retain their approved composition.
- SlateRoofKit01: unchanged approved fitted roof assembly, including the approved character pass. Original-shaped roof carriers retain the dormer shell and collision. New kit underlays remain disabled, preventing two rendered backing layers. No roof silhouette redesign.
- PairedWindowBay02: unchanged insert at (-.46,3.44,-4.20), yaw180; optional original card dressing disabled in favour of BotanicalPlanterKit01. The fitted host has two .84 x1.69m rough apertures instead of the old .76 x1.60m display holes. No overlapping full4.5m host wall on the approved4.65m elevation.
- FacadeBay01: installed shared posts, horizontal beams and diagonal braces. Timber member lengths fit approved spans; only member length axes are scaled, not complete finished wall bays. Custom fitted plaster/return/gable panels retain the approved occupied envelope rather than forcing standard3m bays onto it. The east window has true arched corner infills matching its approved scaled WindowBay01 insert. The angled wing front is retained.
- BotanicalPlanterKit01: the41 approved integration placements, shared alpha-clipped matte materials and existing LODs. No botanical colliders. Approved WindowBay01 side/study inserts, open door, foundation stones, chimney joints, signage, lanterns, path, beds and garden fence are reused.

The fixed site meshes are combined by shared material in a new reusable prefab. Existing art assets are referenced, not edited. Source prefab geometry is not deleted. Empty containers left by batching were removed only from this new scene.

## Interior and circulation

Finished ground floor .20m; upper floor3.44m; floor rise3.24m. The approved18-riser stair is preserved (riser.18m,tread.28m,width1.25m).

Ground: public shop/display projection; treatment room behind the stair screen; preparation bench in the side wing; enclosed rear storage on the garden-exit route. The new storage divider has an aligned1.45m doorway. Upper: bedroom in the left hero volume, living quarters to its right, rear landing and medical study in the wing. The bedroom divider moves.21m to the paired-window central post instead of cutting into a casement.

Eight simple Blender-built furniture fixtures identify the room functions. They are provisional functional furnishings, not a new finished interior-art family. Their matching box colliders keep routes honest. The shop counter sits beneath the front display, clear of the open door; the narrow study shelf is placed against the rear part of the side wall.

Floors, shell, roof carriers, stairs, major framing, open door and installed windows have matching architectural collision. Cosmetic foliage stays non-colliding. Existing motor/input/camera scripts and their input asset are unchanged. Scene-only camera settings enable obstruction avoidance at4m distance and .05m near clip; mouse response remains unchanged.

## Sources and reusable assets

- `CM_CrookedMortar_Production01.blend`: editable fitted building and provisional fixtures, packed approved paint source.
- `build_production01.py`: bpy preparation of the approved B envelope, fitted aperture/partition changes, UV generation, integrity checks and validated FBX axis conversion. It reuses source models read-only. Rerunning overwrites only this new production export/source.
- `Assets/BlightBloom/Art/Architecture/CrookedMortar/Production01/Models/CM_Production01_FittedBuilding.fbx`.
- `.../Prefabs/CM_CrookedMortar_ProductionArchitecture.prefab`: connected building prefab, nested production kits retained.
- `.../Prefabs/CM_Production01_FixedSiteDressing.prefab` and `CM_Production01_FoundationMasonry.prefab`.
- Six new shared matte URP materials and a copy of the approved gouache sheet, used by the fitted adapters. Original kit materials remain shared and unchanged.
- `ArtSource/Pipeline/Review/*CrookedMortarProduction01.cs`: Editor-only integration/capture/validation snippets evaluated through the running Pipeline session; these are outside Assets and add no runtime scripts.

## Validation and limits

- `GeometryValidation.json`:117 fitted mesh parts,6040 triangles; zero nonmanifold edges, positive signed volumes, zero degenerate UV triangles. Shared paint UV reuse is deliberate.
- `UnityValidation.json`: zero missing scripts/materials; complete finite UVs/normals; maximum Blender-to-Unity mesh bounds discrepancy0.00000137m. Metre scale and orientation verified. No cosmetic botanical colliders.
- `TraversalValidation.json`: actual2m-high,.4m-radius CharacterController.Move in Play mode,43/43 waypoints. Covers approach, shop, treatment, preparation, storage, rear exit, study, bedroom, living, landing, stairs up/down, garden aisle and complete outer perimeter. This is automated swept-controller validation, not a human input playthrough or exhaustive proof of every point in the building.
- Camera:172 actual placement-method tests at four yaw angles per waypoint, zero blocked boom segments. Fourteen samples retract below.5m; minimum distance is about.274m. These angles can feel cramped or show the capsule too close. Manual indoor camera comfort remains a known follow-up; no gameplay camera code was changed to hide this limitation.
- `InputMotorValidation.json`: existing action asset initialized, existing motor gives sprint/walk ratio2.00,120 mouse pixels produce36degrees at both30 and120fps equivalent delta times.
- `SceneInventory.json`:362 enabled renderers,390 material slots and194206 triangles before culling/LOD,809 active transforms,220 colliders. These are scene inventory bounds, not measured GPU draw calls or a village-wide performance budget. Fixed-site batching reduced150 renderers;163 empty site containers were removed.
- Front, three-quarter, side, elevated, gameplay-distance and four interior camera renders in `Previews/`. `ActualGameViewExterior.png` and `ActualGameViewInterior.png` are captured from the running Play-mode Game view. No fog/bloom/blur was added. Two memoryless-depth load/store warnings occurred during screen capture; these are recorded separately from compilation/gameplay errors.

## Remaining refinement

Manual camera comfort in the narrower rooms/landing is the main gameplay-review concern. Interior furniture, books, medicine equipment, door interaction, and interior finish/detail are provisional. Some secondary windows retain the approved opaque painted glazing; they are not transparent views. Rear/side fitted-panel paint transitions and timber texture scale deserve art review. No claim of exhaustive seam/intersection testing or GPU profiling is made; approved roof junction geometry is reused unchanged.

## Open and test

Open the production scene and press Play. Click Game view to capture the mouse; WASD moves, Shift sprints, mouse orbits, Escape releases the cursor. Start through the canopy and open front door. Visit the shop, follow the central passage into treatment, enter the side preparation wing, continue through rear storage to the garden. Return, take the left straight stair to the landing, explore the study and front living/bedroom rooms, then descend. Walk around both building sides and the garden, and test camera orbit near walls and at the landing.

No packages, project settings, original prefabs, prior scenes or gameplay files were intentionally changed. No commits were made. See `PreservationValidation.json` for the byte-level baseline audit and `ChangedFiles.json` for the new-file inventory.
