import pytest

from algo_discovery.nemotron_equations import (
    SYSTEM,
    equation_key,
    external_spec,
    messages,
    parse_block,
)


def test_training_prompt_normalizes_whitespace_and_requests_index():
    assert messages(" Abstract\n text  ", 9) == [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": "Abstract:\nAbstract text\n\nStart equation: 9"}]


def test_numbered_block_and_end_marker():
    eqs, complete = parse_block("(9) H=H^\\dagger\n(10) U=I\n<END_EQUATIONS>", 9)
    assert complete and [e["index"] for e in eqs] == [9, 10]
    assert parse_block("(1) H=I", 1)[1] is False


def test_changing_equation_tag_is_not_new_equation_content():
    assert equation_key(r"U=I. \tag{1}") == equation_key(r"U=I. \tag{8}")
    assert equation_key(r"U=H \tag{1}") != equation_key(r"U=I \tag{1}")


def test_code_stage_export_preserves_predictions_without_inventing_evidence():
    result = {"status": "partial", "abstract": "We use the quantum Fourier transform.", "equations": [{"index": 1, "latex": "U=F"}]}
    wrapped = external_spec(result)
    spec = wrapped.specification
    assert spec.equations[0].latex == "U=F"
    assert spec.equations[0].abstract_quote is None
    assert spec.equations[0].provenance == "assumption"
    assert spec.registers == [] and spec.steps == [] and spec.missing_information
    assert wrapped.request().abstract == result["abstract"]


@pytest.mark.parametrize("text", ["", "Here are equations:\n(1) H=I", "(2) H=I", "(1) H=I\n(3) U=I"])
def test_reject_invalid_numbering_and_prose(text):
    with pytest.raises(ValueError):
        parse_block(text, 1)
