from apps.word_doc_services.parsing_document import *

from apps.triage.models import (
    BusinessCaseResponseSummary,
    BusinessCaseResponseBlock
)

from django.test import Client
import pytest
from apps.accounts.models import User
import time
from django.urls import reverse

from apps.word_doc_services.parsing_document import _SectionContent

@pytest.fixture
def client(db):
    user = User.objects.create_user(
        username="test.user@example.gov.uk", email="test.user@example.gov.uk"
    )
    client = Client()
    client.force_login(user)
    session = client.session
    session["id_token_claims"] = {"exp": time.time() + 3600}
    session.save()
    return client


@pytest.fixture
def started_session(client):
    """Start a triage session and return the client with session set up."""
    client.get(reverse("triage:start"))
    return client


def test_section_content_new():
    # Arrange
    sect_content = _SectionContent()

    # Act
    # Assert
    assert sect_content is not None
    assert sect_content.section_header == ""
    assert sect_content.content == [] 


def test_adding_data_to_section_content():
    # Arrange
    header:str = "TestHeader"
    content_string = "TestContent"
    content_dict = {}
    sect_content = _SectionContent()

    # Act
    sect_content.add_section_header(header)
    sect_content.add_item_to_content(content_string)
    sect_content.add_item_to_content(content_dict)

    # Assert
    assert sect_content.content[0] == content_string
    assert isinstance(sect_content.content[1], dict)
    assert sect_content.section_header == header


def test_summary_data_can_be_submitted_to_summary_model(client):
    # Arrange
    response_summary: BusinessCaseResponseSummary | None = None

    test_summary_data: dict = {}
    test_author = "TestAuthor"
    test_sro_scs_author = "SroScsAuthor"
    test_directorate = "TestDirectorate"
    test_summary_text = "Some Summary Test"
    test_whole_life_cost = "£404"

    empty_document_data: list[_SectionContent] = []

    test_summary_data[summary_key_author] = test_author
    test_summary_data[summary_key_sro_scs] = test_sro_scs_author
    test_summary_data[summary_key_directorate] = test_directorate
    test_summary_data[summary_key_text] = test_summary_text
    test_summary_data[summary_key_whole_life_cost] = test_whole_life_cost

    # Act
    summary_result, document_result = submit_data_to_models(test_summary_data, empty_document_data)

    response_summary = BusinessCaseResponseSummary.objects.first()

    # Assert
    assert summary_result == True
    assert document_result == True
    assert response_summary is not None, "result_object is None"
    assert response_summary.author == test_author, "Incorrect Author"
    assert response_summary.sro_scs == test_sro_scs_author, "Incorrect SRO/ SCS Author"
    assert response_summary.directorate == test_directorate, "Incorrect Directorate"
    assert response_summary.summary_text == test_summary_text, "Incorrect Summary Text"
    assert response_summary.whole_of_life_cost == test_whole_life_cost, "Incorrect Whole Life Cost"


def test_response_data_can_be_submitted_to_response_model(client):
    # Arrange
    empty_summary_data: dict = {}
    test_header: str = "TestHeader"
    string_content: str = "Content"
    dict_key: str = "key"
    dict_value: str = "val"
    dict_content: dict[str, str] = {}
    dict_content[dict_key] = dict_value

    section_content : _SectionContent = _SectionContent()
    document_data: list[_SectionContent] = []

    section_content.add_section_header(test_header)
    section_content.add_item_to_content(string_content)
    section_content.add_item_to_content(dict_content)
    document_data.append(section_content)

    # Act
    summary_result, document_result = submit_data_to_models(empty_summary_data, document_data)

    response_block_str = BusinessCaseResponseBlock.objects.get(block_type="Paragraph")
    response_block_table = BusinessCaseResponseBlock.objects.get(block_type="Table")

    block_data_str = response_block_str.block_data.decode('utf-8')

    block_two_data_json = response_block_table.block_data.decode('utf-8')
    block_two_result = json.loads(block_two_data_json)

    # Assert
    assert summary_result == True
    assert document_result == True
    assert block_data_str is not None
    assert block_two_result is not None

    assert isinstance(block_two_result, dict)
    assert block_two_result[dict_key] == dict_value
    assert block_data_str == string_content

