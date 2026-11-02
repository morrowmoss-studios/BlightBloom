# Briarwick Hamlet Dev01 — playable-scale layout review

New independent scene: `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`. Saved and left open in Unity 6000.4.5f1, Edit mode. Press Play; WASD moves, Shift sprints, mouse orbits, Escape releases the cursor. This scene reuses the unchanged input/motor/orbit scripts with a temporary 2 m capsule reference. It does not substitute or edit the Production02 plague doctor.

## Layout

Editable 320 × 320 m Unity terrain, from (-160,-170) to (160,150), with a shallow inhabited valley and surrounding hills. Height range approximately 2.59–44.40 m, mostly at the outer hills; main-road grades peak at 10.13°. Settlement including farming/garden reserves spans approximately 150 × 110 m. These are planning dimensions, not approved final architecture.

A curved south-to-north road crosses the west-to-east creek before reaching an organic 26 × 30 m village common. The well sits aside from the road centreline. Crooked Mortar faces the common from its northwest edge, near the northern woodland route. Forge and farmland occupy southern/eastern working edges. Chapel and graveyard lie west; the miller's site overlooks the north creek bank. The farmhouse has an auxiliary stable mass at the same primary location.

| ID | Primary location | Main footprint, metres | Centre X/Z |
|---|---|---|---|
|01|Crooked Mortar — actual prefab|7.254 × 13.756|-19 / 25|
|02|Inn / tavern|12 × 15|18 / 16|
|03|Blacksmith / forge|10 × 8|-26 / -25|
|04|Bakery|8 × 9|19 / -10|
|05|General merchant|9 × 10|-19 / 0|
|06|Elder's cottage|8 × 9|5 / 42|
|07|Farmhouse + stable|10 × 12; stable 8 × 11|47 / -30|
|08|Miller's cottage|8 × 9|38 / -47|
|09|Chapel|8 × 13|-44 / 30|
|10|Family cottage A|7 × 9|-43 / -4|
|11|Family cottage B|7.5 × 9|25 / 43|

The main road is nominally 5.2 m wide; the bridge reserves 4.8 m usable width across an 18 m span. Most footpaths are 2.4 m; smaller garden/graveyard links 2.2 m. Farm access is 3.2 m. House doors are visual approach markers only, 1.8 × 2.4 m; placeholder buildings are solid masses without interiors.

| Route | Approximate distance | At existing 3 m/s walk |
|---|---:|---:|
|Southern road start → common|149 m|50 s|
|Bridge centre → common|74 m|25 s|
|Common → northern woodland endpoint|96 m|32 s|
|Whole main road|245 m|82 s|
|Common-side junction → Crooked Mortar steps|18 m|6 s|
|Common-side chapel branch|41 m|14 s|

Times exclude pauses and use measured centreline lengths. Routes are sampling/planning geometry, not a NavMesh or NPC route system.

## Validation

- Scene saved, reopened successfully, one loaded scene, eleven identified sites, existing player input enabled.
- Crooked Mortar remains a connected instance of the exact requested Standalone01 prefab at unit scale: 503,363 visual triangles and five materials. Source models, prefab and materials were not edited. Its existing transition marker remains; no loader or interactive exterior door was added.
- Static route support/clearance sampling: all fourteen routes have ground support and no sampled human obstructions. Main road and bridge clear a 1.2 × 2.8 m horizontal, 2.6 m tall horse planning envelope. This is not validation with a real horse controller or mounted camera.
- In Play mode, the existing 2 m / radius .4 m / step .3 m CharacterController reached all sampled points on all fourteen routes forward and reverse, with grounded endpoints. After extending Crooked Mortar's path to the actual step edge, that route was retested both directions, plus the original porch steps up/down to the existing door-marker region. All passed. Motor/orbit components and starting position restored.
- These are synchronous CharacterController.Move collision tests, not injected-keyboard or manual comfort playtests. Normal existing controls remain available for manual review. No manual horse riding, NPC traffic, build, full-project regression or camera-comfort approval is claimed.
- Missing scripts/material slots: zero. Final Console: zero current errors/warnings; compilationFailed=false; no new captured warning/error entries beyond baseline cursor365. Existing historical Pipeline transport errors were not reproduced. A report-only Vector3 JSON serialization error after the initial scene save was fixed without rebuilding the scene; it was not a project compilation failure.
- 1,668 pre-existing Assets/settings/package/guide/tracking files match baseline SHA256, including all previous scenes and the standalone prefab/model. The approved Blender source also matches its known SHA256. See PreservationValidation.json. No settings, packages, shared gameplay, existing assets, Git tracking or old sources changed. No commit/push or LFS/cleanup work.

## Visual review and remaining work

Five requested views are direct Unity camera renders, captured in Play mode without gizmos or postprocessing. Planning labels are visible in the overhead view; the player/ground cameras omit their built-in Ignore Raycast layer so edge-on lettering does not obscure navigation. No geometry is hidden for these views.

- [Bird's-eye](01_BirdsEye.png)
- [Main-road approach](02_MainRoadApproach.png)
- [Common with Crooked Mortar](03_CommonAndCrookedMortar.png)
- [Creek and bridge](04_CreekAndBridge.png)
- [Crooked Mortar terrain contact](05_CrookedMortarTerrainPlacement.png)
- [Actual Play-mode existing player camera](06_PlayMode_ExistingPlayerCamera.png)

This is a layout candidate, not final environment art. Woodland cones are opaque combined massing proxies, not a foliage system. Fields, grave markers, bridge and ten houses are deliberately simple. Creek water is a visual strip without swimming/current gameplay; outer banks and valley boundaries need future terrain authoring. Hill slopes outside the reserved routes are not certified traversal areas. The solid placeholder houses have no entry or services.

Crooked Mortar's inherited Tripo contact collars, fused rock/ivy and provisional exterior colliders remain unchanged. Steps and foundation were visually inspected and the entrance route checked; a later village integration must refine local terrain blends and detailed rear collision without changing the approved source casually. The standalone door remains closed/fused and has no scene-loading implementation.

Recommended next review: judge street spacing, Crooked Mortar sightline, common size, farm/chapel placement and walking times in Play mode. Then approve or revise the layout before detailed landscape/architecture production. Horse turning, mounted camera, NPC circulation, creek safety and landmark silhouettes remain future work; no new systems were implemented here.

## Files and tools

Only new scene/assets under `Assets/BlightBloom/Environments/Briarwick/HamletDev01/` and this new review/documentation folder were created. CreatedAssets.txt lists all new Unity files including metadata. New blockout assets occupy about 1.45 MB before the scene file; the reused hero house is not reimported or duplicated as a new model.

BuildBriarwick.cs refuses an existing scene or asset folder and is intended only for initial new-candidate creation. RefineBlockout.cs and RecordLayout.cs record scoped corrections/measurement; the saved scene, TerrainData and mesh assets are the editable delivered state. RefineBlockout includes one-time winding/offset corrections and must not be rerun blindly. ValidateBriarwick.cs is read-only; ProbeBriarwickPlay.cs temporarily disables/restores local motor/orbit during its collision check. CaptureBriarwick.cs restores the review camera after capture. Read any snippet before use; do not regenerate over the saved scene.

STOPPED for visual review. No production/interior integration, external archiving, Git protection, package installation, commit or push.
