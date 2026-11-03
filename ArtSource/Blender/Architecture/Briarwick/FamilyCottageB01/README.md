# FamilyCottageB01 editable source

Authoritative source: `BW_FamilyCottageB01.blend`, metric/unit scale. Existing FBX conversion -Zforward/Yup; Unity+Zfront. Origin at original location11 ground datum; floor+.12m. Base-color images packed for editable reference.

`build_cottage_b.py` writes only this candidate and refuses to overwrite existing source. Reuses read-only cottage source metadata, StableA02 helper definitions, Bakery02 continuous-wall helper and the established layered shingle-patch method used by ElderCottage01/Inn01. It creates a different main volume, side profile and roof form; no approved building is modified. For regeneration use a separately authorized fresh output workspace.

`ModelCatalog.json` lists eleven grouped FBX exports and material roles. Unity materials and static colliders belong to the new prefab, with entry markers and no new gameplay scripts. See `ArtSource/Pipeline/Review/BriarwickFamilyCottageB01/README.md` and `GeometryValidation.json` for dimensions, dependencies, validation and limitations.
