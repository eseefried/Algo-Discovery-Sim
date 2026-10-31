# Equation to Qiskit

Qiskit module implementing the scoped construction: a second-order (Strang) Trotter-Suzuki approximation of exp(-i H_N t) for the discretized 1D quantum harmonic oscillator H_N = (X^2 + P^2)/2 on an n-qubit position register (N = 2^n Fourier-grid points, Delta x = sqrt(2 pi/N), x_j = (j - N/2) Delta x). Each of the r steps is exp(-i X^2 delta/4) F_c^dag exp(-i X^2 delta/2) F_c exp(-i X^2 delta/4) with delta = t/r. The diagonal quadratic phases are realized exactly by single-qubit phase gates, pairwise controlled-phase gates and a global phase; the centered DFT F_c is realized exactly as e^{i pi N/2} Z_0 . QFTGate(n) . Z_0. An optional flag adds the global phase e^{i t/2} that turns the evolution into the fractional Fourier transform of angle t. The operation contains no state preparation or measurements.

Source equation run: `168416ba-f57b-4911-a0ac-be58ef6cbdf5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'pos': 3 qubits (indices 0,1,2) for the example instance; N = 8 grid points.
- Qubit index a holds bit of weight 2^a of the grid label j (Qiskit little-endian: index 0 is the least significant bit).
- Grid position encoded by |j> is x_j = (j - N/2) * sqrt(2*pi/N); for N = 8, x_j = (j - 4) * sqrt(pi/4).
- Momentum representation reached through F_c = e^{i pi N/2} Z_0 QFT Z_0 uses the same register and the same bit convention for the momentum label k.

## Assumptions

- Units hbar = m = omega = 1 and the symmetric Fourier grid with Delta x = sqrt(2 pi / N), x_j = (j - N/2) Delta x, as in the specification.
- Momentum is defined as P = F_c^dag X F_c; the alternative sign convention P = F_c X F_c^dag gives the same P^2 and hence the same circuit.
- The time t may be any finite real (including 0 or negative); r is a positive integer up to 4096; n between 1 and 12.
- QFTGate(n) implements |j> -> N^{-1/2} sum_k exp(2 pi i jk/N)|k> on the given index order with index 0 the least significant bit, as stated in the task description.
- The runner prepares the input state (e.g. the discretized Gaussian) and performs any measurement; the module only returns the evolution operation.

## Unresolved issues

- The paper's refined Lie-algebraic Trotter error bound and the resulting step schedule achieving O(exp(gamma sqrt(log(N/epsilon)))) are not reconstructed; the generic second-order bound governs the choice of r here.
- For n = 1 (N = 2) the centered-grid construction is degenerate (positions +-sqrt(pi)) and the global phase e^{i pi N/2} = -1 is nontrivial; the circuit is still a valid unitary but has little physical meaning.
- No simulation or verification has been performed; correctness of the phase decompositions relies on the algebraic identities stated in the docstrings.

## Equation mapping

- `eq_1`: background; no code location. Defines the continuum QHO Hamiltonian H = (x^2 + p^2)/2 and the sl(2,R) commutator closure that motivates the paper's refined Trotter analysis. The splitting into X^2 and P^2 terms is what the circuit implements, but the commutation relations themselves are not used in the code and the refined bound is not reconstructed.
- `eq_2`: implemented; _apply_quadratic_phase (grid constants dx^2 = 2 pi/N, x_j = (j - N/2) dx) and _apply_centered_qft (F_c = e^{i pi N/2} Z_0 QFT Z_0, so P = F_c^dag X F_c). The discretized position operator enters through the quadratic phases and the momentum operator is obtained by conjugating with the centered DFT realized exactly via QFTGate and Z gates.
- `eq_3`: implemented; build_circuit (loop over r Trotter steps; comment 'eq_3: symmetric Strang step'). Each step applies e^{-iX^2 d/4}, F_c, e^{-iX^2 d/2}, F_c^dag, e^{-iX^2 d/4} with d = t/r, repeated r times. The error bound part of eq_3 is analytical and not represented in code.
- `eq_4`: implemented; _apply_quadratic_phase. Exact decomposition of exp(-i theta dx^2 (j - N/2)^2) into n single-qubit p gates, n(n-1)/2 cp gates and a global phase using (j - N/2)^2 = sum_a j_a(4^a - N 2^a) + sum_{a<b} j_a j_b 2^{a+b+1} + N^2/4.
- `eq_5`: out_of_scope; no code location. The subpolynomial complexity bound O(exp(gamma sqrt(log(N/epsilon)))) is an analytical result about the paper's refined step schedule; the module uses a user-supplied step count r and does not implement or claim that scaling.
- `eq_6`: implemented; build_circuit, optional include_frft_phase flag (comment 'eq_6'). When include_frft_phase is true the global phase e^{i t/2} is added so the circuit approximates the fractional Fourier transform of angle alpha = t; for t = pi/2 this approximates the ordinary (continuum) Fourier transform on bounded-energy states.

## Specification changes

- eq_2: Bit labeling of the grid index j changed from the specification's big-endian description j = sum_l j_l 2^{n-1-l} to Qiskit's little-endian convention: qubit index a carries the bit of weight 2^a. Reason: Qiskit qubit 0 is the least significant bit and QFTGate(n) follows this convention; the operator meaning (grid label j in 0..N-1) is unchanged, only the physical qubit assignment is fixed.
- eq_2: The centered DFT F_c is realized as e^{i pi N/2} Z_0 . QFTGate(n) . Z_0 (and F_c^dag as e^{-i pi N/2} Z_0 . QFTGate(n).inverse() . Z_0), including the exact global phase e^{i pi N/2} via circuit.global_phase. Reason: Exact algebraic identity (j - N/2)(k - N/2) = jk - N(j+k)/2 + N^2/4 and (-1)^j = (-1)^{j_0}; the specification only stated 'up to a global phase', the code tracks the phase exactly.
- eq_4: The constant term -theta dx^2 N^2/4 of the quadratic phase is included as a global phase rather than dropped. Reason: Keeps the implemented unitary exactly equal to exp(-i theta X^2) so that the composed circuit equals the product formula of eq_3 as an operator, not only up to phase.
- eq_3: Scope narrowed to the operation only: initial Gaussian state preparation, computational-basis measurement, and classical comparison described in the specification are not part of the module; the instance parameters n, t, r are user-supplied with caps n <= 12 and r <= 4096. Reason: Task requires a measurement-free unitary operation with the input prepared by the runner, a 12-qubit cap, and rejection of invalid parameters.
- eq_6: The fractional-Fourier global phase e^{i t/2} is made optional (instance flag include_frft_phase, default false). Reason: The primary scoped operation is the Hamiltonian evolution exp(-i H_N t); the phase is a trivial global factor relevant only when interpreting the circuit as a fractional Fourier transform.
- eq_3: Adjacent e^{-iX^2 d/4} factors between consecutive Trotter steps are not merged. Reason: Keeps the circuit a literal transcription of the r-fold symmetric product; merging would be an equivalent optimization but obscures the one-to-one mapping to eq_3.
