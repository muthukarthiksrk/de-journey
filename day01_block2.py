import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def calculate_average(numbers: list) -> float:
    try:
        if not numbers:
            raise ValueError("List is empty")
        avg = sum(numbers) / len(numbers)
        logging.info(f"Average calculated: {avg}")
        return avg
    except ValueError as e:
        logging.error(f"Error: {e}")
        return 0.0

def safe_divide(a, b) -> float:
    try:
        if b == 0:
            raise ZeroDivisionError("b is zero!")
        div = a / b
        logging.info(f"Safe division calculated: {div}")
        return div
    except ZeroDivisionError as e:
        logging.error(f"safe_divide() Error: {e}")
        return 0.0

print(calculate_average([10, 20, 30, 40]))
print(calculate_average([]))
print(safe_divide(10, 2))
print(safe_divide(10, 0))