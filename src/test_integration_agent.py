import pytest
from agent import extract_filter_values, vector_query


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
