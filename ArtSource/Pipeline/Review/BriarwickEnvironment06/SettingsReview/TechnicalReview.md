# Environment06 settings technical review — retained, not blanket-approved

2026-11-05. Read-only technical investigation plus documentation. **All five settings/profile files retained unchanged, as instructed. Earlier uncommitted work is not reverted. Environment06 is NOT visually approved.** User reports excessive vegetation clutter, artificial-looking ground and rendering performance requiring improvement. No vegetation addition, reduction, redistribution or expansion in this review.

## Evidence and limits

Installed Unity6000.4.5f1; URP/SRP Core17.4.0 (packages declare Unity6000.4 compatibility). Reviewed the current YAML, installed package source and existing Editor build log. No Unity commands, builds, profile initialization, services UI, reimports or Play-mode tests were executed during this documentation pass; invoking those paths could itself serialize settings. No Git commands/history access. User's GitHub Desktop comparison is the source for the old-versus-new changes below; repository-baseline file contents were not independently obtained.

Distinguish (a) code that legitimately derives data during a build, (b) whether current values match the intended rendering setup, and (c) authorization to retain a particular diff. Explaining a mechanism does not approve every changed field or prove every removed reference was correct.

## 1. DefaultVolumeProfile.asset

**User-observed difference:** added serialized post-processing properties and removed serialized references; origin/necessity previously unverified.

**Verified mechanism:** installed `URPPreprocessBuild.OnPreprocessBuild` calls `EnsureVolumeProfile`, which invokes `VolumeProfileUtils.TryEnsureAllOverridesForDefaultProfile`. That routine removes null/obsolete component references, enables/normalizes defaults and adds missing compatible VolumeComponent types. It can copy default values and mark the profile dirty. The historical Editor log explicitly records the default-profile-modified message and a stack through this exact build callback. This establishes a relevant automatic update during the baseline build, rather than merely a timestamp inference.

**Necessity:** a complete, valid default profile is part of URP's build preparation; missing runtime overrides can cause rendering problems. It does NOT follow that all added values or removed references are artistically intended or that every serialized subasset is needed. Full old/new parameter review remains necessary before accepting visual changes; no assumption that added fields are all neutral.

**Additional finding:** current YAML contains19 component-list references, all resolving to local subasset IDs. It also contains five **unreferenced Editor-test subassets**, with test-assembly class identifiers and zero script references:

- CopyPasteTestComponent1,2,3
- VolumeComponentSupportedEverywhere
- VolumeComponentSupportedOnAnySRP

None is in the current component list, so this is NOT evidence of five active post-processing effects. They are not required for production URP rendering and should not be accepted as necessary configuration. Reflection-based enumeration of compatible volume types plus later null-reference removal is a plausible route for test-type debris, but creation timing and whether it predates this task are unproven. See VolumeProfileReadOnlyInspection.json. Leave all untouched until a separately approved, component-level cleanup/value review; do not delete/recreate the profile or reset its artistic settings.

**Local sources:**

- `Library/PackageCache/com.unity.render-pipelines.universal@4d008a28541a/Editor/BuildProcessors/URPPreprocessBuild.cs:17` (EnsureVolumeProfile at35; normalization call48).
- `Library/PackageCache/com.unity.render-pipelines.core@2269be549234/Editor/Volume/VolumeProfileUtils.cs:167` (remove obsolete/null, normalize, add missing overrides).
- `Library/PackageCache/com.unity.render-pipelines.core@2269be549234/Runtime/Volume/VolumeManager.cs:458` (compatible type enumeration).
- `Library/PackageCache/com.unity.render-pipelines.core@2269be549234/Runtime/Volume/VolumeProfile.cs:340` (Sanitize removes null list entries).
- Existing Editor.log near22692 records build-triggered profile update; no new build run.

## 2. PC_RPAsset.asset

**User-observed difference:** additional-light/shadow, Forward+, SSAO and other shader-prefilter flags changed.

**Verified mechanism:** `ShaderBuildPreprocessor.OnPreprocessBuild` gathers features, calls `UpdateShaderKeywordPrefiltering`, marks each included URP asset dirty and explicitly saves it. These are serialized **Editor shader-variant selection/stripping inputs**, not direct runtime feature-enable switches. Boolean prefilter fields frequently mean strip/remove, so interpreting1 as feature-enabled would be wrong.

Current separate renderer data, `PC_Renderer.asset`, selects RenderingMode2 (installed enum: Forward+) and contains an active SSAO feature. Current RP asset has SRP Batcher1, dynamic batching0, additional-light shadows supported and soft-shadow quality3. Prefilter ForwardPlus2 means SelectOnly; AdditionalLight0 means remove that conventional keyword path, which does not mean Forward+ cannot light objects. The installed feature-gathering and prefilter code handle clustered lighting separately. Resource/variant retention for SSAO likewise does not itself turn SSAO on.

**Necessity:** build-time filtering derived from the actual included renderers/quality/platform/development configuration is legitimate and matters for shader availability. The saved flags are not a user requirement to change the game's lighting design. Broadly reverting or hand-editing them can produce unsuitable build variants and may be regenerated at the next build. No complete independent re-computation or variant validation was performed because invoking the preprocessor writes assets; exact acceptance of every value remains pending. Preserve runtime artistic/performance choices and review them separately from derived filtering data.

**Local sources:**

- `...universal@4d008a28541a/Editor/ShaderBuildPreprocessor.cs:230` (build callback),253(gather),493–498(update/dirty/save),1029–1054(mode selection).
- `...universal@4d008a28541a/Runtime/Data/UniversalRenderPipelineAssetPrefiltering.cs:11` (enums),276(assignment from gathered data).
- `...universal@4d008a28541a/Runtime/UniversalRenderer.cs:11` (RenderingMode).
- `Assets/Settings/PC_Renderer.asset:56` (mode),73(active SSAO).

## 3. UniversalRenderPipelineGlobalSettings.asset

**User-observed difference:** runtime settings list changed from empty to populated resource IDs.

**Verified mechanism:** SRP Core `RenderPipelineGraphicsSettingsContainer.OnBeforeSerialize` clears the runtime list, then fills it through graphics-settings stripping when `BuildPipeline.isBuildingPlayer` is true. `OnAfterDeserialize` clears that runtime list in the Editor. Editor settings and runtime settings are deliberately separate lists. This directly explains why a serialized build-time runtime list can differ from an empty Editor state.

Current file has35 managed-reference definitions and15 runtime IDs; **all15 resolve to definitions**. They include terrain-detail shaders and rendering resources/settings. A resource entry alone does not enable its associated feature (for example XR or ray tracing). Numbers are managed-reference IDs, not new external assets by themselves. See GlobalSettingsReadOnlyInspection.json.

**Necessity:** runtime resources/settings that survive stripping are needed by the built pipeline where used; the Editor does not require manually maintaining a populated runtime list. Exact list content depends on stripping/configuration. Mechanism is confirmed; exact historical serialization sequence and minimal necessity of each resource were not independently traced. Do not manually purge IDs or reconstruct the whole asset. Retain as instructed, with acceptance of the diff pending.

**Local source:** `Library/PackageCache/com.unity.render-pipelines.core@2269be549234/Runtime/RenderPipeline/RenderPipelineGraphicsSettingsContainer.cs:44` (OnBeforeSerialize),55(OnAfterDeserialize). Initialization also populates compatible settings through RenderPipelineGlobalSettings.Reset and RenderPipelineGlobalSettingsUtils; these were read, not invoked.

## 4. ProjectSettings.asset

**User-observed difference:** Standalone batching row added, static1/dynamic0.

**Verified mechanism:** URP's installed build validator calls `PlayerSettings.SetDynamicBatchingForPlatform` for the active target, deriving the value from all included URP assets. The baseline log identifies PC_RPAsset as the included asset; it has supportsDynamicBatching0, so the validator's requested dynamic flag is0. This gives a concrete build-time reason for writing platform batching data. Native creation/default serialization of the new row and the exact origin of static1 were not traced in available package code.

**Necessity:** dynamic0 matches the currently selected URP asset; it is not a universal engine requirement. Static batching is an optional rendering/memory tradeoff, not a prerequisite for a functioning scene. It is distinct from SRP Batcher and native terrain-detail instancing; enabling it does not automatically solve the flower-patch draw-submission cost. No evidence warrants changing either flag during this review. Retain the row pending approval, not because the engine universally requires static1.

**Local source:** `Library/PackageCache/com.unity.render-pipelines.universal@4d008a28541a/Editor/BuildProcessors/URPBuildDataValidator.cs:25` (derives dynamic flag),38(setter),63(validation call).

Unity's [Unity6.4 SRP Batcher documentation](https://docs.unity3d.com/6000.4/Documentation/Manual/SRPBatcher.html) distinguishes SRP draw-preparation optimization from generic batching. This supports treating the mechanisms separately, not a claim of measured savings for Briarwick.

## 5. UnityConnectSettings.asset

**User-observed difference:** top-level m_Enabled0→1; services activation not authorized.

**Assessment:** this is an **unexpected, unapproved configuration change**, not established as required by Unity6.4 or URP. No inspected URP rendering/build code requires this top-level flag for terrain, foliage or ordinary local rendering. The baseline's native-symbol upload403 proves a Unity Services request was attempted, but does NOT prove which code changed the flag or that the request required the persistent change.

Current file has multiple service-specific enabled flags at0 and a separate engine-diagnostics enable flag at1. These do not justify the top-level change and do not prove every service/network path is off. No credentials, account sessions or cloud dashboards were read, and no telemetry/privacy guarantee is made. Public [Unity C# reference bindings](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Editor/Mono/UnityConnect/UnityConnect.bindings.cs) expose cloud connection behavior but do not establish the native setter/cause for this exact serialized field; that source's master branch is supplementary, not version-pinned proof.

**Required? Not demonstrated; no rendering justification found. Cause remains unresolved.** Recommended approval decision is a narrowly scoped restoration of the top-level flag to its intended pre-task value, preserving every other earlier change, only after explicit authorization. Do not implement it now. If root-cause reproduction is later authorized, use a disposable project copy with full pre/post content backups and controlled service/build steps; do not repeat a long build or open Services settings in the working project merely to investigate this flag.

## Environment06 visual/performance disposition

User review supersedes any earlier positive candidate assessment: **NOT VISUALLY APPROVED**. Vegetation is excessively cluttered; ground appears artificial; rendering performance requires improvement. Coverage counts and passing traversal tests do not establish artistic success.

Earlier matched Editor data remains evidence, not new testing: extra154–189 reported draw calls despite only17k–43k added rendered triangles at sampled views. This points to investigating submissions/patches, card overdraw and composition together; it does not prove a GPU bottleneck. A successful build is not a standalone runtime benchmark, and no GPU measurement exists.

**No additional vegetation or expansion.** A future, separately approved correction should prioritize less clutter, intentional negative space, better ground/path/yard transitions and measured submission/overdraw reduction. No removals, density changes, shader edits or global setting changes are authorized by this review. No new screenshots, profiling or gameplay regression were needed for the documentation task.

## Approval state and verification

- Retain all five files exactly as found; no automatic accept/revert, no earlier uncommitted work discarded.
- Technical mechanism supported for profile normalization, prefilter generation, runtime-list population and dynamic-batching synchronization; this is NOT blanket approval of every resulting field.
- Static1 provenance/minimal necessity, exact removed/added profile content, per-resource minimality, and UnityConnect cause remain qualified/unresolved as above.
- UnityConnect top-level enable and Editor-test debris are not required for the intended local rendering workflow based on evidence found; proposed corrections require separate explicit approval.
- ReviewStartHashes.json/ReviewVerification.json verify all five files plus scene/TerrainData unchanged during this pass. Only documentation/evidence was written. No Unity execution, settings writes, scene changes, vegetation changes, Git operations, commits, pushes or branches. Stop for approval.
