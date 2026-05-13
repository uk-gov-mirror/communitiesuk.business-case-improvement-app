import pytest
from apps.triage.flow import (
    get_question,
    get_next,
    get_result_from_answers,
    get_first_question_slug,
    QUESTION_SLUGS,
    QUESTIONS,
)

# ── Question definitions ──────────────────────────────────────────────────────


def test_first_question_exists():
    slug = get_first_question_slug()
    assert slug is not None
    assert get_question(slug) is not None


def test_all_questions_have_required_fields():
    for q in QUESTIONS:
        assert "slug" in q, f"Question missing slug: {q}"
        assert "title" in q, f"Question missing title: {q}"
        assert "type" in q, f"Question missing type: {q}"
        assert "choices" in q, f"Question missing choices: {q}"
        assert len(q["choices"]) > 0, f"Question has no choices: {q['slug']}"


def test_get_question_returns_correct_question():
    slug = QUESTION_SLUGS[0]
    q = get_question(slug)
    assert q is not None
    assert q["slug"] == slug


def test_get_question_returns_none_for_invalid_slug():
    assert get_question("not-a-real-question") is None


def test_all_question_slugs_are_unique():
    assert len(QUESTION_SLUGS) == len(set(QUESTION_SLUGS))


# ── Routing ───────────────────────────────────────────────────────────────────


def test_routing_below_12k_continues_to_next_question():
    next_step = get_next("total-value-of-business-case", "below-12k")
    assert next_step is not None
    assert not next_step.startswith("result:")


def test_routing_above_12k_continues_to_next_question():
    next_step = get_next("total-value-of-business-case", "above-12k")
    assert next_step is not None


def test_routing_raises_for_unknown_question():
    with pytest.raises(KeyError):
        get_next("not-a-real-question", "any-answer")


def test_last_question_routes_to_calculate_result():
    last_slug = QUESTION_SLUGS[-1]
    last_question = get_question(last_slug)
    first_choice_value = last_question["choices"][0][0]
    next_step = get_next(last_slug, first_choice_value)
    assert next_step == "calculate-result"


def test_all_routing_rules_point_to_valid_questions_or_results():
    from apps.triage.flow import ROUTING

    for (slug, answer), next_step in ROUTING.items():
        if next_step == "calculate-result":
            continue
        if next_step.startswith("result:"):
            continue
        assert get_question(next_step) is not None, (
            f"Routing rule ({slug}, {answer}) -> {next_step} "
            f"points to a question that doesn't exist"
        )


# ── Result calculation ────────────────────────────────────────────────────────


def test_result_below_12k_not_part_of_programme():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "below-12k",
            "new-project-or-programme": "no",
        }
    )
    assert result == "you-do-not-need-a-business-case"


def test_result_below_12k_part_of_programme():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "below-12k",
            "new-project-or-programme": "yes",
        }
    )
    assert result == "speak-to-someone-first"


def test_result_above_12k_over_2m_not_novel():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "above-12k",
            "is-business-case-less-than-two-million": "no",
            "novel-contentious-or-repercussive": "no",
        }
    )
    assert result == "you-need-to-start-a-full-business-case"


def test_result_above_12k_under_2m_not_novel():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "above-12k",
            "is-business-case-less-than-two-million": "yes",
            "novel-contentious-or-repercussive": "no",
        }
    )
    assert result == "you-need-to-start-a-business-justification-case"


def test_result_above_12k_under_2m_novel():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "above-12k",
            "is-business-case-less-than-two-million": "yes",
            "novel-contentious-or-repercussive": "yes",
        }
    )
    assert result == "you-need-to-start-a-full-business-case-novel-or-complex"


def test_result_above_12k_over_2m_novel():
    result = get_result_from_answers(
        {
            "total-value-of-business-case": "above-12k",
            "is-business-case-less-than-two-million": "no",
            "novel-contentious-or-repercussive": "yes",
        }
    )
    assert result == "you-need-to-start-a-full-business-case-novel-or-complex"


def test_result_always_returns_a_slug():
    """No combination of answers should return None."""
    result = get_result_from_answers({})
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
