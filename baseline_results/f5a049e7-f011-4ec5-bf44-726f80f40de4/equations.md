# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Grover search over a real (classical, unstructured) database: given a classical table D mapping each index x in {0,...,N-1} (N = 2^n) to an m-bit record D[x], and a target record t, find an index x with D[x] = t. The oracle must be realised as an explicit circuit containing a quantumly accessible classical memory (a data-lookup unitary) that stores D, rather than as an abstract black box.

Scope: Smallest useful instance (chosen here as an assumption, no experiment_scope was supplied): n = 2 address qubits (N = 4 records), m = 1 data bit per record, database D = (D[0],D[1],D[2],D[3]) = (0,1,0,0), target t = 1, so exactly one marked index x* = 1 and a single Grover iteration suffices. Scope covers: (i) the data-lookup unitary U_D as a multi-controlled-X circuit, (ii) the phase oracle built as compute-lookup / compare-with-target / uncompute-lookup, (iii) one Grover iteration and measurement. Outside scope: the paper's specific memory architecture and gate-level optimisations, resource/gate counts, larger N or m, multi-bit comparison circuits beyond the generic phase-flip on |t>, and any claims about scalability of the quantumly accessible classical memory.

## Symbols

- $n$: number of address (index) qubits; domain: positive integer; n = 2 in scoped instance
- $N$: number of database records, N = 2^n; domain: positive integer; N = 4 in scoped instance
- $m$: bit-width of each database record; domain: positive integer; m = 1 in scoped instance
- $x$: database index / address, encoded big-endian on the address register as x = \sum_{i=0}^{n-1} 2^{i} a_i with a_{n-1} the first (most significant) qubit; domain: \{0,\dots,N-1\}
- $D[x]$: classical record stored at index x; domain: \{0,\dots,2^m-1\}; D=(0,1,0,0) in scoped instance
- $t$: target record being searched for; domain: \{0,\dots,2^m-1\}; t = 1 in scoped instance
- $M$: number of marked indices, M = |\{x : D[x]=t\}|; domain: \{0,\dots,N\}; M = 1 in scoped instance
- $U_D$: data-lookup unitary (quantumly accessible classical memory) that XORs D[x] into the data register; domain: unitary on n+m qubits
- $O_t$: Grover phase oracle marking indices with D[x]=t; domain: unitary on n (address) qubits, diagonal
- $G$: Grover iterate (oracle followed by diffusion); domain: unitary on n qubits
- $k$: number of Grover iterations; domain: non-negative integer; k = 1 in scoped instance
- $|s\rangle$: uniform superposition over all N indices; domain: n-qubit state

## eq_1: Quantumly accessible classical memory (data lookup)

$$
U_D\,|x\rangle_{\mathrm{addr}}|y\rangle_{\mathrm{data}} = |x\rangle_{\mathrm{addr}}|y \oplus D[x]\rangle_{\mathrm{data}},\qquad x\in\{0,\dots,N-1\},\ y\in\{0,1\}^m
$$

Defines the memory as a unitary that, given a (possibly superposed) address, XORs the stored classical record D[x] into an m-qubit data register; this is the standard semantics of a quantum-readable classical memory (QROM/QRACM) and is a bitwise XOR, not arithmetic addition.

Provenance: `abstract_inferred`. The abstract states the oracle contains a quantumly accessible classical memory storing the database; the XOR-lookup form is the standard mathematical meaning of such a memory. The paper's actual memory model is not given, so this is an inference.

Abstract evidence: The oracle contains a kind of quantumly accessible classical memory, which stores the database.

Equation assumptions:

- The memory is modelled as a reversible XOR lookup; the paper's specific memory architecture (fan-out, bucket-brigade, QROM, etc.) is unknown.

## eq_2: Simple circuit realisation of U_D for m = 1 (multi-controlled X per stored 1)

$$
U_D = \prod_{x\,:\,D[x]=1} C^{(x)}X,\qquad C^{(x)}X = |x\rangle\langle x|_{\mathrm{addr}}\otimes X_{\mathrm{data}} + (I-|x\rangle\langle x|)_{\mathrm{addr}}\otimes I_{\mathrm{data}}
$$

One explicit circuit for the lookup: for every address x whose stored bit is 1, apply an X on the data qubit controlled on the address register being exactly |x> (an n-controlled Toffoli with X gates on address lines where the bit of x is 0). The factors commute, so the product order is immaterial. For D=(0,1,0,0), n=2 this is a single Toffoli controlled on a_1=0, a_0=1, i.e. X on a_1, CCX(a_1,a_0 -> data), X on a_1.

Provenance: `assumption`. The abstract promises a simple circuit implementation but gives no construction; this is the most elementary correct realisation chosen for the scoped instance and should not be taken as the paper's circuit.

Equation assumptions:

- m = 1 (single data bit); for m > 1 one such product is used per data bit j with the condition on bit j of D[x].
- Multi-controlled X gates are available as primitives.

## eq_3: Grover phase oracle from lookup, compare, uncompute

$$
O_t = U_D^{\dagger}\,\big(I_{\mathrm{addr}}\otimes (I - 2|t\rangle\langle t|)_{\mathrm{data}}\big)\,U_D,\qquad O_t\,|x\rangle_{\mathrm{addr}}|0\rangle_{\mathrm{data}} = (-1)^{[D[x]=t]}\,|x\rangle_{\mathrm{addr}}|0\rangle_{\mathrm{data}}
$$

The oracle is the memory lookup, followed by a phase flip of the data register when it equals the target t, followed by the inverse lookup (U_D^\dagger = U_D since it is a product of self-inverse gates) to restore the data register to |0>. The bracket [D[x]=t] is 1 if true, else 0. For m=1, t=1 the middle operator is simply Z on the data qubit; for general t it is X^{\bar t} (multi-controlled Z) X^{\bar t} on the data register.

Provenance: `abstract_inferred`. The abstract says the Grover oracle contains the memory; the compute/compare/uncompute sandwich is the standard way a lookup memory yields a phase oracle for the predicate D[x]=t. The paper's exact comparison circuit is unknown.

Abstract evidence: A simple circuit implementation of the oracle for Grover’s quantum search of a real unstructured classical database is proposed.

Equation assumptions:

- The search predicate is exact equality of the stored record with a fixed target t.
- Data register is initialised to |0...0> and is uncomputed by the oracle (no garbage).

## eq_4: Grover iterate and uniform initial state

$$
|s\rangle = H^{\otimes n}|0\rangle^{\otimes n} = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle,\qquad G = \big(2|s\rangle\langle s| - I\big)\,O_t,\qquad 2|s\rangle\langle s| - I = H^{\otimes n}\big(2|0\rangle\langle 0| - I\big)H^{\otimes n}
$$

Standard Grover iteration: oracle followed by inversion about the mean, acting on the address register (data register returns to |0> after each oracle call).

Provenance: `standard_background`. Textbook Grover search; the abstract names Grover's search but does not restate these relations.

## eq_5: Iteration count and success probability

$$
k = \left\lfloor \frac{\pi}{4}\sqrt{\frac{N}{M}} \right\rfloor,\qquad P_{\mathrm{succ}}(k) = \sin^2\!\big((2k+1)\theta\big),\ \ \sin\theta = \sqrt{M/N};\qquad N=4,\ M=1:\ k=1,\ P_{\mathrm{succ}}=1
$$

Standard Grover iteration count (floor of the optimal real value) and exact success probability after k iterations. For the scoped instance N=4, M=1, theta = pi/6, a single iteration gives (2k+1)theta = pi/2 and the marked index is measured with probability exactly 1.

Provenance: `standard_background`. Standard Grover analysis; used only to fix k for the chosen instance. Requires M to be known (assumed M = 1 here).

Equation assumptions:

- M = 1 marked record is known in advance; unknown-M variants (e.g. exponential search) are out of scope.

## Registers

- addr: n = 2 qubits; Address/index register holding x = 2 a_1 + a_0 (big-endian, a_1 first); Grover search space.
- data: m = 1 qubits; Data register into which the memory XORs D[x]; initialised to |0>, phase-flipped on match, uncomputed to |0> inside each oracle call.

## Initial state

|0\rangle^{\otimes 2}_{\mathrm{addr}} \otimes |0\rangle_{\mathrm{data}}; after the first step the address register is |s\rangle = \frac{1}{2}(|00\rangle+|01\rangle+|10\rangle+|11\rangle) and the data register remains |0\rangle.

## Measurement

Measure both address qubits in the computational basis; read out x = 2 a_1 + a_0. For the scoped instance the outcome is x = 1 (bitstring 01) with probability 1 under ideal execution. The data qubit is expected to be |0> and may be measured as a sanity check.

## Classical postprocessing

Look up D[x] classically and check D[x] = t; if the check fails (possible for general N, M where P_succ < 1), rerun the circuit. For unknown M, use the standard randomised iteration-count schedule (out of scope).

## Algorithm steps

1. Prepare the uniform superposition over indices: apply H to each address qubit; leave the data qubit in |0>. (eq_4)
2. Oracle call, part 1 (memory lookup): apply U_D so the data qubit holds D[x] in superposition. For D=(0,1,0,0): X on a_1, Toffoli(a_1,a_0 -> data), X on a_1. (eq_1, eq_2)
3. Oracle call, part 2 (compare with target): apply the phase flip I - 2|t><t| on the data register; for t=1, m=1 this is a single Z on the data qubit, giving phase (-1)^{[D[x]=1]}. (eq_3)
4. Oracle call, part 3 (uncompute lookup): apply U_D^\dagger (= U_D, same gate sequence) to return the data qubit to |0>, completing O_t. (eq_1, eq_2, eq_3)
5. Diffusion: apply H^{\otimes 2}, then 2|00><00| - I (e.g. X on both address qubits, CZ, X on both, up to global phase), then H^{\otimes 2}. Together with the oracle this completes one Grover iterate G. (eq_4)
6. Repeat the oracle + diffusion steps k times in total; for N=4, M=1, k=1 so no further repetition is needed. (eq_5)

## Assumptions

- No experiment_scope was provided; the instance n=2, m=1, D=(0,1,0,0), t=1 was chosen as the smallest useful demonstration.
- The quantumly accessible classical memory is modelled as the reversible XOR lookup U_D of eq_1; the paper's concrete memory circuit is unknown and eq_2 is only one simple realisation.
- The search predicate is exact equality D[x] = t with a single marked index (M = 1).
- The data register is uncomputed inside each oracle call so that Grover's diffusion acts on a clean address register.
- Multi-controlled X/Z gates are treated as available primitives; no decomposition into a specific gate set is specified.

## Missing information

- The paper's actual oracle circuit construction, gate counts, depth, and how the memory is laid out (e.g. fan-out/multiplexer, bucket-brigade, or QROM-style unary/binary iteration).
- How multi-bit records (m > 1) and the comparison with the target t are implemented in the proposed circuit.
- Whether the proposed oracle uses additional ancilla qubits or garbage registers.
- Whether the paper addresses unknown numbers of matches M or only the single-match case.
- Any numerical results, resource estimates, or scalability claims for the memory with respect to N.
