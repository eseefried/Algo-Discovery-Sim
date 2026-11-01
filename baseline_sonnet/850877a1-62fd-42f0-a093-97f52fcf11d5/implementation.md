# Equation to Qiskit

Qiskit construction of the quantum order-finding (phase-estimation) operation for a given N and coprime a. For each counting qubit k it applies a controlled multiplication by a^(2^k) mod N on the work register. The controlled multiplication is built from standard multi-controlled X gates (cycle decomposition of the permutation), with no dense unitaries. An inverse QFTGate then acts on the counting register. Hadamards on the counting register and preparing the work register in |1> are left to the runner. Classical post-processing (continued fractions, gcds, odd-order square-coprime logic) is out of scope.

Source equation run: `ab7d21ea-c2a3-4661-ba0e-e65c7cb6ebd6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: counting register 'count', little-endian (qubit k controls multiplication by a^(2^k) mod N); after the inverse QFT it holds y with y/2^n ≈ s/r
- qubits n..n+m-1: work register 'work', m=ceil(log2 N), little-endian encoding of an integer in [0,2^m); the runner should prepare |1> (qubit n = 1)
- for the example N=15, a=4, n=5: count = qubits 0-4, work = qubits 5-8

## Assumptions

- The runner prepares the counting register in a uniform superposition (Hadamards) and the work register in |1>.
- Little-endian bit order is used in both registers, consistent with Qiskit and QFTGate.
- N must be at least 3 and a must satisfy 1<a<N with gcd(a,N)=1; N need not be checked for compositeness.
- Controlled multiplications by a^(2^k) mod N that equal 1 are skipped, since they are the identity.
- The multiplication by c is implemented as a permutation decomposed into transpositions, each realized with multi-controlled X gates and X conjugations.

## Unresolved issues

- The circuit is not optimized: multi-controlled X gate count grows quickly with m, which is acceptable only for tiny instances.
- The paper's odd-order retrieval and new-relation techniques are not reconstructed and are not included.
- With the 12-qubit cap, the default n=ceil(log2 N^2) is only feasible for small N (up to 15).

## Equation mapping

- `eq_1`: background; no code location. Order definition; it is the quantity encoded in the eigenphases of U_a but is not computed in the circuit.
- `eq_2`: out_of_scope; no code location. Classical gcd factor extraction from even r; not part of a unitary circuit.
- `eq_3`: out_of_scope; no code location. Classical odd-order/square-coprime gcd relation; the paper's odd-order techniques are not reconstructed.
- `eq_4`: implemented; build_circuit (loop over counting qubits calling _controlled_mult, then QFTGate(n).inverse()). Controlled modular exponentiation (controlled |y> -> |a^(2^k) y mod N>) followed by the QFT on the counting register, giving the phase-estimation peaks y/2^n ≈ s/r. The inverse QFT sign convention is used (see specification_changes).
- `eq_5`: out_of_scope; no code location. Classical continued-fraction post-processing of the measured y.

## Specification changes

- eq_4: Apply the inverse QFT (QFTGate(n).inverse()) to the counting register instead of a literal +2*pi*i*x*y/2^n forward QFT. Reason: With U|u_s>=exp(2*pi*i*s/r)|u_s> the inverse QFT gives y/2^n ≈ s/r, matching the step list ('apply inverse QFT'). The literal + sign of eq_4 would peak at y/2^n ≈ -s/r mod 1, which is the same up to relabeling s->r-s, so r is recovered equally.
- eq_4: The circuit contains only controlled modular multiplications and the inverse QFT. Hadamards on the counting register and the work-register preparation |1> are omitted. Reason: The task requires the circuit to be an operation with the input state prepared by the runner.
- eq_1, eq_2, eq_3, eq_5: Scope narrowed to the quantum order-finding unitary. Classical order verification, gcd steps, odd-order handling and the paper's two techniques are not implemented. Reason: They are classical post-processing or are not specified in the abstract.
- eq_4: Controlled modular multiplication acts as the identity on work basis states y>=N, and the work register uses m=ceil(log2 N) qubits, with the counting size n allowed to be overridden. The default is the smallest n with 2^n>=N^2. Reason: This gives a well-defined unitary permutation on the full register. The 12-qubit cap means N=15 is the largest default-n case, and larger N needs a smaller explicit n.
