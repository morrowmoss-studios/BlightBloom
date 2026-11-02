# Bakery01 editable source

Open `BW_Bakery01.blend` for the current review candidate. All visible meshes and source colors are editable; metric Blender +Z-up source exports with established FBX -Z-forward/Y-up conversion to Unity. Native package mesh/UV extracts and stable helper code are read-only dependencies.

Reproduction sequence (only if regeneration is needed):
1. Run `ArtSource/Paint/Architecture/Briarwick/Bakery01/paint_clay.py` and `prepare_plaster.py` with Pillow available.
2. Run `build_bakery.py` in Blender. It refuses to overwrite an existing candidate unless explicitly passed `--refine-own`.
3. Run `repair_plaster_normals.py` to normalize plaster UVs, clear imported custom normals and pack the cleaned plaster painting. It detects already normalized UVs.
4. Run `fit_door_leaves.py` to fit the two separate static leaves to actual wood bounds, avoiding hinge-bound offsets.
5. For a fresh Unity integration, run `Integrate.cs` then `FinalizeMaterials.cs` from the Bakery01 review folder in the existing Editor. Integrate deliberately refuses a duplicate active review root or existing derivative materials.

Do not regenerate unchanged previous buildings. The saved `.blend` is authoritative; no reconstruction of the bakery interior has been undertaken. See the review README for dependencies, dimensions, counts and limitations.
