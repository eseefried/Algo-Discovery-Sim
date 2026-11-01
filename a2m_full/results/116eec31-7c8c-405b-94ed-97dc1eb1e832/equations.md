# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate Rz(theta) to operator-norm error epsilon (up to global phase) by a single-qubit Pauli+V circuit, using quaternion lattice enumeration with a sum-of-two-squares solve in place of a grid search. The abstract states only that the Ross-Selinger deterministic-search technique is adapted to Pauli+V with simple geometric methods; every equation below is background or an assumption.

Scope: One tiny instance: single qubit, no black box, theta=pi/5 (assumed), epsilon about 0.3, small k (at most 3). Enumerate integer quaternions of norm 5^k near the target, reduce them to a V-word, and build the circuit. Outside scope: the paper's actual search algorithm, its proofs, its optimality and depth bounds, and any asymptotic claims.

## Symbols

- $\theta$: target z-rotation angle; domain: real
- $\epsilon$: target approximation error; domain: positive real
- $k$: level, i.e. denominator exponent (word length); domain: nonnegative integer
- $a,b,c,d$: integer quaternion coordinates; domain: integers
- $q$: quaternion a+bi+cj+dk; domain: integer quaternions
- $U_q$: SU(2) matrix of q/5^{k/2}; domain: 2x2 unitary

## eq_1: Quaternion to unitary

$$
U_q=\frac{1}{5^{k/2}}\left(a I - i(b X + c Y + d Z)\right),\quad a^2+b^2+c^2+d^2=5^k
$$

A unit quaternion with denominator 5^{k/2} is a single-qubit SU(2) matrix. The coordinate-to-Pauli assignment is a convention; V=(I+2iX)/sqrt5 corresponds to 1+2i at k=1 (with sign convention -i X).

Provenance: `assumption`. Standard quaternion-SU(2) correspondence. The sketch assumes the V gates are of this type.

Equation assumptions:

- Sign and axis convention fixed here; the Pauli-conjugated V gates are the 1+-2i, 1+-2j, 1+-2k types

## eq_2: Target rotation

$$
R_z(\theta)=\cos(\theta/2)I-i\sin(\theta/2)Z
$$

The target corresponds to the quaternion direction (cos(theta/2),0,0,sin(theta/2)), with the Z coefficient being d.

Provenance: `standard_background`. Definition of Rz.

## eq_3: Slab region

$$
\left|a-5^{k/2}\cos\tfrac\theta2\right|,\ \left|d-5^{k/2}\sin\tfrac\theta2\right|\lesssim \epsilon 5^{k/2},\quad |b|,|c|\lesssim \epsilon 5^{k/2}
$$

Enumeration region in Z^4 for a level-k candidate. The sketch's sqrt(epsilon) bound on b,c is not a derived or established bound. Use the direct condition below as the actual acceptance test.

Provenance: `assumption`. Heuristic region. The actual acceptance test is the operator-norm distance computed by simulation.

Equation assumptions:

- Region bounds heuristic only; the final check is the explicit distance

## eq_4: Two-squares residue

$$
b^2+c^2=5^k-a^2-d^2
$$

For each candidate (a,d) in the sector, solve for (b,c). The residue is representable as a sum of two squares iff every prime p=3 mod 4 divides it to an even power. Solve via Gaussian-integer factorization, which is brute force at tiny sizes.

Provenance: `standard_background`. Classical number theory. The sketch's norm-equation approach is a proposal.

Equation assumptions:

- Brute-force search over b,c is acceptable at small k

## eq_5: Approximation criterion

$$
\min_{\phi}\|U_q-e^{i\phi}R_z(\theta)\|_{op}\le\epsilon
$$

Verification in operator norm up to global phase. It is equivalent to a threshold on |Tr(R_z^\dagger U_q)|, i.e. |a cos(theta/2)+d sin(theta/2)|/5^{k/2}.

Provenance: `assumption`. Error metric chosen in the sketch assumptions.

Equation assumptions:

- Global phase ignored

## Registers

- q: 1 qubits; single data qubit

## Initial state

|0>

## Classical postprocessing

Classical enumeration, two-squares solve, quaternion factoring and word reduction as in the steps. Verify distance by simulating the unitary.

## Algorithm steps

1. Pick theta and epsilon. For k=0,1,2,... enumerate integer (a,d) with a^2+d^2<=5^k in the sector near 5^{k/2}(cos(theta/2),sin(theta/2)). (eq_2, eq_3)
2. For each (a,d), solve b^2+c^2=5^k-a^2-d^2 (when nonneg and representable). Accept the first candidate meeting the error criterion, taking k minimal. (eq_4, eq_5)
3. Reduce the quaternion to a word. Primitive reduction: if q is divisible by none of the 5 divisors (not divisible by an ideal above 5 beyond Pauli), peel off V-type factors (1+-2i, 1+-2j, 1+-2k) one at a time (by trial division in Hurwitz/Lipschitz quaternions) to get a length-k word, plus a Pauli (unit) factor. Alternative for tiny k: brute-force search over all reduced words of length k and compare to the target. (eq_1)
4. Build the single-qubit circuit by applying the V-word gates as unitary gates (e.g. from rx/rz/h compositions or U gates with the computed matrices) and Pauli gates (x,y,z). The gate order is the reverse of the matrix product order. No measurement; the statevector or unitary is read. (eq_1)

## Assumptions

- The scope instance (theta, epsilon, k) is my choice
- Unique reduced word via unique factorization is assumed. In Lipschitz/Hurwitz quaternions factorization is unique only up to units, so Pauli factors must be tracked
- Implement V as exact Qiskit gates built from rx(-2*atan(2))-type rotations: V=(I+2iX)/sqrt5=Rx(-2 arctan 2). Pauli-conjugates are Ry and Rz of the same angle, and the inverses are the opposite angles
- The expected depth about 3 log_5(1/epsilon) is an unverified heuristic from the sketch

## Missing information

- The paper's actual deterministic search procedure and its guarantees
- Exact depth and T-count-analogue bounds
- Precise slab region and enumeration order
- Handling of divisibility by 5 and the canonical normal form of words
