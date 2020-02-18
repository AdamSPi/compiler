#from r0 import *
from r1 import *

ast = gen(rand_r1, 4)
ast1 = gen(rand_r1_no_read, 4)

while 1:
	ast = gen(rand_r1, 8)
	if ast.interp(True, inp=1) != ast.opt().interp(True, inp=1):
		import pdb; pdb.set_trace()
		print('🐞')