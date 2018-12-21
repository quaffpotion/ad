#All the user will need to import:
from operators import grad
import wrapped_numpy as np

#imports for testing
from wrappers import Box, sin
from operators import box_args
from tracer import toposort

def f(x,y,z):
    return x*y, x*z

def g(x, n):
    for _ in range(0,n):
        x = sin(x * 2)
    return x

for _ in toposort(g(Box(2.0),3)):
    print(_)

for _ in f(Box(2.0), Box(3.0), Box(4.0)):
    for __ in toposort(_):
        print(__)
        

# print(grad(f)(2.,3.))

# x = Box(5.0)
# y = Box(6.0)

# print((x+y).parents)
# print((x+5.0).parents)
# print((5.0+x).parents)


# print(Box(6.9))