# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Bounded-occurrence Max E3LIN2: given n boolean variables x_1..x_n and m linear equations over GF(2), each of the form x_a + x_b + x_c = b_e (mod 2) on exactly three distinct variables, with every variable appearing in at most D equations, find an assignment maximizing the number of satisfied equations. The abstract claims that level-one (p=1) QAOA achieves an expected satisfied fraction of at least 1/2 + 1/(101 D^{1/2} ln D) in the worst case and 1/2 + 1/(2 sqrt(3e) D^{1/2}) in the typical case, versus 1/2 for a uniformly random string.

Scope: Scope (chosen by the agent, no experiment_scope supplied): the level-one QAOA circuit for a single explicit Max E3LIN2 instance encoded as a diagonal Ising-type cost operator with three-body Z terms, a transverse-field mixer, computational-basis measurement, and classical evaluation of the satisfied-equation count. Tiny instance: n=4 variables, m=2 equations, D=2. Outside scope: the paper's analytic lower bounds on the p=1 expectation (the 1/(101 D^{1/2} ln D) and 1/(2 sqrt(3e) D^{1/2}) constants), the specific (gamma, beta) choices used in the proofs, the definition of the 'typical case' ensemble, the local-neighborhood argument, and the comparison to classical algorithms [5,6]. These results are recorded as claims, not reconstructed.

## Symbols

- $n$: number of boolean variables (and qubits); domain: positive integer
- $m$: number of equations (clauses); domain: positive integer
- $D$: maximum number of equations any single variable appears in (bounded occurrence); domain: positive integer, D \ge 2 for the stated bounds to be meaningful (\ln D > 0)
- $x_j$: boolean value of variable j; qubit j in computational basis state |x_j\rangle; domain: \{0,1\}, j=1,\dots,n
- $e=(a_e,b_e,c_e)$: index triple of the three distinct variables in equation e; domain: e=1,\dots,m; 1\le a_e<b_e<c_e\le n
- $d_e$: sign of equation e: d_e=(-1)^{r_e} where r_e \in \{0,1\} is the required parity (right-hand side) of equation e; domain: \{+1,-1\}
- $C(x)$: classical cost: number of equations satisfied by assignment x; domain: \{0,1,\dots,m\}
- $C$: diagonal cost operator with C|x\rangle = C(x)|x\rangle; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $B$: transverse-field mixer operator; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $\gamma,\beta$: level-one QAOA angles for the cost and mixer unitaries; domain: \gamma\in[0,2\pi), \beta\in[0,\pi)
- $Z_j, X_j$: Pauli Z and X acting on qubit j; domain: operators on qubit j
- $F_1(\gamma,\beta)$: expected number of satisfied equations in the p=1 QAOA state; domain: real, 0\le F_1\le m

## eq_1: Max E3LIN2 classical objective

$$
C(x)=\sum_{e=1}^{m}\mathbf{1}\left[x_{a_e}\oplus x_{b_e}\oplus x_{c_e}=r_e\right]=\sum_{e=1}^{m}\frac{1}{2}\left(1+d_e(-1)^{x_{a_e}+x_{b_e}+x_{c_e}}\right),\qquad d_e=(-1)^{r_e}
$$

Number of satisfied equations; each equation on three variables requires their mod-2 sum to equal r_e. The second form uses spin variables (-1)^{x_j} and is an exact identity.

Provenance: `abstract_inferred`. Direct formalization of the abstract's verbal problem definition; the spin form follows from (-1)^{x_a+x_b+x_c}=d_e iff the parity equals r_e.

Abstract evidence: each equation says that the sum of the variables mod 2 is 0 or is 1

Equation assumptions:

- The three variables in each equation are distinct (standard meaning of E3LIN2).

## eq_2: Diagonal cost operator

$$
C=\sum_{e=1}^{m}\frac{1}{2}\left(1+d_e\,Z_{a_e}Z_{b_e}Z_{c_e}\right),\qquad C|x\rangle=C(x)|x\rangle,\qquad |x\rangle=|x_1\rangle\otimes\cdots\otimes|x_n\rangle
$$

Quantization of eq_1 with Z_j|x_j\rangle=(-1)^{x_j}|x_j\rangle; qubit j encodes variable j, qubit 1 leftmost in the tensor product. The constant m/2 contributes only a global phase in e^{-i\gamma C}.

Provenance: `standard_background`. Standard QAOA encoding of a constraint-satisfaction objective as a diagonal operator; the three-body ZZZ term is the E3LIN2 analogue of the MaxCut ZZ term.

Equation assumptions:

- Register ordering: qubit j corresponds to variable x_j, |0\rangle \leftrightarrow x_j=0.

## eq_3: Level-one QAOA state

$$
|\gamma,\beta\rangle=e^{-i\beta B}\,e^{-i\gamma C}\,|+\rangle^{\otimes n},\qquad B=\sum_{j=1}^{n}X_j,\qquad |+\rangle=\tfrac{1}{\sqrt{2}}(|0\rangle+|1\rangle)
$$

The p=1 QAOA trial state of reference [1]; e^{-i\gamma C} factorizes exactly as a product over equations of three-qubit rotations e^{-i(\gamma/2)d_e Z_{a_e}Z_{b_e}Z_{c_e}} (up to global phase), and e^{-i\beta B}=\prod_j e^{-i\beta X_j}.

Provenance: `standard_background`. The abstract names the QAOA [1] and 'level one'; the explicit state form is recalled from the standard QAOA definition, not stated in the abstract.

Equation assumptions:

- Standard QAOA mixer B=\sum_j X_j and uniform superposition initial state, as in [1].

## eq_4: Worst-case p=1 performance claim

$$
F_1(\gamma,\beta)=\langle\gamma,\beta|C|\gamma,\beta\rangle,\qquad \max_{\gamma,\beta}F_1(\gamma,\beta)\;\ge\;\left(\frac{1}{2}+\frac{1}{101\,D^{1/2}\ln D}\right)m
$$

Expected number of satisfied equations in the p=1 state, and the abstract's guarantee that suitable angles achieve the stated fraction for every bounded-occurrence instance; a string achieving at least roughly this value is then obtained by repeated sampling.

Provenance: `abstract_explicit`. The abstract states the bound explicitly; the formulation as an expectation of C in the QAOA state is the standard way QAOA guarantees are stated. The specific (\gamma,\beta) achieving it is not given in the abstract.

Abstract evidence: the level one QAOA will efficiently produce a string that satisfies

Equation assumptions:

- The guarantee is interpreted as a bound on the expectation F_1 at the paper's (unknown here) angle choice; conversion to an actual output string uses repeated sampling.
- D \ge 2 so that \ln D>0.

## eq_5: Typical-case p=1 performance claim

$$
\max_{\gamma,\beta}F_1(\gamma,\beta)\;\approx\;\left(\frac{1}{2}+\frac{1}{2\sqrt{3e}\,D^{1/2}}\right)m\quad\text{(typical instances)}
$$

The abstract's typical-case value of the satisfied fraction; a uniformly random string gives expectation m/2 by comparison.

Provenance: `abstract_explicit`. Stated numerically in the abstract. The precise meaning of 'typical' (presumably a random-instance ensemble, e.g. random signs d_e) and whether the relation is a lower bound or asymptotic equality are not specified in the abstract, so it is written as an approximate relation.

Abstract evidence: in the typical case the quantum computer will output a string that satisfies

Equation assumptions:

- 'Typical case' is interpreted as an instance ensemble with random signs d_e; this is not confirmed by the abstract.

## eq_6: Tiny explicit instance (n=4, m=2, D=2)

$$
x_1\oplus x_2\oplus x_3=0\;(d_1=+1),\qquad x_2\oplus x_3\oplus x_4=1\;(d_2=-1),\qquad C=1+\tfrac{1}{2}Z_1Z_2Z_3-\tfrac{1}{2}Z_2Z_3Z_4,\qquad \max_x C(x)=2
$$

Smallest nontrivial instance with a variable shared between equations: variables x_2,x_3 occur in D=2 equations. Both equations are simultaneously satisfiable (e.g. x=0001), so the optimum is 2 and a random string satisfies 1 in expectation.

Provenance: `assumption`. Chosen by the agent as a minimal test instance for circuit generation; the asymptotic bounds of eq_4/eq_5 are not informative at D=2 and this instance is for verifying the circuit, not the theorem.

Equation assumptions:

- Instance chosen for size, not for exercising the paper's bounds.

## Registers

- q: n (n=4 for the tiny instance) qubits; One qubit per boolean variable; qubit j holds x_j in the computational basis with |0\rangle\leftrightarrow x_j=0; qubit 1 is the leftmost tensor factor.

## Initial state

|+\rangle^{\otimes n}=H^{\otimes n}|0\rangle^{\otimes n}, the uniform superposition over all 2^n assignments (eq_3).

## Measurement

Projective measurement of all n qubits in the computational (Z) basis, yielding x\in\{0,1\}^n; the sample mean of C(x) estimates F_1(\gamma,\beta)=\langle\gamma,\beta|C|\gamma,\beta\rangle.

## Classical postprocessing

Evaluate C(x) (eq_1) for each measured string; report the best string and the estimated expectation F_1. For the tiny instance, angles may be chosen by a classical grid search over (\gamma,\beta)\in[0,2\pi)\times[0,\pi) (an agent choice); the angles used in the paper's proofs are not available from the abstract.

## Algorithm steps

1. Prepare the uniform superposition by applying a Hadamard gate to every qubit of register q starting from |0\rangle^{\otimes n}. (eq_3)
2. Apply the cost unitary e^{-i\gamma C}: for each equation e, apply the three-qubit rotation e^{-i(\gamma/2) d_e Z_{a_e}Z_{b_e}Z_{c_e}} (e.g. CNOT ladder onto qubit c_e, R_z(\gamma d_e) on qubit c_e, uncompute the ladder); the constant term m/2 is a global phase and is dropped. (eq_2, eq_3)
3. Apply the mixer unitary e^{-i\beta B}=\prod_j e^{-i\beta X_j}, i.e. R_x(2\beta) on every qubit. (eq_3)
4. Measure all qubits in the computational basis to obtain a bit string x; compute C(x) classically. Repeat for a chosen (\gamma,\beta) to estimate F_1 and retain the best observed string. (eq_1, eq_4)
5. (Instance) Instantiate the above with the n=4, m=2, D=2 equations of eq_6; optimum is 2 satisfied equations. (eq_6)

## Assumptions

- No experiment_scope was provided; the agent chose the p=1 QAOA circuit on a single n=4, m=2, D=2 instance as the smallest useful construction.
- Standard QAOA components (uniform initial state, mixer B=\sum_j X_j, cost unitary e^{-i\gamma C}) are taken from the generic definition in reference [1], not from the abstract.
- Qubit j encodes variable x_j with |0\rangle\leftrightarrow 0; qubit 1 is the leftmost tensor factor.
- Each equation involves three distinct variables (E3LIN2); d_e=(-1)^{r_e} with r_e the required parity.
- 'Typical case' is interpreted as a random-instance ensemble (e.g. random signs); the abstract does not define it.
- The performance claims are interpreted as statements about the expectation F_1 at some angle choice, with a concrete string obtained by repeated sampling.
- Angle selection for the tiny instance by classical grid search is an agent choice, not the paper's method.

## Missing information

- The specific (\gamma,\beta) used in the paper's proof of the 1/2+1/(101 D^{1/2} \ln D) bound and in the typical-case analysis.
- The precise definition of the 'typical case' instance ensemble and whether eq_5 is an asymptotic equality or a lower bound.
- The derivation of the constants 101 and 2\sqrt{3e} (the local-neighborhood/light-cone analysis of the p=1 expectation is not available from the abstract).
- Whether the analysis assumes additional structure (e.g. no two equations share the same variable triple, or D \ge 2).
- How the expectation guarantee is converted to an output string (number of repetitions / concentration argument).
- The comparison with the classical algorithms [5,6] is cited only as a number; no details are available.
