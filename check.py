import tests.risk_scorer.test_rules as m
import inspect
fns = [name for name, obj in inspect.getmembers(m) if inspect.isfunction(obj) and name.startswith('test_')]
print(f'Found {len(fns)} test functions:')
for f in fns: print(' ', f)
