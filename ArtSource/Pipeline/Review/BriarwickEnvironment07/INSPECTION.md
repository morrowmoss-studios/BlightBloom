# Environment07 inspection decisions

See README.md for full findings and original heights/widths.

- MainRoad and13Path meshes: structural walkable ribbons with MeshColliders. Retain original vertices and collision assets; replace visual references/materials only.
- Common_26x30m_ActivityReserve: no collider; visual common surface safe for equivalent visual mesh derivative.
- Bridge_ContinuousWalkDeck, DeckThickness, ContinuousGuard, GuardPost and BridgeSupport: actual bridge placeholder, retain every component/asset unchanged. Broad bridge-mesh bounds include unused original main-route vertices; do not rebuild it just to improve bounds in this task.
- Farm plots, herb-garden soil reserves, graveyard reserve: not unfinished road surfaces. Preserve them.
- No separate road prefab system was discovered. The final cross-check found the Woodland03 gathering-grove continuation in existing Terrain paint, beyond the14mesh routes; it is included in the refinement along its recorded alignment. Ground wear uses the same Terrain's eight layer weights. Existing soil layer7 and owned low-contrast diffuse fit this pass.
- Original opaque earth texture uses world UVs but has hard geometric edges. All intersections can share the same world-coordinate texture with no independently oriented texture seams. New edge-coordinate UV channel is added only to owned mesh copies.
- Narrow paint at256resolution had1.25m texels, unsuitable for soft secondary-path margins.1024resolution selected; eight layers retained, memory tradeoff documented.
- Elevated bridge-approach earth edges are a local construction issue. A136-triangle fitted shoulder and one collider support only those existing ramps; original bridge and road collision remain untouched.
