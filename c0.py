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

RAND = choice(range(100))

class Expr:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, env, db, inp):
		return self


class READ(Expr):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self):
		self.str = "(read)"

	def interp(self, env, db, inp):
		if db:
			if inp:
				self.num = inp
			else:
				self.num = READ._db_cnt
				READ._db_cnt = self.num - 1
		else:
			self.num = int(input("Input an integer: ",))
		READ._rd_cnt = READ._rd_cnt + 1
		return self.num

class NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {self.expr})"

	def interp(self, env, db, inp):
		return 0 - self.expr.interp(env, db, inp)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {self.lhs} {self.rhs})"

	def interp(self, env, db, inp):
		return self.lhs.interp(env, db, inp) + self.rhs.interp(env, db, inp)


class ARG(EXPR):
	def __init__(self):
		pass

	def interp(self, env, db, inp):
		pass

class NUM(ARG):
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

class VAR(ARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"

	def interp(self, env, db, inp):
		try:
			return env[self.name]
		except KeyError:
			print(f'Undefined var {self.name}')
			raise SystemExit


class TAIL:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, env, db, inp):
		pass

class RET(TAIL):
	def __init__(self, expr):
		self.arg = arg
		self.str = f"(return {self.arg})"

	def interp(self, env, db, inp):
		return self.arg.interp(env, db, inp)

class SEQ(TAIL):
	def __init__(self, stmt, tail):
		self.stmt = stmt
		self.tail = tail
		self.str = f"(seq {self.stmt} {self.tail})"

	def interp(self, env, db, inp):
		self.stmt.interp(env, db, inp)
		self.tail.interp(env, db, inp)


 class STMT:
	def __init__(self, var, expr):
		self.var = var
		self.expr = expr
		self.str = f"(assign {self.var} {self.expr})"

	def interp(self, env, db, inp):
		env[self.var.name] = self.expr.interp(env, db, inp)


class P:
	def __init__(self, env):
		# a dict of labels to tails
		self.env = env

	def interp(self, db=False, reset=False, inp=0):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.env['main'].interp({}, db, inp)
		return ans

	def print(self):
		print('(program info ',)
		for k,v in self.env.items():
			print(f"{k} . {v}")
		print(')')

def econ(r):
	pass
