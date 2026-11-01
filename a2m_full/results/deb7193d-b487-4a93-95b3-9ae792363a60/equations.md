# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Factor N=p1*p2 using quantum order finding for a coprime a, with classical post-processing that also exploits odd orders: when a is a perfect square a=b^2, odd r still gives factors via b^r, and failed runs are reused through order relations involving sqrt(a).

Scope: One tiny instance: N=21 with a=4 (square, b=2, order r=3, odd, so the odd-order extension applies), plus a standard non-square control case such as N=15, a=7 (r=4). The scope covers the textbook phase-estimation circuit (t control qubits, n work qubits), continued-fraction order extraction, the odd-order gcd rule for square a, and the check of x^2=1 relations. The two-run relation-combining techniques and the efficiency/probability analysis are outside scope.

## Symbols

- $N$: Integer to factor, N=p_1 p_2; domain: positive integer, small (e.g. 15, 21, 35)
- $a$: Base coprime to N; domain: integer, 1<a<N, gcd(a,N)=1
- $r$: Multiplicative order of a mod N; domain: positive integer
- $b$: Classical integer square root of a when a=b^2 (as integers); domain: integer, b^2=a
- $n$: Work register size, ceil(log2 N); domain: positive integer
- $t$: Control register size; domain: positive integer, about 2n or fewer if the qubit cap requires
- $y$: Measured control register integer, little-endian: y=sum_i c_i 2^i for measured bit c_i of control qubit i; domain: 0..2^t-1
- $s$: Random integer in the eigenphase s/r; domain: 0..r-1
- $U_a$: Modular multiplication |x> -> |a x mod N> on the work register; the black box is its controlled powers; domain: unitary on n qubits, acts as identity on x>=N

## eq_1: Order definition

$$
r=\min\{k\ge 1: a^{k}\equiv 1 \pmod N\},\quad \gcd(a,N)=1
$$

The order that the QOFA computes.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: the smallest integer, $r$, satisfying $a^{r}\mod N=1$, where $a$ is a randomly chosen integer coprime to $N$

## eq_2: Even-order factor extraction

$$
p_1=\gcd(a^{r/2}-1,N),\quad p_2=\gcd(a^{r/2}+1,N)
$$

For even r the factors are obtained from gcds. The method succeeds only if a^{r/2} is not congruent to -1 mod N.

Provenance: `abstract_explicit`. Given in the abstract; the nontriviality condition is standard background.

Abstract evidence: the factors are given by $p_{1}=\gcd(a^{\frac{r}{2}}-1,N)$ and $p_{2}=\gcd(a^{\frac{r}{2}}+1,N)$

Equation assumptions:

- r even
- a^{r/2} != -1 mod N

## eq_3: Phase estimation outcome distribution

$$
P(y)=\frac{1}{r}\sum_{s=0}^{r-1}\left|\frac{1}{2^{t}}\sum_{k=0}^{2^{t}-1}e^{2\pi i k (s/r-y/2^{t})}\right|^{2},\quad \frac{y}{2^{t}}\approx\frac{s}{r}
$$

Distribution of the control-register outcome after controlled U_a^{2^j}, inverse QFT, and measurement, starting from work register |1>. Candidate r is the denominator of the continued-fraction convergent of y/2^t with denominator < N, verified by a^r mod N = 1.

Provenance: `standard_background`. Textbook Shor order finding; the abstract does not give the circuit.

Equation assumptions:

- Work register starts in |1>
- Controlled U_a^{2^j} from control qubit j
- Qiskit little-endian: y bit i is the result of measure(i,i)

## eq_4: Odd order with square coprime

$$
a=b^{2},\ r\text{ odd}\Rightarrow (b^{r})^{2}\equiv a^{r}\equiv 1 \pmod N,\quad f_{\pm}=\gcd(b^{r}\mp 1,N)
$$

If a is a perfect square and r is odd, then b^r is a square root of 1 mod N (an integer, unlike a^{r/2}); it yields factors when b^r != +-1 mod N.

Provenance: `abstract_inferred`. The abstract notes this possibility; the explicit formula is derived from b^2=a and a^r=1.

Abstract evidence: the factors can sometimes be found from odd orders if the coprime is square

Equation assumptions:

- b computed classically as an exact integer square root of a
- b^r not congruent to +-1 mod N

## eq_5: Order of the square root

$$
r_b=\operatorname{ord}_N(b)\in\{r,2r\},\quad b^{2r}\equiv 1
$$

Since b^2=a, the order of b divides 2r and is either r or 2r. A found order r for a gives a relation for b, and this is the kind of new order-finding relation a failed run may supply. If r_b=2r is even, gcd(b^{r}\pm 1,N) applies.

Provenance: `abstract_inferred`. This is my reading of the second technique as relating orders of a and sqrt(a); the exact procedure in the paper is not known.

Abstract evidence: looking out for new order finding relations in the case of failure

Equation assumptions:

- a=b^2 over the integers

## eq_6: Nontrivial square root of unity gives factors

$$
x^{2}\equiv 1 \pmod N,\ x\not\equiv \pm 1\Rightarrow \gcd(x-1,N)\in\{p_1,p_2\}
$$

Any nontrivial square root of 1 mod N gives a factor of N. This is the final classical check for all cases.

Provenance: `standard_background`. Standard number theory for N=p1 p2 with distinct odd primes.

Equation assumptions:

- N is a product of two distinct odd primes

## Registers

- control: t (e.g. 4 to 6 for N=15 or 21) qubits; Phase-estimation register; H on all qubits, controlled U_a^{2^j}, inverse QFT, then measured
- work: n=ceil(log2 N) (5 for N=21, 4 for N=15) qubits; Holds |1> initially; the opaque controlled-U_a^{2^j} black boxes act here; not measured

## Initial state

control in |0...0>, work in |1> (little-endian, work qubit 0 set to 1); H applied to every control qubit.

## Measurement

Measure the t control qubits only, with measure(i,i); in a Qiskit counts key the last character is bit 0.

## Classical postprocessing

Continued fractions on y/2^t, verification of a^r mod N=1 (also try multiples and divisors of r), then gcd steps from eq_2, eq_4, and eq_6. For non-square a with odd r the abstract does not clearly show a way to find factors; the sketch's suggestion is unverified.

## Algorithm steps

1. Pick the instance (N,a); for a square a, compute b=sqrt(a) classically. Prepare work=|1> and apply H to all t control qubits. (eq_1)
2. For j=0..t-1 apply controlled-U_a^{2^j} (one black-box query each, control qubit j, target work register). (eq_3)
3. Apply the inverse QFT to the control register (H, controlled-phase, swaps), with attention to little-endian ordering, then measure only the control qubits. (eq_3)
4. Classical: convert counts to y, run continued fractions on y/2^t, test candidates r (and small multiples) with a^r mod N=1. (eq_3, eq_1)
5. If r is even and a^{r/2} != -1, use the gcd formulas. If r is odd and a=b^2, use the b^r gcds. If r_b=2r, test b^r. Otherwise record the relation and retry with a different a. (eq_2, eq_4, eq_5, eq_6)

## Assumptions

- Instance N=21, a=4 chosen by me as the smallest useful odd-order square example, plus N=15, a=7 as a control case.
- The black box is controlled multiplication by a^{2^j} mod N and is used as given.
- The qubit cap allows t+n qubits; for N=21 t may need to be reduced, so the outcome would be coarser.
- The sketch's claim about x=a^{(r+1)/2} for non-square a is not adopted as an equation; it is unestablished.

## Missing information

- The abstract does not give the exact procedure for combining relations across runs.
- The abstract does not give the success-probability formulas or the efficiency comparison.
- The circuit details (t, QFT variant) are not specified.
