# Qatalyst visualization data

A snapshot of completed papers from the real Nemotron + Sonnet hybrid swarm.
Start with paper **0710.3196**, selected candidate **c003**, for the Grover demo.
Choose a run with `deaths > 0` in runs.csv to show actual culling and replacement.

- **runs.csv**: run selector, outcomes, spending, population and artifact links.
- **agents.csv**: clickable lobsters, parent links, birth/death times, final energy,
  last recorded activity/candidate and recorded failure context.
- **events.csv**: chronological replay, action details and code/evidence links.
- **candidates.csv**: method cards, complete review feedback, instances and outputs.
- **probabilities.csv**: histogram rows, keyed by candidate and simulation case.

Join agents and events on `agent_key`, and candidates on `candidate_key`.
Agent IDs reset for each paper, so use the global keys, not bare a01/a02 IDs.
Playback uses `elapsed_seconds`, with `sequence` breaking ties. All times are
seconds since that paper run began; ticks are logical rounds, not seconds.
Events without an agent key are run/candidate-level events; do not attribute them
to a lobster. Nested data is JSON inside correctly quoted CSV cells.

All artifact paths are relative to this directory. Host or copy the entire export
folder to preserve click-through links. Python uses build_circuit(instance);
compiled.qasm is also provided where saved. Raw equations live in artifacts/*/*/native/.
Original events and summaries are retained alongside generated code and validation.

`alive` means alive when that run ended, not currently running. Culling means
virtual-energy depletion, not necessarily a process crash. Failure context and
last activity describe recorded history, not an independently proven cause.
Energy is the saved final balance; per-event energy balances were not recorded.
Replacement agents need not have a donor parent when no successful donor exists.
Simulation probabilities are exact saved outputs, not invented shot counts.
Some saved simulation previews are truncated: these are flagged in candidates.csv
and excluded from probabilities.csv, while their original text is preserved.
Successful execution and model review are recorded separately and do not certify
full-paper reproduction. No unfinished run is included in this snapshot.

Candidate/code links show saved final snapshots for that candidate; event details
preserve the recorded activity at that moment. Repeated implementation attempts
may have intermediate artifacts in blackbox/, but not every event records an
exact intermediate code ID.
