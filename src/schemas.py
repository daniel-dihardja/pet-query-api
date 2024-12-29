from typing_extensions import TypedDict


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
