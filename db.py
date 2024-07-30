#### Some topics to cover
# Finding out the size of the file (Compaction and Partitioning)
# DONE: 2M scans taking a very long time: (File Size: )
# DONE: Finding offset if key not in cache and setting in the cache
# DONE: Writing to a file: Saving after writing
# DONE: Reading from a file
# DONE: Finding out the offset of inside a file (Indexing)
# ADVANCED: Exploring locks and concurrency for writing inside of a file

##### Stepwise approach
# use cache to store incoming queries. If timeout write to a file
# For writes gathering info like file and content to store in a queue. On backend running threads to store those one by one
# DONE: set to a file and get from file (Read Write O(n), but still locks on reads writes)
# ADVANCED:
# --------------------------------------------------------

import os, sys, time

sys.path.insert(0, f'{os.getcwd()}/services')
from set_manager import SetManager
from get_manager import GetManager

class LSMStore (SetManager, GetManager):
    ...

if __name__ == "__main__":
    path = "./data/"
    filename = "db_testdata_2m.txt"
    # filename = "db_mainfile.txt"
    file_path = os.path.join(path, filename)
    cursor = LSMStore(file_path)
    start = time.time()
    print(cursor.get("nice"))
    print(cursor.get("nice"))
    end = time.time()
    print("Search Time: {}ms".format((end - start) * 10 ** 3))
