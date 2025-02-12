from dataclasses import dataclass
from typing import Any, Type

@dataclass
class Response:    
    status: int = 404
    raw_data: Any = ""
    type: Type = str
    formatted_value: Any = None    

class ResponsePackage:
    def __init__(self, value): 
        self.value = value        
        self.res = Response()   
        # 200 -> Found, 300 -> Type unknown, 404 -> Not found    

    def package_response(self) -> Response:        
        self.value = self.value.strip()
        if self.value == None or (isinstance(self.value, str) and self.value.strip == ""): return self.res
        self.res.status = 300
        self.res.raw_data = self.value
        if isinstance(self.value, str) and self.value.strip().lstrip('-').isdigit():
            self.res.status = 200
            self.res.type = int
            self.res.formatted_value = int(self.value)
        elif isinstance(self.value, str):
            self.res.status = 200            
            self.res.type = str
            self.res.formatted_value = str(self.value)
        else:            
            self.res.type = type(self.value)
            self.res.formatted_value = None        
        return self.res        