# Cottage A Style01 editable source

`BW_FamilyCottageA_Style01.blend` contains an assembled preview, editable derivative meshes at native pivots, packed painted colour maps, and a hidden original-geometry reference collection. Imported package files remain the authoritative untouched original materials and geometry.

`SourceMeshReadOnly.json` records the actual Unity source mesh vertices, UVs and material roles; `SourceMaterials.json` records package texture dependencies. `paint_atlases.py` uses Pillow/numpy to create registered painted albedo and linear metallic/smoothness derivatives. Optional role arguments update only those textures (for example `roof`). No AI artwork or unrelated asset regeneration is required.

`refine_cottage.py` runs in Blender 5.2.2 LTS. Metric scale, established Unity (x,y,z) → Blender (-x,-z,y), FBX -Z forward / Y up, baked conversion. FBX round-trip positions/pivots and material assignments were checked. `GeometryManifest.json` records first-face export material order, which can differ from the original slot order after beveling. Unity integration must use that order.

The full modeling script rebuilds **this derivative only**; do not run it as part of ordinary scene validation. Its `--entrance-only` option exports the entrance and unchanged-topology gable variants without rewriting the other five exports. Current gables retain original topology; beveling their thin/open panels was rejected. `preserve_open_panels.py` and `read_export_layout.py` document the diagnostic path, but are not part of final regeneration and should not be run as routine validators.

The scene has 27,920 rendered triangles including its existing approach. Scene-local fitted adjacent-panel transforms are documented in `ArtSource/Pipeline/Review/FamilyCottageAStyle01/README.md`. No new playable interior or door interaction is included.

For later refinement, preserve the source package, atlas layout and real controller dimensions. Do not copy Crooked Mortar's fused atlas onto this modular geometry. Artistic approval of this first pass is pending.
