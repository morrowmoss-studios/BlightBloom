# Crooked Mortar — Apothecary furnishings 01

First integrated ground-floor furnishing family for Production02. No gameplay interaction systems are implemented.

## Assets and sources

- 20 UV-mapped FBX modules; 26 reusable prefabs including six dressed stations; ten shared matte URP materials.
- Editable source: `CM_ApothecaryFurnishings01.blend`; reproducible modeling/export: `build_furnishings01.py`.
- Unity assets: `Assets/BlightBloom/Art/Interiors/CrookedMortar/ApothecaryFurnishings01/`.
- Shared approved architectural paint atlas is reused without modification. Authored botanical label/ledger artwork is preserved under `ArtSource/Paint/Interiors/CrookedMortar/ApothecaryFurnishings01/` as SVG and its drawing script.
- Models include counter, shelving, preparation bench, side table, instrument stand, examination couch, stool, washstand, cabinet, drying rack, scales, mortar/pestle, instrument tray, measuring tools, jars, bottles, stocked rows, ledger and linens. Existing approved herb bundles and potted sage are reused.

## Integration

Scene root: `17 Apothecary furnishings - production family 01`. Shop, treatment and preparation groups remain separate. Six previous ground-floor placeholder furnishings have their collision and baked visual objects disabled scene-locally; they are recoverable. Nine simple new furniture colliders block the substantial furniture only; small utensils and botanical dressing are non-obstructing.

Shop: 5.4 × 4.4 m. Treatment: 3.6 × 4.4 m. Preparation: 3.4 × 4.2 m. Floor elevation +0.20 m. Main room connections retain their 1.8/2.0 m widths. Sales counter runs along the shop west side, preserving approximately 1.1 m staff aisle and broad customer circulation. Treatment bed is on the east side with clinician and patient approach markers. Kitchen workbench keeps approximately 1.6 m of central surface available for future crafting poses. Stool is stowed against the rear wall.

Use/Customer/Shopkeeper/Clinician/PatientApproach transforms are planning markers, not interactions. All nine standing markers were checked using the unchanged 2 m high, 0.4 m radius player capsule. A future patient NPC and animation reach still need dedicated validation.

## Validation and review

See SourceValidation.json, UnityImportValidation.json, MarkerClearance.json and runtime reports for current checks. Previews contain room-level captures plus actual existing-player Game-camera views. Input-route tests use temporary input devices through the existing controller, not direct CharacterController movement. Automated route checks do not replace manual camera comfort approval.

Furniture drawers, cabinet doors, instruments and scales are static first-pass props. Glass is deliberately stylized; labels use simplified botanical symbols. No inventory, treatment, crafting or patient logic is included. Collider shapes are practical broad furniture envelopes rather than every leg and handle. Existing stair-camera behavior remains unchanged.

Do not rerun InstallAndIntegrate.cs over the integrated scene; it is the one-time guarded installation source. Use scoped module export when editing an individual asset.


### Current results

All 20 Blender modules passed UV/normal/finite-coordinate/degenerate-triangle checks (35,052 triangles across the unique library). Unity import has complete UV/normal arrays, assigned materials and no missing scene scripts. Live input routes reached 57 waypoints in total; no sampled camera sphere overlapped collision geometry. The existing camera retracted to 0.78–1.16 m minimum across the route tests and made six emergency corrections on stairs. This remains a manual comfort review item, not an asserted improvement. Normal walk/sprint speeds remained 3/6 m/s with visible animated skin and grounded samples. Console reported no new errors/warnings and no compilation failure.

All 99 original collider definitions are unchanged; six old furniture GameObjects are inactive. Nine new furnishing colliders are present. Scene diff confirms the only changes to existing objects are those six placeholders and six corresponding baked visual activation overrides; new furniture root/prefab instances were added. Shared gameplay, architecture, lighting, camera, doors, settings and approved assets were not edited.
