# CM_FacadeBay01 — modular facade review candidate

The Crooked Mortar benchmark: CM_CrookedMortar_B_StyledDetails07. No existing scene, asset, gameplay script, collider, package or project setting was modified. This is an isolated render-only construction kit, not an installed facade replacement.

## Deliverables

- Editable CM_FacadeBay01.blend, with named logical parts, per-module display layout and socket reference empties. Approved paint and baked atlas packed in source.
- build_facade_bay01.py: deterministic bpy construction, reveal Boolean, fitted timber shoulders, mitred corners, seated gable king posts, UV unwrap, paint transfer and established FBX export conversion.
- 17 independent FBX models, 17 component prefabs, two approved-window compatible assembly prefabs, one shared matte URP Lit kit material, 4096 albedo atlas.
- CM_FacadeBay01_ArtReview.unity: two-storey assembly with corner, approved window insert, secondary gable; detached B hero-gable profile, narrow bay, and unchanged portal as material/scale reference. No roof kit or botanicals created.
- Previews: Front.png, ThreeQuarter.png, GameplayDistance.png, KitOverview.png. GameplayDistance is a static 1.75m-height / 55-degree camera reference, not a playable scene.
- GeometryValidation.json, uv_validation.json, SourceDimensions.json, UnityValidation.json, SeamValidation.json, PreservationValidation.json, ModuleCatalog.json and triangulated UV SVG.

## Module inventory

| Module | Nominal grid width / height (m) | Purpose |
|---|---|---|
| CM_FacadeBay01_Plain_3m | 3 / 3.35 | Plaster infill, .28m thick; .18m shared post grid and .22m floor/head beams; exterior at Z=0. |
| CM_FacadeBay01_Plain_1p5m | 1.5 / 3.35 | Plaster infill, .28m thick; .18m shared post grid and .22m floor/head beams; exterior at Z=0. |
| CM_FacadeBay01_Plain_3m_Tall | 3 / 3.6 | Plaster infill, .28m thick; .18m shared post grid and .22m floor/head beams; exterior at Z=0. |
| CM_FacadeBay01_Post_3p35m | 0.18 / 3.35 | Single shared boundary post; 0.18m width, .42m depth. No duplicate posts between bays. |
| CM_FacadeBay01_Post_3p60m | 0.18 / 3.6 | Single shared boundary post; 0.18m width, .42m depth. No duplicate posts between bays. |
| CM_FacadeBay01_Beam_3m | 3 / 0.22 | Between-post shoulder length grid width minus .18m; bottom-centre pivot, .22m height, .42m depth. |
| CM_FacadeBay01_Beam_1p5m | 1.5 / 0.22 | Between-post shoulder length grid width minus .18m; bottom-centre pivot, .22m height, .42m depth. |
| CM_FacadeBay01_Brace45_L | 1 / 1 | Flat seated end shoulders fit post face and beam underside; embedded rear depth, grain follows diagonal. |
| CM_FacadeBay01_Brace45_R | 1 / 1 | Flat seated end shoulders fit post face and beam underside; embedded rear depth, grain follows diagonal. |
| CM_FacadeBay01_Corner90 | 3 / 3.35 | Exterior vertex pivot; walnut corner with two complete 3m grid return bays and mitred timber/plaster transitions. |
| CM_FacadeBay01_WindowOpening_3m | 3 / 3.35 | Actual 1.6m wide arch through .28m plaster. Approved WindowBay01 insert at same origin; original wall/framing/eave omitted in adapter. |
| CM_FacadeBay01_Plain_3m_Benchmark | 3 / 3.24 | Plaster infill, .28m thick; .18m shared post grid and .22m floor/head beams; exterior at Z=0. Benchmark variant: 3.24m finished-floor rise. |
| CM_FacadeBay01_Post_3p24m | 0.18 / 3.24 | Single shared boundary post; 0.18m width, .42m depth. No duplicate posts between bays. Benchmark variant: 3.24m finished-floor rise. |
| CM_FacadeBay01_Corner90_Benchmark | 3 / 3.24 | Exterior vertex pivot; walnut corner with two complete 3m grid return bays and mitred timber/plaster transitions. Benchmark variant: 3.24m finished-floor rise. |
| CM_FacadeBay01_WindowOpening_3m_Benchmark | 3 / 3.24 | Actual 1.6m wide arch through .28m plaster. Approved WindowBay01 insert at same origin; original wall/framing/eave omitted in adapter. Benchmark variant: 3.24m finished-floor rise. |
| CM_FacadeBay01_Gable_HeroB | 5.55 / 4.37 | B-derived asymmetric wall-end profile; no roof surfaces. Bottom baseline pivot. Shared .28m wall depth. |
| CM_FacadeBay01_Gable_Secondary | 3 / 1.95 | B-derived asymmetric wall-end profile; no roof surfaces. Bottom baseline pivot. Shared .28m wall depth. |

The two extra prefabs are CM_FacadeBay01_WindowBay01_Compatible (3.35m storey) and CM_FacadeBay01_WindowBay01_Benchmark (3.24m storey). Each nests the original painted v02 window prefab and overrides only renderer visibility in the new instance: frame, shutters and existing planter remain; original plaster, structural frame and eave renderers are omitted to avoid double walls/framing/roof. Original WindowBay01 prefab/source/materials are unchanged.

## Connections and measurements

Metres; +Y up; +Z exterior; unit prefab roots, zero geometry transform. Plain bays and beams use bottom-centre pivots. Posts use base-centre. Corner90 uses the exterior corner post centre at ground; its front return extends -X and its side return extends -Z. Braces use their lower post shoulder pivot, not a bounding-box centre. Gables use the measured base datum. All connection positions are explicitly stored in ModuleCatalog.json and the prefab Connections hierarchy. Side-return modules face +X when placed with yaw +90 degrees.

3m / 1.5m spans refer to **post-centre grid spacing**, not raw plaster width. One shared .18m post belongs at each boundary. Plaster infill widths are 2.82m / 1.32m; wall thickness .28m. Timber extends to Z=.14m in front of the plaster plane Z=0 and to Z=-.28m behind. Horizontal beams are .22m high, actual shoulder lengths 2.82m / 1.32m. Place floor beam at y=0 and head beam at height-.22m. Infill runs y=.22 to height-.22. When storeys stack, the floor/header sections form a deliberately doubled .44m floor band, not coincident faces.

Corner assembly includes its own .28m corner post, two mitred plaster return bays and four mitred rails. It requires shared end posts at (-3,0,0) and (0,0,-3); do not add a second post at the actual corner or overlay another complete plain bay on its returns. Its exact end sockets allow a further straight bay to continue with the normal shared post.

End shoulders and mating profiles remain straight. Handcrafted irregularity is restrained to post midsections (~2mm) and small visible bevels. Plaster bevels exclude edges that would cut holes through mating corners; front/reveal edges remain softened. Diagonal braces seat against the post face and beam underside. Their rear portions are housed into the infill thickness; this is intentional embedment, with no coplanar exposed faces. No brace is placed beside the upper window where it could clash with an open shutter.

The approved scene was inspected read-only: ground finished floor .20m, upper finished floor 3.44m, giving **3.24m** rise. Benchmark wall/post/corner/window variants match this. Standard 3.35m and tall 3.60m options are also included for later village assets. Do not non-uniformly scale a finished textured bay to match a different rise; use the corresponding source parameters/variant.

Window compatibility: actual opening width1.60m, sill1.10m, spring1.75m, crown2.40m; thickness .28m, exterior plane0. The approved timber frame/shutters/sill/planter reuse their original origins and scale. Opening ray tests confirmed a clear centre, solid adjacent plaster and solid reveals. Use the insert-only assembly; placing the entire original window bay on a new wall would duplicate its original plaster/framing/eave.

EntryPortal02 remains unchanged and separate. Its post centres are 2.20m apart versus the facade grid of3m. Eventual entrance fitting therefore needs narrow return/infill pieces and specific beam shoulder lengths (nominal grid-centre difference .40m per side); do not fill the doorway with PlainWall or add duplicate boundary posts. Retain the approved 3.32m recessed door relationship behind the canopy-front portal. Portal timber projects about .11m from its centre plane versus the facade timber .14m: align exterior datum and bearing connections during an authorized integration, rather than scaling the approved portal. No entrance installation was attempted here.

HeroB gable derives the actual B profile: heroL=-2.8, heroR=1.85, peakX=-1.05, peakY=10.40; roof profile base datum6.03. Result: 5.55m outer rake width, 4.37m rise, shifted apex x=-.575 relative to module datum. The rake changes slope deliberately at the shoulders. This is the front wall-end/rake geometry only, not a roof surface. It includes the projecting eave profile; the underlying approved hero wall width is4.65m. Eventual integration needs crop/return adapters at wall-to-eave shoulders and stepped intersections; do not scale this infill across the old box footprint. The smaller gable is3m wide /1.95m rise (~52.4 degrees), demonstrated on the grid assembly.

## Textures and materials

Broad ivory/plaster and walnut brushwork comes directly from the approved GouacheMaterialSheet_v02 artwork. No photoreal noise, gloss, blur, bloom or new decorative clutter. UV0 is a unique shared atlas across all33 mesh parts. Density p05/median/p95: 173/185/193 pixels/metre at4096; tiny bevels vary. The atlas is a rebake of existing approved paint, not newly generated native4K detail. Paint projection is reconstructed by the source script and packed source image; final editable mesh UV0 and the atlas remain in the blend. Shared material metallic0/smoothness0 with specular/environment reflections disabled. Neutral review lighting has no fog, bloom or grading.

## Validation

All33 source mesh parts: closed manifold edges, positive signed volumes, zero degenerate triangles. Entire unique component library totals 4744 triangles before repeated scene instances and reused approved assets. All17 models matched canonical Blender bounds within0.001mm in Unity, with complete finite normals/UVs and valid shared URP materials. Source display offsets are excluded from exports; geometry and prefab pivots verified zero/identity/unit. UV0: within0..1, zero positive-area triangle overlaps (1e-9 UV-area tolerance).

168 seam ray probes across assembled front/side timber-plaster joints and stack boundaries found zero holes. Tests sample critical interfaces rather than claiming an exhaustive proof of every possible arbitrary arrangement. Temporary validation colliders were destroyed; scene and kit prefabs contain zero colliders. The review scene has no gameplay scripts; two URP built-in light-data components are expected. No traversal systems were changed or invoked.

One Pipeline request timed out during the initial bulk import. Imports subsequently completed and validation calls succeeded; it was an Editor automation timeout, not a script compilation failure or bad mesh import. Final Play mode smoke check completed with zero Console errors or warnings; EditorSmokeCheck.json records the result.

## Review and regeneration

Open Assets/Scenes/CM_FacadeBay01_ArtReview.unity. Inspect Connections on each prefab and compare front/angled/gameplay-distance renders. The assembled example demonstrates the kit; it is not a new approved building design. Final integration still needs site-specific shoulder/recess pieces for irregular widths, roof intersections and portal returns. No LOD is necessary for this small library at this stage; evaluate repeated-instance draw calls and any static combining after integration without losing modular source prefabs.

Run Blender with --background --factory-startup --python-exit-code1 --python build_facade_bay01.py. For deliberate regeneration of only this kit, append -- --refine-own-kit. validate_facade_uvs.py checks unique UVs and writes canonical bounds. Unity snippets are outside Assets in ArtSource/Pipeline/Review: CreateFacadeBay01Review.cs (refuses an existing review scene), FinalizeFacadeBay01Review.cs (creates benchmark variants and assembles new review contents), ValidateFacadeBay01.cs, ValidateFacadeBay01Seams.cs, CaptureFacadeBay01.cs. Do not rerun authoring snippets over an artist-edited review without first preserving their edits. Nothing committed.
