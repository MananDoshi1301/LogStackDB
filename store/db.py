import os, sys, time

sys.path.insert(0, f'{os.getcwd()}/services')
from store.services.set_manager import SetManager
from store.services.get_manager import GetManager

class LSMStore (SetManager, GetManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)