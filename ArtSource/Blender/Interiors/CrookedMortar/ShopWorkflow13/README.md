# Workflow13 — reference-led shop reconstruction

Review scene: `Assets/Scenes/CM_CrookedMortar_ShopWorkflow13_Review.unity`.
Based on the saved Workflow12 scene. Production02 and all earlier scenes, asset libraries and Blender sources remain intact. Nothing committed or pushed.

## Completed coherent section

The medicine-wall / counter frontage and its surrounding timber finish are reconstructed. This is a new set of fitted visual assets, not additional loose ornaments:

- Tall fitted medicine case, authored as continuous shaped standards, six structural shelf datums, an arched upper register, swept cornice and eight recessed remedy drawers with modeled pulls. It occupies the old cabinet footprint and uses existing stock-bearing levels, extending into unused height below the ceiling. The rear upper register steps down around the existing cross-tie; individual rebates accommodate retained timber without missing shelf faces.
- Replacement medicine display:20 purpose-made lathed vessels, rolled mouths, corks and curved, registered botanical labels. Six herb identities share a painted label atlas. This replaces the old stock courses/working collections instead of stacking more clutter on them. Two top-register reference folios provide a quiet functional detail.
- Fitted records cupboard with shaped cheeks, curved crown and bearing aprons. Original Robert records remain at their saved mounting datum.
- New principal tie, continuous standards, curved housed bearings, ceiling joists and fitted treatment/kitchen opening frames. Earlier thin beam/joinery batches are disabled in this review. No opening or route is moved.
- New substantial service counter body, four engaged bearing standards, curved plinth/rails, inset end fields, service drawers and three integrated relief fields. It reuses the successful shaped top and deliberately registered Workflow07 sculpt artwork, not the old light table-like counter body. The previous counter remains recoverable and disabled only in this scene. Countertop datum remains1.0525m above its pivot, footprint2.28×.78m; existing station markers/dressing/interaction placement remain on their original roots.
- Dedicated painted walnut and vessel/sage/paper atlas; registered carving paint is reused from Workflow07. Existing fitted window paneling, plaster and entrance stone survive with review-local material coordination. Plaster UV scale is adjusted; no additional room is invented.

## Reference adaptation and remaining artistic gap

The concept's broad wall of cabinetry is adapted to the existing narrower medicine bay, with the door, windows, stairs and staff/customer aisles retained. A new ladder, fireplace, rear arched room, outside village or wider counter would conflict with the actual layout and has not been fabricated for a screenshot. No shutters were added. Existing rugs, runner, records and herbs are retained rather than multiplied.

**Result: stronger fitted-shop identity and warmer, more coherent materials, but not a faithful recreation of the reference's artistic quality.** The taller case and closed service-counter mass change the visible construction; the clay pairs demonstrate that this is not a texture-only change. The label artwork is a clear improvement over generic containers. Nevertheless, the room remains more regular and sparse than the illustration. The reference's individually shaped stone, individually authored wood edges, broad cabinet-wall composition, integrated botanical history and soft directional atmosphere are not fully reproduced. The empty exterior/solid camera background and simple retained glazing are conspicuous in the open-door view. Existing character, rugs and nearby furnishings also limit cohesion, but were outside this reconstruction.

This pass prioritizes a completed coherent frontage over claiming a finished whole-shop reference match. The rear shop walls and retained entrance masonry would require a further authored mesh/paint pass; do not present this candidate as approved or roll it into Production02 automatically. More small props will not resolve those gaps.

## Sources, methods and cost

`CM_ShopWorkflow13.blend` contains separate editable parts and joined game exports. Source workflow: reference-led continuous cross-sections/Bezier profiles, lathed vessel families, actual recessed construction and registered scalar-field relief with curvature reduction. Workflow08/10 helper/export code transports these new designs; prior asset files are read-only. Texture sources:PaintedWalnut.png, PaintedVesselAtlas.png and HerbLabels.png; prompts/provenance in Prompts.md. Paint is mapped onto actual geometry, not used as an image backdrop or screenshot paint-over.

Five reusable FBX/prefabs under `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/`:

| Module | Triangles |
| --- | ---: |
| FittedApothecaryCabinet |14,944|
| RemedyDisplay |11,056|
| RecordsCase |5,084|
| StructuralJoinery |5,712|
| ServiceCounter |29,040|
| **Total new modules** |**65,836**|

The prior counter alone was77,390 triangles. Five joined new renderers replace the listed old renderers in PresentationStates.json; there is no GameObject per vessel or timber part. Costs exclude retained room/player geometry. No GPU draw-call/overdraw profile or LOD production was performed.

The small review-scoped `PaintedInterior` shader uses URP's standard Forward+ lighting path, matte response, controlled indirect light and broad baked vertex cavity. No bloom, fog, exposure or global render-settings change. One local window-daylight spotlight is added; the existing shop fill is adjusted from1.65 to1.3 and slightly warmer. The initial custom light loop did not support the project's clustered Forward+ renderer; it was corrected to URP's own lighting function before final captures. These are real lighting/material changes, not a post-process painted filter.

Source scripts are stateful execution records, not blindly repeatable generators. SeatCabinetJoinery.py is a rejected compound-cutter experiment, explicitly disabled; it removed shelf faces and is not the delivered geometry. RepairCabinetFit.py restored the cabinet and fitted it against separate closed structural members. CorrectCounterNormals.py repairs the outer relief fields after backing adjustment; CounterNormalValidation.json verifies outward front normals for all three. `build_shop13.py` establishes the four fitted modules; BakeCavity.py bakes low-frequency cavity only onto those joined meshes. ReconstructCounter.py adds the counter using the preserved shaped top and scalar relief artwork; FinishCounterSupport.py/FitCounterFields.py make one-time support/backing corrections. Do not repeatedly run the adjustments on the final source. SyncPaintSource.py packs the final surface atlas for Blender editing. Source artist materials approximate the Unity lighting shader; Unity is the final review renderer.

## Visual evidence

Previews/Comparison contains exact matched before/after camera/FOV pairs:EntranceWide, CounterGameplay, WorkingSide, CabinetClose, EntranceOpen and RoomClay. Baseline is the saved Workflow12 appearance. Colour pairs include the documented local lighting changes; clay uses identical baseline lighting and neutral materials. The open and closed door views demonstrate both states. Player views come from the unchanged orbit-camera setup; close/clay inspection views hide the avatar temporarily and restore it afterward.

Concept_EntranceWide.jpg and Concept_CounterGameplay.jpg place the original illustrated target beside actual Unity output. No scene geometry is hidden just for the final artwork; new and old variants are toggled only for the before/after comparison. The source concept is archived as ReferenceTarget.png. These comparisons are for critical assessment, not evidence of equivalence.

## Validation and scope

- SourceValidation.json: finite coordinates/normals/UVs, one UV layer per mesh, zero degenerate triangles; metric source and established Unity axis conversion.
- IntegrationValidation.json: imported mesh channels complete; no missing materials/scripts; all116 original colliders unchanged, no added permanent colliders;43 full outward door-swing poses clear against the new visible meshes.
- ClearanceValidation.json:190 dense capsule-volume samples pass entry, customer/staff aisles and stair/kitchen connections with unchanged2m/.4m controller dimensions.
- The first live test could not obtain application focus; FocusBlockedAttempt.json records its cancellation. A follow-up test used a cloned, unsaved InputSettings object allowing queued events while unfocused, and restored the original settings object/content afterward (settingsRestored=true). **E-key opening passed, but the movement route did not run**: TraversalInput.Update explicitly clears Move whenever Application.isFocused is false, so the unchanged player remained at its initial position and the first route segment timed out. No gameplay focus guard was bypassed. This is an incomplete walking test, not a navigation pass. See RoomRouteValidation.json; a fresh focused manual/input-driven walking smoke test remains outstanding. No direct route Move calls or action/door method invocation were used.
- SavedScopeValidation.json compares saved scene records; original gameplay script/camera/collider records remain unchanged. ProtectionValidation.json checks prior scene/asset/source hashes against the task-start state, including the pre-existing modified stone material.
- A counter backing overlap discovered in clay/close views was corrected internally so outer relief fields are unobstructed. Four bearing standards support the service carcass; shelf/vessel bottoms meet their load datums. No additional gameplay collision is introduced by art.
- Full upstairs/stairs regression, human camera-comfort acceptance, and production-wide profiling were not repeated for this localized visual reconstruction. Relevant local routes and entrance clearance are the validation scope.

Leave this separate review scene open for manual artistic review. No changes to Production02, shared gameplay, project settings or reusable approved kits. No commits/pushes.

## Final handoff notes

Final state: saved, stopped, one loaded scene; player/input/motor/orbit camera/door enabled; no temporary input devices or missing visible meshes. All293 protected hashes match the task-start baseline, including the pre-existing stone-material working-tree modification. Native Editor log entries were empty at final inspection; Pipeline reported0 current errors, no compile failure and2 retained warning counters, with no new captured warning entries or matching recent shader/compile/shadow warnings in the Editor log tail. The local capture snippet initially had a missing Quaternion argument; that automation-only compilation diagnostic was corrected and is not a gameplay script failure. Console history was not cleared.

CounterConstructionClose.png is an additional direct Unity-camera inspection proving that all three relief fields now render outward; no paint-over. Final fitting uses individual structural solids, and the rejected compound-cutter file is guarded against execution. Remaining art limitations and the failed focus-dependent walking test are deliberately retained in the reports.
