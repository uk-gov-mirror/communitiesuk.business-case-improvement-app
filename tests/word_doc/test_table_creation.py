from apps.word_doc_services.word_document_wrapper import BusinessCaseWordDocumentWrapper
from apps.word_doc_services.word_tables.table_definitions import TABLE_DEFINITION

def test_create_table_method_adds_table_footer():
    # arrange
    word_count = 100
    test_doc = BusinessCaseWordDocumentWrapper()
    
    # act
    test_doc.add_input_box(word_count)
    test_para = test_doc.doc.paragraphs[0]
    paragraph_count = len(test_doc.doc.paragraphs) + 1
    
    # assert
    assert paragraph_count == 3
    assert test_para.text == f"Word count guideline: {word_count} words"


def test_create_table_method_can_add_a_table_for_each_table_definition():
    # arrange
    test_doc = BusinessCaseWordDocumentWrapper()
    tbl_count: int = 0

    # act 
    for tbl_def in TABLE_DEFINITION:
        print(tbl_def)
        tbl_count +=1
        test_doc.add_generic_table(tbl_def)

    # assert
    assert tbl_count == len(test_doc.doc.tables)


def test_checkbox_creation():
    # arrange
    test_doc = BusinessCaseWordDocumentWrapper()
    options: list[str] = ["Opt 1", "Opt 2"]

    # act 
    test_doc.add_checkbox(options)

    # assert
    assert len(test_doc.doc.tables) == 1
    assert test_doc.doc.tables[0].cell(0, 1).paragraphs[0].text == options[0]
    assert test_doc.doc.tables[0].cell(1, 1).paragraphs[0].text == options[1]


def test_helbox_creation():
    # arrange
    test_doc = BusinessCaseWordDocumentWrapper()
    help_strings: list[str] = ["Help Text title", "Further details"]

    # act 
    test_doc.add_help_box(help_strings)

    # assert
    assert len(test_doc.doc.tables) == 1
