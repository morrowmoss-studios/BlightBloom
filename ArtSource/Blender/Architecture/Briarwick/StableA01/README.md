# Stable A Review01 source

`BW_StableA01.blend` is the editable assembled prototype, with named shell, structure, roof, loft hatch, floor, foundation and three door meshes. Painted colour maps are packed for source inspection; Unity materials retain the original full texture sets read-only.

`build_stable.py` reads the existing inspected package mesh/material records in `../FamilyCottageA/Style01/` without changing them. Uses metres and the established FBX conversion (-Z forward, Y up). Reused Unity faces explicitly correct handedness before export. New boards use per-face UV mapping to native timber strips; original roof and door atlases remain registered. No texture-generation step is involved.

The builder refuses to overwrite its own model unless `--refine-own` is supplied. Partial-export flags in the script limit exports during its specific fitting operations. This is a source-generation utility, not a validator; do not rerun it merely to inspect the scene. `ModelCatalog.json` records material order, dimensions and fixed-open door transforms used by the Unity integration snippet.

Unity prefab and scene integration/validation are documented in `ArtSource/Pipeline/Review/BriarwickStableA01/README.md`. All approved cottage/Crooked Mortar/package assets are preserved. Visual approval is pending.
