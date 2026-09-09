# EDU1 Op-Amp Test Block — Schematic Capture Specification (self-contained hierarchical block)

**Scope: op-amp characterization only (OPAMP1 and OPAMP2), packaged as one drop-in
hierarchical block. No other EDU1 block, and no board-wide infrastructure (the DUT
symbol, the main VAA bench connector, the current-insertion jumper, the scan/control
header, or the AGND/DGND tie point) is in this spec — those live in the master board
project and are out of scope here.**

This is a complete, pin-level net specification. It is written to be executed, not
interpreted. Every net is enumerated; nothing is left to inference.

---

## 0 · Instructions for the agent

Read all of this section before generating anything.

### What to produce

A KiCad 8 project consisting of one **self-contained hierarchical block**,
`opamp_block.kicad_sch`, with exactly the 8 external pins in §1a, containing both
channels internally (§2). This is meant to be dropped into a separate, larger board
project as a single sheet symbol — the person doing that will wire its 8 pins to
their DUT symbol and board power rails. Generate **both channels in this pass** —
channel 1 and channel 2, complete.

### Hard rules

1. **Do not invent values.** Any component whose `value` field is `TBD` or `TBD-AD` gets
   that literal string as its schematic value. Do not substitute a plausible number.
   These are blocked on simulation data that does not exist yet (§8).
2. **Do not add components.** If a net looks like it needs a pull-up, a series resistor,
   or extra decoupling, it does not. Every intentional part is listed. If you believe
   something is genuinely missing, emit it as a comment in your output and stop —
   do not add it silently.
3. **Do not remove components.** Parts marked `fitted: false` (DNP) still get a symbol
   and a footprint. They are laid out deliberately.
4. **Do not merge or rename nets.** Net names are load-bearing; they map to a test
   procedure document. `CH1_A_INN` and `OP1_INN` are different nets separated by a
   jumper, and that separation is the point (§4).
5. **Do not place or route.** Schematic capture only. Layout is a separate pass.
6. **Every pin listed must be connected.** No floating pins, no implicit connections.
   If a component pin does not appear in the net list in §3–§8, that is a spec bug —
   report it rather than guessing.
7. **No `DUT` symbol anywhere in this project.** The chip is owned by the master
   board project, not this block. Wherever an earlier version of this spec would
   have said `DUT.op1_inn`, instead terminate that net on a **hierarchical sheet
   pin** named `op1_inn` on `opamp_block.kicad_sch` (see §1a for the full list of 8).
   A hierarchical sheet pin is the standard KiCad mechanism for exposing a named
   connection point on the outside of a sheet block — when this block is placed as
   a sheet symbol in another project, that pin appears on the box's border for a
   human to wire up by hand. Do not use global labels for this; global labels only
   resolve within one project, and this block is meant to be portable into a
   different project entirely.
8. **`vaa` and `agnd` are also hierarchical sheet pins, not internal nets.** Every
   component inside this block that needs supply or ground connects to these two
   pins, not to a locally-instantiated bench connector — the bench VAA connector,
   the current-insertion jumper, and the AGND/DGND tie point all live in the master
   project, upstream of this block's `vaa`/`agnd` pins, and are out of scope here.

### Symbol selection

Use generic KiCad library symbols. Verify names against the installed library version
before use rather than trusting the suggestions below.

| Type | Suggested symbol | Pins used |
|---|---|---|
| `R` | `Device:R` | 1, 2 |
| `C` | `Device:C` | 1, 2 |
| `SW` | `Switch:SW_SPST` | 1, 2 |
| `JP` | `Connector_Generic:Conn_01x02` | 1, 2 |
| `TP` | `Connector:TestPoint` | 1 |
| `J1` (single terminal) | `Connector_Generic:Conn_01x01` | 1 |
| `SMA` | `Connector_Coaxial:Conn_Coaxial` | signal → 1, shield → 2 → AGND |
| `OPAMP` | any single op-amp with explicit power pins | `+`, `-`, `OUT`, `V+`, `V-` |

The op-amp part numbers are not selected yet. Use a generic symbol and leave the value
field as the string given in the component table (`U_REF` → `ZERO_DRIFT_RRIO_TBD`).

### Footprints

Leave every footprint field empty. Package selection is blocked (§8) and passives will be
chosen during layout. Do not assign footprints speculatively.

### Self-check before you finish

Report these counts. If they do not match, something was dropped.

| Quantity | Expected |
|---|---|
| External hierarchical sheet pins | 8 |
| Internal shared/support components (REF generator + AUX_5V) | 12 |
| Components per channel | 53 |
| Total components (both channels, no DUT — it isn't in this project) | 118 |
| Internal shared/support nets | 6 |
| Nets, per channel | 29 |
| Total internal nets (both channels) | 64 |

---

## 1 · Context an agent needs

Three facts drive the whole design. Do not re-derive them; they are settled.

**EDU1 has no negative analog supply rail.** The padframe carries `vaa` (pin 40) and `agnd`
(pin 41) for the analog domain. Passive signal-reference ground nodes in the cited
MIL-STD-883-4 figures become `REF`, a buffered vaa/2 pseudo-ground generated directly
on this block's own top sheet (§2, §3). Bench-instrument returns/coax shields remain
on `AGND`; their stimulus
voltages are offset so the intended signal is centered on `REF`. `AGND` is real ground
and is also the return for supply decoupling.

**Four fixtures share three external pins.** Fixtures A, B, C and D all connect to
`op1_inn` / `op1_inp` / `op1_out`. They are isolated from each other by shunt jumpers,
and exactly one fixture's jumper set is fitted at a time. This is why the fixture-side
net (`CH1_A_INN`) and the pin-side net (`OP1_INN`) are separate nets.

**The board is two identical channels.** Channel 1 drives OPAMP1, channel 2 drives
OPAMP2. Duplicating the fixtures removes the need for any DUT-select multiplexing,
which keeps switches out of the offset-voltage and bias-current paths.

---

## 1a · The 8 external hierarchical sheet pins

These are the only points where this block touches the outside world. Define them
as hierarchical sheet pins on `opamp_block.kicad_sch` itself (§2) — not global
labels, not a symbol.

| Pin name | Electrical type | Purpose |
|---|---|---|
| `vaa` | power_in | Chip supply rail — feeds the REF generator and local decoupling |
| `agnd` | power_in | Chip analog ground — return for everything in this block |
| `op1_inp` | passive | Channel 1 fixture-side connection to the DUT's noninverting input |
| `op1_inn` | passive | Channel 1 fixture-side connection to the DUT's inverting input |
| `op1_out` | passive | Channel 1 fixture-side connection to the DUT's output |
| `op2_inp` | passive | Channel 2 fixture-side connection to the DUT's noninverting input |
| `op2_inn` | passive | Channel 2 fixture-side connection to the DUT's inverting input |
| `op2_out` | passive | Channel 2 fixture-side connection to the DUT's output |

Whoever places this block in the master board project wires these 8 pins by hand
to their DUT symbol and board power rails. Nothing else about this block is visible
from outside it — `REF`, the AUX_5V bench connector, and every fixture-internal net
are fully enclosed.

---

## 2 · Sheet structure

One project, containing this block plus its two channel sub-sheets:

```
opamp_block.kicad_sch          (top of this block — carries the 8 pins in §1a)
├── opamp_ch1.kicad_sch        §4–§7 with CH = CH1, OP = OP1, prefix 1_
└── opamp_ch2.kicad_sch        §4–§7 with CH = CH2, OP = OP2, prefix 2_
```

The REF generator and AUX_5V hardware (§3) live directly on `opamp_block.kicad_sch`
itself — no separate "shared" sheet, since there's nothing left on it that needs to
be its own file once the DUT, scan header, bench-VAA connector, and ground tie point
are all out of scope. Two levels total: the block's own top sheet, and its two
channel children.

Generate **both channel sheets in this pass.** They are identical except for the
substitutions in §10.

---

## 3 · Block-internal shared hardware (REF generator + AUX_5V)

Lives directly on `opamp_block.kicad_sch`'s own top level (§2) — not a separate sheet.

### Components

```yaml
components:
  - {ref: C_VAA1,     type: C,     value: "100n",                  fitted: true}
  - {ref: C_VAA2,     type: C,     value: "10u",                   fitted: true}
  - {ref: R_REF1,     type: R,     value: "10k",  tol: "0.1%",     fitted: true}
  - {ref: R_REF2,     type: R,     value: "10k",  tol: "0.1%",     fitted: true}
  - {ref: C_REF1,     type: C,     value: "10u",                   fitted: true}
  - {ref: U_REF,      type: OPAMP, value: "ZERO_DRIFT_RRIO_TBD",   fitted: true}
  - {ref: R_REFISO,   type: R,     value: "10",                    fitted: true}
  - {ref: C_REF2A,    type: C,     value: "10u",                   fitted: false}
  - {ref: C_REF2B,    type: C,     value: "100n",                  fitted: true}
  - {ref: J_AUX,      type: J1,    value: "AUX_5V_BENCH",          fitted: true}
  - {ref: C_AUX1,     type: C,     value: "100n",                  fitted: true}
  - {ref: C_AUX2,     type: C,     value: "10u",                   fitted: true}
```

`J_AUX`/`C_AUX1`/`C_AUX2` are this block's own bench-supply entry point for `U_REF`
and the two null amps — separate from the chip's `vaa`, and out of scope for the
master project. It's a normal bench connector living inside this block, not a
hierarchical pin, since nothing outside this block ever needs to see it.

**Not in this block — removed from the original design because they're board-wide,
not op-amp-specific, and belong to the master project instead:**
`J_VAA`/`JP_IVAA` (the main chip VAA bench connector and current-insertion jumper —
one single point should break the *whole chip's* rail, not one per block), `J_SCAN`
(the scan/control header — none of these fixtures ever touch the scan bus or
`power_en`), and `R_GNDLINK` (the single AGND/DGND tie point for the whole board).

### Nets (internal to this block, visible on both channel sheets)

```yaml
nets:
  VAA:        [vaa, C_VAA1.1, C_VAA2.1, R_REF1.1]
  REF_DIV:    [R_REF1.2, R_REF2.1, C_REF1.1, U_REF.+]
  U_REF_OUT:  [U_REF.OUT, R_REFISO.1]
  REF:        [R_REFISO.2, U_REF.-, C_REF2A.1, C_REF2B.1,
               R1_AVQI.1, R1_BV1.1, R1_BBIAS.2, R1_C1A.1, R1_C1B.1,
               C1_D1A.2, C1_D1B.2, R1_D1B.1,
               R2_AVQI.1, R2_BV1.1, R2_BBIAS.2, R2_C1A.1, R2_C1B.1,
               C2_D1A.2, C2_D1B.2, R2_D1B.1]
  AUX_5V:     [J_AUX.1, C_AUX1.1, C_AUX2.1, U_REF.V+, U1_NULL.V+, U2_NULL.V+]
  AGND:       [agnd, C_VAA1.2, C_VAA2.2, R_REF2.2, C_REF1.2,
               C_REF2A.2, C_REF2B.2, C_AUX1.2, C_AUX2.2,
               U_REF.V-, U1_NULL.V-, U2_NULL.V-,
               J1_BSIG.2, J1_DSIG.2, J2_BSIG.2, J2_DSIG.2]
```

`vaa` and `agnd` here are the hierarchical sheet pins from §1a, not component
references — the net simply terminates on the pin.

### Design intent (do not act on this — it is for a human reviewer)

`U_REF` runs from `AUX_5V` rather than `VAA` so it has headroom to both source and sink
at vaa/2. `R_REFISO` is 10 Ω and sits **inside** the feedback loop — feedback is sensed at
`REF`, after the resistor — which is the standard way to keep an op-amp stable while
driving a capacitive load. That is why the isolation resistor exists; setting it to 0 Ω
would remove the mitigation rather than provide one.

`C_REF2B` (100 nF) is fitted and `C_REF2A` (10 µF) is DNP. Some AC bypass on `REF` is
not optional: `REF` is a pseudo-ground, and its impedance rises with frequency as
`U_REF`'s loop gain falls. The GBW test (§6) returns the DUT's inverting node into `REF`
through a 10 Ω `R_BG`, so any `REF` impedance at the sweep frequency adds directly to that
10 Ω and corrupts the gain ratio. Populate `C_REF2A` as well once the `U_REF` part is
selected and checked. The divider is ratiometric to `VAA` by design, so `REF` tracks the rail.

---

## 4 · Channel 1 — fixture isolation

These three nets are where all four fixtures meet the block's external interface.
Every jumper's pin 2 lands here, on the `op1_inn`/`op1_inp`/`op1_out` hierarchical
sheet pins from §1a; every jumper's pin 1 is on its own fixture's local net.

```yaml
nets:
  OP1_INN: [op1_inn, JP1A_INN.2, JP1B_INN.2, JP1C_INN.2, JP1D_INN.2]
  OP1_INP: [op1_inp, JP1A_INP.2, JP1B_INP.2, JP1C_INP.2, JP1D_INP.2]
  OP1_OUT: [op1_out, JP1A_OUT.2, JP1B_OUT.2, JP1C_OUT.2, JP1D_OUT.2]
```

Fitting rule, for the fabrication notes: exactly one fixture's three shunts may be
fitted at a time. Silkscreen the fixture letter beside each jumper.

---

## 5 · Channel 1 — Fixture A · Vos, Ib, Ios

Mirrors MIL-STD-883-4 Figure 4001-1. Nothing removed from the figure.

```yaml
components:
  - {ref: R1_A1,    type: R,  value: "10k",   tol: "0.1%", fitted: true,  mil: "R1"}
  - {ref: R1_A2,    type: R,  value: "1M",    tol: "0.1%", fitted: true,  mil: "R2"}
  - {ref: R1_A3A,   type: R,  value: "10M",                fitted: true,  mil: "R3 inverting"}
  - {ref: R1_A3B,   type: R,  value: "10M",                fitted: true,  mil: "R3 noninverting"}
  - {ref: R1_A4,    type: R,  value: "9k90",  tol: "0.1%", fitted: true,  mil: "R4 = R1||R2"}
  - {ref: R1_AVQI,  type: R,  value: "0",                  fitted: true,  mil: "VQI source link"}
  - {ref: SW1_A1,   type: SW,                              fitted: true,  mil: "S1"}
  - {ref: SW1_A2,   type: SW,                              fitted: true,  mil: "S2"}
  - {ref: JP1A_INN, type: JP,                              fitted: true}
  - {ref: JP1A_INP, type: JP,                              fitted: true}
  - {ref: JP1A_OUT, type: JP,                              fitted: true}
  - {ref: TP1_EA0,  type: TP,                              fitted: true,  mil: "E0"}
  - {ref: TP1_VQI,  type: TP,                              fitted: true,  mil: "VQI"}

nets:
  CH1_VQI:   [R1_AVQI.2, R1_A1.1, R1_A4.1, TP1_VQI.1]
  CH1_A_SUM: [R1_A1.2, R1_A2.1, R1_A3A.1, SW1_A1.1]
  CH1_A_INN: [R1_A3A.2, SW1_A1.2, JP1A_INN.1]
  CH1_A_NIP: [R1_A4.2, R1_A3B.1, SW1_A2.1]
  CH1_A_INP: [R1_A3B.2, SW1_A2.2, JP1A_INP.1]
  CH1_A_OUT: [R1_A2.2, JP1A_OUT.1, TP1_EA0.1]
```

`SW1_A1` is in parallel with `R1_A3A`; `SW1_A2` is in parallel with `R1_A3B`. Both
switches must be independently operable — the measurement uses all four of their
combined states.

**Layout constraint to carry forward:** `CH1_A_SUM`, `CH1_A_INN`, `CH1_A_NIP` and
`CH1_A_INP` are high-impedance nodes carrying possible picoamp currents. They need
`REF`-driven guard rings, no vias inside the ring, and no solder-mask opening. Record
this as a schematic note or net class so it survives into layout.

---

## 6 · Channel 1 — Fixture B · Slew rate, phase margin, GBW, PD/Iq

One network reproduces the 4002-1 and 4004-4 signal topologies. `JP1_BG` open gives
the unity-gain follower used for slew-rate and phase-margin testing; `JP1_BG` closed
gives the Figure 4004-4 gain stage (≈101). The PD/Iq use of this fixture is a documented
EDU1 engineering adaptation of Method 4005.1 §3.1, not a literal implementation of
Figure 4005-1.

```yaml
components:
  - {ref: R1_BF,    type: R,  value: "1k",   tol: "0.1%", fitted: true,  mil: "4002-1 R1 / 4004-4 R2"}
  - {ref: R1_BIN,   type: R,  value: "1k",   tol: "0.1%", fitted: true,  mil: "4002-1 R2 / 4004-4 R3"}
  - {ref: R1_BG,    type: R,  value: "10",   tol: "0.1%", fitted: true,  mil: "4004-4 R1 gain leg"}
  - {ref: R1_BV1,   type: R,  value: "0",                 fitted: true,  mil: "4004-4 V1 link"}
  - {ref: R1_BDIR,  type: R,  value: "0",                 fitted: true}
  - {ref: C1_BAC,   type: C,  value: "1u",                fitted: false}
  - {ref: R1_BBIAS, type: R,  value: "10k",               fitted: false}
  - {ref: JP1_BG,   type: JP,                             fitted: true}
  - {ref: JP1B_INN, type: JP,                             fitted: true}
  - {ref: JP1B_INP, type: JP,                             fitted: true}
  - {ref: JP1B_OUT, type: JP,                             fitted: true}
  - {ref: J1_BSIG,  type: SMA, value: "GENERATOR",        fitted: true,  mil: "V1 / eI"}
  - {ref: J1_BV1,   type: J1,  value: "V1_BIAS",          fitted: true}
  - {ref: TP1_EB0,  type: TP,                             fitted: true,  mil: "E0 / e0"}

nets:
  CH1_B_SIGIN: [J1_BSIG.1, R1_BDIR.1, C1_BAC.1]
  CH1_B_SIG:   [R1_BDIR.2, C1_BAC.2, R1_BIN.1]
  CH1_B_INP:   [R1_BIN.2, JP1B_INP.1, R1_BBIAS.1]
  CH1_B_INN:   [R1_BF.2, R1_BG.1, JP1B_INN.1]
  CH1_B_GJ:    [R1_BG.2, JP1_BG.1]
  CH1_B_V1:    [JP1_BG.2, R1_BV1.2, J1_BV1.1]
  CH1_B_OUT:   [R1_BF.1, JP1B_OUT.1, TP1_EB0.1]
```

`R1_BDIR` and `C1_BAC` are alternates in the same signal path: `R1_BDIR` fitted gives a
DC-coupled input, which is the default. To AC-couple instead, remove `R1_BDIR` and fit
`C1_BAC` and `R1_BBIAS`. Never fit both `R1_BDIR` and `C1_BAC`.

`J1_BSIG` shield connects to `AGND`. For the PD/Iq state, do **not** physically
disconnect the generator: leave it connected, set its ac/pulse amplitude to zero, and
set its dc level to `REF`. That keeps the DUT noninverting input normally biased while
there is no signal stimulus. If formal Figure 4005-1 conformity is later required, use
the Figure 4005-1 fixture rather than describing this Fixture-B adaptation as literal
Method-4005.1 compliance.

---

## 7 · Channel 1 — Fixture C · Open-loop gain, output swing

Mirrors MIL-STD-883-4 Figure 4004-3 **as stripped**: S1A, S1B, S2, S3 and both R3 are
deliberately absent. Do not add them back for this board revision. Three passages in the
standard support the hardwiring: Method 4004.2 §3.3 states explicitly that switches S1–S4
are closed for output-swing testing; Method 4003.2 §3 states that all switches are assumed
normally closed; and Method 4001.1 §3 states that for methods using the null loop circuit,
all switches (relays) are assumed normally closed. Figure 4004-3 is that null-loop circuit.
Method 4004.2 §3.1 itself does not restate switch states, so the basis there is the
general rule rather than a §3.1-specific sentence — accurate wording matters if this is
ever audited. `JP1_C` retains S4 so the loop can be opened during bring-up, but it is closed
for both retained measurements.

```yaml
components:
  - {ref: R1_C1A,   type: R,     value: "1k",     tol: "0.1%", fitted: true,  mil: "R1 inverting"}
  - {ref: R1_C1B,   type: R,     value: "1k",     tol: "0.1%", fitted: true,  mil: "R1 noninverting"}
  - {ref: R1_C2,    type: R,     value: "TBD-AD",              fitted: true,  mil: "R2"}
  - {ref: R1_CL,    type: R,     value: "TBD",                 fitted: true,  mil: "RL"}
  - {ref: R1_CVC,   type: R,     value: "0",                   fitted: true}
  - {ref: C1_CNULL, type: C,     value: "TBD",                 fitted: false}
  - {ref: U1_NULL,  type: OPAMP, value: "ZERO_DRIFT_RRIO_TBD", fitted: true,  mil: "NULL AMP"}
  - {ref: JP1_C,    type: JP,                                  fitted: true,  mil: "S4"}
  - {ref: JP1C_INN, type: JP,                                  fitted: true}
  - {ref: JP1C_INP, type: JP,                                  fitted: true}
  - {ref: JP1C_OUT, type: JP,                                  fitted: true}
  - {ref: J1_VC,    type: J1,    value: "VC",                  fitted: true,  mil: "VC"}
  - {ref: J1_V1C,   type: J1,    value: "V1",                  fitted: true,  mil: "V1"}
  - {ref: TP1_V2,   type: TP,                                  fitted: true,  mil: "V2"}
  - {ref: TP1_EC0,  type: TP,                                  fitted: true,  mil: "E0 loop output"}

nets:
  CH1_C_INN:     [R1_C1A.2, R1_C2.1, JP1C_INN.1]
  CH1_C_INP:     [R1_C1B.2, JP1C_INP.1]
  CH1_C_OUT:     [JP1C_OUT.1, R1_CL.1, U1_NULL.+, TP1_V2.1]
  CH1_V1TERM:    [R1_CL.2, J1_V1C.1]
  CH1_C_VCN:     [U1_NULL.-, R1_CVC.2, C1_CNULL.2]
  CH1_VCTERM:    [R1_CVC.1, J1_VC.1]
  CH1_C_NULLOUT: [U1_NULL.OUT, JP1_C.1, C1_CNULL.1, TP1_EC0.1]
  CH1_C_LOOP:    [JP1_C.2, R1_C2.2]
```

`U1_NULL` has **no local feedback**. Its feedback path runs out through `JP1_C` and
`R1_C2` into the DUT's inverting input, through the DUT, and back to `U1_NULL.+`. This
is a servo loop and it is correct as drawn. Do not "fix" it by adding a feedback
resistor around `U1_NULL`.

`R1_CVC` is fitted at 0 Ω and is the required dc connection from the VC terminal to
`U1_NULL.-`; it must not be DNP in the default build. `C1_CNULL` is DNP. Together the
two footprints reserve a compensation/integrator option: if the complete DUT + null-amp
servo loop is unstable, `R1_CVC` may be changed to a finite value and `C1_CNULL` may be
populated after analysis. With `JP1_C` open the null amplifier has no closed feedback
path, so its output may rail; that is expected and is not a bring-up failure by itself.

---

## 8 · Channel 1 — Fixture D · Output impedance (entire fixture DNP)

Mirrors MIL-STD-883-4 Figure 4005-1. **Every component on this sheet section is
`fitted: false`.** Place the symbols and preserve their DNP status. Leave footprint
fields empty in this schematic-capture pass; footprint sizing is a later layout decision.

```yaml
components:
  - {ref: R1_D1A,   type: R,  value: "TBD-AD",      fitted: false, mil: "R1 feedback"}
  - {ref: R1_D1B,   type: R,  value: "TBD-AD",      fitted: false, mil: "R1"}
  - {ref: C1_D1A,   type: C,  value: "TBD-AD",      fitted: false, mil: "C1 inverting"}
  - {ref: C1_D1B,   type: C,  value: "TBD-AD",      fitted: false, mil: "C1 noninverting"}
  - {ref: C1_D2,    type: C,  value: "TBD",         fitted: false, mil: "C2"}
  - {ref: R1_D2,    type: R,  value: "TBD",         fitted: false, mil: "R2 ~= nominal ZO"}
  - {ref: JP1D_INN, type: JP,                       fitted: false}
  - {ref: JP1D_INP, type: JP,                       fitted: false}
  - {ref: JP1D_OUT, type: JP,                       fitted: false}
  - {ref: J1_DSIG,  type: SMA, value: "GENERATOR",  fitted: false, mil: "V2"}
  - {ref: TP1_V0,   type: TP,                       fitted: false, mil: "V0"}

nets:
  CH1_D_INN: [R1_D1A.2, C1_D1A.1, JP1D_INN.1]
  CH1_D_INP: [R1_D1B.2, C1_D1B.1, JP1D_INP.1]
  CH1_D_OUT: [R1_D1A.1, C1_D2.1, JP1D_OUT.1, TP1_V0.1]
  CH1_D_INJ: [C1_D2.2, R1_D2.1]
  CH1_DSIG:  [R1_D2.2, J1_DSIG.1]
```

`J1_DSIG` shield connects to `AGND`. `JP1D_INN`, `JP1D_INP` and `JP1D_OUT` are also
DNP by default, but their footprints remain so Fixture D can be populated later without a
board revision.

`C1_D1A` and `C1_D1B` are sized by `2·π·f·R1·C1 ≥ 10·A_D`, which at A_D = 10⁵ demands
roughly 16 µF on a guarded input node. Whether this fixture is ever populated depends on
the simulated A_D. Choose footprints generous enough to accept a large film capacitor.

---

## 9 · Pin-48 open item (carry-forward note, not an action item here)

This block has no `DUT` symbol and does no chip-pin wiring — see §0 rules 7–8. This
note exists only so the open item travels with the design: per `Chip_pins.xlsx`, pin
48 carries the block label "OPAMP1" but is named `op2_inp`. Pins 48/49/50 group
cleanly as `op2_*`, so the block-name column appears to be a typographical error.
This spec's `op2_inp`/`op2_inn`/`op2_out` naming (§1a) assumes the signal names are
correct. Not resolved yet — flag it again if it surfaces during integration with the
master project's `DUT` symbol.

---

## 10 · Channel 2

Identical to §4–§8 with these substitutions, and no others:

| In channel 1 | In channel 2 |
|---|---|
| refdes prefix `R1_`, `C1_`, `SW1_`, `U1_`, `TP1_`, `J1_` | `R2_`, `C2_`, `SW2_`, `U2_`, `TP2_`, `J2_` |
| jumper prefix `JP1A_`, `JP1B_`, `JP1C_`, `JP1D_`, `JP1_` | `JP2A_`, `JP2B_`, `JP2C_`, `JP2D_`, `JP2_` |
| net prefix `CH1_` | `CH2_` |
| `OP1_INN`, `OP1_INP`, `OP1_OUT` | `OP2_INN`, `OP2_INP`, `OP2_OUT` |
| `op1_inn`, `op1_inp`, `op1_out` (hierarchical pins, §1a) | `op2_inn`, `op2_inp`, `op2_out` (hierarchical pins, §1a) |

Values, topology, fitted flags and net membership are all unchanged. `REF`, `AGND`,
and `AUX_5V` (§3) are internal to this block and shared by both channel sheets.

---

## 11 · Values blocked on external information

These are `TBD` on purpose. Emit them as literal strings and list them in your output
summary so they are visible.

| Component | Blocked on | Constraint once known |
|---|---|---|
| `R1_C2`, `R2_C2` | A_D from Cadence | Ratio to `R_C1A` sets resolution of the open-loop-gain reading |
| `R1_A2`/`R1_A1` ratio | A_D | Method 4001.1 requires min(100, 0.1 × A_D). Currently drawn at 100 |
| `R1_CL`, `R2_CL` | Acquisition document | MIL-STD-883-4 does not specify a load value |
| `C1_D1A`, `C1_D1B` | A_D | 2·π·f·R1·C1 ≥ 10·A_D |
| `R1_D2`, `R2_D2` | Nominal ZO | R2 ≈ ZO |
| `C1_D2`, `C2_D2` | Test frequency, R_D2 | C2 ≥ 10 / (2·π·f·R2) |
| `R1_A3A/B`, `R2_A3A/B` | DUT input impedance | 10 MΩ is provisional; Method 4001.1 requires R3 ≤ nominal input impedance |
| `R1_BG`, `R2_BG` | DUT gain/output-drive check | 10 Ω gives ≈101 noise gain with 1 kΩ feedback; confirm the DUT remains linear and the ratio is useful for the crossover sweep |
| `U_REF`, `U1_NULL`, `U2_NULL` | Part selection | Zero-drift, rail-to-rail input/output, 5 V supply; verify input/output range and stability in the actual loops |
| `C_REF2A` | U_REF stability analysis | 10 Ω isolation with `C_REF2B` fitted is the default; add the 10 µF once the U_REF part is selected and checked for capacitive-load stability |
| DUT footprint | Package confirmation | Blocks the carrier board entirely |

---

## 12 · What this spec does not cover

Out of scope for this pass, deliberately:

- Everything that lives in the master board project instead of this block: the `DUT`
  symbol, the chip carrier board, the main VAA bench connector and current-insertion
  jumper, the AGND/DGND tie point, the scan/control header, and the FPGA connector,
  level shifting, and Basys 3 interface that eventually drives that header.
- Every non-op-amp EDU1 block: IDACs, VDACs, ADC, instrumentation amplifiers,
  comparators, timers, LDOs, bandgap reference.
- PCB layout, placement, routing, stackup and net classes — except the guard-ring
  constraint in §5, which is recorded now so it is not lost.

---

## 13 · Provenance

Every fixture here is derived from MIL-STD-883-4, Part 4 (Electrical Tests, Linear),
Methods 4001.1, 4002.1, 4004.2 and 4005.1. Fixture B's PD/Iq state is explicitly an
EDU1 engineering adaptation of 4005.1 §3.1 rather than the Figure 4005-1 test figure. The `mil:` field on each component gives the
designator it carries in the source figure. Components with no `mil:` field are additions
required by this board — isolation jumpers, test points, links and the vaa/2 reference —
not part of the original figures.

Deviations from the figures, with the section-level justification for each, are recorded
in the companion document *EDU1 Op-Amp — Finalized Test Circuits*. An agent generating
this schematic does not need those reasons, but a human reviewing the output will.
