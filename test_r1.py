from r1 import *

ast0 = P(LET(VAR('x'), ADD(NUM(12), NUM(20)), ADD(NUM(10), VAR('x'))))
ast1 = P(LET(VAR('x'), NUM(32), ADD(LET(VAR('x'), NUM(10), VAR('x')), VAR('x'))))
ast2 = P(LET(VAR('x'), NUM(10), LET(VAR('y'), VAR('x'), ADD(VAR('x'), NEG(VAR('y'))))))

rand_ast = \
	P(
		LET(
			VAR('t'),
			NEG(NEG(NEG(READ()))), 
			ADD(
				ADD(
					ADD(VAR('t'), VAR('t')), 
					NEG(VAR('t'))
				),
				LET(
					VAR('H'),
					NEG(VAR('t')),
					ADD(VAR('t'), VAR('t'))
				)
			)
		)
	)

rand_ast_opt = \
	P(
		LET(
			VAR('t'),
			NEG(READ()), 
			ADD(
				ADD(
					ADD(VAR('t'), VAR('t')), 
					NEG(VAR('t'))
				),
				ADD(VAR('t'), VAR('t'))
			)
		)
	)

def test_r1_interp():
	assert ast0.interp() == 42
	assert ast0.interp() == ast0.opt().interp()
	assert ast1.interp() == 42
	assert ast1.interp() == ast1.opt().interp()
	assert ast2.interp() == 0
	assert ast2.interp() == ast2.opt().interp()

def test_r1_opt():
	assert rand_ast.interp(True, True) == rand_ast.opt().interp(True, True)
	assert rand_ast.opt().interp(True, True) == rand_ast_opt.interp(True, True)

def test_rand_r1():
	for n in range(16):
		ast = gen(rand_r1, n)
		ast.interp(True, True) == ast.opt().interp(True, True)
		ast1 = gen(rand_r1_no_read, n)
		ast1.interp(True, True) == ast1.opt().interp(True, True)