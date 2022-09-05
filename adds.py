from time import time


def print_time_passed(func):
    def wrapper(*args):
        time_init = time()
        func(*args)  # function
        time_after = time()
        time_delta = time_after - time_init
        print(func.__name__, time_delta)

    return wrapper
