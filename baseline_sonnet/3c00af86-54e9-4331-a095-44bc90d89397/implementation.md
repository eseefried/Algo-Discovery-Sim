# Equation to Qiskit

Narrowed construction: Lie-Trotter-sliced simulation of a qubit semigroup e^{tL} with L = gamma*D[sigma_-] + kappa*(Z.Z - id), each slice realised as an exact Stinespring dilation using fresh ancillas. Amplitude damping uses a controlled-Ry and a CNOT. Dephasing uses an Ry and a CZ. This is not the paper's algorithm.

Source equation run: `47dc35a4-7181-46a1-9b7c-2b48b8ad0a35`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system S (input state rho, computational basis |0>,|1>; sigma_- maps |1> to |0>)
- qubits 1+2k (k=0..r-1): fresh ancilla for amplitude-damping dilation of slice k, input |0>
- qubits 2+2k (k=0..r-1): fresh ancilla for dephasing dilation of slice k, input |0>
- output channel: trace out all ancillas (qubits 1..2r)

## Assumptions

- Amplitude damping is L_a(rho)=gamma(s- rho s+ - 1/2{s+ s-,rho}) with s-=|0><1|.
- Dephasing is L_d(rho)=kappa(Z rho Z - rho).
- The runner prepares the system in qubit 0 and all ancillas in |0>, and traces out the ancillas to obtain the channel output.
- Time slices are equal, with s = t/r.

## Unresolved issues

- The paper's actual decomposition of L, its recombination rule and its channel-approximation circuits are not reconstructed.
- The single-ancilla property is not achieved.
- The gate-count scaling O((||L|| t)^{3/2}/epsilon^{1/2}) is not implemented.
- The error norm for epsilon remains unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit: gate parameters theta_a, theta_p derived from gamma, kappa, t. The target semigroup channel is implemented for one explicit Lindbladian (amplitude damping plus dephasing), not for an arbitrary L.
- `eq_2`: out_of_scope; no code location. Asymptotic gate-count scaling of the paper is not reproduced. This circuit uses 4r gates (3r for the slice dilations plus one CNOT/CZ pair), with no relation to the stated bound.
- `eq_3`: out_of_scope; no code location. The accuracy requirement is a property to be checked externally. The two generator pieces commute, so the sliced product equals e^{tL} exactly, and no epsilon parameter is used.
- `eq_4`: implemented; build_circuit: loop over k in range(r) with s = t/r. Semigroup slicing into r equal slices and a product over the generator pieces (L = L_a + L_d).
- `eq_5`: implemented; build_circuit: cry+cx (damping) and ry+cz (dephasing) per slice. Stinespring dilations of each elementary channel with one ancilla qubit per elementary channel, ancilla initial state |0>.

## Specification changes

- eq_1, eq_4: Narrowed from an arbitrary qubit generator L to a fixed two-term family: amplitude damping with rate gamma plus Z-dephasing with rate kappa. The decomposition is L = L_a + L_d. Reason: The paper's decomposition and recombination rule for general L is not given in the specification.
- eq_5: Uses a fresh ancilla per elementary channel per slice (2r ancillas in total) instead of a single reused ancilla. Total qubits are capped at 12, so r <= 5. Reason: Reset and dynamic circuits are disallowed, so a single ancilla cannot be reused across slices. This departs from the paper's single-ancilla claim.
- eq_2, eq_3: No gate-count optimality or epsilon-driven slice-count selection. r is a user parameter. The Trotter error is zero because L_a and L_d commute. Reason: The paper's channel approximation method and the error norm are unspecified.
