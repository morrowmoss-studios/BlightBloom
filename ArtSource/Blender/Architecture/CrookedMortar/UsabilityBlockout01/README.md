# Crooked Mortar — expanded usability blockout 01

Scene: `Assets/Scenes/CM_CrookedMortar_UsabilityBlockout01.unity`.

This separate neutral blockout tests the approved expanded room arrangement. It does not replace Production01 or integrate finished art. The envelope is 11.4 × 9.4 m excluding porch: a dominant front shop/living volume, offset rear bedroom/treatment and stair volume, recessed kitchen/study wing and lower storage extension. Steep hero gable and subordinate roofs are silhouette guides, not resolved production roof junctions.

## Actual clear dimensions

| Space | Clear size | Notes |
|---|---|---|
| Shop | 5.4 × 4.4 m | 2.2 × 0.75 m counter; direct kitchen opening |
| Treatment | 3.6 × 4.4 m | 0.9 × 2.0 m exam bed; cabinet |
| Kitchen/prep | 3.4 × 4.2 m | 0.65 m bench depth; 2.75 m central width beside east bench |
| Storage/garden vestibule | 3.4 × 2.4 m | 0.45 m shelves; 2.5 m between shelf faces |
| Bedroom | 3.6 × 4.4 m | 1.6 × 2.1 m bed; 1.0 m side aisles; wardrobe near foot end |
| Study | 3.4 × 4.2 m | 0.70 m desk; 0.35 m rear bookcase |
| Living | 5.4 × 4.4 m | Open to landing / west-return nook; no boxed corridor |
| Landing reserve | 2.4 × 2.4 m | Within combined living/landing floor; do not double count |
| U stair bay | 3.2 × 4.2 m | 1.5 m flights; 1.5 m deep turning platform |
| Ground stair lobby | 2.0 × 2.4 m | Local turning space connects shop to lower flight |

Room dimensions are between wall faces. Walls are 0.20 m. Room doorways are 1.8–2.0 m wide, 2.75 m high. Floor surfaces are +0.20 / +3.60 m: 3.40 m rise, 3.10 m clear ceilings. Stair: 18 risers at 188.9 mm, 300 mm goings. Exterior footprint is irregular; room areas do not imply a filled rectangular envelope. See `FloorPlan.svg`.

## Comparison with Production01 assessment

- Treatment: about 4.5 → 15.84 m²; bedroom: about 8.5 → 15.84 m².
- Kitchen: about 5.2 → 14.28 m²; bench aisle about 1.05 → 2.75 m.
- Storage: about 2.7 → 8.16 m². Study: about 5.2 → 14.28 m².
- Doorways: roughly 1.3–1.6 → 1.8–2.0 m. Stair flight: 1.25 → 1.5 m.
- The old 0.84 m landing restriction is replaced by an open 2.4 m landing reserve.
- Kitchen access no longer goes through treatment. The front door swings outward into a reserved porch pocket, never into that interior branch.
- Ceiling clearance increases from roughly 2.5–2.66 → 3.10 m. Full 4 m camera orbit is still not possible at every wall/bedside position; unchanged camera settings must be manually judged indoors.

## Test controls

Open this scene alone and press Play. WASD / Shift / mouse / Escape retain existing behavior. Press **E** within 3.2 m of the front hinge to toggle the temporary front door; stand clear of the marked outward swing pocket. Approach from (4, -2.5) or operate from inside the shop. The leaf pauses if its actual sweep would hit the player and resumes when they step clear; an on-screen message explains the obstruction. The new `BlockoutDoor` is a scene-local fixture; no shared gameplay/input scripts or existing prefabs are edited. The rear garden opening and internal openings deliberately have no leaves yet.

## Review boundaries

Furniture is solid full-size blockout geometry. Cosmetic roof guides carry no colliders; sealed ceilings define indoor headroom. Existing controller/camera and their serialized settings are cloned unchanged from Production01; only the scene spawn moves. Front-door hinge and wall/floor/furniture/stair colliders are new in this scene only.

Validation and remaining concerns are recorded after the targeted Editor checks; do not infer manual camera comfort from automated reachability.

## Targeted validation — Unity 6000.4.5f1

- **56/56 connected actual CharacterController routes passed**: furnished shop, kitchen, storage/garden, treatment, stairs both directions, open landing/living, bedroom foot and both bed-side aisles, study and full exterior loop. Original controller remains height 2 m / radius 0.4 m / step 0.3 m / skin 0.04 m.
- **2,028 floor samples, zero holes**, across all principal room rectangles and west landing. Standing-capsule samples distinguish furniture/wall occupancy from usable floor.
- Closed front leaf blocks entry. Open front passage and direct kitchen route pass; kitchen remains accessible with the front leaf closed. Door completed its animated 105° opening over live Play frames; original motor/input/camera were re-enabled and grounding confirmed. This original baseline checked the component directly, not the E path; see the later door-input regression report below.
- Final porch enlarged to 4.5 × 2.8 m to cover the complete reserved outward swing pocket. Additional surface checks confirmed +0.20 m across the added area; interior routes were unaffected.
- 64 unchanged-camera placement samples at 20° pitch found no obstacle between pivot and final camera position. **These do not prove subjective camera comfort.**

| Representative position | Minimum / median / maximum camera distance |
|---|---|
| Shop | 2.39 / 3.59 / 4.00 m |
| Treatment | 1.35 / 2.05 / 4.00 m |
| Kitchen | 1.35 / 2.35 / 4.00 m |
| Bedroom foot | 1.67 / 2.16 / 4.00 m |
| Study | 1.30 / 2.12 / 4.00 m |
| Landing | 1.33 / 3.32 / 4.00 m |
| Living | 2.09 / 3.32 / 4.00 m |
| Stair turn | 0.56 / 0.96 / 4.00 m |

- Runtime / compilation Console: **0 current errors, 0 current warnings** after testing; older Pipeline/log history was not cleared or counted as new gameplay errors. No missing script components.
- Exit Play restores enabled controller/motor/input/camera and closed door. New scene saved and left open in Edit mode. Production01, shared traversal code, input asset, existing prefabs and project settings remain unchanged. Unity synchronized a legacy roof material texture alias while the old scene was loaded; that incidental change was restored, leaving no existing tracked-file changes. Nothing committed.

## Remaining usability concerns before production reconstruction

1. **Manual camera review is required**, especially the U-stair turn: some yaws shorten to 0.56 m (median 0.96 m there). A useful longer view exists down the flight, but free orbit at that turn is not established as comfortable. Do not treat this blockout as automatic approval to rebuild finished art.
2. Bedroom side aisles are 1.0 m, sufficient for the unchanged capsule and tested with the full bed footprint, but these are secondary access aisles rather than 2.2 m principal routes. Judge bed interaction/camera framing manually.
3. Internal doors and garden door are represented by clear openings only; future leaves need their own swing checks. The prototype front door is deliberately simple and is not a production interaction system.
4. Roofs are massing guides with intentionally unresolved visual intersections. Finished kit fitting, windows, exterior treatment, lighting polish and exact approved-facade reconciliation are deferred until the playable layout is accepted.

Previews: `Previews/ExteriorMassing.png`, `ShopCamera.png`, `BedroomCamera.png`, `StairTurnCamera.png`. Interior captures use the unchanged runtime camera placement; no gizmos, blur or art integration. Validation snippets are under `ArtSource/Pipeline/Review/*CrookedMortarUsabilityBlockout01.cs`; they guard the scene path and route tests require Play mode.

## Architectural integration requirement — not an approved exterior

This is a **temporary functional layout blockout**, not an approved exterior design. Its generic house appearance and large left-side roof overhang are unacceptable for the future production building. Do not carry these guide roofs or generic exterior proportions into finished assembly. Preserve the approved `CM_CrookedMortar_B_StyledDetails07` visual direction: layered roof hierarchy, asymmetrical gables, tucked/interlocking masses and distinctive sheltered entrance composition. Reconcile the expanded usable rooms with that benchmark during future architectural integration. No decoration or architectural remodeling is part of the door fix.

## Front-door interaction correction

The original fixture polled the E key directly and silently rejected `SetOpen` inside a broad 2.45 m radius in front of the hinge. This rejected ordinary front-door approaches, even though the earlier component-only checks passed from a preselected safe position. It also provided no indication that safety rejection, rather than missing input, was preventing movement.

The corrected scene-local fixture copies the existing `Player/Interact` bindings (E / gamepad north) into a private **Press** action. The shared action has a **Hold** interaction; its settings and all shared gameplay code remain unchanged. The scene now explicitly references the existing input asset. Actual sampled leaf-vs-CharacterController sweep checks pause animation before contact, display a step-clear message, and resume the pending motion when clear. Range remains 3.2 m horizontally around the hinge, restricted to the same floor. Only the front-door hinge moved 0.16 m outward (Z −0.10 → −0.26 m), mounting the leaf outside the wall face and clearing the left jamb across its full swing. Leaf dimensions and collider shape, all architectural/furniture colliders, rooms, roofs and decoration remain unchanged.

The door-input regression uses a temporary Input System keyboard, queues E press/release events through the actual binding and lets normal Play-mode updates animate the door. It does not invoke door methods or force action callbacks. Unity Game view must be focused; unfocused synthetic-input trials are not valid gameplay-input evidence. Temporary test devices and background-run state are restored. See `DoorInteractionValidation.json` for the resulting checks.

Final door regression: **14/14 interaction/safety checks and 9/9 passage checks passed**, using six E-key press/release events through the actual Input System bindings. The front approach opened on E; actual player obstruction paused at about 23.5° opening / 64.2° closing, then resumed when clear. The full 105° swing cleared wall/frame colliders at 43 sampled angles. No new Console errors or warnings during the final run. Normal controller, input and camera remained enabled; no shared gameplay changes. This is automated input-path verification, not a claim of physical keyboard manual playtesting.

Door-fix file scope:
- `Assets/BlightBloom/Prototypes/CrookedMortarUsability01/BlockoutDoor.cs` — local input and sweep behavior.
- `Assets/Scenes/CM_CrookedMortar_UsabilityBlockout01.unity` — only input-asset reference and hinge Z changed.
- `ArtSource/Pipeline/Review/CreateCrookedMortarUsabilityBlockout01.cs` — keep the existing generator consistent with the corrected fixture.
- `ArtSource/Pipeline/Review/TestCrookedMortarBlockoutDoorInput.cs` — focused live-input regression.
- This README and `DoorInteractionValidation.json` — scope, architecture requirements and results.

Production01 and StyledDetails07 scene hashes, all three shared traversal-script hashes and the input-action asset hash match their pre-fix values. No tracked existing assets/settings changed; nothing committed.
