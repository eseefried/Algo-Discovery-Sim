# Equation to Qiskit

Builds the Trotterized quantum phase estimation operation for the reduced pairing Hamiltonian on N pair-level qubits (hard-core bosons, |1> = pair occupied). Ancilla k applies a controlled U^(2^k), where U is r first-order Trotter steps of size dt/r built from controlled-phase, RXX and RYY gates. An inverse QFT on the ancillas follows. The circuit contains no state preparation (reference state and ancilla Hadamards are supplied by the runner), no measurements, and no adiabatic stage.

Source equation run: `29fc3a92-a41d-4f7a-8945-c07f31a82c25`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..N-1: system pair-level qubits, qubit j = level j, |1> = pair occupied (example N=3: qubits 0,1,2)
- qubits N..N+t-1: QPE ancillas, ancilla k at qubit N+k controls U^(2^k), k=0 least significant (example t=4: qubits 3,4,5,6)
- Inverse QFTGate(t) acts on ancilla qubits [N..N+t-1] in that order; the ancilla output integer is int(bits,2) with qubit N as LSB, phi = value/2^t

## Assumptions

- Example parameters eps_j=j, G=0.5, dt=0.4, r=2 are chosen by me, since the abstract gives no parameters.
- The runner prepares ancillas in |+> and the system in a reference state with |1> = occupied pair.
- Blocked levels are removed, and the hard-core boson (pseudospin) mapping is used with all-to-all pair hopping of uniform strength G.
- Controlled RXX/RYY gates come from Qiskit's standard .control(1) of the standard gates, with no native-hardware decomposition.
- G>=0 is required, and dt>0 is assumed small enough that the spectrum fits one 2pi/dt window.

## Unresolved issues

- The abstract does not give the paper's actual algorithms for other native Hamiltonians (Ising/XY etc.), its gate sequences or its schedules, so this is a generic reconstruction.
- The Trotter error and phase wrapping of eigenenergies depend on the chosen dt and r, and are not tuned here.
- Adiabatic ground-state preparation and fidelity evaluation are not implemented.

## Equation mapping

- `eq_1`: background; no code location. Reduced pairing Hamiltonian is the physical target. The circuit realizes it through the qubit form in eq_2 and the Trotter product in eq_3.
- `eq_2`: implemented; _controlled_trotter_step and eps_eff in build_circuit. Spin mapping with n_j=|1><1|, hopping coefficient -G/2 (XX+YY), and the diagonal j=k terms absorbed as eps_j -> eps_j - G. The garbled trailing zero term is dropped.
- `eq_3`: implemented; _controlled_trotter_step; repetition loop in build_circuit. First-order Trotter step of size dt/r: controlled phase for the diagonal part and controlled RXX(-G h)·RYY(-G h) per pair j<k, repeated r times per U. Control is on the ancilla.
- `eq_4`: out_of_scope; no code location. Adiabatic state preparation and fidelity are state-preparation and analysis tasks, not part of this QPE operation. The runner supplies the input state.
- `eq_5`: implemented; build_circuit: controlled-U^(2^k) loop and QFTGate(t).inverse(). Ancilla k applies U^(2^k) via 2^k*r controlled Trotter steps, followed by an inverse QFT on the ancillas, so the readout phase is phi = frac(-E dt / 2pi).
- `eq_6`: background; no code location. Classical post-processing of measured bitstrings. With QFTGate-inverse and ancilla qubit N as LSB, phi = integer/2^t. No measurement is included in the circuit.

## Specification changes

- eq_2: Dropped the trailing term -(G/2)(N/2)*2*0 (identically zero). Diagonal j=k pairing terms are absorbed as eps_j -> eps_j - G and applied in the circuit as part of the diagonal phase. Reason: The term is notational noise, and the sum over j,k of P+_j P_k includes diagonal terms equal to n_j for hard-core bosons.
- eq_3, eq_2: Diagonal part is implemented as a controlled phase cp(-h*eps', ancilla, sys_j) on |1>, not as RZ. Reason: A controlled evolution needs the single-qubit global phase exp(-i h eps'/2), which RZ would omit. A controlled phase on n_j=|1><1| is exact.
- eq_5: Ancilla Hadamards are not included, and the reference system state is not prepared by the circuit. Reason: The task requires an operation with no input-state preparation. The runner must prepare ancillas in |+>^t and the system in the chosen reference state.
- eq_4, eq_6: Scope narrowed to the Trotterized QPE operation only. The adiabatic stage, fidelity analysis and counts-to-energy conversion are omitted. Reason: One construction is implemented. The prepared-state and analysis steps involve preparation, measurement and classical processing, which are excluded.
- eq_5, eq_3: U^(2^k) is formed by repeating the same r-step Trotter unitary 2^k times, with N+t<=12 and r*(2^t-1)<=2000 enforced. Spectrum rescaling into one 2pi window is left to the chosen eps, G and dt. Reason: This keeps Trotter error consistent across powers, and the size cap bounds the circuit.
