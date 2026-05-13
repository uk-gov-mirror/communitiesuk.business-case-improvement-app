import pytest
from django.test import Client
from django.urls import reverse
from apps.triage.models import TriageSession
from apps.triage.flow import get_first_question_slug, QUESTION_SLUGS


@pytest.fixture
def client(db):
    return Client()


@pytest.fixture
def started_session(client):
    """Start a triage session and return the client with session set up."""
    client.get(reverse("triage:start"))
    return client


# Pages load


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
    session = TriageSession.objects.filter(completed_at=None).last()
    assert session is not None
    assert session.answers.get(slug) == "above-12k"


def test_start_clears_previous_session(client, db):
    # Start once
    client.get(reverse("triage:start"))
    assert TriageSession.objects.count() == 1

    # Start again
    client.get(reverse("triage:start"))
    assert TriageSession.objects.count() == 1


def test_session_result_set_after_completion(client, db):
    """Complete the full flow and check result is saved."""
    client.get(reverse("triage:start"))

    answers = {
        "total-value-of-business-case": "above-12k",
        "new-project-or-programme": "no",
        "have-you-spoken-to-finance-business-partner": "yes",
        "is-business-case-less-than-two-million": "no",
        "novel-contentious-or-repercussive": "no",
        "where-is-the-budget-held": "Digital",
    }

    for slug in QUESTION_SLUGS:
        answer = answers.get(slug)
        if answer:
            client.post(
                reverse("triage:question", kwargs={"slug": slug}),
                data={"answer": answer},
            )

    session = TriageSession.objects.filter(completed_at__isnull=False).last()
    assert session is not None
    assert session.result != "in-progress"
    assert session.result != ""


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
