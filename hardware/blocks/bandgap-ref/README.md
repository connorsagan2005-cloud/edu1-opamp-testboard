# hardware/blocks/bandgap-ref

Owner: TBD. Status: **not started.**

Self-contained KiCad hierarchical block for characterizing the EDU1 bandgap reference
(BGR). Follow the structure of [`../opamp/`](../opamp/) exactly: own `.kicad_pro` +
schematic set, a small set of external hierarchical pins (`vaa`, `agnd`, plus the
chip-facing BGR pins named as the EDU1 symbol names them), bundled generic symbol libs
+ local `sym-lib-table`, no `DUT` symbol, no board-wide power/scan/ground
infrastructure.

Standards note: **no block-specific IEEE/JEDEC standard was found.** Fallback is the
MIL-STD-883 4001-series offset/drift methodology plus datasheet-driven structure
(initial accuracy, tempco / box method, line regulation, noise, start-up). See
[`docs/standards/INDEX.md`](../../../docs/standards/INDEX.md).

Block-local net prefix: `BGR_...`.

No test circuits are specified yet — do not fabricate them here.
