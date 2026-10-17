# CM_BotanicalPlanterKit01 — modular storybook botanical library

## Review

- Assets/Scenes/CM_BotanicalPlanterKit01_ArtReview.unity: separate gallery with three box combinations, all five medicinal species, pots/bucket, ivy wall/corner, four dried bundle types, garden bed, border and groundcover.
- Assets/Scenes/CM_BotanicalPlanterKit01_IntegrationPreview.unity: non-destructive copy of the approved StyledDetails07 exterior with41 placed botanical modules. The running Editor is left on this scene in Edit mode.
- Previews/Review: Front, ThreeQuarter, CloseUpHerbs, CloseUpIvy, HangingHerbs, WindowBoxes, GameplayDistance, ReverseAngle. Previews/Integration: Front, ThreeQuarter, CloseUp, GameplayDistance. All are direct camera renders without Editor gizmos or postprocessing tricks.

The approved scene remains unchanged. This is a botanical installation study, not assembly of the production roof, facade, window or portal kits. The copy deliberately keeps the approved benchmark building geometry and lighting. Its original rough roof and other presentation approximations were not revised.

## Library and editable sources

CM_BotanicalPlanterKit01.blend contains34 component collections,1644 named editable source pieces, packed paint images and attachment sockets. Blender sources remain separate for leaf/stem/pot editing; exported role meshes combine these to avoid per-leaf Unity GameObjects. build_botanical_kit01.py is the bpy recipe. Use background Blender only; it refuses existing output unless -- --refine-own-kit is supplied deliberately. No plugin dependency.

61 FBXs =34 base exports plus27 reduced-detail exports.45 prefabs =34 components, seven potted arrangements and four box combinations. Components and planting inserts can be enabled/replaced independently. Six shared matte URP Lit runtime materials: fresh foliage, dried foliage, walnut, terracotta, soil and twine. Review neutral material is an extra display-only asset. New paint PNG/manifest/UV-region JSON live under ArtSource/Paint/Architecture/CrookedMortar/BotanicalPlanterKit01. The transparent1254px atlas contains eight separately painted botanical elements. Approved GouacheMaterialSheet_v02 artwork supplies walnut paint and terracotta surface variation; muted material tint gives the earth palette. No photoreal noise, new lighting filter, blur or bloom.

| Family | Components |
|---|---|
| Containers | Small/medium/large hollow terracotta pots, open wooden bucket, herb tray,1.76m and2.10m window boxes |
| Medicinal plants | Lavender, sage, rosemary, thyme, chamomile; A/B size/pose variations for each |
| Window inserts | Flowering/greenery in Small and Paired widths, with over-rim ivy trails |
| Climbing/trailing | Wall A/B, corner90, beam drape and hanging/trailing ivy |
| Dried herbs | Lavender, rosemary, sage and mixed bundles, top attachment sockets |
| Garden | HerbBed A/B, flowering border and thyme groundcover |

Plant forms are deliberately simplified recognizable silhouettes, not scientific botanical specimens. No harvesting, wind or other gameplay system is included. Fresh geometry is genuinely arranged in3D: individual curved leaf/sprig strips around several stems, shaped using the alpha silhouettes. There are no crossed full-plant rectangles. Foliage surfaces are open and double sided by design; pots/stems/ties are closed solids. The source paint is an editable flat PNG, not a layered painting document. Additional artist-painted variants, wind and regional species can be developed later without changing the attachment interface.

## Fit and placement

Metres; unit prefab roots; Unity+Y up, +Z exterior/front for wall-mounted modules. Container pivot is base-centre. Plant/bed inserts use root/soil-level pivots. Hanging bundles use a top loop socket and extend downward. Wall ivy uses the base stem datum; Trailing uses top datum; BeamDrape spans about1.3m around its central mounting line. Corner geometry includes leaves turned around the return rather than all facing one camera. Connections children expose PlantRoot, WallMount, Mount/End or Hang as appropriate.

Pots: nominal body diameters .32/.47/.64m; heights .32/.46/.62m; soil roots .2688/.3864/.5208m above base. Bucket soil .32m; tray soil .192m. New boxes are1.76m wide/.38m deep/.30m high and2.10m wide/.39m deep/.28m high; soil sockets .24/.224m. Window insert root footprints approximately1.55m and1.91m fit the approved original and paired boxes. Let foliage spill beyond edges; keep root positions inside the soil. Trailing stems crest over the rim before dropping, rather than passing through a front board.

For CM_WindowBay01 reuse its existing planter and place the Small insert at its soil surface; do not stack the entire new container on top. For CM_PairedWindowBay02 use Paired insert at the existing flower-box soil datum; disable its old optional PlanterDressing cards. Either kit can instead take a complete Box combination if the existing planter is disabled in an authorized integration. New containers/planting do not alter3.24m facade floor spacing; their socket is a local furnishing datum, not a structural bay height. No approved window prefab was edited here.

The integration copy hides only redundant old botanical-card and old potted-container Renderers, never their GameObjects, scripts or colliders. New pots use the existing approved positions, while window inserts retain existing architectural boxes. Climbing modules fit portal/fascia/wall positions; the garden planting stays in existing beds. The original53 collider/behaviour/light components match before/after, including37 colliders. No new Collider or gameplay behaviour exists. The central approach volume is clear over .90m width, versus the existing CharacterController .80m diameter,2m height. Physical traversal routes, doorways, rooms and stairs are unchanged. Validation sampled the central visual approach and preserved physics; it is not a full navigation/autoplay test.

## Geometry/rendering budget

| Asset group | LOD0 triangles |
|---|---:|
| Individual plant | 250–730 |
| Ivy segment | 372–468 |
| Pot/tray/box | 344–368 |
| Hanging bundle | 602–1692 |
| Garden cluster/border/groundcover | 900–2370 |
| Full window planting insert | 4228–5858 |
| Complete unique base library | 42114 |

Reduced foliage library is26242 triangles versus39658 full foliage triangles:about34% reduction. Container library adds2456 triangles and does not need a second LOD at these counts. Prefab LOD thresholds are .025/.0065 screen height; reduced meshes drop selected subordinate leaves, retain main flower heads and turn off distant leaf shadows. Reduced exports use _Reduced filenames; prefabs own LODGroups. An earlier _LOD1-only filename import warning was corrected, with no new warnings/errors after reimport. No packages or automatic LOD tool were needed.

Plants, ivy, window inserts and garden patches use one renderer/material per LOD, sharing solid painted stems with leaf geometry. Dried bundles use two including ties. Containers use two or three material slots. The41-instance integration adds64510 triangles at all-LOD0,64 renderer/material slots before culling/batching and extra shadow passes. These are structural counts, not measured GPU draw calls/frame time. Materials have instancing enabled. This is suitable for review and reuse, but a populated village still needs target-hardware profiling, distance/shadow budgets, streaming and possibly non-destructive combining/HLOD per building. Do not duplicate an entire house's41 decorations throughout the village without profiling.

Leaves use opaque alpha clipping at .42, ZWrite enabled, queue2450 and CullOff/double-sided rendering. There is no alpha blending or blend-sorting dependency. Alpha-is-transparency and mip coverage preservation are enabled; trilinear filtering and restrained alpha-to-coverage help edges. Shaped meshes avoid much transparent rectangle area: sampled accepted leaf area is about74%. This is mask efficiency, not a measurement of screen-space overlap. Leaf overlap and shadow passes still cost fill rate. No claim of zero overdraw. Keep patches restrained and avoid many coplanar duplicates.

## Validation and provenance

SourceValidation.json:418 closed solid parts,1226 intentional open shaped-leaf parts, zero degenerate geometry/UV triangles, finite normals, UVs within0..1 and opaque stem paint patches. Intentional shared sprite/paint-trim UV reuse is documented; this is not a unique painting atlas. Source images are packed; AtlasRegions.json gives exact nonuniform sprite bounds for repainting.

UnityValidation.json:all34 modules/61 FBX imports match recorded topology and bounds (maximum discrepancy under0.000001m), complete valid normals/UVs, proper unit roots and materials. Alpha mode, clipping, depth writes, mip coverage, collider preservation and approach clearance checks passed. Front/angled/rear views inspected for alpha borders and view-dependent disappearance. Source leaf bands hold depth and shape from different angles; no rectangular card borders observed. Existing architecture may occlude planted foliage as expected.

Brief integration Play-mode smoke check passed with no new warnings/errors; Editor is stopped again. No project compilation failure. Initial import naming warnings were fixed rather than suppressed. The full existing scene was not performance-profiled or rebuilt. GPU frame time remains unmeasured.

PreservationValidation.json lists files created and hashes all pre-existing project files. No approved scene, gameplay/traversal scripts, colliders, roof assets, package settings or unrelated scenes were changed. No package installed and nothing committed.
