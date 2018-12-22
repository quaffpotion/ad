from wrappers import function_deltas, type_mappings
from collections import defaultdict

# Takes a graph (in the form of a box computed from a function) and computes
# the change w.r.t. the leaf nodes

#Here we assume our graph has a single forward leaf and a single backward
#leaf
def backwardpass(end_box):
    
    # outgrades = defaultdict(lambda: 0, end_box = 1.0)
    # does not work as expected so we use outgrads[end_box]=1.0 below
    outgrads = defaultdict(lambda: 0)
    outgrads[end_box]=1.0
    for current in toposort(end_box):

        # 1: seems to be an issue with using <dictionary>.get(current) w/ a <defaultdict>
        # 2: fixed by using outgrads[current]
        # 3: after fixing initialization (can't use defaultdict( ... a=1)) now <defdict>.get(...) works
        # 4: opting for original dictionary syntax
        outgrad = outgrads[current]
        func, args, kwargs, argnums = current.func, current.args, current.kwargs, current.parent_argnums
        for argnum, parent in zip(argnums, current.parents):
            delta_func = function_deltas[func][argnum]
            parent_grad = outgrad * delta_func(*args, **kwargs)
            outgrads[parent] = outgrads[parent] + parent_grad
    return outgrad

#From Autodidact

#note: end_node != toposort(end_node) as far as object id's are concerned 
# can't key dictionary off them b/c yield ==> it returns a generator
# >>> def f(x):
# ...     yield x
# ...
# >>> x = 5.0
# >>> id(x)
# 4559893128
# >>> id(f(x))
# 4566907016
def toposort(end_node):
    child_counts = {}
    stack = [end_node]
    while stack:
        node = stack.pop()
        if node in child_counts:
            child_counts[node] += 1
        else:
            child_counts[node] = 1
            stack.extend(node.parents)

    childless_nodes = [end_node]
    while childless_nodes:
        node = childless_nodes.pop()
        yield node
        for parent in node.parents:
            if child_counts[parent] == 1:
                childless_nodes.append(parent)
            else:
                child_counts[parent] -= 1




