from markupsafe import Markup
from .slugs import *
from .calculate_result_helpers import AnswerConstants

"""
Triage question flow for Phase 1.

Each question is a dict with:
  slug        — used in the URL and as the key in answers JSON
  title       — the <h1> on the page
  hint        — optional hint text shown below the title
  type        — e.g. "radio"
  choices     — list of (value, label) tuples
  help_text   - help text for pages 

Notice types provide information or guidance during the triage journey between questions.
They do not require an answer.

Routing is defined by ROUTING — a dict of:
  (question_slug, answer_value) -> next_question_slug OR result_slug

If the next value starts with "result:" it's a result page, not a question.
If there's no specific match for an answer, the fallback key (slug, "*") is used.

Result pages are defined in RESULTS.
"""

# Types: Radio, Checkbox, Select, Input, Character Count Textarea
QUESTIONS = [
    {
        "slug": total_value_of_business_case,
        "title": "What is the estimated total value of your request?",
        "type": "radio",
        "hint": '<div class="govuk-inset-text">The total value means the whole life cost of the business case including VAT.</div>',
        "help_text": "We ask this first because the value influences whether you need a business case at all. The total value is the whole life cost of the business case, including staffing costs, capital and revenue.",
        "choices": [
            (AnswerConstants.BELOW_12K, "Below £12,000"),
            (AnswerConstants.BETWEEN_12K_AND_2M, "Between £12,000 and 2m"),
            (AnswerConstants.ABOVE_2M, "Above 2m")
        ],
    },
    {
        "slug": part_of_wider_programme_with_existing_fbc,
        "title": "Is this request part of a wider programme with an existing FBC?",
        "type": "radio",
        "help_text": "We ask this to make sure spend is routed through the correct approvals process. If this work is part of a wider piece of activity, or if multiple related pieces of spend together exceed approval thresholds, you should answer Yes, even if this individual business case is for a smaller amount.",
        "choices": [
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": does_request_involve_anything_digital,
        "title": "Does you request involve anything digital?",
        "type": "radio",
        "choices":[
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": is_this_request_a_pilot,
        "title": "Is this request a 'pilot' with the potential to turn into a larger proposal in the future?",
        "type": "radio",
        "choices":[
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": making_a_change_to_or_additional_money_for_existing_business_case,
        "title": "Are you making a change to, or asking for additional money for an existing business case?",
        "type": "radio",
        "help_text": "We ask this to make sure spend is routed through the correct approvals process. If this work is part of a wider piece of activity, or if multiple related pieces of spend together exceed approval thresholds, you should answer Yes, even if this individual business case is for a smaller amount.",
        "choices":[
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": any_other_business_cases_that_are_connected_to_this_work,
        "title": "Are there any other business cases that are in draft or review connected to this work or initiative?",
        "type": "radio",
        "choices":[
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": which_option_describes_what_you_are_trying_to_do,
        "title": "Select the option that best describes what you're trying to do.",
        "type": "radio",
        "choices":[
            (commission_research, "Commision Research"),
            (procure_goods_and_services_from_third_party, "Procure goods and services from a 3rd party"),
            (hire_contracted_workers_to_fill_temporary_capacity_gap, "Hire contracted workers to fill a temporary capacity gap (i.e money for contingent labour)")
        ]
    },
    {
        "slug": which_best_describes_your_spend,
        "title": "Which best describes your spend?",
        "type": "radio",
        "choices": [
            (spend_on_corporate_activities,"Spend money on corporate activities - Purchase additional licences, equipment, training or similar operational items that do not require a new procurement approach"),
            (procuring_something_else, "I'm procuring something else")
        ]
    },
    {
        "slug": are_you_procuring_consulting_and_professional_services,
        "title": "Are you procuring Consulting & Professional services?",
        "type": "radio",
        "choices": [
            ("yes", "Yes"),
            ("no", "No")
        ]
    },
    {
        "slug": we_want_to_continue_improving_our_service,
        "title": "We want to continue improving our service.",
        "hint": "To help us improve, for reporting, and if you're able to, what does your procurement relate to? select all the apply. Don't worry - this won't impact what template we give you.",
        "type": "checkbox",
        "choices":[
            ("procurement-of-brand-new-service-contract-or-delivery", "Procurement of a brand new service, contract or delivery activity"),
            ("re-procurement-of-an-existing-good-or-service", "Re-procurement of an existing good or service"),
            ("variation-to-or-extension-of-existing-contract", "Variation to, or extension of, an existing contract"),
            ("direct-award-without-competition", "Direct award without competition"),
            ("other", "Other"),
            ("dont-know", "I don't know")
        ]
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
        "slug": novel_repercussive_contentious_hmt_consent,
        "title": "Is it novel, repercussive, contentious, or needs HMT consent?",
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
        "slug": where_is_the_budget_held,
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
            ("Digital", AnswerConstants.DIGITAL_STRING),
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
    {
        "slug": give_your_bjc_a_name,
        "title": "Give your BJC a name",
        "type": "input",
    },
    {
        "slug": provide_a_high_level_summary,
        "title": "What’s this business case about?",
        "type": "charactercounttextarea",
        "maxwords": 30,
        "hint": Markup('<div class="govuk-inset-text">Provide a brief summary of your proposal (up to 30 words).</div>'),
        "help_text": """
        <p>Describe what you are proposing and why.</p>
        <p>For example:</p>
        <p>Procure a supplier to deliver a new grants management system, replacing manual processes and improving efficiency for applicants and staff.</p>
        <p>Keep your summary short and avoid unnecessary detail. You can provide more information later in the business case.</p>
        
        <p><strong>Not sure?</strong></p>
        <p>Imagine you only had one sentence to explain your proposal to someone unfamiliar with the work. What would you say?</p>    
        """,
        "errorMessage": "Summary must be 30 characters or less",
    },
    
    # Types: notice
    {
        "slug": novel_repercussive_contentious_hmt_consent_notice,
        "title": 'What you need to know',
        "type": "notice",
        "content": """<p>Before you start drafting a business case, speak to your <strong>Finance Business Partner (FBP)</strong> and/or a <strong>Commercial colleague</strong>.</p>
        <p>They can help you confirm:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>whether a business case is needed</li>
            <li>which template is right for your proposal</li>
            <li>any approvals, assurance or governance requirements you should be aware of</li>
        </ul>""",
        "help_title": "Why am I seeing this message?",
        "help_text": """
        <p>You told us your proposal may be novel, contentious, repercussive, high risk or may need HM Treasury approval.</p>
        <p>These proposals often need extra assurance and approval. Speaking to your FBP and/or Commercial colleague early will help you follow the right business case and approvals process.</p>
        """,
    },
    {
        "slug": is_this_request_a_pilot_notice,
        "title": 'What you need to know',
        "type": "notice",
        "content": """<p>Before you start drafting a business case, speak to your <strong>Finance Business Partner (FBP)</strong> and/or a <strong>Commercial colleague</strong>.</p>
        <p>Your proposal is likely to need the standard 3-stage business case process. It may also need approval from the Investment Sub-Committee (ISC) and, in some cases, His Majesty’s Treasury (HM Treasury).</p>
        <p>The template you need depends on the stage your proposal has reached. This could be a:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>Project Brief</li>
            <li>Strategic Outline Case (SOC)</li>
            <li>Outline Business Case (OBC)</li>
            <li>Full Business Case (FBC)</li>
        </ul>
        <p>If you are not sure which template to use, speak to your FBP, Commercial colleague or the ISC Secretariat.</p>
        <p>If you know which template you need, select <strong>Continue</strong>.</p>  
        """,
        "help_title": "Why am I seeing this message?",
        "help_text": """
        <p>You told us your proposal may be novel, contentious, repercussive, high risk or may need HM Treasury approval.</p>
        <p>These proposals often need extra assurance and approval. Speaking to your FBP and/or Commercial colleague early will help you follow the right business case and approvals process.</p>
        """,
    },
    {
        "slug": is_this_request_part_of_a_wider_programme_with_existing_business_case_notice,
        "title": 'What you need to know',
        "type": "notice",
        "content": """<p>Before you start drafting a business case, speak to your <strong>Finance Business Partner (FBP)</strong> and/or a <strong>Commercial colleague</strong>.</p>
        <p>They can help you decide whether you can:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>update an existing approved business case using an addendum</li>
            <li>use the change control tolerance process</li>
            <li>create a new Business Justification Case (BJC)</li>
        </ul>
        <p>An addendum is used to record and seek approval for changes to an existing approved business case.</p>
        <p>If an addendum or the change control tolerance process is not suitable, select <strong>Continue</strong> to access a Business Justification Case (BJC) template.</p>
        <p>Reviewers may ask how your request relates to the wider programme and any existing approvals.</p>
        """,
        "help_title": "Why am I seeing this message?",
        "help_text": """
        <p>You told us that your request relates to an existing approved business case or wider programme.</p>
        <p>In some cases, changes can be managed through an addendum or an existing change control process instead of creating a new business case.</p>
        <p>Speaking to your FBP and/or Commercial colleague before you start will help you identify the correct route and avoid unnecessary work.</p>
        """,
    },
    {
        "slug": any_other_business_cases_that_are_connected_to_this_work_notice,
        "title": 'What you need to know',
        "type": "notice",
        "content": """<p>Before continuing, consider whether this work could be included in an <strong>existing business case</strong> or <strong>combined into a single business case</strong> with related work.</p>
        <p>Combining business cases can help provide a complete view of:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>costs</li>
            <li>benefits</li>
            <li>risks</li>
            <li>dependencies</li>
        </ul>
        <p>This can make it easier for decision-makers to understand the wider initiative and assess its overall value.</p>
        <p>We understand this is not always practical. If separate business cases are needed, select <strong>Continue</strong>.</p>
        """,
        "help_title": "Why am I seeing this message?",
        "help_text": """
        <p>You told us that there are other business cases connected to this work or initiative. Where possible, combining related business cases can help provide a clearer view of the overall investment, outcomes and risks.</p>
        <p>It can also help reviewers understand how different pieces of work fit together.</p>
        <p>If combining business cases is not appropriate, you can continue and create a separate business case.</p>
        """,
    },
    {
        "slug": are_you_procuring_consulting_and_professional_services_notice,
        "title": 'What you need to know',
        "type": "notice",
        "content": """<p>You told us that your proposal involves <strong>Consultancy and Professional Services (C&PS)</strong>.</p>
        <p>C&PS spend is subject to additional approvals and spend controls.</p>
        
        <h2>What you need to do</h2>
        <p>1. Download your business case template</p>
        <p>2. Review the C&PS guidance</p>
        <p>Before starting your business case, review the C&PS guidance to understand the approvals and controls that may apply.</p>
        <p>3. Allow time for approvals</p>

        <p class="govuk-!-margin-bottom-2">You should allow time for reviews and approvals before starting any procurement. Typical timescales include:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li><strong>Commercial review:</strong> approximately 2 weeks</li>
            <li><strong>Chief Financial Officer (CFO) approval:</strong> approximately 1 week</li>
            <li><strong>Ministerial approvals:</strong> standard ministerial timescales</li>
        </ul>

        <h2>Who will approve this?</h2>
        <p>Approval requirements depend on the value and nature of the spend.</p>
        <p>Where different approval thresholds apply, the highest level of approval will be required.</p>

        <h3>Need help?</h3>
        <p>If you're unsure whether your requirement should be treated as C&PS, <a class="govuk-link" href="mailto:BFRG-CCM@communities.gov.uk">email the team</a>.</p>
        <p>Learn more about the <a class="govuk-link" href="https://intranet.communities.gov.uk/guidance/procurement-and-grants/procurement/buying-consultancy-and-professional-services/">C&PS</a> process and controls here.</p>
        """
    },
    {
        "slug": hire_contracted_workers_to_fill_temporary_capacity_gap_notice,
        "title": 'What you need to know',
        "type": "radio",
        "hint": """<p class="govuk-body">You selected "Hire contracted workers to fill a temporary capacity gap". This is otherwise known as Contingent labour. </p>
        <p class="govuk-body">Before continuing, we need to check whether you need:</p>
        <p class="govuk-body"><strong>Contingent labour</strong> (temporary people working as part of your team), or</p>
        <p class="govuk-body"><strong>Consultancy and Professional Services (C&PS)</strong> (external advice, expertise or specialist services).</p>
        <h2 class="govuk-heading-m">Are you looking for temporary staff to fill a resource or capacity gap?</h2>
        """,
        "choices": [
            ("yes", "Yes, I need contingent labour"),
            ("no", "No, I need Consultancy and Professional Services (C&PS)"),
        ],
        "help_title": "What do these terms mean?",
        "help_text": """

        <p><strong>Contingent labour</strong></p>
        <p>Temporary people who work as part of your team and help fill a resource or capacity gap.</p>
        <p class="govuk-!-margin-bottom-2">Examples include:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>maternity cover</li>
            <li>temporary project support</li>
            <li>additional administrative support</li>
            <li>interim staff</li>
        </ul>

        <p><strong>Consultancy</strong></p>
        <p>External experts who provide advice, recommendations or specialist expertise.</p>
        <p class="govuk-!-margin-bottom-2">Examples include:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>strategic planning</li>
            <li>organisational change</li>
            <li>market analysis</li>
            <li>specialist policy advice</li>
        </ul>

        <p><strong>Professional Services</strong></p>
        <p>A supplier delivers specialist work or a specific outcome for you.</p>
        <p class="govuk-!-margin-bottom-2">Examples include:</p>
        <ul class="govuk-list govuk-list--bullet">
            <li>software development</li>
            <li>cyber security services</li>
            <li>systems integration</li>
            <li>specialist technical services</li>
        </ul>

        <p class="govuk-!-margin-bottom-2"><strong>A simple way to tell the difference:</strong></p>
        <ul class="govuk-list">
            <li><strong>Contingent labour</strong> fills a temporary resource gap.</li>
            <li><strong>Consultancy provides</strong>  advice and expertise.</li>
            <li><strong>Professional services</strong> delivers specialist work or outcomes.</li>
        </ul>
        <p><strong>Not sure?</strong></p>
        <p>Speak to your Finance Business Partner (FBP), a Commercial colleague or the HR Business Partner (HRBP) team before continuing.</p>
        """,
    },
]


ROUTING = {
    # work-type branches first
    (total_value_of_business_case, AnswerConstants.BELOW_12K): part_of_wider_programme_with_existing_fbc,
    (total_value_of_business_case, AnswerConstants.BETWEEN_12K_AND_2M): novel_repercussive_contentious_hmt_consent,
    (total_value_of_business_case, AnswerConstants.ABOVE_2M): "calculate-result",
    (part_of_wider_programme_with_existing_fbc, "yes"): "calculate-result",
    (part_of_wider_programme_with_existing_fbc, "no"): does_request_involve_anything_digital,
    (does_request_involve_anything_digital, "yes"): "calculate-result",
    (does_request_involve_anything_digital, "no"): "calculate-result",
    (novel_repercussive_contentious_hmt_consent, "no"): is_this_request_a_pilot,
    (novel_repercussive_contentious_hmt_consent, "yes"): novel_repercussive_contentious_hmt_consent_notice,
    (novel_repercussive_contentious_hmt_consent_notice, "*"): "calculate-result",
    (is_this_request_a_pilot, "yes"): is_this_request_a_pilot_notice,
    (is_this_request_a_pilot_notice, "*"): "calculate-result",
    (is_this_request_a_pilot, "no"): making_a_change_to_or_additional_money_for_existing_business_case,
    (making_a_change_to_or_additional_money_for_existing_business_case, "yes"): is_this_request_part_of_a_wider_programme_with_existing_business_case_notice,
    (is_this_request_part_of_a_wider_programme_with_existing_business_case_notice, "*"): any_other_business_cases_that_are_connected_to_this_work,
    (making_a_change_to_or_additional_money_for_existing_business_case, "no"): any_other_business_cases_that_are_connected_to_this_work,
    (any_other_business_cases_that_are_connected_to_this_work, "*"): where_is_the_budget_held,
    (any_other_business_cases_that_are_connected_to_this_work, "yes"): any_other_business_cases_that_are_connected_to_this_work_notice,
    (any_other_business_cases_that_are_connected_to_this_work_notice, "*"): where_is_the_budget_held,
    (where_is_the_budget_held, "*"): which_option_describes_what_you_are_trying_to_do,
    (which_option_describes_what_you_are_trying_to_do, commission_research): "calculate-result",
    (which_option_describes_what_you_are_trying_to_do, procure_goods_and_services_from_third_party): which_best_describes_your_spend,
    (which_option_describes_what_you_are_trying_to_do, hire_contracted_workers_to_fill_temporary_capacity_gap): hire_contracted_workers_to_fill_temporary_capacity_gap_notice,
    (hire_contracted_workers_to_fill_temporary_capacity_gap_notice, "yes"): give_your_bjc_a_name,
    (hire_contracted_workers_to_fill_temporary_capacity_gap_notice, "no"): are_you_procuring_consulting_and_professional_services_notice,
    (which_best_describes_your_spend, spend_on_corporate_activities): give_your_bjc_a_name,
    (which_best_describes_your_spend, procuring_something_else): are_you_procuring_consulting_and_professional_services,
    (are_you_procuring_consulting_and_professional_services, "no"): we_want_to_continue_improving_our_service,
    (are_you_procuring_consulting_and_professional_services, "yes"): are_you_procuring_consulting_and_professional_services_notice,
    (are_you_procuring_consulting_and_professional_services_notice, "*"): we_want_to_continue_improving_our_service,
    (we_want_to_continue_improving_our_service, "*"): give_your_bjc_a_name,
    (give_your_bjc_a_name, "*"): provide_a_high_level_summary,
    (provide_a_high_level_summary, "*"): "calculate-result"
}


BUSINESS_CASE_EXIT_SCREEN_TYPES = {
    "exit-to-download-template-procurement-route": "Procurement",
    "exit-to-download-template-corporate-spend-fbp-route": "Corporate Spend FBP",
    "exit-to-download-template-hrbp-contingent-labour-route": "HRBP Contingent Labour",
}

# ---------------------------------------------------------------------------
# Exit pages - TODO
# ---------------------------------------------------------------------------


# Ordered list of all question slugs (used for progress indicator)
QUESTION_SLUGS = [q["slug"] for q in QUESTIONS]


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


def get_business_case_type_from_result_slug(result_slug: str, default: str) -> str:
    return BUSINESS_CASE_EXIT_SCREEN_TYPES.get(result_slug, default)
