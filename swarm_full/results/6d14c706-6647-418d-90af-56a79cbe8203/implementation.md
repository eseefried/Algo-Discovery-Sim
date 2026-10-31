# Equation to Qiskit

Builds the first-order Trotter circuit (eq_1) for an illustrative transverse-field Ising Hamiltonian H=A+B, with A=-J sum Z_i Z_{i+1} and B=-g sum X_i. The circuit repeats n steps of exp(-iAt/n) then exp(-iBt/n), using ideal RZZ and RX gates. It has no state preparation, no measurement and no noise.

Source equation run: `7fa3ed95-c2c3-4c3e-b691-24604640a3c7`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'sys' with N=num_qubits qubits (example N=4): qubit i = spin site i, i=0..N-1
- Computational basis: qubit 0 is the least significant bit; Z/X act in the usual basis
- No ancilla qubits; no input-state preparation or measurement in the circuit

## Assumptions

- H=-J sum Z_i Z_{i+1} - g sum X_i, with A the ZZ part and B the X part.
- Periodic boundary adds the edge (N-1,0) only when N>2, to avoid double counting for N=2.
- time may be any finite real, including negative or zero.
- Trotter number is capped at 2000 and qubit count at 12.

## Unresolved issues

- The paper's actual Hamiltonian, gate error model and exact n* formula are not given in the abstract.
- The imperfect-gate behavior that creates the optimum n* is not modeled in this ideal circuit.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop over n Trotter steps applying RZZ gates (A part) then RX gates (B part). First-order Trotter product (exp(-iAt/n) exp(-iBt/n))^n realized for the concrete TFIM split A=-J sum ZZ, B=-g sum X.
- `eq_2`: background; no code location. Assumed error tradeoff model D(n)=a/n+bn is classical analysis of gate noise plus Trotter error. The unitary circuit is ideal, so it is not encoded.
- `eq_3`: out_of_scope; no code location. The optimum n*=sqrt(a/b) is a classical minimization of eq_2. It is not a circuit operation. The user selects n through the trotter_number parameter.

## Specification changes

- eq_1: Scoped to a concrete two-term transverse-field Ising Hamiltonian (open or periodic chain) with ideal gates. Hamiltonian parameters J, g, t, N are instance inputs. Reason: The specification leaves the Hamiltonian abstract, and a circuit needs concrete gates.
- eq_2, eq_3: Gate imperfection, the statistical-distance analysis and the n* optimization are not implemented in the circuit. Reason: The required output is a noise-free, measurement-free unitary circuit. Noise and the classical postprocessing are outside it.
- eq_1: The initial state |0...0>, the computational-basis measurement and the total variation distance computation are left to the runner. Reason: The circuit is an operation and must contain no state preparation or measurement.
