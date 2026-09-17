# EDU1 DUT

Standalone KiCad symbol + footprint for the EDU1 device under test (U_DUT1), split out of the op-amp block project so it can be reused independently.

- `EDU1_Rebuilt.kicad_sym` — the `EDU1` symbol (64-pin), rebuilt from `Chip pins.xlsx`.
- `EDU1_Selected.pretty/EDU1_DUT_Socket_PGA64_PCB3006-1.kicad_mod` — the assigned footprint, a PGA64 socket pattern targeting the Proto Advantage PCB3006-1 carrier.

## Footprint status: unverified candidate

Per the source project's `DUT_FINDINGS.md`: this footprint is a **candidate** assignment, not a fabrication-verified one. The four pin groups (top/bottom/left/right) do not all sit on one shared 2.54 mm grid, and inter-group spacing was chosen for clearance rather than measured off the physical PCB3006-1 carrier or its dimensioned mechanical drawing. Do not order DUT socket hardware or approve this footprint for fabrication until the carrier's actual mating-pin coordinates are measured and cross-checked against this pattern.
