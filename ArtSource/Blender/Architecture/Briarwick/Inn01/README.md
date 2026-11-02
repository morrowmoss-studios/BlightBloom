# Inn01 source

Current editable source: `BW_Inn01.blend`, metric units and packed working color images. Main two-storey block plus lower recessed wing; no complete interior, stair or playable room assembly.

Reproduction only when needed: paint `prepare_shingles.py`, then Blender `build_inn.py` -> `finish_frames_and_deck.py` -> `seat_roof_cover.py` -> `clear_door_sills.py`; use review `Integrate.cs` for a fresh integration. Initial builder refuses an existing candidate and integration refuses duplicate roots. The saved source is authoritative for ordinary editing; do not regenerate other village buildings.

`ModelCatalog.json` records final group counts and material order. New exports use the established Blender -Z-forward/Y-up FBX conversion. Native package/cottage extracts and StableA02/Bakery02 helper files are read-only dependencies. Unity prefab owns marker transforms and static collision. See `ArtSource/Pipeline/Review/BriarwickInn01/README.md` for all measurements, validation and limitations.
