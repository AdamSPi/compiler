from r0 import *

ast1 = P(EX_ADD(EX_NUM(10), EX_NUM(10)))
ast2 = P(EX_NEG(EX_ADD(EX_READ(), EX_NUM(10))))
ast3 = P(EX_ADD(EX_READ(), EX_NEG(EX_READ())))

def test_interp():
	assert ast1.interp() == 20

def test_read():
	assert ast2.interp(True) == -52
	assert ast2.interp(True) == -51
	assert ast2.interp(True) == -50
	assert ast2.interp(True) == -49
	assert ast3.interp(True) == 1
	assert ast2.interp(True) == -46

def test_gen():
	for n in range(12):
		assert gen(exp_r0, n).interp() == 2**n
		gen(rand_r0, n).interp(True)

# test_gen()
# print(abs(EX_READ.debug_counter - 50))