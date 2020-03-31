from r1 import *

def test_expcon():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		assert r_ast.opt().interp(True, True) == r_ast.to_c(opt=1).interp(True, True)

def test_select():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		x_prog = r_ast.to_x(1)
		assert r_ast.opt().interp(True, True) == x_prog.interp(True, True)[rax]

def test_assign_homes():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		x_prog = r_ast.to_x(1)
		assert r_ast.opt().interp(True, True) == x_prog.assign_homes().interp(True, True)[rax]
