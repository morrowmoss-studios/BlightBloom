# Crooked Mortar — shop room-scale workflow test 10

Open **`Assets/Scenes/CM_CrookedMortar_ShopWorkflow10_Review.unity`**. It is an isolated copy of Production02. Counter09 is a review candidate only, not installed in Production02. Original architecture, furniture and sources remain recoverable. No changes to other rooms, floor plan, stairs, player, camera, interactions, shared gameplay/settings or approved kits.

## Plan and implemented scope

The baseline mixed simple thin shelving, striped timber atlas samples and flat room illumination with an increasingly detailed counter. The plan prioritized a coherent walnut/ivory/sage construction language, cabinet depth, fitted inside finishes and deliberate visual rest instead of additional stock.

- Reused the Workflow09 counter prefab unchanged as the hero.
- Reconstructed the existing medicine shelving as a fitted cabinet with continuous shaped cheeks, chamfered uprights, short bearing knees, separate inset sage back boards, shaped shelf noses, lower storage fronts and a restrained continuous crown. Existing stocked courses remain in their original positions. Their contact points are approximate to within about 1cm; this is not a final shelf-contact polish pass.
- Rebuilt the small wall records cabinet at its existing datum. Robert's original casebooks, bottle, index artwork and records were extracted from the old joined mesh and retained, not supplemented with more clutter. Connected-component classification welds FBX split vertices before removing structural boards, cheeks and pegs. Eleven original structural components are removed from this derived contents mesh; the original asset is untouched.
- Replaced the shop tie beam, added coordinated interior joinery and ceiling joists, and fitted doorway trim to existing openings. These are nonstructural visual meshes; original collision-bearing architecture remains authoritative. No alterations to the stair or doorway clearances.
- Applied new painted plaster only to inside-facing triangles copied from the actual saved walls. Openings are preserved; exterior and opposite room faces are unchanged. Ten inside-face finishes are batched into one renderer. Original individual fitted mesh sources are retained for editing.
- Added a joined shallow flagstone finish within the shop footprint. The visual top is 3mm above the original continuous collision floor. Stone UVs are projected within each slab without wrapping across polygons. Its palette was darkened after the first review because the initial pale floor competed with the counter.
- Tuned only the existing shop fill: from white, intensity 1.3/range 6 at (2.7,2.8,2.2), to warm ivory, 1.15/range 4.6 at (1.55,2.78,1.15). Global lights, exposure, bloom, fog and URP settings remain unchanged. No additional lights or shadow maps.

## Reusable art methods and editable files

`CM_ShopWorkflow10.blend` retains the editable cabinet, records shelving, timber, joists and individual stone sources, plus joined export copies. `build_shop10.py` reuses the Workflow08 mesh, bevel, grain-UV, profile and export helpers. Cross-sections, shaped cheek outlines, curved shelf edges and varying recess depth provide construction rather than loose applied ornaments. `FinishAssets.py` applies only the targeted cabinet/floor corrections to the saved new source and exports those two modules; unchanged modules are not regenerated.

Workflow09 walnut/iron materials are shared directly; its counter and sculpt are not rebuilt. One new gouache plaster/stone atlas supplies broad pigment variation, paired with a matte sage material. Painting source: `PlasterStonePaint.png`; prompt/provenance in `Prompts.md`. No photographic noise, normal-map surface trick, new carved jewelry, software installation or paid external service.

New FBX, five reusable prefabs and materials are under `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow10/`. Unity-native fitted finishes/retained contents are editable mesh assets in `FittedMeshes/`. Metres, Unity +Y up/+Z front and zero pivots use the established export conversion.

The external C# files are **stateful execution records**, not a general one-click regeneration tool. Read them before execution. The initial monolithic installer timed out and is preserved as `InstallReview_Superseded.cs.txt`; do not run it. Its completed import/prefab work was inspected before continuing in smaller furniture/surface/light stages, then `RepairRecordExtraction.cs` and `BatchPlaster.cs`. Duplicate-install guards and current scene state must be respected. No new compiled Editor/gameplay scripts were added to Assets.

## Evidence and critical assessment

`Previews/Comparison` pairs Production02 left / review right from three useful player-camera viewpoints (`CounterArrival`, `WorkingSide`, `RoomConnections`), plus `CabinetClose` and `RoomClay`. The camera poses, FOV, original dressing and global rendering conditions match. The intended local fill adjustment is included in the colour comparisons. Clay uses the original fill for both versions and neutralizes affected shop surfaces; adjoining rooms/exterior and door remain context, not fully clay-rendered.

These are actual Unity Play-mode Game-view screenshots, with no gizmos, paint-over or generated beauty image. Player and camera placement, light and material overrides used for capture are restored afterward. Player-camera views are not input-driven route playtests.

**Result: a meaningful cohesion improvement, but only a partial success against the artistic target.** Cabinet depth, more consistent wood, quieter plaster and integrated counter improve the working-shop read without adding clutter. Original records, books, labels and herbs carry Robert's history. The new cabinet is better constructed but still comparatively regular; stone shapes and framing remain repetitive at room scale. Flat glazing, simple bottle/character silhouettes, and broad wall areas continue to weaken the rich illustrated illusion. There is insufficient individually authored surface history, shaped reveals and painterly edge treatment to claim the supplied reference quality. The room remains a review prototype, not an approved production rollout.

Future work should address those specific form/paint weaknesses with artist-directed meshes/UV painting. More jars, rugs or foliage would not resolve them. No broader reconstruction was started.

## Geometry/performance

Five new FBX modules total **30,712 triangles**: medicine cabinet 9,940; records cabinet 3,740; tie beam 580; room joinery 3,852; stone finish 12,600. Reused counter: **77,390 triangles**.

The visible replacement group totals **113,784 triangles across nine renderers and 18 material slots**, including original records contents and fitted surfaces. These are mesh/rendering submission counts, not measured frame draw calls. Unchanged room props are additional. Batching plaster saved nine renderers; no GameObject per stone or timber member. Two high-level counter-only sources dominate complexity: relief and excessively dense quiet panel grids. A counter LOD/bake and simpler curved-panel topology are the most valuable optimization candidates. Floor bevels could also be simplified. This pass investigated those costs but did not alter the approved candidate's sculpt budget or deliver LODs/GPU profiling.

## Validation and limits

Final source checks passed: finite geometry, normals/UVs, no degenerate triangles, metre scale and pivots. Unity import channels/references are complete; no missing scripts/materials. All **116 original colliders unchanged**, zero new colliders. **43 static full-swing door poses** and **190 dense capsule-volume probes** pass entry, both counter sides and nearby stair/kitchen connections. Existing markers and functionality remain on their original roots.

`SceneScopeValidation.json` confirms exactly five original shop renderers disabled for visual replacement, with no original renderer transform/material changes elsewhere. Protected hashes verify Production02 and all Workflow07/08/09 scenes, sources and assets unchanged. No commit/push.

No fresh E-key, walk/sprint, full stair-route input test or manual camera-comfort approval was performed. No new compilation errors. Pipeline timeouts occurred during installation/read-only operations. An additive baseline audit temporarily produced duplicate-audio-listener notices; the baseline was closed and final captures used only the review scene. The corrected scope audit closes its read-only scene in a finally block. These transient automation diagnostics are retained in `ConsoleValidation.json`; final scene has one active listener, no current errors and two pre-existing warnings. They are not presented as evidence of gameplay defects or ignored as successful tests.
