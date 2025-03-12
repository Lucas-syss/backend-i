from typer import Typer
import logging
from rich import print
from time import perf_counter
import sys

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

app = Typer()

@app.command()
def main(number: int):
    timeStart = perf_counter()
    print(number * number)
    timeEnd = perf_counter()
    logging.info(f"Execution time: {timeEnd-timeStart}")

if __name__ == "__main__":
    app()