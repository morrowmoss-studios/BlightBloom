## Architectural proxy pass — applied

The existing saved scene now includes a pitched roof, framed open windows, plaster and timber exterior, stone plinth/chimney, storage hearth, ceiling beams, stair joinery, room-colour floor finishes, and furniture proxy details. All initial room, stair, floor and player transforms were retained. The original exterior wall panels are disabled in place; matching segmented panels provide the window apertures. Original furniture collision envelopes remain, while decorative joinery and floor finishes have disabled colliders. The roof, new wall panels, foundation and fireplace use solid colliders.

`Tools/ApothecaryArchitecturalPass.cs` is the Editor-only authoring source, compiled on demand through Unity Pipeline run_script. It refuses duplicate application. Edit `08 Architectural proxy pass` and the individual shared URP materials in `ProxyMaterials` to iterate. The initial generator below still describes the original greybox and should not be rerun on the saved proxy scene.

Validation: all 134 original transforms preserved; 13 doorway/landing capsule-clearance checks passed. In Play mode the existing CharacterController completed a 26-waypoint collision route including ascending/descending stairs, private rooms, downstairs workspaces and the garden exit. Movement was driven through CharacterController.Move for this physics test, not through simulated keyboard input. No new runtime or compilation errors were observed. Manual camera comfort remains to be evaluated.

# Uncle Robert’s Apothecary — greybox

## Generate the scene

Unity is open but automation is not reachable. The scene must be serialized by the Editor; no handwritten scene YAML is supplied.

1. Open the existing project `/Users/zak/Desktop/MorrowMoss Studios/BlightBloom` in Unity 6000.4.5f1 and wait for script compilation.
2. Outside Play mode choose **BlightBloom > Create Uncle Robert’s Apothecary** (menu label uses a straight apostrophe).
3. Open `Assets/Scenes/UncleRobertsApothecary.unity` alone, then press Play and click the Game view.
4. WASD moves, Left Shift sprints, mouse orbits; Escape releases the cursor and click recaptures it.

The generator creates a separate scene using Unity APIs, restores the previous active scene, and never saves or overwrites SampleScene or TraversalSandbox. It refuses to replace an existing apothecary. It can also be called from a closed-project batch Editor via `-executeMethod BlightBloom.Locations.Editor.ApothecaryBlockoutBuilder.Create` with the actual project path. Do not start a second Editor on an already open project.

## Layout

The 16m x 14m footprint faces south (-Z); the garden lies north (+Z). Floors are 3.6m apart with wide 2.2–2.4m thresholds and 2.8m door clearance. The generous dimensions deliberately prioritize third-person traversal over historical proportions.

Ground floor: front shop and counter lead to examination/treatment at the west and medicine preparation at the east. Both connect to rear storage and a clear garden exit. The eastern stair is reached from the front entry without walking through the treatment room. Furniture is kept away from doorways.

Upper floor: stairs arrive at a rear landing, opening into an eastern living/passage space. Bedroom is southwest and library/study northwest, with separate doors and a connecting threshold. The stairwell has a real floor opening and upper guards; 18 steps rise 0.2m per 0.5m tread, below the existing CharacterController’s 0.3m step offset. Its 2.8m usable width and broad landing accommodate camera orbit.

Exterior: open walking space surrounds the house; a path connects the rear door to four primitive herb beds and a low boundary with an opening. Roof is intentionally omitted for cutaway inspection and iteration. Upper exterior openings have waist-high sills; these are window blockouts, not exits. No operable doors, textures, polished medieval details, interactions, or medical mechanics are included.

## Iteration

Named hierarchy groups separate exterior, modular shell, downstairs rooms, stairs, upstairs rooms, traversal/spawn, and lights. Geometry is cube primitives with BoxColliders; the temporary capsule uses the existing TraversalInput, ThirdPersonMotor, and ThirdPersonOrbitCamera. No player prefab currently exists, so the builder wires those components directly and includes a named front-entry spawn marker. There is no respawn logic.

After creation edit individual geometry or parent room groups directly in the saved scene. Moving architectural groups independently requires checking doorway alignment. The Editor builder is the reproducible source for an initial blockout; it never automatically rebuilds or overwrites hand edits.

The shared orbit camera has optional obstacle shortening, enabled here with a 3m distance. TraversalSandbox retains its prior behavior because the option defaults off. This is a prototype sphere-cast camera: tight corners or a target already overlapping geometry can still produce occlusion. There is no roof or camera fading system.

## Test route

- Walk from front spawn into the shop, around both sides of the counter, into treatment, through to preparation and storage, and out the rear door.
- Circle the four herb beds and walk around both sides of the exterior to the front.
- Ascend and descend all stairs at walk and sprint speed. Verify no head collision at the floor opening, no stuck steps, and guard blocking from the upper rooms.
- Visit bedroom, connecting study door, study desk, and living space. Orbit near walls, ceilings, doors, and stair corners; report clipping or uncomfortable camera compression.
- Check Console errors and confirm existing scenes remain unchanged. The surrounding site is finite and has no fall recovery.

## Validation

C# compilation is checked with Unity’s bundled compiler and cached project references. Live scene generation, visual inspection, physics clearances, lighting, and Play mode require the Editor steps above. No packages or build settings are changed.
