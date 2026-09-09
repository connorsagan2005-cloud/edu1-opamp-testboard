# hardware/master-board

Owner: groupmate (master-board project owner). Status: not yet started as a KiCad
project / git content — this folder is a labeled landing place for it.

## What lives here

The **master board project** — the one project that owns the chip:

- The `DUT` symbol for the EDU1 64-pin padframe (from
  [`hardware/shared-libs/EDU1.kicad_sym`](../shared-libs/)).
- The main **VAA bench connector** + **current-insertion jumper** (supply-current
  measurement break).
- The **scan/control header** (`sin` / `sclk` / `srstb` / `slatch` / `ssel`).
- The single **AGND/DGND tie point**.

No per-block fixtures live here — each block is its own project under
[`hardware/blocks/`](../blocks/).

## How a block gets integrated

Each folder under `hardware/blocks/<block>/` is a self-contained KiCad hierarchical
block exposing a few named pins (`vaa`, `agnd`, plus chip-facing signal pins). To
integrate one:

1. In the master schematic, add a hierarchical sheet pointing at
   `../blocks/<block>/<block>.kicad_sch` (relative path — this is why the repo is a
   monorepo, not submodules).
2. Import the sheet pins from that block's top-sheet hierarchical labels.
3. Wire those pins by hand to the `DUT` symbol and the board's analog rails. The
   master owns VAA supply/current-break, scan/control, and the ground tie.

**Worked example:** [`hardware/blocks/opamp/README.md`](../blocks/opamp/README.md) —
its "Integrating into the master project" section, including the 8-pin border table,
is the concrete procedure to copy for every future block.
