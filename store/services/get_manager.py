from collections import deque
from store.services.cache_manager import CacheManager

class GetManager(CacheManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, key: int | str) -> int | str | None:
        ### Get the key
        value = None
        def return_value():
            nonlocal value
            return int(value) if (value and value.isdigit()) else (value.strip() if value else value)

        def get_offset(position: int, buffersize: int, key: str | int) -> int:
            read_size = buffersize
            self._file.seek(position)

            # Iterate through text
            buffer_read = self._file.read(2 * read_size)
            key_bytes = str(key).encode('utf-8')
            offset = buffer_read.rfind(key_bytes)
            if offset != -1:
                return (position + offset)
            else:
                print("Key not found in buffer")
                return -1

        if key in self._offset_map:
            print("Key in cache")

            # Reading offset from the cache
            offset = self._offset_map[key]

            # Moving pointer to that position in the file
            self._file.seek(offset)

            # Reading the line in that file
            line_bytes = self._file.readline()
            line = line_bytes.decode(self._byte_encode_decode_format)
            k, v = line.split(',')
            if k == key: value = v
            return return_value()

        else:
            # Optional: Check if key exists using bloom filter
            # Efficiently reading file backwards and searching in linear time
            # Caching location offset

            # Move the cursor to the end of the file
            self._file.seek(0, 2)
            position = self._file.tell()
            size = position // 20
            buffer_size = size + size % 2
            queue = deque()
            res = []
            set_offsets_for = []

            while position > 0:
                read_size = min(buffer_size, position)
                position -= read_size
                # print(position)
                self._file.seek(position)

                # Iterate through text
                buffer_read = self._file.read(read_size)
                lines = buffer_read.split(b'\n')

                # Handle the first (possibly incomplete) line
                if queue:
                    back_element = queue.popleft()
                    front_element = lines.pop()
                    text = front_element + back_element
                    res.append(text.decode(self._byte_encode_decode_format))

                if not queue and lines: queue.append(lines[0])

                # search for key: if found break or else clear buffer
                for idx in range(len(lines) - 1, 0, -1):
                    res_text = lines[idx].decode(self._byte_encode_decode_format)
                    if res_text != '': res.append(res_text)

                    for string in res:
                        k, v = string.split(',')
                        # Can add concurrency
                        if k not in self._offset_map: set_offsets_for.append((position, key))

                        if k == key:
                            value = v
                            offset_val = get_offset(position, buffer_size, key)
                            self.set_cache(key, offset_val)
                            return return_value()

                    res.clear()

            if queue:
                res_text = queue.popleft().decode(self._byte_encode_decode_format)
            k, v = res_text.split(',')
            if k == key:
                value = v
                self._offset_map[key] = 0
                return return_value()

        return None
