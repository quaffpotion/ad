# Takes a graph (in the form of a box computed from a function) and computes
# the change w.r.t. the leaf nodes

#Here we assume our graph has a single forward leaf and a single backward
#leaf
def backwardpass(last_box):
    raise NotImplementedError
    
    # last_box.value = 1.0
    # queue = [last_box]
    # while current:
    #     current = queue.pop()
    #     for parent in current.parents
    #         parent.value = current.value * parent.func.delta

#From Autodidact
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




