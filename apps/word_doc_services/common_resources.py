from docx.shared import RGBColor
from datetime import date, datetime

'''
This file is for generic variables, values and methods used throughout the Word Doc
creation logic. This file contains things to be used in Document creation in both
Paragraphs and Tables and these should be imported from here.
If it appears that any aren't being used (e.g due to being faded in an IDE) it's probably
because of the preceding _ to note 'do not change'. Check it is not being imnported elsewhere.
'''

_regular_font_name: str = "Arial Regular"
_bold_font_name: str = "Arial Bold"
_italic_font_name: str = "Arial Italic"

_hyperlink_font_colour_hex: str = "#1D70B8"
_regular_font_colour_hex: str = "#000000"
_mhclg_green_hex: str = "#00625E"

def get_general_font_colour_rgb() -> RGBColor:
    return translate_hex_to_rgb(_regular_font_colour_hex)

def get_mhclg_green_rgb() -> RGBColor:
    return translate_hex_to_rgb(_mhclg_green_hex)


def translate_hex_to_rgb(hex_colour: str) -> RGBColor:
    return RGBColor(
        int(hex_colour[1:3],16),
        int(hex_colour[3:5],16),
        int(hex_colour[5:7],16)
)

def get_financial_year(fy_offset: int = 0) -> int:
    current_date: date = datetime.now().date()
    financial_year_start_for_current_year: date = date(current_date.year, 4, 1)
    financial_year_end_for_current_year: date = date(current_date.year + 1, 3, 31)

    # curent date in between this years financial year and next. So greater than April, less than March next year 
    if financial_year_start_for_current_year <= current_date <= financial_year_end_for_current_year:
        return current_date.year + fy_offset

    # means we are in Jan, Feb, or March so need to use the previous year's FY, so -1
    if current_date < financial_year_start_for_current_year:
        return current_date.year - 1 + fy_offset

    # default to current year
    return current_date.year
