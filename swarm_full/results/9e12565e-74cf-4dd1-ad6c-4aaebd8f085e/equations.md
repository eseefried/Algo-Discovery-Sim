# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reduce the exponential measurement cost of qubit state tomography by using complete sets of mutually unbiased bases (MUBs) for n qubits, generated cyclically from a basic generator built only from Hadamard and controlled-phase gates. The abstract covers three and four qubits, with different entanglement structures and the circuits implementing them.

Scope: Abstract-level reconstruction only: MUB-based tomography for 3 and 4 qubits via a cyclic generator of H and CZ gates. The explicit generator, the stabilizer or partition structure, and the circuits are not given in the abstract and are not reconstructed.

## Symbols

- $n$: number of qubits; domain: positive integer, here 3 or 4
- $d$: Hilbert space dimension; domain: d=2^n
- $\{|\psi_k^{(a)}\rangle\}$: orthonormal basis a and its k-th vector; domain: a=0..d, k=0..d-1

## eq_1: Mutual unbiasedness

$$
|\langle \psi_k^{(a)}|\psi_l^{(b)}\rangle|^2=\frac{1}{d}\quad (a\neq b)
$$

Defining condition for two bases to be mutually unbiased.

Provenance: `standard_background`. Standard definition of MUBs, implied by the abstract's topic but not written there.

Equation assumptions:

- d=2^n

## eq_2: Complete MUB set size

$$
N_{\text{MUB}}=d+1=2^n+1
$$

A complete set of MUBs for n qubits has 2^n+1 bases, which suffices for full tomography.

Provenance: `standard_background`. Standard result for prime-power dimension; the abstract only mentions complete sets.

Equation assumptions:

- d is a prime power

## Registers

- q: n (3 or 4) qubits; system qubits whose state is to be reconstructed; MUB circuits are applied to them before computational-basis readout

## Initial state

Unknown n-qubit state rho to be reconstructed (the input to each basis-change circuit).

## Measurement

For each of the 2^n+1 bases, apply the basis-change circuit and measure all n qubits in the computational basis, giving outcome frequencies p_k^(a) estimating <psi_k^(a)|rho|psi_k^(a)>.

## Classical postprocessing

Reconstruct rho from the measured frequencies using the standard MUB inversion rho = sum_{a,k} p_k^(a) |psi_k^(a)><psi_k^(a)| - I (valid for a complete MUB set); optionally apply a physicality correction such as maximum likelihood for finite statistics. This is background, not stated in the abstract.

## Algorithm steps

1. Pick one of the 2^n+1 bases of a complete MUB set; the computational basis needs no circuit. (eq_1, eq_2)
2. Apply the basis-change circuit built from Hadamard and controlled-phase gates. Per the abstract, the basic generator is applied cyclically to obtain successive bases, and the entanglement class determines the circuit. The explicit gate pattern is not given in the abstract. (eq_1)
3. Repeat for each basis in the set, preparing fresh copies of rho each time. (eq_2)

## Assumptions

- The MUB definition and the 2^n+1 count are standard background, not taken from the abstract.
- Circuit steps are a generic abstract-level plan; the cyclic application of the generator follows the abstract but the gate details are not specified.
- Each basis is measured on fresh copies of the state.
- Measurement is projective in the computational basis after the basis-change unitary; the inversion formula is standard background.

## Missing information

- Explicit cyclic generator unitary
- Gate sequences for the 3- and 4-qubit entanglement classes
- Which qubit pairs receive controlled-phase gates in each basis circuit
- Paper's specific reconstruction formulas and shot counts
