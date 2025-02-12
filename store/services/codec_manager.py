from store.services.base_store import BaseStore

class CodecManager(BaseStore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._byte_encode_decode_format = 'utf-8'

    def encode(self, text: str) -> bytes:
        return text.encode(self._byte_encode_decode_format)        
    
    def decode(self, text_bytes: bytes) -> str:
        return text_bytes.decode(self._byte_encode_decode_format)        