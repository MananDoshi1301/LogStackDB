##### Testing approach
# Setting and getting key
# Return None if key doesn't exist
# Unit tests on setting file, get and set

import os
import unittest
from db import LSMStore

class TestStore(unittest.TestCase):
    
    def setUp(self):
        self._filename = os.environ.get('TEST_DB_FILENAME', 'db_testdata.txt')
        self._db_cursor = LSMStore(self._filename)                
        
    def test_set(self):
        pass
        
    def test_get(self):
        pass
        
        
if __name__ == "__main__":
    unittest.main()