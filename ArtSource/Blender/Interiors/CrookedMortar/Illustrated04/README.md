# Crooked Mortar — illustrated composition pass 04

## Reference and intent

The two supplied Crooked Mortar illustrations guide craftsmanship, botanical identity, varied working collections and meaningful layers. They are not floor plans or inventories. The production building's rooms, dimensions, roof silhouette, windows, stairs, camera, player and door systems are preserved. No shutters were reintroduced. This pass remains subject to manual artistic approval.

The before images exposed large triangular-looking plaster colour fields, simple counter/shelf profiles, isolated papers and sparse visible planting. Work targeted the full counter/records/preparation composition and front facade, rather than a larger unrelated asset catalogue.

## What changed

- Customer-facing counter panels now have painted botanical carving, a central mortar emblem, fitted mouldings and a woven runner. Side panels sample different botanical areas rather than repeating the central emblem. Existing drawer access, dimensions and functional markers remain.
- Existing medicine shelving has shaped knees and beaded edges. Two stock courses are replaced scene-locally by curated books, bound records, prepared orders and vessels; two old courses remain inactive and recoverable. Shelf structure and reusable source prefabs are unchanged.
- Botanical working archives occupy verified solid jambs and preparation wall faces. Carved jamb stiles and lintels finish connections between the rooms. Paper is fixed to rails with explicit pins. No picture was placed across the stair opening.
- Preparation gains fitted drawer decoration, records and wrapped orders on the existing side table, a botanical hanging, woven floor mat and a window lining fitted to the measured existing elliptical arch. Existing bench, press and craft work surface remain usable.
- Selected shop/preparation plaster renderers use a new matte material and an actual painted brushwork texture crop. Original approved shared materials are unchanged. No exposure, lighting, bloom, blur, fog or camera adjustment was used to produce the comparison.
- Front gable fan braces, carved bearing details, a botanical emblem and window consoles are fitted cosmetic meshes. A painted walnut sign face replaces the simple sign illustration through a new scene material; the existing backing and supports remain.
- Approved ivy components are reused selectively along facade timber. The same generic root-height assumption buried all eight window inserts by 0.13–0.14 m. All eight were checked and seated on actual existing planter soil triangles (WindowPlantingDatums.json), correcting the repeated datum error scene-locally. A west-wall herbal banner and limited limewash repairs provide secondary interest.

## Painting placement diagnosis

The earlier herbarium board was placed in the open stair passage because an installer assumed the west wall continued past z=2.2. It was not a coordinate-space conversion problem. The preceding LivedIn03 pass moved it to the solid shop/kitchen jamb and corrected that installer. This pass inspected the saved result and rechecked nine back-plane points against the actual visible wall mesh: approximately 3 mm clearance. It was already correctly mounted at this task's start; it has not been moved again or given an indiscriminate collider.

Previously repaired racks, plaque and cupboard support were rechecked. New wall rails, banners, jambs and lintels also have multi-point visible-mesh support reports. Front planting root burial was an additional confirmed defect, corrected in this pass. A pre-existing order parcel on the stair-side circulation floor was moved onto the records shelf with verified surface contact (ParcelSeat.json).

## Editable sources and reuse

- `CM_Illustrated04.blend`, `build_illustrated04.py`: metric, UV-mapped fitted ornament and room composition meshes. Existing modeling/export helpers and painted walnut/sage materials are reused.
- Unity additions: `Assets/BlightBloom/Art/Interiors/CrookedMortar/Illustrated04/`.
- Paint sources: `ArtSource/Paint/Interiors/CrookedMortar/Illustrated04/`. The unmodified imagegen atlas/sign masters, exact prompts and repeatable plaster-crop script are retained. These are real albedo images; no reference image is projected into the scene or substituted for a screenshot.
- The established FBX conversion remains metre scale, +Y up / +Z exterior. Only revised/new exports were re-exported after iteration; approved kits were not regenerated.
- `InstallIllustrated04.cs`, `FinishIllustrated04.cs`, `ApplyPaintedSurfaces.cs` are installation records, not idempotent rebuild commands. Do not rerun them over the saved scene. Production02 has scene overrides that must be inspected first.

## Visual review

`Previews/Before` and `Previews/After` are actual Unity ScreenCapture Game-view PNGs using the normal player camera and visible avatar. `GameViewPoses.json` records baseline camera position, rotation and field of view. After views pin the same camera transform only while capturing, then restore normal operation. No observer-camera render, paint-over or image generation is used for gameplay evidence. Comparison contact sheets label before/after; originals remain unretouched.

Views cover front exterior, exterior three-quarter, shop, counter/shelves, stair transition, preparation, preparation bench and the mounted records alcove. Close craft views supplement gameplay-scale evidence. Original before frames were captured before installing this pass, without rolling back the saved scene.

## Validation and limitations

`SourceValidation.json`, `IntegrationValidation.json`, `ExistingSupportValidation.json`, `NewSupportValidation.json` and `PlantingSeats.json` record targeted checks. All 116 baseline colliders retain their definitions, transforms and activation. No new colliders are added to this cosmetic pass. The 105-degree outward door sweep has 43 sampled poses with no intersections against the new ornament. Unity import has complete UV/normal arrays and no missing scripts/materials.

A mirrored corbel n-gon caused two importer warnings during iteration; the source polygon was corrected and reimported without repeating that warning. Pipeline request timeouts during import were automation errors, not C# compilation failures. Current Console and live gameplay results are recorded below when testing finishes.

The result is richer, especially in the counter's illustrated surfaces and wall working displays, but it does not reproduce the reference's density or bespoke carved sculpture. Much timber still shares the previous relatively straight grain. Plaster around some large fields and the broader exterior remain simpler; the surrounding village, background landscape and reference fireplace are outside this task. Roof geometry and its approved material were deliberately preserved rather than risk a new roof iteration. Decorative annotations are illustrative, not verified readable medical text. Manual artistic and camera-comfort approval is still required; technical tests cannot establish it.

### Final live-test status

The sequential room/door/stair/locomotion suite waited 150 seconds for Unity focus and did not start. It was rearmed after the user replied ready, but desktop access still reported a locked Mac and the second attempt also timed out before starting. Desktop access confirmed the Mac was locked. Its waiting callback and temporary input device were removed safely. No live regression pass is claimed. Multi-point placement, import, mesh/UV/normal and door-sweep checks are independent of this blocker and passed. Manual navigation and artistic review remain necessary.

No commits or pushes were made. Prior uncommitted LivedIn03 and HeroRefinement02 work remains preserved; this pass adds Illustrated04 assets and edits only Production02 plus the existing issue tracker. `ChangedFiles.json` distinguishes this pass's exact paths from pre-existing work.

Close entrance views also reveal existing sky slivers at the stone/timber surround transitions. That original architecture was not changed in this cosmetic pass and needs a separate fit review; these are not claimed resolved. The current Console retains one Pipeline request-timeout error and two historical corbel importer warnings; the polygon was corrected and reimported without a new warning. Compilation is not failing.
