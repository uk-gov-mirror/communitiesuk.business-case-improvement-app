from markupsafe import Markup

"""
Triage question flow for Phase 1.

Each question is a dict with:
  slug        — used in the URL and as the key in answers JSON
  title       — the <h1> on the page
  hint        — optional hint text shown below the title
  type        — e.g. "radio"
  choices     — list of (value, label) tuples
  help_text   - help text for pages 

Routing is defined by ROUTING — a dict of:
  (question_slug, answer_value) -> next_question_slug OR result_slug

If the next value starts with "result:" it's a result page, not a question.
If there's no specific match for an answer, the fallback key (slug, "*") is used.

Result pages are defined in RESULTS.
"""

# Types: Radio, Checkbox, Select
QUESTIONS = [
    {
        "slug": "total-value-of-business-case",
        "title": "What is the total value of the business case?",
        "type": "radio",
        "hint": '<div class="govuk-inset-text">The total value means the whole life cost of the business case including VAT.</div>',
        "help_text": "We ask this first because the value influences whether you need a business case at all. The total value is the whole life cost of the business case, including staffing costs, capital and revenue.",
        "choices": [
            ("below-12k", "Below £12,000"),
            ("above-12k", "£12,000 or above"),
        ],
    },
    {
        "slug": "new-project-or-programme",
        "title": "Is this spend part of an existing project or programme?",
        "type": "radio",
        "help_text": "We ask this to make sure spend is routed through the correct approvals process. If this work is part of a wider piece of activity, or if multiple related pieces of spend together exceed approval thresholds, you should answer Yes, even if this individual business case is for a smaller amount.",
        "choices": [
            ("yes", "Yes"),
            ("no", "No"),
        ],
    },
    {
        "slug": "have-you-spoken-to-finance-business-partner",
        "title": "Have you discussed this business case with your Finance Business Partner (FBP) or a Commercial colleague?",
        "type": "radio",
        "hint": "<div class=\"govuk-inset-text\"><p>You should always engage your FBP and a Commercial colleague before you start drafting a business case.</p><p>If you are from the Digital Directorate, see additional guidance under 'Help with this question'</p></div>",
        "help_text": """Speaking with your FBP and the Commercial team early can help avoid delays later in the process.
            <p><strong>Finance Business Partner (FBP)</strong><br>
            FBPs are embedded across MHCLG (usually one per policy area). They help check affordability, identify financial risks and provide assurance.</p>

            <p>If you haven't already, speak to your FBP and let them know what you're planning.</p>

            <p><strong>Commercial</strong><br>
            Commercial colleagues are responsible for grants and if you want to procure something. They check the proposed procurement route, ensure your case complies with policy and regulations and they also provide assurance.</p>

            <p>You can contact the Commercial team at <a class="govuk-link" href="mailto:Commercial@communities.gov.uk">Commercial@communities.gov.uk</a></p>

            <p><strong>Digital Directorate FBP exception</strong><br>
            If you are in the Digital Directorate and want to spend from Digital budget, you do not need to engage your FBP directly. Instead, let the Digital Corporate Office know you are doing this case at <a class="govuk-link" href="mailto:digitalbusinesscase@communities.gov.uk">digitalbusinesscase@communities.gov.uk</a></p>

            <p>You'll likely still need to engage the Commercial team. If you have already informed the Digital Corporate Office that you are starting this business case, you can select 'Yes' and continue.</p>""",
        "choices": [
            ("yes", "Yes"),
            ("no", "No"),
        ],
    },
    {
        "slug": "is-business-case-less-than-two-million",
        "title": "You already told us the total value is above £12,000. Is it less than £2million?",
        "type": "radio",
        "hint": '<div class="govuk-inset-text">The total figure must include VAT.</div>',
        "help_text": "We are asking this again because the amount influences the type of business case (and approvals) you'll need.",
        "choices": [
            ("yes", "Yes"),
            ("no", "No"),
        ],
    },
    {
        "slug": "novel-contentious-or-repercussive",
        "title": "Is it novel, contentious, sets precedent, repercussive or requires HM Treasury consent because of legislation?",
        "type": "radio",
        "hint": '<div class="govuk-inset-text">This includes something that could be deemed unusual, risky or is likely to be challenged.</div>',
        "help_text": """<p>We ask this because anything that may be deemed novel, contentious or repercussive will need to go through particular approvals (including HM Treasury for consent due to legislation). </p>

      <p>What do these terms mean?</p>

      <p><b>Novel</b> - Something new or unusual for government. For example, a type of spend, funding approach, or arrangement that hasn\'t been done before. </p>

      <p><b>Contentious</b> - The proposal could be challenged or criticised. For example, by Ministers, Parliament, the media, or internally. </p>

      <p><b>Repercussive</b> - The decision could have knock-on effects beyond this project, such as affecting other departments, organisations, or future spending decisions across government. </p>

      <p><b>Sets a precedent</b> - Approving it could make it harder to say no to similar requests in future, because others may expect the same treatment. </p>

      <p><b>Requires HM Treasury consent because of legislation</b> - Requires HM Treasury consent because of legislation - Some types of spending must go to HM Treasury by law, even if the value is low. An FBP can advise if this applies. </p>

      <p><b>Not sure?</b><br>
        If you\'re unsure, check with your Finance Business Partner or speak to the ISC Secretariat at <a
          class="govuk-link" href="ISCSecretariat@communities.gov.uk">
          ISCSecretariat@communities.gov.uk</a>. It\'s normal to need advice at this stage.
      </p>""",
        "choices": [
            ("yes", "Yes"),
            ("no", "No"),
        ],
    },
    {
        "slug": "where-is-the-budget-held",
        "title": "Where is the budget held?",
        "type": "select",
        "hint": Markup(
            '<div class="govuk-inset-text"><p>Select the directorate that holds the budget and is financially accountable for this spend.</p></div>'
        ),
        "help_text": "This information does not influence the type of business case template you need, but it does help us to understand how many business cases are in development and how we make improvements to this service.",
        "choices": [
            ("Analysis and Data", "Analysis and Data"),
            ("Building Design and Construction", "Building Design and Construction"),
            ("Building Management & Insight", "Building Management & Insight"),
            ("Chief Planner", "Chief Planner"),
            ("Chief Scientific Adviser", "Chief Scientific Adviser"),
            ("Commercial", "Commercial"),
            ("Communications", "Communications"),
            ("Communities and Inclusive Growth", "Communities & Inclusive Growth"),
            (
                "Departmental Strategy & Governance",
                "Departmental Strategy & Governance",
            ),
            ("Deputy Prime Minister's Data Unit", "Deputy Prime Minister's Data Unit"),
            ("Digital", "Digital"),
            ("Digital Process Improvement", "Digital Process Improvement"),
            ("Elections Directorate", "Elections Directorate"),
            ("Executive Team", "Executive Team"),
            ("Finance", "Finance"),
            ("Grenfell Community & Memorial", "Grenfell Community & Memorial"),
            ("Holocaust Memorial Programme", "Holocaust Memorial Programme"),
            ("Homelessness and Rough Sleeping", "Homelessness and Rough Sleeping"),
            ("Housing Markets and Strategy", "Housing Markets and Strategy"),
            (
                "Leasehold, Private Renting and Digital",
                "Leasehold, Private Renting and Digital",
            ),
            ("Local Funding & Investments", "Local Funding & Investments"),
            ("Local Government Finance", "Local Government Finance"),
            (
                "Local Government Oversight and Accountability",
                "Local Government Oversight and Accountability",
            ),
            (
                "Local Government Reform & Strategy",
                "Local Government Reform & Strategy",
            ),
            ("Local Growth and Devolution", "Local Growth and Devolution"),
            (
                "New Towns_Infrastructure_and_Housing Deliv",
                "New Towns, Infrastructure & Housing Deliv",
            ),
            ("People Capability and Change", "People Capability and Change"),
            ("People Capability and Change C-O", "People Capability and Change C/O"),
            ("Planning", "Planning"),
            ("Policy and DPM Support", "Policy & DPM Support"),
            ("Remediation Policy", "Remediation Policy"),
            (
                "Remediation Programme Funds & Interventi",
                "Remediation Programme Funds & Interventi",
            ),
            ("Resilience and Recovery", "Resilience and Recovery"),
            ("Resettlement", "Resettlement"),
            ("Social Housing", "Social Housing"),
        ],
    },
]


ROUTING = {
    # work-type branches first
    ("total-value-of-business-case", "below-12k"): "new-project-or-programme",
    (
        "total-value-of-business-case",
        "above-12k",
    ): "have-you-spoken-to-finance-business-partner",
    ("new-project-or-programme", "*"): "where-is-the-budget-held",
    (
        "have-you-spoken-to-finance-business-partner",
        "yes",
    ): "is-business-case-less-than-two-million",
    (
        "have-you-spoken-to-finance-business-partner",
        "no",
    ): "is-business-case-less-than-two-million",
    (
        "is-business-case-less-than-two-million",
        "yes",
    ): "novel-contentious-or-repercussive",
    (
        "is-business-case-less-than-two-million",
        "no",
    ): "novel-contentious-or-repercussive",
    (
        "novel-contentious-or-repercussive",
        "no",
    ): "where-is-the-budget-held",
    (
        "novel-contentious-or-repercussive",
        "yes",
    ): "where-is-the-budget-held",
    (
        "where-is-the-budget-held",
        "*",
    ): "calculate-result",
}

# ---------------------------------------------------------------------------
# Exit pages - TODO
# ---------------------------------------------------------------------------


# Ordered list of all question slugs (used for progress indicator)
QUESTION_SLUGS = [q["slug"] for q in QUESTIONS]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def get_question(slug: str) -> dict | None:
    return next((q for q in QUESTIONS if q["slug"] == slug), None)


def get_next(current_question_slug: str, answer: str) -> str:
    """
    Returns the next question slug, or "result:<slug>" for a result page.
    Raises KeyError if the routing table has a gap.
    """
    specific = ROUTING.get((current_question_slug, answer))
    if specific:
        return specific
    wildcard = ROUTING.get((current_question_slug, "*"))
    if wildcard:
        return wildcard
    raise KeyError(
        f"No routing rule for ({current_question_slug!r}, {answer!r}) "
        f"and no wildcard (*) fallback defined."
    )


def get_first_question_slug() -> str:
    return QUESTIONS[0]["slug"]


def get_result_from_answers(answers: dict) -> str:
    """
    Works out which result to show based on the combination of answers.

    Returns a result slug.
    """
    total_value = answers.get("total-value-of-business-case")
    new_project = answers.get("new-project-or-programme")
    spoken_to_fbp = answers.get("have-you-spoken-to-finance-business-partner")
    less_than_2m = answers.get("is-business-case-less-than-two-million")
    novel = answers.get("novel-contentious-or-repercussive")
    where_is_budget_held = answers.get("where-is-the-budget-held")

    # Exit 1
    if total_value == "below-12k" and new_project == "no":
        return "you-do-not-need-a-business-case"

    # Exit 2
    elif total_value == "below-12k" and new_project == "yes":
        return "speak-to-someone-first"

    # Exit 3
    elif total_value == "above-12k" and less_than_2m == "no" and novel == "no":
        return "you-need-to-start-a-full-business-case"

    # Exit 4
    elif total_value == "above-12k" and less_than_2m == "yes" and novel == "no":
        return "you-need-to-start-a-business-justification-case"

    # Exit 5
    elif total_value == "above-12k" and less_than_2m == "yes" and novel == "yes":
        return "you-need-to-start-a-full-business-case-novel-or-complex"

    # Exit 5b
    elif total_value == "above-12k" and less_than_2m == "no" and novel == "yes":
        return "you-need-to-start-a-full-business-case-novel-or-complex"

    else:
        return "we-could-not-find-the-right-process-for-you"
