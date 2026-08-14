
from docx.enum.style import WD_STYLE_TYPE
from docx.document import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx import Document as WordDoc

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

class _SectionContent():
    def __init__(self):
        self.clear()

    def clear(self):
        self.section_header = None
        self.content = []

    def add_section_header(self, header: str):
        self.section_header = header

    def add_item_to_content(self, item: str | dict[str, str]):
        self.content.append(item)

    @property
    def is_valid(self) -> bool:
        return (self.section_header is not None 
                and self.section_header != "")

@require_POST
def trigger_parsing(request):
    doc = WordDoc("FullDoc.docx")

    result = parse_word_document(doc)
    return result  


'''
Summary:
    Read through a Word Doc and extract the Tables and Paragraphs contained in it
    Currently, formatting is ignored.
Returns:
     
Params:
    doc - the word Doc to extract sections from
'''
def parse_word_document(doc: Document) -> tuple[list, dict]:
    sections: list[_SectionContent] = []
    temp_section: _SectionContent = _SectionContent()
    summary_section: dict = {}

    for s in doc.sections:
        for content in s.iter_inner_content():

            if not content or not content.style:
                continue

            if isinstance(content, Paragraph):
                content_text = escaped_string(content.text)
                if content_text == '':
                    continue

                if content.style.name == "Heading 1":
                    if temp_section.is_valid:
                        sections.append(temp_section)

                    temp_section = _SectionContent()
                    temp_section.add_section_header(content_text)
                else:
                    temp_section.add_item_to_content(content_text)
            elif isinstance(content, Table):
                temp_section.add_item_to_content(_extract_data_from_doc_table(content))

    summary_section = _get_summary_data(doc)
    
    return sections, summary_section


def _get_summary_data(doc: Document) -> dict:
    summary_data: dict = {}
    directorate: str
    sro_scs: str
    approved_by_sro_scs: str = ''
    author: str

    author, sro_scs, directorate = _get_data_from_details_table(doc)
 
    summary_data["author"] = author
    summary_data["sro_scs"] = sro_scs
    summary_data["directorate"] = directorate
    summary_data["summary"] = _get_summary(doc)
    summary_data["whole_life_cost"] = _get_whole_life_cost(doc)

    return summary_data


def _get_whole_life_cost(doc: Document) -> str:
    whole_life_cost: str = "-"

    if doc and doc.tables:
        for tbl in doc.tables:
            if escaped_string(tbl.rows[0].cells[0].text) == "Whole Life Cost":
                whole_life_cost = f'£{escaped_string(tbl.rows[0].cells[1].text)}'
                break

    return whole_life_cost


def _get_summary(doc: Document) -> str:
    summary:str = "-"

    if doc and doc.tables[2]:
        tbl = doc.tables[2]
        summary = tbl.rows[0].cells[0].text

    return summary


def _get_data_from_details_table(doc: Document) -> tuple[str, str, str]:
    author_name_header: str = "author name:"
    sro_or_scs_header: str = "sro or area scs name (approver):"
    directorate_header: str = "directorate:"

    author_name_result: str = "-"
    sro_or_scs_result: str = "-"
    directorate_result: str = "-"

    key_words = {author_name_header, sro_or_scs_header , directorate_header}

    if doc and doc.tables[0]:
        tbl = doc.tables[0]

        for r in tbl.rows:
            cell_header: str = escaped_string(r.cells[0].text).lower()
            if cell_header in key_words:
                match cell_header:
                    case header if header == author_name_header:
                        author_name_result = escaped_string(r.cells[1].text)
                    case header if header == sro_or_scs_header:
                        sro_or_scs_result = escaped_string(r.cells[1].text)
                    case header if header == directorate_header:
                        directorate_result = escaped_string(r.cells[1].text)
                    case _:
                        continue

    return author_name_result, sro_or_scs_result, directorate_result


'''
Summary:
    Extract all the data from a table from a Word Doc into a single Dictionary.
Returns:
    dict:
        key - row index (determined by the Word Doc's row index for the table)
        value - a list of strings, representing the cell values from columns left->right
Params:
    tbl - the table from which to extract the data
'''
def _extract_data_from_doc_table(tbl: Table) -> dict[str, str]:
    tbl_dict: dict = {}

    for r in tbl.rows:
        tbl_dict.setdefault(r._index, [])
        for c in r.cells:
            tbl_dict[r._index].append(escaped_string(c.text))
    
    return tbl_dict


def escaped_string(value: str) -> str:
    return (value.replace("\xa0", " ") # non-breaking space
                .replace("\n", " ") # newline
                .replace("  ", " ") # replace any double spaces, or any created by the \n replace earlier
                .replace("£", "") # easier to strip this than check and replace if not etc. Then calling code can format.
                .strip()
            )
