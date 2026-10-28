# CM_MasterMedicineCabinet01 — artistic review candidate

One standalone cabinet based on **The Crooked Mortar Cabinet Concept.png**. Not installed in Unity. Production02, Workflows07–14, all approved assets and gameplay remain untouched. No commits or pushes.

## Created

- Wide1.80m timber body, roughly1.94m high, gently arched layered crown, continuous chamfered stiles, shaped bearing feet, housed corner/shelf knees and recessed side construction.
- Three open shelf bays, sage tongue-and-groove backing, walnut reverse and four rear battens seated between rear stiles.
- Eight independent wooden drawer constructions in2×4; actual boxes, shaped fronts, small joinery pins, hollow brass cup pulls and recessed replaceable label holders. Labels are blank, ready for later painted lettering.
- Detachable living ivy:139 individually bent, silhouette-cut leaves with three painted variations, continuous runners/petioles and varied orientations. Crown runners follow the crown's actual profile.
- Eleven small moss clusters: short curled tuft ribbons ray-fitted to the actual wood surfaces; unsupported roots rejected. These replace the first flat patches that looked like floating ledges. Moss is deliberately restrained and does not cover drawer operation or storage.
- One hollow sage ceramic planter, real suspension hook, four rope slings/belly bindings and a separate trailing plant. It hangs near the left front shoulder to keep the core within the measured bay width. This differs slightly from the concept's more outboard installation.

Shelf contents are omitted by the brief, not hidden to conceal missing furniture. No bottles/books/skull/staging collection was produced.

## Files and modularity

- `CM_MasterMedicineCabinet01.blend`: editable native metric source; separate component meshes in8 named collections plus attachment empties for mounting/three shelves/wall anchors. Textures packed. Individual drawer parts remain editable by numbered names; no drawer animation is implemented.
- `Exports/CM_MasterMedicineCabinet01.fbx`:8 grouped game meshes, floor-centred common pivot, established Blender→Unity axis conversion, metre scale. No camera/studio/physics or animation in export.
- `Exports/CM_MasterMedicineCabinet01.glb`:same8 grouped meshes, embedded paints/materials, +Y-up/+Z-front transport matching FBX. Foliage is double-sided alpha MASK with cutoff.4.
- `Textures/`:three1254×1254 source maps: new4-quadrant cabinet paint, new transparent living-botany atlas and an unchanged copy of the approved Workflow13 ceramic atlas. Original approved maps are unmodified. `Prompts.md` records provenance.
- `MaterialManifest.json`:12 reusable material definitions with texture/tint/roughness/metallic/alpha bindings. Blender materials can be appended from the source; GLB embeds them. FBX is intended for the established Unity material-remapping workflow, **not a promise of automatic Blender-node-to-URP material conversion**. For Unity, use shared matte URP/Lit materials, smoothness=1−roughness, alpha clip/cull off only for leaves/moss. No Unity materials/prefabs/scenes were edited or created in this task.

The model is authored with continuous variable cross-sections, real chamfered profiles, curved swept moldings, boolean V-tool cuts directly into stiles, closed drawer construction and thin-shell cup handles. UV islands sample appropriate vertical/horizontal/trim/sage paint regions; hero drawer faces receive denser independently offset paint. This avoids mapping a whole mixed atlas across a cabinet face. No noise displacement, flat carved plaques or loose prop accumulation.

`build_cabinet.py` creates only this asset; `ExportCabinet.py` re-exports the saved source without regeneration. `FinalizeUV.py` records the rope-seam repair now incorporated in the builder; `FitRearBattens.py` and `FitRearPlinths.py` are **one-time** saved-source joinery corrections, already reflected in the builder. Do not rerun those repeatedly on the delivered blend. Render/validation scripts do not modify Unity.

## Counts and fitting

**60,388 triangles** including plants/planter. Eight exported meshes,18 material primitives,12 materials. Furniture/hardware41,274 triangles; vines10,308; moss3,972; planter assembly4,834. Native source contains505 small editable components; exports batch those components, so it does not require505 Unity renderers.

Measured existing bay:1.846m wide,2.926m high,.759m maximum current visual depth. New wood/hardware bounds:1.800×1.940×.487m (W×H×D); depth includes feet/pulls beyond the approximate.45m case. Entire dressed asset:1.884×1.940×.733m. Foliage exceeds the measured width by~38mm total and must be locally fitted/disabled before integration; the room is not altered to accommodate it. Feet have6mm bearing padding above the source origin; seat that datum explicitly on import. See `FittingReport.json`.

Hero-asset budget only: no LODs, Unity GPU/draw-call profiling or repeated-village performance acceptance. Hardware/interior drawer geometry can be simplified for distance variants after artistic approval. Do not call these renderer counts measured Unity draw calls.

## Visual review and honest comparison

`Previews/`:Front, perspective ThreeQuarter, Side, Back, Clay, WoodAndDrawers, MossDetail and BotanicalAndPlanter. All are actual Blender Cycles renders against a neutral studio. No reference projection, paint-over or generated beauty image. Clay hides the detachable botanical/planter groups to expose the furniture's actual construction. The clay image remains valid for assessing the same visible furniture geometry; later corrections affect moss and hidden rear faces, rather than the visible front construction. Neutral studio is deliberately unsaved and absent from source/exports.

`ConceptComparison.jpg` places the approved cabinet front beside this actual model; `ReviewSheet.jpg` collects all views. The concept's stocked shelves affect perceived richness; those are explicitly optional staging and have not been used to dress up this candidate.

**Recognizable match, not a finished production-quality match to the concept.** The wide composition, crown,3 shelf bays,8 drawers, sage backing, cup hardware and living growth are reproduced. Differences remain:

- Foot/corner sculpting and timber surface history are cleaner and less individually carved than the reference. Stile tooling is restrained V-cut leaf marks, not the reference's richer sculpted botanical stems.
- Some long timber/trim paint remains soft in extreme close-up; hero drawers have better registration/density, but this is not a complete unique painted unwrap for every visible board.
- Moss is now physically rooted geometry but much sparser and coarser than the illustration; the moss close-up shows this shortfall openly; vine rhythm is still more regular and leaf silhouettes are less varied.
- Rope suspension and cup hardware are simpler, labels blank, and material variation less carefully authored around each joint. Palette reads somewhat lighter under neutral studio illumination than the dark reference sheet.

These are artistic limitations, not a need for more jars or another room decoration pass. This candidate needs explicit artistic review before it establishes a production benchmark or is installed. No other furniture family has been started.

## Validation

- `GeometryValidation.json`:finite coordinates/normals/UVs, exactly1UV layer per source mesh, zero degenerate triangles/UVs, positive closed volumes/manifold opaque components; open bent foliage and tuft ribbons are intentional. All final checks pass.
- `ExportValidation.json`:FBX and GLB reimport into independent empty Blender states; both retain8 meshes,60,388 triangles, expected metric transport bounds, UVs and material slots. No missing channels/slots. GLB contains3 embedded paint images,12 materials and correctly masked double-sided ivy/moss.
- Final studio views inspected, including the lowest shelf (duplicate coplanar surface removed), planter attachment, moss support and rear batten ends. Rejected/first renders were replaced in final comparison views. An earlier foot-specific diagnostic is not the final moss review.
- **Not performed:**Unity installation/import smoke test, scene collision/traversal tests, manual artistic acceptance, LOD/profiling. None is claimed; this asset remains outside `Assets/` and the Unity scene was used only for one read-only dimension query. No packages or gameplay changes.

Only this new `ArtSource/Blender/Interiors/CrookedMortar/MasterMedicineCabinet01/` directory was added. Existing tracked project files remain unchanged.

Export notes:Blender5.2 emits a material-node deprecation notice and a shared albedo/alpha sampler consolidation warning during GLB writing. The relevant texture nodes use the same sampler settings; actual GLB reimport confirms all3 embedded images and MASK/double-sided foliage bindings. These are not Unity compilation/runtime errors. No Unity import result is inferred from them.
