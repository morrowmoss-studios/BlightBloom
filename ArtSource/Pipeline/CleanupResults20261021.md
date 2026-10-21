# BlightBloom approved cleanup results — 2026-10-21

Completed approved groups D and H only. Group R is preserved. **Nothing staged, committed or pushed.**

- Recovery commit verified: `6253fc0d57f9c0f6bf3c5c0210003d67b9fb03d9`. Candidate hashes and Git blobs matched; live dependencies and serialized inbound references rechecked before deletion. No skipped candidates.
- Removed 260 primary files (about 110.28 MiB), 174 corresponding Unity file metas and 28 empty-folder metas: **462 tracked files total**. Imported assets/scenes removed with `AssetDatabase.DeleteAsset`; folders removed only when genuinely empty. Deletions exactly match the approved paths; no unlisted deletion.
- Exact path inventory, individual operation results, skipped-candidate map (empty) and test data: `CleanupResults20261021.json`. Original approved manifest remains unchanged in `CleanupAudit20261021.json`.
- All 870 protected-file hashes unchanged, including Production02 and its dependencies. All 31 primary Blender sources retained, with painted sources, approved kits, benchmark/review scenes, current Locomotion03 and its recoverable predecessors. All 132 retained scene/prefab dependency sets are unchanged.
- AGENTS.md now identifies Production02 as the current playable candidate and points to the historical recovery record. Historical source documentation/issue tracker retained; the audit report links to these execution results.

## Targeted verification

| Check | Result |
| --- | --- |
| Production02 reopening | Passed; no missing scripts, object references, materials or prefab instances. Current avatar and BB_DoctorLocomotion03 controller present. |
| Idle, walking, sprinting, turning/stopping | Passed in focused Play mode through full W / LeftShift and the unchanged input/controller path; walk ~3 m/s, sprint ~6 m/s; live elbow/knee transforms and distinct states sampled. No direct pose/animation-method invocation. |
| Stairs and connected rooms | Passed 19 waypoints: ascent, intermediate turn, upper landing, bedroom/study/living connections and descent; normal motor/camera enabled. |
| E-key front door | Passed eight entry/exit/shop/kitchen waypoints, using E input through the existing interaction path. |
| Garden and exterior route | Passed 12 treatment/storage/garden/perimeter waypoints. |
| Unity compilation/Console | No compilation failure, new error or warning. Final Console: zero errors/warnings. Retained historical Pipeline timeout buffer entries were not cleared. |
| Final scene state | Production02 remains open in Edit mode, clean/unsaved-change flag false; temporary test object/devices cleaned up. Scene file unchanged. |
| Scope/Git | Deleted paths match all 462 expected paths, protected hashes unchanged, diff whitespace check passed. No staging, commit, push or history rewriting. |

Smoke tests establish no observed cleanup regression; they do not replace manual camera-comfort or animation-art approval. Existing cloth/stair-foot-placement polish and previously tracked usability/visual issues are unchanged. No regeneration, redesign, package or settings changes.

Untracked `ArtSource/Pipeline/.idea/` was present before cleanup and remains untouched. Exclude it from the future checkpoint unless separately authorized. Generated caches/logs were left alone while Unity was running.

## Prepared checkpoint — approval required

```text
chore: archive superseded BlightBloom prototypes and test outputs

Remove approved D/H legacy scenes, exclusive exports, captures, autosaves and one-off tools.
Preserve Production02, approved libraries, current locomotion, editable sources and recovery history.
Update AGENTS.md and record the exact removal inventory.
Verify retained dependencies and focused locomotion, stair, E-key door and garden smoke tests.
```

Stage only the approved deletions, AGENTS.md and the four cleanup audit/results documents. Do not stage unrelated editor data. Await separate user approval before committing or pushing.
