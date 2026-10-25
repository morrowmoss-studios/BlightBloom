# Built-in imagegen prompt record

All images were generated with the built-in imagegen tool, no paid external service or CLI/API fallback. Original outputs are preserved in this source directory.

1. `CounterRelief_Source.png` — request a wide 3:1 grayscale scalar depth field with three carving fields: asymmetric sage and roots; mortar/pestle with laurel and scroll; different medicinal flowers and roots. No perspective/shadow/noise. **Rejected as a depth source** because the model returned a directionally shaded relief image.
2. `CounterStencil.png` — edit the first result: preserve triptych motifs and layout; convert to pure white filled silhouettes on pure black, black vein cuts, no grayscale/light/shadows. Used only as a sculpt stencil, not as albedo or a claimed measured depth map.
3. `CounterPaint_RejectedBusy.png` — use stencil as registration source and supplied Crooked Mortar interior image as art reference. Paint same-wood walnut carvings and recesses, broad gouache strokes, no text/frame/perspective, quiet sage/ochre hints, no cast shadows. **Rejected as final colour** for excessive grain and contrast.
4. `CounterPaint.png` — targeted correction: preserve canvas/motif positions; remove 90% of micrograin, replace with calm broad walnut brush groups; halve motif/background contrast; remove black shadows and bright metal/applique appearance; no blur filter. Used as the candidate's registered colour source. Some illustrative shading remains and is documented as a limitation.
5. `WalnutPaint.png` — square edge-to-edge wood albedo, warm medium-dark walnut, broad lengthwise brush strokes and gentle curving ribbons, low microdetail; no seams, knots, carvings, shadows, gloss, text or photographic noise. Used on shaped structural members at consistent physical UV scale.

The original user reference is `/Users/zak/Downloads/The Crooked Mortar Apothecary-2.png`; it is an artistic reference, not a texture pasted onto the model. No generated beauty image is presented as a Unity result.
