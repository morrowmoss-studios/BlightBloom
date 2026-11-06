# BlightBloom — ArtSource & Pipeline storage audit

2026-11-05. **Read-only investigation; cleanup is NOT authorized.** Only this report and the small focused duplicate index are added. No Unity/Blender execution, source regeneration, asset/settings edits, deletions, moves, archives, cache clearing or Git operations. No status/diff/history/tracked-file queries; Git tracking is **unknown** unless explicitly described as historical evidence.

## 1. Measured storage

Regular files total **24.881 GiB logical / 25.021 GiB allocated**, 52,455 files. ArtSource: **8.505 GiB**, 2,898 files. Pipeline/Review: **472.660 MiB**, 983 files. Measurement precedes this small audit package.

|Directory|Logical|Allocated file blocks|Files|Purpose|
|---|---:|---:|---:|---|
|`ArtSource/`|8.499 GiB|8.505 GiB|2,898|Editable sources + pipeline/review work|
|`Assets/`|2.632 GiB|2.642 GiB|4,305|Imported/runtime assets; protect paths and .meta|
|`Library/`|5.230 GiB|5.340 GiB|40,195|Unity-generated cache; excluded from cleanup plan|
|`.git/`|8.474 GiB|8.485 GiB|4,183|Protected repository metadata/history; filesystem size only|
|`Temp/`|37.405 MiB|39.168 MiB|818|Unity temporary state; active-use status unverified|
|`Logs/`|10.071 MiB|10.316 MiB|15|Diagnostics; active-use status unverified|
|`ProjectSettings/`|0.056 MiB|0.129 MiB|25|Protected settings|
|`Packages/`|0.015 MiB|0.020 MiB|2|Protected package manifests|
|`UserSettings/`|0.092 MiB|0.109 MiB|6|User preferences; retain|

“Allocated” sums measured filesystem file blocks, deduplicating hard-linked inodes; symlinks are not followed. It excludes directory metadata and does not measure unique APFS clone/snapshot extents. Actual freed capacity can be smaller. Existing Editor/application writers may continue independently, so cache/log totals are a point-in-time observation.

The source/asset/settings working-file set, excluding `.git`, `Library`, `Temp` and `Logs`, is approximately11.15GiB. This is a filesystem distinction, **not a tracked/untracked determination**. Repository metadata is not disposable working-tree data. Library is regenerable but not a proposed cleanup target: no closure/reimport readiness verified. Process inspection was restricted by the sandbox; no application shutdown state was certified.

No root Build/Builds regular-file output was found. The known standalone diagnostic build at `/private/tmp/BlightBloomEnvironment06Baseline/` occupies **1.129GiB** (du measurement), outside the project and excluded from all project/review totals and recovery sums. It is an older baseline build, not editable source. Retain its build report; consider its binary only after separately approving removal and verifying no process uses it and no unique baseline is needed. Rebuilding previously cost about33minutes; exact historical source/build reproducibility was not re-established here.

### ArtSource branches (nested rows are not additive)

|Directory|Allocated|Files|
|---|---:|---:|
|`ArtSource/Blender/`|8.010 GiB|1,836|
|`ArtSource/Blender/Exteriors/`|4.057 GiB|381|
|`ArtSource/Blender/Architecture/`|2.006 GiB|480|
|`ArtSource/Blender/Interiors/`|1.906 GiB|830|
|`ArtSource/Blender/Characters/`|43.125 MiB|144|
|`ArtSource/Paint/`|31.812 MiB|64|
|`ArtSource/Pipeline/`|474.582 MiB|996|
|`ArtSource/Pipeline/Review/`|472.660 MiB|983|

Blender `.blend` files occupy5,087.379MiB across86files;16`.blend1` prior saves occupy1,749.512MiB. These are editable/recovery resources, **not caches**, even when superseded. Packed texture copies contribute to large cottage/stable sources: inspected builders explicitly load and `image.pack()` base-color maps. Removing objects/materials or unpacking sources would require a separately approved art/source-maintenance task, not this audit.

### Largest ArtSource files

|Exact relative path|Allocated|Disposition|
|---|---:|---|
|`ArtSource/Blender/Architecture/Briarwick/FamilyCottageB01/BW_FamilyCottageB01.blend`|183.54 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Architecture/Briarwick/StableA01/BW_StableA01.blend`|182.73 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/BW_StableA02OpenFront.blend`|182.62 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage01.blend`|164.34 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend`|164.21 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparated01.blend1`|164.21 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage02.blend`|164.09 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/CM_CrookedMortar_TerrainSeparation01_WORKING.blend`|164.06 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage03.blend`|164.06 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/Stage04.blend`|163.94 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_CLOSURES.blend`|163.86 MiB|Protected editable/recovery source; not disposable|
|`ArtSource/Blender/Exteriors/CrookedMortar/TripoExteriorStandalone01/TerrainSeparation01/SafeSeparated_UNCAPPED.blend`|163.83 MiB|Protected editable/recovery source; not disposable|

The earlier2026-10-31 audit identified external-archive possibilities among Stage01–05, working/closure checkpoints and rejected exterior tests. Those files still carry historical reconstruction dependencies; this report does **not** convert that old proposal into deletion approval or count their size as immediately recoverable. All current exterior candidate, source imports, boundary decisions and important recovery history remain protected.

## 2. Individual Review folders

All paths below are relative to `ArtSource/Pipeline/Review/`. Recursive folder totals include nested diagnostics; top-level snippets are grouped separately. Do not add these to the Review parent again.

|Folder|Allocated|Files|
|---|---:|---:|
|`BriarwickEnvironment06_Revision01`|77.250 MiB|89|
|`BriarwickEnvironment06`|63.574 MiB|86|
|`BriarwickEnvironment07`|53.547 MiB|75|
|`BriarwickEnvironment05Revision01`|50.957 MiB|79|
|`BriarwickWoodland03`|24.398 MiB|31|
|`BriarwickEnvironment05`|19.129 MiB|37|
|`BriarwickEnvironment02`|17.414 MiB|30|
|`FamilyCottageAStyle01`|15.887 MiB|36|
|`BriarwickWoodland04`|15.086 MiB|28|
|`BriarwickPlayable01`|12.367 MiB|25|
|`BriarwickBakery02`|11.695 MiB|40|
|`FamilyCottageAOriginalAppearance01`|10.738 MiB|28|
|`BriarwickStableA03Rural`|10.262 MiB|25|
|`BriarwickStableA01`|9.598 MiB|25|
|`BriarwickWoodland01`|8.027 MiB|27|
|`BriarwickMerchant01`|7.754 MiB|24|
|`BriarwickInn01`|7.520 MiB|26|
|`BriarwickStableA02OpenFront`|7.195 MiB|22|
|`BriarwickChapel01`|6.914 MiB|22|
|`BriarwickMillerCottage01`|6.617 MiB|21|
|`BriarwickFarmhouse01`|6.598 MiB|24|
|`BriarwickBlacksmith01`|5.934 MiB|24|
|`BriarwickBakery01`|5.520 MiB|22|
|`BriarwickFamilyCottageB01`|5.305 MiB|21|
|`BriarwickElderCottage01`|5.254 MiB|21|
|`BriarwickFirstHouseTest01`|4.258 MiB|17|
|`BriarwickHamletDev01`|3.520 MiB|21|
|`(top-level shared/historical snippets)`|0.344 MiB|57|

|Review file type|Files|Allocated|
|---|---:|---:|
|`.png`|299|369.457 MiB|
|`.json`|322|53.098 MiB|
|`.bin`|34|36.320 MiB|
|`.before`|4|9.004 MiB|
|`.jpg`|12|2.793 MiB|
|`.cs`|246|1.348 MiB|
|`.md`|43|0.355 MiB|
|`.txt`|22|0.281 MiB|
|`.shader`|1|0.004 MiB|

Images dominate: PNGs alone are about78%of Review storage. C# snippets are only1.348MiB; Markdown only0.355MiB. Deleting useful tools/reports would save little. Current Environment07 contains75review files/53.547MiB, not121review files: the prior121-created-file inventory also included46new Unity asset/metadata files. Do not confuse its production assets with disposable evidence.

## 3. Purpose and dependency classification

|Class|Keep/handling|Specific findings|
|---|---|---|
|A — essential production source/assets|Protect|Editable `.blend`, original Tripo GLBs, painted/editable artwork, textures, source meshes, reusable kits, exported Unity models/prefabs/materials/shaders, `.meta`, gameplay and settings. Copies under both ArtSource and Assets serve different source/import roles.|
|B — active development resources|Retain in place|Current generation/integration scripts; `BriarwickHamletDev01/Layout.json`; Environment05/06/07 integration/configuration records; current issue trackers; capture camera definitions; current validation baselines and rollback sources.|
|C — review/validation evidence|Curate only after approval|Before/after images, raw performance/test JSON, component snapshots, serialized detail/height maps, `.before`scene/TerrainData files. Some are executable test inputs, not just output. Preserve significant failure traces and decisions.|
|D — demonstrably regenerable/redundant diagnostics|Narrow candidates below|Seven Finder metadata files, two source-grass inspection renders, one redundant rejected-profile summary. No extension-wide deletion rule.|

**Critical non-obvious dependencies:**

- `ArtSource/Blender/Architecture/Briarwick/FamilyCottageA/Style01/SourceMeshReadOnly.json` and `SourceMaterials.json` are read by later building generators. The rejected Style01 palette does not make these records obsolete.
- `ArtSource/Blender/Architecture/Briarwick/StableA02OpenFront/build_open_stable.py` and `.../Bakery02/reconstruct_bakery.py` supply helper definitions to current builds (including FamilyCottageB01), via explicit source-text extraction/exec. Do not archive/delete their whole folders as “old versions.” This helper sharing is fragile; extracting shared functions later should be a focused refactor, with validation.
- `ArtSource/Pipeline/Review/BriarwickHamletDev01/Layout.json` is used by current road/approach/environment tools. Woodland03/Integration.json supplies the existing grove alignment to Environment07/RefineGroveTrail.cs.
- Environment07/Validate.cs reads its SceneBefore.json, HeightsBefore.bin, six DetailBefore maps, Integration.json and LayersBefore.json. ProfilePaired.cs/ProfileBridge.cs read AlphamapsBefore.bin and Integration.json. Their snapshot paths cannot simply be removed because the current scene already looks correct.
- Environment06_Revision01/Validate.cs and ProfilePaired.cs similarly consume their snapshots. Current `.before` copies provide distinct rollback value while the candidates await visual approval. Preserve the two recent rollback bundles until approval/recovery policy is resolved.
- `BriarwickEnvironment07/Source/BriarwickRoadFeather.shader` is editable shader source with a Unity import counterpart, **not a temporary validation snippet**. Likewise preserve the new painted turf source under ArtSource/Paint and its Unity texture import.
- Hash-identical test JSON can represent separate deterministic executions. It does not prove copied/fabricated tests, nor make pass provenance dispensable. Keep the pass summary and source identity when consolidating.

Static text inspection covered5,075project text files under Assets, ArtSource, Packages and ProjectSettings; no Assets text directly mentioned `ArtSource/Pipeline/Review`. Review files have no imported Unity metadata/runtime asset identity. That supports separation from runtime dependencies, **not universal proof of non-use**: dynamically assembled paths and binary/packed Blender links were not fully resolved. No Blender or live Unity dependency loading was performed. Uncertain source/texture/export dependencies are protected; no runtime asset removal is recommended.

**Tracking/backup status:** current status is unknown. Older audit inventories describe prior states only. The current `.gitignore` contains `*.blend`, `*.blend1` and `.DS_Store`; pattern matching shows ignore intent, not whether an existing file is tracked or safely backed up. No current GitHub/LFS/source-recovery assurance is made. No Git index, history, objects or configuration contents were queried; `.git` was measured via filesystem metadata only.

## 4. Hash-verified duplication

SHA-256 was evaluated only where file sizes matched (unequal-size files cannot be byte-identical):484ArtSource candidates/211,086,990logical bytes read. Found76content groups with110extra ArtSource copies, **99.938MiB allocated** as a theoretical single-copy consolidation ceiling. None of the `.blend`/`.blend1` files was established as an exact duplicate; similar allocated sizes are not duplicate proof.

Within Review specifically: **49groups,65extra copies,54.145MiB allocated**:

|Type|Groups|Extra copies|Allocated ceiling|Why not immediate deletion|
|---|---:|---:|---:|---|
|PNG|26|27|39.988MiB|Before/after galleries and historic review reports use different paths. Preserve evidence and update links only with approval.|
|BIN|6|13|13.062MiB|Validators/profilers read local snapshot paths; changing inputs would break reruns.|
|JSON|17|25|1.094MiB|Pass provenance/baselines may differ in role despite identical bytes.|

Exact group membership, sizes and full hashes: [ReviewDuplicateIndex.tsv](ReviewDuplicateIndex.tsv). This index is **not a removal manifest** and selects no mandatory keeper. Entries are content-equivalent, not necessarily semantically interchangeable.

Examples:

- Nine identical513²height snapshots (SHA-256 starts`6b796667f0446be3`), including Playable01, Environment02/05/05Revision01/06/06_Revision01/07 and Woodland03/04; eight extra copies alone occupy about8.06MiB. Their validators still read their respective filenames.
- Environment06 “After” screenshots and Revision01 “Before” screenshots repeat the same state; e.g. the WoodlandEdge pair (SHA starts`82fac6387b615cfc`) is2.54MiB per copy. Gallery links must be retained/retargeted, not broken.
- Four original detail-map files are identical between Environment06 and Environment06_Revision01. Current Environment07 maps are a different state and are not interchangeable with those older maps.
- `UnrelatedBefore.json`/`UnrelatedAfter.json` across the two cottage material reviews are identical, but record separate preservation assertions.

A cross-check also found37content groups shared between ArtSource and Assets. **Do not count them as cleanup savings.** For example, the16,388,732-byte standalone FBX exists as an export and as the Unity model import; original house color/normal maps and painted masters similarly have source/import copies. Export `.fbm` texture copies may be Blender/FBX relink inputs. They are protected until native external-reference handling is explicitly audited and redesigned.

## 5. Prioritized cleanup proposal — approval required

### Low risk:10files,0.543MiB allocated maximum

|Group|Count|Allocated|Class / dependency / reproducibility|Risk and recommended action|
|---|---:|---:|---|---|
|L1 — listed `.DS_Store` only|7|0.078MiB|D: Finder folder-view metadata, not source/runtime input; regenerated by Finder|Low. Approve exact files only; retain directories and `.meta`.|
|L2 — listed SourceGrass inspection PNGs|2|0.457MiB|D: readback inspection of retained `Assets/ALP_Assets/GrassFlowersFREE/Textures/GrassFlowers/grass01.tga` and `grass02.tga`. No code read or gallery/README link found; only ChangedFiles inventory mentions. Reproducible using existing texture readback.|Low; recheck no new reference before approved removal. Do not remove original TGA, painted turf source or LocalTest image.|
|L3 — rejected-profile derived summary only|1|0.008MiB|D: derived medians of the retained rejected raw capture; no reader found, only ChangedFiles inventory. Raw invalid-capture evidence and rejection rationale remain.|Low. Remove only this redundant summary if approved; retain raw capture and valid paired results.|

Exact scope and hashes (allocated bytes, not a wildcard authorization):

|Group|Relative path|Allocated bytes|SHA-256|
|---|---|---:|---|
|L1|`ArtSource/.DS_Store`|12,288|`f3296d849e1e6ed687f754e020f6a5e5932dc6e627f5ee1b220788ab05fb2b6d`|
|L1|`ArtSource/Blender/.DS_Store`|12,288|`76e7141e72f4bb735f944bd6c438f2a32e05bccd7873a1458950600a8310e7b5`|
|L1|`ArtSource/Blender/Exteriors/.DS_Store`|8,192|`23fe75140110e8c2e1c982f428555c99fd279759236918925d672385b09bbfb4`|
|L1|`ArtSource/Blender/Exteriors/CrookedMortar/.DS_Store`|8,192|`2bb4fbb1e20e26ac5288e28f8a860e6786c8b1942668db808679fd05c2065437`|
|L1|`ArtSource/Blender/Architecture/.DS_Store`|12,288|`bbcb162e1a2b84b378ff7c9b50d7a4a4e193337b967ac8210c440f99e0396ac6`|
|L1|`ArtSource/Blender/Architecture/CrookedMortar/.DS_Store`|16,384|`eb970cae40280f3d779a2483239a236d0464055c0f9398e4edb1e2e9041bd1c5`|
|L1|`ArtSource/Blender/Architecture/Briarwick/.DS_Store`|12,288|`510726e957714a849e28b77adca4b1f0f552f0fd2185333f2202a02e10de75f3`|
|L2|`ArtSource/Pipeline/Review/BriarwickEnvironment06_Revision01/SourceGrass1.png`|241,664|`e7994ac4c5cb6b073bad83cb1ade3072ffa6e509fb5b39a293ea0340223f8226`|
|L2|`ArtSource/Pipeline/Review/BriarwickEnvironment06_Revision01/SourceGrass2.png`|237,568|`44e8ed39e2b2d3d467ebbf85214ca8e4c5ae0f0cac113afa0afbb8d610add86f`|
|L3|`ArtSource/Pipeline/Review/BriarwickEnvironment07/PerformanceSummary_Rejected_NoGameViewRendering.json`|8,192|`0f289d4c31364bda43f59cf2d7c68859425fc6a247c2aeb079c82c9d63adcfb9`|

Before any approved removal, recheck path identity, hash, new dependencies and current use; skip changed/uncertain candidates. These small candidates are not a meaningful solution to multi-GiB storage pressure.

### Requires review / consolidation / external archive

|Group and exact selection scope|Count / allocated|Dependency findings and reproducibility|Risk / recommendation|
|---|---|---|---|
|C1 — hash groups in ReviewDuplicateIndex.tsv|65extra-copy ceiling /54.145MiB|Content duplicates, but gallery/validator inputs and test provenance remain. Need canonical paths plus approved reader/link updates. Exact old before-states cannot be regenerated merely by rerendering the current scene.|Medium. Consolidate references first, retain one correct state and per-pass provenance. No direct file deletion approved.|
|R1 — Review image pool under all existing pass folders **except** BriarwickEnvironment06_Revision01 and BriarwickEnvironment07; `.png`/`.jpg` only|250files /276.102MiB|Historical approval/comparison images; many linked. Some old states are not reproducible without corresponding source checkpoints. Current two review packages excluded.|Medium. Human-select core visual evidence first, then archive unique surplus with reports and relative links. Pool is a ceiling, not an instruction to remove250images. Contains duplicate-image space already in C1.|
|R2 — `.bin`, `.before` and SceneBefore/protected-state JSON in Review|BIN34files/36.320MiB; BEFORE4files/9.004MiB; JSON subset not given a deletion total|Inputs to current/historical tests, rollback and technical proof. Some binary copies are hash-identical (included in C1), others encode unique states.|Medium/high. Keep recent rollback sets. After artistic approval, choose a checkpoint retention policy and centralize only verified equivalent inputs. No blanket `.bin`/JSON deletion.|
|R3 — copied validation/capture implementations|9normalized-equal groups,14extra C# copies; all Review C# is only1.348MiB|Same source after replacing only per-pass output directory literals. Current variants and generated-asset builders have real inputs/side effects.|Medium, low storage benefit. Parameterize shared tools after separate approval; do not simply delete old scripts or rewrite them during this audit.|
|R4 — Blender intermediates, backups, packed source/export copies|Protected source/history; no new deletion/recovery subtotal|Native references and recovery value unresolved. Existing earlier archive proposals are historical, not fresh authorization.|High. Retain sources; any later archive requires verified independent backup and preserved helper/input paths.|

**Do not add C1 and R1/R2 together.** They overlap. The276.102MiB image pool is not all safely disposable; the54.145MiB duplicate ceiling includes referenced input paths and provenance. No larger immediate recovery is certified. Git-history savings from removing working files are not counted. The standalone build/Library numbers are separate, unapproved categories and not included in these sums.

## 6. Why Review grew, and a leaner policy

Recent passes emit fixed capture catalogs: Environment06 has30PNGs, Revision01 has37, Environment07 has24. Paired regional/close-up requests explain much of this, but the helpers also default to the whole catalog for a local correction. Later-pass “before” captures frequently duplicate prior-pass “after” files byte-for-byte. Binary height/detail snapshots are copied again even when terrain heights/details are unchanged. SceneBefore/protected-reference JSON, before-copies, raw profiler samples, summaries and final status checks accumulate in parallel. Separate before/after C# files often differ only by a phase/output string.

Confirmed duplication after normalizing only literal review-directory strings: Snapshot.cs across five passes; ProbeCollision.cs across several environment passes; ProbeTrunksCamera.cs across three; LiveInput.cs in two pairs; two cottage ValidateEdit implementations. Centralization is principally a correctness/maintenance benefit, not large storage savings. **Some “Validate” tools mutate runtime state or write output, and builders can overwrite assets; do not execute them to perform this audit.** None was executed.

Recommended default for ordinary tasks:

1. **One concise README + one ChangedFiles inventory +3–5meaningful images.** A matched before/after pair counts as two; add more only where distinct defects/routes or the explicit brief require evidence. Do not reduce necessary collision/input validation to meet an image cap.
2. Reuse the prior final image by relative link when it is the exact intended baseline. Retain camera/lighting identity and source-state hash; regenerate only changed views. Do not claim old evidence proves the current scene.
3. Keep one compact validation/performance summary with method, source hash, sample counts, relevant distributions and failures. Raw successful frame-by-frame dumps remain in temporary work storage; retain raw failure traces when they explain a technical decision.
4. Use a small shared capture/route-probe module with task-specific config/output directory. Keep asset generators and material/source code beside their asset family. No large new framework is needed.
5. Save one coherent recoverable pre-change bundle for the affected data, keyed by state hash. Avoid copying unchanged heights/whole-scene state into every pass. Preserve rollback until approval; do not replace the only backup with a hash or a temporary file.
6. Separate “latest candidate,” “approved evidence” and “scratch/rejected outputs” by explicit status in reports. Newest timestamp is not approval. Retain a short failure rationale plus indispensable raw trace, not every intermediate derived report.

## 7. Sustainable organization and ignore proposals

Preserve existing Unity Assets paths and source-family locations. Do not reorganize the whole ArtSource tree. Recommended roles:

- `ArtSource/Blender/<family>/`: authoritative editable models, meaningful recovery checkpoints, necessary external images and model/export scripts.
- `ArtSource/Paint/<family>/`: original/editable painted masters and approved references.
- `Assets/BlightBloom/...`: production imports/materials/prefabs/shaders; Unity references and metadata stable.
- `ArtSource/Pipeline/`: shared small utilities, audit/decision documentation.
- Existing `ArtSource/Pipeline/Review/<pass>/`: lean approved/review package; historical unique evidence retained or separately archived after approval.
- Future scratch example **outside the repository**: `/Users/zak/BlightBloomWork/ReviewScratch/<task-id>/` for reproducible images, raw metrics and experiments. Do not create/move anything there during this audit. Critical rollback requires durable storage/backup, not `/tmp` as the sole copy.
- Standalone builds stay outside Assets/ArtSource in a deliberate regenerable build-output location; no committed build bundles.

Possible future `.gitignore` additions, **proposal only**:

```gitignore
# Deliberately designated transient workspaces only
/ArtSource/Pipeline/Review/_scratch/
/ArtSource/Pipeline/Review/**/RawCaptures/
/ArtSource/Pipeline/Review/**/Transient/
# Blender automatic saves beyond the existing *.blend1 rule
*.blend[0-9]*
```

Do not blanket-ignore all Review PNG/JSON/BIN/CS: some are approved evidence, active inputs or editable shader/code sources. Do not further hide approved `.blend` assets; separately resolve selective source protection with explicit approval. Ignore rules do not untrack already tracked files, provide a backup, or reclaim Git history. No ignore/config/tracking change was made here.

## 8. Recommended approval sequence and audit limits

1. If desired, approve **L1/L2/L3 exact files** first; only0.543MiB measured block recovery at most.
2. Approve a small shared-helper/output-policy refactor, preserving inputs and proving existing test behavior; no deletion needed initially.
3. Review C1 keeper semantics and affected links/readers. Authorize exact consolidation changes and final removed-path list separately.
4. Select historical images for an archive bundle while retaining approved references and present unapproved candidate evidence. Verify backup/restoration before any later local removal.
5. Treat source archives, standalone-build disposal and cache decisions as separate approvals. Do not touch `.git`, Unity Library, Blender sources, installed packages or active application state under this plan.

Limits: static file/text/hash inspection, not live Unity dependency resolution or binary Blender image/library enumeration. No artistic approval, missing-reference health check or gameplay validation was attempted. Visually similar images are not called duplicates without matching bytes. Current tracking/backup status remains unknown. APFS sharing, snapshots and active writers prevent a promised filesystem-free-space gain from block sums alone. **Stop here for explicit cleanup approval.**

Audit completion check: all2,898pre-existing ArtSource files retain their original sizes/mtime and none is missing. AGENTS.md, .gitignore, both current scenes and all five protected settings match the hashes taken during this audit. The only audit package files are README.md and ReviewDuplicateIndex.tsv (about50KiB total); no screenshots, large manifests or project validation outputs were generated. This metadata/hash check is not a Git query or a live Unity health test.
