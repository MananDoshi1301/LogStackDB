#### Some topics to cover
# DEBUG: 2M scans taking a very long time: (File Size: )
# TODO: Offset to a file
# Finding out the size of the file (Compaction and Partitioning)
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

import os
import time
from collections import defaultdict, deque
class LSMStore:

    def __init__(self, filename: str):
        # set file permission: 'a+'
        self._file_opening_permission = 'a+b'
        self._byte_encode_decode_format = 'utf-8'

        # key: (byte offset in a file)
        self._offset_map = defaultdict(int)

        # Opening file and using it constantly to store data
        try:
            self._file = open(r"{}".format(filename), self._file_opening_permission)

        except Exception as e:
            print("Some error:", e)


    def __del__(self):
        # Closing fil
        try:
            self._file.close()
            # print("File closed sucessfully")
        except Exception as e:
            print("Error in closing file:", e)

    def set_cache(self, key, val) -> None:
        if key != -1: self._offset_map[key] = val

    def get_cache(self, key: str) -> str | int:
        return self._offset_map[key]

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

    # Read is O(n) -> Assumption is key exists (Bloom filter to check if key exists in database)
    # Read is O(1) with offset indexing
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


if __name__ == "__main__":
    path = "./data/"
    filename = "db_testdata_2m.txt"
    file_path = os.path.join(path, filename)
    cursor = LSMStore(file_path)

    start = time.time()
    val = cursor.get("nice")
    new_time = time.time()
    val = cursor.get("nice")
    end = time.time()

    print("Key: nice, Value:", val)
    print("Searching Time:", (new_time - start) * (10 ** 3), "ms")
    print("Hash Time:", (end - new_time) * (10 ** 3), "ms")