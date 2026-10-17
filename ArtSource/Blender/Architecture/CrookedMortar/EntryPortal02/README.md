# CM_EntryPortal02 — review candidate

Created against measured geometry from CM_CrookedMortar_B_StyledDetails07. The approved scene is unchanged. This is the entrance framing module, not a replacement door, canopy, sign, lantern or herb assembly.

## Deliverables
- Editable `CM_EntryPortal02.blend`, with original approved paint image and baked atlas packed inside.
- Repeatable `build_entry_portal02.py`; refuses existing outputs unless explicitly passed `--refine-new-asset`.
- FBX, 2048-square painted walnut base-colour atlas, matte URP Lit material and modular prefab in `Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/`.
- New scene `Assets/Scenes/CM_EntryPortal02_ArtReview.unity`; four actual Unity renders in `Previews/`.
- Measurement, geometry, UV, paint-transfer and Unity validation JSON reports; UV SVG template.
- Unity automation snippets under `ArtSource/Pipeline/Review/`: CreateEntryPortal02Review.cs, ValidateEntryPortal02.cs, CaptureEntryPortal02.cs. These are evaluation snippets outside Assets, not gameplay scripts.

## Construction / import
12 logical LOD0 mesh parts: paired posts, open socket base shoes, mortised caps, concealed tenons and octagonal pegs; continuous outer curved timber and smaller inner curved trim. Small bevels and controlled <=3mm post irregularity retain the measured silhouette. Parts remain separate for editing and material replacement.

LOD0: 3,272 triangles. LOD1: 1,798 triangles; joined distance mesh. Unity LOD transitions: .18 and .008 screen-relative height. Material is a single shared matte atlas material. FBX preserves source semantic slots, all mapped to that material in the prefab.

Metric source, 1 Unity unit = 1 metre, +Y up, +Z exterior/front. Root scale is one. FBX uses the established export-only axis conversion; editable Blender source is saved before export conversion. Imported dimensions: 2.43m wide x 2.98m tall x .221m deep. Minimum timber starts .02m above the origin, matching the approved stoop relationship.

UV0 is a unique shared atlas with zero positive-area overlaps, within 0..1. Averaged physical island scale: p05/p50/p95 approximately 567/597/633 pixels per metre at 2048; bevel surfaces account for some local variation. PaintProjection is a second editable source-paint UV layer, including curved grain mapping. Approved walnut quadrant of GouacheMaterialSheet_v02.png supplies broad painted colour/grain; no procedural noise or image blur. Atlas resolution does not imply new native 2K brush detail: it rebakes existing approved artwork at consistent asset scale. No normal map or gloss map added.

## Prefab attachment contract
`Attachments_Replaceable_EmptySockets` contains 13 explicitly named sockets. Positions, rotations and purposes are in AttachmentPoints.json. DoorModule_RearRecess is **3.32m behind** the front portal, matching the approved recessed entrance; it is not a door mounted in the front arch. Sign bracket and canopy herb-line sockets require the existing building/canopy structure; they must not be interpreted as load-bearing connections to the freestanding arch. Lantern sockets are the approved lantern body pivots. Side herb sockets must retain central headroom.

The prefab is render-only, has no gameplay scripts and no colliders. Existing gameplay/collision remains authoritative until a separately approved integration. Decorative attachments are deliberately not baked into the portal mesh.

## Review / validation
Open CM_EntryPortal02_ArtReview in Unity. It contains the prefab, neutral stage, camera and two lights. No bloom, fog or blur. The inactive Approved07_VisualContext_ONLY_NoScriptsOrColliders group is a renderer-only contextual copy, with old portal proxies excluded; toggle it to inspect fit. It contains no copied gameplay behaviours or colliders. Existing decoration remains contextual, not part of the new module. Preview captures reset to isolated three-quarter view after rendering.

All 12 source parts and LOD1: closed manifold surfaces, positive signed volumes, zero degenerate triangles. Imported meshes have complete UV/normal arrays, valid normals and no missing mesh/material references. Unique UV0 overlap audit: zero overlaps. Unit scale/orientation checked through imported bounds and actual Unity renders.

Temporary mesh colliders were generated only during clearance testing, then destroyed. A 2m-height, .4m-radius CharacterController with .04m skin traversed 3.2m through the opening at x=0 and +/- .45m, with zero side collisions. Clear widths are 1.99m at base shoes and 2.055m between posts; central headroom to the inner trim is 2.7225m. This is a portal clearance test, not a new full-building traversal certification.

Unity compilation completed with zero current Console errors. Existing unrelated warnings remained; no new portal warning was captured. No packages installed and nothing committed.

Before integration: approve the new framing/paint appearance in context, then validate final attached decoration against head clearance and the destination's existing collision setup. Production review should also inspect LOD transitions at the intended display resolution. The approved scene has not been integrated or changed.
