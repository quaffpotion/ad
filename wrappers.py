from math import sin, cos, exp, log

# Wrap a function so it keeps track of positional boxed arguments
# (Design choice: Our library reserves keyword arguments for function 
# variables that will not be differentiated)
def primitive(func):
    def primitive_func(*args, **kwargs):
        # note: isinstance is not the fastest way to do this, will change
        # to isBox(x) later once all mappings are written
        if any(map(lambda _ : isinstance(_, Box), args)):
            parents = [_ for _ in enumerate(args) if isinstance(_[1], Box)]
            extracted_values = [_.value if isinstance(_, Box) else _ for _ in args]
            value = func(*extracted_values, **kwargs)
            return Box(value, primitive_func, [parent[1] for parent in parents], extracted_values, kwargs, [parent[0] for parent in parents])
        else:
            return func(*args, **kwargs)
    primitive_func.__name__ = func.__name__
    return primitive_func


#Instead of wrapping float.__add__ when creating each boxed float we wrap them all at once and then
#assign them when the object is initialized
type_mappings = {
                    float.__add__: primitive(float.__add__), float.__mul__: primitive(float.__mul__),
                    float.__radd__: primitive(float.__radd__), float.__rmul__: primitive(float.__rmul__),
                    float.__pow__: primitive(float.__pow__), float.__rpow__: primitive(float.__rpow__),
                    float.__sub__: primitive(float.__sub__), float.__rsub__: primitive(float.__rsub__)  
                }
function_deltas = {
                    type_mappings[float.__add__]:{0: lambda x, y: 1.0, 1: lambda x, y: 1.0},
                    type_mappings[float.__radd__]:{0: lambda x, y: 1.0, 1: lambda x, y: 1.0},
                    type_mappings[float.__mul__]:{0: lambda x, y: y, 1: lambda x, y: x},
                    type_mappings[float.__rmul__]:{0: lambda x, y: y, 1: lambda x, y: x},
                    type_mappings[float.__sub__]: {0: lambda x, y: 1.0, 1: lambda x, y: -1.0},
                    type_mappings[float.__rsub__]: {0: lambda x, y: -1.0, 1: lambda x, y: 1.0},
                    type_mappings[float.__pow__]: {0: lambda x, y: y*(x**(y-1)), 1: lambda x, y: (x**y)*log(x)},
                    type_mappings[float.__rpow__]: {0: lambda x, y: (y**x)*log(y), 1: lambda x, y: x*(y**(x-1))},
}


class Box():
    
    def __init__(self, value, func = None, parents = [], args = [], kwargs = {}, parent_argnums = []):
        self.value = value
        self.func = func
        self.parents = parents #Will only keep boxed parents
        self.args = args
        self.kwargs = kwargs
        self.parent_argnums = parent_argnums #Keeps track of which parents go into which arguments so we can fetch derivatives

        # seems you can't assign a function to __add__ here that python will recognize
        # seems to be because python checks the *class* definition for an add function

    def __str__(self): return f'{self.func.__name__} {self.value}' if self.func in function_deltas else f'{self.value}'
    
    def __add__(self, other): return type_mappings[type(self.value).__add__](self, other)
    def __radd__(self, other): return type_mappings[type(self.value).__radd__](self, other)
    def __mul__(self, other): return type_mappings[type(self.value).__mul__](self, other)
    def __rmul__(self, other): return type_mappings[type(self.value).__rmul__](self, other)
    def __sub__(self, other): return type_mappings[type(self.value).__sub__](self, other)
    def __rsub__(self, other): return type_mappings[type(self.value).__rsub__](self, other)
    def __pow__(self, other): return type_mappings[type(self.value).__pow__](self, other)
    def __rpow__(self, other): return type_mappings[type(self.value).__rpow__](self, other)


#Wrap Python math operations
sin = primitive(sin)
cos = primitive(cos)
exp = primitive(exp)


#testing

# print(str(id(None)))

# print(list(map(id, list(type_mappings.values()))))
# print(list(map(id, list(function_deltas.keys()))))
# x = Box(2.0)
# y = Box(2.1)
# z = Box(2.2)

# x + y 
# x + y




