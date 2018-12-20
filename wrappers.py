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
    return primitive_func

class Box():

    #Instead of wrapping float.__add__ when creating each boxed float we wrap them all at once and then
    #assign them when the object is initialized
    type_mappings = {
                    float.__add__: primitive(float.__add__), float.__mul__: primitive(float.__mul__),
                    float.__radd__: primitive(float.__radd__), float.__rmul__: primitive(float.__rmul__),
                    }
    
    def __init__(self, value, func = None, parents = [], args = [], kwargs = {}, parent_argnums = []):
        self.value = value
        self.func = func
        self.parents = parents #Will only keep boxed parents
        self.args = args
        self.kwargs = kwargs
        self.parent_argnums = parent_argnums #Keeps track of which parents go into which arguments so we can fetch derivatives

        #seems you can't assign a function to __add__ here that python will recognize

    def __str__(self): return self.value.__str__()
        
    def __add__(self, other): return self.type_mappings[type(self.value).__add__](self, other)
    def __radd__(self, other): return self.type_mappings[type(self.value).__radd__](self, other)
    def __mul__(self, other): return self.type_mappings[type(self.value).__mul__](self, other)
    def __rmul__(self, other): return self.type_mappings[type(self.value).__rmul__](self, other)
