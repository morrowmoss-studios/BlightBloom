# Blacksmith01 editable source

`BW_Blacksmith01.blend` is the current architectural review candidate. Metric source, Unity frontage +Z via established FBX -Z-forward/Y-up conversion. Meshes are grouped by construction role; working color images are packed. The actual Unity prefab owns collision and future interaction markers.

Reproduction only when required: `build_smithy.py` -> `finalize_local.py` -> `clear_road_approach.py` -> `repair_flue.py`, then review-folder `Integrate.cs`. Initial builder refuses an existing source; subsequent local adjustments are scoped to the new candidate. `FinishFloorCollider.cs` documents the continuous floor collider already included by the final integration recipe. Do not regenerate unchanged cottage, stable, bakery or Crooked Mortar assets.

Helpers/native UV extracts are read-only dependencies in the established FamilyCottageA, StableA02OpenFront and Bakery02 source folders. Texture source remains in the installed package plus existing project-owned bakery paintings; none was modified. `ModelCatalog.json` lists export roles/counts. See `ArtSource/Pipeline/Review/BriarwickBlacksmith01/README.md` for placement, dimensions, validations and limitations.
