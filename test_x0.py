from x0 import *

init_ms = {
	rsp: xNUM(0),
	rbp: xNUM(0),
	rax: xNUM(0),
	rbx: xNUM(0),
	rcx: xNUM(0),
	rdx: xNUM(0),
	rsi: xNUM(0),
	rdi: xNUM(0),
	r8 : xNUM(0),
	r9 : xNUM(0),
	r10: xNUM(0),
	r11: xNUM(0),
	r12: xNUM(0),
	r13: xNUM(0),
	r14: xNUM(0),
	r15: xNUM(0),
}


dbl_main_blck = BLCK({}, [
		MOV(xNUM(5), rax),
		xADD(rax, rax),
		xRET()
	]
)

dbl_ms = init_ms.copy()
dbl_ms['_main'] = dbl_main_blck

x0_test = X({}, dbl_ms)

def test_x0_double():
	assert x0_test.interp()[rax] == xNUM(10)

read_dubl_main_blck = BLCK({}, [
		CALL('read_int'),
		xADD(rax, rax),
		xRET()
	]
)

read_ms = init_ms.copy()
read_ms['_main'] = read_dubl_main_blck

x0_test2 = X({}, read_ms)

def test_x0_input():
	assert x0_test2.interp(True, True)[rax] == xNUM(2 * RAND)
