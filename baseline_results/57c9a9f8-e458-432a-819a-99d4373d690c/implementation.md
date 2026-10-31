# Equation to Qiskit

Qiskit module implementing the bipartite diagonal random-phase gate U (eq_1) on registers A (x) B for N = 2^n (n = 1 by default, two qubits), using the exact phase-gate decomposition of eq_6 generalized to n qubits per side via a Mobius (inclusion-exclusion) transform of the diagonal phases: global phase, single-qubit P gates, CP gates and multi-controlled phase gates. The Choi-state Bell pairs of eq_5 are NOT prepared inside the circuit (inputs are prepared by the runner); an option allocates idle reference registers A', B' so the runner can prepare |Phi>_{AA'}|Phi>_{BB'} and tomograph rho_{AA'}, whose spectrum equals that of rho = A A^dagger / N^2 (eq_2, eq_4).

Source equation run: `ff873f02-81d3-479e-9791-3e1bf272cf17`

Generation: **generated**; validation: **failed**.

Generated source was not executed: ValueError: Module constants must be literals or small numeric expressions.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: register B (1 qubit for N=2; least significant basis bit, index k)
- qubit 1: register A (1 qubit for N=2; most significant basis bit, index j)
- diagonal entry on |j>_A|k>_B is exp(i*phases[j*N+k]); for the example: |00> -> e^{0.3i}, |01>(A=0,B=1) -> e^{1.1i}, |10>(A=1,B=0) -> e^{2.4i}, |11> -> e^{0.7i}
- optional (include_reference_registers=true): qubits 2n..3n-1 = B' and 3n..4n-1 = A' idle reference registers for the runner-side Choi construction; total qubits 4n <= 12
- for general N=2^n: qubits 0..n-1 = B, n..2n-1 = A

## Assumptions

- Phases are i.i.d. uniform on [0, 2pi) when sampled from a seed; explicit phase lists are accepted as arbitrary finite reals (any diagonal unitary).
- N must be a power of two so that each subsystem is a qubit register; the N=2 example matches the specification's chosen instance.
- The runner performs the Choi-state preparation, tomography of rho_{AA'} and the entropy computation / ensemble averaging; the circuit itself only applies U.
- Natural logarithm for entropies in post-processing (not part of the module).

## Unresolved issues

- The exact mean von Neumann entropy (Borel-triangle result) and the moments of the unimodular ensemble are not reconstructed, so only the qualitative Theta(log N) scaling can be compared by sampling over seeds.
- Multi-controlled phase gates (qc.mcp) for n>=2 are exact but not optimized in gate count.
- Idle reference registers (when requested) contain no gates; some runners may flag unused qubits.

## Equation mapping

- `eq_1`: implemented; build_circuit (overall diagonal gate) and _extract_phases (explicit phases or i.i.d. uniform sampling via 'seed'). The circuit is exactly the diagonal unitary sum_{jk} e^{i phi_jk} |j><j|_A (x) |k><k|_B with A the most significant register; phases can be supplied or drawn uniformly i.i.d. from a seeded generator.
- `eq_2`: background; no code location. The reshaped unimodular matrix A and rho = A A^dagger/N^2 are classical reference objects; the module documents that the flat phase list reshaped row-major gives A_{jk}, but rho is not computed in the circuit.
- `eq_3`: background; no code location. Definition of operator Schmidt coefficients and Schmidt strength; a classical quantity used in post-processing, not part of the operation.
- `eq_4`: background; no code location. Identity K_Sch(U) = S(rho) for diagonal gates; motivates the construction but is a classical statement verified by the runner's post-processing.
- `eq_5`: background; no code location. Choi-state protocol: Bell-pair preparation and tomography are input preparation and measurement, which the runner performs; the module only optionally allocates idle reference registers A', B' so the runner can embed U into the Choi circuit.
- `eq_6`: implemented; _mobius_coefficients and the gate loop in build_circuit (global_phase, qc.p, qc.cp, qc.mcp). For N=2 the Mobius transform yields exactly c_B = phi_01-phi_00 (P on B), c_A = phi_10-phi_00 (P on A), c_AB = phi_11-phi_10-phi_01+phi_00 (CP on A,B) and global phase phi_00; for N=2^n the same expansion with multi-controlled phases. The Theta(log N) average-scaling statement is an ensemble property estimated by the runner over seeds, not encoded in a single circuit.

## Specification changes

- eq_5: Bell-pair preparation (H + CNOT on AA' and BB') is removed from the generated circuit; the circuit is only the operation U. Optionally, idle reference registers B', A' are allocated (include_reference_registers) so the runner can prepare |Phi>|Phi> and apply U on A,B. Reason: Implementation rules require an operation without input-state preparation or measurement; inputs are prepared by the runner.
- eq_1, eq_6: Generalized from the N=2 instance to N=2^n (n<=3 without reference registers, n<=3 with them, capped at 12 qubits) via a Mobius/inclusion-exclusion expansion of the phase vector into P, CP and multi-controlled phase gates. Reason: The construction must work for varying valid instance parameters; for n=1 it reduces exactly to eq_6.
- eq_6: The global phase e^{i phi_00} is retained via qc.global_phase rather than omitted. Reason: Keeps the circuit exactly equal (not just up to phase) to the specified diagonal unitary; harmless for the entanglement quantities.
- eq_1: Qubit ordering fixed as register B on qubits 0..n-1 (least significant) and A on qubits n..2n-1 (most significant), so that phases[j*N+k] is the entry on Qiskit basis integer x = j*N+k. Reason: Resolves the spec's 'A most significant' convention against Qiskit's little-endian qubit indexing.
