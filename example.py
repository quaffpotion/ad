#All the user will need to import:
from operators import grad
#import wrapped_numpy as np #to implement

#imports for testing
from wrappers import Box



def f(x,y):
    return x*y

print(grad(f)(2.,3.))

x = Box(5.0)
y = Box(6.0)

print((x+y).parents)
print((x+5.0).parents)
print((5.0+x).parents)


print(Box(6.9))