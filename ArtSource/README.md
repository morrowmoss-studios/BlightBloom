# BlightBloom Blender-to-Unity pipeline

Verified on this Mac: Blender 5.2.2 LTS at `/Applications/Blender.app/Contents/MacOS/Blender`, Unity 6000.4.5f1, October 16, 2026. No applications, plugins or Unity packages were installed for this validation.

## Recommended structure

```text
ArtSource/                              # Editable source, outside Unity's Assets importer
  Blender/Architecture/Apothecary/       # .blend masters when actual asset work begins
  Paint/Architecture/Apothecary/         # Layered painting masters and UV templates
  Pipeline/Tests/blender_probe.py       # Disposable geometry/export calibration
Assets/BlightBloom/Art/
  Architecture/Apothecary/
    Models/                             # Exported .fbx only, not editable .blend masters
    Materials/                          # Explicit URP materials
    Textures/                           # Published PNG/TGA maps
    Prefabs/                            # Render prefabs assembled in Unity
  _PipelineTests/Blender522Probe/        # Current disposable import test only
```

Production directories above are a convention, not populated assets. Only the test/import folders and this documentation/tooling have been created. Do not put .blend masters in Assets and depend on Unity launching Blender during import.

## Verified static export recipe

- Blender metric units, Unit Scale 1.0; one Blender unit = one metre.
- Authoring convention: +X right, +Y forward, +Z up. Unity convention: +X right, +Z forward, +Y up.
- Apply object rotation and scale. Define the asset origin deliberately; calibration root is at the body's feet.
- This Blender FBX exporter / Unity importer combination reverses source X/Y without an explicit conversion. On the export copy only, rotate objects 180 degrees around Blender Z and apply that rotation. Preserve the original editable source orientation.
- FBX: selected mesh objects, global scale 1, Apply Unit Scale enabled, `FBX_SCALE_UNITS`, forward -Z, up Y, space transform and bake-space-transform enabled, mesh modifiers applied, FACE smoothing, animation off, leaf bones off.
- The preset is validated for static architecture, not armatures or animation. Those require their own probe before use.
- Unity default ModelImporter was sufficient: globalScale 1, useFileScale true, fileScale 1. No project settings or existing importers were changed.

Do not simplify this to 'just export -Z/Y': the export-only orientation correction is part of the tested recipe. The saved calibration .blend is unconverted; conversion is applied only in the background export process and restored before glTF export.

## Repeat the calibration

Run the following outside the Codex sandbox/through an approved Blender execution:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python ArtSource/Pipeline/Tests/blender_probe.py -- /private/tmp/blightbloom-pipeline-validation
```

The script refuses foreground Blender and project-local output, uses factory startup, never saves user preferences, and writes only to the disposable external directory. It creates a .blend, .fbx, .glb, and JSON export report. Blender's glTF 2.0 GLB export uses its standard Y-up conversion; both formats were reimported into Blender successfully. The standard FBX axis preset initially failed the Unity left/right probe; the documented export conversion corrected it.

## Unity validation results

The existing Editor imported the FBX as a model asset; no objects were instantiated into any scene. Four mesh parts, 48 triangles total, UVs and outward normals retained. Body world bounds are (-0.5,0,-0.25) to (0.5,2,0.25), i.e. 1m wide, 2m tall, 0.5m deep. Axis-marker centres: right (1.5,0.1,0), forward (0,0.1,1.5), up (0,2.8,0). Floating-point tolerance 0.0001m. Imported root rotation zero and scale (1,1,1).

The GLB is a valid version-2 container and round-trips in Blender, but Unity currently imports it as DefaultAsset rather than a GameObject. No glTF importer is installed/enabled. Use FBX now; any glTF importer installation requires separate approval.

## Environment observations

The sandboxed headless process crashed before Python ran. The identical headless check and all exports succeeded outside the sandbox, exit code zero. Blender's desktop UI was not controlled or changed. Existing Unity Editor was used throughout.

One initial Unity import request exceeded Pipeline's 5-second dispatcher timeout, although import completed. Subsequent asset inspections/imports with a 30-second command timeout succeeded. The retained Console error is that automation timeout, not a mesh or C# compilation error. No Console entries were cleared.

All three scenes, package manifest/lock, and existing ProjectSettings files were hash-checked and unchanged. Apothecary stayed open, clean and in Edit mode. No gameplay work or window-bay modeling was performed.
