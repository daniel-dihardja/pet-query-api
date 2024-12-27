import os
from typing_extensions import TypedDict, Optional, List
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
import certifi


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


class Filter(TypedDict):
    type: str


if os.getenv("ENV") != "production":
    load_dotenv()

client = MongoClient(os.getenv("ATLAS_MONGODB_URI"), tlsCAFile=certifi.where())
collection = client[os.getenv("DB")][os.getenv("COLLECTION")]

vectorStore = MongoDBAtlasVectorSearch(
    collection,
    OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
    index_name=os.getenv("VECTOR_SEARCH_INDEX_NAME"),
)


def search_pets(query: str, filter_obj: Optional[dict] = None) -> List[Pet]:
    """
    Search for pets based on a query and optional filter.

    Args:
        query (str): The search query.
        filter_obj (Optional[dict]): Optional filter criteria.

    Returns:
        List[Pet]: A list of pets matching the query and filters.
    """
    if filter_obj is None:
        # If no filter is provided, exclude pre_filter from the call
        res = vectorStore.similarity_search(query, include_scores=True)
    else:
        # Use the filter when provided
        res = vectorStore.similarity_search(
            query, include_scores=True, pre_filter=filter_obj
        )

    return map_to_pet(res)


def map_to_pet(res: List[dict]) -> List[Pet]:
    """
    Map the result of the vector search to a list of Pet objects.

    Args:
        res (List[dict]): The result list from the vector search.

    Returns:
        List[Pet]: A list of Pet objects including page_content but excluding _id.
    """
    return [
        Pet(**r.metadata, text=r.page_content)  # Access attributes correctly
        for r in res
    ]


query = "sehr zurückhaltend"
res = search_pets(query, {"type": "katze"})
print("***")
print(res[0])
