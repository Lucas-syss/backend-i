def factorial(n):
    assert not isinstance(n, (str, bool, float, dict, list,
    tuple)), f"{type(n)} is not acceptable"
    if n < 0:
        raise ValueError("Factorial of negative numbers is not allowed.")

    if n == 0:
        return 1
    return n * factorial(n - 1)
