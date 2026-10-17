# The Crooked Mortar — presentation details 07

New scene: Assets/Scenes/CM_CrookedMortar_B_StyledDetails07.unity. Non-destructive duplicate of CM_CrookedMortar_B_StyledProof06.unity, still based solely on B – Moderate refinement. All prior scenes and source assets remain unchanged.

## Presentation changes

The entrance is now the focus of the dressing: a shallow walnut portal and inner trim, carved post caps/shoes, the reused botanical mortar sign mounted over the entry on a swan-neck bracket, and two curled lantern brackets with warm local lights. The former side-mounted sign is hidden only in this duplicate, avoiding competing signage. The doorway, canopy, stoop and collision-bearing walls were not moved or rebuilt.

Flower boxes are fuller, with overlapping herb/flower clumps and selected ivy cascades. Additional drying bundles have visible ties/hooks. Handmade terracotta and sage planters frame the approach asymmetrically. A small crate stack, herb-sorting stool and basket-like hamper suggest the shop's daily use. A thin sage runner accents the stoop, and low sage/walnut garden rails plus a few restrained path-edge plants finish the immediate setting. The central entrance route remains visually clear.

Reused: the existing painted B architecture and slate overlay, CM_WindowBay01/CM_EntranceBay01 parts already fitted in proof06, approved ivory/walnut/sage material language, painted botanical-card sheet, sign artwork, medicine displays, worn stone path and herb beds. New materials are matte. No new texture generation, packages, bloom, fog or blur were used in this detail pass. Pottery, crate/stool/hamper and fence are intentionally simple presentation proxies; botanical cards remain flat cutout approximations, not production foliage meshes.

## Visual assessment

The named sign, warm framed threshold, abundant but localized herbs, pottery and shop props read more clearly as a botanical apothecary than the plainer cottage-like proof. The architectural silhouette itself is intentionally unchanged: the large triangular gable and upright wing still retain some formal house-like character compared with the softer illustrated reference. This pass improves identity and hierarchy; it does not establish that every architectural proportion is final.

## Preservation and validation

No gameplay, input, motor, orbit-camera setup, room functionality or collision-bearing architecture was edited. The inherited collision/script serialized blocks and all five inherited prefab instances are byte-for-byte identical to proof06. Total colliders remain 37, with zero colliders in the new detail group. The 27-waypoint CharacterController Play-mode route passes again, including entry, stairs up/down, upper rooms/study, ground workrooms, rear garden exit and exterior return. As with proof06, decorative props/foliage have no collision; physical interaction with them is outside this mockup.

Unity reports no current compilation/Console errors, missing scripts or material errors. See PreservationValidation.json, UnityValidation.json and Traversal_B.txt. Manual camera and visual comfort review is still appropriate.

## Review and files

Open the scene and press Play for the unchanged B traversal. Presentation cameras only were reframed to better show the entry; the actual traversal camera and its settings are unchanged. Door is held open in the playable scene. Capture temporarily closes the presentation door/hides the player, then restores both before saving.

Previews/Front.png, Hero.png, GameplayDistance.png and Side.png are actual running-Editor renders. No paint-over is used.

New assets: scene and .meta; Assets/BlightBloom/Art/Architecture/CrookedMortar/StyledDetails07/Materials and Meshes (reusable planter and combined botanical-detail mesh), with their .meta files. Existing proof06 assets are referenced without edits.

External reproducible Editor eval utilities: ArtSource/Pipeline/Review/CreateStyledDetails07.cs, CaptureStyledDetails07.cs and TestStyledDetails07.cs. These stay outside Assets and are not gameplay scripts. Scene creation refuses overwrite. Notes/reports/captures live in this source folder. No Git commit was made.
