# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate a single-qubit unitary U within precision epsilon by a Repeat-Until-Success (RUS) circuit over Clifford+T with one ancilla and measurement. Scoped instance: one RUS attempt, a measurement-free 2-qubit Clifford+T unitary W whose ancilla-|0> success branch implements a non-unitary Kraus operator proportional to a unitary V approximating U = R_z(theta).

Scope: Only a tiny, assumed single-attempt unitary W on system q0 and ancilla q1 is specified, together with the Kraus-operator, success-probability and expected-T-count relations. The randomized polynomial-time classical synthesis (sampling Z[1/sqrt2,i] entries, norm-equation solving with randomized factoring), the paper's actual circuit family, the failure-branch correction, the retry loop and numerical T-count comparisons are outside scope. The concrete W is a placeholder illustration, not the paper's construction.

## Symbols

- $U$: target single-qubit unitary (assumed R_z(theta)); domain: SU(2)
- $\varepsilon$: approximation precision; domain: positive real
- $W$: Clifford+T unitary of one RUS attempt on system and ancilla; domain: U(4)
- $K_0,K_1$: Kraus operators for ancilla outcome 0 (success) and 1 (failure); domain: 2x2 complex matrices
- $V$: unitary proportional to K_0; domain: SU(2) up to phase
- $c$: scalar with |c|^2 = success probability p (state-independent when K_0 = cV); domain: complex, 0<|c|<=1
- $p$: success probability per attempt; domain: (0,1]
- $T_a$: T-count of one attempt; domain: positive integer
- $\theta$: rotation angle of target R_z; domain: real

## eq_1: Kraus operators of one attempt

$$
K_m=(I\otimes\langle m|)\,W\,(I\otimes|0\rangle),\quad K_0^\dagger K_0+K_1^\dagger K_1=I
$$

Ancilla prepared in |0>, W applied, ancilla measured in the computational basis; completeness follows from unitarity of W.

Provenance: `standard_background`. Standard Kraus-operator formalism for ancilla-assisted measurement.

Equation assumptions:

- Ancilla measured in computational basis

## eq_2: Success operator proportional to a unitary

$$
K_0=cV,\quad p=|c|^2,\quad \|V-U\|\le\varepsilon
$$

Success branch acts as a unitary V close to U with success probability p, so K_0^dagger K_0 = p I.

Provenance: `abstract_inferred`. Approximating U by an RUS circuit requires the success branch to be a unitary approximating U; proportionality to a unitary is the assumed structure from the method sketch.

Abstract evidence: approximate any given single-qubit unitary within precision $\varepsilon$

Equation assumptions:

- Norm is the operator norm, up to global phase

## eq_3: Expected T-count

$$
\mathbb{E}[T]=T_a/p
$$

Expected T-count of the repeat-until-success loop with geometric number of attempts, ignoring failure-correction T cost.

Provenance: `abstract_inferred`. Geometric retry statistics give expected attempts 1/p; correction gates are assumed free of T.

Abstract evidence: expected $T$-count on average $2.5$ times lower

Equation assumptions:

- Failure correction costs no T gates
- Each attempt has equal T-count

## eq_4: Ancilla-free reference bound

$$
T_{\mathrm{ancilla\text{-}free}}\approx 3\log_2(1/\varepsilon),\quad \mathbb{E}[T]_{RUS}\approx \tfrac{1}{2.5}\,T_{\mathrm{ancilla\text{-}free}}
$$

Reference lower bound and the reported average ratio of about 2.5.

Provenance: `abstract_explicit`. The abstract states the bound and the 2.5 average factor (numerical evidence, not derived here).

Abstract evidence: theoretical lower bound of $3\log_{2}(1/\varepsilon)$ for ancilla-free single-qubit circuit decomposition

Equation assumptions:

- Ratio is an empirical average, not a guarantee per instance

## eq_5: Target rotation

$$
U=R_z(\theta)=\mathrm{diag}(e^{-i\theta/2},e^{i\theta/2})
$$

Chosen tiny target instance.

Provenance: `assumption`. The scope is chosen as one small instance since the abstract gives no explicit U.

Equation assumptions:

- theta fixed classically, e.g. pi/8-type angle

## Registers

- q0: 1 qubits; system qubit, arbitrary input state; qubit 0
- q1: 1 qubits; ancilla, initialized |0>, success when measured 0; qubit 1

## Initial state

|psi>_{q0} tensor |0>_{q1}

## Measurement

Ancilla q1 measured in the computational basis after W; outcome 0 is success. Not included in the built unitary.

## Classical postprocessing

Retry on failure after a fixed correction; the randomized polynomial-time search over Z[1/sqrt2,i] candidates with norm-equation solving and the filtering ||V-U||<=epsilon is described qualitatively only.

## Algorithm steps

1. Prepare ancilla in |0> and system in the input state; basis ordering |q1 q0>, little-endian as in Qiskit. (eq_1)
2. Apply a fixed Clifford+T attempt unitary W on (q0,q1), e.g. H on ancilla, controlled Clifford+T blocks with T and T-dagger, closing H on ancilla. The specific W must be supplied by classical search; no paper-specific W is known. (eq_1, eq_5)
3. Success branch is ancilla outcome 0, giving K_0=cV with V close to U; the measurement and retry loop are outside the unitary circuit. (eq_2)
4. Classically, compute expected T-count T_a/p and compare to the ancilla-free reference. (eq_3, eq_4)

## Assumptions

- Scope is a single attempt for U=R_z(theta) with fixed theta
- W is a placeholder Clifford+T circuit whose exact gates are not given by the abstract
- Failure branch is correctable by Cliffords at no T cost

## Missing information

- Explicit gate sequence W of the paper's RUS circuits
- The randomized synthesis algorithm and its norm-equation details
- Exact failure-correction procedure
- Numerical T-count data
