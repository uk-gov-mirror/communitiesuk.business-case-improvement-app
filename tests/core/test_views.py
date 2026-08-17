from django.urls import reverse

from apps.triage.models import BusinessCase, BusinessCaseTriageResponse


def test_index_lists_business_cases(client, db):
    triage_response = BusinessCaseTriageResponse.objects.create(session_key="test-session")
    older = BusinessCase.objects.create(
        business_case_triage_response=triage_response,
        name="Older business case",
    )
    newer = BusinessCase.objects.create(
        business_case_triage_response=triage_response,
        name="Newer business case",
    )

    response = client.get(reverse("index"))

    assert response.status_code == 200
    content = response.content.decode()
    assert content.index(newer.name) < content.index(older.name)


def test_index_paginates_business_cases(client, db):
    triage_response = BusinessCaseTriageResponse.objects.create(session_key="test-session")
    for index in range(21):
        BusinessCase.objects.create(
            business_case_triage_response=triage_response,
            name=f"Business case {index}",
        )

    first_page = client.get(reverse("index"))
    second_page = client.get(reverse("index"), {"page": 2})

    assert first_page.status_code == 200
    assert second_page.status_code == 200
    assert "Business case 20" in first_page.content.decode()
    assert "Business case 0" not in first_page.content.decode()
    assert "Business case 0" in second_page.content.decode()
    assert 'aria-label="Pagination"' in first_page.content.decode()
