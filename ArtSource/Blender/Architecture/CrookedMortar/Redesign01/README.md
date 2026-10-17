# The Crooked Mortar — Architectural Redesign 01

A separate architectural approval prototype. This replaces the rectangular footprint in a **new scene**, not the existing `UncleRobertsApothecary.unity`. Geometry, circulation, roof hierarchy and room identity are the review subjects. Painted surfaces are temporary massing materials derived from the approved window palette; detailed roof tiles/trim and final decorative props are deliberately deferred.

## Open, compare and test

- New scene: `Assets/Scenes/CM_CrookedMortar_ArchitecturalRedesign01.unity` — currently open, in Edit mode.
- Building assembly prefab: `Assets/BlightBloom/Art/Architecture/CrookedMortar/Redesign01/Prefabs/CM_CrookedMortar_Redesign01.prefab`.
- Editable Blender sources here: `CM_Redesign01_Geometry.blend` and `CM_Redesign01_Painted_v01.blend`.
- FBX: `Assets/BlightBloom/Art/Architecture/CrookedMortar/Redesign01/Models/CM_Redesign01_Painted_v01.fbx`.
- `Previews/Front.png`, `ThreeQuarter.png`, `Side.png`, `Elevated.png`; `Previews/Original_ThreeQuarter.png` captures the existing building without saving or editing it.
- `Previews/Layout.svg` diagrams both floor plans. It is schematic; the actual wall apertures and collision mesh are authoritative.

Press Play and click the Game view to use the existing camera-relative WASD controller; Shift sprints, mouse orbits, Escape releases the cursor. Spawn is on the front approach at (-3,0.05,-9). The existing InputAction asset, motor, input and camera scripts are reused without source edits. Obstruction avoidance is enabled with a 3m follow distance on this new camera instance. Review cameras are disabled during normal Play and can be rendered by the capture utility.

The entrance door is held open 95 degrees with static collision for this prototype. It is not a newly implemented interactive door. Other thresholds are open. Ground height is 0, interior floor top 0.20m, upstairs floor top 3.50m. No build-list changes are required for manual Play testing.

## Architectural decisions and comparison

| Feature | Existing building | Redesign 01 |
|---|---|---|
| Footprint | One 16m × 14m rectangle; about 224m² ground floor | Three offset connected volumes; about 125.2m² ground floor |
| Street composition | Broad, largely flat frontage; repeated windows | Narrow projecting shop gable, 3.5m recessed living wing and deeper entrance court |
| Roof | One dominant broad roof over the rectangular house | Steep front roof, lower intersecting cross roof, and single-storey rear workroom roof |
| Ridge levels | Large single primary silhouette | 9.70m / 8.55m / 4.85m; chimney flues up to 10.86m |
| Window rhythm | Regular rows across large wall planes | Full-size bedroom arch, smaller offset living arch, high-sill treatment window, shop display window and differently sized study/workroom casements |
| Stair | 18 × 0.20m rises over about 9m, 2.8m wide | 17 × 0.1941m rises, 0.31m treads, 5.27m flight, 1.7m clear width |
| Interior scale | Very large generic rooms | Smaller public/work rooms plus a private bedroom/reading volume, living room and medical study |

The reference's visual language comes primarily from the **narrow tall gable over the shop, lower off-axis residential roof, wall returns with real depth, low workroom roof, focal entrance, and windows placed for their rooms**. The facade is not a repeated row of approved modules on the old box. The new roofs use modest flared eaves, and the front bargeboard follows that profile rather than bridging above it as a straight floating strip.

This is still a silhouette approval prototype, not a claim of matching the illustration's final art quality. It deliberately lacks village dressing, mature planting, bespoke roof-course meshes, rich interior props and final painted wear. Broad wall and roof surfaces are calm so shape/proportion can be assessed. The original comparison is framed to fit its larger building; it is not an exact-camera metric overlay.

## Footprint and room organization

Plan coordinates use Unity X/Z metres:

- **Front shop / bedroom volume:** X -5.5..-0.5, Z -6..3.0. The public shop occupies the projecting front; a rear dispensing/service area leads to the other wing. Upstairs is a large bedroom and reading alcove.
- **Recessed living / study volume:** X -0.5..6.3, Z -2.5..5.8. Ground floor has a compact treatment room, side circulation, stairs and rear service hall. Upstairs has living quarters to the front, medical library/study behind, and the landing to the east.
- **Lower preparation / storage annex:** X 2.6..8.0, Z 5.8..10.2. Preparation is in the front 2.55m; storage is behind the 8.35m partition, with its own rear garden door. Another garden exit opens directly from the service hall.

The service route lets staff reach treatment, preparation, storage, garden and stairs without taking all traffic through the examination space. Ground service clearance was increased by relocating the chimney breast to the rear shop wall and pulling the treatment rear wall forward to Z1.0. Doorways are approximately 1.45–2.2m wide depending on purpose; main entry is the approved entrance's 1.8m opening, down from the old 2.4m. Effective service passage width beside treatment is about 1.76m. Public circulation in the shop stays clear of the simple counter proxy.

Upper walkable slab area is about 90m² including landing, excluding the stairwell void; the old upper slabs total about 197m². The bedroom includes an intentionally open reading zone and can be subdivided later if the approved architecture calls for it. The annex is **not** an upstairs room: its lower roof meets the residential rear wall below the second-storey eaves, clear of study windows.

## Authored meshes, approved modules and collision

The new building shell has **17 logical Blender mesh groups / 3,732 triangles**. These include floors with a real stair void, walls with real door/window apertures, partitions, a closed stair profile and guards, windows, chimney and roof masses. Static MeshColliders use the imported geometry. The main/cross roof intersection is an exact Boolean union; a rear overhang was trimmed back to supported walls. The stair landing meets the last tread exactly; the initial 13cm gap was removed.

Roof meshes are closed attic mass proxies, not finished rafter/valley construction or explorable attics. Their lower surfaces form prototype upper ceilings. Future art production must author the final roof thickness, flashing, gutters, ridge caps, rafters and trim at these approved junctions. The annex eave/wall seam likewise remains a production-detail task. No claim of structural engineering certification is intended.

Three existing approved prefab instances are reused with **scene-local overrides only**:

- `CM_EntranceBay01`: front entrance at (-3,0,-6.035), yaw 180, with source wall disabled because the building has its own cut-through shell; source door held open and threshold/leaf collision added locally.
- `CM_WindowBay01_Painted_v02`: full-size front bedroom bay at (-3,3.5,-6.035), yaw 180.
- Same approved window at 75% scale: living-room bay at (1.5,3.8725,-2.535), yaw 180, clearly subordinate to the shop gable.

Upper-window mini-eaves are disabled locally; the new building gables supply the roof cover. Approved plaster panels/frame geometry are retained as slightly proud facade infill over real shell apertures. These panel-to-shell overlaps are intentional prototype assembly; eventual production wall modules should remove hidden duplicate surfaces. This limitation does not change traversal or the approved source assets.

The reused modules retain their authoring part hierarchies. Consequently total scene transforms exceed the 17 newly authored shell groups; the design does **not** claim the full property is 17 objects. Only a small set of neutral cubes was created for room-function furniture and site beds. No new decorative primitive cloud, final foliage or prop production was added.

## Materials and source workflow

`ArtSource/Paint/Architecture/CrookedMortar/Redesign01/bake_redesign.py` transfers the approved window v02 source painting into a unique 4096px albedo atlas. The sheet is reused unchanged and is packed into the painted .blend along with the baked texture. Plaster and slate color groups are deliberately compressed toward quiet palette values for this large-scale massing review. Timber retains directional brushwork; glazing is a simple matte grey/green placeholder. Materials are matte URP Lit. There are no new shader packages, procedural noise textures, bloom, fog or grading changes.

The unique full-building atlas has about 64px/m median texel density: enough for massing views, **not** final hero close-up texturing. Approved hero bays retain their existing higher-density assets. Future production should use modular trim/tiling painted textures and dedicated UV work once geometry is approved. No claim of new native 4K source painting detail is made.

Source axes remain Blender +X right / +Y forward / +Z up, exported through the validated static FBX conversion to Unity +X / +Z / +Y. Root scale and rotation are clean. Authoring order for reproduction: `build_redesign.py` → `refine_junctions.py` → `repair_uvs.py` → `add_treatment_window.py` → `validate_uvs.py` → paint bake. Creation refuses existing output unless the explicit new-design refinement flag is passed; junction/window utilities are purpose-specific and should not be repeatedly applied to an already refined source. UV repair isolates only audit-identified faces, with no mesh edits.

Unity creation, capture, original-comparison and collision-test utilities are under `ArtSource/Pipeline/Review/` with CrookedMortarRedesign/Traversal names. These remain outside Assets and are evaluated through the already running Editor. No runtime source files were added.

## Validation and practical limits

- Blender: all 17 logical mesh groups have manifold edges and positive signed volume. Body geometry includes real apertures and continuous stair/landing geometry. Roof UV intersections on two projection faces were corrected by separate UV islands; final audit reports zero positive-area overlaps and all UVs within 0–1.
- Unity: imported triangle/group counts match; UVs, normals, materials and collision references pass; exact stair bounds validate scale/orientation. Compilation failure is false; no new Console warnings/errors remain.
- **Final Play-mode route: 52/52 sequential waypoints passed**, covering entry, shop, service hall, stairs up/down, bedroom/reading, living, study, treatment, preparation, storage, both garden exits and a circuit around the building.
- The route uses the existing 2m-high, 0.4m-radius CharacterController and `Move` with gravity while temporarily disabling input/motor/orbit **in Play mode only**. It validates collision and accessible routes, not a manual keyboard/mouse or camera-comfort acceptance test. Components restore when Play mode stops. The scene is saved with normal traversal components enabled.
- Initial tests caught a chimney choke point and a shelf encroaching on the landing. Both were corrected and the complete route re-run on final geometry. Some initial straight-line waypoints were also routed through the actual room door centres rather than through partition walls.
- Pipeline briefly disconnected during the Play-mode domain reload; reconnect/retry succeeded in the same Editor. No second Editor was launched.

Reports here: `geometry_validation.json`, `uv_validation.json`, `uv_repair.json`, `unity_validation.txt`, `traversal_validation.txt`; UV guide: `CM_Redesign01_UV.svg`. Painting transfer fingerprints are in the paint-source folder.

## Preservation and approval boundary

Existing apothecary, SampleScene, TraversalSandbox, approved asset-review scenes, gameplay scripts, Packages and ProjectSettings retain their original hashes. The existing apothecary was loaded only to capture a comparison, closed without saving, and is unchanged. Approved entrance/window prefab sources were not modified. This task adds new redesign files; pre-existing uncommitted entrance-bay files remain as found. No commits or package installations.

Approve or revise footprint, front-gable proportions, residential recess, roof hierarchy, annex placement, window composition, and room/stair comfort before detailed art. Final decorative props, roof courses, richer storefront displays, foliage, interactive doors, optimized collision proxies, attic carpentry, light baking and production texture/detail work remain outside this milestone.
