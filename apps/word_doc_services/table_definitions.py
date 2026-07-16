from enum import IntEnum, auto
from dataclasses import dataclass, field

from docx.shared import Cm

table_footer_word_count: str = "Word count guideline: {} words"
# usage: table_footer=f"{table_footer_word_count}".format(300),

class TableDefinition(IntEnum):
    DEVELOP_AND_SUPPORT_PROPOSAL = auto()
    EXPECTED_BENEFITS = auto()
    SPEND_AT_RISK = auto()
    ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION = auto()
    HOW_INTEND_PROPOSAL_FUNDED = auto()
    FUNDING_REFERENCE_NUMBER = auto()
    WHOLE_LIFE_COST = auto()
    BREAKDOWN_OF_COST = auto()
    MAIN_RISKS = auto()
    OTHER_BUSINESS_CASES = auto()
    SME_RECOMMENDATIONS_COMMERCIAL = auto()
    SME_RECOMMENDATIONS_FINANCE = auto()
    ADDITIONAL_SME = auto()
    SRO_SCS_APPROVAL = auto()
    SINGLE_CELL_TEXT_BOX = auto()

@dataclass
class _TextRunData:
    text: str
    italic: bool = False
    bold: bool = False

@dataclass
class _ParagraphData:
    runs: list[_TextRunData] = field(default_factory=list)

# NOTE: If the last row(s) or column(s) in a table should be blank, you need to add a blank record in the table def
    # To add a blank row 2 to a table, do: _CellData(row=2, column=1)
    # To add a blank column 2 to a table, do _CellData(row=1, column=2)
    # If you have multiple blank cells to add, you need only add the last in the series
    # so to add 2 blank rows after a header row (so 3 rows total) you need only write _CellData(row=3, column=1)
    # Same goes for extra blank columns.
@dataclass
class _CellData:
    row: int
    column: int # 15.9cm total in table widths available currently
    paragraphs: list[_ParagraphData] = field(default_factory=list)

@dataclass
class _TableContent:
    definition: TableDefinition
    row_heights: list[Cm] = field(default_factory=list)
    column_widths: list[Cm] = field(default_factory=list)
    cells: list[_CellData] = field(default_factory=list)

TABLE_REGISTRY = [
    _TableContent(
        definition=TableDefinition.DEVELOP_AND_SUPPORT_PROPOSAL,
        row_heights=[Cm(5.08), Cm(1.27), Cm(2.03), Cm(1.27), Cm(1.27), Cm(1.27), Cm(1.27), Cm(1.27)],
        column_widths=[Cm(4.89), Cm(11.01)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Title:",
                        bold=True
                    )
                ])    
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Primary author team:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Case contributors and /or reviewers:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="[If applicable, list anyone who helped draft, develop or review the business case before it was submitted for approval. Do not include subject matter experts (SMEs) or SRO/SCS, as these named will be captured separately elsewhere in this document]",
                        italic=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Project title:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Programme title:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=6, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Portfolio area:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=7, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Directorate:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=8, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Type of business case:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=8, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Business Justification Case - Procurement",
                        italic=True
                    )
                ])
            ])
        ]
    ),
    _TableContent(
        definition=TableDefinition.FUNDING_REFERENCE_NUMBER,
        row_heights=[Cm(1.51)],
        column_widths=[Cm(7.95)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="What is the reference number?",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2),
        ]   
    ),
    _TableContent(
        definition=TableDefinition.WHOLE_LIFE_COST,
        row_heights=[Cm(1.51)],
        column_widths=[Cm(7.95)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="What is the Whole Life Cost? (£m)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2),
        ]   
    ),
    _TableContent(
        definition=TableDefinition.BREAKDOWN_OF_COST,
        row_heights=[Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.01)],
        column_widths=[Cm(4.20), Cm(3.9), Cm(3.9), Cm(3.9)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Breakdown of cost",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="FY26/27",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=3, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="FY27/28",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=4, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="FY28/29",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="CDel (£m)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="RDel (£m)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Other (£m)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Total (£m)",
                        bold=True
                    )
                ])
            ]),
        ]   
    ),
    _TableContent(
        definition=TableDefinition.EXPECTED_BENEFITS,
        row_heights=[Cm(1.27), Cm(1.27)],
        column_widths=[Cm(5.3), Cm(5.3), Cm(5.3)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Benefit",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Value/positive impact",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=3, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="When will this benefit be realised?",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=1)
        ]
    ),
    _TableContent(
        definition=TableDefinition.SPEND_AT_RISK,
        row_heights=[Cm(0.74), Cm(1.27), Cm(1.27), Cm(1.27)],
        column_widths=[Cm(7.95), Cm(7.95)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Spend at risk",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Value",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Requirement cost\n(cost of the contract with extensions)"
                    )
                ])
            ]),
            _CellData(row=2, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="£"
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Procurement Cost\n(How much will be spent on labour to carry out the procurement)"
                    )
                ])
            ]),
            _CellData(row=3, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="£"
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Implementation Costs\n(Once the service/product has been procured what costs are there to ensure proper utilisation)"
                    )
                ])
            ]),
            _CellData(row=4, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="£"
                    )
                ])
            ]),
        ]
    ),
    _TableContent(
        definition=TableDefinition.ADDITIONAL_PROCUREMENT_AND_COMMERCIAL_INFORMATION,
        row_heights=[Cm(1.27), Cm(1.27), Cm(1.27), Cm(1.27), Cm(1.27), Cm(1.27)],
        column_widths=[Cm(7.95), Cm(7.95)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Contract number(s) for new contracts",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Contract numbers(s) for contracts being changed",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Accredited Contract Manager (and accreditation level secured or sought)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Have you completed the Procurement Strategy (optional)?",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Y/N/NA"
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Have you completed the Evaluation Report (optional)?",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Y/N/NA"
                    )
                ])
            ]),
            _CellData(row=6, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Have you completed the Contract Modification request (optional)?",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=6, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Y/N/NA"
                    )
                ])
            ])
        ]   
    ),
    _TableContent(
        definition=TableDefinition.HOW_INTEND_PROPOSAL_FUNDED,
        row_heights=[Cm(1.51), Cm(1.51)],
        column_widths=[Cm(1.3), Cm(14.6)],
        cells=[
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Existing approved budgets.",
                        bold=True
                    ),
                    _TextRunData(
                        text=" The funding already exists within an approved budget, forecast, or Spending Review allocation."
                    )
                ])
            ]),
            _CellData(row=2, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="New funding request above forecast or Spend Review allocations.",
                        bold=True
                    ),
                    _TextRunData(
                        text="\nThe proposal requires new funding that has not yet been approved."
                    )
                ])
            ])
        ]   
    ),
    _TableContent(
        definition=TableDefinition.MAIN_RISKS,
        row_heights=[Cm(0.5), Cm(1.27)],
        column_widths=[Cm(2.65), Cm(3.65), Cm(3.7), Cm(6.06)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Risk type (strategic, operational, financial, commercial, technical)",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Risk",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=3, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Impact if it happens",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=4, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Your Mitigation Plan "
                    ),
                    _TextRunData(
                        text="(What will you do to fix it and when will this be reviewed?)",
                        bold=True,
                        italic=True
                    )
                ])
            ]),
            _CellData(row=2, column=1)
        ]   
    ),
    _TableContent(
        definition=TableDefinition.OTHER_BUSINESS_CASES,
        row_heights=[Cm(1.01), Cm(1.01), Cm(1.01)],
        column_widths=[Cm(5.3), Cm(5.3), Cm(5.3)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Business Case Title",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Activity / procurement",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=3, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Author / lead contact",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=1)
        ]
    ),
    _TableContent(
        definition=TableDefinition.SME_RECOMMENDATIONS_COMMERCIAL,
        row_heights=[Cm(1.19), Cm(3.57), Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.93)],
        column_widths=[Cm(6.90), Cm(9.0)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="SME Area:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Commercial"
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Declaration:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="I confirm this case has met the minimum standards of good practice and fulfils all applicable compliance criteria. I also confirm that, where necessary, I have advised that this case has been referred to additional corporate experts to ensure adequate technical support was provided.",
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Name:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Recommendation:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Date:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=6, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Any additional comments, risks or conditions:",
                        bold=True
                    )
                ])
            ]),
        ]
    ),
    _TableContent(
        definition=TableDefinition.SME_RECOMMENDATIONS_FINANCE,
        row_heights=[Cm(1.19), Cm(3.57), Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.93)],
        column_widths=[Cm(6.90), Cm(9.0)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="SME Area:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Finance Business Partner"
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Declaration:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="I confirm that the planned activity/procurement detailed in this case meets affordability criteria and there are sufficient funds approved within the budget to cover the requested amount of spend.",
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Name:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Recommendation:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Date:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=6, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Any additional comments, risks or conditions:",
                        bold=True
                    )
                ])
            ]),
        ]
    ),
    _TableContent(
        definition=TableDefinition.ADDITIONAL_SME,
        row_heights=[Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.01), Cm(1.93)],
        column_widths=[Cm(6.90), Cm(9.0)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="SME Area:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Name:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Recommendation:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Date:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=5, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Any additional comments, risks or conditions:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2)
        ]
    ),
    _TableContent(
        definition=TableDefinition.SRO_SCS_APPROVAL,
        row_heights=[Cm(1.01), Cm(2.7), Cm(1.01), Cm(1.01)],
        column_widths=[Cm(5.30), Cm(10.60)],
        cells=[
            _CellData(row=1, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="SME Area:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=1, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="SRO/Area SCS Declaration"
                    )
                ])
            ]),
            _CellData(row=2, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Declaration:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=2, column=2, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="I confirm that the planned activity/procurement in this case complies with departmental guidance and processes. I also confirm that I am satisfied to approve this expenditure, accepting the risks detailed within this case and those inherent to the activity/procurement being undertaken.",
                    )
                ])
            ]),
            _CellData(row=3, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Name:",
                        bold=True
                    )
                ])
            ]),
            _CellData(row=4, column=1, paragraphs=[
                _ParagraphData(runs=[
                    _TextRunData(
                        text="Date:",
                        bold=True
                    )
                ])
            ]),
        ]
    ),
    _TableContent(
        definition=TableDefinition.SINGLE_CELL_TEXT_BOX,
        row_heights=[Cm(2.5)],
        column_widths=[Cm(15.9)],
        cells=[
            _CellData(row=1, column=1)
        ]   
    )
]

