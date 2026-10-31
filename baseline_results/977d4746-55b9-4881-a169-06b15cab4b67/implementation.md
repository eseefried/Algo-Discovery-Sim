# Equation to Qiskit

Qiskit module implementing one coined discrete-time quantum walk on a cyclic lattice of 2^n sites with a Hadamard coin, a QFT-based conditional +/-1 shift, and T steps. The phenomenological spin (coin) and spatial (position) dephasing channels are implemented unitarily as Stinespring dilations with fresh ancilla qubits per step (ancillas assumed to start in |0> and to be traced out by the runner). Spin dephasing uses one ancilla per step (Ry then CZ onto the coin); spatial dephasing uses a flag ancilla plus n copy ancillas per step (Ry then Toffoli copies of the position bits). The circuit is measurement-free and unitary; sampling P(x,T) and the variance diagnostic are left to the runner.

Source equation run: `53b1228a-3c45-4c4c-9671-0ddffb1215ba`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-2: pos[0..2], lattice site x mod 8 in binary (qubit 0 least significant); walker starts at |000> = site 0
- qubit 3: coin[0], spin qubit; |0> = up (shift +1), |1> = down (shift -1); start |0>
- qubits 4-6: env[0..2], one fresh spin-dephasing ancilla per step (steps 1,2,3), assumed prepared in |0> and traced out after the circuit
- (general layout) for p_x > 0 each step additionally allocates 1 flag ancilla followed by n copy ancillas after that step's spin ancilla; total qubits = n + 1 + T*([p_s>0] + (n+1)*[p_x>0]) <= 12

## Assumptions

- Environment ancillas (env register) are prepared in |0> by the runner and traced out; otherwise the circuit does not realize the dephasing channels.
- Walker input |x=0>|up> = |000>|0> is prepared by the runner; the operation itself is valid for any input on pos and coin.
- Hadamard coin, Markovian per-step dephasing, and the channel order (W, spin, spatial) follow the math specification's stated choices, not the paper.
- Cyclic lattice of 2^n sites; for T < 2^(n-1) starting from site 0 no wrap-around occurs.

## Unresolved issues

- The paper's actual phenomenological decoherence model and its parametrization are unknown; dephasing form is an assumption.
- Quasi-stationary (non-Markovian) spin dephasing, coherence length, and the discrete Wigner-function analysis are not modelled.
- Ancilla cost grows as T*(1 + (n+1)) when both channels are enabled, so only very small instances fit under the 12-qubit cap with spatial dephasing on.

## Equation mapping

- `eq_1`: implemented; _apply_coin (qc.h on coin). Hadamard coin applied to the spin qubit at the start of each step.
- `eq_2`: implemented; _apply_shift (QFTGate, p/cp phases, inverse QFTGate). Conditional +/-1 shift mod 2^n realized as a QFT adder: unconditional +1 phases plus coin-controlled -2 phases give +1 for coin |0> and -1 for coin |1>.
- `eq_3`: implemented; build_circuit step loop (comment 'eq_3'). Each step applies the coin then the shift, W = S(1 x C).
- `eq_4`: implemented; _apply_spin_dephasing (ry on ancilla, cz onto coin). Stinespring dilation of the coin dephasing channel with a fresh ancilla per step; tracing the ancilla yields (1-p_s)rho + p_s Z rho Z exactly.
- `eq_5`: implemented; _apply_spatial_dephasing (ry on flag, ccx copies of position bits). Stinespring dilation of position dephasing: with amplitude sqrt(p_x) the position bits are copied into fresh ancillas; tracing gives (1-p_x)rho + p_x sum_x |x><x| rho |x><x|. Disabled in the example instance (p_x = 0) to respect the 12-qubit cap at n=3, T=3.
- `eq_6`: implemented; build_circuit step loop (comment 'eq_6'); ordering W, then spin, then spatial dilation. The per-step composition E_x(E_s(W rho W^dag)) is realized unitarily on system+environment; the position distribution P(x,t) is obtained by the runner by measuring/tracing the pos register and ignoring env and coin.
- `eq_7`: background; no code location. Variance diagnostic is classical post-processing of P(x,T); not part of the circuit operation.

## Specification changes

- eq_4, eq_5, eq_6: Non-unitary dephasing channels are implemented as unitary Stinespring dilations with fresh environment ancillas per step (1 ancilla per step for spin dephasing; n+1 per step for spatial dephasing). The channel is recovered only after the runner traces out (ignores) the env register; ancillas are assumed to be supplied in |0>. Reason: The deliverable must be a measurement-free unitary circuit without reset or dynamic circuits, so Kraus channels cannot be applied directly.
- eq_5: Spatial dephasing is optional (p_x = 0 in the example) and limited by the 12-qubit cap; with n=3, T=3 the spin-only channel fits (7 qubits) while enabling p_x would need 19 qubits. Smaller instances (e.g. n=2, T=2, both channels: 11 qubits) can enable both. Reason: Qubit budget; the specification's tiny instance with both channels cannot be dilated within 12 qubits.
- eq_2: Shift implemented via QFT adder (QFTGate, phases 2*pi*2^l/2^n on Fourier-basis qubit l, coin-controlled sign flip, inverse QFTGate) rather than a multi-controlled-X incrementer/decrementer. Reason: Equivalent unitary on the cyclic register; uses the recommended QFTGate with Qiskit's little-endian qubit order (qubit l of the Fourier register carries phase weight 2^l).
- eq_6, eq_7: Measurement of the position register, histogramming, signed-site reinterpretation, and variance/fit are excluded from the module. Reason: The module returns an operation only; experiment steps are the runner's responsibility.
