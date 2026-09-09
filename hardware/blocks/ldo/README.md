# hardware/blocks/ldo

Owner: TBD. Status: **not started.**

Self-contained KiCad hierarchical block for characterizing the two EDU1 LDOs. Follow
the structure of [`../opamp/`](../opamp/) exactly: own `.kicad_pro` + schematic set, a
small set of external hierarchical pins (`vaa`, `agnd`, plus the chip-facing LDO pins
named as the EDU1 symbol names them), bundled generic symbol libs + local
`sym-lib-table`, no `DUT` symbol, no board-wide power/scan/ground infrastructure.

Design / test notes:

- The team now has **temperature-chamber access**, so LDO tempco and dropout-vs-temp
  sweeps are in scope.
- Expect fixtures for line/load regulation, dropout, PSRR, load-transient, and
  quiescent current.

Block-local net prefix: `LDO1_...`, `LDO2_...`.

No test circuits are specified yet — do not fabricate them here.
