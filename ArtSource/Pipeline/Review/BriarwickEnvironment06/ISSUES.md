# Environment06 issues

| Issue | Status | Next action |
|---|---|---|
| Five settings/profile files differ around baseline build | **Retain unchanged; approval pending** | User comparison documented; installed-source technical review in SettingsReview/TechnicalReview.md. No blind reversion. |
| Standalone runtime performance | Unmeasured | Build succeeded; desktop launch hung. Target-build/GPU capture needed; no FPS/GPU claim. |
| Extra native patch submissions | Measured review concern | +154–189 reported Editor draw calls in matched views; profile before expanding density/range. |
| Distant culling / high-view simplicity | Outstanding |95m distance retained, no source LODs/global fog changes; later approved art/performance decision. |
| Close foliage-card repetition | Outstanding refinement | Alpha-fitted bowed strips improve silhouettes; not bespoke volumetric botany. |
| Natural debris / reeds unavailable | Asset gap | Purpose-built compatible assets later; no architectural substitutes. |
| Environment06 artistic result | **NOT VISUALLY APPROVED** | Excessively cluttered vegetation, artificial ground, performance needs improvement. No additions or expansion. Counts do not imply artistic success. |
| Navigation and source-map preservation | Passed targeted checks |20 route runs,22 approaches,102 tree tests and normal-input route passed; original79,032 maps intact. |

| Additional review finding | Status | Action |
|---|---|---|
| Default profile has five unreferenced Editor-test subassets | Verified YAML finding; not production-required | Retain untouched; targeted cleanup/value review needs separate approval. Origin timing unresolved. |
| UnityConnect top-level m_Enabled0→1 | Unexpected/unapproved; rendering necessity not demonstrated | Retain1 for now as explicitly requested; investigate/restore only after approval. |

## 2026-11-05 — Environment06_Revision01 follow-up

The original entries above describe the pre-revision candidate. [Revision01 report](../BriarwickEnvironment06_Revision01/README.md) and [current issues](../BriarwickEnvironment06_Revision01/ISSUES.md) record the new candidate: native details84,204→22,914,199coarse filler chunks disabled, owned short-turf/grass derivatives, reduced paired Editor rendering cost. Original detail maps are now intentionally reduced, with before snapshots preserved; the old unchanged79,032-map result is historical. Approved trees/colliders and unrelated architecture/settings remain unchanged.

**Still awaiting visual approval.** Ground repetition/uniformity, road outlines, close grass cards and standalone performance remain limitations. Historical NullReference stack points to UnityEditor.WindowLayout maximization; no recurrence during current tests. Automated traversal/approaches/trunks pass. Normal-input locomotion/orbit follow-up now passes after unlocking/focusing Unity:12waypoints,207grounded samples, idle/walk/sprint/stopping and91.96°orbit. Earlier focus failures remain recorded; no manual camera-comfort claim. No expansion or global settings changes.
