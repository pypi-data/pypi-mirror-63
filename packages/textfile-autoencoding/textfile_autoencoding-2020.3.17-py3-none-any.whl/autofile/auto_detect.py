import functools
import io
import os
import sys

from chardet.universaldetector import UniversalDetector


@functools.lru_cache(maxsize=io.DEFAULT_BUFFER_SIZE)
def file_encoding(filepath):
    default_encoding = sys.getdefaultencoding()

    if not (os.path.exists(filepath) and os.path.isfile(filepath)):
        return default_encoding

    detector = UniversalDetector()
    with io.open(filepath, 'rb') as file:
        while True:
            data = file.read(io.DEFAULT_BUFFER_SIZE)
            if data:
                detector.feed(data)
                if detector.done:
                    break
            else:
                break
    detector.close()

    return detector.result.get('encoding', default_encoding).lower()
