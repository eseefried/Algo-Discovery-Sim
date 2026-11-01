# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Exact synthesis of a single-qubit unitary U over the Clifford-cyclotomic gate set (Clifford + Rz(pi/n), n even), returning a gate word with the minimum number of pi/n z-rotations, and then building that word as a one-qubit circuit.

Scope: Tiny instance: n=4 (Clifford+T), one qubit, U given by explicit entries in Z[e^{i pi/4},1/2]. The classical synthesis output is a word in H,S,X,Rz(pi/n), which is built as a 1-qubit circuit with no ancilla, no measurement and no black box. Outside scope: the proof that the ring characterization fails for 100% of even n, the exact height-drop bound for general n, and the optimality proof for general n.

## Symbols

- $n$: even positive integer defining the rotation angle pi/n; domain: even integers >= 2; n=4 in scope
- $\zeta_{2n}$: primitive 2n-th root of unity e^{i pi/n}; domain: complex
- $U$: target single-qubit unitary with entries u_{ij}; domain: 2x2 unitary
- $\sigma_k$: Galois conjugation zeta_{2n} -> zeta_{2n}^k, k coprime to 2n; domain: k in (Z/2nZ)^*
- $h(U)$: heuristic height proxy of the first column of U (log-norm of |u|^2 denominators); a candidate quantity, not the paper's definition; domain: nonnegative integers
- $R$: candidate move C1 Rz(pi/n) C2 with C1, C2 single-qubit Cliffords; domain: finite set
- $m$: number of pi/n rotations in the output word; domain: nonnegative integers

## eq_1: Rotation gate

$$
R_z(\pi/n)=\mathrm{diag}(e^{-i\pi/2n},e^{i\pi/2n})
$$

Standard Qiskit rz convention; for n=4 it equals T up to global phase.

Provenance: `standard_background`. Standard gate definition. The abstract only names a z-rotation by pi/n; the exact convention is assumed.

Equation assumptions:

- Global phase is ignored in comparison

## eq_2: Ring characterization

$$
\text{for } n=4:\; U\in\langle \mathrm{Clifford},T\rangle \iff U\in U_2(\mathbb{Z}[e^{i\pi/n},1/2])
$$

Exactly synthesizable unitaries equal unitaries over the ring for n=4. The abstract says it fails for most even n.

Provenance: `abstract_inferred`. Direct reading of the abstract claim for n=4.

Abstract evidence: For the Clifford+T case $n=4$ the group of exactly synthesizable unitaries was shown to be equal to the group of unitaries with entries over the ring $\mathbb{Z}[e^{i\frac{\pi}{n}},1/2]$.

Equation assumptions:

- Phase factors absorbed in the ring

## eq_3: Column unitarity in every conjugate

$$
\sum_{i}\sigma_k(u_{ij})\,\overline{\sigma_k(u_{ij})}=1\quad\forall k,j
$$

Unitarity is preserved under Galois embeddings, since the identity is algebraic over the field.

Provenance: `standard_background`. Follows from U^dagger U = I holding in the field, with complex conjugation commuting with the Galois action in an abelian CM field. This is the sketch's step 1, not abstract-sourced.

Equation assumptions:

- Entries in the cyclotomic field

## eq_4: Height proxy (assumed)

$$
h(U)=\max_{k}\;\log_2\!\big|\sigma_k(2^{d})\big|\ \text{with }d=\min\{d:\,2^{d}|u_{00}|^2,\,2^{d}|u_{10}|^2\in\mathbb{Z}[\zeta_{2n}]\}
$$

Least denominator exponent of the first column, used as a T-count proxy. Equals 0 iff the column is Clifford-like (monomial) in the intended setting.

Provenance: `assumption`. The sketch proposes a least-denominator exponent from a norm. The exact definition is not in the abstract, so this is a placeholder.

Equation assumptions:

- For n=4 this reduces to the known sde-based T-count

## eq_5: Greedy descent step

$$
U_{t+1}=R_t^{-1}U_t,\; R_t=\arg\min_{R\in\mathcal{R}}h(R^{-1}U_t),\;\; U_m\in\mathrm{Clifford},\; U=R_1\cdots R_m\,U_m
$$

Pick the Clifford-conjugated rotation that lowers the height, and iterate until the residual is Clifford. m is the number of rotations.

Provenance: `assumption`. The abstract claims an efficient algorithm that is optimal in rotation count. The greedy form with meet-in-the-middle search comes from the sketch and is not confirmed.

Equation assumptions:

- Height drops by a bounded amount per rotation
- The greedy choice attains the bound

## Registers

- q: 1 qubits; Single data qubit carrying the synthesized word; no ancilla

## Initial state

|0> on q; the circuit is compared via its unitary or statevector to U up to global phase

## Classical postprocessing

Classical synthesis search gives the gate word. The word is compared to U up to global phase. Rotation count m is reported.

## Algorithm steps

1. Fix n (n=4 in scope) and the explicit target U with cyclotomic entries; check unitarity and ring membership. (eq_2, eq_3)
2. Compute the height of the first column and enumerate the finite set of moves C1 Rz(pi/n) C2 over Clifford coset representatives. (eq_1, eq_4)
3. Greedily apply the height-lowering move, record it, and repeat until the height is 0. Fail if no move lowers the height (non-synthesizable). (eq_5)
4. Fix the final Clifford residual by matching it to one of the 24 Clifford classes up to phase, and emit the word in h,s,x,rz gates in time order. Reverse the order of the recorded product when building, since the product is written right-to-left. (eq_5)

## Assumptions

- Smallest useful construction: n=4, one qubit, explicit U
- Gate set is H, S, X, Rz(pi/n)
- Search over Clifford cosets is finite, 24 classes up to phase
- The Galois-norm height is a valid lower bound on m, taken from the sketch and unverified

## Missing information

- Exact definition of the height and of the per-rotation drop for general n
- The paper's actual algorithm; the abstract gives no equations for it
- Criterion for exact synthesizability for n other than 4
- Explicit target instances
