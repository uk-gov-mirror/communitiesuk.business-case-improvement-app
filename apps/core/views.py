from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render

from apps.triage.models import BusinessCase


def index(request):
    paginator = Paginator(BusinessCase.objects.all(), settings.BUSINESS_CASES_PER_PAGE)
    business_cases = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "core/index.html",
        {"business_cases": business_cases},
    )


def health(request):
    return JsonResponse({"status": "ok"})
