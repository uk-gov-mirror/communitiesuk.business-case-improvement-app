import pytest
from django.test import Client
from django.urls import reverse
from apps.triage.models import BusinessCase, BusinessCaseTriageResponse
from apps.triage.flow import get_first_question_slug, QUESTION_SLUGS
from apps.triage.slugs import *

@pytest.fixture
def client(db):
    return Client()


@pytest.fixture
def started_session(client):
    """Start a triage session and return the client with session set up."""
    client.get(reverse("triage:start"))
    return client

# Pages load

def test_3_stage_process_page_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "you-need-to-follow-a-three-stage-process"}))
    assert resp.status_code == 200


def test_below_12k_no_programme_not_digital_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "do-not-need-a-business-case-no-programme-not-digital"}))
    assert resp.status_code == 200


def test_corporate_spend_fbp_exit_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "exit-to-download-template-corporate-spend-fbp-route"}))
    assert resp.status_code == 200


def test_hrbp_contingent_labour_exit_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "exit-to-download-template-hrbp-contingent-labour-route"}))
    assert resp.status_code == 200


def test_procurement_template_exit_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "exit-to-download-template-procurement-route"}))
    assert resp.status_code == 200


def test_procurement_route_digital_spend_page_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "procurement_route_digital_spend"}))
    assert resp.status_code == 200


def test_speak_to_research_team_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "you-need-to-speak-to-the-research-team"}))
    assert resp.status_code == 200


def test_below_12k_no_programme_digital_loads(client):
    resp = client.get(reverse("triage:result", kwargs={"slug": "do-not-need-a-business-case-no-programme-digital"}))
    assert resp.status_code == 200


def test_index_page_loads(client):
    resp = client.get(reverse("triage:index"))
    assert resp.status_code == 200


def test_start_redirects_to_first_question(client, db):
    resp = client.get(reverse("triage:start"))
    assert resp.status_code == 302
    assert get_first_question_slug() in resp["Location"]


def test_first_question_page_loads(started_session, db):
    slug = get_first_question_slug()
    resp = started_session.get(reverse("triage:question", kwargs={"slug": slug}))
    assert resp.status_code == 200


def test_invalid_question_slug_redirects(started_session, db):
    resp = started_session.get(
        reverse("triage:question", kwargs={"slug": "not-a-real-question"})
    )
    assert resp.status_code == 302


#  Validation


def test_question_requires_answer(started_session, db):
    slug = get_first_question_slug()
    resp = started_session.post(
        reverse("triage:question", kwargs={"slug": slug}),
        data={},
    )
    assert resp.status_code == 200
    assert b"Select an answer" in resp.content


def test_question_with_answer_redirects(started_session, db):
    slug = get_first_question_slug()
    resp = started_session.post(
        reverse("triage:question", kwargs={"slug": slug}),
        data={"answer": "above-12k"},
    )
    assert resp.status_code == 302


#  Session / answer saving


def test_answers_are_saved_to_database(started_session, db):
    slug = get_first_question_slug()
    started_session.post(
        reverse("triage:question", kwargs={"slug": slug}),
        data={"answer": "above-12k"},
    )
    session = BusinessCaseTriageResponse.objects.filter(completed_at=None).last()
    assert session is not None
    assert session.answers.get(slug) == "above-12k"


def test_start_clears_previous_session(client, db):
    # Start once
    client.get(reverse("triage:start"))
    assert BusinessCaseTriageResponse.objects.count() == 1

    # Start again
    client.get(reverse("triage:start"))
    assert BusinessCaseTriageResponse.objects.count() == 1


def test_procurement_template_route(client, db):
    client.get(reverse("triage:start"))

    answers = {
        total_value_of_business_case: "between-12k-and-2m",
        novel_repercussive_contentious_hmt_consent: "no",
        is_this_request_a_pilot_with_potential_to_be_a_larger_proposal: "no",
        is_this_request_part_of_a_wider_programme_with_existing_business_case: "no",
        any_other_business_cases_that_are_connected_to_this_work: "*",
        where_is_the_budget_held: "*",
        is_this_a_retrospective_case: "*",
        which_option_describes_what_you_are_trying_to_do: procure_goods_and_services_from_third_party,
        which_best_describes_your_spend: spend_on_corporate_activities,
        give_your_bjc_a_name: "*",
        provide_a_high_level_summary: "*"
    }

    for slug in QUESTION_SLUGS:
        answer = answers.get(slug)
        if answer:
            client.post(
                reverse("triage:question", kwargs={"slug": slug}),
                data={"answer": answer},
            )

    session = BusinessCaseTriageResponse.objects.filter(completed_at__isnull=False).last()
    assert session is not None
    assert session.result != "in-progress"
    assert session.result != ""
    
    business_case = BusinessCase.objects.last()
    assert business_case is not None
    assert business_case.created_at is not None
    assert business_case.modified_at is not None
    assert business_case.deleted_at is None


#  Result pages


def test_result_page_loads(client, db):
    resp = client.get(
        reverse(
            "triage:result", kwargs={"slug": "you-need-to-start-a-full-business-case"}
        )
    )
    assert resp.status_code == 200


def test_invalid_result_slug_returns_404(client, db):
    resp = client.get(reverse("triage:result", kwargs={"slug": "not-a-real-result"}))
    assert resp.status_code == 404
