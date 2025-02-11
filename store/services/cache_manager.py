
from store.services.base_store import BaseStore
class CacheManager(BaseStore):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def set_cache(self, key, val) -> None:
    if key != -1: self._offset_map[key] = val

  def get_cache(self, key: str) -> str | int:
    return self._offset_map[key]