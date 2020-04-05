from r1 import *
import os
import sys

import pexpect

import re

from rand import RAND

r = \
	P(
		LET(
			VAR('t'),
			NEG(NEG(NEG(READ()))), 
			ADD(
				ADD(
					ADD(VAR('t'), VAR('t')), 
					NEG(VAR('t'))
				),
				LET(
					VAR('H'),
					NEG(VAR('t')),
					ADD(VAR('t'), VAR('t'))
				)
			)
		)
	)

r2 = \
	P(
		LET(
			VAR('z'),
			NEG(
				ADD(
					NUM(246),
					NUM(137)
				)
			),
			LET( # z -> -383
				VAR('z'),
				ADD(
					VAR('z'),
					READ()
				),
				NEG(VAR('z')) # z -> ADD(-383, READ())
			)
		)
	)


r3 = \
	P(
		LET(
			VAR('F'),
			LET(
				VAR('r'),
				LET(
					VAR('u'),
					LET(
						VAR('S'),
						READ(),
						READ()
					),
					NEG(NUM(-209))
				),
				LET(
					VAR('E'),
					LET(
						VAR('v'),
						VAR('r'),
						READ()
					),
					NEG(VAR('E'))
				)
			),
			LET(
				VAR('x'),
				NEG(NEG(VAR('F'))),
				ADD(
					LET(
						VAR('F'),
						READ(),
						VAR('x')
					),
					NEG(NUM(146))
				)
			)
		)
	)

r4 = \
	P(
		LET(
			VAR('I'),
			NEG(
				ADD(
					NEG(
						NUM(-36)
					),
					LET(
						VAR('H'),
						READ(),
						VAR('H')
					)
				)
			),
			LET(
				VAR('c'),
				NEG(NEG(VAR('I'))),
				LET(
					VAR('I'),
					NEG(READ()),
					ADD(
						VAR('c'),
						VAR('I')
					)
				)
			)
		)
	)

r5 = \
	P(
		NEG(
			LET(
				VAR('w'),
				NEG(
					LET(
						VAR('r'),
						ADD(
							LET(
								VAR('I'),
								READ(),
								READ()
							),
							ADD(
								NUM(-221), 
								NUM(110)
							)
						),
						LET(
							VAR('l'),
							NEG(NUM(194)),
							LET(
								VAR('G'),
								NUM(-116),
								VAR('G')
							)
						)
					)
				),
				ADD(
					LET(
						VAR('J'),
						NEG(NEG(VAR('w'))),
						LET(
							VAR('w'),
							ADD(
								VAR('J'),
								VAR('w')
							),
							ADD(
								VAR('w'),
								VAR('J')
							)
						)
					),
					NEG(NEG(NEG(NUM(-101))))
				)
			)
		)
	)

r6 = P(\
	ADD(
		ADD(NUM(2), NUM(3)),
		LET(VAR('X'), READ(), ADD(VAR('X'), VAR('X'))
		)
	)
)

r7 = P(\
	LET(
		VAR('rco1'),
		ADD(NUM(2), NUM(3)),
		LET(
			VAR('rco2'),
			READ(),
			LET(
				VAR('rco3'),
				ADD(VAR('rco2'), VAR('rco2')),
				LET(
					VAR('rco0'),
					ADD(VAR('rco1'), VAR('rco3')),
					VAR('rco0')
				)
			)
		)
	)
)

def test_asm():
	for r_ast in [r,r2,r3,r4,r5,r6,r7]:
		x = r_ast.to_asm(1)
		
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
				child.sendline(f'{RAND-i}')
				i += 1
			except:
				break
		nums = re.findall(r'-?\d+', str(child.before)) 
		assert r_ast.opt().interp(True, True) == int(list(map(int, nums))[-1])

def test_asm_gen():
	for n in range(8):
		r_ast = gen(rand_r1, n)
		x = r_ast.to_asm(1)
		
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
				child.sendline(f'{RAND-i}')
				i += 1
			except:
				break
		nums = re.findall(r'-?\d+', str(child.before)) 
		assert r_ast.opt().interp(True, True) == int(list(map(int, nums))[-1])