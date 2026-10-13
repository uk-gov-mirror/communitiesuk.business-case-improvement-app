from abc import ABC, abstractmethod
from enum import StrEnum

from apps.word_doc_services.word_tables.table_definitions import TABLE_DEFINITION
from apps.word_doc_services.word_document_wrapper import BusinessCaseWordDocumentWrapper


class HeaderSection(StrEnum):
    OVERVIEW = "Overview"
    SECTIONS = "Business case sections"
    APPROVALS_AND_SUPPORTING_INFORMATION = "Approvals and supporting information"


class Section(ABC):

    def __init__(self):
        self.section_number: int = -1

    @property
    @abstractmethod
    def section_title(self) -> str:
        return ""

    @property
    @abstractmethod
    def header_section(self) -> HeaderSection:
        pass

    @abstractmethod
    def create_section(self, wrapper: BusinessCaseWordDocumentWrapper):
        pass


class ParticipantsAndOrganisationalDetails(Section):

    @property
    def section_title(self) -> str: return "Participants and organisational details"

    @property
    def header_section(self) -> HeaderSection: return HeaderSection.OVERVIEW

    def create_section(self, wrapper: BusinessCaseWordDocumentWrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}")
        wrapper.add_paragraph("The author of this business case should complete this section.")
        wrapper.add_generic_table(TABLE_DEFINITION.AUTHOR_SHOULD_COMPLETE_SECTION)


class ExecutiveSummarySection(Section):

    @property
    def section_title(self) -> str: return "Executive Summary"

    @property
    def header_section(self) -> HeaderSection: return HeaderSection.OVERVIEW

    def create_section(self, wrapper: BusinessCaseWordDocumentWrapper):
        wrapper.add_paragraph(f"{self.section_number}. {self.section_title}", True)
        wrapper.add_paragraph("Provide a concise overview of the proposal. Summarise what you are proposing, why it is necessary, and the decision you need approval for.")
        wrapper.add_help_box([
            "Here's an example executive summary:",
            "Approval for £3m RDEL to continue funding the Audit Assessment Team for one financial year.",
            "To maintain a specialist national support function that helps local authorities inspect higher-risk buildings, progress enforcement activity and support remediation where building safety defects are present.",
            "This will improve onboarding for new starters to reduce friction and save HR time when vetting and setting up new accounts."
        ])
        wrapper.add_input_box()


class StrategicCase(Section):

    @property
    def section_title(self): return "Strategic case"

    @property
    def header_section(self): return HeaderSection.SECTIONS
    
    def create_section(self, wrapper: BusinessCaseWordDocumentWrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}: why is this needed?")
        wrapper.add_paragraph(f"{self.section_number}a. What is the purpose of your proposal, and what problem or opportunity does it address?")
        wrapper.add_bullet_point_list(["Describe the current situation. Who does it affect and why change is needed?"])
        wrapper.add_input_box(150)
        wrapper.add_paragraph(f"{self.section_number}b. Why is action needed now?", True)
        wrapper.add_bullet_point_list(["Explain why action is needed now and the likely impact if the proposal is delayed or not approved."])
        wrapper.add_input_box(80)
        wrapper.add_paragraph(f"{self.section_number}c. How long will the proposal take to deliver?")
        wrapper.add_paragraph("Give the planned start and end dates, or the expected duration if exact dates are not yet known.")
        wrapper.add_input_box(10)
        wrapper.add_paragraph(f"{self.section_number}d. How does this proposal support MHCLG's goals and objectives?", True)
        wrapper.add_bullet_point_list([
            "Explain how your proposal supports one or more of MHCLG's goals (e.g. homes, places and growth) or another relevant departmental or government priority.",
            "Why is MHCLG the right organisation to deliver the proposal?"
        ])
        wrapper.add_input_box(150)
        wrapper.add_paragraph(f"{self.section_number}e. What outcomes will this proposal achieve?", True)
        wrapper.add_paragraph("An outcome is the change or result the proposal will produce. A benefit is the positive value that change delivers to people or the organisation.")
        wrapper.add_bullet_point_list(["Describe what success will look like. Explain what will be different if the proposal succeeds, who or what will be affected"])
        wrapper.add_help_box([
            "Help with this question",
            "Focus on outcomes. An outcome is the change or result the proposal will produce rather than the activities you will carry out.",
            "For example, Employees who use the new ergonomic chairs will experience less back pain and improved posture within six months of implementation.",
            "It describes:",
            " - what will change - less back pain and improved posture",
            " - who will be affected - employees using the chairs",
            " - when it will happen - within six months",
            "Benefits will be covered in a later question."
        ])
        wrapper.add_input_box(150)

        
class OptionsAnalysis(Section):

    @property
    def section_title(self) -> str: return "Options analysis"

    @property
    def header_section(self): return HeaderSection.SECTIONS

    def create_section(self, wrapper: BusinessCaseWordDocumentWrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}: why is this the best option and how does it show value for money?")
        wrapper.add_paragraph(f"{self.section_number}a. What options have you considered?", True)
        wrapper.add_paragraph("Identify the realistic ways the need could be met, then describe the advantages and disadvantages of each.")
        wrapper.add_paragraph("List at least three options that include continuing with current arrangements and your recommended option.")
        wrapper.add_generic_table(TABLE_DEFINITION.OPTIONS_CONSIDERED)
        wrapper.add_paragraph(f"{self.section_number}b. Explain why the recommended option provides the best overall value for money compared with the alternatives.", True)
        wrapper.add_bullet_point_list(["Explain why you selected this option over the alternatives. Focus on the factors that are most important for your proposal."])
        wrapper.add_help_box([
            "Help with this question:",
            "Keep your response proportionate. For straightforward or low-risk proposals, a short explanation may be enough. You do not need to comment on every area if it is not relevant.",
            "The detailed costs, procurement, delivery and risk information are covered later sections.",
            "You can refer to the MHCLG Appraisal Guide if you need support understanding and assessing value for money."
        ])
        wrapper.add_input_box(100)
        wrapper.add_paragraph(f"{self.section_number}c. What benefits will the recommended option deliver?", True)
        wrapper.add_bullet_point_list(["List the expected benefits. For each one, describe the positive impact, who will benefit and when it is expected to be realised. Include measurable values where possible, but you can also include benefits that cannot be measured easily."])
        wrapper.add_generic_table(TABLE_DEFINITION.EXPECTED_BENEFITS)


class CommercialCase(Section):

    @property
    def section_title(self) -> str: return "Commercial case"

    @property
    def header_section(self): return HeaderSection.SECTIONS

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}: how will you procure this?")
        wrapper.add_paragraph(f"{self.section_number}a. What will your recommended option deliver?", True)
        wrapper.add_bullet_point_list(["Describe the goods, services, works or activities that will be delivered. Include the main outputs and any significant items that are not included."])
        wrapper.add_input_box(100)
        wrapper.add_paragraph(f"{self.section_number}b. How will you buy or obtain what is needed?", True)
        wrapper.add_paragraph("Describe how you plan to buy or obtain what is needed. For example, you may use an existing contract, a framework, a new procurement, a contract variation or modification, or another commercial arrangement.")
        wrapper.add_paragraph("If the approach has not been agreed, state the options being considered and when a decision will be made.")
        wrapper.add_input_box(80)
        wrapper.add_paragraph(f"{self.section_number}c. Why is this the right way to buy or obtain what is needed?", True)
        wrapper.add_paragraph("Explain why this route is appropriate for the value, complexity, timescales and market. Consider:")
        wrapper.add_bullet_point_list([
            "why the route is complient",
            "how it supports value for money",
            "whether the market can deliver what is needed",
            "whether the route supports the required timescales"
        ])
        wrapper.add_input_box(80)
        wrapper.add_paragraph(f"{self.section_number}d. Could any supplier, contract or market issues affect delivery?", True)
        wrapper.add_bullet_point_list(["Describe any supplier, contract or market issues that could affect procurement or delivery."])
        wrapper.add_input_box(50)
        wrapper.add_paragraph(f"{self.section_number}e. Additional procurement and commercial information", True)
        wrapper.add_bullet_point_list(["If you have the information available and it's applicable, please complete the following fields. If you're unsure, work with your Commercial SME to complete this section."])
        wrapper.add_generic_table(TABLE_DEFINITION.ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION)


class FinancialCase(Section):

    @property
    def section_title(self) -> str: return "Financial case"

    @property
    def header_section(self): return HeaderSection.SECTIONS

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title} - can we afford it?")
        wrapper.add_paragraph(f"{self.section_number}a. What is the whole life cost?")
        wrapper.add_generic_table(TABLE_DEFINITION.WHOLE_LIFE_COST)
        wrapper.add_paragraph(f"{self.section_number}b. How will this proposal be funded? Select one option.", True)
        wrapper.add_checkbox([
            "Existing approved budgets. Select this if the full cost is already included in an approved budget for the relevant financial year. Go to question 6d.",
            "New funding request above business planning allocations. Select this if any of the funding needed has not been included in an approved budget. Go to question 6c."
        ])
        wrapper.add_paragraph(f"{self.section_number}c. If this is a new funding request above your business planning allocation, where do you expect it to come from?", True)
        wrapper.add_paragraph("Explain where you expect the funding to come from, if known. For example, additional departmental funding, funding reallocated from another directorate or programme, or an underspend.")
        wrapper.add_paragraph("If this has not yet been agreed, explain what funding is being sought.")
        wrapper.add_input_box(150)
        wrapper.add_paragraph(f"{self.section_number}d. How have you calculated the costs for this proposal?", True)
        wrapper.add_bullet_point_list([
            "Explain how you estimated the costs for this proposal. For example, for licences, state the number of users and unit costs. For people, state the day rates and duration etc.",
            "Only include VAT if non-recoverable."
        ])
        wrapper.add_help_box([
            "Help with this question:",
            "Provide enough evidence for reviewers to understand and check your calculations. The level of detail should reflect the value and complexity of the proposal.",
            "For straightforward or low-value proposals, you can explain your calculations in the text box below.",
            "For more complex proposals, add a link to the detailed cost model and use the text box to summarise your approach."
        ])
        wrapper.add_input_box(50)
        wrapper.add_paragraph(f"{self.section_number}e. Break down the costs by funding type and financial year.", True)
        wrapper.add_bullet_point_list([f"Use the calculations from question {self.section_number}d to enter the costs against the relevant funding type and financial year. Make sure the total matches the whole-life cost in question {self.section_number}a."])
        wrapper.add_help_box([
            "Help with this question:",
            "If you are unsure which funding type applies, including capital departmental expenditure limit (CDEL) or resource departmental expenditure limit (RDEL), speak to your Business Management Office or Finance Business Partner."
        ])
        wrapper.add_generic_table(TABLE_DEFINITION.BREAKDOWN_OF_COST)
        wrapper.add_paragraph(f"{self.section_number}f. How will VAT be treated for this proposal, and why?", True)
        wrapper.add_bullet_point_list([
            "Confirm if the costs include VAT and whether it can be recovered.",
            "If you’re unsure, speak to your Business Management Office or Finance Business Partner."
        ])
        wrapper.add_input_box(40)
        wrapper.add_paragraph(f"{self.section_number}g. Provide the work breakdown structure (WBS) number or cost centre that the funding will be drawn from.", True)
        wrapper.add_generic_table(TABLE_DEFINITION.WBS_OR_COST_CENTRE)
        wrapper.add_paragraph(f"{self.section_number}h. If your proposal has a digital element, what is the spending review bid reference number for the planned spend?", True)
        wrapper.add_generic_table(TABLE_DEFINITION.BID_REFERENCE_NUMBER)
        wrapper.add_paragraph("If your proposal involves a digital element, such as software, platforms, systems, technology or data, add the spending review bid reference number for the planned spend.")
        wrapper.add_hyperlink(
            "https://mhclg.sharepoint.com/:x:/s/DigitalDirectorateCorporateTeam/IQCef7ZzSYgPTKttnQOq0uQuAWpJvuoFGaxQUu5GrdFXiAc?e=kAi2Ve",
            "Use [Digital Spending Review Bids.xlsx.] to find and enter the relevant Spending Review bid reference number.",
            "Digital Spending Review Bids.xlsx."
        )


class ManagementCase(Section):

    @property
    def section_title(self) -> str: return "Management case"

    @property
    def header_section(self): return HeaderSection.SECTIONS

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}: can this be delivered?")
        wrapper.add_paragraph(f"{self.section_number}a. What is your delivery plan?", True)
        wrapper.add_paragraph("What are the start and end dates")
        wrapper.add_generic_table(TABLE_DEFINITION.START_END_DATE)
        wrapper.add_paragraph("Summarise the key milestones and expected timescales")
        wrapper.add_input_box(150)
        wrapper.add_paragraph("Who and what is driving the deadline")
        wrapper.add_input_box(150)
        wrapper.add_paragraph("Proposed checks/review points to monitor progress and quality")
        wrapper.add_input_box(150)
        wrapper.add_paragraph("Governance and change management requirements (if needed).")
        wrapper.add_input_box(150)
        wrapper.add_paragraph(f"{self.section_number}b. Describe the estimated time, people and costs needed to carry out the procurement.", True)
        wrapper.add_bullet_point_list([
            "Identify the roles involved and give an approximate number of people, their grades and the time they will need to spend on the procurement. Include full-time equivalent (FTE) figures where available.",
            "Give your best estimate. If precise figures are not available, provide an approximate cost or describe whether the level of effort is low, medium or high."
        ])
        wrapper.add_input_box(50)
        wrapper.add_paragraph(f"{self.section_number}c. What are the main risks?", True)
        wrapper.add_paragraph("Describe the main risks that could affect successful delivery and explain how you will manage them.")
        wrapper.add_help_box([
            "Help with this question",
            "Think about the main risks that could affect delivery of your proposal (for example, strategic, operational, financial, commercial or technical risks). You can add additional risk boxes should you need to.",
            "For each risk, assess:",
            " - Likelihood - how likely is it to happen? (1 = very unlikely, 5 = very likely)",
            " - Impact - if it happens, how serious would the effect be? (1 = minor impact, 5 = severe impact)",
            " - Multiply the likelihood score by the impact score to get the overall risk score. Maximum score = 25."
        ])
        wrapper.add_paragraph("Risk 1")
        wrapper.add_generic_table(TABLE_DEFINITION.RISK_TABLE)
        wrapper.add_paragraph("Risk 2")
        wrapper.add_generic_table(TABLE_DEFINITION.RISK_TABLE)
        wrapper.add_paragraph("Risk 3")
        wrapper.add_generic_table(TABLE_DEFINITION.RISK_TABLE)
        wrapper.add_paragraph(f"{self.section_number}d. Are there any key dependencies?", True)
        wrapper.add_bullet_point_list(["Describe anything the proposal relies on, such as approvals, resources or other projects."])
        wrapper.add_input_box(50)
        wrapper.add_paragraph(f"{self.section_number}e. How will you measure whether the expected outputs and outcomes have been achieved?", True)
        wrapper.add_bullet_point_list(["Explain how you'll monitor and review the outputs and outcomes."])
        wrapper.add_input_box(100)
        wrapper.add_paragraph(f"{self.section_number}f. What one-off activities, effort and costs will be needed to implement the recommended solution after contract award?", True)
        wrapper.add_paragraph("Explain the additional work needed to make sure the solution delivers the intended outcomes. Include indicative effort and costs where exact figures are not available.")
        wrapper.add_paragraph("Consider factors such as:")
        wrapper.add_bullet_point_list([
            "onboarding",
            "training",
            "communications",
            "process changes",
            "system updates",
            "technical integration",
            "change management",
            "ongoing support"
        ])
        wrapper.add_input_box(100)


class OtherBusinessCases(Section):

    @property
    def section_title(self) -> str: return "Other business cases"

    @property
    def header_section(self): return HeaderSection.SECTIONS

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}")
        wrapper.add_paragraph("If applicable, identify any other business cases in development, pending approval or already approved which could be affected by this case, could affect this case or otherwise seek approval for spend that relates to the same overall piece of work.")
        wrapper.add_generic_table(TABLE_DEFINITION.OTHER_BUSINESS_CASES)

        
class SubjectMatterExpert(Section):

    @property
    def section_title(self) -> str: return "Subject Matter Expert (SME) assurance recommendations and declaration"

    @property
    def header_section(self): return HeaderSection.APPROVALS_AND_SUPPORTING_INFORMATION

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}")
        wrapper.add_paragraph("The subject matter experts (SMEs) who reviewed the proposal must complete this section. All mandatory SME assurance must be complete before the proposal is sent to the Senior Responsible Owner (SRO) or Senior Civil Servant (SCS) for approval.")
        wrapper.add_generic_table(TABLE_DEFINITION.SME_AREA_COMMERCIAL)
        wrapper.add_generic_table(TABLE_DEFINITION.SME_AREA_FINANCE_BUSINESS_PARTNER)
        wrapper.add_h2_section_header("Additional SMEs and reviewers (optional):")
        wrapper.add_paragraph("Additional subject matter experts and reviewers should complete this section if their input or assurance was needed. This may include Digital Front Door, Legal or the Programme Management Office.")
        wrapper.add_paragraph("Add a separate table for each additional subject matter expert or reviewer.")
        wrapper.add_generic_table(TABLE_DEFINITION.ADDITIONAL_SME_OR_REVIEWER)


class SroOrScsApproval(Section):

    @property
    def section_title(self) -> str: return "Senior Responsible Owner (SRO) or Senior Civil Servant (SCS) approval"

    @property
    def header_section(self): return HeaderSection.APPROVALS_AND_SUPPORTING_INFORMATION

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. SRO or SCS approval")
        wrapper.add_generic_table(TABLE_DEFINITION.SRO_OR_SCS_APPROVAL)
        wrapper.add_paragraph("Additional approvals (if applicable)", True)
        wrapper.add_paragraph("Following advice from your Lead SME, record any additional approval processes completed to secure spend approval.")
        wrapper.add_generic_table(TABLE_DEFINITION.ADDITIONAL_APPROVALS)


class SupportingDocuments(Section):

    @property
    def section_title(self) -> str: return "Supporting documents"

    @property
    def header_section(self): return HeaderSection.APPROVALS_AND_SUPPORTING_INFORMATION

    def create_section(self, wrapper):
        wrapper.add_h2_section_header(f"{self.section_number}. {self.section_title}")
        wrapper.add_paragraph("Add a link to each supporting document, with its title and short description.")
        wrapper.add_empty_paragraph()
        wrapper.add_paragraph("You're nearly there! Once you recieve approval:", True)
        wrapper.add_paragraph("Once you have received all required approvals, use your unique link below to return to the business case service and upload your completed business case.")
        wrapper.add_hyperlink("https://www.google.com", "Link: [completion_link]", "[completion_link]")
        wrapper.add_paragraph("If you have problems uploading your business case, contact")
        wrapper.add_hyperlink("Businesscaseproject@communities.gov.uk", "Businesscaseproject@communities.gov.uk.", "Businesscaseproject@communities.gov.uk", True)
        wrapper.add_paragraph("To receive the funding, you must also raise a buying request in SAP.")
