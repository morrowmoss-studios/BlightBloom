# Briarwick Stable A — Review01

New prototype in `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, beside the reserved farmstead at **(46, 5.98, -12), yaw 255°, scale 1**. Existing farmhouse/stable placeholder remains intact; this is a separate supporting farm building, not a replacement of another approved asset. Stop for visual approval before expansion.

## Building

- Low, broad timber barn: main volume **8.4 × 5.4 m**; recessed tack/feed wing **2.3 × 4.2 m**, giving a combined wall envelope **10.7 × 5.4 m** and about 55 m² floor area. Roof peak approximately **4.88 m**, lower than Cottage A. Eaves/verges project beyond these wall dimensions.
- One paired horse doorway, measured clear frame **2.791 × 2.900 m**, with two outward-open leaves. Separate human entry **1.300 × 2.300 m**, and a connecting opening between tack room and stable.
- Central aisle, two simple stall rail partitions, packed-earth floor, low masonry returns, footed posts, modest braces and a closed loft loading hatch. No extra signs, ivy, loose feed props or exterior clutter.
- Roof pitch and lower lean-to distinguish it from the cottage's taller intersecting gables/dormer. Continuous lean-to edge boards finish the sloping cladding joint.
- Doors are **fixed-open review geometry**, not a new interaction system. Horse NPCs, horse controls and functional stable-management gameplay are not implemented.

## Appearance and pipeline

Eight project-owned material copies exactly match the approved Cottage A original-appearance materials, plus the existing packed-earth route material. Original atlases/normal/roughness textures are reused read-only. No repainting, contrast increase, sharpening, new gloss treatment or lighting change. Timber cladding is deliberately simpler than Crooked Mortar's plaster, curved roofs and ornament.

Editable Blender source: `ArtSource/Blender/Architecture/Briarwick/StableA01/BW_StableA01.blend`. Native roof, post and door geometry is reused from the package's existing inspected mesh data; fitted siding, framing, foundations and lean-to geometry are project-owned. Face-specific timber UVs keep grain along each member. Original source assets remain unchanged.

Nine FBXs and a reusable prefab: `Assets/BlightBloom/Art/Architecture/Briarwick/StableA01/Prefabs/BW_StableA01.prefab`. The separate approach is a 3.2 m wide terrain-following spur off the existing farm path; it is outside the building prefab. No terrain editing. Building root is at floor level for reuse; markers identify entries and stall areas.

**23,660 building triangles**, nine mesh renderers, eight shared materials. Separate approach: 52 triangles. Renderer count is not draw-call count: multi-material doors and roof require additional submesh draws. Original detailed hinges account for much of the geometry; repeated-village LOD/batching is future work.

## Validation

- Final meshes: complete UV/normal arrays, finite data, no degenerate triangles or missing materials; supported URP shaders. Material properties/maps match the approved source copies. Roof surface normals face upward. An initial source-face handedness defect was corrected before final captures/validation; no repainting was used to mask it.
- Horse clearance: sampled **1.2 × 2.6 × 2.8 m** geometric envelope at three lateral positions through approach, opening and central aisle; no stable collisions. This is not a horse-controller, turning-radius, mounted-rider or stall-animation certification.
- Fourteen Play-mode cases passed using the unchanged real CharacterController.Move: three horse-entry/aisle lanes both ways; human entry/tack room both ways; tack-to-main connection both ways; perimeter both ways; new farm spur both ways. All endpoints grounded. Motor, camera and player state restored. No keyboard-input or manual camera-comfort claim.
- Prefab and scene triangle counts match; prefab root scale is 1 and fixed-open door poses persist. Solid floors, thresholds and associated basic mesh collisions included. No shared gameplay edits.
- Existing **244 scene objects** match their full component snapshots. SHA256 check of **2,224 existing files** found only the authorized Briarwick scene changed; nothing missing. Approved Cottage A, Crooked Mortar, source package, other scenes, settings and previous review/source files remain intact.
- Final Console: no new warnings/errors; compilationFailed=false. No build or unrelated project-wide regression was run.

## Review and limitations

The prototype reads as a small working timber stable, with a lower silhouette, large horse opening and modest service wing. It shares the cottage's weathered brown/grey material character while retaining a simpler, less ornate construction than Crooked Mortar.

Cladding is regular and reuses a small set of native grain regions; it is not final bespoke hand-painted barn art. The earth spur has blockout edges matching current village routes. Stall gates, feed fixtures, horse placement/turning, weather blending, LODs and manual camera review remain future work. Do not expand detailing until this massing and material treatment receive approval.

- [Three-quarter](StableA_ThreeQuarter.png)
- [Front](StableA_Front.png)
- [Entrances](StableA_Entrances.png)
- [Loft and side](StableA_LoftAndSide.png)
- [Player-height approach render](StableA_GameplayApproach.png)
- [Farmstead/village context](StableA_VillageContext.png)
- [Stable, Cottage A and Crooked Mortar](VillageStyleComparison.jpg)

Comparison cameras share 20 m horizontal distance, 9 m elevation offset, 55° FOV and 3.4 m target height. Stable camera uses its front approach direction; others retain their established comparison azimuth. Scene sun/fog/exposure are unchanged, so different building orientations receive naturally different incident light. No editing gizmos, grading or depth-of-field masking.

## Changed files

Existing file changed: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`.
New assets: `Assets/BlightBloom/Art/Architecture/Briarwick/StableA01/` — FBXs, approach mesh, eight materials, prefab and metadata.
New source: `ArtSource/Blender/Architecture/Briarwick/StableA01/` — editable model, guarded builder and model catalog.
New reports/captures/snippets: this directory. `ChangedFiles.json` lists exact task paths.

No commits, pushes, packages, cleanup, archiving or LFS work. Briarwick is saved and left open with Stable A selected for manual review.
