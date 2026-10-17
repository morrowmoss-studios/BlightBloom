# CM_PairedWindowBay02 — isolated modular production candidate

Open Assets/Scenes/CM_PairedWindowBay02_ArtReview.unity. The running Editor is left on this isolated review. Nothing was installed on the approved building.

## Result and benchmark

Paired rectangular casements reproduce the approved front proportions: two .76m frame-centre widths, .98m centre spacing, 1.60m height, local base1.11m/top2.71m above the finished floor. This is the specific paired front design from StyledDetails07, not a redesign of the single arched WindowBay01. Curved-top sage shutters follow the approved approximately1.32m height; walnut, plaster and sage are transferred from the existing approved GouacheMaterialSheet_v02 artwork. Matte amber glazing is a stylized opaque painted surface matching the prototype language, not physically transparent glass. New weighted bevels, housed rails, rebated leaf framing, hinge straps, small latches, a sloped sill and independent support corbels establish reusable construction.

The shallow arched hood is a separate optional module, disabled by default: the approved front pair stays rectangular. It is provided for appropriate future arch-trim use without turning this bay into the old single arched window.

## Deliverables

Editable CM_PairedWindowBay02.blend:54 named source parts in11 logical collections, packed approved paint and baked atlas, attachment empties. build_paired_window_bay02.py reproduces the asset via bpy. Eleven FBX exports combine source parts into one mesh/material per independent component. Fourteen prefabs:11 components, insert assembly, full facade assembly and detachable reused botanical-card dressing. Unique2048 albedo atlas plus shared matte URP Lit material; separate neutral stage material. Four gizmo-free previews: Front, ThreeQuarter, GameplayDistance, RearReveals.

Main prefab: Assets/BlightBloom/Art/Architecture/CrookedMortar/PairedWindowBay02/Prefabs/CM_PairedWindowBay02.prefab. Components: FixedFrame, Casement_L/R, Shutter_L/R, Sill, PlanterBrackets, FlowerBox, ArchedHood_Optional, FacadeInfill_4p5m and WideHeader_4p5m. Shutters, casements, box, supports and plant dressing are independent. Connections exposes floor, floor-above, grid edges, hinges, sill and planter datums. Source pivots for casements/shutters are actual hinge datums. Source is authored closed for mesh editing; Unity prefabs pose shutters open153degrees. No runtime opening/animation system is added.

The optional botanical dressing is20 triangles/ten alpha-cutout cards using the existing approved CM06_BotanicalCards material/artwork. It is replaceable, uses no new plant texture and is outside the architectural FBX. It has no volume and casts no card shadows, as in the benchmark. Disable PlanterDressing independently for a bare asset.

## Triangle counts

| Configuration | Triangles |
|---|---:|
| Window insert, hood disabled, no plant cards | 6404 |
| Default window insert including20 plant-card triangles | 6424 |
| Optional shallow arch hood | +660 |
| Full default4.5m facade assembly, including reused posts and dressing | 7340 |
| Complete unique11-FBX library, including optional hood and host parts | 7512 |

Default insert has9 active MeshRenderers, one per architectural component plus dressing; no per-plank Unity renderers. Source parts remain separately editable. No LOD or runtime script is included.

## FacadeBay01 integration

Unit scale; +Y up, +Z exterior, pivot at floor-centre/exterior plaster datum. Floor rise3.24m; plaster .28m thick, frontZ=0/rearZ=-.28. Full host uses4.5m post-centre width (three1.5m grid increments), boundary posts atX+/-2.25, .18m section. It reuses existing FacadeBay01_Post_3p24m prefabs unchanged. New4.32m shoulder-length headers use the established .22m height/.42m depth; place them atY0 and3.02. Infill spansY.22..3.02.

Two genuine rough openings are .84m wide by1.69m tall, centred atX+/- .49, Y1.915. This pair is wider and rectangular, so it does not fit the existing1.6m single arched FacadeBay01 opening. Use the new host or a site-specific opening adapter. Do not overlay it on a solid wall or scale the original arched bay. Open shutters need approximately3.7m total visual width; a3m span cannot retain this open-shutter composition without crossing boundary framing. The4.5m host omits an intermediate post through the window and uses its wider header. Adjacent bays share one boundary post, never duplicate it. Do not place an intermediate post inside the paired openings.

Reference placement for eventual approved-front fitting is approximately(-.46,3.44,-4.2), yaw180; this is a measurement only, not an integration. The approved front wall is4.65m wide versus this4.5m grid host, so eventual installation requires approximately75mm custom return/infill per side or a dedicated4.65m host, preserving room/collider architecture. Roofs, entrance and existing wall meshes were not changed. The insert can be reused independently of the supplied host.

## Validation

All54 solid source parts:closed manifold edges, positive signed volumes, no degenerate geometry or UV triangles. Unique UV atlas has no positive-area triangle overlaps and stays within0..1. Density p05/median/p95 approximately195/206/215 pixels/metre at2048; small bevel islands vary. Existing paint transfer is editable and packed, not new native4K art. Normals recalculated/weighted and FBX render normals verified finite and normalized. All11 component import bounds agree with canonical source within0.000001m. Unit prefab roots, correct +Y/+Z orientation, single shared paint material per component, no missing components. Seven geometry-only opening probes confirm empty rough openings and solid adjacent plaster/central pier; no temporary colliders were needed. The review/prefabs have zero colliders or gameplay scripts. Unity compilation and Console checks show no new errors.

Front, three-quarter, rear reveal and gameplay-distance renders inspected in neutral lighting without fog, bloom or grading. This is a static art review, not a traversal test, animated casement implementation or final in-building installation. The overall paired composition/palette matches the approved benchmark; final artistic acceptance remains with you.

PreservationValidation.json records exact file inventory and hashes:all pre-existing project files preserved. No packages, gameplay/traversal/colliders or unrelated scenes modified. Roof work remains untouched. Nothing committed.
