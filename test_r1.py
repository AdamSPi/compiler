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

rand_ast2 = \
	P(
		LET(
			VAR('z'),
			NEG(
				ADD(
					NUM(246),
					NUM(137)
				)
			),
			LET( # z -> -383
				VAR('z'),
				ADD(
					VAR('z'),
					READ()
				),
				NEG(VAR('z')) # z -> ADD(-383, READ())
			)
		)
	)

rand_ast2_opt = \
	P(
		LET(
			VAR('z'),
			ADD(
				NUM(-383),
				READ()
			),
			NEG(VAR('z'))
		)
	)


rand_ast3 = \
	P(
		LET(
			VAR('F'),
			LET(
				VAR('r'),
				LET(
					VAR('u'),
					LET(
						VAR('S'),
						READ(),
						READ()
					),
					NEG(NUM(-209))
				),
				LET(
					VAR('E'),
					LET(
						VAR('v'),
						VAR('r'),
						READ()
					),
					NEG(VAR('E'))
				)
			),
			LET(
				VAR('x'),
				NEG(NEG(VAR('F'))),
				ADD(
					LET(
						VAR('F'),
						READ(),
						VAR('x')
					),
					NEG(NUM(146))
				)
			)
		)
	)

rand_ast3_opt = \
	P(
		LET(
			VAR('F'),
			LET(
				VAR('E'),
				READ(),
				NEG(VAR('E'))
			),
			LET(
				VAR('x'),
				VAR('F'),
				ADD(
					VAR('x'),
					NUM(-146)
				)
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
	assert rand_ast2.interp(True, True) == rand_ast2.opt().interp(True, True)
	assert rand_ast2.opt().interp(True, True) == rand_ast2_opt.interp(True, True)
	assert rand_ast3.interp(True, inp=1) == rand_ast3.opt().interp(True, inp=1)
	assert rand_ast3.opt().interp(True, inp=1) == rand_ast3_opt.interp(True, inp=1)

def test_rand_r1():
	for n in range(16):
		ast = gen(rand_r1, n)
		# need to take same input every read in case some reads are dropped by opt
		assert ast.interp(True, inp=1) == ast.opt().interp(True, inp=1)
		ast1 = gen(rand_r1_no_read, n)
		assert ast1.interp() == ast1.opt().interp()