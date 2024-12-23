import functools
import time
import psutil
import os

def measure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        mem_after = process.memory_info().rss
        print(f"INFO: Memory before: {mem_before} bytes")
        print(f"INFO: Memory after: {mem_after} bytes")
        print(f"INFO: Memory consumed: {mem_after - mem_before} bytes")
        print(f"INFO: Time elapsed: {end - start} seconds")
        return result
    return wrapper