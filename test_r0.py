from r0 import *

ast1 = P(ADD(NUM(10), NUM(10)))
ast2 = P(NEG(ADD(READ(), NUM(10))))
ast3 = P(ADD(READ(), NEG(READ())))

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
# print(abs(READ.debug_counter - 50))

def test_optimize():
	assert ast1.optimize().show() == P(NUM(20)).show()
	assert ast2.optimize().show() == P(NEG(ADD(READ(), NUM(10)))).show()
	assert ast3.optimize().show() == P(ADD(READ(), NEG(READ()))).show()

	assert gen(exp_r0, 1).optimize().show() == P(NUM(2)).show()
	assert gen(exp_r0, 2).optimize().show() == P(NUM(4)).show()
	assert gen(exp_r0, 3).optimize().show() == P(NUM(8)).show()

# ast4 = gen(rand_r0, 5)
# ast4.show()
# print()
# ast4.optimize().show()