# opamp_block — v4, KiCad 8

Fresh schematic capture from EDU1_Opamp_Block_Spec_v4.md. Both channels are complete. Open `opamp_block.kicad_pro`, then open the schematic.

The project contains exactly three schematic files:

- `opamp_block.kicad_sch`: the 12 support components, eight external hierarchical labels and two channel sheet symbols.
- `opamp_ch1.kicad_sch`: channel 1, fixtures A–D, 53 components.
- `opamp_ch2.kicad_sch`: channel 2, fixtures A–D, 53 components.

No DUT symbol, shared sheet, board-wide VAA entry/current jumper, scan header or ground tie is included. No PCB file, footprints, placement or routing is supplied. Symbols are arranged by fixture; matching local labels provide the connections within each sheet. The channel-to-top connections use hierarchical sheet pins, never global labels.

## Integrating into the master project

1. Copy this folder into the master project's folder, keeping the three schematic files together.
2. In the master schematic, place a hierarchical sheet and set its sheet file to `opamp_block/opamp_block.kicad_sch` (adjust the folder path if necessary).
3. Import the sheet pins from that sheet's hierarchical labels. Place exactly the eight pins below on the box border.
4. Wire those eight pins to the master project's DUT and analog rails by hand. The master owns the DUT, chip VAA supply/current break, scan/control and AGND/DGND tie.
5. Keep the existing child sheets intact. REF and AUX_5V are internal support connections, not additional external interface pins.

| Border pin | Internal net | Master connection |
|---|---|---|
| vaa | VAA | Chip analog supply, downstream of the board's current insertion point |
| agnd | AGND | Board analog ground |
| op1_inp | OP1_INP | DUT op1_inp |
| op1_inn | OP1_INN | DUT op1_inn |
| op1_out | OP1_OUT | DUT op1_out |
| op2_inp | OP2_INP | DUT op2_inp |
| op2_inn | OP2_INN | DUT op2_inn |
| op2_out | OP2_OUT | DUT op2_out |

KiCad implementation detail: a child file exposes **hierarchical labels**. The parent sheet symbol owns the matching border **sheet pins**, which are imported when placing the block. Therefore there is no extra wrapper sheet in this deliverable. KiCad's sheet-label direction types do not include `power_in`: `vaa` and `agnd` use `input` shape/direction, and the six signal ports use `passive`. Actual op-amp supply pins remain `power_in`. This implements the specified eight-port interface using KiCad's native hierarchy.

The uppercase internal net labels and lowercase external names are both preserved. KiCad's exported net names add the normal hierarchy prefix, such as `/Channel 1/CH1_A_SUM`. When nested, the master may determine the final full net path/name.

The symbols are cached inside the schematics. Small bundled generic libraries and `sym-lib-table` also support editing this standalone project. Do not overwrite the master's symbol table; if it needs these library entries for subsequent symbol updates, merge them deliberately. The generic OPAMP symbol has 1=+, 2=-, 3=V+, 4=V-, 5=OUT. This is a placeholder pin mapping, not a selected physical part/package or a simulation model.

## Validation results

Validated with **KiCad 8.0.8**: all three schematics load, export an XML netlist and render as SVG. The exported netlist was checked against the YAML net tables in v4, including all component values, tolerance fields, DNP flags and empty footprints.

| Self-check | Expected | Actual |
|---|---:|---:|
| External interface pins | 8 | 8 |
| Shared/support components | 12 | 12 |
| Channel 1 components | 53 | 53 |
| Channel 2 components | 53 | 53 |
| Total components | 118 | 118 |
| Shared/support nets | 6 | 6 |
| Channel 1 nets | 29 | 29 |
| Channel 2 nets | 29 | 29 |
| Total nets | 64 | 64 |

All **226 component pins** match their specified net membership; no missing, extra or duplicated pin memberships. **29 DNP components** are retained. Both shields on each channel's two coax connectors are connected as specified.

A separate temporary master schematic connected eight test points to the block's eight border pins. Its KiCad export confirmed that every external pin reaches exactly the specified internal nodes. That temporary test fixture is not part of this project.

The supplied v2 checker expects the old architecture (123 components and 73 nets) and cannot validate this block unchanged. `check_netlist_v4.py` checks the actual exported XML against the v4 Markdown source. As an independent cross-check, the supplied v2 topology was compared after removing only DUT, J_VAA, JP_IVAA, J_SCAN and R_GNDLINK and their now-empty nets: all remaining component types and internal net memberships agree.

To check future edits, first export a fresh netlist, then run:

```sh
kicad-cli sch export netlist --format kicadxml -o opamp_block.net.xml opamp_block.kicad_sch
python check_netlist_v4.py opamp_block.net.xml
```

The Python checker requires PyYAML. `tools/generate.py` is the fresh-generation source; it accepts the path to an installed KiCad symbol directory. Running it overwrites this generated capture, so do not run it over subsequent manual edits.

### ERC and annotation findings — not suppressed

The standalone ERC report has **2 errors and 58 warnings**:

- 2 `power_pin_not_driven` errors: AUX_5V and AGND do not contain a power-output source symbol. The bench terminal is passive, and board power belongs outside this block. The capture intentionally includes no extra power flags or supply-source components.
- 50 `similar_labels` warnings: the required lowercase external ports and uppercase internal labels differ only by case.
- 8 `multiple_net_names` warnings: each external port connects to its specified uppercase internal net, e.g. `vaa` to `VAA`.

There are no other reported ERC violation categories. The naming aliases connect as intended, as verified by the parent-sheet test. ERC is **not clean**, and no violations were hidden or excluded. Power-drive modeling must be reviewed in the complete master project.

KiCad's netlist exporter also reports an annotation warning while preserving the spec's literal reference designators (many have nonnumeric endings, such as `U_REF` and `JP1A_INN`). These references were not automatically renumbered. Coordinate any later annotation with the master project and update the spec/checker mapping if references change.

These tests establish schematic capture/connectivity correctness, not analog stability, measurement accuracy, physical package selection or new MIL-STD compliance verification.

## Values deliberately unresolved

| References | Literal value |
|---|---|
| R1_C2, R2_C2 | TBD-AD |
| R1_CL, R2_CL, C1_CNULL, C2_CNULL | TBD |
| R1_D1A, R1_D1B, R2_D1A, R2_D1B | TBD-AD |
| C1_D1A, C1_D1B, C2_D1A, C2_D1B | TBD-AD |
| C1_D2, C2_D2, R1_D2, R2_D2 | TBD |
| U_REF, U1_NULL, U2_NULL | ZERO_DRIFT_RRIO_TBD |

Components without a specified value have an empty schematic Value field; KiCad represents that as `~` in its XML export. No numerical values were invented.

## Carry-forward build and integration notes

- Fit exactly one fixture's three isolation shunts at a time per channel. A jumper symbol's fitted flag represents its hardware; it is not an instruction to install every fixture's shunts simultaneously. Silkscreen fixture letters beside them.
- Fixture A's SUM/INN/NIP/INP high-impedance nodes require REF-driven guards, no vias inside the guard and no solder-mask opening, as stated in the spec. Notes appear on both channel sheets.
- Fixture B defaults to R_BDIR fitted, C_BAC and R_BBIAS DNP. For AC coupling, remove R_BDIR and fit both alternatives. JP_BG open selects the follower; closed selects the approximately 101 noise gain configuration. For PD/Iq, leave the generator connected, set AC/pulse amplitude to zero and DC level to REF. This is the specified EDU1 adaptation, not literal Figure 4005-1 conformity.
- Fixture C retains its servo path through the external chip. R_CVC is 0 ohm and fitted; C_CNULL is DNP. JP_C is closed for the retained tests. Do not add local feedback around the null amplifier.
- Fixture D is entirely DNP, including its isolation jumpers.
- U_REF senses feedback after the 10-ohm R_REFISO. C_REF2A remains DNP; stability and final amplifier selection remain unresolved.
- J_AUX is the block's AUX_5V terminal. Its bench supply return connects to the board's AGND; no additional ground connector is added here.
- The pin-48 discrepancy remains open: the source spreadsheet labels its block OPAMP1 but names the signal op2_inp. This project follows the specified signal names. Resolve this when wiring the master's DUT; no physical chip-pin assignment is made here.

`verification/` contains the actual SVG sheet previews, connectivity/integration results and unsuppressed ERC JSON. `expected_v4.json` records the generator's parsed model for traceability; the checker independently reads the Markdown source instead.
