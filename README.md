# Algo-Discovery-Sim

**Can AI agents rebuild a quantum algorithm from a paper's abstract alone?**

We give an AI system only the abstract of a published quantum-computing paper. It has to
work out the mathematics, write a quantum circuit, and run it in a simulator, without ever
seeing the paper. We then compare its equations with the ones in the paper.

We use this to compare one strong AI agent against teams ("swarms") of cooperating agents
on the same 96 papers.

## How it works

```
 abstract ──▶ 1. math spec ──▶ 2. Qiskit code ──▶ 3. simulation ──▶ scored against the paper
              equations,        circuit built       Qiskit Aer         (the paper is only
              registers, steps  in a locked-down                        used for scoring)
                                Docker sandbox
```

1. **Math spec.** An agent (or a team of agents) turns the abstract into a structured
   specification: equations in LaTeX, qubit registers, algorithm steps, and assumptions.
   Every equation is labelled with where it came from: stated in the abstract, inferred
   from it, textbook background, or an assumption.
2. **Code.** A shared code stage turns the spec into a Qiskit circuit. Generated code only
   ever runs inside an isolated Docker container with no network or file access.
3. **Simulation.** The circuit is simulated with Qiskit Aer.
4. **Scoring.** The spec's equations are compared with the paper's own key equations,
   adjusted for chance (0 = no better than comparing against an unrelated paper).

Steps 2-4 are identical for every system, so differences in the results come from step 1.

## Results

Four systems, 96 papers, scored on the 84 papers all four completed:

| System | Math score | Paper equations recovered | Circuits that ran | Cost |
|---|---|---|---|---|
| Single agent, Claude Fable 5.1 | **0.23** | **78 / 320** | 70 / 96 | $77 |
| Single agent, Claude Sonnet 5.5 | 0.18 | 54 / 320 | 77 / 96 | **$7.50** |
| Ledger swarm, Sonnet 5.5 | 0.11 | 26 / 320 | 48 / 96 | $14 |
| Abstract2Method swarm, Sonnet 5.5 | 0.17 | 46 / 320 | **93 / 96** | $62 |

- **One strong agent recovered the most mathematics.** On the same model, a single Sonnet
  agent matched the best swarm's math score at about an eighth of the cost.
- **The Abstract2Method swarm produced the most working circuits.** It tests its own specs
  by building them and keeps the ones that run, so this advantage is partly by design.
- **How a swarm is organised matters.** The Abstract2Method swarm clearly beat the ledger
  swarm on the same model, mainly by exploring several methods per paper.

**Caveats.** The math score measures how closely the equations match the paper's notation
and structure, not whether the mathematics is equivalent. "Ran" means the circuit built and
simulated, not that it is correct: there is no ground-truth circuit for most papers. Each
system was run once, and the systems did not have equal budgets.

## The systems

| System | What it is | Docs |
|---|---|---|
| **Single agent** | One model call writes the spec. | [Pipeline reference](docs/pipeline.md) |
| **Ledger swarm** | Three workers split one paper's spec into parts and bid for them through a shared ledger. | [Ledger swarm](docs/ledger-swarm.md) |
| **Abstract2Method (a2m)** | A swarm of agents that propose, implement, test and critique methods under an economic survival game. It also includes its own benchmark of 7 hand-built tasks with hidden tests. | [Abstract2Method](docs/SWARM.md), [architecture](docs/ARCHITECTURE.md) |

Experimental: running the swarms on a locally served model, see
[docs/nemotron-swarm.md](docs/nemotron-swarm.md).

## Quickstart

Requires Python 3.12+, [uv](https://docs.astral.sh/uv/) and Docker.

```bash
uv sync
docker build -t algo-discovery-qiskit:local runtime   # the sandbox that runs generated code
cp .env.example .env                                   # then set CLAUDE_HACKATHON_API
```

Try it on one paper:

```bash
# Single agent: abstract -> math spec -> circuit -> simulation
uv run run-pipeline --arxiv-id 1411.5949

# The Abstract2Method swarm writing the spec instead
uv run a2m-spec --arxiv-id 1411.5949 --out a2m_demo
```

Run a whole benchmark (resumable; results are scored automatically at the end):

```bash
PAPERS_FROM=single_agent_specs scripts/run_baseline.sh my_results 4   # single agent
scripts/run_a2m_batch.sh single_agent_specs my_a2m_results 3          # a2m swarm
```

Tests make no paid model calls: `uv run pytest`.

## Repository layout

```
src/algo_discovery/   single-agent pipeline, code stage, simulation, scoring, ledger swarm
src/a2m/              Abstract2Method swarm and its benchmark
data/                 300 arXiv quantum-algorithm papers (abstracts, full text, equations)
evaluation/           hand-labelled key equations for the 96 benchmark papers
scripts/              batch runners
runtime/              the Docker sandbox for generated code
docs/                 detailed documentation
baseline_results/  baseline_sonnet/  swarm_full/  a2m_full/   results of the runs above
```

The paper dataset is described in [data/circuit_dataset_300_v1/README.md](data/circuit_dataset_300_v1/README.md).
Agents only ever see the abstracts; full texts and equations are used for scoring.
