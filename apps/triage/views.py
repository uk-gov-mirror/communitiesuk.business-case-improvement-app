from django.shortcuts import redirect, render
from django.utils import timezone
from django.http import JsonResponse, Http404

from .flow import (
    get_first_question_slug,
    get_next,
    get_question,
)
from .models import BusinessCase, BusinessCaseTriageResponse
from .slugs import give_your_bjc_a_name
from .calculate_result_helpers import get_result_from_answers
from ..word_doc_services.parsing_document import parse_word_document


from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from pathlib import Path

from docx import Document

def _get_or_create_session(request) -> BusinessCaseTriageResponse:
    if not request.session.session_key:
        request.session.create()

    session, _ = BusinessCaseTriageResponse.objects.get_or_create(
        session_key=request.session.session_key,
        completed_at=None,
        defaults={"result": "in-progress"},
    )
    return session


def index(request):
    return render(request, "triage/index.html")

def upload(request):
    return render(request, "triage/upload_document_placeholder_template.html")


def parse_word_doc():
    current_folder = Path(__file__).resolve().parent
    doc = Document(f"{current_folder}/FullDoc.docx")
    parse_word_document(doc)
    

def trigger_work_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    parse_word_doc()
    return JsonResponse({
            'status': 'success',
            'message': "Complete"
        })


def start(request):
    if not request.session.session_key:
        request.session.create()

    BusinessCaseTriageResponse.objects.filter(
        session_key=request.session.session_key,
        completed_at=None,
    ).delete()

    BusinessCaseTriageResponse.objects.create(
        session_key=request.session.session_key,
        result="in-progress",
    )
    return redirect("triage:question", slug=get_first_question_slug())


def question(request, slug: str):
    question_def = get_question(slug)
    if not question_def:
        return redirect("triage:index")

    triage_session = _get_or_create_session(request)

    if request.method == "POST":
        answer = request.POST.get("answer", "").strip()

        if not answer:
            return render(
                request,
                "triage/question.html",
                {
                    "question": question_def,
                    "selected": "",
                    "error": "Select an answer to continue",
                },
            )

        triage_session.set_answer(slug, answer)
        triage_session.result = triage_session.result or "in-progress"
        triage_session.save()

        try:
            next_step = get_next(slug, answer)
        except KeyError:
            return redirect("triage:index")

        if next_step == "calculate-result":
            result_slug = get_result_from_answers(triage_session.answers)
            
            triage_session.result = result_slug
            triage_session.completed_at = timezone.now()
            triage_session.save()
            BusinessCase.objects.get_or_create(
                business_case_triage_response=triage_session,
            )

            request.session["business_case_title"] = triage_session.answers.get(give_your_bjc_a_name, "")

            return redirect("triage:result", slug=result_slug)

        return redirect("triage:question", slug=next_step)

    return render(
        request,
        "triage/question.html",
        {
            "question": question_def,
            "selected": triage_session.get_answer(slug),
            "error": "",
        },
    )


def result(request, slug):
    try:
        return render(request, f"triage/results/{slug}.html")
    except Exception as e:
        print(f"RESULT ERROR for slug '{slug}': {type(e).__name__}: {e}")
        raise Http404


def debug_session(request):
    triage_session = _get_or_create_session(request)
    return JsonResponse(
        {
            "session_key": triage_session.session_key,
            "answers": triage_session.answers,
            "result": triage_session.result,
            "completed_at": str(triage_session.completed_at),
        }
    )
