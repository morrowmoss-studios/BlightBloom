# Apothecary exterior — storybook style test

First in-engine direction test based on the written art brief; the actual concept image was not available during this pass.

Palette: warm ivory plaster, dark walnut framing, grey/moss limestone, charcoal/moss slate, sage shutters, aged copper, amber lanterns, restrained lavender/gold flowers. All surface materials use existing URP Lit with metallic and smoothness at zero and specular/environment highlights disabled. The 256px painted-looking base maps use procedural broad pigment variation, grain and brush marks; these are visual approximations, not artist-painted production textures. Stonework and wood UVs remain proxy UVs.

Architecture: overlapping scalloped roof tiles, smooth gable faces, lightly bevelled timber render meshes, pointed window hoods, shutters, eave brackets, small steep entrance canopy, lanterns, mortar-and-pestle signage, two herb boxes and restrained ivy. The main roof envelope, existing window apertures, doorways, floor plan and collision geometry are retained. All new art lives under `09 Storybook exterior style test`. New art is deliberately non-colliding. Original collider states were compared before and after initial application; no changes were detected.

Lighting: scene-specific warm directional sunlight with reduced shadow strength, cool fill, soft tri-colour ambient and a restrained procedural sky. No URP pipeline, quality, input or package settings were changed. The thin tile overlay does not cast or receive shadows, avoiding thin-mesh self-shadow artefacts; the existing solid roof remains the shadow and collision proxy. No post-processing package or custom rendering pipeline is required.

Validation: 13 doorway/landing capsule probes remain clear; no missing scripts/shaders. Player, motor, input and camera initialized in Play mode with a grounded spawn and no new Console errors. SampleScene, TraversalSandbox and traversal source hashes are unchanged. The Editor is left out of Play mode.

Authoring source: `Tools/ApothecaryStorybookPass.cs`, compiled on demand through Unity Pipeline run_script. Apply refuses duplicate application. Do not regenerate the initial greybox over this saved scene. Iterate directly on the scene groups and shared materials; Polish updates only this pass's thin mesh normals and gable shading, and HandHewnTimber assigns the render-only timber mesh.

Next dedicated art needs: authored painted atlases and UVs; more organic/asymmetric structural meshes; a bespoke apothecary sign, lanterns and shutters; curved roof silhouettes matched to the forthcoming concept image; proper botanical leaf cards and flower meshes. The garden, surrounding ground, interior furnishings and village remain unfinished proxies. Warm light affects the existing interior too through scene ambient; its point lights were preserved.
