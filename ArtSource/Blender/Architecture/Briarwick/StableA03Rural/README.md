# Stable A03 editable source

Review candidate only. See `ArtSource/Pipeline/Review/BriarwickStableA03Rural/README.md` for validation, visual comparisons and the retained low-pitch historical compromise.

`BW_StableA03Rural.blend` was derived from A02 without overwriting it. Visible A02 body groups remain; the old roof copy is hidden in `REFERENCE_A02_WoodRoof_NOT_EXPORTED`. New covering, plain ridge and sparse joinery are editable meshes. Painting maps are packed for recovery; external working painting remains under `ArtSource/Paint/Architecture/Briarwick/StableA03Rural/`.

`refine_thatch.py` reuses A02 source and exports only the three A03 mesh groups. `--refine-own` explicitly permits updating this candidate; `--texture-fit` exports only thatch and joinery. Do not use this script to regenerate A01/A02 or approved cottage assets. `ModelCatalog.json` records reused body exports and placements, new groups and counts; original underlying ridge/overhang fields refer to A02 support structure, while the added coat extends above/beyond it.
