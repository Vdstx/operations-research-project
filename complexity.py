import time

def measure_algorithm_time(algorithm, *args, **kwargs):
    start = time.perf_counter()
    result = algorithm(*args, **kwargs)
    end = time.perf_counter()
    return end - start, result
