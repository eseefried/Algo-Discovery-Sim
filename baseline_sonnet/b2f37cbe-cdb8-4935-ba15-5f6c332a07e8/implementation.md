# Equation to Qiskit

Builds t steps of a split-step 2D discrete-time quantum walk U = S D (I⊗C) on an L x L periodic lattice (L in {2,4,8}) with a 4-state Grover coin. Disorder is a diagonal site phase e^{i theta_x}, and S reflects on a user-given set of cut links. The circuit uses only standard gates (H, X, CZ, CX, MCX, MCP) and no dense unitaries. Initial state preparation, measurement and P_B(t) are left to the runner.

Source equation run: `29176df7-38bb-42ce-aeee-580e9426c8d3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: x position bits (LSB first), m=log2(L)
- qubits m..2m-1: y position bits (LSB first)
- qubits 2m..2m+1: coin bits c = q_2m + 2*q_(2m+1); 0=+x(right),1=-x(left),2=+y(up),3=-y(down)
- example L=4: x=q0,q1; y=q2,q3; coin=q4,q5 (6 qubits); basis index = x + L*y + L^2*c
- cut_links entry [x,y,0] cuts link (x,y)-(x+1,y); [x,y,1] cuts link (x,y)-(x,y+1); periodic wrap

## Assumptions

- Grover coin, periodic boundaries, reflecting cuts and phase disorder are proposed choices, not the paper's actual walk
- Direction coding is 0=+x, 1=-x, 2=+y, 3=-y, with the opposite direction c XOR 1
- Site index is x + L*y
- Disorder phases are given per site in row-major order of x + L*y

## Unresolved issues

- The paper's actual coin, shift, disorder model and cut geometry are not available
- The Floquet Hamiltonian realization and winding invariant are not specified
- The source A, target B and initial coin state must be prepared by the runner

## Equation mapping

- `eq_1`: implemented; build_circuit (loop over steps) with _coin. One step applies the coin on the coin register, then disorder, then shift, i.e. U = S D (I x C), repeated for each step.
- `eq_2`: implemented; _disorder. For each site, X gates on the zero bits followed by an MCP applies the phase e^{i theta_x} independently of the coin.
- `eq_3`: implemented; _cut_swaps and _shift. The plain shift is a controlled modular increment/decrement. It is preceded by swaps of |x,R> and |x+e,L> on each cut link, which makes the walker stay at its site with flipped direction.
- `eq_4`: implemented; build_circuit step loop. The circuit implements U^t. The initial state |A,c0> is prepared by the runner, and P_B(t) is obtained by measurement outside this module.
- `eq_5`: out_of_scope; no code location. The quasienergy eigenproblem and winding invariant are spectral analysis of U, not part of the circuit operation.

## Specification changes

- eq_1: The Grover coin is built as H H (flip of |00>) H H with an explicit global phase of pi per step, which equals 2|s><s|-I exactly. Reason: This realizes the 4x4 coin with standard gates and no dense unitary.
- eq_3: The reflecting shift is decomposed as S = S_plain times a product of basis-state swaps across the cut links. Cut links are supplied as [x,y,axis] entries with periodic boundaries. Reason: This is an equivalent permutation, and it is implementable with multi-controlled X gates.
- eq_1, eq_2, eq_3, eq_4: The scope is narrowed to L in {2,4,8}, 0..16 steps, and explicit disorder phases supplied in the instance (zeros if omitted). Reason: This keeps the circuit within 12 qubits and a bounded gate count, and removes random sampling from the module.
- eq_5: The Floquet quasienergy and winding invariant are not implemented. Reason: They are classical spectral analysis, and the abstract does not define the invariant.
