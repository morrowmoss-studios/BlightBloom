# Production02 focused repair — 2026-10-18

Scene: `Assets/Scenes/CM_CrookedMortar_Production02.unity`. Saved, open in Edit mode.

## Changes

- **Door/shutter:** `ShopDisplay - approved insert only/CM_PairedWindowBay02_Shutter_L` was spread across the door sweep. Changed this scene instance's world yaw from 27° to 99°, retaining its hinge position, mesh, materials and other window components. Door still opens outward through 105°. Approved prefab unchanged.
- **Stair protection:** removed the redundant upper-flight wall-side balustrade and north turning-wall handrail/brackets from the Production02-only editable stair source and FBX. The adjacent full-height bedroom/north walls provide protection. Retained the centre sloping guard and stringers. Added a matching 1.65 m open timber guard across the exposed upper-floor edge over the lower flight, seated into the west wall and centre newel. Moved/renamed the former wall-side continuous safety box to this edge; corresponding physical timber meshes updated. No rooms, flights or landing dimensions changed.
- **Local camera:** the existing Production02-specific variant now cancels assist when look input arrives and gives it priority for one second. Stationary orbit no longer auto-recentres; movement assistance can resume after input quiets. Added local assist zones at kitchen, bedroom and study doorways. Preserved the requested pitch when considering the first candidate. During local obstruction, FOV eases from the original 65° toward a maximum 78° to retain more context; restores outside zones/on disable. Original boom collision casts, visible timber/wall collision, mouse scaling, player dimensions and shared traversal source are unchanged. Invisible safety guards remain player obstacles, not camera walls.

## Targeted validation

- `ShutterSweepValidation.json`: 211 samples over 0–105°, using the actual shutter mesh and door envelope expanded by 3 cm on every side: no intersections.
- `DoorInteractionValidation.json`: all 14 checks and nine related passage checks passed. Temporary keyboard E press/release events used the existing interaction binding and live animation; obstruction pause/resume and shop/kitchen circulation passed. No animation method was invoked to establish interaction success.
- `GuardValidation.json`: all 36 actual CharacterController checks passed: repeated edge pushes, adjoining wall protection, centre guard, ascent/descent, turn, and connected bedroom approach. Deterministic movement probes temporarily disable input/motor only during synchronous checks and restore them in finally.
- `LiveRouteValidation.json`: 19 connections passed through temporary Gamepad move events → existing TraversalInput → existing motor Update, with normal camera LateUpdate. Both flights/directions, intermediate turn, living/bedroom/study and kitchen connections included; no camera overlaps. Steering compensates for camera yaw, so this is not human feel approval. Head/torso stayed visible in stair-assist samples. Recorded two emergency recovery turns. Minimum recorded boom was 1.35 m at initial placement; whole-route median about 3.22 m.
- `ManualOrbitValidation.json`: full-circle Mouse.delta events through existing Player/Look input at bottom, turn, upper landing, kitchen and bedroom openings. All five passed; maximum requested/rendered mouse yaw difference <0.001°, no camera overlaps. This isolates input authority and collision safety, not manual comfort.
- Updated Blender source: 45 editable solids, positive volume, no non-manifold edges or degenerate faces. Unity import: five renderer groups / 4,860 triangles; UV0, finite normals and unit scale verified, approved walnut material retained.
- Current Unity Console: zero errors/warnings; no compilation failure. Historical Pipeline retained counts are not new findings. Scene restored to normal Edit-mode state; controller height 2 m, radius 0.4 m, step offset 0.3 m unchanged.

## Remaining concern / review

CM-005 remains open. Full manual circles deliberately facing close walls still retract to roughly 0.54–1.16 m in the tested positions. No visible geometry collision was bypassed. The change removes input fighting and gives more context, but does **not** establish comfortable visibility for every possible wall-facing orbit. Two automatic recovery turns remain in the live route. Please review mouse orbit, bottom approach and turning feel manually before accepting camera comfort; these limitations are not concealed by the passing route tests.

## Previews and scope

`Previews/Game_Bottom.png`, `Game_Turn.png`, `Game_UpperLanding.png` are actual Game-view captures at controlled player poses using the running local camera, with mouse look paused only during capture and restored afterward. They include an unfavorable bottom approach rather than hiding camera compression. `UpperOpeningGuard.png` and `DoorShutterClearance.png` are clean observer renders for geometry review, not gameplay framing claims.

Only Production02, its dedicated stair source/export, its scene-specific camera, and repair documentation/reports changed. No approved kit, shared gameplay source, package, project setting or other scene changed. An already modified shared slate material was present before this task and was left byte-for-byte unchanged. Nothing was committed.

Exact task files: `ChangedFiles.json`. Prior StairUsability02 reports describe the earlier revision; this report supersedes its camera/guard acceptance claims.
