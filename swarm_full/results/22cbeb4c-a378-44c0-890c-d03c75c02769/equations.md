# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Unitary Permutation: given n unitary gates U_1..U_n and a permutation sigma of {1..n}, apply the gates in the order given by sigma, i.e. implement U_{sigma(n)} o ... o U_{sigma(1)}. Complexity is measured as the number of gate calls in the standard query model, or as the number of quantum switches in the second-order model.

Scope: Complexity bounds only: upper and lower bounds on the number of quantum switches and of queries. The abstract gives no explicit circuit, so no circuit construction is reconstructed. The lower bound for queries assumes an extra restriction on the gate family.

## Symbols

- $n$: number of unitary gates; domain: positive integer
- $U_i$: i-th input unitary gate; domain: i in {1..n}
- $\sigma$: permutation giving the order of application; domain: permutations of {1..n}
- $\epsilon$: arbitrary positive constant in the query lower bound; domain: real, epsilon>0

## eq_1: Target operation

$$
U_{\sigma(n)}\circ\cdots\circ U_{\sigma(1)}
$$

Composition of the gates in the order specified by sigma.

Provenance: `abstract_explicit`. Stated in the abstract as the quantity to be performed.

Abstract evidence: U_{\sigma(n)}\circ\ldots\circ U_{\sigma(1)}

## eq_2: Switch complexity

$$
n\log_2(n)+\Theta(n)
$$

Number of quantum switches that is necessary and sufficient.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: n\log_{2}(n)+\Theta(n)

## eq_3: Query upper bound

$$
n^2-2n+4
$$

Number of calls that suffice in the standard circuit model.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: n^{2}-2n+4

## eq_4: Query lower bound

$$
n^2-o(n^{7/4+\epsilon})
$$

Number of queries required, under an additional assumption on the gate family.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: n^{2}-o(n^{7/4+\epsilon})

Equation assumptions:

- Additional unspecified assumption on the family of gates

## Registers

- data: unknown (a system on which the gates act) qubits; Holds the quantum state transformed by the gates; dimension not given in the abstract
- control: unknown qubits; Assumed to encode sigma classically or as a control for switches; not specified in the abstract

## Measurement

None specified in the abstract. The task is implementing a unitary (the composition in eq_1), so no measurement is part of the stated problem; any verification would measure the output data register after applying the circuit to a test state (assumed).

## Classical postprocessing

None specified. The only classical input is the permutation sigma, which determines the order of application. No result decoding is described in the abstract.

## Algorithm steps

1. Take the input state on the data register and the description of sigma as the control; the sequence must realize the composition in eq_1. (eq_1)
2. Query model: realize the composition by a circuit calling the gates, with the number of calls bounded by the stated upper bound; the actual construction (via the permutation-as-substring connection) is not given in the abstract. (eq_3, eq_4)
3. Switch model: realize the composition with quantum switches, using n log2(n)+Theta(n) switches; the construction is not given in the abstract. (eq_2)

## Assumptions

- The registers listed are generic placeholders, not taken from the abstract.
- No measurement is part of the problem; any measurement is an assumed verification step.

## Missing information

- Circuit construction, registers and initial state are not given in the abstract.
- The additional assumption on the gate family is not specified.
- The permutation-as-substring connection is not detailed.
- Explicit step-by-step constructions achieving the stated bounds are absent.
