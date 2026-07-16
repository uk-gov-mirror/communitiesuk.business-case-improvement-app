from docx.text.paragraph import Paragraph
from docx.shared import Pt

aptos_font_name: str = "Aptos"
aptos_bold_font_name: str = "Aptos Bold"

def add_text_with_default_formatting(p: Paragraph, content: str):
    r = p.add_run(content)
    r.font.size = Pt(12)
    r.font.bold = False
    r.font.name = aptos_font_name

