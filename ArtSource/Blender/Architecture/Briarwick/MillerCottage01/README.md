# MillerCottage01 editable source

Authoritative source: `BW_MillerCottage01.blend`, metric, unit scale. Existing conversion: Blender FBX -Z forward/Y up, Unity +Z frontage. Pivot at original location08 ground datum; geometry includes +.12m planned floor offset.

`build_miller.py` reuses read-only cottage mesh/UV metadata, StableA02 helper definitions and Bakery02 continuous wall helper; writes only MillerCottage01. Refuses to overwrite existing candidate. `fit_timber.py` is the saved local correction to six flush tie/sill islands, guarded against duplicate application. Regeneration sequence into a fresh authorized workspace: build, then fit. Do not rerun over approved building sources.

Ten grouped FBX exports and material roles recorded in `ModelCatalog.json`. Packed source base-color images preserve editing references; authoritative Unity materials and exact dependencies listed in the review report/FinalValidation.json. No original package or other building edits.

See `ArtSource/Pipeline/Review/BriarwickMillerCottage01/README.md` for dimensions, tests, views and limitations. Review candidate only, no complete interior or mill mechanism.
