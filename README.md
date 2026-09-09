# EDU1 MQP — chip characterization & datasheet

Top-level repository for the WPI Major Qualifying Project characterizing the **EDU1**
mixed-signal IC (reported name **CRIMSON**). The chip was designed and taped out by a
prior team; this project develops the test procedures, characterizes each analog block
on custom PCBs, and produces the chip's first datasheet from measured results.

- **Team:** Connor, James, Matthew
- **Advisor:** Prof. Suat Ay · **TA:** Ibrahim Bozyel

## The chip

64 pins, ~12 independent analog/digital blocks (2× VDAC, 2× IDAC, 4-channel ADC,
2× instrumentation amp, 2× op-amp, 2× comparator, 2× 555-style timer, 2× LDO,
1× bandgap reference), all configured over a 5-pin serial scan chain
(`sin` / `sclk` / `srstb` / `slatch` / `ssel`).

**This term's scope:** bandgap reference (BGR), LDO, comparator, op-amp.
Everything else (VDAC / IDAC / ADC / instrumentation amps / timers) is next term, on
separate PCBs.

## Architecture: master board + portable hierarchical blocks

This is a **monorepo** (not submodules — the master project and the blocks reference
each other by relative KiCad sheet paths, which submodules make painful).

- **One master board project owns the chip.** It carries the `DUT` symbol for the EDU1
  padframe, the main VAA bench connector + current-insertion jumper, the scan/control
  header, and the single AGND/DGND ground tie point. Owned by a groupmate; lives in
  [`hardware/master-board/`](hardware/master-board/).
- **Each analog block is its own self-contained, portable KiCad hierarchical block**
  under [`hardware/blocks/`](hardware/blocks/), exposing a small set of named external
  pins (e.g. `vaa`, `agnd`, plus the block's signal pins). No `DUT` symbol inside a
  block, no duplicated board-wide infrastructure.
- **Integration** = place the block as a hierarchical sheet in the master project and
  wire its exposed pins to the `DUT` symbol by hand.

Why: portability (a block can be opened, edited and verified standalone) and a single
shared DUT / power / scan infrastructure instead of a copy per block.

The op-amp block ([`hardware/blocks/opamp/`](hardware/blocks/opamp/)) is complete and
is the **reference example** — its README's integration section is the worked
procedure every future block should follow.

## Net-naming convention

- **Chip pin names** stay exactly as the padframe / pinout spreadsheet and the shared
  `EDU1` KiCad symbol define them. That is the source of truth — never renamed per
  block.
- **Board-wide global nets** (chip supply / ground) get UPPERCASE names defined once:
  `vaa` → `VAA`, `agnd` → `AGND`, etc.
- **`REF`** (the vaa/2 pseudo-ground) is reserved globally. Reuse it exactly; never
  redefine it in a new block.
- **Block-local nets** get a `<BLOCK><CHANNEL>_<FIXTURE>_` prefix, e.g. `CH1_A_INN`
  for op-amp channel 1, fixture A. Future blocks follow the same pattern:
  `COMP1_...`, `BGR_...`, `LDO_...`.

## Directory map

```
docs/
  chip/            EDU1 pinout spreadsheet, shared EDU1.kicad_sym + changelog, pin notes
  standards/       INDEX.md only — links each block to its test-template standard/datasheet
                   (no copyrighted PDFs in git)
  test-procedures/ one subfolder per block: finalized test-circuit spec + deviations doc
  meeting-notes/
hardware/
  master-board/    groupmate's project: DUT symbol, VAA connector + current jumper,
                   scan header, AGND/DGND tie  (README stub for now)
  blocks/
    opamp/         complete — reference example
    comparator/    not started (stub)
    bandgap-ref/   not started (stub)
    ldo/           not started (stub)
  shared-libs/     symbol/footprint libraries shared across blocks + master
firmware/          FPGA (Basys 3) scan-chain driver / test automation  (stub)
test-scripts/      bench automation / data capture / per-block analysis  (stub)
results/           measured characterization data → datasheet source  (stub)
```

## How to add a new block

Derived from how the op-amp block was built and integrated:

1. **Make a folder** under `hardware/blocks/<block>/` with its own `.kicad_pro` and
   schematic set. No `DUT` symbol, no board-wide power/scan/ground infrastructure —
   the master board owns all of that.
2. **Define the external interface** as a small set of hierarchical labels on the top
   sheet: `vaa`, `agnd`, plus the block's chip-facing signal pins named exactly as the
   EDU1 symbol names them. Reuse `REF` as-is if the block needs the vaa/2 pseudo-ground;
   never redefine it.
3. **Keep block-local nets prefixed** `<BLOCK><CHANNEL>_<FIXTURE>_` (see convention
   above).
4. **Bundle the generic symbol libs** you use plus a local `sym-lib-table` with
   `${KIPRJMOD}` URIs so the project opens standalone. The corrected `EDU1.kicad_sym`
   comes from `hardware/shared-libs/`, not a per-block copy.
5. **Verify standalone:** export an XML netlist with `kicad-cli`, check it against the
   spec, run ERC, and record results under `verification/`. Document any ERC findings
   you are deliberately not suppressing.
6. **Integrate:** in the master project, place the block as a hierarchical sheet
   pointing at `../blocks/<block>/<block>.kicad_sch`, import its sheet pins, and wire
   them to the `DUT` symbol and analog rails by hand.
7. **Write the block README** with an integration table (border pin → internal net →
   master connection), following `hardware/blocks/opamp/README.md`.

## Branch convention

One feature branch per block/person, merged into the default branch via PR, so the
master-board owner and each block owner aren't editing the same schematic files
directly.
