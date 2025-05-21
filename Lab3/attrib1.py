#!/usr/bin/env -S uv run --script
# This function uses attributes
def static_func():
    print(f"value a={static_func.a} b={static_func.b}")
    static_func.a += 1
    static_func.b += 5


# Need to initialize first
static_func.a = 0
static_func.b = 0

for i in range(0, 10):
    static_func()
