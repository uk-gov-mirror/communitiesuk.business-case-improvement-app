import pytest
from apps.triage.flow import (
    get_question,
    get_next,
    get_result_from_answers,
    get_first_question_slug,
    QUESTION_SLUGS,
    QUESTIONS,
    DIGITAL_STRING
)

from apps.triage.slugs import *

#  Question definitions

def test_first_question_exists():
    slug = get_first_question_slug()
    assert slug is not None
    assert get_question(slug) is not None


#handle types
def test_all_questions_have_required_fields():
    for q in QUESTIONS:
        assert "slug" in q, f"Question missing slug: {q}"
        assert "title" in q, f"Question missing title: {q}"
        assert "type" in q, f"Question missing type: {q}"

        if q["type"] == "checkbox" or q["type"] == "radio" or q["type"] == "select":
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


#  Routing
def test_routing_raises_for_unknown_question():
    with pytest.raises(KeyError):
        get_next("not-a-real-question", "any-answer")


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


#  Result/Exit screen Routing

def test_over_2m_exit_screen_routing():
    # act
    result = get_next(total_value_of_business_case, "above-2m")
    exit = get_result_from_answers({total_value_of_business_case: "above-2m"})

    # assert
    assert result == "calculate-result"
    assert exit == "you-need-to-do-3-stage-process"


def test_result_always_returns_a_slug():
    """No combination of answers should return None."""
    result = get_result_from_answers({})
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_procurement_routes_to_calculate_result_1():
    # arrange
    procurement_answers = [
        "between-12k-and-2m",
        "no",
        "no",
        "no",
        "Any Answer",
        "Any Answer",
        "Any Answer",
        procure_goods_and_services_from_third_party,
        spend_on_corporate_activities,
        "title",
        "details"
    ]

    counter: int = 0
    step: str = total_value_of_business_case
    answers: dict = {}

    # act 
    while step != "calculate-result":
        answers[step] = procurement_answers[counter]
        step = get_next(step, procurement_answers[counter])
        counter += 1

    result = get_result_from_answers(answers)

    # assert
    assert step == "calculate-result"
    assert result == you_need_to_start_a_business_justification_case


def test_procurement_routes_to_calculate_result_2():
    # arrange
    procurement_answers = [
        "between-12k-and-2m",
        "no",
        "no",
        "no",
        "Any Answer",
        "Any Answer",
        "Any Answer",
        procure_goods_and_services_from_third_party,
        procuring_something_else,
        "no",
        "Any Answer",
        "title",
        "details"
    ]

    counter: int = 0
    step: str = total_value_of_business_case
    answers: dict = {}

    # act 
    while step != "calculate-result":
        answers[step] = procurement_answers[counter]
        step = get_next(step, procurement_answers[counter])
        counter += 1

    result = get_result_from_answers(answers)

    # assert
    assert step == "calculate-result"
    assert result == you_need_to_start_a_business_justification_case


def test_procurement_routes_including_digital_routes_away_from_procurement():
    # arrange
    procurement_answers = [
        "between-12k-and-2m",
        "no",
        "no",
        "no",
        "Any Answer",
        DIGITAL_STRING,
        "Any Answer",
        procure_goods_and_services_from_third_party,
        spend_on_corporate_activities,
        "title",
        "details"
    ]

    counter: int = 0
    step: str = total_value_of_business_case
    answers: dict = {}

    # act 
    while step != "calculate-result":
        answers[step] = procurement_answers[counter]
        step = get_next(step, procurement_answers[counter])
        counter += 1

    result = get_result_from_answers(answers)

    # assert
    assert step == "calculate-result"
    assert result == "we-could-not-find-the-right-process-for-you"

    