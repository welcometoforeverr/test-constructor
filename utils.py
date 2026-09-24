"""Input helpers with exception handling."""


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Read an integer and repeat the request on invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")
