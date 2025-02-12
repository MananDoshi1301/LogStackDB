import pytest
from store.db import LSMStore
from store.services.response_manager import Response


@pytest.fixture
def cursor():
    return LSMStore()

@pytest.fixture
def filename():
    return "db_testdata.txt"

# Search for bear, nice, foo, bar, banana
def test_get_keywords(cursor, filename):
    keys = ["bear", "nice", "foo", "bar", "banana"]
    cursor.init(filename=filename)    
    for key in keys:
        response: Response = cursor.get(key)
        assert response.type == int
        assert response.status == 200
        assert type(response.formatted_value) == int

