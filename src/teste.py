from functools import cache
from time import sleep

@cache
def delay(x):
    sleep(x)
    return 'Feito'

print(delay(5), delay(5))