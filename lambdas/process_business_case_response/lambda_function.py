import io
import os
import re
import traceback

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from docx import Document

from apps.triage.models import BusinessCase, BusinessCaseResponse  # noqa: E402 (must follow django.setup())
from apps.word_doc_services.parsing_document import parse_word_document  # noqa: E402
from config.aws import get_s3_client  # noqa: E402

# Matches the naming convention written by apps/core/views.py:
# response_{business_case_id}_{version}_{business_case_response_id}_{timestamp}.{ext}
FILENAME_PATTERN = re.compile(
    r"^response_\d+_\d+_(?P<business_case_response_id>\d+)_\d+\.\w+$"
)


def lambda_handler(event, context):
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        filename = key.rsplit("/", 1)[-1]

        match = FILENAME_PATTERN.match(filename)
        if not match:
            print(f"Skipping {filename}: does not match the expected naming convention")
            continue

        business_case_response_id = int(match.group("business_case_response_id"))

        try:
            business_case_response = BusinessCaseResponse.objects.get(id=business_case_response_id)
            doc = download_word_document(bucket, key)
            parse_word_document(doc, business_case_response)
        except Exception:
            mark_response_errored(business_case_response_id)
            print(f"Failed to process BusinessCaseResponse {business_case_response_id}:\n{traceback.format_exc()}")
            continue

        mark_response_completed(business_case_response)
        print(f"Marked BusinessCaseResponse {business_case_response_id} as Completed")

    return {"statusCode": 200}


def download_word_document(bucket, key):
    buffer = io.BytesIO()
    get_s3_client().download_fileobj(bucket, key, buffer)
    buffer.seek(0)
    return Document(buffer)


def mark_response_completed(business_case_response):
    BusinessCaseResponse.objects.filter(id=business_case_response.id).update(
        status=BusinessCaseResponse.BusinessCaseResponseStatus.COMPLETED
    )
    BusinessCase.objects.filter(id=business_case_response.business_case_id).update(
        status=BusinessCase.Status.UPLOADED
    )


def mark_response_errored(business_case_response_id):
    BusinessCaseResponse.objects.filter(id=business_case_response_id).update(
        status=BusinessCaseResponse.BusinessCaseResponseStatus.ERROR
    )
