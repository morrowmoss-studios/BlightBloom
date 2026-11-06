# Briarwick Environment07 — medieval roads and footpaths

2026-11-05. **Saved candidate, awaiting visual approval.** Existing `Assets/Scenes/Briarwick_Hamlet_Dev01.unity` only. No Git commands, commits, pushes, branches, packages, project-wide rendering changes or architecture changes.

## Scope and inspection

Inspected the original road-building/refinement scripts, current meshes/materials/colliders, Layout.json, Terrain layers, Environment06 Revision01 rendering evidence and current scene. The network has14 route ribbons:245m main alignment including the18m placeholder bridge, plus317m of approaches/footpaths, approximately563m of mesh alignment, plus the existing35 m terrain-painted gathering-grove continuation (approximately598m combined). Existing widths are preserved: main5.2m (4.8m near the bridge), farm3.2m, Miller2.8m, inn/forge2.6m, ordinary approaches2.4m and graveyard/herb-garden2.2m. These are original planning/alignment measurements, not a redesigned network.

**Structural objects retained:** all14 original MeshColliders and their original mesh assets, all original transforms/route vertices, bridge deck/guards/supports, and TerrainCollider. Earth ribbons are not disposable presentation objects: they provide walkable surfaces. Their original materials and meshes remain recoverable.

**Visual replacements:**14 earth ribbon MeshFilter references and the common's visual mesh now use owned copies with an extra UV channel for cross-road/radial feathering. Original vertex positions, normals, UV0 and triangles match exactly. The common is a visual activity-reserve surface, not a structural floor collider. No original object or asset deleted.

Original earth meshes sat mostly7–8cm above Terrain; some original bridge-approach edges reached61cm above it. Hard opaque borders, separate overlapping strips at junctions, abrupt common boundary and texture repetition made them look placed on top. Existing UV0 was world-position based; retaining world-aligned sampling lets all intersections share the same earth texture without discontinuities.

## Implemented treatment

- Refined **all14mesh routes, the village common and existing35 m grove continuation**, covering every established building approach plus graveyard and apothecary garden. No major earth route retains the old opaque placeholder treatment. Bridge wood/deck remain deliberately unchanged, as requested.
- Reused the owned low-contrast `BW_Muddy_Soft.png` and existing `BW_Revision01_Muddy.terrainlayer` (slot7). Embedded small stones, earth and fine organic surface detail come from that existing softened texture. No imported material or image was repainted. No new texture or TerrainLayer is used.
- Added one small, project-owned **URP road-edge shader**, with world-aligned earth sampling, broad low-contrast tonal variation, irregular alpha-feathered margins and restrained visual wheel wear on rural cart sections. Footpaths have wider relative feathering; common uses radial edge data; farm/main road retain the more substantial cart-road center. Ruts are visual shading only, not collision trenches.
- Matching Terrain soil paint extends through junctions and irregular margins, with grass still contributing around secondary paths. Common soil and route masks form a continuous union rather than stacked rectangular patches. No additional grass, decals or clutter hide the borders. The final network cross-check identified the Woodland03 continuation as Terrain paint rather than a mesh: (-28,95) → (-25,103) → (-24,112) → (-26,120) → (-25,129). RefineGroveTrail.cs applies lighter soil wear to that same35 m route, tapering from the main-road endpoint, with no new alignment, geometry, collision or plant changes. TrailIntegration.json records1184affected texels in that separate bounded pass.
- Terrain alphamap resolution256→1024 for approximately31cm paint texels, preserving the eight existing layer references/tile settings and both native Terrain material passes. Prior paint was bilinearly upsampled and normalized; soil added only within the road/common masks (30,518new-resolution texels, approximately2,986m²). Terrain heights/detail data are not regenerated.
- Added a narrow fitted **earth-shoulder mesh** only beneath the original elevated bridge approaches.136 triangles, one renderer, **one new MeshCollider**. It meets the original road edge within4mm and slopes down into the unchanged Terrain. It is support for the existing ramp, not a new bridge or network alignment. Initial segmented gaps and a small edge drop were found and corrected; final eight transverse crossing tests show no ungrounded steps. Original road colliders remain unchanged.
- **No vegetation adjustments:** all six detail maps,22,914instances, prototype refs/dimensions/distance and prior disabled filler states remain identical. Approved trees and their colliders remain intact.

## Assets, cost and preservation

New assets:15 visual mesh copies (1,628 triangles replacing the same1,628rendered triangles), one136-triangle shoulder mesh, four shared materials (foot/cart/common/shoulder) and one shader. Total affected rendered road/common/shoulder geometry1,764 triangles, excluding the unchanged bridge. Net geometry+136 triangles; net renderer+1; affected material types1→4. Original mesh assets remain for collision and recovery, so visual copies add a small amount of mesh memory. AssetCosts.json records per-mesh native memory.

The new shader is a single forward PBR pass with main/additional lights, Forward+ cluster support, shadow reception and fog, inspected against installed URP17.4source. No global feature is disabled. It intentionally does not add shadow-casting/depth-normal passes to these thin ground surfaces. Feathering blends in the existing opaque queue with depth writes; intersection/margin views were inspected. Baked-lightmap, motion-vector, other platform/renderer and full standalone-build compatibility are not validated; review these before wider production reuse. It is a scoped road material, not a grass/terrain rendering framework.

Two1024²RGBA32 control textures have8MiB combined base-level pixel payload, versus0.5MiB previously; mips/CPU copies increase actual runtime cost. Unity reports21.3MiB combined object memory for the current control textures. No new terrain layer/pass or diffuse texture allocation was introduced. Larger paint resolution trades memory for convincing narrow margins.

Scene and TerrainData before-copies, scene-component snapshot, six detail maps, height/alpha binaries and layer/hash lists are saved here. Reverting requires explicitly restoring affected scene/TerrainData with Unity safely unloaded from those assets, preserving existing .meta/GUIDs; do not overwrite loaded assets blindly. All original route meshes/materials remain untouched and available. Generation order, if explicitly authorized later: CreateRoadAssets.cs → Integrate.cs → FitApproachShoulders.cs → RefineGroveTrail.cs; guards prevent blindly reapplying over the current scene.

## Rendering evidence

|View|PlayerLoop ms|Render thread ms|GPU counter ms|Draw calls|
|---|---:|---:|---:|---:|
|Common intersection|6.91 → 7.09|10.19 → 10.15|23.60 → 25.57|1,436 → 1,399|
|Main road|6.75 → 7.03|11.32 → 10.83|22.62 → 22.19|1,671 → 1,622|
|Bridge approach|7.10 → 7.48|12.22 → 12.32|22.05 → 22.68|1,902 → 1,884|

Authoritative first paired capture: ProfilePaired.json;40 samples following20 warmup frames per view/phase,240 valid nonzero triangle samples, all focused. Same actual Game view, camera, lighting, controller location and Editor settings. Before/after changes are confined to a disposable runtime TerrainData clone (256/1024paint), visual references/materials and new shoulder active state. Source assets/collision references are never rewritten for the comparison; all runtime state is restored.

These figures are **Editor-inclusive and mixed**, not standalone FPS or an established optimization gain. Draw submissions fall slightly (~1–3%), partly because thin-road shadow/depth passes are no longer drawn. PlayerLoop timings rise slightly; GPU medians range from a small improvement to a regression. Alpha feathering adds fragment work/overdraw and the paint resolution adds memory. Broad environment/building/tree costs still dominate.

That three-view capture preceded the final shoulder flush-edge adjustment (68→136 triangles). ProfilePairedBridge.json rechecks the final bridge candidate:40 samples per phase, valid nonzero triangle counters, reported draw calls1902→1882. Its GPU Frame Time counter returns0, so **no final-fit GPU time is claimed**. Common/main geometry/materials were unchanged by that adjustment. The final grove-only soil refinement has no extra renderer/layer/geometry and was not separately benchmarked. No GPU gain is inferred from triangle/draw-call counts.

The earlier independent ProfileAfter capture had0triangle/SetPass counters and stale draw statistics because the Game view was not rendering normally. It and its summary are explicitly named `*_Rejected_NoGameViewRendering.json` and excluded from conclusions. A paired test with explicit Game-view repainting replaced it. No further project-wide profiling/build was needed. Standalone build not repeated: prior build triggers writes to the five protected settings files; any new build needs that preservation issue addressed first.

## Validation

- Final Validate.json: **zero unexpected changes** to prior scene objects/components. Exactly30 allowed reference changes:15 visual meshes and15 materials. Original collider references unchanged; road vertices/triangles/normals/UV0 exactly match sources; all new edge UV channels complete. No missing scripts/materials or invalid active mesh data found.
- Terrain heights byte-identical; six native detail maps byte-identical; all eight layer references unchanged. Weights valid within eight-channel UNorm8 quantization tolerance. Buildings, trees, roads/bridge transforms, player/input/camera/animation component data preserved.
- SurfaceContinuity.json:3,935 support rays across every original road cross-section on five lanes, **zero unsupported samples**. Ray height changes include continuous slopes; they are not interpreted as discrete stair steps.
- PlayValidation.json:20 CC.Move route runs pass, including three main-road/bridge lanes both ways, woodland, country, farm and creek paths. BuildingApproaches.json:26 runs pass (all 11 building approaches plus graveyard and herb garden, both directions, stopping before static doors).
- ShoulderTraversal.json: eight final transverse shoulder crossings pass, grounded at end, **zero ungrounded probe steps**. The initial drop was corrected in the new shoulder geometry; no controller or original road collider workaround.
- LiveInputValidation.json: **passed** through unchanged TraversalInput→ThirdPersonMotor→Locomotion03 and orbit camera, using virtual gamepad/mouse events in focused Play mode. Twelve waypoints cover woodland, common/intersections, main road, bridge and country approach;235/235 samples grounded, Idle/Walk/Sprint, stopping, speeds3/6m/s and orbit response verified. This input test preceded only the final outer-shoulder flush refinement; the unchanged center route is covered, with final shoulder crossings tested separately. No manual playtesting or comprehensive camera-comfort approval is claimed.
- Shader compiler messages empty; current Unity Console0errors/0warnings, compilation not failed. Captured-log cursor64 unchanged from task start; old retained logs are not new errors and were not cleared. Historical Editor window-layout NullReference did not recur.
- Five protected settings (including UnityConnectSettings) and Production02 remain byte-identical. Final preservation evidence and exact file inventory are saved beside this report.

## Visual assessment and remaining limits

Road-to-grass transitions are substantially softer at player height, the common/junctions read as connected worn ground, and surface texture scale stays consistent across intersecting routes. The treatment is restrained earth/gravel, not decorative paving. All major earth segments received the pass; no intentionally unfinished brown road ribbon remains.

This is **not final artistic approval**. The network's original smooth geometry and shared8m soil texture remain somewhat regular; broad earth areas can still look generic, visual ruts are subtle, and feathering can reveal thin-surface depth differences at very low angles. The new causeway shoulders are deliberately simple, and their end shapes need visual review in the later creek/bridge pass. The bridge, cultivated plots, graveyard reserve, surrounding grass/sky and building roughness remain prior placeholders/limitations outside this scope. No props, vegetation or dramatic lighting were added to disguise them.

Review [GALLERY.md](GALLERY.md): eleven matched pairs (overview/common, Mortar frontage, main road, cottage path, woodland, country, bridge, edge, surface and grove continuation) plus runtime input-test captures. Scene saved and open in Edit mode. **Stop for visual approval; no rocks, creek or bridge development begun.**

Exact files: [ChangedFiles.txt](ChangedFiles.txt).

## Final handoff

Final recheck: saved scene, zero unexpected prior-object changes, unchanged heights/detail maps/layer references, no missing scripts/materials/invalid meshes. All five settings files and Production02 hashes remain identical to the start of Environment07. ProtectedVerification.json records the intentional scene/TerrainData changes separately from protected files. Scene stays open in Edit mode, selected at Environment07. No temporary input devices, profiler terrain clone or gameplay overrides remain.

Persistent existing Unity-file modifications are only the Briarwick scene and its TerrainData. Existing Environment06 Revision01 issue documentation is updated to point to this road candidate. New assets and review evidence are itemized in ChangedFiles.txt; the temporary unused TerrainLayer candidate and its empty folder were removed before handoff, and no pre-existing source/asset was deleted.
