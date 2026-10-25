# Structural craftsmanship benchmark 05

Two areas only: existing front entrance/facade construction, and the shop counter with its ceiling beam. No furnishing/clutter pass and no propagation to the preparation room.

## Changes

- The counter is a replacement visual body with genuinely recessed arch-headed panels, convex carved mortar/foliage, shaped lower stretchers, a swept apron, engaged turned columns, rounded plank worktop, and curved drawer fronts/forged bails. The old body, overlapping HeroRefinement02 body and Illustrated04 printed applique are hidden scene-locally. Existing collider, root, markers, countertop objects and textile stay in place.
- The portal retains its approved post spacing and quadratic arch centreline. Its new mesh uses tapered/fluted posts, stepped shoes/capitals and continuous compound-coved arch sections. Old geometry/LOD rendering and the redundant HeroRefinement02 overlay are hidden; sign, lanterns, herbs and other attachments remain separate and unchanged.
- Two broad front floor beams and the four existing storey corner posts receive continuous hewn/coved profiles with controlled taper and drawbores. The original base rail and upper gable structure remain. The shop ceiling beam receives the same treatment within its existing bearing envelope.
- The three measured front plaster meshes retain their openings, dimensions and UVs, with a few broad authored trowel swells of 4–6 mm. The existing stone surround retains its block layout with restrained shallow face shaping. Small fitted plaster returns close the previously visible rectangular-to-arched reveal corner voids outside the door leaf.
- Only the two front horizontal eave faces are coved; corrected roof junction/end zones and upper/rear roof vertices are preserved. Slate geometry/material, roof heights and silhouette are not changed. Existing paired window/casement assets are preserved; this is not a new window design.
- The four new timber/furniture derivatives reuse the existing gouache walnut material rather than the previous graphic banded wood. No new texture generation, lighting, exposure, post-processing or global material edits.

## Source and recovery

Editable source: `CM_Craftsmanship05.blend`. Builder: `build_craft05.py`, using established metric +Y up / +Z exterior export helpers. `MeasuredSurfaces.json` / `MeasuredEaves.json` preserve actual scene geometry used for fitted derivatives. Unity outputs: `Assets/BlightBloom/Art/Interiors/CrookedMortar/Craftsmanship05/`.

Original approved kits and Blender sources are untouched. Prior state is recoverable at existing Git commit `7e7f330`; no commit was made during this pass. Installation snippets are records of the one-time operation, not commands to rerun over Production02.

## Review evidence

`Previews/Before` and `After` contain matching actual Unity Game-view captures at ordinary player-camera positions: FrontEntrance, FacadeAngle, Counter, CounterAngle, ShopArchitecture. `GameViewPoses.json` records the camera transforms/FOV. After captures pin that same normal camera only while capturing, then restore it. Close views supplement the matching comparisons. No lighting change, paint-over, observer render or additional loose props is used to manufacture the comparison.

Judge profile/relief depth and construction, rather than object counts. The counter is more sculptural and the portal/beam profiles catch light more clearly. Plaster and eave changes remain deliberately subtle; this is not a completed reference-level craftsmanship pass across the building. Window framing remains the approved existing construction. Some carving/stems are still simplified, and much of the exterior remains quieter than the aspirational illustration. Manual artistic approval is still required before extending this treatment.

## Validation

`SourceValidation.json`: UV, coordinates, normals, degeneracy and metre-scale checks. One inherited eave triangulation degeneracy was corrected. An attempted plaster micro-bevel produced degenerate faces and was omitted, preserving the validated wall topology.

`IntegrationValidation.json`: imported geometry/material/script references, unchanged 116 baseline colliders, and 43 door-sweep poses through the existing 105-degree outward arc. `ClearanceValidation.json`: dense 0.10m capsule-volume probes against the new visible meshes using unchanged player dimensions, covering entry, customer/staff counter sides, stair connection and kitchen route. This is static geometry validation, not a claim of fresh live-input playtesting or manual camera comfort. No movement/input/camera/door code was modified.

Loose props, furniture station markers, room layout, door logic and collision setup remain unchanged. The final clearance probe passes 190 samples. The first probe started 0.30m from the existing front wall, inside the unchanged 0.40m capsule radius; that invalid test start was corrected to 0.60m rather than altering architecture. No fresh input-path movement or E-key test was performed for these cosmetic mesh replacements; the existing controller/camera remained enabled during Play-mode capture. Final Console results and exact file inventory are recorded with the completed check outputs. Nothing committed or pushed.

Final Editor state: Production02 saved and open outside Play mode, with no temporary probes. Source validation passes all ten derivatives; import/reference validation and 190 clearance samples pass. Console reports zero current errors and two retained prior warnings, with no new captured entries after this pass's initial Pipeline timeout. No project compilation failure. No loose props added/moved. Roof-junction preservation: all 6,456 original vertices outside the two edited cove bands match within 0.2 mm. Unity serialization produced four empty-override `value: ` trailing spaces reported by git diff --check; no semantic scene issue, and no unrelated YAML reformat was performed.
