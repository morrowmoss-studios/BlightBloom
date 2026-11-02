# Briarwick — first modular house compatibility test

Saved scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Left open in Unity 6000.4.5f1, Edit mode, with Family Cottage A selected. This is an exterior architectural/material compatibility test, not approval of the package as BlightBloom's finished art style.

## What changed

Only Family Cottage A, at its original world position (-43, 5.50587, -4), yaw115°, was replaced visually. Its original outer hierarchy name remains stable. The four original placeholder objects are preserved, disabled; all other ten primary building locations, terrain, roads, camera and player remain unchanged.

`FamilyCottageA_ModularAssembly_Test01` contains67 connected modular prefab instances. The package author's complete example supplies its fitted L-shaped junction/layout recipe; this is assembled from individual modular prefab references rather than a new fused model or a generic primitive substitute. Loose furniture, sign/torch props and ladders are omitted. Fireplace particles, wind and flickering lights are disabled only on the new scene instances. No runtime interaction scripts were added.

The native wall footprint is7 ×6 m, fitting the reserved7 ×9 m plot. The highest chimney is approximately6.52 m above the plot, compared with Crooked Mortar's roughly9.63 m overall bounds. Global building scale stays1. Module-specific fitted beam scales from the original example are preserved. A25 mm vertical seating offset aligns the lowest step/source contact; no terrain or imported model was altered.

Two original stone-floor modules form a small scene-local approach from the unchanged footpath into the recessed doorway. Only their vertical scale is reduced to.20 for a shallow apron. Total:69 module instances including the apron,20,210 rendered triangles; the cottage architecture alone is20,186 triangles,67 renderers and12 shared source materials. This is a review assembly, not a batched/LOD-optimized repeated-village prefab.

## Package inspection and URP

Source package: `Assets/Medieval_house_lite/`. Inspected30 modular-element prefabs,17 material assets, model/collider FBXs and assigned texture dependencies, the supplied example layout and its brief documentation. The used building materials run supported Universal Render Pipeline Autodesk Interactive shaders or URP Lit. Actual scene renders show their assigned maps; no pink/error surfaces, missing slots or shader errors were found. Imported meshes have UV and normal arrays.

Legacy particle shaders also occur in the package. Its fire effects were deliberately omitted/disabled for this test; this delivery does not certify those effects or every package feature for production. No global material conversion, package installation, original material edit or project setting change was needed.

## Comparison and recommendations

The native cottage is a believable smaller building beside the taller Crooked Mortar. Recessed entrance, dormer, intersecting gables, chimney and true timber/wall modules provide much more architectural information than the blockout mass. It is a useful construction/layout base.

It does not yet share Crooked Mortar's finished illustrated language:

1. Pale, fairly uniform weathered timber versus the benchmark's darker warm walnut and stronger painterly colour relationships. Reauthor a dedicated, directionally mapped painted timber/plaster treatment in a separate derivative material set after approval; a uniform tint alone would not resolve the difference.
2. Regular straight profiles, thin planar bracing and repeated shingles versus the benchmark's curved roof rhythm, softened edges and layered masonry/woodwork. Selective profile/trim refinement would help; copying the hero's decoration onto every cottage would not.
3. Neutral/dark glazed windows versus the benchmark's warmer apothecary illumination. Develop a coherent glazing/window-light treatment rather than assuming the imported glass already matches.
4. Stone apron has comparatively photographic, high-frequency cobble detail and square edges. A quieter painted stone treatment and more natural ground transition would improve cohesion.
5. The supplied door leaf is only.726 ×1.834 m. That is not a comfortable usable opening for the unchanged2 m tall/.4 m radius CharacterController. The exterior door remains closed and noninteractive. For future entry, rebuild/enlarge the local door/frame aperture (roughly1.2 m wide and2.2 m or greater high as an initial planning target) rather than enlarging the whole house or shrinking the player. No doorway usability approval is claimed.

Recommendation: retain this single native-scale test for review. Approve the massing/layout separately from the material finish, then prototype one painterly derivative material/profile treatment before expanding construction. No further buildings were replaced.

## Validation

- Cottage branch, recessed stone approach and complete exterior perimeter tested forward/reverse in Play mode using the actual existing2 m CharacterController.Move collision path: six cases passed with grounded endpoints. Motor/orbit enabled states and initial position restored. This is automated collision validation, not a normal-keyboard/manual camera-comfort test, and does not test passage through the undersized closed door.
- Zero missing material slots, unsupported used shaders, shader compilation errors, missing UV/normal arrays or active fire/flicker effects on the new architecture.
- All160 inspected scene objects outside the Cottage A hierarchy matched before/after. All11 primary locations remain present; no other placeholder is replaced.
- SHA256 check of2,050 existing Assets/settings/package/tracking/guide files: only the authorized Briarwick scene changed. No missing files or new Assets files; original package materials, models and prefabs, Crooked Mortar assets, other scenes, shared gameplay and settings remain byte-identical.
- Scene saved and reopened successfully; normal player motor enabled. Final Console reports0 errors,0 warnings and compilationFailed=false. An eval-only WindZone API error was corrected before the assembly executed; it did not change a project script. No full-project regression, packaged build, draw-call benchmark or interior traversal was performed.

## Review images

- [Complete cottage](01_CompleteCottage.png)
- [Cottage in the surrounding village, including Crooked Mortar](02_VillageContext.png)
- [Matched comparison](05_MatchedStyleComparison.jpg)
- [Original cottage comparison render](03_Comparison_Cottage_20m.png)
- [Original Crooked Mortar comparison render](04_Comparison_CrookedMortar_20m.png)

Comparison renders use the same55° FOV,20 m horizontal camera offset,9 m camera elevation above each building root and3.4 m target height. Lighting, fog, materials and camera settings are unchanged between shots. Building orientations remain as placed, so their light-facing angles differ naturally. The contact sheet only adds labels; source renders are unchanged. No geometry is hidden; existing planning labels are omitted by the review camera as in the hamlet overview workflow.

## Reversal and files

To revert visually, disable `FamilyCottageA_ModularAssembly_Test01` and `CottageA_LocalApproach_OriginalStoneModules`; re-enable `SolidFootprint_NoInterior`, `FoundationMass`, `RoofMass_10` and `DoorLocation_1.8x2.4m_VISUAL_ONLY`. The new exterior approach marker is informational and can be disabled as well. Never enable both the solid placeholder and cottage together.

Changed existing file: only `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. New files: this review folder's guarded assembly/capture snippets, inspection/validation records and screenshots. Assembly.json lists every structural source prefab and transform. AssembleCottage.cs refuses an existing test assembly and never applies prefab overrides to sources.

STOPPED for visual review. No cleanup, LFS work, asset purchases, new package imports, source edits, commits or pushes.
