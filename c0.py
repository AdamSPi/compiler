'''
var ::= arg
label ::= string
arg ::= int | var
exp ::= arg | (read) | (- arg) | (+ arg arg)
stmt ::= (assign var exp)
tail ::= (return exp) | (seq stmt tail)
C0 ::= (program info ((label . tail)+))
'''
from random import choice
from rand import RAND

from x0 import *

class cExpr:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, env, db, inp):
		return self

	def select_e(self, dst):
		pass


class cREAD(cExpr):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self):
		self.str = "(read)"

	def interp(self, env, db, inp):
		if db:
			if inp:
				self.num = inp
			else:
				self.num = cREAD._db_cnt
				cREAD._db_cnt = self.num - 1
		else:
			self.num = int(input("Input an integer: ",))
		cREAD._rd_cnt = cREAD._rd_cnt + 1
		return self.num

	def select_e(self, dst):
		return [\
			CALL('_read_int'),
			MAX(rax, dst)
		]

class cNEG(cExpr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {self.expr})"

	def interp(self, env, db, inp):
		return 0 - self.expr.interp(env, db, inp)

	def select_e(self, dst):
		return [\
			MOV(self.expr.select_a(), dst),
			xNEG(dst)
		]

class cADD(cExpr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {self.lhs} {self.rhs})"

	def interp(self, env, db, inp):
		return self.lhs.interp(env, db, inp) + self.rhs.interp(env, db, inp)

	def select_e(self, dst):
		return [\
			MOV(self.rhs.select_a(), dst),
			xADD(self.lhs.select_a(), dst)
		]


class cARG(cExpr):
	def __init__(self):
		pass

	def interp(self, env, db, inp):
		pass

	def select_a(self):
		pass

	def select_e(self, dst):
		return [\
			MOV(self.select_a(), dst)
		]

class cNUM(cARG):
	def __init__(self, num):
		self.num = num
		self.str = f"{self.num}"

	def __add__(self, op):
		return NUM(self.num + op.num)

	def __sub__(self, op):
		return NUM(self.num - op.num)

	def __eq__(self, op):
		return self.num == op.num

	def __neg__(self):
		return NUM(-self.num)

	def interp(self, env, db, inp):
		return self.num

	def select_a(self):
		return xNUM(self.num)

class cVAR(cARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"

	def interp(self, env, db, inp):
		try:
			return env[self.name]
		except KeyError:
			print(f'Undefined var {self.name}')
			raise SystemExit

	def select_a(self):
		return xVAR(self.name)


class TAIL:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, env, db, inp):
		pass

	def uncover_locs(self):
		pass

	def select_t(self):
		pass

class RET(TAIL):
	def __init__(self, arg):
		self.arg = arg
		self.str = f"(return {self.arg})"

	def interp(self, env, db, inp):
		return self.arg.interp(env, db, inp)

	def uncover_locs(self):
		return []

	def select_t(self):
		return [\
			MOV(self.arg.select_a(), rax),
			JMP('_end')
		]

class SEQ(TAIL):
	def __init__(self, stmt, tail):
		self.stmt = stmt
		self.tail = tail
		self.str = f"(seq {self.stmt}\n{self.tail})"

	def interp(self, env, db, inp):
		self.stmt.interp(env, db, inp)
		return self.tail.interp(env, db, inp)

	def uncover_locs(self):
		return self.stmt.uncover_locs() + self.tail.uncover_locs()

	def select_t(self):
		return self.stmt.select_t() + self.tail.select_t()

class STMT(TAIL):
	def __init__(self, var, expr):
		self.var = var
		self.expr = expr
		self.str = f"(assign {self.var} {self.expr})"

	def interp(self, env, db, inp):
		env[self.var.name] = self.expr.interp(env, db, inp)

	def uncover_locs(self):
		return [self.var]

	def select_t(self):
		return self.expr.select_e(self.var.select_a())


  
class C:
	def __init__(self, info, env):
		self.info = info
		# a dict of labels to tails
		self.env = env

	def interp(self, db=False, reset=False, inp=0):
		global RAND
		if reset:
			cREAD._db_cnt = RAND
		ans = self.env['main'].interp({}, db, inp)
		return ans

	def uncover_locs(self):
		self.info = {'locals': self.env['main'].uncover_locs()}

	def select(self):
		main_blck = BLCK({}, self.env['main'].select_t())
		end_blck = BLCK({},  [xRET()])

		return X({}, {'_main': main_blck, '_end': end_blck})

	def pprint(self):
		print(f"(program\n(locals . {self.info['locals']})",)
		for k,v in self.env.items():
			print(f"{k} .\n{v}")
		print(')')
