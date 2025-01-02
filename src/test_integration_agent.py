import pytest
from agent import extract_filter_values, vector_query, compose_answer
from langchain_core.messages import HumanMessage
from mock_data import (
    MOCK_PETS,
    MOCK_MESSAGES,
    MOCK_MESSAGES_FOR_PROBLEMATIC_DOGS,
    MOCK_PROBLEMATIC_DOGS,
)


# Parametrized test using pytest
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message,expected_filter",
    [
        ("Ich suche nach einer katze.", {"filter": {"type": "katze"}}),
        ("Ich möchte einen hund adoptieren.", {"filter": {"type": "hund"}}),
        ("Gibt es Haustiere zu adoptieren?", {"filter": {"type": None}}),
        ("Adoption für Hunde?", {"filter": {"type": "hund"}}),
    ],
)
async def test_extract_filter_values(message, expected_filter):
    state = {"translated_message": message}
    result = await extract_filter_values(state)
    assert result == expected_filter


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message, filter, expected_type",
    [
        (
            "Ich suche nach einer katze die sehr zurückhaltend ist.",
            {"type": "katze"},
            "katze",
        ),
    ],
)
async def test_search_pets(message, filter, expected_type):
    state = {"translated_message": message, "filter": filter}
    result = await vector_query(state)
    # print(result)
    assert result
    assert result["pets"][0]["type"] == expected_type


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lang",
    [
        "de",
        "en",
    ],
)
async def test_compose_answer(lang):
    state = {
        "lang": lang,
        "messages": MOCK_MESSAGES[lang],
        "pets": MOCK_PETS,
    }
    answer = await compose_answer(state)
    print("===")
    print(answer)
    print("===")
    assert answer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lang",
    ["de", "en"],
)
async def test_compose_answer_for_list(lang):
    state = {
        "lang": lang,
        "messages": MOCK_MESSAGES_FOR_PROBLEMATIC_DOGS[lang],
        "pets": MOCK_PROBLEMATIC_DOGS,
    }
    answer = await compose_answer(state)
    print("===")
    print(answer)
    print("===")
    assert answer
