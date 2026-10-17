# CM_SlateRoofKit01 — roof kit and non-destructive fit review

## Open the results

- Assets/Scenes/CM_SlateRoofKit01_ArtReview.unity — isolated kit, six measured roof sections, neutral structural renderer context, exact FacadeBay01 secondary-gable sample, adjacent standard panels, course/valley/pitch-break samples. No colliders or gameplay scripts copied into this scene.
- Assets/Scenes/CM_SlateRoofKit01_IntegrationPreview.unity — non-destructive copy of the approved CM_CrookedMortar_B_StyledDetails07 scene with the new slate kit fitted. This copy remains playable using its original setup.
- Previews/ArtReview and Previews/Integration contain Front, ThreeQuarter, Elevated and GameplayDistance PNGs. ArtReview also contains ModuleOverview. These are actual Unity camera renders, not generated concept images.
- CM_SlateRoofKit01.blend — editable metric Blender source, organised per-module collections, packed approved paint, mesh parts and socket empties. Reusable pieces have an authoring display layout; fitted pieces use the measured building placement.
- Unity models and prefabs: Assets/BlightBloom/Art/Architecture/CrookedMortar/SlateRoofKit01/. Thirty independent model/prefab modules plus CM_SlateRoofKit01_ApprovedRoofAssembly.prefab.

## Module inventory

| Module | Type | Description |
|---|---|---|
| CM_SlateRoofKit01_Panel2x2p4_35 | Reusable | 2m course width, 2.4m on-slope length, measured-family pitch 35 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Panel2x2p4_56p9 | Reusable | 2m course width, 2.4m on-slope length, measured-family pitch 56.9 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Panel2x2p4_71p1 | Reusable | 2m course width, 2.4m on-slope length, measured-family pitch 71.1 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Panel4x2p4_56p9 | Reusable | 4m course width, 2.4m on-slope length, measured-family pitch 56.9 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_SecondaryGablePanel2m_52p43 | Reusable | 2m course width, 2.4601829200285086m on-slope length, measured-family pitch 52.43140797117251 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Panel2x1p2_56p9 | Reusable | 2m course width, 1.2m on-slope length, measured-family pitch 56.9 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Course2m_35 | Reusable | 2m course width, 0.43m on-slope length, measured-family pitch 35 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_Course2m_56p9 | Reusable | 2m course width, 0.43m on-slope length, measured-family pitch 56.9 degrees. Bottom-left eave pivot. |
| CM_SlateRoofKit01_EaveFascia2m_35 | Reusable | Walnut fascia with seated supporting ledger. Align to panel EaveStart. |
| CM_SlateRoofKit01_EaveFascia2m_56p9 | Reusable | Walnut fascia with seated supporting ledger. Align to panel EaveStart. |
| CM_SlateRoofKit01_Ridge2m_Hero | Reusable | Low, asymmetric slate cap fitted to adjacent slope families; ridge-centre start pivot. |
| CM_SlateRoofKit01_Ridge2m_Wing | Reusable | Low, asymmetric slate cap fitted to adjacent slope families; ridge-centre start pivot. |
| CM_SlateRoofKit01_Ridge2m_Secondary | Reusable | Low, asymmetric slate cap fitted to adjacent slope families; ridge-centre start pivot. |
| CM_SlateRoofKit01_Verge2m_35 | Reusable | Walnut sloping edge and slate overcloak. Match panel outside edge, no duplicate bargeboard. |
| CM_SlateRoofKit01_Verge2m_52p43 | Reusable | Walnut sloping edge and slate overcloak. Match panel outside edge, no duplicate bargeboard. |
| CM_SlateRoofKit01_Verge2m_56p9 | Reusable | Walnut sloping edge and slate overcloak. Match panel outside edge, no duplicate bargeboard. |
| CM_SlateRoofKit01_Verge2m_71p1 | Reusable | Walnut sloping edge and slate overcloak. Match panel outside edge, no duplicate bargeboard. |
| CM_SlateRoofKit01_Valley2m_35 | Reusable | Slate-lined open valley, roof edges terminate at channel. Rotate/seat using intersection sockets. |
| CM_SlateRoofKit01_PitchBreak2m_71to57 | Reusable | Bent slate apron across 71.1 to56.9 degree shoulder. Centre crease pivot; ends are along course axis. |
| CM_SlateRoofKit01_Fitted_Hero | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_RearCross | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_SubordinateCross | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_DeepEntryFold | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_LeftShopFold | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_DisplayCatslide | FittedAdapter | Exact measured visible roof surface. Keep placement from catalog; cladding thickness only, no footprint/pitch/ridge deformation. |
| CM_SlateRoofKit01_Fitted_EaveVergeNetwork | FittedAdapter | Measured boundary fascia/barge pieces, merged in one reusable adapter mesh. Excludes the HeroB front rake supplied separately. |
| CM_SlateRoofKit01_Fitted_RidgeNetwork | FittedAdapter | Measured ridge adapters for the approved interlocking roofs. Not a generic substitute for a different intersection. |
| CM_SlateRoofKit01_Fitted_ValleyNetwork | FittedAdapter | Measured valley adapters for the approved interlocking roofs. Not a generic substitute for a different intersection. |
| CM_SlateRoofKit01_Fitted_PitchTransitionNetwork | FittedAdapter | Measured pitchtransition adapters for the approved interlocking roofs. Not a generic substitute for a different intersection. |
| CM_SlateRoofKit01_HeroB_GableVerge | FittedAdapter | Full measured front rake with one continuous walnut band and slate overcloak. FacadeBay01 HeroB profile equivalent, placed at original roof face. |

There are19 standard/reusable modules and11 named fitted adapters. Standard panels support2m/4m course widths and1.2m/2.4m on-slope lengths, measured-family slopes35/56.9/71.1 degrees, plus the exact secondary-gable panel. Courses are independent merged strips, not individual shingle GameObjects. Ridge variants fit Hero/Wing/Secondary profiles. Eaves/fascia and verges are separate. The standalone valley and bent apron provide reusable intersections; the measured networks handle the irregular site-specific junctions.

## Why fitted adapters are necessary

The approved surfaces were read from the running Editor, including original world transforms and triangulated upper surfaces. ApprovedRoofMeasurement.json records all six: Hero, RearCross, SubordinateCross, DeepEntryFold, LeftShopFold and DisplayCatslide. The hero ridge falls40cm to the rear and includes the existing unioned dormer. The cross/wing/canopy surfaces include their actual warps, offsets and nonuniform slopes. The kit does not replace these shapes with uniform planar generic roofs. Fitted skins are clipped to the visible upper envelope; hidden roof intersections and retained chimney footprints are respected.

Exact planar clipping produces trimmed slate edges at roof intersections rather than discarding complete tiles near joints. The site-specific sets contain six fitted cladding/backing sections, eave/verge perimeter, ridge network, valley network, pitch-change network and the full front HeroB gable verge. MeasuredJunctions.json records each retained crease/junction. Benign triangulation diagonals are excluded from visible transition trim. Fitted adapters should be regenerated from measured carriers if architecture changes; they are not universal drop-in shapes for an unrelated house.

## Pivots, dimensions and connections

Metric source; Unity +Y up. Root transforms are zero/identity/unit. Panel +X follows the course/eave and +Z travels upslope; the pivot is the lower-left eave point. On-slope length is distinct from horizontal run: run=L*cos(pitch), rise=L*sin(pitch). Connections mark eave ends and upslope ends; course strips also expose a NextCourse socket at .30m on-slope advance. Caps/fascia start at an edge datum and extend along +X. Verge pieces extend upslope along +Z. Names ending2m normally mean a2m span; **Verge2m_52p43 is the full2.4602m secondary-gable slope**, retained under that family naming prefix. Use its actual endpoint socket, not the filename as a measurement.

The complete site fit uses catalog placement positions for the six roof skins and a world datum for multi-roof trim networks. Do not reset those child positions inside ApprovedRoofAssembly. Fitted parts remain independently editable/reusable. SourceDimensions.json records canonical model bounds and UnityValidation.json compares each imported module against them. Source display-layout translations are excluded from export. FBX uses the previously verified export-only Z conversion and -Z forward/Y-up settings.

FacadeBay01 compatibility: the standalone gable sample reuses the existing3m-wide /1.95m-rise secondary gable at unit scale. Roof panels use its exact half-slope length sqrt(1.5^2+1.95^2) and pitch atan2(1.95,1.5), with the52.43-degree verges and matching ridge. No facade asset was changed. The HeroB full front verge follows the same measured profile as FacadeBay01 HeroB: x[-3.22..2.33], base elevation6.03, apex(-1.05,10.40) on the approved building. These dimensions include the projecting eaves; they are not the4.65m underlying wall width. Roof/facade shoulder pieces must retain that deliberate overhang.

## Painted appearance and construction

The established GouacheMaterialSheet_v02 image is copied unchanged into the new asset family and packed in the blend. Slate uses lower-right painted blue-grey/sage regions, timber uses upper-right walnut. The materials are matte URP Lit: metallic0, smoothness0, specular/environment highlights disabled. No new packages, glossy maps, realistic noise, image blur, bloom, fog or grading were used. After actual render review, high-contrast repeated paint motifs were removed in favour of grouped blue-grey colour and sparse sage slates.

UV0 deliberately reuses this paint trim sheet; it is not a unique painting atlas or a lightmap UV channel. Visible thickness/cap/end faces are also UV mapped. All UV coordinates are finite and inside0..1, with zero collapsed UV triangles. For baked lighting later, author/generate a separate non-overlapping lightmap channel during an approved integration; do not repurpose UV0. No claim of unique UV0 islands is made.

Tiles have solid thickness and staggered courses, with small shared-boundary width changes and restrained cut-toe irregularity. A typical .43m slate overlaps the next .30m course by .13m. Tile layers are seated with nominal0.14mm clearance in the regular same-slope overlap calculation, avoiding interpenetrating row solids. Gable/verge/ridge/valley pieces provide deliberate overcloaks over seams; internal touching or concealed overlap is structural layering, not coplanar exposed surfaces. Border slivers are culled; backing/carriers close the roof below.

All individual solids are merged into logical component meshes. No tile is a separate Unity GameObject. Entire unique library totals39,388 triangles, before repeated review instances. The integration uses12 visible new roof renderers. This is suitable for review; evaluate distance LOD/static batching on target hardware before calling it shipping-optimised. Underlay meshes are composed of closed patch solids; coincident internal contacts are hidden, not exposed render seams.

## Non-destructive integration behaviour

The integration scene is a fresh copy of StyledDetails07, not a replacement or a modification to any earlier scene. Only the three old Dress_Slate renderers and three old roof bargeboard renderers are hidden in the copy. All original roof carrier geometry remains unchanged, including the unioned dormer walls and existing collision. The new assembly is added at its measured world placement. Its six new underlay renderers are disabled only in this instance to avoid redundant backing over the existing carriers; standalone prefabs/review retain backing.

All37 original colliders,10 original behaviour components, and original light settings/transforms were snapshotted and verified unchanged at authoring time. Decorations, player, stairs and room layout were not edited. New roof assets contain no colliders or gameplay scripts. Existing chimney/dormer clearances are preserved; no chimneys, dormers or botanical assets were modelled. Their openings can be revised by the measured-surface workflow later.

## Validation results

-47 source mesh parts: closed manifold edges, positive signed volumes, zero degenerate geometry triangles.
-UV validation: zero collapsed UV triangles; all coordinates finite within0..1. Intended paint-sheet reuse documented above.
-30 imported models: complete valid normals/UV arrays, valid shared matte URP materials, unit pivots/scales and source-matching orientation. Maximum canonical bound error approximately0.0013mm.
-1,431 visible roof-carrier coverage rays: zero missed underlay samples; maximum measured height error approximately0.0015mm against the specified6mm underlay inset. Retained chimney footprints were excluded.
-Regular slate overlap: .13m; nominal layer clearance .0001395m. Geometry at arbitrary changed pitches needs the corresponding adapter rather than forced nonuniform scale.
-All previous project files hash-checked unchanged. No package/settings/gameplay/collider changes and nothing committed.

Fit/coverage tests are sampled and do not certify every possible assembly or future opening. No blanket claim that all concealed overlapping solids have zero volume intersection is made: end caps and weathering overcloaks intentionally overlap their supporting layers. Manual close-up review of gutter endpoints and new attachment clearances remains appropriate before permanent integration. The approved scene itself has not received this kit.

## Rebuild / review tools

build_slate_roof_kit01.py uses bpy in the installed Blender. It refuses an existing source unless explicitly given -- --refine-own-kit. validate_roof_kit01.py reads the source and records topology/UV/coverage audits. New Editor snippets under ArtSource/Pipeline/Review: MeasureSlateRoofKit01.cs, CreateSlateRoofKit01Review.cs, CreateSlateRoofKit01Integration.cs, CaptureSlateRoofKit01Review.cs, CaptureSlateRoofKit01Integration.cs, ValidateSlateRoofKit01.cs. Scene-creation tools refuse existing destination scenes. Do not rerun them over artist-edited review scenes without preserving edits.
