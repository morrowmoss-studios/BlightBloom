# Briarwick Miller’s Cottage01 — rough architectural review

2026-11-02. Saved in the EXISTING `Assets/Scenes/Briarwick_Hamlet_Dev01.unity`, replacing location08 visually. `08 Millers cottage PLACEHOLDER` remains disabled, not deleted. Original transform preserved: (38,5.356443,-47), yaw5°, unit scale. Candidate selected in Edit mode for visual approval.

## Architectural draft

Narrow front-gabled family home, unequal roof slopes and offset ridge, small irregularly placed windows, static main/service doors, integrated hearth chimney and low side grain/tool store. Muted plaster, pale weathered timber, local stone footings and restrained continuous thatch. No decorative timber triangles, goods clutter, milling machinery, NPC or playable interior. Distinct from the wider side-gabled farmhouse and more complex package cottage.

- Main house **6.6 × 7.8 m**, attached store **1.4 × 3.8 m**: total ground area **56.8 m²** (overall body envelope8 ×7.8m, irregular footprint).
- Main roof envelope about **7.44 ×8.5m**; side-store eave extends to localx4.98m. Roof ridge about **5.72 m**, maximum chimney **5.965 m above placement datum**.
- Planned floor +0.12m. Main clear doorway **1.4 ×2.4m**, rear **1.3 ×2.3m**, static closed leaves. No claim of walking through closed doors or of an interior.
- **19,052 triangles**, **10 renderers**, **9 shared materials**. Static mesh colliders; no LODs yet.

## Creek and placement

Foundation vertex samples measure **7.54m minimum horizontal distance to the current creek-water boundary**, with the lowest foundation vertex **1.33m above nearby water**. Terrain under main/store corners varies only centimetres about the original pad. The cottage does not intersect the creek, and both approach and perimeter remain on the existing bank. Existing terrain, creek, bridge, paths and roads untouched.

The unbuilt land toward the creek remains available for later geographic/mill planning. A marker identifies a planning direction only; no hydrology, wheel or working mill fit is claimed, and any mill would need separate siting review. Current water/terrain are blockout geometry, not a flood-risk study.

## Materials and source

Reusable `Assets/BlightBloom/Art/Architecture/Briarwick/MillerCottage01/Prefabs/BW_MillerCottage01.prefab`; ten grouped FBX exports and project-owned derivatives. Editable `ArtSource/Blender/Architecture/Briarwick/MillerCottage01/BW_MillerCottage01.blend`, packed source base-color images.

Reuses original cottage/package weathered timber, stone, door, hardware, firewood and glass maps, Bakery02 plaster and StableA03 thatch maps. Reduced normal strength on only the new thatch derivative. Original package and approved assets unchanged. Exact transitive Unity dependencies in `FinalValidation.json`.

## Targeted validation

- **16/16 grounded Play-mode CharacterController.Move checks passed**: three lateral lanes at each entrance, road connection, complete house/store perimeter; all forward/reverse. Existing controller2m high/.4m radius; motor/orbit temporarily paused and restored; player position/rotation restored. Automated collision smoke checks, not manual input/camera-comfort approval.
- Geometric doorway dimensions measured with static door leaves excluded.
- All ten meshes have finite UVs, valid normals and zero degenerate triangles. Supported shaders and no missing texture references.
- **25/25 main roof coverage rays** hit with correct upward normals. Visually checked main/store roof contact and chimney emergence, side/rear foundations and doorway joins.
- Initial flush timber tie/sill surfaces produced coplanar flicker against plaster. Increased only those six new timber islands’ depth; final views inspected. No new ornament added.
- **416 existing scene objects’ component snapshots unchanged**, outside the new root; original placeholder intentionally disabled. **2,701 file hashes checked**, only authorized Briarwick scene changed. Approved buildings, gameplay, source/package assets and village landscape untouched.
- Final Unity Console **0 errors/0 warnings**, compilation not failed; no new captured warning/error entries beyond historical cursor44. No Console clearing. Existing scene saved, Edit mode.

## Outstanding rough-build limitations

Roof remains a simple continuous thatch coat rather than final dressed bundles; end-grain eaves and store boards show repetition at close range. Plaster is plain and windows dark. Store is a sealed exterior storage volume, not an accessible room. Fine window detailing, thatch ridge treatment, local chimney flashing and collider/LOD optimization await approval for a later pass. No final art approval claimed.

## Review files

Front, three-quarter, side, rear, creek-side and village-context PNGs named `MillerCottage01_*.png`; clean camera renders under existing scene lighting with no editing gizmos. Camera restored after capture. Validation JSON and helper snippets are in this review folder. Exact task file inventory: `ChangedFiles.json`.

No new Unity scene, shared gameplay changes, commit or push. Stop for visual review before building anything else.
