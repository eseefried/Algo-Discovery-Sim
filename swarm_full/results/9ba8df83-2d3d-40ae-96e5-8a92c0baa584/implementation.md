# Equation to Qiskit

Gate-level 4-qubit (default) Grover iteration operator G^k (oracle plus inversion about the mean) for one marked basis state. After each oracle and diffusion block it optionally applies free Ising ZZ evolution between nearest and second-nearest neighbours, lasting tau = pi/Omega per block. It does not include state preparation, fidelity evaluation or Rabi-frequency scans.

Source equation run: `3e76a2f8-34a1-4414-ad5f-51ba8c87e501`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form one register 'spins'; the default is n=4 with qubits 0-3
- Qubit 0 is the least significant bit of the computational-basis index and of the marked item
- Chain neighbours are qubits i and i+1; second neighbours are qubits i and i+2
- Input state (e.g. uniform superposition) is prepared by the runner; the circuit is G^k only

## Assumptions

- Iz = Z/2, so J is an angular frequency in the same units as omega and the time unit is 1/omega
- Each oracle and diffusion block is followed by free Ising evolution of duration pi/omega; omega=None or zero couplings give the ideal Grover operator
- Single marked item and about 3 iterations for n=4
- Qiskit little-endian bit ordering for the marked index

## Unresolved issues

- The exact 2πk condition for second-nearest-neighbour coupling is unknown
- Real coupling constants and pulse decompositions of the oracle and diffusion are unknown
- Ising evolution during the rf pulses is not modelled; only the interleaved free-evolution approximation is
- Fidelity with respect to the ideal state must be evaluated externally

## Equation mapping

- `eq_1`: implemented; _ising_layer. H_J with Iz=Z/2 gives exp(-i J t ZZ/4) = RZZ(J t/2) on nearest (i,i+1) and second-nearest (i,i+2) pairs. It is applied as a discrete layer of duration tau after each oracle and diffusion block.
- `eq_2`: out_of_scope; no code location. Fidelity is an evaluation quantity computed by the runner or simulator, not part of the operation.
- `eq_3`: out_of_scope; no code location. The 2πk condition is only a schematic placeholder in the specification. The code uses omega solely to set the block duration tau = pi/omega, and neither enforces nor scans the condition.

## Specification changes

- eq_1: Continuous simultaneous Ising evolution during rf pulses is replaced by ideal instantaneous gates followed by a free-evolution ZZ layer of duration tau = pi/omega after each oracle and each diffusion block. Reason: The abstract gives no pulse sequences or couplings, so a standard gate decomposition with a Trotter-like coupling layer is the only well-defined construction.
- eq_1, eq_3: No initial Hadamard or pulse layer and no Ising layer for state preparation is included. The circuit is the Grover iterate G^k only, and omega enters only through tau. Reason: The task requires an operation without input-state preparation. The step 1 pulse block is the runner's responsibility.
- eq_2, eq_3: Fidelity computation, the Rabi-frequency scan and identification of 2πk maxima are excluded from the circuit. Reason: These are classical post-processing or experiment steps, and the 2πk formula is unspecified.
- eq_1: The oracle uses a single marked basis state (parameter 'marked'), the default iteration count is floor(pi/4*sqrt(2^n)), and the diffusion operator is implemented up to a global phase. Reason: These details are assumed in the specification and are unspecified in the abstract.
