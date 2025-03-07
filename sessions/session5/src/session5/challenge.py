import sys
import logging
from time import perf_counter
import functools

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def decor1(func):
    def wrapper1(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper1

@decor1
def checkUser(user):
    usersList = ["Jorge", "Jose", "Joao"]
    if user in usersList:
        logger.info(f"Welcome {user}")
    else:
        logger.info(f"Access denied")

def cache_factorial(func):
    @functools.lru_cache(maxsize=None)
    def wrapper(n):
        start_time = perf_counter()
        result_nocache = func(n)
        end_time = perf_counter()
        time_nocache = end_time - start_time

        start_time = perf_counter()
        result_cache = func(n)
        end_time = perf_counter()
        time_cache = end_time - start_time
        
        logger.info(f"WO Caching: Result = {result_nocache}, Time = {time_nocache} seconds")
        logger.info(f"Caching: Result = {result_cache}, Time = {time_cache} seconds\n")
        
        return result_cache
    return wrapper

@cache_factorial
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    checkUser("Jorge")
    factorial(5)