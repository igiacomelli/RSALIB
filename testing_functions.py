import time

def execTime(func):
    def timeit(*args, **kwargs):
        timeStart = time.time()
        result = func(*args, **kwargs)
        timeEnd = time.time()
        tTime = timeEnd - timeStart
        print("Execution time = ", tTime)
        return result
    return timeit
