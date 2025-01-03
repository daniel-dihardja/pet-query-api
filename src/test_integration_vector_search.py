import pytest
from vector_search import PetVectorSearch


@pytest.mark.asyncio
async def test_pet_vector_search():
    """
    Test the async PetVectorSearch.search_pets function with a query and filter.
    """
    # Arrange
    searcher = PetVectorSearch()
    query = "sehr zurückhaltend"
    filter_obj = {"type": "katze"}

    # Act
    res = await searcher.search_pets(query, filter_obj)

    # Assert
    assert res, "The result should not be empty"  # Ensure the result is not empty
    assert res[0]["type"] == "katze", "The first result should have type 'katze'"

    # Debugging output (optional, for development purposes)
    print("***")
    print(res[0])
