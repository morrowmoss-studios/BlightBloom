# Crooked Mortar — Exterior Recovery 01

**Isolated exterior candidate for artistic/technical review. Not approved for production integration.** No interior was constructed, aligned or loaded into this preview. Production02, StyledDetails07 and the prior open Workflow14 review scene remain unchanged (hashes in PreservationValidation.json). Nothing committed or pushed.

## Open the result

- Unity: `Assets/Scenes/CM_CrookedMortar_Exterior_Dev01.unity`.
- Unity render-only prefab: `Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Prefabs/CM_CrookedMortar_ExteriorRecovery01.prefab`.
- Editable repaired source: `CrookedMortar_RepairedHigh.blend`.
- Editable optimized source: `CrookedMortar_Optimized.blend`.
- Original Blender reference: `OriginalReference.blend`; raw GLB remains at the path in SourceManifest.json.
- Transport: `Exports/CM_CrookedMortar_ExteriorRecovery01.{glb,fbx}`. GLB contains the maps; Unity uses FBX plus explicitly assigned external URP materials. Original base color, normal and packed RM images remain byte-exact, including inside the exported GLB.

The source .blend files contain clearly labeled hidden original high-detail geometry. Repaired/optimized collections can be enabled independently. Sign lettering remains editable text in Blender; exported lettering is mesh geometry. Source orientation is Blender Z-up / front -Y. Unity import is Y-up / front +Z; FBX conversion also changes the X coordinate convention. No negative object scale is required in Unity.

## What changed

1. Removed malformed raised/baked sign inset surfaces, retained source perimeter, and fitted three rebated walnut boards using an intentional valid region of the existing approved walnut atlas. Added editable ivory serif lettering: **The Crooked Mortar**, on both sides. No malformed individual glyph was deformed into a letter.
2. Removed nine verified UV islands belonging to the malformed blue-green iron cluster beside the front upper window. A missing rear facade surface required a small fitted plaster return. Its painted detail/edge blend is simpler than the surrounding source and requires artistic review. Added a restrained fascia-mounted hanger with capped ends and two drop links; original sound sign perimeter remains.
3. Preserved sound source roofs, ridges, dormers, beams, masonry, windows, door, ivy and planters. No extra shutters, balconies, buildings or decorative clutter were added. Source shutters remain as imported.
4. Converted normalized miniature units uniformly by 15×: approximately **8.32 × 14.72 m footprint including base, 9.74 m height**. This is a provisional exterior scale, independent of the separate interior plan. Ground offset is 0.3 mm to avoid base/ground coplanarity.
5. On the optimization copy only, welded exact coincident position seams while preserving per-corner UVs. Applied metric geometry scale **before** unweighted quadric reduction. Kept original texture detail and source normal map. No new high-to-low bake was attempted against the invalid UV layout.
6. New exterior-only collision setup: basic building/post blockers, 6,404-triangle upward-surface terrain/stoop proxy, and a 45 m test ground. No collision components in existing scenes or reusable kits were changed.

## Counts and quality

| Version | Render triangles |
|---|---:|
| Original Tripo | 1,880,780 |
| Repaired high detail | 1,869,545 |
| Optimized candidate | 527,497 |

Approximately **72% fewer** triangles than the original. Fifteen renderers / four shared materials. This is still a heavy landmark/hero candidate, not a generic village-building budget. No performance certification or shipping LOD claim is made.

The main silhouette, roof courses and authored color relationships survive at gameplay distance. Extreme close-ups show some softened edge shading and texture/tangent differences after reduction. Retain repaired high detail for hero comparisons and any future clean-UV bake. Many source leaf/stone/tile features remain fused; this is not modular clean retopology.

Initial collapse tests in normalized miniature space produced severe roof folding and were rejected. A broad spatial cut also damaged fused wall surfaces; it was replaced with verified island removal and a fitted return. `RejectedTests/` retains diagnostic images/source; those are NOT the deliverable candidate. The source original was never modified.

## Validation actually performed

- Source inspection and actual Cycles renders, including front/entry, side, rear, above-roof, sign, normal viewing distance and roof/timber/foliage/window details.
- Matched original / repaired / optimized renders: identical camera, lights, exposure and framing; no DOF or hiding defects with dramatic lighting. CameraManifest.json records conditions. See REVIEW.md. The Play-mode snapshot is diagnostic, not a camera-comfort approval.
- Finite geometry/normals/UV values, zero-area triangle checks, UV-collapse counts, material assignment, fresh self-contained GLB import, dimensions and original/map hashes. See Validation.json and PreservationValidation.json.
- Roughly 20,000 bidirectional nearest-surface samples compare the house body against repaired high detail; these quantify sampled distance, not a proof that every face or intersection is correct. New sign/return pieces are excluded from this body-deviation test.
- Unity FBX import: 527,497 triangles; correct Y-up dimensions, 15 renderers, no missing material slots or scripts. Explicit basecolor/normal/metallic-smoothness conversion and assignment; no package installation. Packed source roughness G becomes smoothness alpha, source metallic B becomes Unity metallic R.
- Play mode: existing ThirdPersonMotor / TraversalInput / orbit camera instantiated only in the new scene. Same production capsule height 2 m, radius .4 m, step .3 m. Automated CharacterController.Move probe reached all four exterior perimeter legs and front stoop approach, grounded at endpoints. It did **not** inject keyboard input or establish manual camera comfort. Temporary motor/orbit disabling during the synchronous probe was restored; normal saved setup remains enabled.
- Transition standing marker aligned to the measured stoop feet height, approximately 1.11 m. Door remains a closed fused exterior; no opening animation or scene transition was implemented.
- No new compilation errors; no new reproducible Play-mode Console errors/warnings. Heavy editor-import calls produced Pipeline response-timeout logs. Initial embedded FBX material name-uniqueness warning was resolved by disabling embedded material import and assigning explicit external materials. The Console retains a Pipeline timeout error entry; it is not entirely empty. These automation/import events are distinguished from gameplay problems.

## Transition compatibility

The inspected gameplay code includes `BlockoutDoor`, an E-key proximity/hinge animation component, **not** an exterior-to-interior scene loader. No compatible existing scene-loading transition component was found in the inspected BlightBloom gameplay paths. Keep `FrontDoor_TransitionMarker_NO_LOADING_IMPLEMENTED` and its standing-point child as attachment locations for a separately approved transition implementation. Do not attach an interactive hinge script to the fused door mesh.

## Remaining issues / proposed next steps

- **Approval required:** artistic review of the replacement sign, local plaster return, source roof irregularities and optimized close-ups before any production integration.
- Return UV detail is much less rich than surrounding authored plaster; a carefully painted/registered local texture and boundary retopology would improve this repair. Avoid another broad spatial deletion or palette mask.
- Approximately 1,100 collapsed-UV triangles remain in the optimized body (exact current count in Validation.json), inherited from the generation. No complete unwrap, watertightness certification or exhaustive self-intersection solver was performed.
- Some fused foliage/stone/slate forms remain soft/lumpy at very close range. No obvious detached foliage was observed in the reviewed exterior views, but this is not a semantic reconstruction of every leaf.
- Window warmth is preserved in the texture; glazing has not been separated into emissive materials. The source door is closed, fused and not independently hinged.
- Geometry remains heavy: author clean UVs and selective retopology/LOD tiers if profiling or required camera distances justify further optimization. Do not simply lower the reduction ratio again without matched comparison.
- Collision is a provisional **exterior** test setup, not a finished full-building collision asset. Manual walk/camera testing, especially close to the facade and stoop edges, remains outstanding.
- Test ground is deliberately simple; no village environment, extra props or interior were built.

## Reproduction

Inspect scripts before execution. `inspect_house.py` reads the preserved GLB; `recover_house.py` reconstructs only new recovery outputs; `make_ground_collision.py` builds the separate walkable proxy; `validate_house.py` and `render_comparisons.py` are scoped to these sources. `prepare_unity.py` copies only new assets and converts the packed RM map. `CreateExteriorPreview.cs` is an evaluated Editor snippet outside Assets (no new gameplay assembly); it refuses to overwrite an existing scene. `CaptureAndInspectUnity.cs` captures only the new exterior scene. Reuse existing results rather than regenerating unchanged sources.
