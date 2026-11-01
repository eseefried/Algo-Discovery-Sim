# Equation to Qiskit

build_circuit(instance) returns the measurement-free, bound unitary for the noisy first-order Trotter product U_n = [RX(2gt/n+eps) on both qubits . RZZ(2t/n+eps)]^n for the 2-qubit transverse-field Ising model H=Z0Z1+g(X0+X1). Every gate carries a coherent over-rotation eps. The distance scan, exact reference, fits and n* comparison are classical postprocessing, so they are not in the circuit.

Source equation run: `83835e20-1074-4068-8ea2-3e85b5884a14`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system qubit 0, least significant bit of the computational-basis index
- qubit 1: system qubit 1, most significant bit of the computational-basis index
- No ancillas; total 2 qubits; the runner prepares the input state (|00> in the specification)

## Assumptions

- The coherent over-rotation noise model is used with a sign-fixed, user-supplied eps.
- The first-order (p=1) product formula is used, with order RZZ then RX per step.
- Qiskit conventions apply: RZZ(θ)=exp(-iθ ZZ/2) and RX(θ)=exp(-iθ X/2).
- Defaults are g=1, t=1, n=1, eps=0 when keys are omitted.

## Unresolved issues

- The paper's actual noise model, definition of statistical distance, and constants for n* are not known. Coherent noise is a substitute assumption.
- With coherent errors, the noisy and Trotter errors may cancel, so D(n) may not be monotone and the numerical argmin may not match n*=sqrt(a/(b eps)) exactly.
- The instance (2-qubit TFIM, g=1, t=1) was chosen for this reconstruction and was not specified by the abstract.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop applying qc.rzz(theta_zz,0,1), qc.rx(theta_x,0), qc.rx(theta_x,1) n times. Noisy first-order Trotter product with eps added to each gate angle. The rightmost factor RZZ is applied first, then RX on both qubits.
- `eq_2`: out_of_scope; no code location. Total variation distance and the exact reference exp(-iHt)|00> are classical postprocessing. They are not part of the unitary operation.
- `eq_3`: background; no code location. The a/n + b n eps tradeoff model motivates the scan over n but does not enter the circuit. The fitting is classical.
- `eq_4`: background; no code location. The closed form n* is a classical comparison target derived from eq_3. The circuit does not use it.
- `eq_5`: out_of_scope; no code location. Higher-order scaling for p>1 is not implemented. Only the first-order formula is built.

## Specification changes

- eq_1: Scope narrowed to one (g, t, n, eps) instance per call on a fixed 2-qubit TFIM. The Trotter number n is capped at 5000 and eps is limited to |eps|<=1. The scan over n and eps is left to the runner. Reason: build_circuit must return a single operation, not an experiment.
- eq_1: The gate convention is made explicit: exp(-i(t/n)ZZ)=RZZ(2t/n) and exp(-i(gt/n)X)=RX(2gt/n) in Qiskit. The same eps is added to the RZZ and RX angles, and RX acts on both qubits. Reason: This fixes the ambiguity in the notation R~_sigma and matches the stated Qiskit definitions.
- eq_2, eq_3, eq_4, eq_5: These equations are not implemented in the circuit and are treated as classical postprocessing or background. Reason: The circuit has to be a measurement-free operation without simulation or reference computation.
