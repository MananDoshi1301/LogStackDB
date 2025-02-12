import pytest
from store.db import LSMStore

@pytest.fixture
def cursor():
    return LSMStore()

# Test setting values
def test_set_value():
    # Create new file, 
    # set, 
    # read 
    # delete file
    ...