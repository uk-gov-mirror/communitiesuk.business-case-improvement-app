
from docx.oxml.ns import qn
import docx.oxml.ns
from docx.shared import Cm, RGBColor
from docx.text.paragraph import Paragraph
from docx.oxml.parser import OxmlElement
import docx

from apps.word_doc_services.common_resources import(
    translate_hex_to_rgb,
    _regular_font_name
)

'''
This file is for generic variables, values and methods used in Table creation, and not
used anywhere else.
Anywhere we need other values such as text colour, this will be imported from the more generic common_resources.py
file which contains values common to the entire doc. This file is exclusively for things necessary to create Tables.
'''

_blue_help_box_background_hex: str = "#E4F2FF"
_help_box_footer_font_colour_hex: str = "#E8E8E8"

max_table_width: Cm = Cm(15.9)


def get_blue_help_box_background_rgb() -> RGBColor:
    return translate_hex_to_rgb(_blue_help_box_background_hex)


def get_help_box_footer_font_colour_rgb() -> RGBColor:
    return translate_hex_to_rgb(_help_box_footer_font_colour_hex)


'''
Summary:
    Set some default formatting on the cell.
    Because we are using the default paragraph that exists when creating a table we need
    to set this here via Oxml. If we add a paragraph through add_paragraph() this formatting
    won't be applied and the user will use the default styling in Word, which will be wrong.
'''
def set_default_paragraph_formatting(p: Paragraph):
    pPr = p._p.get_or_add_pPr()

    # Get or create paragraph-level run properties (<w:rPr>)
    rPr = pPr.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        pPr.append(rPr)
        
    # Set the font name
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), _regular_font_name)
    rFonts.set(qn('w:hAnsi'), _regular_font_name)
    rPr.append(rFonts)

    # Set the deafult font colour
    color = OxmlElement('w:color')
    color.set(docx.oxml.ns.qn('w:val'), _regular_font_name)
    rPr.append(color)

    # Set the font size (Word measures this in half-points, so 12pt = 24)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), "24")
    rPr.append(sz)
