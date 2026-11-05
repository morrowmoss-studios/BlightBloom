# Environment05 Revision01 issues

| Issue | Status | Evidence / next step |
|---|---|---|
| Sparse prior valley; no Terrain details | Addressed for coverage review | 79,032 clumps, matched views; artistic approval pending |
| Visible cone proxies | Resolved | 51 replacements, seven nearby existing trees; proxy references disabled |
| Converted albedo sheen / importer test errors | Resolved | Automatic ordinary compression, no alpha; final BC1 and Console checks |
| Natural 3D debris / dedicated reeds unavailable | Outstanding | Ground layers and available plants used; appropriate assets needed |
| Distant presentation, card repetition, GPU cost | Pending | 95 m culling/unchanged fog; build profile and visual approval needed |
| Blockout roads/bridge/creek and terrain edges | Deferred / protected | Geometry unchanged |
| Manual camera comfort | Pending manual review | Automated input/cast checks pass |
| Disk headroom | Caution | Transient full error during docs; ~2.5 GiB subsequently reported; no broad cleanup authorized |

2026-11-05 recovery audit: saved scene reloaded, 79,032 details and all regional totals verified; no repairs required. See [post-storage audit](PostStorageAudit20261105/README.md). All 4,389 audit-baseline asset/config hashes unchanged; current Console clear. Editor profiling now captured360 frames (main-thread medians47–53ms, reported draw calls1,955–2,852). Performance review remains pending a target-build/GPU profile; no GPU timing available.
