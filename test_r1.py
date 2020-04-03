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
			ADD(
				VAR('F'),
				NUM(-146)
			)
		)
	)

rand_ast4 = \
	P(
		LET(
			VAR('I'),
			NEG(
				ADD(
					NEG(
						NUM(-36)
					),
					LET(
						VAR('H'),
						READ(),
						VAR('H')
					)
				)
			),
			LET(
				VAR('c'),
				NEG(NEG(VAR('I'))),
				LET(
					VAR('I'),
					NEG(READ()),
					ADD(
						VAR('c'),
						VAR('I')
					)
				)
			)
		)
	)

rand_ast5 = \
	P(
		NEG(
			LET(
				VAR('w'),
				NEG(
					LET(
						VAR('r'),
						ADD(
							LET(
								VAR('I'),
								READ(),
								READ()
							),
							ADD(
								NUM(-221), 
								NUM(110)
							)
						),
						LET(
							VAR('l'),
							NEG(NUM(194)),
							LET(
								VAR('G'),
								NUM(-116),
								VAR('G')
							)
						)
					)
				),
				ADD(
					LET(
						VAR('J'),
						NEG(NEG(VAR('w'))),
						LET(
							VAR('w'),
							ADD(
								VAR('J'),
								VAR('w')
							),
							ADD(
								VAR('w'),
								VAR('J')
							)
						)
					),
					NEG(NEG(NEG(NUM(-101))))
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
	assert rand_ast4.opt().interp(True, inp=1) == rand_ast4.interp(True, inp=1)
	assert rand_ast5.opt().interp(True) == rand_ast5.interp(True)

def test_rand_r1():
	for n in range(16):
		ast = gen(rand_r1, n)
		# need to take same input every read in case some reads are dropped by opt
		assert ast.interp(True, inp=1) == ast.opt().interp(True, inp=1)
		ast1 = gen(rand_r1_no_read, n)
		assert ast1.interp() == ast1.opt().interp()

def test_unique_ify():
	assert rand_ast.interp(True, True) == rand_ast.uniqueify().interp(True, True)
	assert rand_ast2.interp(True, True) == rand_ast2.uniqueify().interp(True, True)
	assert rand_ast3.interp(True, True) == rand_ast3.uniqueify().interp(True, True)
	assert rand_ast4.interp(True, True) == rand_ast4.uniqueify().interp(True, True)
	assert rand_ast5.interp(True, True) == rand_ast5.uniqueify().interp(True, True)

rco_ast = P(\
	ADD(
		ADD(NUM(2), NUM(3)),
		LET(VAR('X'), READ(), ADD(VAR('X'), VAR('X'))
		)
	)
)

rco_ast_hand = P(\
	LET(
		VAR('rco1'),
		ADD(NUM(2), NUM(3)),
		LET(
			VAR('rco2'),
			READ(),
			LET(
				VAR('rco3'),
				ADD(VAR('rco2'), VAR('rco2')),
				LET(
					VAR('rco0'),
					ADD(VAR('rco1'), VAR('rco3')),
					VAR('rco0')
				)
			)
		)
	)
)

def test_rcoify():
	assert rco_ast.interp(True, True) == rco_ast.rcoify().interp(True, True)
	assert rco_ast_hand.interp(True, True) == rco_ast.rcoify().interp(True, True)

	assert rand_ast.interp(True, True) == rand_ast.rcoify().interp(True, True)
	assert rand_ast2.interp(True, True) == rand_ast2.rcoify().interp(True, True)
	assert rand_ast3.interp(True, True) == rand_ast3.rcoify().interp(True, True)
	assert rand_ast4.interp(True, True) == rand_ast4.rcoify().interp(True, True)
	assert rand_ast5.interp(True, True) == rand_ast5.rcoify().interp(True, True)

	assert rand_ast_opt.interp(True, True) == rand_ast_opt.rcoify().interp(True, True)
	assert rand_ast2_opt.interp(True, True) == rand_ast2_opt.rcoify().interp(True, True)
	assert rand_ast3_opt.interp(True, True) == rand_ast3_opt.rcoify().interp(True, True)

	assert rco_ast.opt().interp(True, True) == rco_ast.opt().rcoify().interp(True, True)
	assert rand_ast.opt().interp(True, True) == rand_ast.opt().rcoify().interp(True, True)
	assert rand_ast2.opt().interp(True, True) == rand_ast2.opt().rcoify().interp(True, True)
	assert rand_ast3.opt().interp(True, inp=1) == rand_ast3.opt().rcoify().interp(True, inp=1)
	assert rand_ast4.opt().interp(True, inp=1) == rand_ast4.opt().rcoify().interp(True, inp=1)
	assert rand_ast5.opt().interp(True, True) == rand_ast5.opt().rcoify().interp(True, True)
		


def test_rand_rcoify():
	for n in range(12):
		ast = gen(rand_r1, n)
		# if ast has unused variables rcoify produces wrong output
		# so we optimize first
		ast_opt = ast.opt()
		ast_rco = ast_opt.rcoify()
		assert ast_opt.interp(True, True) == ast_rco.interp(True, True)
		assert is_rco_form(ast_rco.expr)


