from django.conf import settings
from django.db.models import Max
from django.http import Http404, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.triage.models import BusinessCase, BusinessCaseResponse, BusinessCaseResponseSummary

from config.aws import get_s3_client, upload_file_to_s3


def index(request):
    paginator = Paginator(BusinessCase.objects.all(), settings.BUSINESS_CASES_PER_PAGE)
    business_cases = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "core/index.html",
        {"business_cases": business_cases},
    )


def case_detail(request, pk):
    business_case = get_object_or_404(BusinessCase, pk=pk)
    error = None

    if request.method == "POST":
        uploaded_file = request.FILES.get("document")

        if not uploaded_file:
            error = "Select a file to upload"
        elif not uploaded_file.name.lower().endswith(settings.ALLOWED_UPLOAD_EXTENSIONS):
            error = "The selected file must be a Word document (.doc or .docx)"
        elif uploaded_file.size > settings.MAX_UPLOAD_SIZE_BYTES:
            error = "The selected file must be smaller than 100MB"
        else:
            last_version = BusinessCaseResponse.objects.filter(
                business_case=business_case
            ).aggregate(Max("version"))["version__max"]

            business_case_response = BusinessCaseResponse.objects.create(
                business_case=business_case,
                version=(last_version or 0) + 1,
                uploaded_by=request.user.get_full_name(),
                status=BusinessCaseResponse.BusinessCaseResponseStatus.PENDING,
                original_filename=uploaded_file.name,
            )

            extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
            timestamp = business_case_response.created_at.strftime("%Y%m%d%H%M%S")
            key = (
                f"response_{business_case.pk}_{business_case_response.version}_"
                f"{business_case_response.pk}_{timestamp}.{extension}"
            )

            business_case_response.s3_key = key
            business_case_response.save(update_fields=["s3_key"])

            upload_file_to_s3(uploaded_file, key)

    latest_response = (
        BusinessCaseResponse.objects.filter(business_case=business_case).order_by("-version").first()
    )

    if (latest_response):
        if (latest_response.status == BusinessCaseResponse.BusinessCaseResponseStatus.PENDING
            and timezone.now() - latest_response.created_at > settings.PENDING_RESPONSE_TIMEOUT):
            latest_response.status = BusinessCaseResponse.BusinessCaseResponseStatus.ERROR
            latest_response.save(update_fields=["status"])
        if (latest_response.status == BusinessCaseResponse.BusinessCaseResponseStatus.ERROR):
            error = "The last uploaded business case timed out while processing. Please try again."

    uploaded_response_summary = None
    if business_case.status == BusinessCase.Status.UPLOADED and latest_response:
        uploaded_response_summary = BusinessCaseResponseSummary.objects.filter(
            business_case_response=latest_response
        ).first()

    return render(
        request,
        "core/case_detail.html",
        {
            "business_case": business_case,
            "error": error,
            "latest_response": latest_response,
            "uploaded_response_summary": uploaded_response_summary,
        },
    )


def download_response_document(request, pk, response_id):
    business_case = get_object_or_404(BusinessCase, pk=pk)
    business_case_response = get_object_or_404(
        BusinessCaseResponse, pk=response_id, business_case=business_case
    )

    if not business_case_response.s3_key:
        raise Http404

    s3_object = get_s3_client().get_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=business_case_response.s3_key
    )
    response = HttpResponse(
        s3_object["Body"].read(),
        content_type=s3_object.get("ContentType", "application/octet-stream"),
    )
    filename = business_case_response.original_filename or business_case_response.s3_key
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def health(request):
    return JsonResponse({"status": "ok"})
