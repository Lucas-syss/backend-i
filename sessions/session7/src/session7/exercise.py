from contextlib import contextmanager
import logging 
import sys
from time import perf_counter

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

@contextmanager
def open_file(filename, mode):
    timeStart = perf_counter()
    print(f"Opening file {filename}")
    f = open(filename, mode)
    try:
        yield f
    finally:
        print(f"Closing file {filename}")
        f.close()
        timeEnd = perf_counter()
        logging.info(f"Execution time: {timeEnd-timeStart}")

if __name__ == "__main__":
    with open_file("bla.txt", "a") as f:
        f.write("\nAppending with context manager using @contextmanager."* 10)