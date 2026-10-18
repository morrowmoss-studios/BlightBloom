# The Crooked Mortar — Production02 architectural candidate

**Current staircase revision:** [StairUsability02](StairUsability02/README.md) replaces the earlier solid guards and adds a Production02-only camera profile. Earlier camera/collider counts below describe the reconstruction before this revision.

Open `Assets/Scenes/CM_CrookedMortar_Production02.unity` alone. The original Production01, approved usability blockout, StyledDetails07 benchmark, shared gameplay/input code, original kits and project settings are unchanged. Nothing committed.

## Architecture and functional plan

The functional envelope remains **11.4 × 9.4 m**, excluding the porch. Room dimensions, floor datums (+0.20 / +3.60 m), 3.10 m ceiling clearance, 1.5 m U-stair flights, 2.4 m open landing reserve, furniture footprints and direct shop→kitchen connection are retained. The front leaf still swings outward and uses the manually approved E interaction. The rear garden opening remains accessible. See the unchanged [dimensioned functional plan](../UsabilityBlockout01/FloorPlan.svg).

| Space | Clear dimensions |
|---|---|
| Shop / upstairs living | 5.4 × 4.4 m each, living opens onto west landing return |
| Treatment / bedroom | 3.6 × 4.4 m each |
| Kitchen/preparation / study | 3.4 × 4.2 m each |
| Storage/garden vestibule | 3.4 × 2.4 m |
| Stair bay | 3.2 × 4.2 m, eighteen 188.9 mm risers / 300 mm goings |

This is a reconstruction around the plan, not a material overlay on the rejected guide house. The visible box shell and guide roofs are replaced. The collision volumes remain authoritative and separate; 89 obsolete disabled render/mesh components were removed from those collision objects.

The newly authored roof relationships follow StyledDetails07: an off-centre steep curved hero gable (peak 11.45 m), a lower rear cross-roof, recessed cross-roofed study wing, a small pitched stair-nook cap, lower garden-store roof, and two depth/height-offset canopy folds. The former large flat left overhang is absent. The side/rear accommodation carries the expanded floor area without uniformly enlarging the old building model. Actual roof surfaces are trimmed to the visible upper envelope; fitted ridge, valley and eave/verge networks share those boundaries. No original roof-kit surfaces were stretched or regenerated.

## Reuse and fitted adapters

- **EntryPortal02:** unchanged unit-scale portal, seated beneath the entry canopy; original sign and lantern artwork reused with supports meeting the structure. Herb bundles attach to a timber rail, outside the door swing.
- **FacadeBay01:** shared posts, beams and a correctly seated storage-wing brace. Only linear timber spans are fitted; complete textured wall bays are not non-uniformly stretched. New Blender shell adapters provide real openings and returns at the approved room dimensions.
- **SlateRoofKit01:** existing painted slate/walnut materials, course proportions, restrained irregularity, exact clipping and intersection-finishing construction helpers. New site-specific FBX adapters accommodate the different expanded roof carriers.
- **PairedWindowBay02 / WindowBay01:** original unit-scale inserts and independent shutters/sills/boxes. Rear paired casements and the narrow west return intentionally omit open shutters to avoid corner/post conflicts. Front composition retains the approved paired look and sage shutters.
- **BotanicalPlanterKit01:** interchangeable flower-box inserts, potted herbs, drying bundles, attached ivy and small garden planting clusters, with no cosmetic colliders.
- **EntranceBay01:** approved door and stone artwork transferred to new fitted visual adapters matching the existing 1.96 × 2.70 × 0.10 m moving collision leaf. Stone surround is seated to the floor and stays behind the outboard hinge plane. A fitted timber stop and silhouette-derived arched rebate close the main reveal gap; the approximately 1.81 m finished visual opening stays within the 1.8–2.0 m circulation target. Neither original mesh nor material is modified.
- One new shared **CM02_MatteAmberGlazing** material derives from the existing warm-window treatment, with the incompatible old atlas removed. Existing paired-pane triangles get a separate glass slot; single arched inserts get fitted closed panes. The initial opaque amber treatment was replaced in the finishing pass with restrained tinted translucent glazing, preserving the existing frame and shutter designs. The material retains its original asset name to preserve references.

Editable source: `CM_CrookedMortar_Production02.blend` and `build_production02.py`. Roof helpers are read from the existing roof-kit source; only new output paths are written. The focused `repair_authored_uv0.py` and `fit_arched_apertures.py` document corrections applied to the new structural source; approved kits and the new roof FBX were not regenerated during these fixes. Native Unity glazing/door/stone adapters are reproducible from the Editor snippets, and retain the original kit UV artwork.

Unity assets: `Assets/BlightBloom/Art/Architecture/CrookedMortar/Production02/` (FBXs, fitted mesh adapters, shared glazing material and assembly prefabs). Scene-only collision/input/player setup is copied from the approved layout. The unchanged `Assets/BlightBloom/Prototypes/CrookedMortarUsability01/BlockoutDoor.cs` is still a dependency; do not remove that source when eventually archiving the blockout scene.

## Validation

- **56/56 connected actual CharacterController routes passed:** every principal room, furnished treatment/kitchen, bed foot and both side aisles, stairs both directions, landing, study, garden return and full exterior perimeter.
- **2,028 floor and 2,028 ceiling mesh samples passed**, independently testing the new visible FBX in a temporary isolated physics scene. No sampled visual floor/ceiling holes; inherited collision coverage also passed.
- **4,732 roof surface samples passed** against the authored carrier upper envelope. Blender solids checked manifold edges, signed volume and degenerate triangles; Unity UV/normal arrays are finite and valid. These tests do not claim exhaustive all-pairs mesh intersection proof.
- Four arched aperture meshes were checked from both sides after correcting cutter normals. Original paired rough openings remain fitted to the approved inserts. New glaze uses existing pane triangles rather than overlapping a second plane on the pair.
- **14/14 door-input checks and 9/9 doorway/kitchen route checks passed**, using six E press/release events through the actual Input System bindings and live updates, not direct door animation calls. Outward sweep cleared the wall frame at 43 angles; opening and closing pause safely around the player and resume when clear.
- **90/90 static structural collider transforms/bounds match** the layout baseline; plus the unchanged CharacterController. Collision grouping and removal of disabled renderers did not alter collision behavior. Cosmetic installations add zero colliders.
- **64 camera samples** use the unchanged obstruction method and settings. Representative median distances: shop 3.59 m, bedroom foot 2.16 m, kitchen 2.35 m, landing 3.32 m. No sampled obstruction between pivot and final camera point.
- Final compilation / Console check: **0 current errors, 0 current warnings** during the successful runs. Historical Pipeline entries were not cleared or reported as new runtime faults. No missing script components.

Reports: `TraversalValidation.json`, `IntegrationGeometryValidation.json`, `DoorInteractionValidation.json`, `WindowApertureValidation.json`, `FinalCollisionPreservation.json`. The established traversal and E-input utilities were reused by substituting only the target scene/report paths; shared test utilities and gameplay code were not edited. Geometry probes use original imported model meshes, because runtime static batching replaces renderer MeshFilters with combined buffers.

## Remaining limits and review decisions

1. **Manual camera comfort remains necessary**, especially the U-stair turn: some yaws contract to 0.56 m (median 0.96 m there). The inherited behavior is unchanged; automatic reachability is not a comfort verdict.
2. Interior furnishings retain full-size functional footprint geometry with appropriate materials. They are placeholders for production beds, examination furniture, cabinets and workbench assets, not finished interior art.
3. The larger study wing needs the full 3.10 m headroom. Its eave therefore sits at the main storey datum; a lower peak, cross orientation and 2 m frontage setback keep it subordinate. This is an intentional usability compromise to review against the old benchmark.
4. The expanded main roof and gable are newly fitted designs based on the benchmark's relationships, not an exact reproduction of old dimensions. Final silhouette/art acceptance is yours. Fine trim, chimney/hearth integration and broader garden/path dressing are not complete. The closed-door light line was corrected in the finishing pass; see `Finishing/README.md`.
5. Roughly **293k visible-library triangles / 423 enabled renderers before LOD culling and batching**, including all reused modular components. Static model surfaces batch; this landmark candidate still needs profiling, additional kit LODs and consolidation before village-wide repetition. No frame-rate benchmark was performed.
6. Rear/internal doors remain clear openings. The front interaction is the existing scene-local fixture, not a new shared interaction framework. No unrelated gameplay systems were implemented.

## Previews and manual review

`Previews/Front.png`, `Side.png`, `ElevatedThreeQuarter.png`, `GameplayDistance.png`, `Shop.png`, `Kitchen.png`, `Bedroom.png`, `Staircase.png`, and `ActualGameViewExterior.png`. Exterior architecture previews hide only the player visual temporarily; saved scene visibility is restored. The runtime-camera capture uses the existing 4 m distance / 65° FOV at a valid look-up orbit; it is not manual playtest evidence. No bloom, blur, fog or colour-grading substitute was added.

Press Play, click Game view, use WASD / Shift / mouse as before. Press E within range of the front door; step clear if its outward swing is blocked. Check the furnished room routes and stair camera manually before approving further art integration.

New project work is confined to Production02 assets/scene, this source/report directory and the corresponding `ArtSource/Pipeline/Review/*CrookedMortarProduction02*.cs` snippets. Earlier scenes/assets, gameplay source, packages and settings are preserved; nothing committed.

Final local door regression was repeated after the reveal work: all 14 input/safety and 9 route checks passed. The candidate is saved in Edit mode with all shared controller/input/camera components enabled. Final file inventory is `CreatedFiles.json`; original-scene/script hashes are in `PreservationValidation.json`.


Architectural finishing (2026-10-17): see [focused changes and current validation](Finishing/README.md). Original reconstruction reports above are historical context; the finishing reports describe the current saved candidate.
