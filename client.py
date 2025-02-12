import os, time
from store.db import LSMStore
from store.services.response_manager import Response

if __name__ == "__main__":
    
    filename = "db_testdata_2m.txt"        
    cursor = LSMStore(filename=filename)    
    start = time.time()
    res: Response = cursor.get("nice")
    print(res.status, res.type)
    
    end = time.time()
    print("Search Time: {}ms".format((end - start) * 10 ** 3))