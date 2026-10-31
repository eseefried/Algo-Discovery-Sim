# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Identify an unknown affine Boolean function f:{0,1}^n -> {0,1}, f(x) = a·x ⊕ b, i.e. recover both the linear coefficient vector a and the affine offset b, using quantum oracle queries. The abstract claims the standard one-query Bernstein-Vazirani algorithm identifies a linear (b=0) function with certainty, that affine functions need exactly one additional query (two-query algorithm) to identify b with certainty, and that for incompletely defined functions both algorithms become bounded-error procedures with success probability at least 2/3.

Scope: Scoped to the two-query algorithm for a completely specified affine Boolean function f(x) = a·x ⊕ b on n qubits, with a tiny explicit instance n = 2, a = (a_1,a_0) = (1,0), b = 1, so f(x_1 x_0) = x_1 ⊕ 1. The first query is the standard Bernstein-Vazirani circuit (recovers a exactly; the offset b appears only as an unobservable global phase (-1)^b). The second query is reconstructed as a single evaluation of the oracle at a known point (x = 0^n) to read b; the paper's actual second-query circuit is not given in the abstract. Outside scope: the paper's definition and classes of incompletely defined linear/affine Boolean functions, the specific bounded-error adaptations, and the proof that the 2/3 success bound holds.

## Symbols

- $n$: number of input bits of the Boolean function; domain: positive integer (instance: n = 2)
- $x$: input bit string, written x = x_{n-1} ... x_1 x_0 with x_0 the least significant bit, stored on input register qubits q_{n-1},...,q_0; domain: \{0,1\}^n
- $a$: unknown linear coefficient vector of the affine function; domain: \{0,1\}^n (instance: a = (1,0), i.e. a_1 = 1, a_0 = 0)
- $b$: unknown affine offset (constant term); domain: \{0,1\} (instance: b = 1)
- $a \cdot x$: inner product modulo 2, \bigoplus_{i=0}^{n-1} a_i x_i; domain: \{0,1\}
- $f$: the provided Boolean function (affine in scope; linear when b = 0); domain: f : \{0,1\}^n \to \{0,1\}
- $U_f$: standard bit-flip oracle for f acting on input register and one ancilla qubit; domain: unitary on 2^{n+1}-dimensional Hilbert space
- $|-\rangle$: ancilla state (|0\rangle - |1\rangle)/\sqrt{2}; domain: single-qubit state
- $H^{\otimes n}$: Hadamard transform on all n input qubits; domain: unitary on 2^n-dimensional space
- $p_{succ}$: probability that the algorithm outputs the correct identification; domain: [0,1]

## eq_1: Affine Boolean function

$$
f(x) = a \cdot x \oplus b = \Big(\bigoplus_{i=0}^{n-1} a_i x_i\Big) \oplus b, \qquad a \in \{0,1\}^n,\ b \in \{0,1\}
$$

Definition of the affine Boolean function to be identified; the linear case is b = 0. The instance is f(x_1 x_0) = x_1 \oplus 1.

Provenance: `abstract_inferred`. The abstract speaks of linear and affine Boolean functions; the standard meaning of an affine Boolean function is a linear function (inner product mod 2) plus a constant, and 'identifying the affinity' is read as determining b.

Abstract evidence: if the provided Boolean function is affine, then one more query to the oracle (the two-query algorithm) is required to identify the affinity of the function

Equation assumptions:

- 'Affine Boolean function' is taken in the standard sense a·x ⊕ b over GF(2).

## eq_2: Bit-flip oracle and phase-kickback form

$$
U_f |x\rangle |y\rangle = |x\rangle |y \oplus f(x)\rangle, \qquad U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle
$$

Standard oracle model; with the ancilla in |-> the function value appears as a phase.

Provenance: `standard_background`. Standard query model used by the Bernstein-Vazirani algorithm; the abstract does not specify the oracle model, so the usual one is assumed.

Equation assumptions:

- Oracle is the standard reversible bit-flip oracle for f.

## eq_3: First query (Bernstein-Vazirani) output state

$$
\big(H^{\otimes n} \otimes I\big) U_f \big(H^{\otimes n} \otimes I\big) |0^n\rangle |-\rangle = (-1)^{b} |a\rangle |-\rangle
$$

Exact equality: for affine f the one-query circuit returns the coefficient vector a deterministically; the offset b contributes only an unobservable global phase, so one query cannot identify b.

Provenance: `standard_background`. Follows from eq_1 and eq_2: the amplitude of |z> is 2^{-n} \sum_x (-1)^{a\cdot x \oplus b \oplus z\cdot x} = (-1)^b \delta_{z,a}. This recalls the known Bernstein-Vazirani analysis; the abstract only states the algorithm identifies a linear function with one query with certainty.

Equation assumptions:

- f is completely specified (defined on all 2^n inputs) and exactly affine.

## eq_4: Second query: read the affine offset

$$
U_f |0^n\rangle |0\rangle = |0^n\rangle |f(0^n)\rangle = |0^n\rangle |b\rangle
$$

One further oracle query at the all-zero input (ancilla initialised to |0>) places b in the ancilla, which is then measured; more generally b = f(x_0) \oplus a\cdot x_0 for any known query point x_0.

Provenance: `assumption`. The abstract states that exactly one more query suffices to identify the affinity with certainty but does not give the circuit; querying at a known point and measuring the ancilla is the simplest construction achieving this and is proposed here, not sourced from the paper.

Equation assumptions:

- The paper's actual second-query circuit may differ from this reconstruction.

## eq_5: Bounded-error success guarantee for incompletely defined functions

$$
p_{succ} \geq \tfrac{2}{3}
$$

For the paper's (unspecified) classes of incompletely defined linear and affine Boolean functions, the one-query and two-query algorithms respectively identify the function with probability at least 2/3.

Provenance: `abstract_explicit`. Directly stated in the abstract; the definition of 'incompletely defined', the classes, and how the bound is derived are not available.

Abstract evidence: identify certain classes of incompletely defined linear and affine Boolean functions respectively with probability of success at least $2/3$

Equation assumptions:

- The precise function classes and the modified algorithms are not reconstructable from the abstract.

## Registers

- input: n (instance: 2) qubits; Holds the query input x = x_{n-1}...x_0 (qubit q_i holds bit x_i); after the first query it holds the coefficient vector a.
- ancilla: 1 qubits; Oracle target qubit: prepared in |-> for the first (phase-kickback) query and in |0> for the second (bit-readout) query.

## Initial state

|0^n\rangle_{input} |1\rangle_{ancilla}, then Hadamard on every qubit gives |+\rangle^{\otimes n} |-\rangle (instance: n = 2).

## Measurement

First query: computational-basis measurement of all n input qubits; the outcome string is a exactly (deterministic for completely specified affine f). Second query: computational-basis measurement of the ancilla qubit; the outcome is b. For the incompletely defined case the abstract only guarantees success probability at least 2/3 (eq_5), with repetition/majority details unspecified.

## Classical postprocessing

Output the pair (a, b) and report f(x) = a·x ⊕ b. If the second query is made at a general known point x_0 instead of 0^n, compute b = f(x_0) ⊕ a·x_0 using the a obtained from the first query. Instance check: a = (1,0), b = 1 gives f(x_1 x_0) = x_1 ⊕ 1.

## Algorithm steps

1. Prepare input register in |0^n> and ancilla in |1>; apply H to all n+1 qubits, yielding |+>^{⊗n}|->. (eq_2)
2. First oracle query: apply U_f; by phase kickback the state becomes 2^{-n/2} \sum_x (-1)^{a·x ⊕ b}|x>|->. (eq_1, eq_2)
3. Apply H^{⊗n} to the input register; the state is exactly (-1)^b |a>|->. Measure the input register in the computational basis to obtain a with certainty (instance: outcome a = 10, i.e. a_1 = 1, a_0 = 0). (eq_3)
4. Second oracle query (reconstructed): reset the input register to |0^n> and the ancilla to |0>, apply U_f, and measure the ancilla to obtain f(0^n) = b with certainty (instance: b = 1). (eq_4)

## Assumptions

- No experiment scope was provided; the two-query algorithm for a completely specified affine function with instance n = 2, a = (1,0), b = 1 was chosen as the smallest useful construction.
- Affine Boolean function means f(x) = a·x ⊕ b over GF(2); 'identifying the affinity' means determining b.
- Standard bit-flip oracle U_f|x>|y> = |x>|y ⊕ f(x)> is assumed as the query model.
- The second query is reconstructed as an evaluation of f at a known point (x = 0^n) read out in the ancilla; this is a proposed construction, not sourced from the paper.
- Register ordering: input qubit q_i holds bit x_i with x_0 the least significant bit; a is read out in the same ordering.

## Missing information

- The paper's definition of 'incompletely defined' Boolean functions (e.g. functions specified only on a care set) and the 'certain classes' for which the 2/3 bound holds.
- How the one-query and two-query algorithms are adapted or analysed as bounded-error algorithms, and the derivation of the 2/3 success bound.
- The exact form of the paper's second query (query point, ancilla preparation, any interference-based readout) and its proof of certainty.
- Any proof that one query is insufficient to determine b (the abstract asserts one more query 'is required').
