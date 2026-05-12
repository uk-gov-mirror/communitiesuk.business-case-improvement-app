from django.shortcuts import redirect, render
from django.utils import timezone
from django.http import JsonResponse

from .flow import (
    QUESTION_SLUGS,
    get_first_question_slug,
    get_next,
    get_question,
    get_result_from_answers,
)
from .models import TriageSession


def _get_or_create_session(request) -> TriageSession:
    if not request.session.session_key:
        request.session.create()

    session, _ = TriageSession.objects.get_or_create(
        session_key=request.session.session_key,
        completed_at=None,
        defaults={"result": "in-progress"},
    )
    return session


def index(request):
    return render(request, "triage/index.html")


def start(request):
    if not request.session.session_key:
        request.session.create()

    TriageSession.objects.filter(
        session_key=request.session.session_key,
        completed_at=None,
    ).delete()

    TriageSession.objects.create(
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
    return render(request, f"triage/results/{slug}.html")


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
