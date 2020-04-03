from r1 import *


dbl_main_blck = BLCK({}, [
		MOV(xNUM(5), rax),
		xADD(rax, rax),
		xRET()
	]
)

dbl_ms = {'_main': dbl_main_blck}

x0_test = X({}, dbl_ms)

def test_x0_double():
	assert x0_test.interp()[rax] == xNUM(10)

read_dubl_main_blck = BLCK({}, [
		CALL('_read_int'),
		xADD(rax, rax),
		xRET()
	]
)

read_ms =  {'_main': read_dubl_main_blck}

x0_test2 = X({}, read_ms)

def test_x0_input():
	assert x0_test2.interp(True, True)[rax] == xNUM(2 * RAND)

def test_assign_homes():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		x_prog = r_ast.to_x(1)
		assert r_ast.opt().interp(True, True) == x_prog.assign_homes().interp(True, True)[rax]

def test_patch_instr():
	for n in range(12):
		r_ast = gen(rand_r1, n)
		x_prog = r_ast.to_x(1)
		assert r_ast.opt().interp(True, True) == x_prog.assign_homes().patch_instr().interp(True, True)[rax]

