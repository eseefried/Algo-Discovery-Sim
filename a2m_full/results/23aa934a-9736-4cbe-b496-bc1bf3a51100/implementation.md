# Equation to Qiskit

Unitary circuit for `steps` coined quantum-walk steps on a reflecting open chain of L=2^m sites with i.i.d. dynamic edge percolation. Each step uses fresh edge ancillas rotated by Ry(theta) with sin^2(theta/2)=p, then applies the Hadamard coin and a shift that moves across open edges and reflects with a coin flip at closed edges or boundaries. The shift is built as a fixed cyclic permutation T of the 2L (position, coin) states after a controlled swap Z that is conditioned on closed edges. Ancillas are left entangled and are never reset, so tracing them out gives the random-unitary channel Phi^n. The qubit cap limits how many steps fit (for L=4, at most 3). No state preparation or measurement is included.

Source equation run: `ec21a219-c599-49e6-9317-dce4b4efe76c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: pos register, little-endian walker position x (m=2 in example: qubits 0,1)
- qubit m: coin (c=0 moves right, c=1 moves left); qubit 2 in example
- step s edge ancillas: qubit m+1+s*(2^m-1)+e is the ancilla for edge e between sites e and e+1 (1=open, 0=closed); example: step 0 qubits 3-5, step 1 qubits 6-8, step 2 qubits 9-11
- total qubits = m+1+(2^m-1)*steps, capped at 12

## Assumptions

- Edge e joins sites e and e+1; ancilla value 1 means open, with probability p
- Coin 0 moves right and coin 1 moves left; closed edges and boundaries reflect with a coin flip
- Hadamard coin applied before the shift in each step
- The runner prepares the initial state (for example pos=0, coin=0, ancillas |0>) and reduces over ancillas
- Qubit order is little-endian with the coin as the most significant bit of the encoded cyclic index

## Unresolved issues

- The paper's exact coin, shift and boundary conventions are unknown, so this is a plausible reconstruction rather than the paper's model
- The asymptotic state of the channel is analysed classically, not by this circuit
- Long-time behaviour cannot be probed with the circuit at the 12-qubit cap because only a few steps fit
- The 1D classification and 2D Grover results are not reconstructed

## Equation mapping

- `eq_1`: implemented; build_circuit (fresh Ry-prepared edge ancillas per step controlling _closed_edge_swaps). The channel sum_omega p(omega) U_omega rho U_omega^dagger arises when the edge ancillas are traced out. The circuit is the coherent purification, with one fresh ancilla set per step and no reset.
- `eq_2`: implemented; _closed_edge_swaps and _cycle_shift, plus coin Hadamard in build_circuit. U_omega = S_omega (I x H), with S_omega = T Z. Z swaps |e,0> and |e+1,1> when edge e is closed. T is the fixed cyclic permutation giving the open-edge move and the boundary reflection.
- `eq_3`: implemented; build_circuit (qc.ry(theta, a) with theta=2 asin(sqrt p)). Each edge ancilla is prepared as cos(theta/2)|0>+sin(theta/2)|1>, so it is open with probability p.
- `eq_4`: background; no code location. Peripheral spectrum and the n->infinity limit are classical analysis of the superoperator. The circuit only provides finite-n evolution.
- `eq_5`: out_of_scope; no code location. Position readout and comparison with P_infty involve measurement and post-processing, which are excluded from the operation.

## Specification changes

- eq_2: The shift S_omega is factorized as T after Z, with Z a closed-edge controlled swap and T a fixed cyclic permutation on 2L states. A multi-controlled increment on an encoded index is used instead of per-site multi-controlled gates. Reason: Gives an equivalent permutation (verified analytically: the images of the pair {|e,0>,|e+1,1>} are the same set for open and closed edges) with a compact construction.
- eq_1, eq_3: Mid-circuit reset of ancillas is replaced by fresh ancillas for every step, and the number of steps is limited by the 12-qubit cap (for L=4, steps<=3). Reason: Resets and dynamic circuits are not allowed, so the random-unitary averaging is realised by purification.
- eq_1, eq_2, eq_3: Generalised from the fixed 4-site chain to L=2^m sites with m in 1..3, with p and steps as parameters. The Hadamard coin and the equal-p i.i.d. edge model are kept fixed. Reason: Allows varying valid instances while keeping the same construction; non-power-of-two chains would need extra encoding.
- eq_4, eq_5: Superoperator spectral analysis, P_infty and the position measurement are excluded from the circuit. Reason: The task requires a measurement-free unitary operation without simulation or post-processing.
