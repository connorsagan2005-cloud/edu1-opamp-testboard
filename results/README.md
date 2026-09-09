# results

Owner: whole team. Status: empty for now.

Measured characterization data, organized to become the source for the EDU1 datasheet.

Suggested layout: `results/<block>/<parameter>/<date>/` holding raw instrument dumps,
a reduced CSV, and the plot(s). Each block folder should end up with a summary table
(measured min / typ / max, conditions) that maps directly onto a datasheet section.

Keep large binary instrument captures out of git if they get heavy — link to the
shared drive and commit the reduced data + plots.
