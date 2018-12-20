from wrappers import Box
from tracer import backwardpass

def grad(f, argnum=0):
    def gradfunc(*args, **kwargs):
        args_list = list(args)
        args_list[argnum] = Box(args_list[argnum])
        boxed_args = tuple(args_list)
        return backwardpass(f(*boxed_args, **kwargs))
    return gradfunc



