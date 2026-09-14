from docx import Document
from docx.document import Document as doc
from docx.enum.table import WD_ROW_HEIGHT_RULE
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import qn, nsdecls
from docx.oxml.parser import OxmlElement
from docx.oxml.xmlchemy import BaseOxmlElement
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run

import docx.oxml.ns
import docx.opc.constants
import logging

_mhclg_green_hex: str = "#00625E"
_blue_help_box_background_hex: str = "#E4F2FF"
_regular_font_colour_hex: str = "#000000"
_help_box_footer_font_colour_hex: str = "#E8E8E8"
_hyperlink_font_colour_hex: str = "#1D70B8"

bold_font_name: str = "Arial Bold"
regular_font_name: str = "Arial Regular"
italic_font_name: str = "Arial Italic"

logger = logging.getLogger(__name__)

def get_mhclg_green_rgb() -> RGBColor:
    return translate_hex_to_rgb(_mhclg_green_hex)

def get_blue_help_box_background_rgb() -> RGBColor:
    return translate_hex_to_rgb(_blue_help_box_background_hex)

def get_general_font_colour_rgb() -> RGBColor:
    return translate_hex_to_rgb(_regular_font_colour_hex)

def get_help_box_footer_font_colour_rgb() -> RGBColor:
    return translate_hex_to_rgb(_help_box_footer_font_colour_hex)

def translate_hex_to_rgb(hex_colour: str) -> RGBColor:
    return RGBColor(
        int(hex_colour[1:3],16),
        int(hex_colour[3:5],16),
        int(hex_colour[5:7],16)
    )


'''
Summary:
    Wrapper around the Word Document logic.
    
    Because Python-Docx uses proxy classes to handle the typing and what is returned, you can't have 
    objects like Paragraphs and Tables truly exist outside of the method to add_XXX() which returns the object.
    This requires having a doc somewhere which would couple things together.
    BusinessCaseWordDocument is wrapping the logic so as to separate calling code fromm logic as much as possible.
    
    In this way the wrapper is souly responsible for styling/ handling the word document logic,
    and the methods are simply called by whatever needs a document created.
'''
class BusinessCaseWordDocumentWrapper:
    
    def __init__(self):
        self.doc = Document()


    def add_h1_section_header(self, header_text: str):
        p = self.get_basic_paragraph()
        r = p.add_run(header_text)
        r.font.color.rgb = get_mhclg_green_rgb()
        r.font.size = Pt(28)
        r.font.bold = True
        r.font.italic = False
        r.font.name = bold_font_name


    def add_h2_section_header(self, header_text: str):
        p = self.get_basic_paragraph()
        r = p.add_run(header_text)
        r.font.color.rgb = get_mhclg_green_rgb()
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.italic = False
        r.font.name = bold_font_name

    
    def add_paragraph(self, paragraph_content: str):
        p = self.get_basic_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        r = p.add_run(paragraph_content)
        self.style_paragraph_run(r)


    '''
    Summary:
        Get a paragraph with some basic styling applied that
        applies to all paragraphs.
    '''
    def get_basic_paragraph(self):
        p = self.doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        return p


    '''
    Summary:
        Style a paragraph run.
        Separate styling here so multiple methods can call it.
        This is generic styling for a regualr paragraph, i.e not a header.
    '''
    def style_paragraph_run(self, r: Run):
        r.font.color.rgb = get_general_font_colour_rgb()
        r.font.size = Pt(12)
        r.font.bold = False
        r.font.italic = False
        r.font.name = regular_font_name


    def add_bullet_point_list(self, items: list[str]):
        for item in items:
            p = self.doc.add_paragraph()
            p.style="List Bullet"
            p.paragraph_format.left_indent = Pt(45)
            r = p.add_run(item)
            r.font.color.rgb = get_general_font_colour_rgb()
            r.font.size = Pt(12)
            r.font.bold = False
            r.font.italic = False
            r.font.name = regular_font_name


    '''
    Summary:
        Add fixed text (e.g. text from triage we know about) to the document.
    '''
    def add_fixed_text(self, fixed_text: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        r = p.add_run(fixed_text)
        r.font.color.rgb = get_general_font_colour_rgb()
        r.font.size = Pt(12)
        r.font.italic = True
        r.font.bold = False
        r.font.name = italic_font_name


    '''
    Summary:
        Add a Hyperlink to the Word Document.
        Because there is no explicit hyperlink class in Docx we have to make it using the Oxml.
        Take in a string that represents the URL, the entire text to display, and the text that should become the hyperlink.
    '''
    def add_hyperlink(self, url: str, text: str, text_to_replace_with_hyperlink):
        if (text_to_replace_with_hyperlink not in text):
            logger.warning(f"Text to replace with a hyperlink does not exist in the paragraph string. Paragraph: {text}, Text to replace: {text_to_replace_with_hyperlink}")
            self.add_paragraph(text)
            return
        
        p = self.doc.add_paragraph()

        part = p.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

        # Create the w:hyperlink tag and add needed values
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(docx.oxml.ns.qn('r:id'), r_id, )

        # Create a w:r element
        new_run = OxmlElement('w:r')

        new_run.append(self.get_hyperlink_run_style())
        new_run.text = text_to_replace_with_hyperlink
       
        sections = text.split(text_to_replace_with_hyperlink, 1)
        start = sections[0]
        end = sections[1]
        
        hyperlink.append(new_run)

        # join the text before the hyperlink, then the hyperlink, then the text after it
        start_run = p.add_run(f"{start.strip()} ")
        self.style_paragraph_run(start_run)

        p._p.append(hyperlink)

        end_run = p.add_run(f" {end.strip()}")
        self.style_paragraph_run(end_run)


    '''
    Summary:
        Style the hyperlink. Only the hyperlink itself, not the surrounding text.
    '''
    def get_hyperlink_run_style(self) -> BaseOxmlElement:
        # Create a new w:rPr element - Run Properties
        rPr = OxmlElement('w:rPr')
        
        color = OxmlElement('w:color')
        color.set(docx.oxml.ns.qn('w:val'), _hyperlink_font_colour_hex)
        rPr.append(color)

        underline = OxmlElement('w:u')
        underline.set(docx.oxml.ns.qn('w:val'), 'single')
        rPr.append(underline)

        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), bold_font_name)
        rFonts.set(qn('w:hAnsi'), bold_font_name)
        rPr.append(rFonts)

        # add Bold text
        b = OxmlElement('w:b')
        rPr.append(b)

        return rPr


    '''
    Summary:
        Add a help box to the Word Document.
    Params:
        contents: List of strings that the help box should contain.
                The first element will be in bold.
    '''
    def add_help_box(self, contents):
        help_box = _HelpBox(contents)
        help_box.add_help_box(self.doc)


    '''
    Summary:
        Add an input box to the Word Document.
    Params:
        word_limit: optional, guidance on how many words to use in the Input box.
    '''
    def add_input_box(self, word_limit: int = -1):
        input_box = _InputBox(word_limit)
        input_box.add_input_box(self.doc)


    '''
    Summary;
        Save the document to the location required.
        If errors are encountered return a failing result.
    '''
    def save_document(self, save_location: str) -> bool:
        try:
            self.doc.save(save_location)
            return True
        except Exception as ex:
            logger.error(f"Error while saving Business Case template. Message: {ex.__str__}")
            return False


'''
Summary:
    Wraps the creation of the help box logic so as to not bloat the word doc wrapper.
    Creates the help box, formatting etc., and adds it to the Document
'''
class _HelpBox:

    def __init__(self, contents: list[str]):
        self.contents = contents


    '''
    Summary:
        Add a help box the the document passed through.
    '''
    def add_help_box(self, doc: doc):
        p: Paragraph | None = None
        tbl = doc.add_table(1, 1)
        self.set_cell_background(tbl._cells[0])

        for idx, content in enumerate(self.contents):
            # the add_table() method above adds a paragraph by default, so use this
            # so the styling works with the indents and spaces as we use the default
            if idx == 0:
                p = tbl._cells[0].paragraphs[0]
            else:
                p = tbl._cells[0].add_paragraph()

            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
            p.paragraph_format.left_indent = Pt(8)
            p.paragraph_format.right_indent = Pt(8)
                            
            r = p.add_run()
            r.font.color.rgb = get_general_font_colour_rgb()
            r.font.size = Pt(12)

            if idx == 0:
                p.paragraph_format.space_before = Pt(8)
                r.font.bold = True
                r.font.name = bold_font_name
                r.add_text(f"➡️ {content}")
            else:
                r.font.bold = False
                r.font.name = regular_font_name
                r.add_text(content)

        # after the loop set the spacing for the last paragraph
        if p is not None:
            p.paragraph_format.space_after = Pt(8)


    '''Summary:
        Set the background to the blue colour we need for help boxes
    '''
    def set_cell_background(self, cell: _Cell):
        shading_elm_xml = f'<w:shd {nsdecls("w")} w:fill="{_blue_help_box_background_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_elm_xml))

'''
Summary:
    Wraps the creation of the input box logic so as to not bloat the word doc wrapper.
    Creates the input box, styling, and footer, and adds it to the Document
'''
class _InputBox:

    _footer_string: str = "Word count guideline: {} words"
    _table_width: Cm = Cm(16.30)


    def __init__(self, word_limit: int = -1):
        self.word_limit = word_limit


    '''
    Summary:
        Addds an input box to the Word Document
    '''
    def add_input_box(self, doc: doc):
        tbl = doc.add_table(1, 1)
        box = tbl.rows[0]

        tbl._cells[0].width = self._table_width
        tbl.style = "Table Grid" # adds gridlines (in this case, a border) to the table
        box_paragraph = tbl._cells[0].paragraphs[0]
        self.set_box_formatting(box_paragraph)

        box.height = Cm(2.55)
        box.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST

        box_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

        # add a footer to the input box with the word limit
        if self.word_limit != -1:
            tbl_footer = doc.add_paragraph()
            tbl_footer.paragraph_format.space_before = 0

            r = tbl_footer.add_run(self._footer_string.format(self.word_limit))
            r.font.color.rgb = get_general_font_colour_rgb()
            r.font.size = Pt(12)
            r.font.bold = False
            r.font.italic = False
            r.font.name = regular_font_name


    '''
    Summary:
        Set some default formatting on the input box.
        Because we are using the default paragraph that exists when creating a table,
        we need to set this here via Oxml. If we add a paragraph through add_paragraph()
        this formatting won't be applied and the user will use the default styling in Word.
    '''
    def set_box_formatting(self, p: Paragraph):
        pPr = p._p.get_or_add_pPr()

        # Get or create paragraph-level run properties (<w:rPr>)
        rPr = pPr.find(qn('w:rPr'))
        if rPr is None:
            rPr = OxmlElement('w:rPr')
            pPr.append(rPr)
            
        # Set the font name
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), regular_font_name)
        rFonts.set(qn('w:hAnsi'), regular_font_name)
        rPr.append(rFonts)

        # Set the deafult font colour
        color = OxmlElement('w:color')
        color.set(docx.oxml.ns.qn('w:val'), regular_font_name)
        rPr.append(color)

        # Set the font size (Word measures this in half-points, so 12pt = 24)
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), "24")
        rPr.append(sz)
