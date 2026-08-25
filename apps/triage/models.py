from django.db import models
from django.utils import timezone
    
class BusinessCaseTriageResponse(models.Model):
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
        return f"BusinessCaseTriageResponse {self.session_key[:8]}… ({len(self.answers)} answers)"

class BusinessCase(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        UPLOADED = "Uploaded", "Uploaded"
        WITHDRAWN = "Withdrawn", "Withdrawn"

    name = models.CharField(max_length=255, blank=True, default="")
    directorate = models.CharField(max_length=255, blank=True, default="")
    type = models.CharField(max_length=255, blank=True, default="")
    lead_contact = models.CharField(max_length=255, blank=True, default="")
    summary = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=9,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    business_case_triage_response = models.ForeignKey(
        BusinessCaseTriageResponse,
        on_delete=models.PROTECT,
        related_name="business_cases",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"BusinessCase id: {self.pk}"


class BusinessCaseResponse(models.Model):
    class BusinessCaseResponseStatus(models.TextChoices):
        COMPLETED = "Completed", "Completed"

    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.CharField(max_length=150, blank=False, null=False, default="-")
    
    business_case_id = models.ForeignKey(
        BusinessCase,
        on_delete=models.PROTECT,
    )

    status = models.TextField(
        choices=BusinessCaseResponseStatus.choices,
        default=BusinessCaseResponseStatus.COMPLETED
    )

    def __str__(self):
        return f"BusinessCase: {self.business_case_id} - response version: {self.version}"


class BusinessCaseResponseSummary(models.Model):
    business_case_response_id = models.ForeignKey(
        BusinessCaseResponse,
        on_delete=models.PROTECT,
    )
    summary_text = models.TextField(blank=False, null=False, )
    whole_of_life_cost = models.CharField(blank=False, null=False, default="0")
    directorate = models.CharField(blank=False, null=False, default="-")
    sro_scs = models.CharField(blank=False, null=False, default="-")
    approved_by_sro_scs = models.DateField(default=timezone.now)
    author = models.CharField(blank=False, null=False, default="-")


    def __str__(self):
        return f"BusinessCaseResponse: id: {self.business_case_response_id}"


class BusinessCaseResponseSection(models.Model):
    business_case_response_id = models.ForeignKey(
        BusinessCaseResponse,
        on_delete=models.PROTECT,
    )

    header_text = models.CharField(max_length=100, blank=False, null=False, default="")
    
    def __str__(self):
        return f"BusinessCaseResponseSection: header: {self.header_text}"


class BusinessCaseResponseBlock(models.Model):
    class BlockType(models.TextChoices):
        PARGRAPH = "Paragraph", "Paragraph"
        TABLE = "Table", "Table"

    business_case_response_section_id = models.ForeignKey(
        BusinessCaseResponseSection,
        on_delete=models.PROTECT,
    )
    block_type = models.TextField(
        choices=BlockType.choices,
        default=BlockType.PARGRAPH,
        help_text="The type of Block this data represents, e.g Paragraph, Table, etc."
    )

    block_number = models.IntegerField(default=0, help_text="The order in which this block appeared under the header")
    block_data = models.BinaryField(blank=False, null=False)

    def __str__(self):
        return f"Content: {self.block_data} - Content Type: {self.block_type}"
    
