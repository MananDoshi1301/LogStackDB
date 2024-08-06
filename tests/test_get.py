import os
from db import LSMStore

def test_get():
    path = "./data/"
    filename = "db_testdata_2m.txt"
    file_path = os.path.join(path, filename)
    cursor = LSMStore(file_path)
    assert(cursor.get("nice") == '1')