# test-scripts

Owner: TBD. Status: not started.

Bench automation, data capture, and per-block analysis scripts (instrument control,
sweep drivers, data reduction, plot generation). Organize by block
(`opamp/`, `comparator/`, `bandgap-ref/`, `ldo/`). Raw and reduced measurement data
goes in [`results/`](../results/), not here.

Python: use a `.venv/` (git-ignored); pin dependencies in a `requirements.txt` per
subfolder or at this level.
