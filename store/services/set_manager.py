from store.services.cache_manager import CacheManager

class SetManager(CacheManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, key: str, value: int | str) -> None:
        ### Append key, value to the end of the file

        # Moving cursor to the end of the file
        self._file.seek(0, 2)

        # Getting the current offset
        offset = self._file.tell()

        # Form the text to store and append to file
        text = "{}, {}\n".format(key, value)
        bytes_text = text.encode(self._byte_encode_decode_format)
        self._file.write(bytes_text)

        # Store the offset in the cache
        self._offset_map[key] = offset
