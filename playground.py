#from r0 import *
from r1 import *

ast = gen(rand_r1, 4)
ast1 = gen(rand_r1_no_read, 4)

#import pdb; pdb.set_trace()

'''
P(
	NEG(
		LET(
			VAR('Q'), 
			ADD(
				ADD(
					NUM(141), READ()
				), 
				ADD
					(NUM(214), NUM(-142)
				)
			),
			LET(
				VAR('h'),
				LET(
					VAR('S'),
					NUM(-143), 
					NUM(17)
				),
				LET(
					VAR('z'),
					READ(),
					VAR('z')
				)
			)
		)
	)
)

P(
	NEG(
		LET(
			VAR('z'),
			READ(),
			VAR('z')
		)
	)
)
'''
'''

while 1:
	ast = gen(rand_r1, 4)
	if ast.interp(True, True) != ast.opt().interp(True, True):
		import pdb; pdb.set_trace()
		print('🐞')

'''