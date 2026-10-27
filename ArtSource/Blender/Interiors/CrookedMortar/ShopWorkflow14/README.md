# Workflow14 — fixed-layout reference-element reconstruction

Review scene: `Assets/Scenes/CM_CrookedMortar_ShopWorkflow14_Review.unity`.
Baseline: clean committed checkpoint **c597269**, saved Workflow13 review. The two new illustrations are appearance references only. `ReferenceElementMap.md` records the actual layout before editing. No illustrated staircase, balcony or extra room has been invented.

## Element translation

- **Entrance:** individually authored radial voussoirs and dressed jamb solids, wider softened arrises, shallow broad chisel facets, quiet per-block tone variation, actual stone returns and continuous recessed lime bed. Inner radius1m, spring1.92m and existing door/outer stone are retained. The new intrados bedding is set back12mm to eliminate the coplanar sawtooth artifacts exposed by the first preview. This is a new visual mesh, not a cover arch over the old renderer.
- **Timber / cabinetry / counter:** existing shaped Workflow13 members, housing rebates, fitted registers, drawer construction and three registered Workflow07 relief fields remain. A new dedicated walnut paint replaces the highly streaked surface. Native geometry and fixed furniture transforms are retained. Palette and brush scale are coordinated across ceiling, fitted entrance timber, counter, medicine case and stair guards. No new jars, herbs or clutter.
- **Plaster:** actual retained lime surface triangles are exported with explicit physical-scale UVs. A review-scoped derivative of the proven Forward+ shader samples painted lime continuously in world space, with restrained base/head shading; selected existing shop doorway and lobby-return renderers share this finish. No wall position or opening changes. Stairwell walls beyond the selected shop return remain baseline materials.
- **Floor:** the EXACT existing flagstone triangles are reused with a dedicated gouache limestone map and corrected stone UV projection. Its old stretched streaks read like wood; the replacement reads as stone. Rug/runner transforms are unchanged. No new carpet or floor height.
- **Windows:** retained paired frame/glazing transforms and dimensions; eight fitted lead members articulate the two existing rectangular lights. No shutters or new openings. Existing transparent amber glazing remains. Empty exterior/cyan background is not replaced with the illustration.
- **Staircase:** existing rear-left U-turn retained: nine lower rises toward rear, landing at1.9m, nine upper rises returning toward front at3.6m. Only visual treads are replaced: fitted boards, rounded dressed noses, seated closed risers and lower side fields at exactly the existing tread-top datums. Original collision, stringers, open guards, upper landing, direction and destination are unchanged. The source includes shallow riser rebates rather than open butt gaps.
- **Lighting:** existing local window spot reduced3.6→2.6, same position/direction, to retain detail around front reveals. Global illumination/render settings, fog, bloom and grading unchanged. No added light or fixture.

## Editable assets and method

`CM_ShopWorkflow14.blend`: metric native scene, separate editable components and joined export meshes, packed painted images. `build_shop14.py` is a scoped reproducible candidate builder using established Workflow08/10 profile/UV/export helpers. It reads measured scene geometry, never generates collision or architecture layouts. Blender's +Y-native depth transport follows established Unity +Y-up conversion (export-copy Z rotation, FBX -Z forward/Y up, metric1).

`MeasuredStairs.json` / `MeasuredSurfaces.json` preserve the read-only scene measurements; `PaintedTimberLime.png` and `PaintedStone.png` preserve full generated painting sources. Production crops and Blender textures live in the new asset folder; `Prompts.md` records generation provenance. No normal-map noise, photographic textures or painted screenshot backdrops.

Five reusable FBX/prefabs:

| Module | Triangles |
|---|---:|
| DressedEntrance |13,344|
| StairTreads |18,612|
| FlagstoneFinish (existing geometry, new UVs) |12,600|
| RegisteredLime (retained surfaces, new UVs) |3,881|
| FittedWindowLeads |1,632|
| **Total installed candidate meshes** |**50,069**|

These replace22 original visible renderers rather than add duplicate render surfaces. Five joined renderers, six material submeshes across the new modules; no GameObject per block/board. Existing shared-shader texture grouping remains useful but visible materials introduce additional batches. Three new albedo maps (two1024×2048, stone native resolution), uncompressed review imports, mirrored edge sampling. No LOD/compression tuning or GPU profiler capture was performed; native source contains duplicate editable/export representations, so its total is not the runtime triangle count.

`ImportAndInstall.cs` and `FinishMaterials.cs` are execution records and must not be blindly rerun on the installed scene (material override lists are stateful). The source generator exports only this new asset family. Prior workflows and Production02 are read-only.

## Comparison / artistic assessment

`Previews/Comparison`: matched Entrance, Shop, EntranceOpen, StairBottom, StairTurn, EntranceClay and Gameplay pairs, left committed13 / right14. Captured with the actual Unity camera in Play mode at identical fixed poses/FOV, no editor gizmos or paint-over. Gameplay view includes the existing avatar; inspection views hide it temporarily and restore it. Clay pair uses the same local light intensity and material. The four preliminary map captures were made in Edit mode; final paired views are runtime camera renders. These are presentation captures, not evidence of player-input traversal.

**This is a visible surface/construction improvement, not attainment of the reference's full artistic quality.** The floor no longer reads as planking, the arch reads as worked stone, lead divisions add window scale, and stair noses/risers have real depth. The clay pair also shows the limits honestly: most larger silhouettes already come from13, and the arch change is restrained. Walnut knots still repeat across members; shelf vessel families remain regular; plaster/stone need more individually directed maintenance and edge painting. Existing character and adjoining room surfaces are less refined. The references' integrated light/shadow hierarchy, masonry individuality and wholly authored furnishing rhythm are not fully matched. More loose clutter would not resolve this. No claim of an approved art benchmark or automatic Production02 integration.

The upper stair inspection also exposes a green opening/background region and ceiling seams already present in the matched baseline13 view. This task does not conceal or remodel those unrelated upper-floor elements; record separately for structural inspection if visible during manual play.

## Validation

See SourceValidation.json, IntegrationValidation.json, ClearanceValidation.json, SavedScopeValidation.json and CaptureValidation.json. Live-input result and final scope/Console status are recorded separately at handoff. Automated static checks do not establish manual camera comfort or artistic approval.

### Final validation results

- Source validation passes141 editable/export mesh objects (native source total100,138 triangles includes duplicates); finite UVs/coordinates/normals, one UV layer each, zero degenerate triangles. Five imported modules total50,069 triangles, complete imported normal/UV channels.
- All116 original collider serialized records, matrices and active states are identical; no new permanent colliders. The first comparison utility incorrectly matched duplicate-named bearing pads; matching also by their matrices resolved this validation ambiguity. No colliders were altered to make the test pass.
-43 actual leaf collider poses across105° outward swing clear the new visual meshes.190 static capsule samples clear entrance, both counter aisles and connected passages.
- **Focused real-input Play test passes23 route targets**, including E/full door opening, outward/inward threshold, customer/staff/records approaches, kitchen passage, lower ascent, intermediate turn, upper ascent and both descents. Temporary device events feed existing input actions and normal motor/camera updates; no direct animation/door method calls or route teleports. One initial test pose only. The cloned unsaved InputSettings object and both temporary devices are removed/restored. Existing playerheight2m/radius.4m unchanged.
-324 route visibility samples:zero camera overlap samples, minimum2 of4 body sample points visible;1 existing camera emergency correction. This is quantitative route coverage, **not manual camera-comfort approval**, and no camera behavior was changed.
- Saved YAML scope check passes: no original gameplay-script/camera/CharacterController/physics record changes. New scene changes are renderer/prefab visual overrides, one local light adjustment and new art root. All original tracked-file hashes remain unchanged except the explicitly updated issue-tracker documentation.
- Final Unity Console:0 current errors/0 current warnings, no compile failure; new shader has0 compiler errors. An initial Pipeline inspection request timed out and was retried with a longer timeout; one inspection snippet had a syntax diagnostic and was corrected. These were automation diagnostics, not gameplay compilation failures. No Console history was deliberately cleared.
- Not repeated: garden/upstairs room regression, sprint-specific locomotion validation, GPU profiling, manual artistic approval or subjective camera-comfort acceptance. None of those systems were edited.

Workflow14 remains isolated and saved for review. Production02, previous reviews, source workflows, approved kits, scripts, player/camera/door and project/package settings remain unchanged. Nothing committed or pushed.
