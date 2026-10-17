# Crooked Mortar Production01 — open issues

Scene: `Assets/Scenes/CM_CrookedMortar_Production01.unity` (project-relative).
These are reported issues, recorded without investigation or fixes in this documentation task. Exact object names and locations remain unconfirmed; identify them before editing.

| ID | Description | Suggested investigation scope | Status |
| --- | --- | --- | --- |
| CM-001 | Hanging herbs visibly float or lack convincing attachments. | Inspect affected bundle roots, hooks/ties and canopy/beam contact in the production scene; check instance overrides before changing shared assets. | Open — reported; attachment audit pending. |
| CM-002 | At least one lantern floats away from its intended mount. | Identify the lantern and bracket, compare rendered geometry with mounting surfaces, and inspect transforms/overrides. Distinguish light gizmos from the rendered fixture. | Open — reported; location unconfirmed. |
| CM-003 | Unexplained diagonal markings appear on two walls. | Locate and reproduce in Game view; distinguish geometry overlap, UV/material discontinuities and lighting/shadow artifacts before choosing a fix. | Open — reported; cause unconfirmed. |
| CM-004 | Window treatments vary between glazing and boarded/opaque-looking openings. | Inventory only the affected window instances; distinguish intentional shutters/painted glazing from missing or mismatched materials. Agree on treatment before editing approved modules. | Open — art consistency decision pending. |
| CM-005 | Indoor camera comfort needs manual review. | Walk principal rooms, landing, stairs and doorways; orbit near walls and furniture. Judge visibility, retraction and capsule occlusion, beyond automated obstruction checks. | Open — manual acceptance pending. |
| CM-006 | Unity shadow-atlas resolution warnings need investigation. | Capture the exact warning and reproduction conditions; inspect relevant shadow-casting lights and active URP shadow budgets. Do not assume screenshot depth-buffer warnings have the same cause. | Open — reported; diagnosis pending. |

## Next milestone: production stabilization and manual acceptance

1. Confirm the repaired saved scene in a manual walkthrough: every principal room, bedroom floor, stair direction, entrance, perimeter and garden route. Any fall-through, blocked route, collider mismatch or unusable camera view is a functional blocker and takes priority.
2. Review CM-005 and diagnose CM-006. Camera obstruction that prevents navigation is a blocker; discomfort without blocked play is a refinement. Escalate shadow warnings if they cause missing/unstable lighting or significant performance loss; otherwise schedule rendering cleanup.
3. Resolve CM-001–004 in a focused visual-coherence pass after functional acceptance. These are deferred visual issues unless inspection reveals a collision or navigation impact. Preserve the approved architecture and kits.

No new structural blocker was confirmed by this documentation-only task. Earlier successful automated checks remain context, not a substitute for manual acceptance. Do not begin this milestone until requested; no new asset families or broad redesign are needed to start it.
