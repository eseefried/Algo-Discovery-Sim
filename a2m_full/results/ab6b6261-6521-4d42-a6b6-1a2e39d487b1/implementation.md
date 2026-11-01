# Equation to Qiskit

Lossy-hop Grover walk on the complete graph with self-loops: T repetitions of [oracle phase flip U_w, then an ancilla-dilated hop]. Each hop uses a fresh ancilla rotated by Ry(theta) with sin(theta/2)=eps, and R_s=2|s><s|-I is applied on the search register controlled on ancilla=0, with the controlled global phase handled explicitly. Input |s> preparation, measurement, and the eps-scaling sweeps are left to the runner.

Source equation run: `1a4a0502-c454-4ac4-be94-c80d3472478f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: search register, little-endian (qubit i is bit i of the vertex index); runner prepares |s> here
- Qubits n..n+T-1: one fresh hop-failure ancilla per step; qubit n+t is used in step t (starts |0>, |1> means the hop failed)
- Example (n=3, steps=2): search = qubits 0,1,2; anc = qubits 3,4

## Assumptions

- eps is the same at every step and lies in [0,1].
- eps is given directly or as c/sqrt(N), with exactly one of eps or c supplied.
- The barrier affects only the hop, not the oracle.
- The runner prepares |s> on the search qubits and leaves the ancillas in |0>.
- The default number of steps is floor(pi/4*sqrt(N)) when steps is omitted.
- The marked index is little-endian, with qubit i holding bit i.

## Unresolved issues

- The exact hop-failure model of the source paper (coherent versus incoherent) is unknown. The coherent ancilla dilation here is a modeling choice.
- The scaling theorem and its constants are not reproduced.
- The continuous-time version and the barrier-reduced hopping amplitude are not implemented.
- The ancilla-per-step design limits the walk length to T<=12-n steps.

## Equation mapping

- `eq_1`: implemented; _lossy_hop (realized through the dilation). The lossy hop sqrt(1-eps^2) R_s + eps I is realized as the ancilla-dilated unitary. The ancilla=0 block gives sqrt(1-eps^2) R_s and the ancilla=1 block gives eps I.
- `eq_2`: implemented; _lossy_hop. Ry(theta) with theta=2*asin(eps) on a fresh ancilla, followed by R_s on the search register controlled on ancilla=0, including the correct controlled global phase of R_s.
- `eq_3`: implemented; _oracle and the loop in build_circuit. Each walk step is U_w followed by the lossy hop, repeated T times. The oracle is the phase flip I-2|w><w| on the marked index given in the instance. The initial |s> preparation is left to the runner. P(w) is computed by the runner.
- `eq_4`: background; build_circuit (default steps). Ideal Grover analysis. It is used only to choose the default T=floor(pi/4*sqrt(N)) when steps is omitted. No rotation-angle formula is coded.
- `eq_5`: out_of_scope; no code location. The scaling dichotomy and its proof are not constructed. The circuit only accepts eps directly or as c/sqrt(N) so that sweeps can be done outside the module.

## Specification changes

- eq_3: The initial H^n preparation of |s> is omitted from the circuit. Reason: The task requires an operation without input-state preparation. The runner must supply |s> on the search register, with ancillas in |0>.
- eq_3: The black-box oracle U_w is implemented as an explicit phase flip on the marked index 'marked' from the instance, with one oracle per step. Reason: A concrete gate-level operation is needed. The oracle is not a hardcoded output state.
- eq_1, eq_2: A fresh ancilla is used for every step and is never reset, measured, or recombined. The resulting operation is a unitary dilation. The exact product of H_eps operators appears only in the all-ancillas-0 post-selected block. Later steps act on the ancilla=1 failure branches as well, so the total state is not literally (H_eps U_w)^T|s>. Reason: This follows the specification's fresh-ancilla option and the no-reset, no-dynamic-circuit rule. Postselection on all ancillas=0 can be done by the runner.
- eq_2: The controlled-R_s global phase is made explicit: the ancilla=0 branch applies D = 2|0><0| - I between Hadamard layers, built as a -1 phase on ancilla=0 combined with a -1 phase on (search=0, ancilla=0). Reason: Controlling only the central multi-controlled Z would implement -R_s, which would flip the sign of the sqrt(1-eps^2) term relative to eps I.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to discrete-time walks with n in 2..4 search qubits, a single marked vertex, and n+T<=12. The eps sweeps, optimal-T search, and the continuous-time and physical barrier models are excluded. Reason: Matches the stated reconstruction scope and the 12-qubit cap.
