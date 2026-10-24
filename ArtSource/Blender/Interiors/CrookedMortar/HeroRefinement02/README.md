# Crooked Mortar — shop and entrance artistic refinement 02

Scoped artistic derivative of the approved Production02 foundation. Original furnishing FBXs, prefabs, editable Blender sources, approved architecture, botanical assets and painted atlas remain unchanged. This pass is ready for artistic review, not an assertion of final art approval.

## Geometry

15 reusable FBXs/prefabs, 43,070 triangles across the complete unique library. The counter and shelving derivatives contain their original geometry plus fitted construction details; their original scene visuals are hidden with renderer overrides, while original furniture colliders and interaction markers remain active.

- Counter: shaped pilasters/collars, stepped beads, arch-headed panel fields, botanical relief and a central mortar/pestle crest, side rails, drawbore pegs and a selected keyed repair. Placement and working surface retained.
- Shelving: continuous shaped pediment replacing the stepped crown, scalloped brackets, rounded shelf noses, fitted labelled herb drawers, varied ceramic/tincture silhouettes and a dry-herb caddy. Existing herb rail raised 0.12 m to clear the pediment.
- Entrance: fitted post collars/pegs and carved botanical details, arch bead, consultation plaque, individual stone facing on the existing stoop, one limewash repair and a restrained reused ivy drape. No new shutters. No roof kit or building silhouette changes.
- Records cluster, wrapped order parcel, herbarium board and optional research sheet are reusable surface/wall details. The parcel is beside the shelving, clear of the staff route. No functional interactions were added.

## Materials and artwork

Two new shared matte URP materials: ink/paper artwork and painted walnut. Existing sage, ivory, pottery, glass, brass and iron materials reused. The new timber sheet preserves the original atlas layout and uses broad authored brush shapes with sparse low-contrast grain strokes. It applies only to the new derivative meshes. No noise, scratch filter, bloom, fog, lighting or post-processing changes.

Editable SVG and drawing scripts are under `ArtSource/Paint/Interiors/CrookedMortar/HeroRefinement02/`. The 2048×1024 ink atlas contains medicinal herb labels, Robert’s formulary, consultation information, practice accounts and gathering notes. Existing ledger mesh receives the accounts/notes artwork through a scene-local material override.

## Scene organization and recovery

Scene: `Assets/Scenes/CM_CrookedMortar_Production02.unity`.

New independent decoration root: `18 Shop and entrance - artistic refinement 02`. Counter/shelving/stock derivatives are attached under the corresponding original furniture objects to retain their exact pivots. The old visual renderers remain disabled for recovery; the old models and reusable prefabs were not edited. No colliders were added, removed or changed. No shared gameplay, camera, input, door, settings or other scenes were edited.

`InstallHero02.cs` is guarded one-time source, not a utility to rerun over the installed scene. `FinishHero02.cs` synchronizes only the new family materials. Modeling uses the established Blender 5.2.2 metric FBX conversion (+Y up, +Z exterior). Blender source packs the painted images. The new derivative source can be rebuilt independently of AF01.

## Review

`Previews/Before/` and `Previews/After/` use matching transforms, FOV, resolution and existing lighting. Shots cover counter/shelves, wider shop, entrance, exterior three-quarter and counter craftsmanship. `Previews/Comparison/` contains paired images, before left / after right. Runtime shots use the unchanged player camera.

SourceValidation.json checks UVs, normals, finite geometry, unit scale and degenerate triangles. IntegrationValidation.json checks Unity import/materials/scripts, all 108 pre-existing collider definitions/transforms/activation, and 43 positions over the unchanged 105° door sweep against actual triangles of the new installed art. Live-input route reports are recorded separately; static door sweep does not substitute for E-key input validation.

## Remaining limitations

This is an authored hero-area pass; the rest of the house deliberately retains its existing detail level. Glass and paper remain simplified, small labels are secondary close-range details, and the embroidery/wood relief still need manual style approval. Drawers, books, scales and case notes are static. The old counter jar’s mirrored paper label is replaced with a correctly mapped derivative visual, preserving its original asset. Historical details are environmental storytelling rather than quest/crafting systems. Existing indoor camera comfort remains a manual review item; no camera behavior was changed. The roof was preserved rather than reopening its approved geometry/material pass.


### Verification state

Source and Unity checks passed for all 15 modules, with 43,070 triangles across the unique library. No missing scene scripts/materials were found. All 108 pre-existing collider definitions, transforms and activation states remain identical. No new colliders. New detail triangles clear all 43 sampled positions of the unchanged 105-degree door arc.

**Live input validation passed:** nine shop/counter/staff-aisle/kitchen-connection waypoints and eight E-key entrance/exit waypoints completed through the existing input/controller path in focused Play mode. Both routes had zero camera emergency corrections and zero sampled camera/geometry overlap. Door returned closed, unblocked, at its unchanged 180-degree closed angle after E-key opening, passage and closing. Actual player-camera capture is under `Previews/Runtime/`. These are current-pass results, not reused furnishing reports. No claim of manual camera comfort approval is made. Unity reported no new Console errors/warnings or compilation failure. Production02 is left open in Edit mode.
