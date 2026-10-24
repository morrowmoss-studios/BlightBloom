# Crooked Mortar — supported, lived-in rooms 03

HeroRefinement02 is **not artistically approved**. This pass corrects its placement defects and develops the shop and preparation room as connected working spaces. Manual visual approval remains required.

## Placement diagnosis

The herbarium board was at `(0.065, 1.85, 3.20)`, but the west shop wall ends at z=2.20. It therefore occupied the open stair/lobby connection. The installer assumed a continuous wall and checked neither wall support nor the visible mesh. Its local/world transform was numerically consistent because the presentation root was identity; the architectural support assumption was wrong. A cosmetic non-colliding frame made the error walk-through. Adding a collider would have created an obstacle in a valid route rather than fixing its installation.

The frame is now on the solid shop-to-kitchen jamb at `(5.377, 2.08, 1.10)`, facing into the shop. Nine back-plane samples hit the **visible wall triangles**, with approximately 3 mm seating clearance. The former opening is clear. Its original prefab and materials are unchanged.

The audit also corrected:

- Shop drying rail: roughly 4 cm support gap → seated against the west shop wall.
- Preparation drying rail: rear rail embedded about 4 cm → seated just in front of the wall.
- Porch plaque: roughly 4 cm off its supporting post → centrally seated on the timber.
- Limewash repair: roughly 10 cm in front of plaster → seated on plaster and reduced to fit the plaster field rather than encroaching on stone trim.
- Ivy drape: unsupported canopy placement → stem attached to a ray-checked point on the existing curved arch.

`VisibleSupportValidation.json` records actual visible-mesh hits. `SurfaceValidation.json` checks tabletop contact (roughly 2.5–6.5 mm for paper, ink, jar and gently folded cloth). `ExteriorAttachmentCorrections.json` records the fitted arch anchor. Existing herbs' loops overlap their hanging rails; new ceiling herbs use explicit driven hooks. Thin wall artwork, paper, herbs and utensils remain cosmetic. Two fixed wall-furniture boxes and six beam/bearing-pad boxes provide purposeful collision; the 108 pre-existing collider definitions remain unchanged.

Historical HeroRefinement02 install/finish source is corrected for the discovered placements. The new installer uses explicit wall-back/surface datums, nine-point support checks and recorded prefab transform overrides. No shared gameplay or camera source was changed.

## Room composition

- The shop gains a supported records/dispensary alcove on its previously bare east wall, with patient-case bindings, notes and supplies below the relocated botanical reference. The counter remains the commercial focal point. A wall-to-wall timber and shaped bearing pads connect the upper room visually; two small herb groups hang from explicit underside hooks above player clearance.
- Preparation gains a fitted low reagent cupboard and separate tool rail above it on its west wall, balancing the existing east workbench. A mounted formulary completes the wall above the existing herb rack. An initial cabinet-height camera retraction was caught in route samples; the new cupboard was lowered below the usual camera line, retaining its footprint. The bench receives fitted knee braces, nosing, an offset portable herb press, working cloth, prepared leaves and a notebook. Main workbench access, storage route and central circulation remain available.
- Existing sage/walnut/ivory paint, ink artwork and botanical prefabs are reused. Lighting, exposure, post-processing, roof, window treatment, room dimensions and existing furniture footprints were not redesigned. No noise/grime filter or repetitive prop scatter was added.

## Gameplay-view review

`Previews/Comparison/`: before left, after right. Six matched views cover shop, counter/shelving, stair transition, preparation cabinet, preparation bench and corrected mounting. PNG originals are under `Before/` and `After/`.

These are Unity **ScreenCapture Game-view frames using the existing gameplay camera and visible avatar**, not a separate observer camera. Before poses are recorded in `GameViewPoses.json`; after comparisons pin that same camera to those recorded transforms for the capture only, then restore normal camera operation. After choosing more representative opposing room angles, the before state was replayed temporarily in Play mode from the pre-pass placements with new fixtures disabled. The saved scene was never rolled back. The capture utility waits for the queued screenshot frame before restoring the player, avoiding an end-frame restoration artifact. Original PNGs are not retouched.

Room-level judgments are more important than library counts: the opposite wall now reads as a records station, the stair connection no longer contains floating art, preparation has opposed work/storage areas and overhead structure. Large plaster fields and quiet circulation space deliberately remain. These changes do **not** establish final illustrated-art quality or approval.

## Sources and scope

Editable Blender: `CM_LivedIn03.blend`; modeling/export: `build_lived03.py`. Unity family: `Assets/BlightBloom/Art/Interiors/CrookedMortar/LivedIn03/`. Shared painted sources remain in the prior approved/foundation folders. Original art and previous variants were not overwritten. One-time installer/finish snippets are guarded; do not rerun them over the saved scene.

New scene root: `19 Lived-in shop and preparation 03`; fitted workbench details are children of its original bench. `ChangedFiles.json` is the exact inventory. Nothing committed or pushed.

## Remaining limitations

The new storage, press and records are visual props, with no medical/crafting/inventory interactions. Small labels and incised detail remain secondary and some surfaces are still simplified; this is not final hero art. Bone-driven player cloth and existing indoor camera behavior are unchanged. Automated camera visibility checks cannot establish manual comfort. The painting now has verified support, but final composition and storybook richness still require manual artistic review.


### Current verification state

Visible support and tabletop contact checks passed. Blender UV/normal/geometry checks passed. Unity import has no missing scripts/materials; 108 original colliders are unchanged, with eight purposeful new wall-furniture/timber colliders. The 105-degree door sweep clears the new art in 43 sampled poses.

The first 17-waypoint room/garden route passed, but exposed a near-cabinet camera retraction (0.50 m minimum). That report is retained as `RoomRouteBeforeCupboardAdjustment.json`. The cupboard was lowered afterward. The final arrangement reached 16 of 17 room/garden waypoints, including the cupboard approach and garden exit, before application focus was lost. Sampled camera distance at the cupboard approach improved to approximately 0.99 m; this is not manual comfort approval. The final garden-return segment remains unverified.

E-key entrance/exit, stairs and idle/walk/sprint regression checks remain **blocked by the locked Mac / missing Unity focus**. No successful result is claimed for these checks. The waiting callback and five leftover temporary input devices were removed; Play mode was stopped. Production02 is saved and open in Edit mode. Compilation is successful; Console reports zero current errors and two warnings whose messages were not available in the captured buffer, so warning-free status is not claimed. No Console entries were cleared.
