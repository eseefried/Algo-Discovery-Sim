# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct the mathematical content of Shor's factoring algorithm (SFA) with the quantum order finding algorithm (QOFA) as its subroutine, together with the classical post-processing rule by which an odd order r can still yield the factors of N = p_1 p_2 when the chosen coprime a is a perfect square a = b^2, as described in the abstract.

Scope: One run of the QOFA (standard phase-estimation order finding) for the smallest explicit instance in which an odd order with a square coprime yields the factors: N = 21, a = 4 = 2^2 (so b = 2), whose order is r = 3 (odd). The scope covers: definition of the order, the controlled-modular-multiplication unitary and its eigenphases, the phase-estimation measurement and continued-fraction recovery of r, the standard even-order factor extraction, and the inferred odd-order square-coprime extraction rule via b^r. Outside scope: the paper's second technique ('looking out for new order finding relations in the case of failure'), its quantitative analysis of the success-probability improvement, the claimed efficiency equivalence with avoiding square coprimes, and any specific circuit decomposition of modular multiplication.

## Symbols

- $N$: Composite number to be factored, N = p_1 p_2; domain: odd composite positive integer; instance N = 21
- $p_1, p_2$: Prime factors of N; domain: primes; instance 3 and 7
- $a$: Randomly chosen base coprime to N (here chosen as a square a = b^2 mod N); domain: integer, 1 < a < N, gcd(a,N) = 1; instance a = 4
- $b$: Square root of the coprime, a \equiv b^2 \pmod N, assumed known; domain: integer, 1 < b < N, gcd(b,N) = 1; instance b = 2
- $r$: Multiplicative order of a modulo N; domain: positive integer dividing \lambda(N); instance r = 3
- $n$: Number of qubits in the work register, n = \lceil \log_2 N \rceil; domain: positive integer; instance n = 5
- $t$: Number of qubits in the control (phase) register; domain: positive integer; instance t = 2n = 10 (assumption)
- $U_a$: Modular multiplication-by-a unitary on the work register; domain: unitary on 2^n-dimensional Hilbert space
- $s$: Index of the U_a eigenstate selected by the measurement; domain: integer, 0 \le s \le r-1
- $m$: Integer measurement outcome of the control register; domain: integer, 0 \le m \le 2^t - 1
- $|x\rangle$: Computational basis state encoding integer x with qubit j holding bit x_j, x = \sum_j x_j 2^j (qubit 0 is least significant); domain: basis states of a register

## eq_1: Definition of the order

$$
r = \min\{\,k \in \mathbb{Z}_{\ge 1} : a^{k} \equiv 1 \pmod N\,\}, \qquad \gcd(a,N) = 1
$$

The order r is the smallest positive integer with a^r mod N = 1; it is the quantity computed by the QOFA.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: calculates the order – the smallest integer, $r$, satisfying $a^{r}\mod N=1$, where $a$ is a randomly chosen integer coprime to $N$

## eq_2: Even-order factor extraction

$$
r \text{ even},\; a^{r/2} \not\equiv -1 \pmod N \;\Rightarrow\; p_1 = \gcd\!\left(a^{r/2}-1,\,N\right),\quad p_2 = \gcd\!\left(a^{r/2}+1,\,N\right)
$$

Standard classical post-processing of Shor's algorithm: for even r with a^{r/2} not congruent to -1, the two gcds give the nontrivial factors. The abstract states this holds with probability at least 1/2 over the random choice of a.

Provenance: `abstract_explicit`. Stated in the abstract; the explicit side-condition a^{r/2} \not\equiv -1 (mod N) is added from standard background to make the relation exact.

Abstract evidence: the factors are given by $p_{1}=\gcd(a^{\frac{r}{2}}-1,N)$ and $p_{2}=\gcd(a^{\frac{r}{2}}+1,N)$

Equation assumptions:

- The condition a^{r/2} \not\equiv -1 \pmod N is the standard requirement for the gcds to be nontrivial; the abstract folds this into the 'probability not less than 1/2' statement.

## eq_3: Modular multiplication unitary and its eigenphases

$$
U_a|y\rangle = \begin{cases}|a y \bmod N\rangle & 0 \le y < N\\ |y\rangle & N \le y < 2^n\end{cases}, \qquad U_a|u_s\rangle = e^{2\pi i s/r}|u_s\rangle,\quad |u_s\rangle = \frac{1}{\sqrt r}\sum_{k=0}^{r-1} e^{-2\pi i s k/r}|a^k \bmod N\rangle,\quad |1\rangle = \frac{1}{\sqrt r}\sum_{s=0}^{r-1}|u_s\rangle
$$

The QOFA is phase estimation of U_a; its eigenvalues encode s/r, and the easily prepared state |1> is a uniform superposition of the eigenstates.

Provenance: `standard_background`. Standard formulation of order finding as phase estimation; the abstract only names the QOFA.

Equation assumptions:

- The work register has n = \lceil \log_2 N \rceil qubits and U_a acts as identity on basis states y \ge N.

## eq_4: Phase estimation state and order recovery

$$
\frac{1}{2^{t/2}}\sum_{x=0}^{2^t-1}|x\rangle|a^{x} \bmod N\rangle \xrightarrow{\mathrm{QFT}^{-1}_{t}} \;\text{measure } m,\qquad \left|\frac{m}{2^t} - \frac{s}{r}\right| \le \frac{1}{2^{t+1}} \text{ with probability } \ge \frac{4}{\pi^2},\qquad 2^t \ge 2N^2 \Rightarrow \frac{s}{r} \text{ is the unique convergent of } \frac{m}{2^t} \text{ with denominator } < N
$$

After controlled modular exponentiation and inverse QFT on the control register, the outcome m approximates 2^t s/r; continued fractions recover a candidate r (the denominator of the convergent, exact only when gcd(s,r)=1).

Provenance: `standard_background`. Standard analysis of Shor's order finding; the approximation is not exact equality, and the recovered denominator may be a divisor of r when gcd(s,r) > 1, which is checked classically via a^{r'} mod N.

Equation assumptions:

- Control register size t with 2^t \ge 2N^2 (t = 2n suffices up to rounding; t = 10 chosen for N = 21).
- Controlled-U_a^{2^j} is applied with control qubit j of the control register.

## eq_5: Odd-order factor extraction for a square coprime

$$
a \equiv b^2 \pmod N,\; r \text{ odd} \;\Rightarrow\; b^{2r} \equiv 1 \pmod N;\qquad b^{r} \not\equiv \pm 1 \pmod N \;\Rightarrow\; p_1 = \gcd\!\left(b^{r}-1,\,N\right),\; p_2 = \gcd\!\left(b^{r}+1,\,N\right)
$$

If the coprime is a known square a = b^2, an odd order r of a implies (b^r)^2 ≡ 1 mod N, so b^r is a square root of unity; whenever it is a nontrivial square root, the gcds give the factors. This is the mechanism by which odd orders can lead to factors.

Provenance: `abstract_inferred`. The abstract asserts that odd orders can yield factors when the coprime is square; the stated relation is the natural inference (b^r plays the role of a^{r/2}), with the exceptional case b^r \equiv \pm 1 explaining the word 'sometimes'. The paper's exact formulation is not available.

Abstract evidence: the factors can sometimes be found from odd orders if the coprime is square

Equation assumptions:

- b with a \equiv b^2 \pmod N is known to the experimenter (e.g., a is chosen as b^2).
- The abstract does not state the side-condition b^r \not\equiv \pm 1; it is supplied here as the standard requirement for nontrivial gcds.

## eq_6: Tiny explicit instance

$$
N = 21,\; b = 2,\; a = b^2 = 4:\quad 4^1 \equiv 4,\; 4^2 \equiv 16,\; 4^3 = 64 \equiv 1 \pmod{21} \Rightarrow r = 3;\qquad 2^{3} = 8 \not\equiv \pm 1 \pmod{21},\quad \gcd(8-1,21) = 7,\quad \gcd(8+1,21) = 3
$$

Worked instance: the order of the square coprime a = 4 modulo 21 is odd (r = 3), eq_2 is inapplicable, but eq_5 with b = 2 recovers the factors 3 and 7. Expected QPE outcomes with t = 10 cluster near m \approx 1024 s/3 \in \{0, 341.33, 682.67\}.

Provenance: `assumption`. Chosen as the smallest explicit instance exhibiting an odd order with a square coprime that leads to the factors; not taken from the abstract.

Equation assumptions:

- Instance choice N = 21, a = 4, b = 2 is the reconstructor's choice, not from the paper.

## Registers

- control (phase) register: t = 10 qubits (symbolic t with 2^t >= 2N^2) qubits; Holds the superposition over exponents x and, after inverse QFT, the measured approximation m of 2^t s/r; qubit j (0 = least significant) controls U_a^{2^j}.
- work register: n = 5 qubits (n = ceil(log2 N)) qubits; Holds integers modulo N in binary (qubit 0 least significant); initialized to |1> and acted on by controlled modular multiplications by a^{2^j} mod N.

## Initial state

|0\rangle^{\otimes t} \otimes |1\rangle, i.e. control register all zeros and work register encoding the integer 1 (= uniform superposition of U_a eigenstates |u_s>, eq_3).

## Measurement

Computational-basis measurement of all t control-register qubits, read as the integer m = \sum_j m_j 2^j; the work register is not measured (or measured and discarded).

## Classical postprocessing

Continued-fraction expansion of m/2^t to recover s/r in lowest terms (denominator is r or a divisor thereof; verify with a^{r} mod N). Then apply eq_2 for even r, or the odd-order square-coprime rule eq_5 for odd r when a = b^2 with b known; both rules use only gcd computations. Failure cases (a^{r/2} ≡ -1 or b^r ≡ ±1) lead to relaunching the QOFA with a new a.

## Algorithm steps

1. Classically choose b coprime to N and set a = b^2 mod N (here b = 2, a = 4, N = 21); verify gcd(a,N) = 1 (if gcd > 1 a factor is found directly). (eq_1, eq_6)
2. Apply Hadamard gates to all t control qubits to prepare (1/2^{t/2}) \sum_x |x\rangle|1\rangle. (eq_4)
3. For j = 0,...,t-1 apply controlled-U_{a^{2^j} mod N} with control qubit j of the control register, producing (1/2^{t/2}) \sum_x |x\rangle |a^x mod N\rangle. (eq_3, eq_4)
4. Apply the inverse quantum Fourier transform on the control register. (eq_4)
5. Measure the control register to obtain m; run the continued-fraction expansion of m/2^t to obtain a candidate denominator r'; verify a^{r'} ≡ 1 mod N (otherwise try small multiples of r' or repeat). (eq_4, eq_1)
6. Classical post-processing: if r is even and a^{r/2} \not\equiv -1, output gcd(a^{r/2} ± 1, N). If r is odd and a = b^2 with known b, compute b^r mod N; if b^r \not\equiv ±1 output gcd(b^r ± 1, N) (for the instance: 7 and 3). Otherwise relaunch with a different a. (eq_2, eq_5, eq_6)

## Assumptions

- No experiment scope was supplied; the smallest useful construction (one QOFA run for N = 21, a = 4 = 2^2, r = 3) was chosen by the reconstructor.
- Control register size t = 10 (2^t ≥ 2N^2 = 882) is a standard choice, not from the abstract.
- The square root b of the coprime a is known (a is chosen as b^2), which is what makes the odd-order rule eq_5 usable.
- Little-endian integer encoding (qubit 0 least significant) in both registers.
- The side-conditions a^{r/2} \not\equiv -1 and b^r \not\equiv ±1 (mod N) are supplied from standard number theory; the abstract only says the odd-order approach works 'sometimes'.

## Missing information

- The paper's second technique, 'looking out for new order finding relations in the case of failure', is not described mathematically in the abstract and could not be reconstructed.
- The quantitative size of the success-probability improvement from using odd orders is not given.
- The precise argument for the claimed efficiency equivalence between the new techniques and 'avoiding square coprimes and disregarding odd orders' is not available.
- Whether the paper's odd-order rule requires b to be known in advance, or recovers it otherwise, is not stated.
- No circuit-level decomposition of controlled modular multiplication by a^{2^j} mod N is provided; this is left to the circuit-generation stage.
