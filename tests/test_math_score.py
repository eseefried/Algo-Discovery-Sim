import pytest

from algo_discovery.math_score import (
    MATCH_THRESHOLD,
    Candidate,
    pieces,
    score_paper,
    similarity,
    tokens,
)

IDF = {}


def sim(a, b):
    return similarity(Candidate(a, "a"), Candidate(b, "b"), IDF)


def test_formatting_differences_do_not_change_tokens():
    assert tokens(r"H=\frac{1}{2}(\hat{x}^{2}+\hat{p}^{2})\;. \tag{4}") == tokens(
        r"H = \tfrac{1}{2}\left(\hat x^2 + \hat p^2\right)"
    )
    assert tokens(r"\ket{\psi}") == tokens(r"|\psi\rangle")


def test_renamed_variables_still_score_as_a_match():
    assert sim(r"\sum_{k=0}^{N-1} a_k |k\rangle", r"\sum_{j=0}^{M-1} b_j |j\rangle") > 0.7


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (r"H = -\gamma A - |w\rangle\langle w|", r"\Pr[\text{fail}] = (1-p)^m"),
        (r"(2d+1)^k \geq n", r"C_0 = 2|s_c\rangle\langle s_c| - I_d"),
    ],
)
def test_unrelated_equations_stay_below_match_threshold(a, b):
    assert sim(a, b) < MATCH_THRESHOLD


def test_combined_agent_line_matches_one_paper_equation():
    agent = pieces(r"C_0 = 2|s_c\rangle\langle s_c| - I_d,\qquad C = I_N\otimes C_0", "eq_1")
    paper = Candidate(r"C_{0}=2|s_{c}\rangle\langle s_{c}|-I_{d},", "p1")
    assert max(similarity(a, paper, IDF) for a in agent) > 0.95


def test_score_paper_counts_matches_and_recovered_core_equations():
    agent = [{"id": "eq_1", "latex": r"H = -\gamma A - |w\rangle\langle w|"}]
    paper = [
        {"id": "p1", "latex": r"H=-\gamma A-|w\rangle\langle w|, \tag{14}", "equation_number": 14},
        {"id": "p2", "latex": r"\Pr[\text{fail}] = (1-p)^m", "equation_number": 15},
        {"id": "p3", "latex": r"x = y + z + w", "equation_number": None},
    ]
    result = score_paper(agent, paper, IDF)
    assert result["matched_agent_equations"] == result["strong_agent_matches"] == 1
    assert result["matches"][0]["paper_id"] == "p1"
    assert result["main_equation_source"] == "numbered_fallback"
    assert result["main_paper_equations"] == 2  # without labels, numbered equations count
    assert result["main_equations_recovered"] == 1


def test_labelled_main_equations_replace_the_numbered_fallback():
    agent = [{"id": "eq_1", "latex": r"H = -\gamma A - |w\rangle\langle w|"}]
    paper = [
        {"id": "p1", "latex": r"H=-\gamma A-|w\rangle\langle w|", "equation_number": 1},
        {"id": "p2", "latex": r"\Pr[\text{fail}] = (1-p)^m", "equation_number": 2},
        {"id": "p3", "latex": r"x = y + z + w", "equation_number": 3},
    ]
    result = score_paper(agent, paper, IDF, main_ids=["p1"])
    assert result["main_equation_source"] == "labelled"
    assert result["main_paper_equations"] == result["main_equations_recovered"] == 1
    assert result["recall"] > 0.95


def test_one_agent_equation_recovers_at_most_one_repeated_paper_equation():
    qft = r"QFT|x\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}e^{2\pi i xk/N}|k\rangle"
    agent = [{"id": "eq_1", "latex": qft}]
    paper = [
        {"id": f"p{i}", "latex": qft.replace("x", v), "equation_number": i}
        for i, v in enumerate("xab", 1)
    ]
    result = score_paper(agent, paper, IDF)
    assert result["main_equations_recovered"] == 1  # not 3: the paper repeats one idea


def test_chained_equality_side_matches_a_single_paper_term():
    agent = pieces(r"S = \sum_{j=1}^{m} w_j x_j = w\cdot x", "eq_1")
    paper = Candidate(r"\sum_{m=1}^{N}a_{m}x_{m}", "p1")
    assert max(similarity(a, paper, IDF) for a in agent) >= MATCH_THRESHOLD
