from collections import defaultdict

class BaseStore:
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
