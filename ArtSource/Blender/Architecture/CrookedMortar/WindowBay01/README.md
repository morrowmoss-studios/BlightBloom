# The Crooked Mortar — upper-left window bay 01

Geometry-review prototype built in Blender 5.2.2 LTS with bpy. Primary reference: the user's Storybook Apothecary by the River image. No concept image pixels or generated materials are applied. The source is intentionally neutral for silhouette and construction review.

## Open and review

- Editable source: `CM_WindowBay01.blend` in this directory. A `.blend1` backup retains the initial prototype revision.
- Unity model: `Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01/Models/CM_WindowBay01.fbx`.
- Reusable review prefab: `Assets/BlightBloom/Art/Architecture/CrookedMortar/WindowBay01/Prefabs/CM_WindowBay01.prefab`.
- Isolated review scene: `Assets/Scenes/CM_WindowBay01_ArtReview.unity`. It is currently open in the existing Editor. No Play mode or player is needed for this static review.
- Review cameras: `Review_Front`, `Review_ThreeQuarter`, `Review_GameplayDistance`. Three-quarter is the enabled camera. PNGs are in `Previews/` here.
- Gameplay-distance camera is 8 metres from the facade, 1.7 metres above the implied ground with the upper-storey module base at 3.6 metres. It uses a 55-degree vertical field of view; it is a scale reference, not a running traversal test.

## Measurements and fit

The wall is nominally 3m wide, 3.6m storey height, 0.28m deep. Its top follows the underside of the eave. Full decorative bounds are approximately 3.3595m wide × 3.6636m tall × 1.1857m deep including shutters/eave.

The real through-opening is 1.6m wide. Sill elevation is 1.1m, arch spring 1.75m, crown 2.4m relative to the module base. Arch reveals have actual thickness, not an overlay mask. There is no opaque glazing to hide the opening.

Reference placement in the existing facade: Unity position (-4.5, 3.6, -6), yaw 180 degrees. These measurements match the current upper-left window zone; no facade objects have been replaced or hidden. Final seam and roof integration must be evaluated during a separately authorized installation pass. The existing rectangular collision opening is retained and has not been recut.

Source axes: Blender +X right, +Y exterior, +Z up. Export-only 180-degree Blender Z conversion plus the validated FBX -Z forward/Y up settings map source X/Y/Z to Unity X/Z/Y. Imported root rotation is zero and scale is one.

## Construction

- Exact Boolean arched plaster opening with curved timber frame, separate jambs, projecting sill, centre mullion, transom and fan tracery.
- Two fitted arched three-plank shutters, shown open, with rear rails and hinge straps. These are static mesh pieces; a future interactive version needs deliberate pivot hierarchy and hinge clearance checks.
- Slightly bowed/tapered posts, tie beam, pegged beam/post intersection, knee brace and lower rail. Pegs communicate joinery; fully engineered mortise/tenon cutouts are outside this prototype.
- Open-topped hollow planter with end cheeks, base, recessed soil and diagonal supports. No flowers are represented with primitive stand-ins.
- Four staggered courses of thick bevelled slate, continuous supporting roof boarding, rafters and fascia. Slate edge variations are subtle; this is an eave strip, not the complete steep gable from the concept.
- Six neutral, matte URP Lit review materials, no textures, bloom, fog or color-grading changes.

## Validation

`validation.json`: 82 mesh objects, 13,424 triangles; all mesh edges manifold, positive signed volumes, no zero-area faces. Ray tests confirm that the opening is clear and adjacent plaster is solid.

`uv_validation.json`: all visible and hidden geometry unwrapped into one unique shared 0–1 atlas; average island scale then global packing. Exhaustive candidate triangle clipping found zero positive-area UV overlaps (1e-9 UV-area tolerance). Linear UV density percentiles 5/50/95 are approximately 0.0683/0.0822/0.0917 per metre, or 280/337/376 pixels per metre on a 4096 atlas. Small bevel islands have more distortion than broad architectural faces. `CM_WindowBay01_UV.svg` is the 4096-unit triangulated UV guide. An artist should review seams and straighten key wood-grain islands before production painting.

`unity_validation.txt`: imported mesh/triangle counts match; UV and normal arrays valid; global bounds match source axis mapping within 1mm; unit scale and zero root rotation; no colliders added. No new Console warnings/errors occurred during this task; the previously recorded Pipeline timeout remains in the Console. Compilation failure flag is false.

Hashes of the existing scenes, traversal scripts, package files and ProjectSettings were unchanged. The only scene created is the separate art-review scene. No build-list, package, renderer or gameplay configuration was changed.

## Next art work

Approve or adjust arch proportions, shutter opening, sill/planter mass and eave silhouette first. Then paint plaster planes, restrained age, warm edge accents, directional timber grain, shutter wear and slate hue variation in the shared atlas. Avoid baking strong directional light into these maps. Create a small authored foliage-card cluster and flower atlas for the planter later. Final hinge shapes, more expressive asymmetric timber profiles, glazing, true housing joints and final roof/facade seams remain artistic refinement items. Do not call this final textured production art yet.

The 82 parts are convenient for authoring; a later render-ready prefab can combine static pieces by material and introduce distance variants after the design is approved. No LODs, colliders or gameplay behaviour are included.

## Reproducibility

`build_window_bay.py` runs only in background Blender and normally refuses to overwrite an existing source/export. `--revise-this-prototype` explicitly allows updating this prototype only. It saves the editable source before applying export-only transforms. Run `validate_uvs.py` afterward to refresh UV checks and template. Unity authoring/capture utilities live under `ArtSource/Pipeline/Review/` and are evaluated through the running Editor; they are not runtime scripts. The scene creation utility refuses an existing scene and should not be rerun over the current review.
