import numpy as np

# Wrap a function so it keeps track of boxed arguments
def primitive(func):
    def primitive_func(*args, **kwargs):
        if any(map(lambda _ : isinstance(_, Box), args)):
            parents = [_ for _ in args if isinstance(_, Box)]
            extracted_values = [_.value if isinstance(_, Box) else _ for _ in args]
            value = func(*extracted_values, **kwargs)
            return Box(value, primitive_func, parents)
        else:
            return func(*args, **kwargs)
    return primitive_func


# Transforms a function f: floats -> float into a function 
# f_wrapped: wrapped_floats -> wrapped_float provided the operations 
# in f (e.g. +, *, etc.) have analogs for wrapped_floats
def function_of_floats_wrapper(f):
    def wrapped(*args, **kwargs):
        wrapped_args = [wrapped_float(x) for x in args]
        wrapped_kwargs = {key: wrapped_float(value) for key, value in kwargs.items()}
        return f(*wrapped_args, **wrapped_kwargs)
    return wrapped




class Box():

    #Instead of wrapping float.__add__ when creating each boxed float we wrap them all at once and then
    #assign them when the object is initialized
    type_mappings = {
                    float.__add__: primitive(float.__add__), float.__mul__: primitive(float.__mul__),
                    float.__radd__: primitive(float.__radd__), float.__rmul__: primitive(float.__rmul__),
                    }
    
    def __init__(self, value, func = None, parents = []):
        self.value = value
        self.func = func
        self.parents = parents
        #seems you can't assign a function to __add__ here that python will recognize

    def __str__(self): return self.value.__str__()
        
    def __add__(self, other): return self.type_mappings[type(self.value).__add__](self, other)
    def __radd__(self, other): return self.type_mappings[type(self.value).__radd__](self, other)
    def __mul__(self, other): return self.type_mappings[type(self.value).__mul__](self, other)
    def __rmul__(self, other): return self.type_mappings[type(self.value).__rmul__](self, other)


class wrapped_float(float):
    def __new__(cls, value):
        return float.__new__(cls, value)

    def __add__(self, other):
        print("Adding!")
        return wrapped_float(float.__add__(self, other))

    def __mul__(self, other):
        print("Multiplying!")
        return wrapped_float(float.__mul__(self, other))
    

x = Box(5.0)
y = Box(6.0)

print(type(x+y))
print(type(x+5.0))
print(type(5.0+x))

def f(x,y,z):
    return x*2+y*3

print(Box(6.9))









# This will play the same role for np.array as float.
# This is the class the user is expected to use most often.
# Note, subclassing here requires fewer zany circumlocutions 
# than the wrapped_float class above.
class Tensor(np.ndarray):

    
    pass

# Only intended for the tutorial, generally you will be using arrays
# and will be composing classes instead

# The following demonstrates that you can subclass from float in python
# and modify the __add__ method, and add attributes. Note the __new__
# method. 

# class test_wrapped_float(float):
#     #need __new__ because float is immutable
#     #if you want class variables, you must pass them into __new__
#     # and also to __init__
#     def __new__(cls, value, extra="default"):
#         return float.__new__(cls, value)

#     def __init__(self, value, extra="default"):
#         super().__init__()
#         self.extra = extra

#     def __add__(self, other): 
#         print("Adding!")

#         # how can you make this work without `float`?
#         # super causes many issues - also super is called
#         # differently depending on which version of python
#         # is installed
#         # super(), super(<class_name>), super(<class_name>, self), etc.
#         # do not work
#         return test_wrapped_float(float.__add__(self, other))

# #Test Code:
# f = test_wrapped_float(1.0, "extra")
# g = test_wrapped_float(2.0)
# print((f+g).extra)



@function_of_floats_wrapper
def f(x,y):
    z = x*y
    #a = 5 + z # todo: Here seems to use __rmul__ of int class
    a = z + 5
    return a


