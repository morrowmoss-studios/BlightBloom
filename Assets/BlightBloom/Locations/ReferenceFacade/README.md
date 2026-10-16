# Concept-directed front facade pass

Primary visual reference: the user's `Storybook Apothecary by the River.png`. The work targets its illustrated shape language rather than duplicating its setting or proportions.

## Comparison and decisions

- Reference: steep, gently curved roof and asymmetrical gables. Previous scene: broad shallow symmetric roof. This pass adds an off-centre curved roof silhouette, bargeboards, gabled attic vent and taller visual flue, without changing the retained physics roof or playable rooms.
- Reference: warm cream plaster painted in broad planes, walnut framing with selective edge wear, muted slate and buff cut stone. Previous scene: procedural mottling and repetitive grain. This pass uses a generated painted surface atlas with four isolated material regions; all remain matte URP Lit with no normal maps or glossy reflections. This is a texture candidate, not a production artist-authored atlas.
- Reference: arches, fitted curved shutters, fan tracery and masonry entrance. Previous scene: rectangular openings with pointed hoods. New front window surrounds, arched pane meshes and visual corner infills stay within the existing aperture extents; doors retain their original clearances and collision geometry.
- Reference: a broad sheltered shopfront and projecting illustrated sign. Previous scene: small triangular canopy and wall lettering. New tiled lean-to canopy and hanging mortar-and-pestle sign read as a shop-house. The entry stays open; no solid door is introduced.
- Reference: botanical clusters around structural features. Previous scene: scattered diamond leaves. This pass groups lobed ivy leaves and small cream flowers into one climbing seam and adds a few hanging medicinal herb bundles. Existing garden and exterior walking space remain.
- Reference: warm hand-painted daylight, coherent environmental storytelling, village/river context. Existing scene lighting was retained for this focused comparison; there is no blur, new grading or brightness trick. River, village, trees, paving and full property dressing are out of scope.

## Assets and authoring

`Tools/ApothecaryReferenceFacadePass.cs` is an Editor-only, on-demand Unity Pipeline authoring utility. Apply refuses duplicate application. Superseded renderers are disabled rather than removed; existing geometry and colliders are retained. New art is under `10 Concept-directed facade`.

`Textures/IllustratedSurfaceAtlas.png` is an AI-generated material candidate created with the image-generation tool, then copied into the project. It contains cream plaster, walnut, limestone and slate quadrants. Materials use inset UV scale/offset to avoid quadrant bleeding. Generated texture candidates need art review and eventual unique UV/texture work; the supplied concept image itself is not used as a texture.

Shared meshes and materials are under this folder. Source materials, room furniture, input settings and runtime gameplay code are unchanged. The facade palette is reused on adjacent exterior panels to avoid seams.

## Validation

989 pre-existing transform records retain their original positions, rotations, scales and parents. Initial application compared serialized collider state, enabled state, world transforms and hierarchy activity before/after: unchanged. New art has zero colliders. All 13 doorway/landing capsule probes pass. In Play mode the existing CharacterController completed all 26 collision-route waypoints, including stairs in both directions, private rooms, work areas and garden exit. This is a CharacterController.Move collision test, not simulated keyboard/camera usability testing. No new compilation or runtime errors were observed.

SampleScene, TraversalSandbox and all three traversal source files have unchanged hashes.

## Deliberate approximations / next dedicated art

The tall roof is a render-only attic shell over the preserved original roof collision proxy. New dormer/attic vents do not imply accessible rooms. Proper roof/attic construction, fascia thickness, dormer cheeks and flue connections require authored architectural meshes if the roof ever becomes accessible.

The window corner infill is a visual arch mask over a rectangular collision aperture. Fitted wall-opening meshes, jamb depth, individually shaped timber, shutter pivots, glazing and masonry blocks need dedicated modular models. The open entrance has no interactive door.

The sign lettering and mortar motif are provisional geometry/TextMesh, not final hand-lettered illustration. Roof UVs, tile batching, chipped edges, foliage cards, flowers and drying herbs need focused artist-authored meshes/textures and distance treatment. The concept's richer village/river composition is not recreated here.
