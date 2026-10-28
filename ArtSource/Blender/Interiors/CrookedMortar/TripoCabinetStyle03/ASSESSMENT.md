# Style03 visual assessment — stop for review

**The test changes the finish visibly, but neither prototype establishes the requested illustrated-fantasy quality. Do not approve either as a production material set on the basis of this experiment.**

## What is genuinely visible

- Compared with Style02, both prototypes replace the timber's burnt/highlighted photographic appearance with a new, calmer walnut diffuse treatment. Modeled crown profiles, drawer seams and carved relief remain present under real neutral lighting.
- A retains finer grain and a comparatively restrained physical surface. B uses broader/darker paint groups and a model-curvature pigment glaze; the raised carving/corner treatment is more conspicuous in B. The wood changes read in the wide views, not only in enlarged pixels.
- Sage backing is clearer. Selected bottles have a greener reflective surface, while hardware has a metallic response distinct from matte wood. These are material changes under an identical rig, not a warmer lighting setup.

## Where the test fails

- **Foliage/moss segmentation is not reliable.** The planter/foliage close-up exposes green pigment patches on timber, brown patches on leaves and incomplete treatment of fused moss. The result reads as a patchy material assignment, not naturally layered botanical painting.
- **Container masks are incomplete.** Bottle shoulders/bodies, old labels, necks, neighbouring pottery and retained printed highlights do not all agree. Some glass remains a glazed/opaque approximation and some old bright streaks survive. It cannot be described as comprehensively reconstructed glass.
- **Original artistic richness is partly lost.** Removing the old painted wear/highlights reveals that some fine carved/aged character existed in the source color image. Geometry is preserved, but a quieter diffuse layer does not automatically replace that authored richness. Some new timber and plants read smoother and more generically CG than the target.
- **Stock remains stylistically mixed.** Protected books, labels, ceramics and the botanical picture retain original baked lighting/detail alongside newly reconstructed wood. This is not yet one cohesive finish across the cabinet.
- A/B separation is strongest in wood pigment and relief treatment; it is less decisive in some protected shelf contents. A measurable pixel difference alone does not establish a better illustration style.

## Actual blocker and next prerequisite

The obstacle is **not simply roughness or lighting**, and it is not proof that the geometry can never be repainted. The automatic hue/spatial masking used here cannot reliably replace a deliberately authored semantic material separation on this fused asset. The inherited collapsed/shared UV coverage makes a straightforward full-atlas rebake unsafe; a color grade or more guesses at thresholds would repeat the earlier failure.

A convincing continuation needs hand-checked material IDs/masks for wood, leaves, moss, rope, brass, glass, labels, books and pottery, followed by controlled secondary UV/texture-transfer work and region-by-region albedo repainting to replace the discarded baked illumination. Hollow/transmissive bottle reconstruction would be a separate geometry decision and was not attempted. Existing geometry, UVs and originals should remain recoverable throughout that work.

**No further material edits or destructive reconstruction were made after identifying these limitations.** The two prototypes and all five four-way comparisons are retained as diagnostic evidence for artistic selection or rejection. No Unity integration occurred.

## Review order

1. `Comparisons/Gameplay_FourWay.png`: can the style difference be read at ordinary viewing distance?
2. `Comparisons/ThreeQuarter_FourWay.png`: overall coherence and wood/stock balance.
3. `Comparisons/FoliagePlanter_FourWay.png`: the strongest evidence of failed semantic masks.
4. `Comparisons/CrownWood_FourWay.png` and `ContentsBrass_FourWay.png`: geometry retained versus lost painted richness and inconsistent container treatment.

Separate `Previews/Prototype{A,B}_*.png` files avoid judging close-ups only through small contact-sheet panels. The accessible Wicket reference guided finish evaluation, but these results do not establish fidelity to its rendered finish.
