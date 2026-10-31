---
domain: biology
eval_timeout_s: 120
role_bias: {hypothesize: 1.1, implement: 1.0, simulate: 1.0, critique: 1.3}
colony_genome: {min_families: 3, max_attempts: 3, critiques_required: 1}
roles:
  hypothesize: propose how to spend a limited measurement budget across rounds
  implement: write the per-round proposal function
  simulate: run the trusted oracle over the rounds
  critique: look for budget violations, invalid sequences, duplicate spend, and collapse to a
    single region of sequence space
libraries: [sklearn, scipy, numpy, math, cmath, time, itertools, functools, collections,
            heapq, random, fractions, statistics, typing, dataclasses]
tools:
  - module: rna
    sandbox: false
    skills: []
backends:
  - NVIDIA BioNeMo NIM (ESM-2 style embeddings) as a source of sequence features, when
    A2M_BIONEMO_URL is set
---

# Biology

## Summary
Rebuild a sequence design method: propose batches of sequences to a hidden measurement oracle
over several rounds and drive the measured fitness up.

## Conventions
- Sequences are strings over a fixed alphabet and a fixed length; anything else is discarded
  from your batch.
- The oracle is hidden and the only way to learn anything about it is to spend measurements,
  which are strictly budgeted. This is the expensive step a real campaign is judged on, and it
  is why this domain ships no tool into the sandbox: the measuring code stays in the runner.
- You are called once per round and given every measurement so far, so any state you want must
  be recomputed from that history.
- Fitness is normalized so that about 1.0 is the best achievable.
