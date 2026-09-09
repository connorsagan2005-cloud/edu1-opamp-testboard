# docs/chip — EDU1 chip source-of-truth data

Owner: whole team (changes reviewed via PR).

What belongs here:

- **`Chip_pins.xlsx`** — the padframe / pinout spreadsheet. Authoritative for chip pin
  names and numbers. Not yet committed.
- **`EDU1.kicad_sym`** — the shared EDU1 padframe symbol used by the master board and
  referenced (not copied) by blocks. The corrected/current copy lives in
  [`hardware/shared-libs/`](../../hardware/shared-libs/); keep a pointer here, not a
  duplicate.
- **`EDU1_symbol_changelog.md`** — every change to the symbol, dated, with the reason
  and who made it.
- **Pin-mapping / discrepancy notes** — e.g. the open pin-48 issue: the spreadsheet
  labels its block `OPAMP1` but names the signal `op2_inp`. Track resolutions here.

Rule: chip pin names are never renamed per block. This folder is where the canonical
names are defined; everything else follows it.
