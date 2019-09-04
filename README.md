# ad
Further minimalist version of https://github.com/mattjj/autodidact.

## Ordered Todo:
- [x] Implement tracer.backwardpass for scalar-valued function taking gradient w.r.t one variable
- [ ] Implement tracer.backwardpass for arbitrary graph (given forward leaf values, compute backward leaf values)
- [ ] Wrap basic numpy functions

## Time independent Todo:
- [ ] Implement isBox via type mappings intead of via python builtin isinstance for a speedup
