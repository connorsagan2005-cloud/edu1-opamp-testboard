# Standards & datasheet templates index

**Do not commit copyrighted standard or datasheet PDFs to this repo.** This file is the
only thing that lives in `docs/standards/` — it links each block to the standard(s) and
commercial datasheet(s) used as its test-procedure template. Keep local PDF copies
outside git (shared drive, course materials).

| Block | Template standard(s) / datasheet(s) | Notes |
|---|---|---|
| Op-amp | MIL-STD-883 Method 4001-series (op-amp electrical test methods: input offset voltage & drift, bias/offset current, CMRR, PSRR, open-loop gain, slew rate) | Fixtures A–F in the block spec are EDU1 adaptations of these methods, not literal figure conformity. Also referenced: commercial zero-drift RRIO op-amp datasheets for the support/reference amplifier structure. |
| Comparator | TODO — standards research not finalized. Shares an unclocked-comparator input stage with the op-amp; output is digital, so timing/propagation-delay methods will differ from the op-amp analog methods. |  |
| Bandgap reference | TODO — no block-specific IEEE/JEDEC standard found. Fallback: MIL-STD-883 4001-series offset/drift methodology + datasheet-driven structure (initial accuracy, tempco / box method, line regulation, noise, start-up). |  |
| LDO | TODO — standards research not finalized. Expect datasheet-driven structure (line/load regulation, dropout, PSRR, load-transient, quiescent current, thermal). Team now has temperature-chamber access for tempco sweeps. |  |

General references to cite where used (link, don't embed):

- **MIL-STD-883** test methods — https://landandmaritimeapps.dla.mil/Programs/MilSpec/ListDocs.aspx?BasicDoc=MIL-STD-883
- **IEEE Std 181** (standard on transitions, pulses, and related waveforms) — https://standards.ieee.org/ieee/181/3492/
- **IEEE Std 1241** (terminology and test methods for ADCs) — https://standards.ieee.org/ieee/1241/3062/  *(next-term ADC scope)*
