from r0 import *

ast1 = P(ADD(NUM(10), NUM(10)))
ast2 = P(NEG(ADD(READ(), NUM(10))))
ast3 = P(ADD(READ(), NEG(READ())))

def test_r0_interp():
	assert ast1.interp() == 20

def test_r0_read():
	global RAND
	assert ast2.interp(True) == -(RAND+10)
	assert ast2.interp(True) == -(RAND+9)
	assert ast2.interp(True) == -(RAND+8)
	assert ast2.interp(True) == -(RAND+7)
	assert ast3.interp(True) == 1
	assert ast2.interp(True) == -(RAND+4)

def test_r0_interp():
	for n in range(12):
		assert gen(exp_r0, n).interp() == 2**n
		gen(rand_r0, n).interp(True)

def test_r0_opt():
	assert ast1.opt().interp() == P(NUM(20)).interp()
	assert ast2.opt().interp(True, True) == P(NEG(ADD(READ(), NUM(10)))).interp(True, True)
	assert ast3.opt().interp(True, True) == P(ADD(READ(), NEG(READ()))).interp(True, True)

	assert gen(exp_r0, 1).opt().interp()== P(NUM(2)).interp()
	assert gen(exp_r0, 2).opt().interp() == P(NUM(4)).interp()
	assert gen(exp_r0, 3).opt().interp() == P(NUM(8)).interp()

	assert P(ADD(NUM(7), ADD(READ(), NUM(8)))).opt().interp(True, True) == P(ADD(NUM(15), READ())).interp(True, True)
	assert P(ADD(ADD(READ(), NUM(8)), NUM(7))).opt().interp(True, True) == P(ADD(READ(), NUM(15))).interp(True, True)
	assert \
		P(
			ADD(
				ADD(ADD(NUM(1), NUM(2)), READ()),
				ADD(READ(), ADD(NUM(7), NUM(3)))
			)
		).opt().interp(True, True) == P(ADD(NUM(13), ADD(READ(), READ()))).interp(True, True)

def test_r0_interp_opt():
	for n in range(12):
		astn = gen(rand_r0_no_read, n)
		assert astn.interp() == astn.opt().interp()
		rand_ast = gen(rand_r0, n)
		assert rand_ast.interp(True, True) == rand_ast.opt().interp(True, True)
		assert gen(exp_r0, n).opt().interp() == 2**n