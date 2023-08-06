import io
from contextlib import contextmanager

from autofile import auto_detect


@contextmanager
def open(file, mode='rt', buffering=-1, encoding=None, errors=None,
         newline=None, closefd=True, opener=None):

    if 'b' in mode:
        raise TypeError("Opening files in binary mode, is not supported")

    if not encoding:
        encoding = auto_detect.file_encoding(file)
    
    with io.open(file, mode=mode, buffering=buffering, encoding=encoding, errors=errors,
                 newline=newline, closefd=closefd, opener=opener) as file_object:
        yield file_object
