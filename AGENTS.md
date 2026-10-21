# BlightBloom working guide

## Project references

- Unity 6.4 / URP; Blender 5.2.2 LTS. Project root is this directory; never create a nested Unity project.
- Playable candidate: `Assets/Scenes/CM_CrookedMortar_Production02.unity`.
- Approved visual benchmark: `Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity`. Preserve its storybook silhouette and matte painted palette; do not overwrite reference/review scenes.
- Approved asset folders under `Assets/BlightBloom/Art/Architecture/CrookedMortar/`: `EntryPortal02`, `FacadeBay01`, `SlateRoofKit01`, `PairedWindowBay02`, `BotanicalPlanterKit01`, and `WindowBay01`. Reuse suitable existing signage and lanterns.
- Editable sources and asset documentation: `ArtSource/Blender/Architecture/CrookedMortar/`; painting sources: `ArtSource/Paint/Architecture/CrookedMortar/`.
- Production notes and issue tracker: `ArtSource/Blender/Architecture/CrookedMortar/Production01/README.md` and `ISSUES.md`.
- Existing Editor automation snippets: `ArtSource/Pipeline/Review/`. Traversal scripts: `Assets/BlightBloom/Traversal/`.

## Efficient execution

- Inspect only the requested change's files, scene objects, components and dependencies. Reuse established knowledge; avoid full-project inventories unless shared systems are affected.
- Make the smallest complete, reliable change. Preserve approved art, prefabs, working systems and unrelated files unless explicitly authorized otherwise.
- Reuse existing modeling/export/Editor utilities. Do not regenerate unchanged assets or recreate validation tools unnecessarily.
- Use the existing running Unity Editor through Pipeline/MCP. Do not launch a second Editor or delete lock files. Report connection blockers.
- Follow the established Blender → FBX → Unity export conversion: metric scale, Unity +Y up and +Z exterior. Reuse the relevant asset's exporter and check pivots, UVs, normals and material assignments when changed.
- Production02 contains scene-local architectural and gameplay overrides. Do not regenerate or reapply prefabs over the saved scene without inspecting them. Historical studies, including Production01, are recoverable at Git commit `6253fc0`; see `ArtSource/Pipeline/CleanupAudit20261021.md` and its approved manifest.
- Read automation snippets before execution: scripts named `Validate` may modify meshes, colliders, prefabs or scenes; traversal probes may disable components during Play mode. Reuse only applicable operations, then restore normal state.
- Ask before destructive actions, major redesigns, dependency installations or unrelated changes. Never commit unless explicitly requested.

## Validation and reporting

- Documentation-only changes: review text, links and changed-file scope; do not launch Unity or run gameplay regression tests.
- Local art/placement fixes: inspect affected geometry, attachments, references and materials; check nearby collisions/routes if relevant. Capture only views needed to judge the change.
- Floors, walls, openings, stairs or structural collision changes: test affected surface coverage and transitions, not just a few waypoints; exercise principal rooms, stairs both directions and garden circulation when connected routes are affected.
- Shared gameplay/input/camera changes: run broader relevant regressions. Never omit necessary correctness, collision or gameplay checks to save usage.
- Check current compilation and Console results for Unity changes. Distinguish historical logs, automation/capture messages and reproducible gameplay problems. Automated camera obstruction checks do not establish manual camera comfort.
- Reuse existing reports as context, not proof of the current scene. Inspect only the relevant baseline/diff and confirm unrelated assets/settings remain untouched. Do not repeat passing checks unless new changes or unresolved concerns justify it.
- Keep screenshots and documentation proportional to the task. Report concise changes, tests, results, remaining issues and changed paths; distinguish automated checks from manual playtesting. Update the issue tracker when an issue is confirmed or resolved.
