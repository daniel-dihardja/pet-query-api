import pytest
from agent import extract_filter_values, vector_query, compose_answer
from langchain_core.messages import HumanMessage


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
    "lang, messages, pets",
    [
        (
            "de",
            [
                HumanMessage(
                    content="Ich suche einen Kater, der eher zurückhaltend ist und sich vielleicht erst an Menschen gewöhnen muss. Es wäre ideal, wenn er später Freigang haben könnte, da ich in einer ruhigen Gegend wohne. Ich habe Geduld und würde ihm die Zeit geben, die er braucht, um Vertrauen aufzubauen."
                )
            ],
            [
                {
                    "name": "Hr. Möckel",
                    "type": "katze",
                    "breed": "Hauskatze",
                    "gender": "male",
                    "neutered": 0,
                    "birth_year": 2020,
                    "image": "https://www.tierheim-leipzig.de/wp-content/uploads/2024/10/20241001_152929.jpg",
                    "url": "https://www.tierheim-leipzig.de/Project/hr-moeckel/",
                    "text": "Herr Möckel kam als Fundtier ins Tierheim. Wir vermuten, daß der ehemals unkastrierte Kater sich früher auch der Straße durch schlagen musste. Dem Menschen gegenüber verhält er sich noch sehr zurückhaltend, aktuell lässt er sich noch nicht anfassen. Wir hoffen aber, dass er noch Vertrauen fassen wird. Herr Möckel hält sich bei uns vermehrt im Außenbereich auf, sodass wir für ihn ein Zuhause mit späteren Freigang suchen. Wenn Sie Interesse an einer unserer Katzen haben, kontaktieren Sie uns bevorzugt per E-Mail. Schildern Sie uns in der Mail, wie die Katze/die Katzen bei Ihnen leben wird/werden und senden Sie uns eine Telefonnummer zu. Es wird sich dann ein*e TierpflegerIn bei Ihnen melden. Info: Tierbeschreibungen basieren auf Beobachtungen im Tierheim oder auf Informationen Dritter und stellen keine zugesicherten Eigenschaften dar.",
                }
            ],
        ),
    ],
)
async def test_compose_answer(lang, messages, pets):
    state = {"lang": lang, "messages": messages, "pets": pets}
    answer = await compose_answer(state)
    # print(answer)
    assert answer
