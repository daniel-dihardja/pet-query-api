import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi
from schemas import Pet, Filter
from openai import OpenAI

# Load environment variables if not in production
if os.getenv("ENV") != "production":
    load_dotenv()


def get_collection():
    """
    Initialize and return the MongoDB collection for vector search.

    Returns:
        pymongo.collection.Collection: The MongoDB collection object.
    """
    client = MongoClient(os.getenv("ATLAS_MONGODB_URI"), tlsCAFile=certifi.where())
    db = client[os.getenv("DB")]
    return db[os.getenv("COLLECTION")]


# Initialize the collection at the module level
collection = get_collection()
openai_client = OpenAI()


def search_pets(query: str, filter_obj: Optional[Filter] = None) -> List[Pet]:
    """
    Perform a vector search for pets based on a query and optional filter.

    Args:
        query (str): The search query.
        filter_obj (Optional[Filter]): Optional filter criteria.

    Returns:
        List[Pet]: A list of pets matching the query and filters.
    """

    query_embedding = get_gpt_embeddings(query)

    # Build the vector search pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "index": os.getenv("VECTOR_SEARCH_INDEX_NAME"),
                "numCandidates": 10,  # Number of candidates to consider
                "limit": 1,  # Set the required "limit" parameter
                "filter": filter_obj if filter_obj else {},  # Add optional filters
            }
        },
        {"$set": {"score": {"$meta": "vectorSearchScore"}}},  # Attach similarity scores
        {"$project": get_project_stage(Pet)},  # Select fields
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(pipeline)

    # Convert results to Pet objects
    return map_to_pet(list(results))


def get_project_stage(schema):
    """
    Generate a $project stage for MongoDB based on the attributes of the schema.

    Args:
        schema: The schema class (e.g., Pet).

    Returns:
        dict: A dictionary representing the $project stage.
    """
    return {field: 1 for field in schema.__annotations__.keys() if field != "_id"}


def get_gpt_embeddings(texts):
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002", input=texts
    )
    return response.data[0].embedding


def map_to_pet(res: List[dict]) -> List[Pet]:
    """
    Map the result of the vector search to a list of Pet objects.

    Args:
        res (List[dict]): The result list from the vector search.

    Returns:
        List[Pet]: A list of Pet objects.
    """
    return [Pet(**doc) for doc in res]
