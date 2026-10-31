# Tripo exterior: technical inspection

Source discovered at `ArtSource/Blender/Architecture/CrookedMortar/TripoImports/storybook cottage 3d model.glb`, rather than the requested, nonexistent Exteriors/TripoImports folder. Actual rendered geometry confirms the house, not a cabinet. Source SHA256 and byte-exact extracted maps are recorded in SourceManifest.json.

- One node, one mesh, one material; **1,880,780 triangles / 1,017,680 vertices**.
- Native dimensions approximately 0.555 × 0.982 × 0.649 units: normalized miniature, not usable metre scale. A uniform 15× unit conversion gives approximately 8.32 m wide × 14.72 m deep × 9.74 m high, including the terrain base. This does not align an interior or alter proportions.
- **1,922 topological islands**. These include UV splits and fused architectural surfaces, not 1,922 separable architectural components. Component bounds and initial renders are in Inspection.json and Inspect_*.png.
- One UV map; **125,411 collapsed UV triangles**. Initial 150,736 open topological edges include UV seams; they are not a count of visible holes. No >2-face edges in the initial triangle-edge usage test. Source geometric triangle areas are nonzero. This is not clean bake-ready topology.
- Three original **4096²** images: base color JPEG (sRGB), packed roughness/metallic JPEG, tangent normal PNG (Non-Color). All are preserved byte-for-byte. One material contains everything, including opaque modeled foliage. There are no leaf transparency cards to optimize separately.
- Main roof courses, dormers, ridges and roof hierarchy are visually coherent. Some tile lips, moss and foliage remain softly fused at very close range. No broad roof reconstruction is justified by the inspected views; preserve the attractive original courses and their irregularity.
- Principal timber posts/braces, entrance stonework, wall surfaces and windows retain strong source character. The door is a fused, closed exterior surface, not an independently operable leaf. Warm window coloring is authored into the texture, not separate emissive glazing.
- Sign has malformed raised/baked lettering, requiring replacement of the inset, not editing individual letters. Source perimeter remains useful.
- An orphan blue-green iron-like cluster beside the front upper window is visibly malformed. Its UV islands can be identified individually, but the wall behind is incomplete/fused. Removing it therefore also requires a fitted wall return. Do not delete a broad spatial volume.
- Ivy/planters are largely attached and readable; dense small leaf clumps are fused. Blind island deletion, smoothing or semantic color masking would damage authored surfaces.

## Repair decisions

Directly repairable: sign inset/lettering, local malformed cluster, missing wall return, unit conversion, external material conversion and simplified exterior collision.

Preserve rather than replace: roof silhouette and sound slate courses, structural timber, warm windows, door, foundation and restrained existing botanicals. Existing source shutters are retained; no shutters or new building features are introduced.

Partial reconstruction required: missing local wall return after fused cluster removal. Future lower-budget retopology/detail baking needs a proper new UV layout. Current source UVs are not suitable for blindly baking high-detail normals onto a new mesh.
