import re
from unittest.mock import patch

import pytest
from django.db import IntegrityError, transaction

from apps.triage.models import BusinessCase, BusinessCaseTriageResponse


@pytest.mark.django_db
def test_business_case_id_is_generated_on_instantiation():
    business_case = BusinessCase()

    assert re.fullmatch(r"[A-Z0-9]{10}", business_case.pk)
    assert BusinessCase._meta.pk.name == "id"
    assert not BusinessCase._meta.pk.editable


@pytest.mark.django_db
def test_duplicate_generated_id_is_rejected_without_overwriting_existing_case():
    triage_response = BusinessCaseTriageResponse.objects.create()
    with patch("django.utils.crypto.secrets.choice", return_value="A"):
        business_case = BusinessCase.objects.create(
            business_case_triage_response=triage_response, name="Original case"
        )
        with transaction.atomic():
            pytest.raises(
                IntegrityError,
                BusinessCase.objects.create,
                business_case_triage_response=triage_response,
                name="Duplicate case",
            )

    business_case.refresh_from_db()
    assert business_case.pk == "AAAAAAAAAA"
    assert business_case.name == "Original case"
    assert BusinessCase.objects.count() == 1
