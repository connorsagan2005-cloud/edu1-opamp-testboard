# hardware/blocks/comparator

Owner: TBD. Status: **not started.**

Self-contained KiCad hierarchical block for characterizing the two EDU1 comparators
(`COMP1`, `COMP2`). Follow the structure of
[`../opamp/`](../opamp/) exactly: own `.kicad_pro` + schematic set, a small set of
external hierarchical pins (`vaa`, `agnd`, plus chip-facing comparator pins named as
the EDU1 symbol names them), bundled generic symbol libs + local `sym-lib-table`, no
`DUT` symbol, no board-wide power/scan/ground infrastructure.

Design notes carried from meeting notes:

- The comparator shares an **unclocked-comparator input stage with the op-amp**. Input
  offset / bias methods can borrow from the op-amp fixtures.
- The comparator's **output is digital** — propagation delay, response time vs.
  overdrive, and hysteresis measurement need dedicated fixtures the op-amp block does
  not have.

Block-local net prefix: `COMP1_...`, `COMP2_...`.

No test circuits are specified yet — do not fabricate them here.
