from r1 import *

# (program ()
# 	(let ([x (+ 12 20)]) (+ 10 x)))

# (program ()
# 	(let ([x 32]) (+ (let ([x 10]) x) x))
# )

# (program ()
# 	(let ([x (read)]) (let ([y (read)]) (+ x (- y)))))

ast0 = P(LET(VAR('x'), ADD(NUM(12), NUM(20)), ADD(NUM(10), VAR('x'))))
ast1 = P(LET(VAR('x'), NUM(32), ADD(LET(VAR('x'), NUM(10), VAR('x')), VAR('x'))))
ast2 = P(LET(VAR('x'), READ(), LET(VAR('y'), READ(), ADD(VAR('x'), NEG(VAR('y'))))))


def test_r1_interp():
	assert ast0.interp() == 42
	assert ast1.interp() == 42
	ast2.interp(True)

def test_rand_r1():
	for n in range(12):
		ast = gen(rand_r1, n)
		assert ast.interp(True, True) == ast.optimize().interp(True, True)