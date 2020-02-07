from r0 import *

ast1 = P(EX_ADD(EX_NUM(10), EX_NUM(10)))

ast2 = P(EX_NEG(EX_ADD(EX_READ(), EX_NUM(10))))

def test_interp():
	assert ast1.interp(True) == 20

def test_read():
	assert ast2.interp(True) == -52
	assert ast2.interp(True) == -51
	assert ast2.interp(True) == -50
	assert ast2.interp(True) == -49

ast2.interp()