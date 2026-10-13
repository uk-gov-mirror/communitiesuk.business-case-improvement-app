
from enum import IntEnum, auto

from .sections import (
    Section, 
    ParticipantsAndOrganisationalDetails,
    ExecutiveSummarySection,
    StrategicCase,
    OptionsAnalysis,
    CommercialCase,
    FinancialCase,
    ManagementCase,
    OtherBusinessCases,
    SubjectMatterExpert,
    SroOrScsApproval,
    SupportingDocuments,
    HeaderSection
)

from apps.word_doc_services.word_document_wrapper import BusinessCaseWordDocumentWrapper
from apps.triage.triage_data import TriageData

class RouteChosen(IntEnum):
    Procurement = auto()
    Grants = auto()
    Undetermined= auto()

'''
List of all the sections that need to go into a template.
Listed as types to avoid instantiating the classes without reason
'''
sections_per_template: dict[RouteChosen, list[type[Section]]] = {
    RouteChosen.Procurement: [
        ParticipantsAndOrganisationalDetails,
        ExecutiveSummarySection,
        StrategicCase,
        OptionsAnalysis,
        CommercialCase,
        FinancialCase,
        ManagementCase,
        OtherBusinessCases,
        SubjectMatterExpert,
        SroOrScsApproval,
        SupportingDocuments
    ],
    RouteChosen.Grants:[

    ]
}


class WordDocumentOrchestrator():
    def __init__(self, answers: dict[str, str]):
        self.triage_data: TriageData = TriageData(answers)
        self.sections_required: list[Section] = []
        self.route: RouteChosen
        self.wrapper: BusinessCaseWordDocumentWrapper = BusinessCaseWordDocumentWrapper()

    '''
    Summary:
        Find the sections needed, determined by the route, and then instantiate them
    '''
    def __determine_sections_to_create(self):
        route: RouteChosen = self.__determine_route()

        if route == RouteChosen.Undetermined:
            return

        self.sections_required = [c() for c in sections_per_template[route]]
         

    def __determine_route(self) -> RouteChosen:
        if self.triage_data.is_procurement_route_completed:
            return RouteChosen.Procurement

        return RouteChosen.Undetermined

    '''
    Summary:
        Generic section so created here. Essentially an index 
    '''
    def __create_what_youll_be_asked(self):
        self.wrapper.add_h2_section_header("What you'll be asked in this document:")

        for header_title in HeaderSection:
            # gets a list of headers
            headers: list[Section] = self.__get_list_of_filtered_sections(header_title)

            header_titles: list[str] = [f"{self.sections_required.index(obj) + 1}. {obj.section_title}" for obj in headers]
            header_titles.insert(0, header_title)
            self.wrapper.add_closely_spaced_content(header_titles)

    '''
    Summary:
        Generic section so created here.
    '''
    def __create_before_you_start(self):
        self.wrapper.add_empty_paragraph()
        self.wrapper.add_paragraph("Before you start", True)
        self.wrapper.add_paragraph("This template aligns to the HM Treasury Green Book Five Case Model. The questions will guide you through developing a clear, evidence-based business case.")
        self.wrapper.add_hyperlink("Commercial@communities.gov.uk", "You must speak to the Commercial team about your procurement before you start drafting this document. If you're unsure who this is, contact Commercial@communities.gov.uk.",
                                   "Commercial@communities.gov.uk.", True)
        self.wrapper.add_help_box(["Look for the blue guidance boxes for help with drafting your answers."])
        self.wrapper.add_paragraph("Once you are finished", True)
        self.wrapper.add_paragraph("Once you have received all required approvals, use your unique link below to return to the business case service and upload your completed business case. You can find this link on the last page of this document, too.")
        self.wrapper.add_hyperlink("https://www.google.com", "Link: [completion_link]", "[completion_link]")
        self.wrapper.add_help_box(["This cover page is for guidance only and can be deleted once the author has read it."])
    

    '''
    Summary:
        return all sections
    '''
    def __get_list_of_filtered_sections(self, header_section_wanted: HeaderSection) -> list[Section]:
        result: list[Section] | None =  [s for s in self.sections_required if s.header_section == header_section_wanted]

        if not isinstance(result, list):
            result = []

        return result


    def populate_word_doc(self):
        business_case_title: str = self.triage_data.business_case_title

        self.__determine_sections_to_create()
        
        self.wrapper.add_h2_section_header(f"This is your business justification case template for {business_case_title}")
        self.__create_what_youll_be_asked()
        self.__create_before_you_start()
        # add section is a new page before the main content
        self.wrapper.doc.add_section()
        self.wrapper.add_h1_section_header(business_case_title)

        # loop each section, and for each one call the method for creating the section.
        for section in self.sections_required:
            section.section_number = self.sections_required.index(section) + 1
            section.create_section(self.wrapper)
            self.wrapper.add_empty_paragraph()

        self.wrapper.set_document_margins(1, 1, 1)

