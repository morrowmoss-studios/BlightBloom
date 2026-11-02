# Bakery01 material sources

`ClayTile_Painting01.svg` is an editable eight-swatch clay painting master. `paint_clay.py` reproduces its restrained broad kiln streaks, raster swatches and opaque URP metallic/smoothness map. The modeled channels and overlapping covers carry the clay-tile construction; no photographic noise or glossy glaze was introduced.

`prepare_plaster.py` extracts the exact unframed source region recorded in `PlasterRegion.json` from the installed package's concrete/plaster painting and corresponding normal/roughness maps. Original source images remain unchanged. Its old baked timber AO is not transferable to this new geometry and is not reused. `Plaster_CleanRegion01.png` preserves the cropped color source.

Unity outputs live at `Assets/BlightBloom/Art/Architecture/Briarwick/Bakery01/Textures/`. Color maps sRGB; normal imported as NormalMap; roughness/metallic maps linear. Native Autodesk Interactive material consumes the roughness map directly; URP Lit clay consumes packed smoothness in alpha (not roughness).
