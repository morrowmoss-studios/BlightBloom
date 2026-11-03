# Chapel01 editable source

Authoritative: `BW_Chapel01.blend`, metric/unit scale, Unity +Z frontage, floor+.12m relative to placement origin. Existing Blender FBX conversion -Zforward/Yup. Packed source base-color images.

Reproduction in a NEW authorized output workspace: run `ArtSource/Paint/Architecture/Briarwick/Chapel01/paint_chapel.py`, `build_chapel.py`, then `fit_roof.py`. The saved candidate already has restored roof eave closure. `refresh_paint.py` refreshes packed candidate painting after a texture revision; no geometry changes. Initial builder refuses to overwrite an existing source. Do not regenerate approved village assets.

Reuses read-only cottage source metadata, StableA02 helper definitions and Bakery02 continuous wall helper. Dedicated aperture bands, reveal, glass, masonry UVs and simple stone trim remain editable. `ModelCatalog.json` lists eleven FBX exports/material roles. Unity integration uses dedicated materials, static colliders and markers only. Review README and FinalIntegration.json document dimensions, checks and dependencies. No playable interior.
