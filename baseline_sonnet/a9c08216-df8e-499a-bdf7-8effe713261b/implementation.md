# Equation to Qiskit

Qiskit operation approximating exp(-iHt) for continuous-time quantum-walk spatial search on the complete graph K_N with N=2^n, H = -gamma*L - |w><w|, L = N(I-|s><s|). It uses second-order (Strang) Trotterization of the |s><s| and |w><w| terms, each a multi-controlled phase, with the -gamma*N*I term as a global phase. No state preparation or measurement. The Lanczos reduction is background only and is not coded.

Source equation run: `f597a24b-ac39-40bd-a708-dcc73f1584fd`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form the vertex register 'v'; qubit q is bit q of the vertex label (qubit 0 = least significant).
- Vertex x in 0..2^n-1 is the computational basis state |x>; N=2^n. Example: n=3 uses qubits 0,1,2 and marked vertex 5 = |101>.
- No ancilla qubits.

## Assumptions

- Complete graph K_N without broken links, with marked vertex w given by the integer 'marked'.
- gamma is supplied by the instance. The example uses gamma=1/N, the usual critical value for complete-graph search.
- The runner prepares the initial state, typically uniform |s>. The circuit applies the evolution to any input.
- The global phase exp(i*gamma*N*t) is kept as the circuit global phase.

## Unresolved issues

- The paper's exact Hamiltonian, optimal gamma, and optimal time are not given in the abstract.
- Trotter error is not bounded or checked here. Validation happens downstream.
- Results for broken-link graphs, bipartite and star graphs, transport efficiency, and the XY spin network are not reconstructed.

## Equation mapping

- `eq_1`: background; no code location. Lanczos recursion is the method used to find the invariant subspace. The circuit does not run it, because the full-space operator is applied via Trotter steps.
- `eq_2`: background; no code location. Reduced-subspace dynamics c(t)=exp(-iTt)e_0 is classical background. The circuit approximates the same evolution in the full 2^n space and does not use a reduced basis.
- `eq_3`: implemented; build_circuit with _phase_on_uniform and _phase_on_marked. H = -gamma*N*I + gamma*N|s><s| - |w><w|. The identity term is a global phase, |s><s| is H^n-conjugated multi-controlled phase, and |w><w| is X-conjugated multi-controlled phase. Evolution uses a second-order Trotter product.
- `eq_4`: background; no code location. The 2D reduced matrix is flagged in the spec as schematic and unverified. It is not implemented, though the dynamics from |s> do lie in span{|s>,|w>}.

## Specification changes

- eq_3: The garbled L expression is read as L = N*I - J = N(I - |s><s|), where J is the all-ones matrix. The vertex count is restricted to N=2^n, with n up to 12. Reason: Qubit encoding needs a power-of-two vertex count, and the Laplacian text in the spec was malformed.
- eq_3, eq_2: Exact exp(-iHt) is replaced by a Strang-split Trotter approximation with a user-set number of steps. The error shrinks as steps grows. Reason: |s><s| and |w><w| do not commute, and the exact evolution would need an opaque dense unitary or a Lanczos-derived basis rotation, which are not allowed.
- eq_1, eq_2, eq_4: Lanczos and the reduced 2D subspace are excluded from the circuit. Broken-link graphs, bipartite and star graphs, transport efficiency, and the XY spin-network bound are also excluded. Reason: The spec lacks explicit Hamiltonians and definitions for these. The equations are classical background or unverified.
