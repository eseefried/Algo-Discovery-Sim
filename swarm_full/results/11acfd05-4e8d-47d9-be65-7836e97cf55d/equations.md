# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantum approximate optimization (QAOA) for combinatorial optimization with an integer depth parameter p>=1; approximation quality improves with p. Studied on MaxCut for regular graphs, with analysis for 2-regular and 3-regular graphs at fixed p. For p=1 on 3-regular graphs the cut is at least 0.6924 times the optimum.

Scope: Small finite instance: MaxCut on a regular graph (e.g. 3-regular) at p=1. Only the abstract-level structure is reconstructed; the explicit gate forms, angle optimization and the 0.6924 derivation are not given in the abstract.

## Symbols

- $p$: number of algorithm layers (circuit depth parameter); domain: integer p>=1
- $C(z)$: objective function, a sum over constraints; domain: z in {+1,-1}^n
- $\gamma,\beta$: variational angles of the p layers; domain: real vectors of length p
- $|\gamma,\beta\rangle$: parameterized quantum state prepared by the circuit; domain: n-qubit Hilbert space

## eq_1: Objective as sum of clauses

$$
C(z)=\sum_{\alpha=1}^{m} C_\alpha(z)
$$

Objective function is a sum over m constraints, each of limited locality.

Provenance: `abstract_inferred`. The abstract refers to the objective's locality and a number of constraints; the sum form is inferred.

Abstract evidence: the number of constraints

Equation assumptions:

- Each C_alpha acts on a bounded number of bits

## eq_2: Depth scaling

$$
\text{depth}=O(p\,m)
$$

Circuit depth grows linearly with p times at worst the number of constraints m.

Provenance: `abstract_explicit`. Direct statement in the abstract.

Abstract evidence: The depth of the circuit grows linearly with $p$ times (at worst) the number of constraints.

## eq_3: Approximation ratio at p=1

$$
\frac{C_{\text{found}}}{C_{\max}}\ge 0.6924
$$

For p=1 on 3-regular graphs the found cut is at least 0.6924 of the optimum.

Provenance: `abstract_explicit`. Direct statement in the abstract.

Abstract evidence: For $p=1$, on 3-regular graphs the quantum algorithm always finds a cut that is at least 0.6924 times the size of the optimal cut.

## eq_4: Variational state

$$
|\gamma,\beta\rangle=\prod_{l=p}^{1}e^{-i\beta_l B}e^{-i\gamma_l C}|+\rangle^{\otimes n}
$$

Standard QAOA state with phase-separation and mixing layers; the form is not stated in the abstract.

Provenance: `standard_background`. Standard QAOA form, assumed to match the paper's algorithm.

Equation assumptions:

- B=sum_j X_j mixer
- Initial state is uniform superposition

## Registers

- q: n (one qubit per graph vertex) qubits; Computational register encoding the bit string z; the cut is read from it

## Initial state

Uniform superposition |+>^{\otimes n} (assumed standard QAOA initial state)

## Measurement

Measure all n qubits in the computational (Z) basis to obtain a bit string z; repeat preparation and measurement many times to estimate <C> and to sample candidate cuts.

## Classical postprocessing

Evaluate C(z) classically for each sampled string and keep the best cut. For fixed p, angles (gamma,beta) are chosen by classical preprocessing/optimization of <gamma,beta|C|gamma,beta> (procedure not given in abstract).

## Algorithm steps

1. Prepare |+>^{\otimes n} by applying Hadamard to each qubit. (eq_4)
2. For each layer l=1..p, apply phase-separation unitary e^{-i gamma_l C}, a product of gates of locality at most that of each clause (two-qubit ZZ phases per edge for MaxCut). (eq_1, eq_4)
3. In each layer apply the mixing unitary e^{-i beta_l B} with single-qubit X rotations on all qubits. (eq_4)
4. Total depth scales as O(p m) with m constraints; for p=1 on 3-regular graphs the target guarantee is ratio >=0.6924. (eq_2, eq_3)

## Assumptions

- The state form in eq_4 is standard QAOA background, not taken from the abstract.
- Registers, initial state and mixer are assumed standard QAOA choices.
- Measurement in the computational basis with best-of-samples postprocessing is assumed standard QAOA practice.

## Missing information

- Explicit gate definitions
- Angle optimization procedure
- Derivation of the 0.6924 bound
- Number of measurement repetitions
- Audit note: abstract states only that the cut found is at least 0.6924 of optimal, not how it is guaranteed (expectation vs. sampled outcome).
- Whether the 0.6924 guarantee refers to expected value or sampled outcomes
