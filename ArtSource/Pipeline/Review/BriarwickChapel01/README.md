# Briarwick Chapel01 — rough architectural review

2026-11-02. Saved in EXISTING `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, replacing location09 visually. Original `09 Small chapel PLACEHOLDER` retained disabled. Position(-44,5.74665,30), yaw135°, unit scale. No new scene or changes to village layout.

## Build and measurements

Modest stone nave, sparse dressed corner/door/window surrounds, plaster gables, weathered wood-shingle roof and static double entry. No bell tower, chimney, cathedral ornament, loose clutter or interior gameplay. Existing graveyard and road approach remain intact.

- Main footprint **7.6 ×10.8m =82.08m²**, within the original8 ×13m placeholder. Roof envelope about8.3 ×11.6m; shallow entry stoop.
- Height **7.37m above placement datum**; floor datum +0.12m.
- Clear entry **1.6 ×2.5m**, two static leaves. Structural dimensions measured excluding closed leaves; no claim of traversing into a playable interior.
- **12,378 triangles**, **11 mesh renderers**, **13 shared materials**. Static mesh colliders; no LODs yet.

## Stained-glass front gable

Implemented a real front-gable aperture and thick glazed panel with a continuous recessed stone reveal and physical dark perimeter. Window **4.7m wide ×3.1m high**. Projected glass area **9.06m²**, about**64.6%** of the14.02m² front gable; the gable is visually dominated by glass rather than plain infill.

Muted blue/sage/amber panes, painted lead lines and simple sun-and-sprig rural imagery. **No letter A or lettering**. The panel uses opaque URP Lit glass artwork with restrained emission for exterior readability; this is a rough exterior glass treatment, not simulated transmission or a playable interior view. No bloom/light added. Paint generator and source PNGs retained under ArtSource/Paint.

## Validation

- **12/12 grounded automated Play-mode CharacterController.Move checks passed**: three lateral entrance lanes, original road connection, front frontage and complete perimeter, forward/reverse. Existing controller2m high/.4m radius; motor/orbit and player transform temporarily paused/restored. Not manual input or camera-comfort approval.
- All eleven meshes: finite UVs, valid normals, zero degenerate triangles; supported materials and no missing texture references.
- Door opening measured1.6 ×2.5m. Terrain contact sampling shows the existing pad stays within millimetres of the original datum.
- **30/30 roof coverage rays hit**, correct upward normals. Initial coverage failure traced to excluded source wood3 faces being structural eave closure; restored complete source roof modules, preserving UVs. Native roof mesh source/package unchanged.
- Initial masonry derivative crop contained padding; corrected using the source floor’s known top-face UV region. Corrected the painting source and refreshed packed Blender texture. Final views checked front, side, rear, gable close-up and context.
- Final Console**0 errors/0 warnings**, compilation not failed; historical captured warning cursor44 unchanged. One transient eval-snippet compile diagnostic was corrected; it was not an imported C# or project compilation error. Console not cleared.
- **431 pre-existing scene objects’ component snapshots unchanged**, outside new chapel root. Placeholder deliberately disabled. **2,749 baseline hashes checked**: only authorized Briarwick scene changed. Other buildings, roads, terrain, bridge, creek, graveyard, approved assets, packages and gameplay unchanged.

## Assets and dependencies

Reusable `Assets/BlightBloom/Art/Architecture/Briarwick/Chapel01/Prefabs/BW_Chapel01.prefab`, eleven grouped FBX models, project-owned materials and two texture exports. Editable packed `ArtSource/Blender/Architecture/Briarwick/Chapel01/BW_Chapel01.blend`.

Reuses read-only cottage/package roof, timber, stone, door and hardware maps; existing plaster and small-window material sources. Own softened stone derivative and stained-glass artwork. Exact current Unity dependencies in `FinalIntegration.json`.

## Remaining rough-build limitations

Roof course pattern remains regular and source geometry simple; future refinement can soften repetition and improve local joins. Corner dressings are plain and need more tactile variation, rear gable intentionally simple, small side glazing dark. Stained glass remains a relatively flat illustrated exterior treatment: no colored light projection, optical transmission or interior. Future lead depth and pane finish would improve close views. No bells, NPCs, interior or religious gameplay introduced. No final artistic approval claimed.

## Review

`Chapel01_Front.png`, `Chapel01_ThreeQuarter.png`, `Chapel01_Side.png`, `Chapel01_Rear.png`, `Chapel01_StainedGlass.png`, `Chapel01_VillageContext.png`. Existing scene lighting, clean camera captures without gizmos. Review camera restored after capture. Building selected in saved Edit-mode scene.

Changed-file inventory in `ChangedFiles.json`. Pre-existing untracked MillerCottage files left untouched. No commit/push. Stop for visual approval.
