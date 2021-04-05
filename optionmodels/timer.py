import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        for k, v in kwargs.items():
            if k == 'timing' and v == True:
                print('{}.{} : {} milliseconds'.format(
                    func.__module__, func.__name__, round((
                        end - start)*1e3, 2)))
        return r
    return wrapper

