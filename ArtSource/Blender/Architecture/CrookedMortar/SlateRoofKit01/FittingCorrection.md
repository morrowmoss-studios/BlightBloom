# CM_SlateRoofKit01 — fitting correction

Review in `Assets/Scenes/CM_SlateRoofKit01_IntegrationPreview.unity`. Its scene file is unchanged; corrected FBX and roof-prefab dependencies update the existing installation. The approved StyledDetails07 scene and all unrelated scenes are unchanged.

## Faults and corrections

- **Hero shoulder / changes in main roof pitch:** each triangle previously restarted its slate grid and pitch strips exaggerated the bend. Shared cumulative-slope coordinates now continue rows across carrier triangles. Superseded Fitted_PitchTransitionNetwork is disabled in the assembly prefab (original asset retained). Original measured control points, heights and intentionally bent profile are retained.
- **Dormer-to-hero valleys and hero/rear cross junction:** adapter widths previously sampled the global highest surface, sometimes switching to a distant lower roof and creating long triangular ribbons. Ridge and valley cross sections now use only the incident local roof planes and narrower fitted widths.
- **Rear cross / subordinate wing:** the same height-sampling fault produced overlong adapter fins. Local-plane adapters remove these; internal clipped roof edges no longer generate exposed timber fascia.
- **Deep entry / left shop canopy step:** a real small height difference was being treated as an exposed timber edge. A fitted vertical slate step apron now finishes the measured discontinuity. Canopy dimensions are unchanged.
- **Display catslide and eaves:** consistent slope coordinates align courses; only true external edges retain fascia. Existing full front gable verge is retained.
- **Slate colour patches:** removed periodic UV jumps into the strongly olive part of the approved paint sheet. Shared matte materials and original paint image are retained, with restrained blue-grey sampling instead. No new procedural texture or colour grading.

## Validation

All six measured roof sections inspected in Unity renders, including above-roof, under-eave and gameplay-distance views. 29 active library modules / 47 mesh parts / 37,488 total library triangles. Blender: zero non-manifold edges, degenerate geometry triangles or zero-area UV triangles; UV0 remains within 0–1 with intentional painted trim-sheet reuse. Fitted carrier coverage: 1,431 samples, no misses, maximum height error about 0.0000015 m. Unity import bounds discrepancy below 0.000002 m; unit scale, orientation, materials and UV/normal arrays validated. Original 37 colliders and all 53 tracked collider/behaviour/light components unchanged. Brief Play-mode smoke test: no new errors, compilation successful. This is not an exhaustive player traversal test or a mathematical all-pairs intersection proof; designed slate-course overlap remains intentional.

## Files

Updated editable blend, build script, 29 FBX exports, EaveVergeNetwork prefab material assignments and ApprovedRoofAssembly prefab activation. Original versions preserved in Archive/BeforeFittingCorrection. Old pitch-transition FBX/prefab retained but not active in fitted assembly. Reports are alongside this file. New capture helper: ArtSource/Pipeline/Review/CaptureRoofFittingCorrection.cs. No gameplay scripts, project settings, existing colliders or texture images changed. No commit created.

## Screenshots

Before and After folders under Previews/FittingCorrection contain HeroShoulder, DormerValleys, HeroRearJunction, RearWingStep, EntryCanopyJunction, DisplayCatslide, BelowEaves, Elevated and GameplayDistance PNGs. The roof remains a fitted modular prototype; subtle measured pitch breaks remain rather than changing the approved silhouette.
