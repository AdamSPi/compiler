from r0 import *

ast1 = P(EX_ADD(EX_NUM(10), EX_NUM(10)))
ast1.print()

ast2 = P(EX_NEG(EX_ADD(EX_READ(), EX_NUM(10))))
ast2.print()

ast1.interp()
ast2.interp()