import functools
import hashlib
import os
import pickle
import tempfile


def file_cache(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        s = func.__name__ + str(args) + str(kwargs)
        h = hashlib.md5(s.encode()).hexdigest()

        cache_file = os.path.join(
            tempfile.gettempdir(), f'cache-{h}.pickle'
        )

        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                result = pickle.load(f)
            return result

        result = func(*args, **kwargs)
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
        return result

    return wrapper


