import os
from typing import Optional, List, cast
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from schemas import Pet, Filter
import httpx
from openai import AsyncOpenAI

# Load environment variables if not in production
if os.getenv("ENV") != "production":
    load_dotenv()


class PetVectorSearch:
    """
    Handles vector search for pets using MongoDB and GPT embeddings.
    """

    def __init__(self):
        self._collection = None
        self._vector_search_index = os.getenv("VECTOR_SEARCH_INDEX_NAME")
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        self._db_uri = os.getenv("ATLAS_MONGODB_URI")
        self._db_name = os.getenv("DB")
        self._collection_name = os.getenv("COLLECTION")
        self._openai_client = AsyncOpenAI(api_key=self._openai_api_key)

    async def _get_collection(self):
        """
        Lazily initializes and returns the MongoDB collection.
        """
        if not self._collection:
            client = AsyncIOMotorClient(self._db_uri, tlsCAFile=certifi.where())
            db = client[self._db_name]
            self._collection = db[self._collection_name]
        return self._collection

    async def _get_gpt_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings asynchronously using OpenAI API.

        Args:
            text (str): The text input for embedding.

        Returns:
            List[float]: The embedding vector.
        """
        response = await self._openai_client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )

        return response.data[0].embedding

    async def search_pets(
        self, query: str, filter_obj: Optional[Filter] = None
    ) -> List[Pet]:
        """
        Perform a vector search for pets based on a query and optional filter asynchronously.

        Args:
            query (str): The search query.
            filter_obj (Optional[Filter]): Optional filter criteria.

        Returns:
            List[Pet]: A list of pets matching the query and filters.
        """
        collection = await self._get_collection()
        query_embedding = await self._get_gpt_embeddings(query)

        # Build the vector search pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "index": self._vector_search_index,
                    "numCandidates": 10,
                    "limit": 3,
                    "filter": filter_obj if filter_obj else {},
                }
            },
            {"$set": {"score": {"$meta": "vectorSearchScore"}}},
            {
                "$project": {
                    "id": {"$toString": "$_id"},
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
            },
        ]

        # Execute the aggregation pipeline asynchronously
        cursor = collection.aggregate(pipeline)
        results = [cast(Pet, doc) async for doc in cursor]

        return results
