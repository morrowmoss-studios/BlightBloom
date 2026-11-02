# Stable A — open-front Review02

Current candidate in `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`: `Stable A - open-front review02/BW_StableA02_OpenFront`. Saved for visual approval. The previous `Stable A - farmstead review01` root is retained **inactive**; its original Blender, FBX, prefab, materials and screenshots remain untouched.

## Architectural change

- Removed both main front wall panels, both horse doors, their narrow jambs, front sill and continuous front foundation runs from the new asset. The main frontage is now fully open between four timber bearing posts; no floating hinges or door hardware remain there.
- Three visible stall bays with low kickboards and rails. Dividers end at z=1.2 m, leaving circulation in front. Kickboards are approximately 0.62 m high; posts/upper rails reach 1.4 m. No gates close the frontage.
- Preserved the low, broad body footprint, position (46, 5.98, -12), yaw 255°, and approximately 4.88 m ridge height. Body footprint remains 10.7 × 5.4 m including the tack wing.
- Extended only the front roof slope. Front edge is z=3.96 m versus posts at z=2.70 m: **1.26 m cover**, previously approximately 0.27 m. Front bearing posts/beam and gable verges fit the revised slope. No change to the rear slope or main ridge height.
- Tack/feed room remains enclosed on one side. Its human door moved to the **outer side wall**; the former front doorway is filled with fitted siding. Service door remains a fixed-open prototype leaf. A connecting opening still links tack room to the stable.
- Removed the front raised plinths and retained small support pads beneath posts. Floors stay continuous; no front barrier crosses the bays.
- Same eight shared muted material assets; no texture repainting, sharpening, tint, roughness or lighting changes. Cottage A and Crooked Mortar unchanged. No loose clutter added.

## Assets and reuse

New prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/StableA02OpenFront/Prefabs/BW_StableA02_OpenFront.prefab`.
Editable source: `ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/BW_StableA02OpenFront.blend`.

Five new FBXs: shell, structure, roof, foundation and low partitions. Existing floor, loft hatch and human-leaf FBXs are reused unchanged from Review01; the human leaf receives a new local placement. The earth spur is reused as a separate scene object. All materials remain shared read-only from Review01.

Building: **14,956 triangles**, eight renderers and eight shared materials, down from 23,660 triangles. The separate approach remains 52 triangles. No new gameplay scripts, interaction system, horse NPCs or packages.

## Validation

- Three measured clear bay widths approximately **2.491 m** between posts, with **3.230 m** under the front bearing beam. The extended eave is lower than that beam; a conservative 2.6 m high horse envelope was checked along the complete approach rather than relying on beam height alone.
- Side service opening: **1.300 × 2.300 m**.
- **369** overlap-box positions checked with a 1.2 × 2.6 × 2.8 m horse envelope across all three approaches/stalls; no obstruction. This does not certify a horse controller, rider clearance or turning animation.
- **377** downward floor probes across shelter and tack room: no missing floor coverage. **27** frontage probes at several widths/heights: no front wall/door obstruction.
- **26 Play-mode CharacterController.Move cases passed**, with grounded endpoints: three lanes through each bay both directions; side service entry; tack connection/front cross aisle; perimeter; farm spur. Existing 2 m controller, radius 0.4 m and all movement/camera settings unchanged. Runtime player/motor/orbit state restored. No manual camera-comfort or keyboard-input claim.
- Valid mesh UV/normal arrays; finite vertices; no degenerate triangles, missing textures/materials or unsupported used shaders. Roof top faces point upward. Material copies still match their approved sources.
- Existing 262 objects' component snapshots unchanged; the historical review root's active state is intentionally disabled. No duplicate active building/path collision. Other village objects and gameplay remain intact.
- SHA256 check of 2,294 existing protected files: only the authorized hamlet scene changed; none missing. Previous stable files, approved cottage, Crooked Mortar, original package and other scenes/settings remain unchanged.
- Final Unity Console: no new errors/warnings; compilationFailed=false. No unrelated project-wide regression or build.

## Visual review and remaining limitations

The frontage now reads as a roofed shelter with visible open bays rather than a closed barn. Low rails, deep roof shade and the side-only service room keep the composition practical and modest. Original regular timber textures and the blockout-edged earth spur remain prototype limitations. Horse gameplay, stall furnishings and manual camera comfort await later review; no decoration was added to compensate.

- [Matched before/after front](BeforeAfterFront.jpg)
- [Front](OpenFront_Front.png)
- [Three-quarter](OpenFront_ThreeQuarter.png)
- [Low approach / visible stalls](OpenFront_GameplayApproach.png)
- [Entrances](OpenFront_Entrances.png)
- [Loft and side](OpenFront_LoftAndSide.png)
- [Village context](OpenFront_VillageContext.png)

Camera settings and scene light/fog match Review01 for the paired views; no editing gizmos or image grading. All final captures are renders from the running Unity scene.

## Scope

Existing file changed: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
New files: the `StableA02OpenFront` asset/source folders and this review folder. `ChangedFiles.json` lists exact task paths.

To compare the prior barn, disable Review02 and re-enable Review01; never enable both at once. No previous asset was deleted or overwritten. No commits, pushes, cleanup, LFS or unrelated changes. Scene left open with the new shelter selected.
