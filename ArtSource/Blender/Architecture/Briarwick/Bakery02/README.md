# Bakery02 source

Authoritative review source: `BW_Bakery02.blend`. Preserves Bakery01 unchanged. Metric Blender coordinates, established -Z-forward / Y-up FBX export. Changed wall/roof/timber/oven groups are new; unchanged door/window/foundation/threshold meshes remain in the editable source and reference existing Bakery01 exports in Unity.

Reproduction, only when needed: run Bakery02 paint `prepare_plaster.py`, `reconstruct_bakery.py` once, `refine_tiles_and_joinery.py` once, then `finish_winding.py`. Initial reconstruction deliberately refuses an existing candidate. Use the saved editable source for routine manual changes; do not regenerate approved buildings or Bakery01.

The oven is a simplified internal source-derived chamber, not finished baking equipment. Clay tiles are open overlapping visual surfaces above the collision roof deck, with the chimney penetration inside its masonry footprint. See `ArtSource/Pipeline/Review/BriarwickBakery02/README.md` for counts, validation, dependencies and remaining limits.

Latest approved gable cleanup: run `remove_applied_gable_beams.py` after the earlier reconstruction steps when reproducing the current candidate. It removes only four identified timber islands, guards against repeated cleanup, and preserves the previous timber in `REFERENCE_BeforeGableCleanup_NOT_EXPORTED`. No other geometry or material changes.
