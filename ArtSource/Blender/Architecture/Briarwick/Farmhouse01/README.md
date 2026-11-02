# Farmhouse01 editable source

Authoritative editable model: `BW_Farmhouse01.blend`. Metric scale; established Blender→FBX conversion (-Zforward/Yup, Unity+Zfront). Origin at location07 ground datum; model includes +.12m floor offset. Source color textures packed; Unity materials separate.

`build_farmhouse.py` constructs only Farmhouse01 using existing native mesh/UV helpers (StableA02OpenFront), continuous wall helper (Bakery02), and cottage source metadata. Refuses to overwrite an existing source. `fit_gables.py` performs the saved candidate's local roof/gable trim and recessed backing correction; guarded against duplicate application. Regeneration order in a new authorized output workspace: build, then fit. Do not regenerate approved village buildings.

`ModelCatalog.json` maps twelve mesh groups to FBX exports and material roles. `ArtSource/Pipeline/Review/BriarwickFarmhouse01/README.md` contains dimensions, validation, dependencies and remaining limitations. No complete interior or gameplay behavior is included.
