# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a classically known 2^n x 2^m isometry V (V^dagger V = I), build a circuit on n qubits using single-qubit gates and CNOTs that, acting on |x>_m (x in 0..2^m-1) tensored with |0>^{n-m}, outputs V|x>, up to global phase, with few CNOTs. The scoped target is the column-by-column decomposition; the other schemes are only described.

Scope: Smallest instance: column-by-column decomposition for a generic isometry, e.g. m=1,n=2 (4x2 matrix, 2 columns, 2 qubits total) with Gray-code uniformly controlled Ry/Rz rotations. Out of scope: Knill/CSD recursion, qubit-by-qubit decomposition, numerical small-case optimizations, exact CNOT counts and constants of the paper, and the Stinespring channel/POVM extension (only sketched).

## Symbols

- $V$: isometry matrix of size 2^n x 2^m; domain: complex, V^dagger V = I_{2^m}
- $m,n$: input and output qubit counts; domain: integers, 0<=m<=n
- $v_k$: k-th column of V; domain: unit vector in C^{2^n}
- $G_k$: circuit (product of multiplexed rotations) for column k; domain: unitary on n qubits
- $N_{CNOT}$: CNOT count; domain: nonnegative integer

## eq_1: Isometry condition

$$
V^\dagger V = I_{2^m},\quad V|x\rangle_m = U\,(|x\rangle_m\otimes|0\rangle^{\otimes (n-m)})
$$

V is realized by a unitary U on n qubits acting on inputs with ancilla-like qubits set to zero (up to global phase); the unitary check compares the relevant columns.

Provenance: `abstract_inferred`. The definition of an isometry from m to n qubits and its embedding as a restriction of a unitary is standard.

Abstract evidence: decomposition of arbitrary isometries into a sequence of single-qubit and Controlled-not (C-not) gates

Equation assumptions:

- Input register holds the m low-order qubits; the other n-m qubits start in |0>.

## eq_2: Parameter-counting lower bound

$$
N_{CNOT}\gtrsim \tfrac14\left(2^{m+n+1}-2^{2m}\right)-O(\text{lower order})
$$

Heuristic bound from the real parameter count of V divided by about 4 parameters per CNOT with single-qubit gates; the exact lower-order terms are not recalled.

Provenance: `abstract_inferred`. The abstract states that a bound exists; the form is taken from the sketch's parameter counting, not the abstract.

Abstract evidence: We derive a theoretical lower bound on the number of C-not gates required to decompose an arbitrary isometry from $m$ to $n$ qubits

Equation assumptions:

- Constants are approximate and not verified against the paper.

## eq_3: Column-by-column reduction

$$
G_{2^m-1}\cdots G_1G_0\,V|x\rangle=|x\rangle\otimes|0\rangle^{\otimes(n-m)}\ \Rightarrow\ U=(G_{2^m-1}\cdots G_0)^\dagger
$$

G_k maps the current column k to the basis state |k>(x)|0..0> while fixing the previously fixed columns 0..k-1; the inverse of the product gives V.

Provenance: `assumption`. The abstract only says that three explicit decompositions exist; this is the sketch's chosen construction, with a generic form of the column-wise clearing.

Equation assumptions:

- G_k are built from uniformly controlled Ry and Rz rotations and a diagonal phase, with controls chosen so that earlier columns remain unchanged.

## eq_4: Uniformly controlled rotation

$$
M=\sum_{j}|j\rangle\langle j|\otimes R(\theta_j),\quad R\in\{R_y,R_z\}
$$

Multiplexed single-qubit rotation with 2^c control states; Gray-code form uses 2^c CNOTs and 2^c single-qubit rotations, with angles obtained by a Walsh-Hadamard transform of theta_j.

Provenance: `standard_background`. A standard result from multiplexor decompositions.

Equation assumptions:

- Gray-code ordering; adjacent CNOTs may be cancelled.

## eq_5: Leading CNOT scaling of the column scheme

$$
N_{CNOT}^{\text{col}}\approx 2^{m+n}
$$

Leading-order cost is about twice the lower bound, per the sketch.

Provenance: `abstract_inferred`. The abstract says the constructions are within about a factor of two of the bound; the 2^{m+n} figure is from the sketch.

Abstract evidence: achieve this bound up to a factor of about two in the leading order

Equation assumptions:

- Applies to leading order only.

## Registers

- q: n qubits; input qubits (m of them) plus n-m qubits initialised to |0>; the unitary U acts on all n qubits

## Initial state

|x>_m (x) |0>^{n-m}, with little-endian integer encoding (qubit i carries bit i of the column index)

## Classical postprocessing

Classical computation of the rotation angles from V, including the Walsh-Hadamard transform for multiplexor angles; no measurement. The check compares the first 2^m columns of the simulated unitary with V up to phase.

## Algorithm steps

1. Classically compute successive columns of V and, for each k, the angles that rotate the current column k to |k>(x)|0>, using the Givens-like cascade of multiplexed Ry/Rz on the target qubits, controlled by the lower qubits. (eq_3, eq_4)
2. Compile each multiplexor with the Gray-code CNOT/rotation pattern, then cancel adjacent CNOTs between consecutive multiplexors. (eq_4)
3. Invert the whole sequence to obtain U, whose restriction to the inputs with ancillas |0> equals V. Check against V with the unitary simulator, ignoring global phase. (eq_1, eq_3)
4. Compare the CNOT count with the bound. (eq_2, eq_5)

## Assumptions

- Gate set: arbitrary single-qubit gates plus CNOT with all-to-all connectivity.
- V is a classically known dense matrix, not an oracle.
- Global phase is ignored.
- Smallest instance m=1, n=2 chosen as the scope.
- Gray-code multiplexor implementation.

## Missing information

- Exact angle formulas and control ordering for the column clearing.
- Exact lower-bound constants and CNOT counts of the paper.
- Details of the CSD and qubit-by-qubit schemes.
- Numerical small-case optimizations.
- Stinespring channel and POVM construction are only sketched.
