import pytest
import time
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from apps.accounts.models import User
from apps.triage.models import BusinessCase, BusinessCaseTriageResponse


@pytest.fixture
def client(db):
    user = User.objects.create_user(
        username="test.user@example.gov.uk", email="test.user@example.gov.uk"
    )
    client = Client()
    client.force_login(user)
    session = client.session
    session["id_token_claims"] = {"exp": time.time() + 3600}
    session.save()
    return client


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


@pytest.fixture
def business_case(db):
    triage_response = BusinessCaseTriageResponse.objects.create(session_key="test-session")
    return BusinessCase.objects.create(
        business_case_triage_response=triage_response,
        name="Test business case",
        type="Procurement",
        status="Active",
    )


def test_case_detail_shows_business_case_name(client, business_case):
    response = client.get(reverse("case-detail", kwargs={"pk": business_case.pk}))

    assert response.status_code == 200
    assert business_case.name in response.content.decode()


def test_case_detail_shows_type_status_and_reference_number(client, business_case):
    response = client.get(reverse("case-detail", kwargs={"pk": business_case.pk}))
    content = response.content.decode()

    assert response.status_code == 200
    assert "Business Justification Case: Procurement" in content
    assert f"Case reference number: {business_case.pk}" in content
    assert "govuk-tag--blue" in content
    assert "Active" in content


def test_case_detail_upload_accepts_valid_docx(client, business_case):
    upload = SimpleUploadedFile(
        "document.docx",
        b"file contents",
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    response = client.post(
        reverse("case-detail", kwargs={"pk": business_case.pk}),
        {"document": upload},
    )

    assert response.status_code == 200
    assert "Business case uploaded!" in response.content.decode()


def test_case_detail_upload_rejects_wrong_extension(client, business_case):
    upload = SimpleUploadedFile("document.pdf", b"file contents", content_type="application/pdf")

    response = client.post(
        reverse("case-detail", kwargs={"pk": business_case.pk}),
        {"document": upload},
    )

    assert response.status_code == 200
    assert "must be a Word document" in response.content.decode()


def test_case_detail_upload_rejects_file_too_large(client, business_case):
    upload = SimpleUploadedFile(
        "document.docx",
        b"0" * (100 * 1024 * 1024 + 1),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    response = client.post(
        reverse("case-detail", kwargs={"pk": business_case.pk}),
        {"document": upload},
    )

    assert response.status_code == 200
    assert "must be smaller than 100MB" in response.content.decode()


def test_case_detail_upload_rejects_missing_file(client, business_case):
    response = client.post(reverse("case-detail", kwargs={"pk": business_case.pk}), {})

    assert response.status_code == 200
    assert "Select a file to upload" in response.content.decode()
