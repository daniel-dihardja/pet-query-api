from vector_search import search_pets
import pytest


def test_search_pets():
    """
    Test the search_pets function with a query and filter.
    """
    # Arrange
    query = "sehr zurückhaltend"
    filter_obj = {"type": "katze"}

    # Act
    res = search_pets(query, filter_obj)

    # Assert
    assert res, "The result should not be empty"  # Ensure the result is not empty
    assert res[0]["type"] == "katze", "The first result should have type 'katze'"

    # Debugging output (optional, for development purposes)
    print("***")
    print(res[0])
