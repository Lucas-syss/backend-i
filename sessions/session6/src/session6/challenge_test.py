from pytest import raises
from challenge import factorial

def test_all_type_cases():
    with raises(TypeError, match=f""):
        factorial(-1)

def test_factorial():
    assert factorial(5) == 120
