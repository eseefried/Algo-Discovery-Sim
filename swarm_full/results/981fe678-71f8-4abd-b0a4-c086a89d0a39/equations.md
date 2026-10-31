# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Assess whether Shor's factoring algorithm (SFA) success probability can be improved by using odd orders returned by the quantum order finding algorithm (QOFA), for N=p1 p2 and coprime a, including the case of square coprimes. Two techniques are considered: not discarding odd orders, and looking for new order finding relations after failure.

Scope: Abstract-level reconstruction of the classical order-to-factor relations and the order definition for a small finite factoring instance, with a generic textbook QOFA skeleton labeled as assumed. The paper's two odd-order techniques and the quantitative improvement are not specified in the abstract and are not reconstructed.

## Symbols

- $N$: Number to factor, N=p_1 p_2; domain: positive integer
- $a$: Randomly chosen integer coprime to N; domain: integer with gcd(a,N)=1
- $r$: Order of a modulo N; domain: smallest positive integer
- $p_1,p_2$: Prime factors of N; domain: primes

## eq_1: Order definition

$$
a^{r}\bmod N=1
$$

r is the smallest positive integer satisfying this relation.

Provenance: `abstract_explicit`. Stated in the abstract as the definition of the order.

Abstract evidence: a^{r}\mod N=1

## eq_2: Coprimality

$$
\gcd(a,N)=1
$$

The base a is coprime to N.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \gcd(a,N)=1

## eq_3: Factor from even order

$$
p_1=\gcd(a^{r/2}-1,N)
$$

The first factor is recovered from the order r.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: p_{1}=\gcd(a^{\frac{r}{2}}-1,N)

Equation assumptions:

- r even
- success probability at least 1/2

## eq_4: Second factor

$$
p_2=\gcd(a^{r/2}+1,N)
$$

The second factor is recovered from the order r.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: p_{2}=\gcd(a^{\frac{r}{2}}+1,N)

Equation assumptions:

- r even

## Registers

- control: t qubits (assumed, t about 2 log2 N) qubits; Phase-estimation register holding the superposition over exponents x
- target: n=ceil(log2 N) qubits (assumed) qubits; Work register for modular exponentiation a^x mod N

## Initial state

Control register in |0>^t, target register in |1> (assumed standard QOFA initialization).

## Measurement

Measure the t-qubit control register in the computational basis to obtain an integer y, approximating a multiple of 2^t/r (assumed standard QOFA readout; not given in abstract).

## Classical postprocessing

Estimate r from y/2^t via continued fractions (assumed), check a^r mod N=1 (eq_1). If r is even, compute gcd(a^{r/2}-1,N) and gcd(a^{r/2}+1,N) (eq_3, eq_4) and accept if nontrivial. If r is odd or fails, the abstract indicates relaunching with a different a, or the paper's odd-order techniques (e.g. square coprimes, new order finding relations), whose details are not specified.

## Algorithm steps

1. Apply Hadamard gates to the control register to create a uniform superposition over x (assumed standard). (no equation reference)
2. Apply controlled modular exponentiation mapping |x>|1> to |x>|a^x mod N>, which encodes the periodicity r of eq_1 given eq_2. (eq_1, eq_2)
3. Apply inverse quantum Fourier transform to the control register to expose multiples of 2^t/r (assumed standard). (eq_1)
4. Measure the control register; the classical outcome is used to estimate r, then factors are computed from r via the gcd relations. (eq_3, eq_4)

## Assumptions

- Even-order relations are taken as stated; for p1 and p2 to be nontrivial, nontrivial square roots of 1 mod N are required.
- Circuit skeleton and register sizes are the generic textbook QOFA, not confirmed from the abstract.
- Continued-fraction postprocessing is assumed standard, not stated in the abstract.
- Continued-fraction order extraction assumed as standard postprocessing.

## Missing information

- Details of the two odd-order techniques are not given in the abstract.
- QOFA circuit details (register sizes, gates) are not in the abstract.
- Quantitative size of the improvement is not given.
- Odd-order handling within the circuit plan and postprocessing is not specified in the abstract.
- Exact rules for extracting factors from odd orders with square coprimes are not in the abstract.
