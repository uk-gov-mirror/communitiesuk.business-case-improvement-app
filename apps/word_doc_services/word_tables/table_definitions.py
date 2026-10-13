from enum import IntEnum, auto
from dataclasses import dataclass, field

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
    optional_headers: dict[str, list[str]] = field(default_factory=dict[str, list[str]])
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
            content="List any additional people who helped draft, develop or review this business case before it was submitted for approval. You don't need to include anyone listed in sections 9 and 10."
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
        definition=TABLE_DEFINITION.ECONOMIC_CASE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "How the project / programme is to be delivered",
            "Why is this the preferred option?",
            "What is the quantity of MHCLG resource to be allocated to this grant?",
            "What costs and resources will the project or programme require?",
            "How will roles and responsibilities meet the three lines of defence requirements?",
            "Which organisation will be responsible for carrying out this assurance?",
            "How will you collect the information needed from grant recipients for assurance?",
            "Will the grant be used for economic activity?", ####
        ],
        optional_headers={
            "grants_for_local_auth":[
                "Have you considered and applied the Funding Simplification Doctrine? Funding Simplification Doctrine?",
                "Describe the outcomes of that consideration",
                "Confirm that you have completed the required pro forma and validated the outcome with the MHCLG Funding Simplification team."
            ]
        }
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
            _ExtraCellContent(row=1, column=2, content="FY-X", is_italic=False, is_bold=True),
            _ExtraCellContent(row=1, column=3, content="FY-Y", is_italic=False, is_bold=True),
            _ExtraCellContent(row=1, column=4, content="FY-Z", is_italic=False, is_bold=True)
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
            "Desribe the risk",
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
            _ExtraCellContent(row=2, column=4, content="e.g. Cabinet office spend control")
        ]
    )
]
