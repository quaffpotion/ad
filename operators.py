from wrappers import Box
from tracer import backwardpass

def grad(f, argnum=0):
    def gradfunc(*args, **kwargs):
        boxed_args = box_args(*args, argnum=argnum)
        return backwardpass(f(*boxed_args, **kwargs))
    return gradfunc

def box_args(*args, argnum=0):
        args_list = list(args)
        args_list[argnum] = Box(args_list[argnum])
        boxed_args = tuple(args_list)
        return boxed_args