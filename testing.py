def deriv(f):
    def f_deriv(x, **kwargs):
        h = 0.0000001
        return (f(x+h, **kwargs)-f(x, **kwargs))/h
    return f_deriv

def make_unary(f, args, argnum=0):
    def unary_f(x, **kwargs):
        return f(*[args[i] if i != argnum else x for i in range(0, len(args))], **kwargs)
    return unary_f
        
def numerical_grad_operator(f, argnum=0):
    def numerical_grad_f(*args, **kwargs):
        return deriv(make_unary(f,args,argnum))(args[argnum], **kwargs)
    return numerical_grad_f
