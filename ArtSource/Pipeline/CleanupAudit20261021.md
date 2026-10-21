# BlightBloom cleanup audit — 2026-10-21

**Proposed only. No deletion, moving, asset edits, scene saves, settings edits, staging or commits performed.** Approval applies only to the explicit paths in `CleanupAudit20261021.json`; recheck hashes/references before execution.

## Evidence and recovery

- Initial Git working tree clean. Recovery anchor: `6253fc0d57f9c0f6bf3c5c0210003d67b9fb03d9` (`feat: upgrade plague doctor rig and locomotion`). Every proposed file has a verified blob at this commit; SHA-256 values and Unity metas are recorded in the manifest.
- Existing Unity Editor open in Production02, Edit mode, not compiling. Queried `AssetDatabase.GetDependencies` for all 23 scenes and 124 BlightBloom prefabs once; checked serialized inbound GUID references, runtime loading patterns and build-scene entries. The first Pipeline query timed out but completed and wrote its result; no second Editor was launched.
- No proposed file is a dependency of any retained scene/prefab or a protected kit. No serialized inbound references remain outside the proposed group. This is dependency evidence, not post-cleanup runtime validation.
- SampleScene is currently the sole enabled Build Settings scene. Retain it; changing the startup/build scene is a separate decision.
- Git history is sufficient to recover the proposed historical bytes **while this repository/history is retained**; it is not an independent off-machine backup. Do not rewrite/prune that history. Restore historical assets and their metas together at original paths. Primary Blender sources and painted artwork stay in the working tree; no extra duplicate archive is needed for committed exports/captures/autosaves.

## Approval groups

| Group | Proposal | Scope |
| --- | --- | --- |
| D — disposable | Delete after approval | Tracked root `.DS_Store` and the Blender522Probe FBX, glTF and copied README: 4 primary files, about 0.03 MiB. Retain the pipeline test Python utility/source documentation outside the imported probe folder. |
| H — historical | Git-archive: remove from active checkout after approval, recoverable at the anchor above | 256 primary files, about 110.25 MiB: 11 scenes, 160 exclusive generated assets, 43 obsolete preview images, 14 `.blend1` autosaves and 28 one-off study/capture scripts. All actual `.blend` files remain. |
| R — retain | No changes | Production02, approved benchmark and libraries, current character and recovery dependencies, active validation/modeling pipeline, editable art, documentation and issue tracker. |

Unity cleanup additionally removes 174 paired file `.meta` files and up to 28 folder metas **only after those folders are empty**. Parent folder deletion is not permission to delete unlisted contents. Approximately 110.28 MiB removed from the checkout, not from Git history or the import cache.

## H: superseded scenes

- `Assets/Scenes/CM_BotanicalPlanterKit01_IntegrationPreview.unity`
- `Assets/Scenes/CM_CrookedMortar_ArchitecturalRedesign01.unity`
- `Assets/Scenes/CM_CrookedMortar_B_StyledProof06.unity`
- `Assets/Scenes/CM_CrookedMortar_ConceptReconstruction02.unity`
- `Assets/Scenes/CM_CrookedMortar_ConceptReconstruction03.unity`
- `Assets/Scenes/CM_CrookedMortar_MassingRefinements05.unity`
- `Assets/Scenes/CM_CrookedMortar_MassingStudies04.unity`
- `Assets/Scenes/CM_CrookedMortar_Production01.unity`
- `Assets/Scenes/CM_EntryPortal02_IntegrationPreview.unity`
- `Assets/Scenes/CM_SlateRoofKit01_IntegrationPreview.unity`
- `Assets/Scenes/UncleRobertsApothecary.unity`

Retain all seven `*_ArtReview.unity` scenes: WindowBay01, EntranceBay01, EntryPortal02, FacadeBay01, SlateRoofKit01, PairedWindowBay02 and BotanicalPlanterKit01. They are reusable library QA fixtures; Production02 does not replace that purpose.

## H: generated exports and supporting assets

- Retire the Unity export folders `Redesign01`, `ConceptReconstruction02`, `ConceptReconstruction03` and `MassingStudies04` under `Assets/BlightBloom/Art/Architecture/CrookedMortar/`, with their retired scenes.
- In `MassingRefinements05`, retire only A/C model exports and the Path/Site materials; keep B and every shared dependency.
- In `Production01`, retire only the 17 exclusive generated assets listed in the manifest. Keep the shared linen, plaster, stone and walnut materials and approved paint atlas used by Production02.
- Retire the old `Assets/BlightBloom/Locations/ProxyMaterials`, `ReferenceFacade` and `StorybookExterior` export folders, which are exclusive to the retired original Uncle Robert scene.
- Keep all Production02 adapters and assembly prefabs even when unpacking means there is no current scene GUID reference. They remain useful production templates.

## H: historical outputs and utilities

- Retire 43 preview images only from obsolete Redesign01, ConceptReconstruction02/03, MassingStudies04, MassingRefinements05, StyledProof06 and Production01 study folders. Keep approved benchmark, current production, kit and character previews. Retain historical README files and validation reports rather than discarding failure/acceptance context for negligible space savings.
- Retire the 14 explicitly listed `.blend1` autosaves via Git history; retain all 31 primary `.blend` files and all painted source images, including earlier approved geometry/paint variants.
- Retire 25 one-off historical scene-study/capture scripts under `ArtSource/Pipeline/Review` and the three old `Tools/Apothecary*Pass.cs` scripts. Keep model/export generators, current Production02/character tests and captures, kit validation/creation utilities, and the small compiled scene builders. Historical regeneration may require restoring the retired scene/export chain from Git; do not run old mutating utilities as validation of current production.

## Protected findings

- Keep all six approved kit folders plus EntranceBay01, shared materials, neutral/painted variants, shutters and future village modules. No asset is selected merely because Production02 does not reference it.
- `StyledProof06` assets remain dependencies of StyledDetails07, Production02 and library prefabs; keep the whole export folder despite archiving its scene.
- `Prototypes/CrookedMortarUsability01/BlockoutDoor.cs` and `Prototypes/CrookedMortarProduction02/Production02StairOrbitCamera.cs` are live systems. Keep both prototype folders; their names do not imply obsolescence.
- Keep Locomotion03 FBX, prefab, controller, script and shared painted material/atlas. Rigged02 and the original rigid avatar are still dependencies of disabled scene recovery instances. Do not delete or detach them in this pass. Their later retirement needs explicit approval after current locomotion acceptance.
- Three texture PNGs are byte-identical: Production01 approved paint, SlateRoofKit01 approved paint sheet and BotanicalPlanterKit01 container paint. All have live material references under separate GUIDs. Keep all; consolidation would modify approved library references/import assumptions.
- Keep Production02, StyledDetails07, UsabilityBlockout01, TraversalSandbox and SampleScene. Keep `AGENTS.md`, all production documentation, issue tracker, package configuration, URP/input settings and gameplay code.
- Leave ignored `Library`, `Temp`, `Logs`, `UserSettings`, generated IDE projects and OS-managed temporary directories alone while Unity is open. They are regenerable caches, not Git cleanup targets.
- `AGENTS.md` still names Production01 as the playable candidate; after approval update that compact reference to Production02 without rewriting project history.

## Execution and verification after approval

1. Recheck clean/expected Git scope, candidate hashes and references. Any changed/new dependency pauses that candidate.
2. Use Unity AssetDatabase deletion for listed imported assets/scenes and their metas; use explicit paths for non-imported history files. Remove only verified empty folders. Preserve protected asset GUIDs and avoid broad directory deletion of mixed-use folders.
3. Record an exact deletion manifest. Update affected active documentation links to identify Git-archived history; preserve original historical records. No missing asset references are expected and no material/prefab retargeting is planned.
4. Open Production02 in the existing Editor; check missing scripts, asset/material/prefab references and compilation. Focused Play-mode smoke test: avatar idle/walk/sprint, stairs both ways, E-key front door and garden route. Report automation/known warnings separately from newly introduced failures. No full rebuild or broad art regeneration.
5. Review the diff and prepare, but do not execute, a checkpoint commit. Proposed subject: `chore: archive superseded BlightBloom prototypes and cleanup project`. Proposed body: preserve Production02, reusable kits, current locomotion and editable sources; retire verified legacy exports/review outputs; record recovery anchor and targeted smoke-test results. Commit or push only after separate explicit approval.

## Current task changes

Created this report and `CleanupAudit20261021.json` only. No game assets, scenes, scripts or settings changed. No cleanup or gameplay validation performed yet; awaiting approval for groups D and H.

## Approved execution

Groups D and H were explicitly approved after manifest review on 2026-10-21. Group R remains protected. The original proposal/manifest above is retained as the approval record. Exact removal inventory and verification results: `CleanupResults20261021.json` and `CleanupResults20261021.md`. No commit or push is authorized.
