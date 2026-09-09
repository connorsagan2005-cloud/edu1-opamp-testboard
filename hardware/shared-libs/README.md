# hardware/shared-libs

Owner: whole team (changes reviewed via PR).

Shared KiCad symbol / footprint libraries used across multiple blocks **and** the
master board project.

- **`EDU1.kicad_sym`** — the corrected EDU1 padframe symbol. This is the single copy.
  Blocks and the master board reference it here via `sym-lib-table` rather than
  keeping per-project duplicates. Its changelog lives at
  [`docs/chip/`](../../docs/chip/).
- Any other footprint/symbol library shared by more than one project.

Generic vendor libraries that a block bundles purely for standalone portability (e.g.
the op-amp block's `Device.kicad_sym`, `Connector.kicad_sym`) stay inside that block's
folder — only genuinely shared, project-specific libraries belong here.

Not yet populated — the corrected `EDU1.kicad_sym` lands here when available.
