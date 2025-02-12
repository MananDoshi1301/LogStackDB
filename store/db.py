import os, sys, time

sys.path.insert(0, f'{os.getcwd()}/services')
from store.services.set_manager import SetManager
from store.services.get_manager import GetManager

class LSMStore (SetManager, GetManager):
    def __init__(self, *args, filename = None, **kwargs):
        self._init_args = args
        self._init_kwargs = kwargs
        self.file_initialized = False
        
        if filename:
            self.init(filename)

    def init(self, filename: str):
        if self.file_initialized: 
            print("The LSMStore has already been initialized!")
            return
        self._init_kwargs["filename"] = filename
        super().__init__(*self._init_args, **self._init_kwargs)
        self.file_initialized = True        