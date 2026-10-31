# Equation to Qiskit

Scoped construction: a qDRIFT-style randomized Trotter circuit for fast-signal-assisted adiabatic evolution on an EC3 (3-bit exact cover) instance. At each step j the Hamiltonian H(t_j)=(1-s)H0+s*HP+H_sig(t_j) is split into Pauli terms. One term is sampled with probability proportional to |coefficient|, and exp(-i*sign*lambda*T/N*P) is applied. Driving, cost and signal terms are therefore implemented in the same randomized sequence. The sampling uses a seeded NumPy RNG at build time, so the returned circuit is fixed, bound and unitary. Input-state preparation (|+>^n) and measurement are left to the runner.

Source equation run: `5ae21b37-bf93-47ad-95a5-0615d4b94f35`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit i (0..n-1) encodes EC3 bit b_i; qiskit index 0 is the least significant bit
- Computational encoding: Z=+1 (|0>) means b_i=0, Z=-1 (|1>) means b_i=1
- Intended input prepared by the runner: |+>^n, the ground state of H0=-sum X_i
- Single register 'q' of n qubits; no ancillas; n<=12

## Assumptions

- Linear schedule s(t)=t/T, evaluated at step midpoints
- H0=-sum_i X_i; the intended input is |+>^n, prepared externally
- Bit b=1 corresponds to Z=-1 (b=(1-Z)/2)
- The signal is a uniform Z field with per-step sign (alternating or random)
- One random Pauli term is sampled per step, with probabilities proportional to |coefficient|
- Randomness is reproducible through the integer seed in the instance
- Clauses are triples of distinct bit indices; there is no trapped-ion pulse-level compilation

## Unresolved issues

- The paper's actual randomized Trotter formula and signal waveforms are not specified in the abstract
- The EC3 instance used in the paper (clauses and qubit count) is unknown
- qDRIFT-style sampling with few steps gives a stochastic approximation; accuracy depends on steps and seed
- The trapped-ion implementation is out of scope and not modeled
- Measurement and success-probability postprocessing are left to the runner

## Equation mapping

- `eq_1`: implemented; _step_terms (X driving terms weighted by 1-s, EC3 Z/ZZ cost terms weighted by s) and the midpoint schedule s=(j+0.5)/steps in build_circuit. Linear interpolation (1-s)H0+s*HP with H0=-sum X_i and HP the EC3 clause Hamiltonian written in Pauli form (constant dropped). The schedule is discretized at step midpoints.
- `eq_2`: implemented; _step_terms signal block (sig*Z_i terms) and the sign sequence sg in build_circuit. The signal Hamiltonian is added as extra Pauli terms in the same term list. It is H_sig = amp*sg_j*sum_i Z_i, where sg_j alternates (regular) or is a random +/-1 (random) at each step. The abstract does not give this form, so it is an assumption.
- `eq_3`: implemented; Sampling loop in build_circuit (rng.choice with probs, then rx/rz/rzz with angle 2*sign*lam*T/steps). The schematic placeholder is replaced by a concrete randomized product formula in the style of qDRIFT. One term is sampled per step with p_k=|c_k|/lambda and exp(-i*sign(c_k)*lambda*T/N*P_k) is applied. Driving and signal terms are sampled from the same list, so they are implemented together.

## Specification changes

- eq_3: Replaced the schematic product of exp(-i p_k h_k dt/p_k) by the qDRIFT-style single-term random sampling with weights |c_k|/lambda and rotation angle lambda*T/N per step. Reason: The placeholder formula was not concrete (p_k cancels), and the paper's actual randomized Trotter formula is not given in the abstract.
- eq_1: Specified the final Hamiltonian as the EC3 clause sum HP=sum (b_i+b_j+b_k-1)^2, expanded as const - (Zi+Zj+Zk)/2 + (ZiZj+ZiZk+ZjZk)/2. The clauses are an instance parameter. Reason: The spec left the EC3 clauses and qubit count unspecified; a concrete Hamiltonian was needed to build the circuit.
- eq_2: Chose the signal form H_sig = amp * sg_j * sum_i Z_i, with sg_j = +/-1 either alternating or seeded-random per step. Reason: The spec says the signal form is unspecified; this is a minimal choice covering the 'regular' and 'random' cases.
- eq_1, eq_2, eq_3: Scope narrowed to the unitary evolution only: no |+>^n preparation, no measurement and no postprocessing. The random sampling is performed at circuit-build time with a seed, so the output circuit is one fixed realization. The schedule is evaluated at step midpoints (not a continuous s(t)). Reason: Required by the operation-only circuit contract, which prohibits state preparation, measurement and dynamic circuits.
