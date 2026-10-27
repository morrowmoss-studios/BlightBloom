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


## Production02 supported shop/preparation pass — 2026-10-24

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-PLACE-003 | HeroRefinement02 herbarium frame was placed in the open stair connection because the installer assumed the west wall continued past z=2.2. Cosmetic collision was appropriate only for a mounted frame; its location was wrong. Relocated to the verified solid shop/kitchen jamb and corrected the install source. | Visible-mesh back-plane support checks pass; the former painting route passed through the normal player controller. Manual visual review pending. |
| CM02-PLACE-004 | Audit found shop rail gap, preparation rail penetration, porch plaque offset, floating limewash patch and unsupported ivy root. | Placements corrected against actual support geometry. Surface/visible-support reports preserved. No collision added to paper, pictures, herbs or tiny tools. |
| CM02-ART-003 | Shop and preparation room remained sparse/disconnected. Added supported records alcove, reagent cabinet/tool rail, connected timber details, formulary and a working herb press/notes arrangement. | Integrated; **not artistically approved**. Matched actual Game-view comparisons available. Initial room/garden route passed but exposed camera retraction near the new cupboard. Cupboard lowered; final route reached 16/17 points through the garden exit before focus loss. Cupboard-approach camera distance improved from about 0.50 m to 0.99 m. Garden return, live E-key door, stairs and locomotion checks remain blocked by locked Mac/application focus; no final gameplay pass claimed. Waiting test and temporary devices cancelled; saved scene open in Edit mode. Zero current Console errors; two warnings require message review. |

Current scope, sources and comparisons: `../../../Interiors/CrookedMortar/LivedIn03/README.md`. Earlier HeroRefinement02 navigation reports did not validate decorative mounting and are not proof of these repairs. No layout, shared gameplay/camera, lighting or settings changes. Nothing committed.


## Production02 illustrated composition pass — 2026-10-24

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-004 | Reference comparison showed sparse wall fields, basic furniture profiles and isolated decoration. Added fitted carving/trim, botanical working displays, mixed book/order collections, textiles and painted plaster/sign surfaces. | Saved for artistic review; not approved. Matched actual Game-view captures document gains and remaining simplicity. No architecture, gameplay, camera or collision changes. |
| CM02-PLACE-005 | All eight window planting inserts shared an incorrect generic root height, burying their roots 0.13–0.14 m below the actual soil surface. | All eight roots checked/seated on actual planter soil mesh triangles. Source kits unchanged. |
| CM02-PLACE-003 follow-up | Rechecked the previously relocated herbarium painting and existing wall furniture against visible meshes; inspected new mounting rails, jamb trim and headers. | Existing painting/support checks and 13 new multi-point mount checks pass. No indiscriminate decoration colliders added. |

Evidence and remaining limitations: `../../../Interiors/CrookedMortar/Illustrated04/README.md`. The first sequential live-input test waited for focus and timed out while the Mac was locked; no final live room/door/stair/locomotion pass is claimed. Waiting test was cancelled. All 116 baseline colliders remain unchanged and 43 outward door-sweep samples clear the new art. Nothing committed or pushed.

CM02-ARCH-005: Close Game-view review revealed rectangular-to-arched corner gaps around the existing entrance surround. Originally deferred in Illustrated04; fitted plaster returns now close these corner voids in Craftsmanship05, with door-sweep clearance verified. The stair-side order parcel was relocated to the records shelf with verified surface contact.


## Production02 structural craftsmanship benchmark — 2026-10-24

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-005 | Printed ornament and simple construction did not provide enough intrinsic craft. Replaced the counter visual body and scoped portal/front/ceiling timber profiles with sculptural derivatives; retained existing loose props and all functional systems. | Saved for controlled artistic review; not approved for wider propagation. Plaster/eave changes are quieter; approved window assets remain unchanged. |
| CM02-ARCH-005 | Existing rectangular-to-arched entrance reveal corner voids were visible. | Fitted plaster returns installed outside the door leaf; 43 full-swing samples clear the new geometry. Close-view confirmation included in this pass. |

Sources, matching Game-view comparisons and validation distinctions: `../../../Interiors/CrookedMortar/Craftsmanship05/README.md`. All 116 colliders remain unchanged. The 190-sample static player-volume clearance probe passes entry, both counter sides and connected stair/kitchen routes; this is not live-input playtesting. No additional loose props, new shutters, room redesign, shared gameplay/settings edits or commits.

## Counter-only art pipeline experiment — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-007 | Repeated primitive-derived construction/shared atlas sampling did not reach the illustrated target. Tested bespoke profile construction, continuous stencil-led sculpt fields and dedicated painted walnut/carving maps on one replacement counter. | Separate `CM_CounterWorkflow07_Review` scene only; Production02 unchanged. Substantially richer carving at tested gameplay distance; manual artistic approval pending. Remaining rectilinear carcass, map/geometry registration, small-edge cleanup and LOD/bake budget documented. No wider rollout. |

Evidence: `../../../Interiors/CrookedMortar/CounterWorkflow07/README.md`. The interrupted Reconstruction06 scene installation was restored before this experiment; its unapproved sources remain recoverable. Existing functional counter, approved kits, scripts and all 116 colliders preserved. No additional loose props or commits.

## Expressive counter form experiment — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-008 | Workflow07's ornament improved but rectangular structure remained dominant. Workflow08 reconstructs the worktop, four shaped supports, bowed fields and scalloped open base; reserves carving for the central board; fixes sculpt paint registration with continuous UVs and a mesh-derived colour bake. | Isolated `CM_CounterWorkflow08_Review` only. Clear silhouette improvement in matched relief-free clay views. Artistic approval pending: rounded supports may feel too formal, close carving remains softer than Workflow07's painted imagery, and surrounding shelves/props need a separately approved future style assessment. Production02 and Workflow07 untouched. |

Evidence/method/limitations: `../../../Interiors/CrookedMortar/CounterWorkflow08/README.md`. Existing 116 colliders, station markers and gameplay systems retained; 43 door poses and 190 static capsule clearance samples pass. Play-mode comparison captures are not a fresh live-input traversal or manual camera-comfort test. No added loose props, commits or wider rollout.

## Focused counter workflow validation — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-009 | Workflow08 supports felt overly smooth/formal and the carving remained soft. Workflow09 directly refines its editable source with chamfered pegged timber posts/bearing knees, a higher-detail central relief and restrained existing-paint colour tuning. | Separate `CM_CounterWorkflow09_Review` only; artistic review pending. Clear joinery improvement, incremental carving/material improvement. Fine sculpt cleanup, repeated grain and LOD budget remain. Production02 and Workflow07/08 protected. |

Evidence and targeted validation: `../../../Interiors/CrookedMortar/CounterWorkflow09/README.md`. Existing colliders/markers/systems retained; static door sweep and nearby capsule-route probes pass. Captures are actual Play-mode comparisons, not fresh live-input traversal testing. No clutter or room changes; no commits.

## Shop room-scale art test — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-010 | Counter detail outpaced room construction/material consistency. Isolated ShopWorkflow10 reuses Counter09 and reconstructs medicine/records cabinets, inside joinery and coordinated finishes, retaining original stock and room layout. | Manual artistic review pending; partial success. Better construction/cohesion, but still below illustrated-reference richness. Flat glazing, repetitive forms, simple props and insufficient individually authored surface history remain. No Production02 rollout. |

Sources, comparisons, costs and validation distinctions: `../../../Interiors/CrookedMortar/ShopWorkflow10/README.md`. All 116 colliders unchanged, static full door sweep and nearby capsule probes pass. No fresh live-input interaction/stair test or manual camera approval. Counter LOD/quiet-panel reduction and floor bevel budget are documented opportunities, not completed optimizations. No added loose clutter or commits.

## Entrance architecture test — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-011 | Entrance inner stone ring and lime/timber connections lacked fitted construction. Workflow11 adds coursed radial masonry with mortar backing, fitted lime spandrels, selected chips, housed timber/scarf joinery and dedicated illustrated stone paint. | Separate EntranceWorkflow11 review only. Construction improves; gameplay-distance artistic improvement is restrained and still below illustrated-reference richness. Manual artistic review pending; no production rollout. |

Evidence: `../../../Interiors/CrookedMortar/EntranceWorkflow11/README.md`. 17,644 new triangles, all 116 colliders unchanged; 43 static door poses/190 capsule samples pass; matched painted and clay Play-mode captures. No fresh live-input traversal/camera-comfort test. Straight frame character, repeated wood and individually authored surface history remain limitations. Production02/prior workflows protected; no commits.

## Crafted shop room test — 2026-10-25

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-012 | Workflow11 entrance still sat within a sparse, regular shop composition. Workflow12 reshapes the medicine/records cabinets, adds fitted window apron paneling and curved timber bearings, and uses dedicated limewash paint plus one existing local fill adjustment. Existing stock/counter/layout retained. | Isolated `CM_CrookedMortar_ShopWorkflow12_Review`; manual artistic approval pending. More coherent/warm and readable, still below reference richness. Flat glazing, simple stock and repeated grain remain. No Production02 rollout. |

Evidence: `../../../Interiors/CrookedMortar/ShopWorkflow12/README.md`. Four new modules,25,432 triangles; old cabinet visuals replaced only in review. All116 colliders unchanged,43 static door poses/190 capsule samples pass. Live existing-controller route passes E-key opening, both threshold directions, customer/staff/records approaches and kitchen doorway. Full stairs regression not repeated for this local art pass. Nothing committed or pushed.

## Workflow13 reference-led shop reconstruction — 2026-10-27

| ID | Finding / action | Status |
| --- | --- | --- |
| CM02-ART-013 | Workflow12 still lacked substantial fitted cabinetry, authored material hierarchy and a weighty service counter. Workflow13 reconstructs the medicine display/case, records case, shop framing and counter body; adds dedicated paint/labels and review-scoped Forward+ matte shading/daylight. | Separate `CM_CrookedMortar_ShopWorkflow13_Review` only. Completed frontage is more coherent; full illustrated reference quality remains unmet. Rear wall artistry, individual stone character, glazing/exterior and retained simple furnishings remain outstanding. Manual artistic approval required before integration. |
| CM02-QA-013 | Focused input traversal could not start. A temporary cloned-input-settings test confirmed E-key/full opening but movement was correctly blocked by TraversalInput's explicit Application.isFocused guard. | Fresh focused walking smoke test remains outstanding. Original settings restored; no shared gameplay changes. Static full door sweep and local capsule clearances pass. |

Evidence: `../../../Interiors/CrookedMortar/ShopWorkflow13/README.md`. Five new modules total65,836 triangles; all116 colliders and earlier scene/source hashes preserved. Corrected cabinet fitting and counter backing/outward normals inspected in actual Unity views. No missing mesh/material/script references or shader compilation errors. No commits/pushes.

## Workflow14 fixed-layout reference elements — 2026-10-27

| ID | Finding / action | Status |
|---|---|---|
| CM02-ART-014 | Actual shop layout mapped before translating the new illustrations. Isolated14 adds individually dressed entry masonry, seated stair tread/nose/riser visuals, fitted window leads, new walnut/lime/stone paint and corrected stone-floor UVs. Counter/case construction and all functional datums retained. | Candidate only; manual artistic review pending. Better material read and fitted construction, still below the illustrations' individuality and light/shadow hierarchy. Repeating grain, regular stock and retained adjoining surfaces remain limitations. No Production02 rollout. |
| CM02-QA-014 | Live existing-controller route covers E/opening, shop aisles/kitchen passage and U-stair ascent/turn/descent, with unchanged116 colliders. | Passed23 targets; zero camera overlap samples.1 camera emergency correction; automated visibility is not manual comfort acceptance. No gameplay/camera tuning in this pass. |
| CM02-OBS-014 | Upper stair inspection reveals a green background/opening region and ceiling seams in BOTH committed13 and14 matched views. Exact object/cause not confirmed. | Pre-existing observation, not repaired in this localized art pass. Targeted upper-landing construction inspection recommended separately; do not infer a newly introduced floor/collision failure from this image alone. |

Evidence: `../../../Interiors/CrookedMortar/ShopWorkflow14/README.md`, ReferenceElementMap.md and matched Previews/Comparison. New module triangles50,069 (includes retained floor/lime surface geometry). Production02 and all previous assets/sources remain unchanged; no commits/pushes.
