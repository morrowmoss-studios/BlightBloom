# ElderCottage01 editable source

Authoritative editable file: `BW_ElderCottage01.blend`. Metric/unit scale, established FBX -Zforward/Yup conversion; Unity+Zfront. Pivot at location06 ground datum; model floor offset+.12m. Source base-color images packed. Eleven FBX groups/material roles listed in `ModelCatalog.json`.

`build_elder.py` reuses read-only cottage mesh/UV metadata, StableA02 helper definitions and Bakery02 continuous wall helper. It builds only this candidate and refuses to overwrite existing source. Current script includes corrected half-hip clipping. `fit_hip_roof.py` records the local replacement of only RoofDeck/Shingles performed on the initial saved candidate; the current Blender file includes that correction. No need to rerun it for ordinary editing. Keep existing village sources untouched.

Wood roof uses Inn01’s existing shingle atlas, layered patches clipped to the half-hip surfaces and a closed deck. The source is editable as grouped meshes. Unity materials/colliders are owned by the new prefab; no new gameplay components. See `ArtSource/Pipeline/Review/BriarwickElderCottage01/README.md` for measurements, validations, dependencies and remaining limitations.
