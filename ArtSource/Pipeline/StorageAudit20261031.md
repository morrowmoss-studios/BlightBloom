# BlightBloom — storage audit and cleanup proposal

Audit date: 2026-10-31 (local). **READ-ONLY AUDIT; NO CLEANUP AUTHORIZED OR PERFORMED.** The sole new file is this requested Markdown report. No existing file was intentionally written, moved, compressed or deleted. No Unity/Blender launch, reimport, validation, Git cleanup, commit or push. Existing application writes can continue independently.

## Findings and achievable savings

- Filesystem capacity: **245.107 GB (228.27 GiB)**; currently available: **1.048 GB (0.98 GiB)**. Availability improved from the earlier 115 MB report before this audit; no cleanup was performed here. APFS uses shared container space/snapshots, so used and available need not subtract directly from capacity.
- Project regular files: **17.881 GB logical / 18.003 GB allocated**, excluding directory metadata and symlink targets. The earlier 17.52 GB figure is approximate; current measurement includes `.git`. GB = decimal billion bytes; GiB = binary.
- Largest consumers: `.git` (protected history), ArtSource (primarily editable Blender snapshots), then Unity Library (regenerable). Assets itself is small.
- Low-disruption cache/log candidates total at most **2.069 GB allocated**, conditional on closing writers and resolving pending updates; retaining current logs reduces that slightly. Library adds **3.824 GB**, giving **5.893 GB** cache-only potential. Library requires a complete reimport and much of that space returns. It is not a durable source of working headroom.
- Codex staged application adds **2.009 GB conditionally**, but its active updater state could not be certified; excluded from conservative savings.
- Documented superseded exterior Blender intermediates add **2.051 GB allocated** (2.051 GB logical), **archive-first**, not safe-delete approved. They remain linked by historical repair scripts.
- **10 GB cannot currently be promised as safely disposable storage.** All cache/log, staged-update and archive candidates together approach **9.953 GB**, but that is a conditional ceiling, not a safe recovery commitment. It includes a disruptive Library rebuild, unverified updater staging and source archiving. No nested directory or duplicate-copy savings are added again.

## Project and Unity storage

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `.` | 17.881 GB | 18.003 GB | 43407 |
| `.git` | 7.026 GB | 7.044 GB | 6000 |
| `ArtSource` | 6.880 GB | 6.884 GB | 1901 |
| `Assets` | 233.76 MB | 237.67 MB | 1610 |
| `Library` | 3.729 GB | 3.824 GB | 33629 |
| `Logs` | 3.88 MB | 4.50 MB | 15 |
| `Packages` | 15.2 KB | 20.5 KB | 2 |
| `ProjectSettings` | 58.2 KB | 135.2 KB | 25 |
| `Temp` | 7.86 MB | 8.25 MB | 211 |
| `UserSettings` | 94.1 KB | 110.6 KB | 6 |

Library subdirectories are explanatory breakdowns, not extra savings:

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `Library/APIUpdater` | 2.35 MB | 2.94 MB | 171 |
| `Library/Artifacts` | 1.864 GB | 1.873 GB | 4807 |
| `Library/Bee` | 136.80 MB | 138.70 MB | 1057 |
| `Library/BuildProfiles` | 6.7 KB | 16.4 KB | 4 |
| `Library/BurstCache` | 103.07 MB | 103.89 MB | 418 |
| `Library/PackageCache` | 1.494 GB | 1.573 GB | 26165 |
| `Library/PackageManager` | 175.9 KB | 184.3 KB | 3 |
| `Library/Pipeline` | 769.8 KB | 774.1 KB | 2 |
| `Library/PlayModeViewStates` | 2.4 KB | 4.1 KB | 1 |
| `Library/ScriptAssemblies` | 28.39 MB | 28.71 MB | 150 |
| `Library/Search` | 27.59 MB | 27.64 MB | 9 |
| `Library/ShaderCache` | 4.53 MB | 6.36 MB | 805 |
| `Library/StateCache` | 3.2 KB | 20.5 KB | 5 |
| `Library/UIElements` | 0.6 KB | 4.1 KB | 1 |
| `Library/com.unity.ide.rider` | 0.5 KB | 4.1 KB | 1 |

`Library/Artifacts`, `Library/Bee`, `Library/BurstCache`, `Library/ScriptAssemblies`, `Library/Search` and shader caches are generated. `Library/PackageCache` is extracted package content; recovery depends on manifests/lockfiles, registry access and credentials. Do not remove the Library while Unity is open, and do not begin a full reimport with only ~1 GB free. Save work and close Unity first if a later cleanup is approved. Retain `Packages/`, `ProjectSettings/`, all `Assets/`, metadata and `.git/`. `Temp/` is disposable only after Unity closes. Logs are regenerable but current diagnostics are useful. `UserSettings/` contains user preferences: retain. `Obj`, `obj`, `Build`, `Builds`, `.vs`, `MemoryCaptures` and `Recordings` are absent at project root.

## ArtSource breakdown

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `ArtSource/Blender` | 6.862 GB | 6.866 GB | 1794 |
| `ArtSource/Blender/Architecture` | 332.57 MB | 333.48 MB | 399 |
| `ArtSource/Blender/Characters` | 44.91 MB | 45.23 MB | 145 |
| `ArtSource/Blender/Exteriors` | 4.440 GB | 4.441 GB | 417 |
| `ArtSource/Blender/Interiors` | 2.044 GB | 2.046 GB | 832 |
| `ArtSource/Paint` | 17.51 MB | 17.60 MB | 37 |
| `ArtSource/Paint/Architecture` | 10.88 MB | 10.94 MB | 25 |
| `ArtSource/Paint/Interiors` | 6.63 MB | 6.66 MB | 12 |
| `ArtSource/Pipeline` | 812.8 KB | 950.3 KB | 68 |
| `ArtSource/Pipeline/.idea` | 4.4 KB | 24.6 KB | 6 |
| `ArtSource/Pipeline/Review` | 247.0 KB | 360.4 KB | 57 |
| `ArtSource/Pipeline/Tests` | 4.0 KB | 4.1 KB | 1 |

### Crooked Mortar exterior

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `ArtSource/Blender/Exteriors/CrookedMortar` | 4.440 GB | 4.441 GB | 417 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01` | 1.096 GB | 1.096 GB | 158 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Comparisons` | 57.10 MB | 57.20 MB | 45 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Exports` | 61.16 MB | 61.17 MB | 6 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/RejectedTests` | 250.23 MB | 250.34 MB | 58 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures` | 15.74 MB | 15.75 MB | 4 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/UnityPreviews` | 3.13 MB | 3.15 MB | 7 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01` | 3.344 GB | 3.345 GB | 259 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/BoundaryMapping01` | 337.51 MB | 337.58 MB | 38 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/BoundaryMapping02` | 329.07 MB | 329.21 MB | 62 |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01` | 2.512 GB | 2.512 GB | 149 |

The original house GLB is actually in the older Architecture tree, not `Exteriors/TripoImports`: `ArtSource/Blender/Architecture/CrookedMortar/TripoImports/storybook cottage 3d model.glb` (**69.20 MB**). The cabinet GLB is `ArtSource/Blender/Interiors/CrookedMortar/TripoImports/rustic wooden cabinet 3d model.glb` (**68.12 MB**). Both protected.

| TerrainSeparation01 contents | Logical size |
| --- | --- |
| Comparison renders and review images | 83.93 MB |
| Analysis arrays, reports, scripts and other support | 24.69 MB |
| Superseded intermediate Blender snapshots | 1.891 GB |
| Texture/normal source and local returns | 14.43 MB |
| Final candidate + its previous-save backup | 344.37 MB |
| Uncut task-start safety source | 153.95 MB |

`RejectedTrials/` inside TerrainSeparation01 is under 1 MB; most rejected heavy snapshots are at the parent level. Recovery `RejectedTests/` totals 250.23 MB, including one 160.59 MB Blender experiment and diagnostic renders. Recovery `Comparisons/` is 57.10 MB, `Exports/` 61.16 MB, and `Textures/` 15.74 MB. Keep approved comparison evidence for now. Transport exports are reproducible but are explicit inputs to validation/Unity-preparation scripts; not orphan files.

### Interior sources

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `ArtSource/Blender/Interiors/CrookedMortar/ApothecaryFurnishings01` | 12.71 MB | 12.78 MB | 27 |
| `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow07` | 59.74 MB | 59.83 MB | 45 |
| `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08` | 51.91 MB | 52.02 MB | 42 |
| `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow09` | 30.75 MB | 30.81 MB | 27 |
| `ArtSource/Blender/Interiors/CrookedMortar/Craftsmanship05` | 27.28 MB | 27.37 MB | 41 |
| `ArtSource/Blender/Interiors/CrookedMortar/EntranceWorkflow11` | 38.19 MB | 38.28 MB | 38 |
| `ArtSource/Blender/Interiors/CrookedMortar/HeroRefinement02` | 21.63 MB | 21.70 MB | 35 |
| `ArtSource/Blender/Interiors/CrookedMortar/Illustrated04` | 43.42 MB | 43.55 MB | 54 |
| `ArtSource/Blender/Interiors/CrookedMortar/LivedIn03` | 33.26 MB | 33.36 MB | 49 |
| `ArtSource/Blender/Interiors/CrookedMortar/MasterMedicineCabinet01` | 44.97 MB | 45.06 MB | 37 |
| `ArtSource/Blender/Interiors/CrookedMortar/Reconstruction06` | 46.00 MB | 46.16 MB | 67 |
| `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow10` | 32.72 MB | 32.83 MB | 49 |
| `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow12` | 26.55 MB | 26.64 MB | 41 |
| `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow13` | 58.29 MB | 58.43 MB | 70 |
| `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow14` | 50.12 MB | 50.26 MB | 58 |
| `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetRecovery01` | 481.37 MB | 481.49 MB | 64 |
| `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetStyle02` | 415.19 MB | 415.26 MB | 35 |
| `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetStyle03` | 501.96 MB | 502.07 MB | 50 |
| `ArtSource/Blender/Interiors/CrookedMortar/TripoImports` | 68.12 MB | 68.12 MB | 1 |

Cabinet recovery/style experiments account for much of the remaining source storage, but this audit does not establish any of them as obsolete. Preserve the current cabinet, prior editable artwork and working review scenes. No blanket deletion of Workflow07–14 or cabinet source families is recommended.

## Assets breakdown

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `Assets/BlightBloom` | 217.77 MB | 221.43 MB | 1521 |
| `Assets/Scenes` | 11.39 MB | 11.51 MB | 42 |
| `Assets/Settings` | 69.6 KB | 110.6 KB | 14 |
| `Assets/Tools` | 4.43 MB | 4.45 MB | 11 |
| `Assets/TutorialInfo` | 51.0 KB | 81.9 KB | 11 |

Additional useful Art breakdown:

| Directory (relative to project) | Logical size | Allocated file blocks | Files |
| --- | --- | --- | --- |
| `Assets/BlightBloom/Art` | 215.20 MB | 218.58 MB | 1432 |
| `Assets/BlightBloom/Art/Architecture` | 100.17 MB | 101.95 MB | 766 |
| `Assets/BlightBloom/Art/Exteriors` | 40.60 MB | 40.67 MB | 32 |
| `Assets/BlightBloom/Art/Interiors` | 74.43 MB | 75.95 MB | 631 |
| `Assets/BlightBloom/Characters` | 2.46 MB | 2.59 MB | 42 |
| `Assets/BlightBloom/Characters/PlagueDoctor01` | 2.46 MB | 2.59 MB | 41 |
| `Assets/BlightBloom/Locations` | 19.1 KB | 36.9 KB | 5 |
| `Assets/BlightBloom/Locations/Editor` | 12.7 KB | 20.5 KB | 2 |
| `Assets/BlightBloom/Prototypes` | 65.5 KB | 139.3 KB | 26 |
| `Assets/BlightBloom/Prototypes/CrookedMortarProduction02` | 16.1 KB | 20.5 KB | 2 |
| `Assets/BlightBloom/Prototypes/CrookedMortarUsability01` | 49.0 KB | 110.6 KB | 22 |
| `Assets/BlightBloom/Traversal` | 23.6 KB | 57.3 KB | 11 |
| `Assets/BlightBloom/Traversal/Editor` | 6.3 KB | 12.3 KB | 2 |

All existing scenes, prefabs, reusable kits, scripts, materials and texture assets remain protected regardless of Production02 reachability. No asset-removal proposal is made.

## Dependency and Git findings

Static GUID traversal from Production02 reaches **306 Assets paths**. Serialized scenes, prefabs, materials, controllers, assets and importer metadata were read. No directly imported `.blend` files exist under Assets. Exterior recovery FBX is referenced by the exterior prefab, and House_Normal.png by its URP material; neither is a Production02 dependency, but both are protected and remain needed by the approved exterior preview. ArtSource filenames are not Unity GUID imports; absence from Production02 therefore does **not** establish dispensability. Dynamic resource loading, binary Blender linked libraries/packed dependencies, package GUID resolution and live Unity AssetDatabase checks were not performed. No Unity missing-reference conclusion is claimed.

Terrain intermediates have explicit script dependencies: `apply_section.py` loads the preceding Stage file, `close_openings*.py` loads Stage05, `close_safe_openings.py` loads SafeSeparated_UNCAPPED, and `finish_safe_repairs.py` loads SafeSeparated_CLOSURES. Other inspection/sampling scripts load WORKING or UNCut recovery. Final capture/validation scripts read the final candidate directly. Moving the intermediates can preserve current test/export work but breaks historical reruns unless their relative tree is restored. `SourceTextureReadOnlyCopy_*` files are referenced in SourceTextureInspection.json. Exported FBX/GLB and their textures are read by recovery validation/preparation. Keep them pending explicit path/packed-image verification.

Current normal checkpoint is **`196e485`**, main/origin main. Important exterior `.blend` files and the standalone directory are currently **untracked** at that checkpoint. Read-only Git object mapping also found these versions in **auxiliary `refs/codex/turn-diffs/...` snapshots**. That explains large loose Git objects; it does not mean these sources are in the approved normal commit. Do not rely on auxiliary snapshots as the only durable backup. No refs, objects, index, packs, LFS content or history are cleanup targets. Never manually delete individual `.git/objects/*` files. Removing working copies does not reclaim their Git-history storage. No Git GC, prune or repack proposed.

## Largest 30 individual files

| # | Filename | Relative path | Logical / allocated | Type | Purpose | Reference evidence | Handling |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Stage01.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage01.blend` | 172.32 MB / 172.32 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 2 | `CM_CrookedMortar_TerrainSeparated01.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend` | 172.18 MB / 172.18 MB | .blend | Approved working Unity-test candidate | Active source for pending standalone export | C: retain protected source |
| 3 | `CM_CrookedMortar_TerrainSeparated01.blend1` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend1` | 172.18 MB / 172.18 MB | .blend1 | Previous save of approved candidate | Recovery value; different bytes from final | C/D: retain; optional verified external backup only |
| 4 | `Stage02.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage02.blend` | 172.06 MB / 172.06 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 5 | `CM_CrookedMortar_TerrainSeparation01_WORKING.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend` | 172.03 MB / 172.03 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 6 | `Stage03.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage03.blend` | 172.02 MB / 172.03 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 7 | `Stage04.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage04.blend` | 171.90 MB / 171.90 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 8 | `SafeSeparated_CLOSURES.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend` | 171.81 MB / 171.81 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 9 | `SafeSeparated_UNCAPPED.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend` | 171.78 MB / 171.79 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 10 | `SafeSeparated_CLOSURES.blend1` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend1` | 171.76 MB / 171.77 MB | .blend1 | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 11 | `SafeSeparated_UNCAPPED.blend1` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend1` | 171.73 MB / 171.73 MB | .blend1 | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 12 | `CM_CrookedMortar_TerrainSeparation01_WORKING.blend1` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend1` | 171.67 MB / 171.67 MB | .blend1 | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 13 | `Stage05.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage05.blend` | 171.62 MB / 171.62 MB | .blend | Intermediate terrain-separation stage/repair snapshot | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 14 | `54328c314095eb11dc129ea58a32fdd98294f3` | `.git/objects/5d/54328c314095eb11dc129ea58a32fdd98294f3` | 170.03 MB / 170.03 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage01.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 15 | `fbc8bdde0c053edac1577e44e1984af45ad8cd` | `.git/objects/14/fbc8bdde0c053edac1577e44e1984af45ad8cd` | 169.90 MB / 169.91 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 16 | `524ff723e4354a98d2f7c742739c4631d9fb0a` | `.git/objects/1d/524ff723e4354a98d2f7c742739c4631d9fb0a` | 169.90 MB / 169.91 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend1` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 17 | `f54f296d36e920a3bbec69d8f1c6f0aad62731` | `.git/objects/61/f54f296d36e920a3bbec69d8f1c6f0aad62731` | 169.77 MB / 169.77 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage02.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 18 | `73af9a577b9adee2644fda87751010592645c9` | `.git/objects/5c/73af9a577b9adee2644fda87751010592645c9` | 169.75 MB / 169.75 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 19 | `1474dd509e59fdd99389b1b267dbf9cb74d842` | `.git/objects/26/1474dd509e59fdd99389b1b267dbf9cb74d842` | 169.74 MB / 169.74 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage03.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 20 | `0cc2f4b33f9f5c908469226ff73e1807cad2f7` | `.git/objects/f4/0cc2f4b33f9f5c908469226ff73e1807cad2f7` | 169.62 MB / 169.62 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage04.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 21 | `863bdae81206e43267723a5ba5cdbcb802e6ee` | `.git/objects/1a/863bdae81206e43267723a5ba5cdbcb802e6ee` | 169.54 MB / 169.54 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 22 | `375f782e975ae208a1cb871f73c28bce839ebe` | `.git/objects/2e/375f782e975ae208a1cb871f73c28bce839ebe` | 169.50 MB / 169.50 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 23 | `43b34c5e00ed3c24362c15fb9c420ea19f81df` | `.git/objects/b1/43b34c5e00ed3c24362c15fb9c420ea19f81df` | 169.49 MB / 169.49 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend1` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 24 | `2a70f9ddd4611e89b0757438d1282715618a10` | `.git/objects/dc/2a70f9ddd4611e89b0757438d1282715618a10` | 169.46 MB / 169.46 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend1` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 25 | `bebdecabdc38b88614fdb88a9184c96eaffade` | `.git/objects/f2/bebdecabdc38b88614fdb88a9184c96eaffade` | 169.40 MB / 169.40 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend1` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 26 | `0ca369bcbcb0d66c0ce2a0b4eb1f0483a6aa37` | `.git/objects/39/0ca369bcbcb0d66c0ce2a0b4eb1f0483a6aa37` | 169.34 MB / 169.35 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage05.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 27 | `Rejected_UnscaledReduction.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/RejectedTests/Rejected_UnscaledReduction.blend` | 160.59 MB / 160.59 MB | .blend | Rejected reduction trial | No direct Unity import; historical Blender scripts reference intermediate stages | B: verified external archive first; dependency/backup approval before removal |
| 28 | `51d12a9334fbf33cfbdbbf2f4f6c81f3ec9cc1` | `.git/objects/d6/51d12a9334fbf33cfbdbbf2f4f6c81f3ec9cc1` | 158.49 MB / 158.49 MB | Git compressed object | History/snapshot blob: `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/RejectedTests/Rejected_UnscaledReduction.blend` | Reachable from all-ref history; not a Unity runtime asset | C: retain Git history; never delete object |
| 29 | `CM_CrookedMortar_BoundaryMapping02_UNCUT.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/BoundaryMapping02/CM_CrookedMortar_BoundaryMapping02_UNCUT.blend` | 153.95 MB / 153.96 MB | .blend | Approved uncut boundary reference | Protected inspection/validation reference | C: retain; optional external archive only with stable access |
| 30 | `CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend` | `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_UNCUT_RECOVERY.blend` | 153.95 MB / 153.96 MB | .blend | Untouched task-start recovery source | Historical repair/selection scripts read it | C: retain safety source; not duplicate |

Top 30 includes `.git` because the request covers the whole project; Git objects are on-disk compressed blobs, not duplicate removable exports. No large source was classified disposable merely by filename.

## SHA-256-confirmed identical content

Compared **65** equal-length source/runtime files of at least 1 MB under ArtSource and Assets. Same size was only a candidate filter; SHA-256 establishes byte identity. No `.blend`/`.blend1` duplicate was confirmed. Potential repeated bytes across these groups total **121.66 MB**, but this is **not** deletion savings: source/export roles, distinct GUIDs, renderer material links and historical scripts require many copies. Not added to totals. Git/cache contents and files below 1 MB were not duplicate-audited.

- **6.04 MB each**, SHA-256 `0d1421753a299ed0e3a593a3211e047bf4c7349bc43dc84d39e667d6c45a3775`.
  - `Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/House_Normal.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SourceTextureReadOnlyCopy_storybook_cottage_3d_model_normal.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/Original_02.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Exports/CM_CrookedMortar_ExteriorRecovery01.fbm/Original_02.png` — retained source/export/review or other-asset role

- **5.52 MB each**, SHA-256 `5664119a4cd81d366d8d6741a3fae82510e46eb2092385955532f3240360e364`.
  - `Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/House_BaseColor.jpg` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SourceTextureReadOnlyCopy_storybook_cottage_3d_model_basecolor.jpg` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/Original_00.jpg` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Exports/CM_CrookedMortar_ExteriorRecovery01.fbm/Original_00.jpg` — retained source/export/review or other-asset role

- **15.53 MB each**, SHA-256 `bea2c36c5f7c5d84bcac920f1fd930cb2bffc71200bd00fe6ef13be6b63ecab5`.
  - `Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Models/CM_CrookedMortar_ExteriorRecovery01.fbx` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Exports/CM_CrookedMortar_ExteriorRecovery01.fbx` — retained source/export/review or other-asset role

- **2.00 MB each**, SHA-256 `0e67925f5aa56a395d2fd02cc95e1ef1a43874ea6f0b873e53a05c28fb9669cf`.
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/Production01/Textures/CM_Production01_ApprovedPaint.png` — Production02 static dependency
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/SlateRoofKit01/Textures/CM_SlateRoofKit01_ApprovedPaintSheet.png` — Production02 static dependency
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/BotanicalPlanterKit01/Textures/CM_BotanicalContainerPaint01.png` — Production02 static dependency
  - `ArtSource/Paint/Architecture/CrookedMortar/WindowBay01/Sources/GouacheMaterialSheet_v02.png` — retained source/export/review or other-asset role

- **1.67 MB each**, SHA-256 `5ae6bcc6d5fc5b573780dfdfc4e2c20f46d1b97aa65a35920c40e2a212cc713d`.
  - `Assets/BlightBloom/Art/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/Sign_Walnut.png` — retained source/export/review or other-asset role
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/EntryPortal02/Textures/CM_EntryPortal02_Walnut_BaseColor.png` — Production02 static dependency
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/Sign_ApprovedWalnut.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Exports/CM_CrookedMortar_ExteriorRecovery01.fbm/Sign_ApprovedWalnut.png` — retained source/export/review or other-asset role

- **2.40 MB each**, SHA-256 `a81cb1fa05b8ee95cde8bc4564195bc6bc2dc4806cad285dd4f24de0a73dd1ce`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Textures/CM_SW13_PaintedVesselAtlas.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow13/PaintedVesselAtlas.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/MasterMedicineCabinet01/Textures/CM_MMC01_ReusedCeramicPaint.png` — retained source/export/review or other-asset role

- **4.25 MB each**, SHA-256 `3404f725d624c817d3d531843f29f0ceb9591aa927cab843093280e24fb55642`.
  - `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetStyle02/Textures/CM_Cabinet_Original_Normal.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetRecovery01/Textures/rustic_wooden_cabinet_3d_model_normal.png` — retained source/export/review or other-asset role

- **3.39 MB each**, SHA-256 `42eed8fca54b165c24e40e514a48ba39f3f5b3598b7d33dcc1dabf8382757631`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/Illustrated04/Textures/CM_Illustrated04_Atlas.png` — Production02 static dependency
  - `ArtSource/Paint/Interiors/CrookedMortar/Illustrated04/CM_Illustrated04_Master.png` — retained source/export/review or other-asset role

- **3.21 MB each**, SHA-256 `fe101e6887e1efb865f56b2d65c6f684991f5f334235661445722355a0f24021`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow14/Textures/CM_SW14_DressedStone.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow14/PaintedStone.png` — retained source/export/review or other-asset role

- **3.18 MB each**, SHA-256 `0e967ef7866bc07f9fc7d3f376320c885180ee7f3ce1c21389bfcadf0800ac87`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/EntranceWorkflow11/Textures/CM_EW11_PaintedStone.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/EntranceWorkflow11/PaintedStone.png` — retained source/export/review or other-asset role

- **3.17 MB each**, SHA-256 `6aa5c0bcdffbe53607bd979920dbfc1aa4c429ca19ff85b9664ecc601b9f7539`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/Illustrated04/Textures/CM_Illustrated04_Sign.png` — Production02 static dependency
  - `ArtSource/Paint/Interiors/CrookedMortar/Illustrated04/CM_Illustrated04_SignMaster.png` — retained source/export/review or other-asset role

- **3.13 MB each**, SHA-256 `720eb033858b00940082354becb257eba63ba830f222650c7ce7b572fce739d5`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Textures/CM_SW13_HerbLabels.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow13/HerbLabels.png` — retained source/export/review or other-asset role

- **2.96 MB each**, SHA-256 `60aa607a682ad53f69bfa5ed5573031df49cece828e1ab21c2adb399638244a8`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow12/Textures/CM_SW12_PaintedLimewash.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow12/PaintedLimewash.png` — retained source/export/review or other-asset role

- **2.81 MB each**, SHA-256 `f3aa058874958c80881c6fcae26f8c3d6eece5d80c37ce7fd8348e9b9b8b84c8`.
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/SlateRoofKit01/Textures/CM_Slate_GouacheColour_v03.png` — retained source/export/review or other-asset role
  - `ArtSource/Paint/Architecture/CrookedMortar/SlateRoofKit01/CharacterPass/CM_Slate_GouacheColour_v03.png` — retained source/export/review or other-asset role

- **2.74 MB each**, SHA-256 `ff50de2c140f115c470c0266905e06b0db5c49e97a3aa680d0dad5cb56f83b31`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow10/Textures/CM_SW10_PlasterStone.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow10/PlasterStonePaint.png` — retained source/export/review or other-asset role

- **2.51 MB each**, SHA-256 `77c96e8480f88e612d9f36b6ff2767e0786de8a74857fdf82b11bc4ea52b5b49`.
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SourceTextureReadOnlyCopy_storybook_cottage_3d_model_rm.jpg` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/Textures/Original_01.jpg` — retained source/export/review or other-asset role

- **2.39 MB each**, SHA-256 `13ded7063e5cfb81a71004fa928acc4276336d274ddc9b7346c501789d1d15b8`.
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08/Previews/Candidate/CarvingClose.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow09/Previews/Existing/CarvingClose.png` — retained source/export/review or other-asset role

- **2.38 MB each**, SHA-256 `14aecd6c557ae43f4e78943a4f39c6a025d9b39492a49878037bda67b2f7fb75`.
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08/Previews/Existing/AngledBare.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow07/Previews/Candidate/AngledBare.png` — retained source/export/review or other-asset role

- **2.38 MB each**, SHA-256 `30872295a51c1aa9eb1b85de82e5aeccbd9873a67c8f0eddb90383261cf42a08`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow08/Textures/CM_CW08_Walnut.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08/WalnutPaint.png` — retained source/export/review or other-asset role

- **2.32 MB each**, SHA-256 `a60614f7c9ae9a70720ddda7a04475e9c21c69b9e0e7af64b37a9f1fc9b1db1c`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/ShopWorkflow13/Textures/CM_SW13_PaintedWalnut.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ShopWorkflow13/PaintedWalnut.png` — retained source/export/review or other-asset role

- **2.22 MB each**, SHA-256 `944036f5f8ee52029a9223d2c8f53f4a978c40365172a23f93c3bce349cb7f65`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow07/Textures/CM_CW07_CarvedWalnut.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow07/CounterPaint.png` — retained source/export/review or other-asset role

- **2.18 MB each**, SHA-256 `40daa0696776930756c1085229f067f82a8c575e41ce53c3aeb49aeb22c72746`.
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/SlateRoofKit01/Textures/CM_Slate_GouacheColour_v04.png` — Production02 static dependency
  - `ArtSource/Paint/Architecture/CrookedMortar/SlateRoofKit01/CharacterPass/CM_Slate_GouacheColour_v04.png` — retained source/export/review or other-asset role

- **2.12 MB each**, SHA-256 `94133041a246d17c149072a547b5e5eefe61fab0dbeb1608308c5895fdb05e1d`.
  - `Assets/BlightBloom/Art/Interiors/CrookedMortar/CounterWorkflow07/Textures/CM_CW07_Walnut.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow07/WalnutPaint.png` — retained source/export/review or other-asset role

- **1.91 MB each**, SHA-256 `ac41d5bbe6b8ecc38f652c0658a7baee6b0643bbc599629ad0b47a5fcfb2404a`.
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08/Previews/Existing/ClayBare.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow07/Previews/Candidate/ClayBare.png` — retained source/export/review or other-asset role

- **1.85 MB each**, SHA-256 `c29543ac32e893ba0a14a49a362689e3878abfbc7b87b024b0b1e31594d84a9b`.
  - `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetStyle02/Textures/Walnut_Painted_Source.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/TripoCabinetStyle03/Textures/Walnut_Painted_Source_Reused.png` — retained source/export/review or other-asset role

- **1.85 MB each**, SHA-256 `e3f2a87781dc969891ec3cc9dfda519eb91dda15002fb5135e8400b281046466`.
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow08/Previews/Candidate/ClayBare.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/CounterWorkflow09/Previews/Existing/ClayBare.png` — retained source/export/review or other-asset role

- **1.37 MB each**, SHA-256 `c628fd90df24fc344ac553b4c7cebc26c1a7ab1b4906c0e0833565d8a0519637`.
  - `ArtSource/Blender/Interiors/CrookedMortar/HeroRefinement02/Previews/Before/CounterShelf.png` — retained source/export/review or other-asset role
  - `ArtSource/Blender/Interiors/CrookedMortar/ApothecaryFurnishings01/Previews/Shop.png` — retained source/export/review or other-asset role

- **1.35 MB each**, SHA-256 `9682f154bb873c3bd2a72713e69938c05098ce0a845b9cc973aeb80e52cb3e80`.
  - `Assets/BlightBloom/Art/Architecture/CrookedMortar/BotanicalPlanterKit01/Textures/CM_BotanicalElements01.png` — Production02 static dependency
  - `ArtSource/Paint/Architecture/CrookedMortar/BotanicalPlanterKit01/CM_BotanicalElements01.png` — retained source/export/review or other-asset role

Repeated texture copies under Assets must not be deleted solely because pixels match: their GUIDs/material references differ. The identical exported house FBX in ArtSource and Assets is deliberate pipeline staging. SourceTextureReadOnlyCopy and `.fbm` transport copies offer only small savings and can break recorded/re-export paths; defer. Comparison-image duplicates are redundant evidence candidates after retaining at least one copy and updating any report links, not immediate deletes.

## External tool-specific caches

| Exact external path | Allocated size | Purpose | Handling / dependencies |
| --- | --- | --- | --- |
| `/Users/zak/Library/Caches/UnityHub` | 442.42 MB | Unity Hub update downloads | Low–medium; close Hub and complete/cancel updater first; redownloadable |
| `/Users/zak/Library/Caches/unityhub-updater` | 414.18 MB | Older Hub updater archives | Low–medium; close Hub and complete/cancel updater first; redownloadable |
| `/Users/zak/.npm/_cacache` | 522.41 MB | npm download/content cache | Low; stop npm installs/builds; network needed to repopulate |
| `/Users/zak/Library/Caches/Unity` | 138.22 MB | UPM download database | Low–medium; close Unity/Hub; do not remove packages.json/lock or required offline-only packages |
| `/Users/zak/Library/Unity/cache` | 141.21 MB | Unity Bee build cache | Low; close Unity/build processes; regenerated |
| `/Users/zak/Library/Caches/com.unity3d.UnityEditor` | 270.49 MB | Unity Editor Bee cache; GiCache presently empty | Low; close Unity/build processes; regenerated |
| `/Users/zak/Library/Caches/Codex` | 47.53 MB | Codex web renderer cache | Low; close Codex; cache only, not Application Support or conversation data |
| `/Users/zak/Library/Caches/Blender` | 483.3 KB | Asset-library indices | Low; close Blender; negligible saving |
| `/Users/zak/Library/Logs/Unity` | 79.43 MB | Editor/package/licensing logs | Low–medium; retain recent diagnostic logs; close Unity/Hub/licensing writers before any approved removal |
| `/Users/zak/Library/Caches/com.openai.codex/org.sparkle-project.Sparkle/Installation` | 2.009 GB | Staged application and update delta | CONDITIONAL; close Codex and updater; verify installed app and update state first; not certified disposable in this audit |
| `/Users/zak/.cache/codex-runtimes` | 1.702 GB | Active bundled Python/Node runtime dependencies | RETAIN; used by Blender texture/export tooling; not just dispensable downloads |
| `/Users/zak/.codex/plugins/cache` | 67.18 MB | Installed plugin/skill bundles | RETAIN; active installed tools, not a blanket cache purge target |
| `/Users/zak/Library/Caches/com.unity3d.unityhub` | 81.9 KB | Hub web cache | Low; close Hub; negligible |
| `/Users/zak/Library/Caches/com.unity3d.unityhub.ShipIt` | 53.2 KB | Hub updater state | Retain until updater state verified; negligible |

Unity Hub contains `update.zip` and `pending/UnityHubSetup-3.22.3-arm64.zip`, each 221,208,418 bytes. The other updater cache contains `update.zip` and `pending/UnityHubSetup-3.21.0-arm64.zip`, each 206,863,089 bytes. Identical length is **not** a hash confirmation of these external archives. The Sparkle Installation tree contains a staged application bundle and a 191,375,418-byte update delta, so it must not be blindly purged while Codex/update helpers are running. Only cache directory names and tool files were inspected; no Codex conversations, personal documents, Downloads library or broad home-folder content scan.

No named Tripo cache was found in the inspected immediate Library/Caches or Application Support locations; Tripo browser-managed storage was not searched. Unity Asset Store cache and pip cache were absent at the tested standard locations. Blender Application Support is only 4 KB and contains preferences/state, not a worthwhile purge. Temporary tool directories `/private/tmp/codex-browser-use` and `/private/tmp/codex-app-tools` report zero allocated data; Unity sockets/locks must remain untouched. Process-list access was denied by the environment, so application/updater idleness is **not verified**. No cache is authorized for removal.

## Ranked proposal — approval required

| Rank/group | Exact path | Maximum allocated saving | Risk | Dependencies / apps to close | Recommendation |
| --- | --- | --- | --- | --- | --- |
| A1 | `/Users/zak/Library/Caches/UnityHub` | 442.42 MB | Low–medium | Close Hub/updater; complete or cancel pending update; archives can be downloaded again | First practical download-cache candidate |
| A2 | `/Users/zak/Library/Caches/unityhub-updater` | 414.18 MB | Low–medium | Same Hub updater check; distinct sibling cache, no nested double count | Older updater-cache candidate |
| A3 | `/Users/zak/.npm/_cacache` | 522.41 MB | Low | Stop npm operations; preserve runtime/node_modules; network needed later | Regenerable download cache |
| A4 | `/Users/zak/Library/Caches/com.unity3d.UnityEditor` | 270.49 MB | Low | Close Unity/build processes | Regenerable Bee cache |
| A5 | `/Users/zak/Library/Unity/cache` | 141.21 MB | Low | Close Unity/build processes | Regenerable Bee cache, separate path |
| A6 | `/Users/zak/Library/Caches/Unity` | 138.22 MB | Low–medium | Close Unity/Hub; verify registry access/offline package availability | UPM cache; preserve manifests and lock |
| A7 | `/Users/zak/Library/Logs/Unity` | 79.43 MB | Low–medium | Close log writers; keep current Editor/licensing diagnostics | Archive/delete old rotated logs only; listed total is upper bound |
| A8 | `/Users/zak/Library/Caches/Codex` | 47.53 MB | Low | Close Codex; only browser renderer cache | Small regenerable cache |
| A9 | `/Users/zak/Desktop/MorrowMoss Studios/BlightBloom/Library` | 3.824 GB | Medium operational cost | Save and close Unity; preserve Assets/Packages/ProjectSettings; allow registry access and ample reimport workspace | Last-resort cache rebuild; saving returns on next full import |
| A10 | `/Users/zak/Desktop/MorrowMoss Studios/BlightBloom/Temp` | 8.25 MB | Low once closed | Close Unity; never remove active sockets/locks | Small temporary data |
| A11 | `/Users/zak/Desktop/MorrowMoss Studios/BlightBloom/Logs` | 4.50 MB | Low–medium | Close writers; retain relevant recent logs | Small diagnostic upper bound |
| A12 | `/Users/zak/Library/Caches/com.openai.codex/org.sparkle-project.Sparkle/Installation` | 2.009 GB | Medium; unresolved updater state | Quit Codex/update helpers, verify installed app launches and update is complete/cancelled; stage is not active executable | Conditional additional saving; exclude from safe total |

A candidates are mutually non-overlapping. Whole Library includes all its child caches, which must **not** be added again. Near-zero Blender/cache-state folders are excluded from practical ranks; the small Blender index is included only in the conservative cache ceiling. No installed runtime/plugin bundle is counted.

### B — superseded intermediates: archive-first inventory

These exact files are documented as rejected/intermediate by their existing reports, rather than guessed from names. Close Blender before any later approved move; verify no linked library uses them and verify an external checksum backup. They are absent from normal HEAD. Archive preserves historical repair reruns; restore the same relative tree to run those scripts. No entire-directory deletion is proposed.

| Exact project-relative file | Size | Dependencies / risk / recommended handling |
| --- | --- | --- |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/RejectedTests/Rejected_UnscaledReduction.blend` | 160.59 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend` | 172.03 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend1` | 171.67 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend` | 171.81 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend1` | 171.76 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend` | 171.78 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend1` | 171.73 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage01.blend` | 172.32 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage02.blend` | 172.06 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage03.blend` | 172.02 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage04.blend` | 171.90 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage05.blend` | 171.62 MB | Medium; historical stage/closure/repair inputs; external archive first, then separate approval to remove local copy |

B subtotal: **2.051 GB logical / 2.051 GB allocated**. Excludes final source, final previous-save backup, both boundary references and their backups, uncut safety source, current optimized/repaired-high sources, textures, arrays, reports and renders. Rejected render groups are not included in the subtotal; they save much less and retain useful diagnostic history.

### C — essential / protected

- All existing Assets scenes/prefabs/materials/textures, approved modular libraries, current plague-doctor rig/locomotion, gameplay scripts, project/package settings and documentation.
- Original Tripo GLBs and original artwork/maps.
- Exterior `OriginalReference.blend`, `CrookedMortar_RepairedHigh.blend`, `CrookedMortar_Optimized.blend`, `ExteriorCollisionSource.blend`, and their recovery backups.
- BoundaryMapping01/02 `.blend` references and their report/guide data; TerrainSeparation01 final `.blend`, prior save, uncut safety source, closure textures and authoritative validation data.
- Full `.git/` history and refs; no history rewrite, LFS removal or object pruning.
- Active Codex runtimes and installed plugin bundles.

### D — external storage options, not deletion

| Exact scope | Local saving ceiling after verified transfer | Risk / dependencies | Recommended handling |
| --- | --- | --- | --- |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/` selected B files only | 1.891 GB | Medium; old scripts require relative inputs; close Blender | First archive option; included in B, never count twice |
| `ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorRecovery01/RejectedTests/Rejected_UnscaledReduction.blend` | 160.59 MB | Medium; rejected diagnostic lineage; close Blender | Archive with original relative path; included in B |
| `ArtSource/` (entire tree, optional future relocation) | 6.884 GB | Medium–high; scripts derive repository-relative paths; source recovery workflows need stable access | Not proposed for immediate blanket move; require external drive/backups plus separately approved path strategy; overlaps B and all protected sources |
| `/Users/zak/Desktop/MorrowMoss Studios/BlightBloom` (whole project on external SSD) | 18.003 GB | Medium–high; preserve .git and all relative paths, source permissions and backups; close Unity/Blender/Codex project writers | Only realistic larger relocation option without deleting protected work; verify external SSD capacity/performance and full transfer before removing local copy; overlaps every project category |

Do not move `.git` alone or move only referenced textures out of Assets. No external drive capacity or backup integrity was assumed. Git alone is not adequate verified recovery for the current untracked editable sources. A full verified external project relocation can exceed 10 GB of local relief; it is a separate relocation decision, not evidence of 10 GB of unnecessary files.

## Audit limits and next decision

Project filesystem enumeration, tool-cache sizing, targeted source/report reads, static Unity GUID references and SHA-256 duplicate checks completed. No source asset regeneration, Blender load, Unity refresh, Console validation, gameplay test, missing-reference validation, cleanup or performance test was appropriate for this storage-only request. Enumeration errors: 0. Hard links/APFS clones/compression/purgeable snapshots can make actual reclaimed physical capacity differ from file block sums; apps may grow logs while measured. Use these figures as estimates and remeasure before approved cleanup.

**Recommended approval scope:** begin with closed-app regenerable download/build caches, retaining current logs and all project sources. Leave Library and Codex staged installer out of the first pass unless their rebuild/update conditions are explicitly accepted. Then archive only the exact B inventory to a verified external destination if more headroom is needed. Do not target 10 GB by deleting protected source or Git history. Stop here for user approval.
