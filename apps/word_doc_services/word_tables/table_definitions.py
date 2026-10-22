from enum import IntEnum, auto
from dataclasses import dataclass, field
from .table_common_resources import get_fy_and_relative_next_fy

class TABLE_DEFINITION(IntEnum):
    AUTHOR_SHOULD_COMPLETE_SECTION = auto()
    OPTIONS_CONSIDERED = auto()
    EXPECTED_BENEFITS = auto()
    ECONOMIC_CASE = auto()
    ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION = auto()
    BREAKDOWN_OF_COST = auto()
    WHOLE_LIFE_COST = auto()
    START_END_DATE = auto()
    RISK_TABLE = auto()
    OTHER_BUSINESS_CASES = auto()
    SME_AREA_COMMERCIAL = auto()
    WBS_OR_COST_CENTRE = auto()
    BID_REFERENCE_NUMBER = auto()
    SME_AREA_FINANCE_BUSINESS_PARTNER = auto()
    ADDITIONAL_SME_OR_REVIEWER = auto()
    SRO_OR_SCS_APPROVAL = auto()
    ADDITIONAL_APPROVALS = auto()
    GRANT_VALUE = auto()
    ECONOMIC_CASE_LOCAL_AUTH = auto()
    COMMERCIAL_CASE = auto()
    COMMERCIAL_CASE_IN_AID = auto()
    COMMERCIAL_CASE_IF_GENERAL = auto()
    COMMERCIAL_CASE_FORMULA = auto()
    COMMERCIAL_CASE_GENERAL_VIA_DIRECT_AWARD = auto()
    FINANCIAL_CASE = auto()
    MANAGEMENT_CASE_RISK_MGMT = auto()
    MANAGEMENT_CASE_PERFORMANCE = auto()
    MANAGEMENT_CASE_GENERAL_GRANTS = auto()
    MANAGEMENT_CASE_CLASSIFICATION = auto()


class HEADER_DIRECTION(IntEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()

@dataclass
class _ExtraCellContent:
    row: int
    column: int
    content: str
    is_italic: bool = field(default=True)
    is_bold: bool = field(default=False)

@dataclass
class _TableContent:
    definition: TABLE_DEFINITION
    header_direction: HEADER_DIRECTION
    headers: list[str] = field(default_factory=list[str])
    bold_headers: bool = field(default=True)
    headers_alternate_direction_object_count: int = field(default=2)
    extra_content: list[_ExtraCellContent] = field(default_factory=list[_ExtraCellContent])
    

TABLE_REGISTRY = [
    _TableContent(
        definition = TABLE_DEFINITION.AUTHOR_SHOULD_COMPLETE_SECTION,
        header_direction = HEADER_DIRECTION.VERTICAL,
        headers = [
            "Business case unique reference number:",
            "Lead author name",
            "Lead author team:",
            "Business case contributors or reviewers:",
            "SRO or area SCS name:",
            "What project is this part of?",
            "What programme is this part of?",
            "Portfolio area:",
            "Directorate:",
            "Type of business case:"
        ],
        extra_content=[
            _ExtraCellContent(
                row=4,
                column=2,
                content="List any additional people who helped draft, develop or review this business case before it was submitted for approval. You don't need to include anyone listed in 'SME assurance, recommendations and declarations', or 'SRO or Senior Civil Servant SCS approval' sections."
            )
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.EXPECTED_BENEFITS,
        header_direction= HEADER_DIRECTION.HORIZONTAL,
        headers_alternate_direction_object_count = 5,
        headers=[
            "Benefit",
            "Value or positive impact and who this will benefit",
            "When will this benefit be realised?"
        ],
        extra_content=[
            _ExtraCellContent(
                row=2,
                column=1,
                content="Insert more rows as appropriate"
            )
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.OPTIONS_CONSIDERED,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Option 1 (recommended)",
            "Option 2",
            "Option 3"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Contract number(s) for new contracts (if applicable)",
            "Contract numbers(s) for contracts being changed (if applicable)",
            "Accredited Contract Manager (and accreditation level secured or sought)"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.BREAKDOWN_OF_COST,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers_alternate_direction_object_count=4,
        headers=[
            "Breakdown of cost",
            "CDEL",
            "CDEL FT",
            "RDEL Programme",
            "RDEL Admin",
            "Local Gov DEL",
            "Other",
            "Total (£m)"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content=f"FY{get_fy_and_relative_next_fy()}", is_italic=False, is_bold=True),
            _ExtraCellContent(row=1, column=3, content=f"FY{get_fy_and_relative_next_fy(1)}", is_italic=False, is_bold=True),
            _ExtraCellContent(row=1, column=4, content=f"FY{get_fy_and_relative_next_fy(2)}", is_italic=False, is_bold=True)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.WHOLE_LIFE_COST,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=["Whole Life Cost"],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="£", is_italic=False)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.START_END_DATE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Start date",
            "End date"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.RISK_TABLE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe the risk",
            "What's the impact if this risk happens?",
            "Risk scores:",
            "Likelihood score =",
            "Impact score =",
            "Overall risk score (likelihood x impact) =",
            "Mitigation: What will you do to reduce or manage the risk? Describe who is responsible and when it will be reviewed."
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.OTHER_BUSINESS_CASES,
        header_direction=HEADER_DIRECTION.HORIZONTAL,
        headers_alternate_direction_object_count=3,
        headers=[
            "Business case title",
            "Activity / procurement",
            "Author / lead contact"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.SME_AREA_COMMERCIAL,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "SME Area:",
            "Declaration:",
            "Name:",
            "Recommendation:",
            "Date:",
            "Any additional comments, risks or conditions:"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="Commercial", is_italic=False),
            _ExtraCellContent(row=2, column=2, 
                content="I confirm this case has met the minimum standards of good practice and fulfils all applicable compliance criteria. I also confirm that, where necessary, I have advised that this case has been referred to additional corporate experts to ensure adequate technical support was provided.", is_italic=False)

        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.WBS_OR_COST_CENTRE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=["WBS or cost centre"],
        headers_alternate_direction_object_count=2
    ),
    _TableContent(
        definition=TABLE_DEFINITION.BID_REFERENCE_NUMBER,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=["Spending review bid reference number"],
        headers_alternate_direction_object_count=2
    ),
    _TableContent(
        definition=TABLE_DEFINITION.SME_AREA_FINANCE_BUSINESS_PARTNER,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "SME Area:",
            "Declaration:",
            "Name:",
            "Recommendation:",
            "Date:",
            "Any additional comments, risks or conditions:"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="Finance Business Partner", is_italic=False),
            _ExtraCellContent(row=2, column=2,
                content="I confirm that the planned activity/procurement detailed in this case meets affordability criteria and there are sufficient funds approved within the budget to cover the requested amount of spend.",
                is_italic=False
            )
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ADDITIONAL_SME_OR_REVIEWER,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "SME Area:",
            "Name:",
            "Recommendation:",
            "Date:",
            "Any additional comments, risks or conditions:"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.SRO_OR_SCS_APPROVAL,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Approval role:",
            "Declaration:",
            "Name:",
            "Date:"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="SRO/Area SCS Declaration", is_italic=False),
            _ExtraCellContent(row=2, column=2, content="I confirm that the planned activity/procurement in this case complies with departmental guidance and processes. I also confirm that I am satisfied to approve this expenditure, accepting the risks detailed within this case and those inherent to the activity/procurement being undertaken.", is_italic=False)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ADDITIONAL_APPROVALS,
        header_direction=HEADER_DIRECTION.HORIZONTAL,
        headers_alternate_direction_object_count=4,
        headers=[
            "Approval activity",
            "Authority holding body/person",
            "Date of approval",
            "Documentation"
        ],
        extra_content=[
            _ExtraCellContent(row=2, column=1, content="e.g. Cabinet office spend control"),
            _ExtraCellContent(row=2, column=2, content="e.g. Cabinet office"),
            _ExtraCellContent(row=2, column=3, content="e.g. 11/05/2026"),
            _ExtraCellContent(row=2, column=4, content="Insert links")
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.GRANT_VALUE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Total grant value (see financial case for RDEL/CDEL breakdown)",
            "Recipient Organisation Type",
            "Country",
            "What is the purpose of the grant? What problem or opportunity does it address? Describe the current situation. Who does it affect and why change is needed?",
            "Why use a grant and not a procurement? (Grant Justification - link to checklist / guidance)",
            "Confirm checklist",
            "Grant Route",
            "Allocation Method",
            "Confirm which legal power (Legislation)",
            "Does the accounting officer responsibility sit with MHCLG?"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="£", is_italic=False),
            _ExtraCellContent(row=10, column=2, content="Y/N", is_italic=False)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ECONOMIC_CASE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "How the project / programme is to be delivered?",
            "Why is this the preferred option?",
            "What is the quantity of MHCLG resource to be allocated to this grant?",
            "What costs and resources will the project or programme require?",
            "How will roles and responsibilities meet the three lines of defence requirements?",
            "Which organisation will be responsible for carrying out this assurance?",
            "How will you collect the information needed from grant recipients for assurance?",
            "Will the grant be used for economic activity?",
            "If you answered Yes to the question above, explain how you have considered the Subsidy Control Act and the outcome."
        ],
        extra_content=[
            # this won't format as a list, only like this for Dev clarity. Maybe add functionality after testing
            _ExtraCellContent(row=4, column=2, content="£", is_italic=False),
            _ExtraCellContent(row=8, column=2, content="Y/N", is_italic=False),
            _ExtraCellContent(row=9, column=2, content="Only answer if the above is Yes", is_italic=False, is_bold=True)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ECONOMIC_CASE_LOCAL_AUTH,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Have you considered and applied the Funding Simplification Doctrine?",
            "Describe the outcomes of that consideration",
            "Confirm that you have completed the required pro forma and validated the outcome with the MHCLG Funding Simplification team."
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.COMMERCIAL_CASE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe how grant recipients will be selected",
            "Explain why",
            "Grant Methodology",
            "Value for Money",
            "'Find a Grant' Advertising",
            'Government Grant Information System'
        ],
        extra_content=[
            _ExtraCellContent(row=3, column=2, content="[outline the methodology you will be using to award the grant. Refer to guidance and work with your corporate partner]"),
            _ExtraCellContent(row=4, column=2, content="[outline how you will evidence value for money, what reporting will be collected from the recipient organisation to evidence this]"),
            _ExtraCellContent(row=5, column=2, content="[confirm that you have considered whether your grant needs to be advertised on the government wide 'find a grant' service. Refer to guidance and work with your corporate partner]"),
            _ExtraCellContent(row=6, column=2, content="Add your GGIS reference here")
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.COMMERCIAL_CASE_IN_AID,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe the recipient",
            "Describe the purpose",
            "Describe allocation arrangements"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.COMMERCIAL_CASE_IF_GENERAL,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe the application process",
            "Describe scoring criteria and weighting",
            "Describe the appraisal process",
            "Describe how decisions will be reached"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.COMMERCIAL_CASE_FORMULA,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe the data used to calculate proposed allocations"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.COMMERCIAL_CASE_GENERAL_VIA_DIRECT_AWARD,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe how the proposed grant recipient has prepared its budget estimates",
            "Describe your assessment of value for money and/or the clear criteria for the award of the proposed grant if it is a criteria-based fund",
            "Include a clear, robust justification for why you have chosen a non-competitive route in this case."
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.FINANCIAL_CASE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Funding Agreement Type",
            "Payment Timescales. Are these payments made in arrears or in advance?",
            "Payment Timescales. What is the date of the first payment?",
            "Payment information. Is the grant ring fenced",
            "Breakdown of cost?"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="[confirm the type of funding agreement type you will use]"),
            _ExtraCellContent(row=2, column=2, content="Y/N", is_italic=False),
            _ExtraCellContent(row=4, column=2, content="Y/N", is_italic=False)
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.MANAGEMENT_CASE_RISK_MGMT,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Risk Management",
            "Have you completed a mandatory, separate Fraud Risk Assessment for your grant scheme, in line with the MHCLG Fraud Risk Assessment policy and guidance?",
            "Due Diligence Checks"
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="Describe how risk to public money is to be managed", is_italic=False),
            _ExtraCellContent(row=2, column=2, content="Y/N", is_italic=False),
            _ExtraCellContent(row=3, column=2, content="[Confirm what due diligence checks you will be undertaking and who will be responsible for doing these]")
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.MANAGEMENT_CASE_PERFORMANCE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Describe how and when the performance of the grant recipient will be measured and monitored.",
            "If the proposed grant scheme has or will be seeking exemption from these requirements for any reason, the scope and rationale for any exemptions, explain why.",
            "Confirm that your evaluation will be published on the new government Evaluation Registry"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.MANAGEMENT_CASE_GENERAL_GRANTS,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Confirm that the grant recipients will be expected to observe the 'Funded by UK Government' branding requirements",
            "If the proposed grant scheme has or will be seeking exemption from these requirements for any reason, the scope and rationale for any exemptions, explain why.",
            "Has the exemption must be approved by the relevant Senior Officer Responsible?",
            "Have you sent a copy to the Central Grants Hub?"
        ]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.MANAGEMENT_CASE_CLASSIFICATION,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "The Central Grants Hub, as part of the assurance of your business case, we will review the relevant information and assess your grant against the framework criteria and seek your agreement to the proposed classification of Gold, Silver or Bronze. Record their decision here."
        ],
        extra_content=[
            _ExtraCellContent(row=1, column=2, content="Confirm if your Grant is classified as Gold, Silver or Bronze")
        ]
    )
]
