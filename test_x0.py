from x0 import *

init_ms = {
	rsp: NUM(0),
	rbp: NUM(0),
	rax: NUM(0),
	rbx: NUM(0),
	rcx: NUM(0),
	rdx: NUM(0),
	rsi: NUM(0),
	rdi: NUM(0),
	r8 : NUM(0),
	r9 : NUM(0),
	r10: NUM(0),
	r11: NUM(0),
	r12: NUM(0),
	r13: NUM(0),
	r14: NUM(0),
	r15: NUM(0),
}


dbl_main_blck = BLCK({}, [
		MOV(NUM(5), rax),
		ADD(rax, rax),
		RET()
	]
)

dbl_ms = init_ms.copy()
dbl_ms['_main'] = dbl_main_blck

x0_test = X({}, dbl_ms)

def test_x0_double():
	assert x0_test.interp()[rax] == NUM(10)

read_dubl_main_blck = BLCK({}, [
		CALL('read_int'),
		ADD(rax, rax),
		RET()
	]
)

read_ms = init_ms.copy()
read_ms['_main'] = read_dubl_main_blck

x0_test2 = X({}, read_ms)

def test_x0_input():
	assert x0_test2.interp(True, True)[rax] == NUM(2 * RAND)
