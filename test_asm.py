from r1 import *
import os
import sys

import pexpect

import re

from rand import RAND
from flags import MAC_OS

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
		# run program with automated input
		proc = pexpect.spawn('./x.bin')
		
		while 1:
			try:
				proc.expect('read_int')
				proc.sendline(f'{RAND-i}')
				i += 1
			except:
				break
		nums = re.findall(r'-?\d+', str(proc.before))
		asm_ans = int(list(map(int, nums))[-1])
		assert r_ast.opt().interp(True, True) == asm_ans
		assert x.interp(True, True)[rax] == asm_ans

def test_reg_alloc():
	for n in range(8):
		r_ast = gen(rand_r1, n)
		x = r_ast.to_asm_w_reg_alloc(1)
		# 
		sys.stdout = open("x.s", "w")
		x.pprint()
		sys.stdout.close()
		sys.stdout = sys.__stdout__
		# link it w/ runtime
		os.system('make build')
		# 
		i = 0
		# run program with automated input
		proc = pexpect.spawn('./x.bin')
		# 
		while 1:
			try:
				proc.expect('read_int')
				proc.sendline(f'{RAND-i}')
				i += 1
			except:
				break
		nums = re.findall(r'-?\d+', str(proc.before))
		asm_ans = int(list(map(int, nums))[-1])
		assert r_ast.opt().interp(True, True) == asm_ans
		assert x.interp(True, True)[rax] == asm_ans

def test_mov_biasing():
	for n in range(8):
		r_ast = gen(rand_r1, n)
		x = r_ast.to_asm_w_reg_alloc(1, 1)
		# 
		sys.stdout = open("x.s", "w")
		x.pprint()
		sys.stdout.close()
		sys.stdout = sys.__stdout__
		# link it w/ runtime
		os.system('make build')
		# 
		i = 0
		# run program with automated input
		proc = pexpect.spawn('./x.bin')
		# 
		while 1:
			try:
				proc.expect('read_int')
				proc.sendline(f'{RAND-i}')
				i += 1
			except:
				break
		nums = re.findall(r'-?\d+', str(proc.before))
		asm_ans = int(list(map(int, nums))[-1])
		assert r_ast.opt().interp(True, True) == asm_ans
		assert x.interp(True, True)[rax] == asm_ans