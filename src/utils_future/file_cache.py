import functools
import os
import pickle
import tempfile

from utils import Hash

from utils_future.Log import Log

log = Log('file_cache')


def file_cache(cache_key_data):
    cache_key = str(cache_key_data)
    h = Hash.md5(cache_key)
    cache_file = os.path.join(tempfile.gettempdir(), f'file-cache-{h}.pickle')

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    result = pickle.load(f)
                return result

            result = func(*args, **kwargs)
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            log.debug_temp(f'{cache_file=}')
            return result

        return wrapper

    return decorator
