from collections import defaultdict
from store.services.codec_manager import CodecManager

class CacheManager(CodecManager):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # In memory caching: {key -> (byte offset in a file)}
    self._offset_map = defaultdict(int)

  def set_cache(self, key, val) -> None:
    if key != -1: self._offset_map[key] = val

  def get_cache(self, key: str) -> str | int:
    return self._offset_map[key]