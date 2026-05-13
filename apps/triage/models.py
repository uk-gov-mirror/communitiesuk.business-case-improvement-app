from django.db import models
from django.utils import timezone


class TriageSession(models.Model):
    """
    Stores a user's answers for one Business Case triage journey.

    TODO:  users Django session key as no login is required.
    logging in can update this to use Entra ID/account ID, etc. when we connect to Entra

    JSON dict of {question_slug: answer_value}.
    """

    session_key = models.CharField(max_length=40, db_index=True)
    answers = models.JSONField(default=dict)
    result = models.CharField(max_length=100, blank=True, default="")
    started_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]

    def set_answer(self, question_slug: str, value: str):
        self.answers[question_slug] = value
        # self.save()

    def get_answer(self, question_slug: str) -> str:
        return self.answers.get(question_slug, "")

    def clear(self):
        self.answers = {}
        self.result = ""
        self.completed_at = None
        self.save()

    def __str__(self):
        return f"TriageSession {self.session_key[:8]}… ({len(self.answers)} answers)"
