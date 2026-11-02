# Stable A03 thatch painting

Project-owned straw finish for the A03 review candidate. The initial painting was made with built-in imagegen, using the exact request in `GenerationPrompt.txt`; no paid external service or software was installed.

- `Thatch_PaintedSource01.png`: preserved generated painting.
- `Thatch_Painting01.ora`: editable layered original + soft finish, readable by OpenRaster painting applications.
- `prepare_material.py`: reproducible subdued color/contrast and map preparation. Does not overwrite generated painting.
- `MaterialPreparation.json`: map preparation details.
- Unity outputs: `Assets/BlightBloom/Art/Architecture/Briarwick/StableA03Rural/Textures/`.

BaseColor uses sRGB; normal is imported as NormalMap, packed metallic/smoothness is linear. Nonmetallic, low smoothness, no emission. All are 2048 px with mipmaps. There are no alpha straw cards. Directional fibers are placed from ridge toward eave through explicit UVs. Remaining limitation: close-up strand distribution is more evenly combed than final hand-laid thatch; the ORA supports a later approved paint adjustment.
