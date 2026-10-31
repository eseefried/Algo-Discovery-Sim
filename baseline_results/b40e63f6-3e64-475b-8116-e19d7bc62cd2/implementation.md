# Equation to Qiskit

Implements the T-step QPA evolution U(theta)^T of eq_3/eq_4 as a unitary circuit: a 2-level coin qubit mixed by C(theta)=Rx(-2*theta) followed by a coin-conditioned cyclic shift (+1 for coin |0>, -1 for coin |1>) on a periodic n-site ring embedded in m=ceil(log2 n) position qubits. The mod-n shift is built from an mcx incrementer mod 2^m followed by a controlled transposition |n><->|0>, which makes the n used sites a closed cycle while unused basis states permute among themselves. Input-state preparation (eq_2), position measurement/partition decision (eq_5), the majority target (eq_1) and the GA fitness (eq_6) are classical or runner-side and are not part of the returned operation.

Source equation run: `f737f24c-52e8-447c-b643-1c313803dcbd`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Total 4 qubits for the example (n_sites=5 -> m=3 position qubits + 1 coin qubit).
- qubits 0,1,2: position register 'pos'; site j in {0,...,4} is the computational basis state |j> with qubit 0 the least significant bit (j = q0 + 2*q1 + 4*q2). Basis states |5>,|6>,|7> are unused and only permuted among themselves by the shift.
- qubit 3: coin register 'coin'; |0>_c shifts +1 (mod n), |1>_c shifts -1 (mod n). Runner should prepare it in |0> per eq_2.
- Input state (eq_2) and position measurement/partition (eq_5) are prepared/performed by the runner, not by build_circuit.

## Assumptions

- The QPA step is the one-parameter coined-walk form of eq_3 (an assumption of the math stage; the actual operator of reference [12] / the GA-found unitaries may differ).
- Periodic boundary conditions (indices mod n) with coin |0> moving +1 and coin |1> moving -1.
- Coin is applied before the shift within each step, matching U = S (I x C).
- n_sites may be any integer >= 2 with ceil(log2 n)+1 <= 12 qubits; n=5 is the paper's case.
- theta is any finite real; the small/large theta mass interpretation is not enforced.

## Unresolved issues

- The exact QPA definition, input encoding, number of steps, and the GA-found unitaries/partitions are unknown, so this operator is a plausible stand-in, not a reproduction of the paper's solution.
- Whether the partition in the paper is over positions only or over position-and-coin basis states is unknown; the circuit is agnostic since it returns only the evolution.

## Equation mapping

- `eq_1`: background; no code location. Classical majority target M(x); used only for evaluation/fitness, not part of the unitary operation.
- `eq_2`: out_of_scope; no code location. Initial particle state |psi_0(x)> is input-state preparation, which the runner performs; the module returns only the evolution operator.
- `eq_3`: implemented; _qpa_step (coin C(theta) as rx(-2*theta)) and _controlled_shift_plus / its inverse (coin-conditioned periodic shift S). One step U(theta) = S (I x C(theta)): coin mixing then +1/-1 cyclic shift on the n-site ring with exact mod-n wrap via incrementer plus controlled transposition |n><->|0>.
- `eq_4`: implemented; build_circuit, loop 'for _ in range(steps)' (comment '# eq_4'). U(theta)^T realized by repeating the step circuit T=steps times.
- `eq_5`: out_of_scope; no code location. Position measurement, marginalization over the coin, and the boundary-partition decision are measurement/classical post-processing outside the returned operation.
- `eq_6`: background; no code location. GA fitness over inputs is a classical outer loop, not a circuit element.

## Specification changes

- eq_3: The n-site ring is embedded in m=ceil(log2 n) qubits (n=5 -> 3 qubits); the shift acts as the exact cyclic shift mod n on basis states 0..n-1 and as an arbitrary (closed) permutation on the 2^m-n unused basis states. Reason: Qiskit registers are qubit-based; a 5-level qudit must be embedded. The used subspace is invariant, so dynamics on valid inputs are unchanged.
- eq_3: Tensor order fixed as position on qubits 0..m-1 (little-endian) and coin on qubit m, i.e. the state |j> x |c> corresponds to integer j + 2^m * c. Reason: The specification's |j> x |c> notation does not fix a physical qubit ordering; an explicit layout is required.
- eq_3: C(theta) is realized as the standard gate Rx(-2*theta), which equals [[cos t, i sin t],[i sin t, cos t]] exactly. Reason: Expressing the coin in terms of a standard gate; no change of meaning.
- eq_4: steps (T) is an instance parameter required to be >= 1; the example uses T=5. Reason: T is unspecified in the source; T=0 (identity) is rejected as a degenerate operation.
- eq_2, eq_5, eq_1, eq_6: Narrowed scope to the evolution operator only; encoding, measurement, partition decision and GA fitness are excluded. Reason: Task requires an operation without state preparation, measurement, or classical post-processing.
