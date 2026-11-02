# Stable A open-front source

`BW_StableA02OpenFront.blend` contains the three-bay open-front revision. `build_open_stable.py` derives from Review01's established builder without changing its files. It retains the native texture atlas mapping, metric scale, handedness correction and FBX export convention.

Only changed groups export to the new asset folder. `ModelCatalog.json` points unchanged Floor, LoftHatch and HumanDoor groups to Review01 FBXs; the human door's new placement is on the side of the tack room. Materials remain existing Review01 shared assets. The source file includes these components for editing even though Unity reuses the unchanged exports.

The builder refuses accidental regeneration unless `--refine-own` is supplied. It is not a validation utility. Read `ArtSource/Pipeline/Review/BriarwickStableA02OpenFront/README.md` for scene integration, dimensions, comparisons and tests. Previous closed-barn sources are preserved. Visual approval pending.
