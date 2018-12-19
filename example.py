#All the user will need to import:
from operators import grad
#import wrapped_numpy as np #to implement

#imports for testing
from wrappers import Box

x = Box(5.0)
y = Box(6.0)

print((x+y).parents)
print((x+5.0).parents)
print((5.0+x).parents)

def f(x,y,z):
    return x*2+y*3

print(Box(6.9))
