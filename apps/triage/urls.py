from django.urls import path

from . import views

app_name = "triage"

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", views.start, name="start"),
    path("question/<slug:slug>/", views.question, name="question"),
    path("result/<slug:slug>/", views.result, name="result"),
    path("debug/", views.debug_session, name="debug"),
]
