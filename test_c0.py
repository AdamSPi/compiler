from r1 import *

def test_expcon():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		assert r_ast.interp(True, True) == r_ast.to_c().interp(True, True)