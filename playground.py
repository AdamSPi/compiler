from r1 import *
import os
import sys

import pexpect

import re

from rand import RAND


rco_ast = P(\
	ADD(
		ADD(NUM(2), NUM(3)),
		LET(VAR('X'), READ(), ADD(VAR('X'), VAR('X'))
		)
	)
)
# # import pdb; pdb.set_trace()
# # rco_ast.rcoify().show()

# P(
# 	LET(VAR('rco0'), ADD(NUM(2), NUM(3)),
# 		LET(VAR('rco1'), READ(), 
# 			LET(VAR('rco2'), ADD(VAR('rco1'), VAR('rco1')),
# 				LET(VAR('rco3'), ADD(VAR('rco0'), VAR('rco2')), VAR('rco3'))
# 			)
# 		)
# 	)
# )

# rco_ast.pprint()
# rco_ast.uniqueify().rcoify().pprint()
# rco_ast.to_c().pprint()
# print(rco_ast.interp(True, True))
# print(rco_ast.uniqueify().rcoify().interp(True, True))
# print(rco_ast.to_c().interp(True, True))
# c1 = rco_ast.to_c()
# c1.uncover_locs()
# print(c1.info['locals'])
# c1.pprint()

# p1 = P(ADD(NUM(52), NEG(NUM(10))))
# p1.to_c().select().pprint()
# print()
# p1.to_x().assign_homes().pprint()
# print(p1.to_x().assign_homes().interp(True, True))

# p2 = P(
# 		LET(
# 			VAR('A'), NUM(42),
# 			LET(
# 				VAR('B'), READ(),
# 				VAR('B')
# 			)
# 		)
# 	)

# x = p2.uniqueify().rcoify()
# x.pprint()
# xx = x.expcon()
# xx.pprint()
# print()
# print(p2.to_x().assign_homes().patch_instr().interp(True, True))

# x1 = X({},\
# 	{'_begin': BLCK({}, [\
# 		MOV(xNUM(42),DREF(rsi, 8)),
# 		MOV(DREF(rsi, 8), DREF(rsi, 16)),
# 		MOV(DREF(rsi, 16), rax),
# 		xRET()
# 	]),
# 	'_main': BLCK({}, [\
# 		JMP('_begin')
# 	])
# 	}
# )

# x1.patch_instr().pprint()

print('Expected: ' + str(rco_ast.interp(True, True)))
print()
x = rco_ast.to_asm()
sys.stdout = open("x.s", "w")
x.pprint()
sys.stdout.close()
sys.stdout = sys.__stdout__
# link it w/ runtime
os.system('make build')

i = 0

child = pexpect.spawn('./x.bin')

while child.isalive():
	try:
		child.expect('read_int')
		print('read')
		print(f'sending {RAND-i}')
		child.sendline(f'{RAND-i}')
		i += 1
	except:
		break
nums = re.findall(r'\d+', str(child.before)) 
print(list(map(int, nums))[-1])
