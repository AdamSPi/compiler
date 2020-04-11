from r1 import *


dbl_main_blck = BLCK({}, [
		MOV(xNUM(5), rax),
		xADD(rax, rax),
		xRET()
	]
)

dbl_ms = {'start': dbl_main_blck}

x0_test = X({}, dbl_ms)

def test_x0_double():
	assert x0_test.interp()[rax] == xNUM(10)

read_dubl_main_blck = BLCK({}, [
		CALL('read_int'),
		xADD(rax, rax),
		xRET()
	]
)

read_ms =  {'start': read_dubl_main_blck}

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

def test_uncover_live():
	test_blck = BLCK(
	{}, 
	[
	MOV(xNUM(1), xVAR('v')),
	MOV(xNUM(46), xVAR('w')),
	MOV(xVAR('v'), xVAR('x')),
	xADD(xNUM(7), xVAR('x')),
	MOV(xVAR('x'), xVAR('y')),
	xADD(xNUM(4), xVAR('y')),
	MOV(xVAR('x'), xVAR('z')),
	xADD(xVAR('w'), xVAR('z')),
	MOV(xVAR('y'), xVAR('t.1')),
	xNEG(xVAR('t.1')),
	MOV(xVAR('z'), rax),
	xADD(xVAR('t.1'), rax),
	JMP('conclusion')
	]
	)

	x = X({}, {'start': test_blck})

	exp_res = {
		2: {'v'},
		3: {'w', 'v'},
		4: {'w', 'x'},
		5: {'w', 'x'},
		6: {'y', 'w', 'x'},
		7: {'y', 'w', 'x'},
		8: {'z', 'y', 'w'},
		9: {'z', 'y'},
		10: {'z', 't.1'},
		11: {'t.1', 'z'},
		12: {'t.1'},
		13: set(),
		14: set()
	}

	assert x.uncover_live().info['liveness'] == exp_res
