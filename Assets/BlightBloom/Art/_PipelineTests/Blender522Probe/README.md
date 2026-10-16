# Disposable Blender import probe

Calibration only; not used by scenes or gameplay. FBX imports natively with four mesh parts/48 triangles, outward normals and UVs. Body = 1 x 2 x 0.5 metres, root rotation zero, root scale one. Right/forward/up marker centres match Unity +X/+Z/+Y using the tested export-only conversion documented in `ArtSource/README.md`.

GLB is intentionally retained as a capability check: it imports as DefaultAsset because no glTF model importer is configured. Nothing was installed.

Editable test source, original exports and JSON report remain outside the Unity project in `/private/tmp/blightbloom-pipeline-validation`. This folder contains only copies of the two exports and their Unity metadata. It can be removed as a unit after review; no removal was performed.
