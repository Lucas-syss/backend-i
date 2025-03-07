import logging
from time import perf_counter
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def audit(func):
    def wrapper(*args, **kwargs):
        timerStart = perf_counter()
        result = func(*args, **kwargs)
        logger.info(f"Arguments: {args} Result: {result}")
        timerStop = perf_counter()  
        logger.info(f"Elapsed time: {timerStop}, {timerStart}")
        runningTime = timerStop - timerStart
        logger.info(f"Running time: {runningTime}")
    return wrapper

@audit
def multiply(a, b):
    return a * b

if __name__ == "__main__":
    multiply(2, 2)