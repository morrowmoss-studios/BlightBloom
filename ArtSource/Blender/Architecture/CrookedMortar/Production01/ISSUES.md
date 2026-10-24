# Crooked Mortar Production01 — open issues

Scene: `Assets/Scenes/CM_CrookedMortar_Production01.unity` (project-relative).
These are reported issues, recorded without investigation or fixes in this documentation task. Exact object names and locations remain unconfirmed; identify them before editing.

| ID | Description | Suggested investigation scope | Status |
| --- | --- | --- | --- |
| CM-001 | Hanging herbs visibly float or lack convincing attachments. | Inspect affected bundle roots, hooks/ties and canopy/beam contact in the production scene; check instance overrides before changing shared assets. | Open — reported; attachment audit pending. |
| CM-002 | At least one lantern floats away from its intended mount. | Identify the lantern and bracket, compare rendered geometry with mounting surfaces, and inspect transforms/overrides. Distinguish light gizmos from the rendered fixture. | Open — reported; location unconfirmed. |
| CM-003 | Unexplained diagonal markings appear on two walls. | Locate and reproduce in Game view; distinguish geometry overlap, UV/material discontinuities and lighting/shadow artifacts before choosing a fix. | Open — reported; cause unconfirmed. |
| CM-004 | Window treatments vary between glazing and boarded/opaque-looking openings. | Inventory only the affected window instances; distinguish intentional shutters/painted glazing from missing or mismatched materials. Agree on treatment before editing approved modules. | Open — art consistency decision pending. |
| CM-005 | Indoor camera comfort needs manual review. | Walk principal rooms, landing, stairs and doorways; orbit near walls and furniture. Judge visibility, retraction and capsule occlusion, beyond automated obstruction checks. | Open — manual acceptance pending. |
| CM-006 | Unity shadow-atlas resolution warnings need investigation. | Capture the exact warning and reproduction conditions; inspect relevant shadow-casting lights and active URP shadow budgets. Do not assume screenshot depth-buffer warnings have the same cause. | Open — reported; diagnosis pending. |

## Next milestone: production stabilization and manual acceptance

1. Confirm the repaired saved scene in a manual walkthrough: every principal room, bedroom floor, stair direction, entrance, perimeter and garden route. Any fall-through, blocked route, collider mismatch or unusable camera view is a functional blocker and takes priority.
2. Review CM-005 and diagnose CM-006. Camera obstruction that prevents navigation is a blocker; discomfort without blocked play is a refinement. Escalate shadow warnings if they cause missing/unstable lighting or significant performance loss; otherwise schedule rendering cleanup.
3. Resolve CM-001–004 in a focused visual-coherence pass after functional acceptance. These are deferred visual issues unless inspection reveals a collision or navigation impact. Preserve the approved architecture and kits.

No new structural blocker was confirmed by this documentation-only task. Earlier successful automated checks remain context, not a substitute for manual acceptance. Do not begin this milestone until requested; no new asset families or broad redesign are needed to start it.


## Production02 finishing status — 2026-10-17

Current working candidate: `Assets/Scenes/CM_CrookedMortar_Production02.unity`.
The Production01 rows above remain historical/open for that preserved scene; these results apply **only to Production02**.

| ID | Production02 finding / action | Current status |
| --- | --- | --- |
| CM-001 | Three drying bundles had no modeled rail at their ties. Added a walnut rail and two short canopy suspensions. | Corrected in Production02; rendered attachment review passed. |
| CM-002 | Left lantern curl ended above its crown. Seated it and added canopy-connected mounting plates for both curls. Existing lights/intensities preserved. | Corrected in Production02. |
| CM-003 | Reviewed current plaster room/exterior views and active window structure. Legacy window knee braces/eaves were already disabled; no unidentified diagonal wall geometry reproduced. Approved plaster brush strokes and the intentional structural brace retained. | Not reproduced in Production02; the two originally reported wall locations still need identification if seen again. |
| CM-004 | Existing paired and arched panes used an opaque amber material. Applied shared, softly tinted translucent glazing while retaining frames, shutters and frame shadows. | Corrected in Production02; inside/outside views inspected. |
| CM-005 | Connected routes and 64 camera samples checked; controller/camera unchanged. Stair-turn camera retraction remains the main manual comfort concern. | Open — manual acceptance still required. |
| CM-006 | No shadow-atlas warning reproduced during this focused Play/capture pass; Console currently has zero errors/warnings. No light budgets or URP settings changed. | Deferred — historical warning remains unconfirmed, not declared fixed. |
| CM02-007 | Exposed wing roof end, buried verges and standing valley strips. Fitted the existing wing pitch into the main envelope, trimmed concealed gable portions, replaced valley caps with conformed liners. Outer eaves, peaks and footprint preserved. | Corrected; surface probes and clean junction views passed. |
| CM02-008 | Thin landing-guard floor seam and unfinished guard tops/ends. Added fitted foot joint, caps and end trim within existing guard footprints. | Corrected; stair ascent/descent and landing routes passed. |
| CM02-009 | Closed entrance leaf had a visible right-edge daylight gap. Deepened and reshaped its existing local arched rebate to seat against the wood silhouette; no extra collider. | Corrected; oblique interior view and live E-key regression passed. |
| CM02-010 | Ivy sat off the facade/post transition. Seated the same instance closer to the plaster and kept it outside the entrance route. Pots and window-box seating inspected. | Corrected in Production02; density unchanged. |

Validation: 56/56 connected traversal routes; 2,028 floor/ceiling surface samples without holes; 4,732 roof-envelope samples without misses; 14/14 live E-input/safety checks and 9/9 related passage checks. All 90 existing colliders unchanged. Reports and current limitations: `../Production02/Finishing/README.md`.


## Production02 staircase manual finding and correction

Manual playtesting rejected the solid-guard stair construction despite earlier obstruction/traversal checks. CM-005 remains **open for manual acceptance**, with a corrected candidate now implemented; the guard-cap-only CM02-008 fix is superseded for this stairwell.

`Production02/StairUsability02/README.md` records the open timber balustrade/landing revision and scene-local predictive camera. The final live-input stair run kept 1.95 m minimum / 3.18 m median camera distance, head/torso visible, no camera overlaps and no emergency corrections during walking. Both stair directions and adjacent rooms passed; 32 guard-edge and 220 landing-floor checks passed. Shared gameplay/camera source and the approved exterior are unchanged. Human review of orbit assistance and turning feel is still required before closing CM-005. Existing Production01 issue statuses above remain untouched for that scene.


## Production02 focused repair — 2026-10-18

| ID | Finding / action | Current status |
| --- | --- | --- |
| CM02-011 | Shop-display door-side shutter intersected the outward front door. Scene-only shutter yaw changed 27° → 99°, hinge retained. Actual mesh tested over the full 105° door sweep with 3 cm envelope margin; live E interaction and related passage checks passed. | Mechanical fix was visually rejected; superseded by FacadeEntrance04 below. |
| CM02-012 | Redundant wall-side upper-flight rail and turning-wall rail removed from dedicated local stair mesh. Added open timber protection across exposed upper-floor lower-flight opening, seated to wall/centre newel; continuous player-safety collider refitted. | Corrected; all 36 guard/connected-route checks passed, including edge pushes and both stair directions. |
| CM-005 | Local assist fought user orbit. Look now takes priority; assistance resumes only while moving after one second without look. Added affected doorway zones and obstruction-driven 65°–78° local FOV. Full mouse circles passed at five locations with no overlaps; 19 live movement connections passed. | **Open — manual comfort acceptance pending.** Close-wall orbit still retracts substantially (down to ~0.54 m in deliberate full-circle tests); two automatic recovery turns recorded. Prior automated acceptance is superseded, not treated as proof of comfort. |

Details, previews and exact scope: `../Production02/FocusedRepair03/README.md`. No other scenes, approved kits, shared gameplay, settings or packages changed; nothing committed.


## Production02 facade / entrance visual correction — 2026-10-18

| ID | Finding / action | Current status |
| --- | --- | --- |
| CM02-011 | Previous 99° single-shutter fix rejected visually. Lower shutters are now a matched 9° / 351° pair; the existing door is right-hung with a 105° outward swing and continuous projected reveal. Right planter moved beyond its stop. Original approved meshes/materials reused; derived door copy preserves correct exterior/hardware orientation. | Visually rejected; superseded by EntryShopComposition05. Mechanical checks did not establish artistic approval. |
| CM02-013 | Left LivingWest shutters hidden by the earlier finalization renderer-disable operation. Restored both leaves; seated the corner-side leaf against the nook return instead of embedding it in the wall. Rear paired windows were inspected and already have visible shutters. | All 14 relevant renderers enabled; adjacent-wall fitting checks passed. **Awaiting manual visual approval.** |

Complete-facade closed/open previews and scope: `../Production02/FacadeEntrance04/README.md`. Other architecture, rooms, cameras, gameplay and approved kits unchanged. No commits.


## Production02 coherent entry / shop section 05 — 2026-10-18

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-011 / CM02-014 | Prior localized arrangements rejected. Replaced broad shop shutters with fitted matching bi-fold stacks, narrowed the existing shop insert with plaster returns, restored the shallow doorway, and used a right-hand outward swing away from the display. Base timber now terminates at the stone jambs; porch/shop finish overlap removed. | Functional checks passed (211 sweep poses, 14 E-key checks, nine passage checks, eight live-input entry/exit connections). **Manual visual approval pending; no previous shutter arrangement is treated as approved.** |

Six complete-facade / approach closed/open previews, source paths and scope: `../Production02/EntryShopComposition05/README.md`. Expanded layout, roof hierarchy, unrelated rooms/assets, camera and gameplay source preserved. Two obsolete projecting-return colliders disabled; original functional collision preserved. Nothing committed.

## Production02 plague doctor locomotion — 2026-10-20

| ID | Finding / action | Status |
| --- | --- | --- |
| BB-CHAR-003 | Rigged02 had limited elbow articulation, minimal body coordination and one short-stride clip accelerated for sprint. Locomotion03 adds coordinated wrist/foot trajectories, separate walk/sprint clips, phase-preserving transitions, authored-knee-plane ground contact and corrected coat weighting/linen walking vents. Rigged02 retained disabled for recovery. | Live focused Play-mode captures passed at unchanged 3/6 m/s; 19 stair/room, eight E-key entry/exit and 12 garden/exterior connections passed. **Manual animation feel approval pending.** Limited bone-driven cloth and approximate stair foot placement remain polish items. No shared gameplay/camera/collision changes. |

Source, previews, reports and exact changed-file list: `../../../Characters/BB_PlagueDoctor01/Locomotion03/README.md`. No character compilation errors or gameplay exceptions observed; Pipeline automation timeout remains in Console. Nothing committed.


## Production02 ground-floor furnishings — 2026-10-21

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-FURN-001 | Placeholder ground-floor furniture replaced scene-locally with a reusable painted furnishing family. Initial stool/cabinet and instrument-stand/bed approach conflicts corrected before live validation. | Nine standing markers clear; 18 furnished-room, 19 stair/connected-room, eight E-key entry/exit and 12 garden route waypoints passed through the existing controller. Walk/sprint/stop smoke test passed at unchanged 3/6 m/s. Manual arrangement and camera comfort approval pending. |
| CM02-FURN-002 | Existing indoor camera can retract strongly near doorways and stairs; six emergency corrections occurred during the stair smoke route. | Retained for manual review; no camera changes in the furnishing pass. No sampled camera/geometry overlap. Automated accessibility does not establish comfort. |

Sources, previews, measurements and validation: `../../../Interiors/CrookedMortar/ApothecaryFurnishings01/README.md`. Furniture stations currently provide planning markers only; patient/crafting animations and interactions remain future work. No architecture, shared gameplay, approved kits or settings changed. Nothing committed.


## Production02 shop/entrance hero-detail pass — 2026-10-21

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-002 | Basic counter/shelf construction and repetitive stock refined with shaped joinery, apothecary relief, varied vessels, case records, consultation signage and fitted entrance detail. Originals preserved through scene-local visual overrides and separate derivative assets. | Integrated and saved; artistic approval pending. Source/import checks pass; all 108 collider definitions/transforms/activation unchanged; 43 door-sweep poses clear the new art. Live input checks passed: nine shop-route and eight E-key entrance/exit waypoints; zero sampled camera/geometry overlaps and zero emergency corrections. Unity reports no new errors/warnings. Manual artistic and camera-comfort approval remains pending. |

Matching before/after previews, editable source, scope and limitations: `../../../Interiors/CrookedMortar/HeroRefinement02/README.md`. No shared gameplay/camera/door/settings or roof changes. No shutters restored. Nothing committed.
