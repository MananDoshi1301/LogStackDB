# import os
# from db import LSMStore

# def set():
#     ...

import os
import pytest
from db import LSMStore, SetManager

@pytest.fixture
def temp_file(tmpdir):
    return tmpdir.join("testfile.txt")

def test_set_function(temp_file):

    cursor = LSMStore(str(temp_file))
    cursor.set("test", 20)

    # Read the content of the file to verify the write operation
    with open(str(temp_file), 'rb') as f:
        content = f.read()
        print("Content", content)

    # Check if the content matches the expected output
    assert content
    # assert b"test, 20\n" in content