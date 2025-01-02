from typing_extensions import TypedDict, List


class Pet(TypedDict):
    name: str
    type: str
    breed: str
    gender: str
    neutered: bool
    birth_year: int
    image: str
    url: str
    text: str


class Filter(TypedDict, total=False):
    type: str


class IndividualPetAnswer(TypedDict):
    pet_id: str
    answer: str


class ResponseType(TypedDict):
    general_answer: str
    individual_pet_answers: List[IndividualPetAnswer]
