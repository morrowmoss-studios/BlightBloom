# Briarwick Village Elder’s Cottage01 — rough architectural review

2026-11-02. Saved in EXISTING `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, location06. `06 Village elders cottage PLACEHOLDER` retained disabled. Original position(5,5.86877966,42), yaw190°, unit scale. Existing buildings, road, paths, terrain and landmarks untouched. Selected in saved Edit-mode scene for visual approval.

## Architectural draft

Compact cottage with clipped/half-hipped gable ends, a lower side service room, a small supported entry roof over a stone stoop, and an integrated hearth chimney. Soft muted timber/plaster and weathered wood-shingle palette. Variation comes from the roof and stepped footprint, without ornamental trusses, props or luxury features. No playable interior, NPC, dialogue or gameplay systems.

- Main house **5.8 ×8m =46.4m²**, side addition **1.6 ×5m =8m²**: total **54.4m²**, irregular overall body envelope **7.4 ×8m**.
- Roof ridge around6.04m including cap/floor offset; **highest chimney6.355m above placement datum**. Planned floor+0.12m.
- Main clear opening **1.4 ×2.4m**, addition service entry **1.3 ×2.3m**, static leaves. Sizes measured between framing, excluding door-leaf colliders. No closed-door passage or interior traversal claimed.
- Sampled porch headroom **>=2.4m** above planned floor datum.
- **16,712 triangles**, **11 mesh renderers**, **10 shared materials**, static mesh colliders. No LODs or final optimization pass.

## Source and dependencies

Editable packed `ArtSource/Blender/Architecture/Briarwick/ElderCottage01/BW_ElderCottage01.blend`. Eleven grouped FBX models and project-owned materials. Reusable `Assets/BlightBloom/Art/Architecture/Briarwick/ElderCottage01/Prefabs/BW_ElderCottage01.prefab`.

Read-only cottage/package timber, stone, door, metal, firewood and interior-roof maps; existing plaster and small-window sources; **Inn01’s eight-cell painted shingle atlas** reused for layered roof patches. No new artwork regeneration or imported-package modifications. Exact Unity dependencies in `GeometryValidation.json`.

## Validation completed

- **16/16 grounded automated Play-mode CharacterController.Move checks passed**: three lanes at main porch, three at service entry, existing road connection and full perimeter, forward/reverse. Existing controller2m high/.4m radius. Motor/orbit temporarily paused and restored; player transform restored. Automated collision smoke checks, not manual keyboard/camera comfort approval.
- Eleven meshes: finite UVs, valid normals, zero degenerate triangles; supported shaders and no missing texture references.
- Main/service geometric opening sizes verified. Terrain-contact samples within millimetres of unchanged pad; porch and service threshold accessible.
- **39/39 roof deck rays passed**, correct upward normals: main roof including clipped ends and lower addition. Minimum porch overhead clearance2.4m. Visually inspected roof, chimney, lower-roof connections and foundation.
- Initial triangular clipping omitted the end-deck tip. Corrected only candidate roof/deck clipping. Reassigned unchanged roof mesh references to refresh stale Editor collider cooking after FBX reimport; no serialized geometry/collider redesign elsewhere.
- **446 pre-existing scene component snapshots unchanged** outside new root. Placeholder intentionally disabled. **2,817 baseline file hashes checked**, only authorized Briarwick scene changed.
- Final Console**0 errors/0 warnings**, compilation not failed, captured historical cursor44 unchanged. No Console clearing. No shared gameplay, camera, packages or settings changed.

## Remaining refinement

Rough-build candidate only. Clipped hip junctions/ridge dressing remain simple and could use finer trim. Roof courses retain repetition, eave edges use simple deck treatment, plaster gables are plain and small glazing remains dark. Close-up material/joinery finishing and careful roof-edge dressing belong to a later approved refinement pass. No furniture, garden props or story dressing added. Service room is exterior volume only. Final artistic approval pending.

## Review files

`ElderCottage01_Front.png`, `ElderCottage01_ThreeQuarter.png`, `ElderCottage01_Side.png`, `ElderCottage01_Rear.png`, `ElderCottage01_VillageContext.png`. Existing scene lighting, clean renders without gizmos; review camera restored. Validation JSON and exact task inventory (`ChangedFiles.json`) retained here.

No new scene, commit or push. Stop for visual review.
