from r0 import *

ast1 = P(ADD(NUM(10), NUM(10)))
ast2 = P(NEG(ADD(READ(), NUM(10))))
ast3 = P(ADD(READ(), NEG(READ())))

def test_interp():
	assert ast1.interp() == 20

def test_read():
	global RAND
	assert ast2.interp(True) == -(RAND+10)
	assert ast2.interp(True) == -(RAND+9)
	assert ast2.interp(True) == -(RAND+8)
	assert ast2.interp(True) == -(RAND+7)
	assert ast3.interp(True) == 1
	assert ast2.interp(True) == -(RAND+4)

def test_interp():
	for n in range(12):
		assert gen(exp_r0, n).interp() == 2**n
		gen(rand_r0, n).interp(True)

def test_optimize():
	assert ast1.optimize() == P(NUM(20))
	assert ast2.optimize() == P(NEG(ADD(READ(), NUM(10))))
	assert ast3.optimize() == P(ADD(READ(), NEG(READ())))

	assert gen(exp_r0, 1).optimize()== P(NUM(2))
	assert gen(exp_r0, 2).optimize() == P(NUM(4))
	assert gen(exp_r0, 3).optimize() == P(NUM(8))

	assert P(ADD(NUM(7), ADD(READ(), NUM(8)))).optimize() == P(ADD(NUM(15), READ()))
	assert P(ADD(ADD(READ(), NUM(8)), NUM(7))).optimize() == P(ADD(READ(), NUM(15)))

def test_interp_opt():
	for n in range(10):
		astn = gen(rand_r0_no_read, n)
		assert astn.interp() == astn.optimize().interp()
		rand_ast = gen(rand_r0, n)
		assert rand_ast.interp(True, True) == rand_ast.optimize().interp(True, True)
		assert gen(exp_r0, n).optimize().interp() == 2**n


# ast4 = gen(rand_r0, 5)
# ast4.show()
# print()
# ast4.optimize().show()