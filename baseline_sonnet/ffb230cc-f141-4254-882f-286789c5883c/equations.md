# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Simon's Problem: given a black box f:{0,1}^n->{0,1}^n with f(x)=f(y) iff y=x or y=x XOR s, find the hidden period s. Scoped to the logical two-qubit version (n=2), which the abstract says was realized one-way on a five-qubit cluster state via single-qubit measurement basis choices.

Scope: Standard circuit-model Simon algorithm for n=2 with one assumed representative oracle (s=11, f(00)=f(11), f(01)=f(10)), plus classical postprocessing of the orthogonality equations. Outside scope: the five-qubit cluster-state construction, measurement angles per function, photonic implementation, experimental fidelity, and the n-qubit resource analysis, none of which can be reconstructed from the abstract.

## Symbols

- $n$: number of logical input qubits (n=2 here); domain: positive integer
- $f$: black-box function; domain: {0,1}^n -> {0,1}^n
- $s$: hidden period (XOR mask); domain: {0,1}^n
- $x,y$: input bit strings; domain: {0,1}^n
- $U_f$: oracle unitary; domain: unitary on 2n qubits
- $H$: Hadamard gate; domain: single-qubit unitary
- $\cdot$: bitwise inner product mod 2; domain: {0,1}

## eq_1: Simon promise

$$
f(x)=f(y)\iff y\in\{x,\;x\oplus s\}
$$

Defines the promise on the black box with hidden period s

Provenance: `standard_background`. Standard definition of Simon's Problem; the abstract only calls it a black-box period-finding problem.

Equation assumptions:

- s is nonzero (2-to-1 case)

## eq_2: Oracle action

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle
$$

Standard reversible oracle

Provenance: `standard_background`. Standard circuit-model oracle; the one-way implementation's realization of it is not given in the abstract.

Equation assumptions:

- Circuit-model oracle, not the cluster-state version

## eq_3: Output distribution after Hadamards

$$
\Pr(z)=\begin{cases}2^{-(n-1)} & z\cdot s=0\\0 & z\cdot s=1\end{cases}
$$

Measuring the input register after H^{\otimes n} yields z uniformly from those orthogonal to s

Provenance: `standard_background`. Standard Simon analysis, not evidence from the abstract.

Equation assumptions:

- Ideal noiseless execution

## eq_4: Assumed n=2 instance

$$
s=11,\; f(00)=f(11)=00,\; f(01)=f(10)=01
$$

One representative two-to-one function for the tiny instance

Provenance: `assumption`. Chosen as a smallest example; the abstract does not specify which functions were tested.

Equation assumptions:

- Chosen as one representative function

## eq_5: Instance outcomes

$$
z\in\{00,11\},\;\Pr(z)=\tfrac12 \text{ each}
$$

For s=11, the allowed z satisfy z\cdot s=0 mod 2

Provenance: `assumption`. Follows from eq_3 and the assumed instance eq_4.

Equation assumptions:

- Ideal noiseless execution

## Registers

- input: 2 qubits; Hadamard-transformed query register, measured
- output: 2 qubits; holds f(x) via the oracle

## Initial state

|00>_input |00>_output

## Measurement

Computational-basis measurement of the 2 input qubits (circuit model); the cluster-state version uses single-qubit measurements in chosen bases, not specified in the abstract.

## Classical postprocessing

Collect the nonzero z values and solve z·s=0 mod 2 for nonzero s; for n=2, s=11 follows from the single outcome z=11.

## Algorithm steps

1. Apply H on both input qubits to form the uniform superposition. (no equation reference)
2. Apply the oracle U_f. (eq_2, eq_4)
3. Apply H on the input qubits and measure them in the computational basis. (eq_3, eq_5)
4. Repeat until the nonzero outcomes determine s via z·s=0. (eq_3)

## Assumptions

- Circuit-model reconstruction is used as a proxy for the one-way implementation
- The instance s=11 is chosen by me, not from the abstract

## Missing information

- Cluster-state graph and qubit-to-role mapping
- Measurement bases/angles for each function
- Which functions were tested
- Resource scaling formulas for n qubits
- Experimental fidelities
