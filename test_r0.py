from r0 import *

ast1 = P(EX_ADD(EX_NUM(10), EX_NUM(10)))
ast1.print()

ast2 = P(EX_NEG(EX_ADD(EX_READ(), EX_NUM(10))))
ast2.print()

assert ast1.interp() == 20
assert ast2.interp() == -33
assert ast2.interp() == -20
assert ast2.interp() == -11
assert ast2.interp() == 1

print("All tests passed! ✓")