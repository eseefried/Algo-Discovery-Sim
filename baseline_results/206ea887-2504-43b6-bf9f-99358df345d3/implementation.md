# Equation to Qiskit

Implements the circuit-level unit of the trivial Grover-based APSP baseline: for one fixed entry (i,j) of a (min,+) squaring step and a classical threshold t, the circuit applies r Grover iterates G_t = Diffusion * O_t^{(i,j)} on an index register over intermediate vertices k plus one flag qubit. The threshold oracle marks k with D[i][k] + D[k][j] < t (eq_3), realized from the classical matrix data as multi-controlled X gates onto the flag qubit (phase kickback when the runner prepares the flag in |->); the diffusion operator 2|psi><psi| - I (eq_4) is realized with H, X and a multi-controlled Z. The classical outer loops (Durr-Hoyer threshold updates, repeated squaring) are out of circuit scope.

Source equation run: `f88d136e-ba6c-4d65-8b79-2136be4b06e5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: idx register (m = ceil(log2 4) = 2); qubit q holds bit q of the intermediate-vertex index k (qubit 0 = least significant bit, Qiskit little-endian)
- qubit 2: flag qubit (oracle output); runner should prepare it in |-> so the oracle acts as the phase oracle (-1)^{f_t(k)}
- example: candidates D[0][k]+D[k][3] = [INF, 6, 4, INF]; with threshold 5 only k=2 (|idx>=|10>, qubit1=1, qubit0=0) is marked; one Grover iterate on the uniform superposition over 4 indices maps it to the marked state

## Assumptions

- Non-edges are given as null or the string 'inf' and obey INF + x = INF, so such k are never marked.
- Edge weights are nonnegative; a null threshold means +infinity (every finite candidate is marked).
- If n is not a power of two, the index register is padded to 2^m basis states and padding indices are unmarked (eq_4 assumption); the uniform superposition prepared by the runner is then over all 2^m indices.
- mcx with up to 11 controls is considered a standard gate available for synthesis by Qiskit.
- Iteration count r is chosen by the user/runner (e.g. r=1 for exactly one marked index among four).

## Unresolved issues

- The paper's actual O(n^{2.5-eps}) algorithms for structured APSP variants are not reconstructable from the abstract and are not implemented.
- Success probability of a fixed-r Grover search depends on the number of marked indices M_t, which the runner must account for (exponential-search schedule) when using the circuit inside Durr-Hoyer minimum finding.

## Equation mapping

- `eq_1`: background; no code location. Definition of shortest-path distance; motivates the (min,+) squaring but is not itself a circuit operation.
- `eq_2`: background; no code location. The repeated (min,+) squaring is the classical outer loop; the circuit handles one entry (i,j) of one product. The candidate values D_ik + D_kj are evaluated classically in _marked_indices as input to the oracle, but the min and the squaring recursion are outside the circuit.
- `eq_3`: implemented; _marked_indices and _apply_oracle (comments '# eq_3'). Threshold oracle |k>|b> -> |k>|b xor f_t(k)> with f_t(k)=1 iff D_ik + D_kj < t, built from classical matrix data as multi-controlled X gates onto the flag qubit; padding indices unmarked.
- `eq_4`: implemented; _apply_diffusion and the iteration loop in build_circuit (comments '# eq_4'). Grover iterate G_t = (2|psi><psi| - I) O_t applied r = instance['iterations'] times; diffusion implemented up to global phase -1. The iteration count r is supplied by the instance rather than computed from the unknown M_t.
- `eq_5`: out_of_scope; no code location. Durr-Hoyer threshold-update loop, measurement and classical verification, and the O(n^{2.5}) cost accounting are classical/experimental control flow outside a single unitary operation.
- `eq_6`: out_of_scope; no code location. The paper's O(n^{2.5-eps}) algorithms are not described in the abstract and cannot be reconstructed.

## Specification changes

- eq_3: The oracle is realized directly from classical matrix data as a sum of multi-controlled X gates (one per marked index), instead of a reversible adder/comparator with QRAM access and ancilla uncomputation; the anc register of the specification is therefore empty. Reason: The matrix is a classical instance parameter, so the marked set can be computed classically; this gives an exact, ancilla-free realization of the same unitary on (idx, flag) within the 12-qubit cap.
- eq_4: Index encoding changed from big-endian to Qiskit little-endian: idx qubit q holds bit q of k. The diffusion operator is implemented up to a global phase of -1. The Grover iteration count r is an explicit instance parameter rather than derived from M_t or an exponential-search schedule. Reason: Qiskit qubit 0 is the least significant bit; global phase is unobservable; M_t is unknown in the algorithm and the random schedule is classical control flow outside a fixed unitary circuit.
- eq_4, eq_5: The circuit contains no preparation of |psi>|-> and no measurement; the runner prepares idx in the uniform superposition and flag in |-> and measures idx. Reason: Required operation-only contract (no state preparation or measurement in the generated circuit).
- eq_2, eq_5: Scope narrowed to a single Grover threshold search for one fixed entry (i,j) and one fixed threshold t of one (min,+) squaring step. Reason: The outer loops over entries, threshold updates, and squarings are classical and not a single unitary operation.
