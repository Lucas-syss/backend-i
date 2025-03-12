from typer import Typer
import logging
from rich import print
import sys

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

app = Typer()

@app.command(help="Add two numbers together.")
def addition(number1: int, number2: int):
    """Perform addition of two integers."""
    if number1 < 0 or number2 < 0:
        print("Error: Negative numbers are not allowed in addition.")
    else:
        print(number1 + number2)

@app.command(help="Subtract second number from the first.")
def subtraction(number1: int, number2: int):
    """Perform subtraction of two integers."""
    print(number1 - number2)

@app.command(help="Divide the first number by the second.")
def division(number1: int, number2: int):
    """Perform division of two integers."""
    if number2 == 0:
        print("Error: Cannot divide by zero.")
    else:
        print(number1 / number2)

@app.command(help="Multiply two numbers together.")
def multiplication(number1: int, number2: int):
    """Perform multiplication of two integers."""
    print(number1 * number2)

if __name__ == "__main__":
    app()
