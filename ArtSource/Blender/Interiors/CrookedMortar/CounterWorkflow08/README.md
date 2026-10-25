# Counter Workflow08 — expressive storybook furniture

Isolated experiment; **not approved or installed in Production02**. Open `Assets/Scenes/CM_CounterWorkflow08_Review.unity`. It duplicates the Workflow07 shop context and retains both counter versions at the exact same functional placement, with Workflow08 visible by default. Original C05 art also remains recoverable. No extra dressing, lighting changes, room changes or gameplay modifications.

## Design and production method

Workflow07 improved carving but kept a rectangular cabinet read. Workflow08 reconstructs the load-bearing furniture instead of applying more ornament:

- Serpentine, rounded breadboard worktop with a modeled ogee section, flat service plane and unchanged 1.0525m local top datum.
- Four continuous, shouldered timber supports with inward waists and outward feet; foot bottoms match the shop floor.
- A scalloped lower frame and open space beneath replace the continuous solid plinth. Bowed end walls, quiet recessed side fields and shaped central stiles connect the construction.
- Enclosed storage bottom, service-side drawers and forged bails remain practical. Cosmetic inset drawers are not interactive drawer mechanisms.
- Only the central mortar-and-pestle/laurel board retains dense relief. Its carved surface follows the same curved substrate and shared border datums as the frame. No additional botanical plaques or loose props.

The new source is authored cross-section/curve geometry and a reused sculpt stencil, not subdivision applied indiscriminately to the old box. `build_counter08.py` preserves separate construction parts in the editable Blender file and joins copies for export. `CM_CounterWorkflow08.blend` contains those parts, the dense sculpture, source paint-value attribute, a final game mesh and a plain-board form comparison.

The established FBX coordinate conversion is retained as transport only: metres, Unity +Y up / +Z front, zero pivot, unit scale. Working envelope remains 2.28 x 0.78m. Existing functional collider and markers stay on the original scene counter root.

## Illustrated surfaces and registration

`WalnutPaint.png` is a dedicated built-in imagegen gouache walnut colour sheet; see `Prompts.md`. Shaped supports have continuous lengthwise UVs. Structural members have grain-oriented projection with proper end-face mapping. The first trial projected the sculpture face by face, which introduced grain discontinuities: that was corrected, not accepted.

The central relief now has **one continuous UV domain**. Its colour is baked in Blender from the painted wood, a restrained warm colour group and a `SculptPaintValues` attribute derived from the actual sculpt height. It is an emission/colour bake, **not a lighting, AO or normal bake**. This precisely registers the broad painted values to the mesh. No separately generated leaf/mortar image is placed over the sculpture, so the old mismatched motif-edge problem is avoided. The original sculpt stencil remains a protected Workflow07 dependency; it is not regenerated.

The initial bake was too grain-dominated in close-up. The final bake quiets the wood inside the central carving and uses a wider, deliberate raised-value group. Fine stencil edges still warrant artist cleanup; this is not a fully undercut hand sculpture.

## Fair comparison

`Previews/Existing` is Workflow07; `Previews/Candidate` is Workflow08. `Previews/Comparison` contains matching pairs, 07 left / 08 right:

- `GameplayDressed`: actual existing player-camera position, pinned identically for the second version.
- `FrontBare`, `AngledBare`: existing loose counter props hidden at runtime.
- `FrontDressed`: the same original dressing restored.
- `CarvingClose`: close inspection of materials and relief.
- `ClayBare`: neutral material, actual relief retained.
- `SilhouetteBare`: neutral material **and relief removed from both versions**, without changing their original structural forms. `BuildForm07.py` creates a comparison-only derivative inside Workflow08; it never writes Workflow07.

All are Unity Game-view captures using identical room lighting/exposure. Inspection cameras are temporary runtime poses, not claims about normal orbit-camera comfort. Visibility, meshes, camera and player placement are restored before leaving Play. No generated beauty illustration or paint-over is presented as a screenshot.

## Assessment and reusable principles

There is a demonstrable geometric improvement: the negative space beneath the frame, curved shoulders, waisted supports, bowed ends and shaped top remain legible without textures or carving. The counter reads as a designed object rather than a rectangular carcass with three ornate panels. The selective central motif better supports a visual hierarchy.

The material treatment is more unified and accurately registered, but Workflow07's separately painted motif has crisper illustrative linework than this geometry-registered colour bake. Workflow08's carving is quieter and more integrated; it should not be claimed as universally superior in close-up ornament. The smoothly rounded supports also risk feeling more formal/curvilinear than rough medieval joinery. These are artistic review decisions, not reasons to decorate the room further.

The source image's warmth and craftsmanship are approached, not achieved in full. The candidate has deliberate curved forms but remains fairly bilateral. It still needs selective artist-led edge breaks, end-grain/pegged joint painting, and fine carving cleanup before final hero approval. No LOD/normal-map asset was delivered; the high-detail review mesh needs a chosen budget before reuse throughout the village.

In context, the unchanged shelving has straight, thin rails and simpler flat panels; the current player and props also have simpler surface treatment. The surrounding timber's stretched/striped atlas grain is more apparent beside the new counter. These mismatches are documented, not changed.

Principles for future assets: approve the unornamented silhouette first; make bearing/load and joinery readable; use a few shaped structural members and varied recess depth; reserve carving for a focal field; align grain to each piece; derive paint registration from the actual mesh; retain quiet areas; review at gameplay distance in existing lighting before multiplying detail. Do not solve mismatches with clutter or by automatically copying the same scallop/leg profile to every object.

## Validation and scope

See `SourceValidation.json`, `IntegrationValidation.json`, `ClearanceValidation.json`, `ProtectionValidation.json` and `ConsoleValidation.json` for final evidence.

Source checks cover finite geometry, normals, UVs, degenerate triangles, scale and pivots. Unity checks cover imported mesh channels and material/script references. All 116 existing colliders remain unchanged; no new colliders. The 43-pose unchanged outward door sweep clears the candidate. 190 capsule-volume samples cover entry, customer/staff counter sides and nearby stair/kitchen connections using the unchanged 2m / 0.4m CharacterController.

These are **static geometry/clearance checks**, not fresh live-input walking/sprinting/stairs/door-interaction tests. Actual Play mode was used for visual captures; no fresh manual gameplay/camera-comfort approval is claimed. Functional systems were not changed. Production02, Workflow07 scene/sources/assets are hash-checked unchanged. Only the new review scene, new Workflow08 assets/source/evidence and the issue tracker are changed. Nothing committed or pushed.
