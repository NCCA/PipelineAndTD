#!/usr/bin/env python


# This function uses attributes
def static_func():
    if not hasattr(static_func, "a"):
        static_func.a = 0  # it doesn't exist yet, so initialize it
    if not hasattr(static_func, "b"):
        static_func.b = 0  # it doesn't exist yet, so initialize it

    print(f"value a={static_func.a} b={static_func.b}")
    static_func.a += 1
    static_func.b += 5


for i in range(0, 10):
    static_func()
