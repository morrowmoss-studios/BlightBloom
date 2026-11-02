# BW_Merchant01 editable source

Authoritative file: `BW_Merchant01.blend`. Metric, unit scale; Unity facade +Z, +Y up. Origin matches location05 terrain placement datum; planned floor is +0.15 m. All14 groups export asFBX with -Z forward / Y up using the established conversion.

Reproduction order, into a clean NEW output workspace: `build_merchant.py`, `simplify_ridge.py`, then `close_serving_recess.py`. The initial builder refuses to overwrite existing source. Do not rerun construction over approved assets. The latter scripts document two local corrections: removing an unnecessary raised ridge island and closing the serving recess. The saved Blender file already includes both.

Builders reuse read-only native mesh/UV metadata from FamilyCottageA/Style01 and helper definitions from StableA02OpenFront and Bakery02. No imported asset edits. Source color images are packed; Unity materials/textures remain separate, with exact dependencies in `ArtSource/Pipeline/Review/BriarwickMerchant01/FinalIntegration.json`. The matte ServingLining Unity material intentionally omits the source wood normal/metal maps.

`ModelCatalog.json` identifies the fourteen exports and material roles. Existing Unity prefab owns materials and static colliders, plus future attachment/approach markers; no new gameplay scripts. See review README for dimensions, tests and artistic limitations. Preserve this as a review candidate until approval.
