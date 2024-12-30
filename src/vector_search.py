import os
from typing import Optional, List
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from schemas import Pet, Filter
import httpx
from functools import lru_cache

# Load environment variables if not in production
if os.getenv("ENV") != "production":
    load_dotenv()


class _CollectionManager:
    """
    Manages the MongoDB collection, ensuring it's initialized only once.
    """

    def __init__(self):
        self._collection = None

    async def get_collection(self):
        """
        Lazily initializes and returns the MongoDB collection.

        Returns:
            motor.motor_asyncio.AsyncIOMotorCollection: The MongoDB collection object.
        """
        if not self._collection:
            client = AsyncIOMotorClient(
                os.getenv("ATLAS_MONGODB_URI"), tlsCAFile=certifi.where()
            )
            db = client[os.getenv("DB")]
            self._collection = db[os.getenv("COLLECTION")]
        return self._collection


# Singleton instance of the CollectionManager
_collection_manager = _CollectionManager()


async def search_pets(query: str, filter_obj: Optional[Filter] = None) -> List[Pet]:
    """
    Perform a vector search for pets based on a query and optional filter asynchronously.

    Args:
        query (str): The search query.
        filter_obj (Optional[Filter]): Optional filter criteria.

    Returns:
        List[Pet]: A list of pets matching the query and filters.
    """
    collection = await _collection_manager.get_collection()
    query_embedding = await get_gpt_embeddings(query)

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
        {
            "$project": {
                "_id": 0,
                "type": 1,
                "name": 1,
                "breed": 1,
                "gender": 1,
                "neutered": 1,
                "birth_year": 1,
                "image": 1,
                "url": 1,
                "text": 1,
            }
        },  # Select fields
    ]

    # Execute the aggregation pipeline asynchronously
    cursor = collection.aggregate(pipeline)
    results = [doc async for doc in cursor]

    return results


async def get_gpt_embeddings(text: str) -> List[float]:
    """
    Generate embeddings asynchronously using OpenAI API.

    Args:
        text (str): The text input for embedding.

    Returns:
        List[float]: The embedding vector.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    url = "https://api.openai.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"model": "text-embedding-ada-002", "input": text},
            headers=headers,
        )
        response.raise_for_status()  # Raise an error for failed requests
        return response.json()["data"][0]["embedding"]
