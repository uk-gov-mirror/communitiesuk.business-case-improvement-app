from enum import IntEnum, auto
from dataclasses import dataclass, field

from docx.shared import Cm

class TABLE_DEFINITION(IntEnum):
    DEVELOP_AND_SUPPORT_PROPOSAL = auto()
    EXPECTED_BENEFITS = auto()
    ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION = auto()
    BREAKDOWN_OF_COST = auto()
    COST_CENTRE = auto()
    WHOLE_LIFE_COST = auto()
    OTHER_BUSINESS_CASES = auto()
    SME_AREA = auto()
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
    headers: list[str] = field(default_factory=list[str])
    bold_headers: bool = field(default=True)
    headers_alternate_direction_object_count: int = field(default=2)
    extra_content: list[_ExtraCellContent] = field(default_factory=list[_ExtraCellContent])
    

TABLE_REGISTRY = [
    _TableContent(
        definition = TABLE_DEFINITION.DEVELOP_AND_SUPPORT_PROPOSAL,
        header_direction = HEADER_DIRECTION.VERTICAL,
        headers = [
            "Title:",
            "Primary Author Team",
            "Case contributors and /or reviewers:",
            "SRO or area SCS name (approver):",
            "What project is this part of?",
            "What programme is this part of?",
            "Portfolio area:",
            "Directorate:",
            "Type of business case:"
        ],
        extra_content=[
        _ExtraCellContent(
            row=3,
            column=2,
            content="[If applicable, list anyone who helped draft, develop or review the business case before it was submitted for approval. Do not include subject matter experts (SMEs) or SRO/SCS, as these named will be captured separately elsewhere in this document]"
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
        definition=TABLE_DEFINITION.ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "Contract number(s) for new contracts",
            "Contract numbers(s) for contracts being changed",
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
        definition=TABLE_DEFINITION.COST_CENTRE,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=["WBS or cost centre"]
    ),
    _TableContent(
        definition=TABLE_DEFINITION.WHOLE_LIFE_COST,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=["Whole Life Cost"]
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
        definition=TABLE_DEFINITION.SME_AREA,
        header_direction=HEADER_DIRECTION.VERTICAL,
        headers=[
            "SME Area:",
            "Declaration:",
            "Name:",
            "Recommendation:",
            "Date:",
            "Any additional comments, risks or conditions:"
        ],
    ),
    _TableContent(
        definition=TABLE_DEFINITION.ADDITIONAL_APPROVALS,
        header_direction=HEADER_DIRECTION.HORIZONTAL,
        headers=[
            "Approvals",
            "Authority holding body/person",
            "Date of approval",
            "Documentation"
        ],
        extra_content=[
            _ExtraCellContent(row=2, column=1, content="e.g. Cabinet office spend control"),
            _ExtraCellContent(row=2, column=2, content="e.g. Cabinet office"),
            _ExtraCellContent(row=2, column=3, content="e.g 11/05/2026"),
            _ExtraCellContent(row=2, column=4, content="Insert links"),
        ]
    )
]


