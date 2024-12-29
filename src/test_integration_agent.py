import pytest
from agent import extract_filter_values


async def call_extract_filter_values(message: str) -> dict[str, dict[str, str | None]]:
    state = {"translated_message": message}
    res = await extract_filter_values(state)
    return res


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
    result = await call_extract_filter_values(message)
    assert result == expected_filter
