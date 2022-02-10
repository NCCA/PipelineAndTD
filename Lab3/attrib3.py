#!/usr/bin/env python


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

# This function uses attributes
@static_vars(a=0,b=0)
def static_func():
    print(f"value a={static_func.a} b={static_func.b}")
    static_func.a += 1
    static_func.b += 5


for i in range(0, 10):
    static_func()
