import os, time
from store import db

if __name__ == "__main__":
    
    filename = "db_testdata_2m.txt"        
    cursor = db.LSMStore(filename=filename)    
    start = time.time()
    print(cursor.get("nice"))
    print(cursor.get("nice"))
    end = time.time()
    print("Search Time: {}ms".format((end - start) * 10 ** 3))