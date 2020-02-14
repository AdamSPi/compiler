from random import choice
from r0 import rand_r0, rand_r0_no_read

import string

RAND = choice([0,100])
READ_COUNT = 0

# e := num | (read) | (-  e) | (+ e e)
#    | var | let var := xe in be
# p := (program any e)

class Expr:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def is_num(self):
		return False

	def is_leaf(self):
		return False

	def interp(self, env, db):
		pass

	def is_var(self):
		return False

	def optimize(self):
		return self

class LET(Expr):
	def __init__(self, var, xe, be):
		self.var = var
		self.xe = xe
		self.be = be
		self.str = f"(let ([{self.var} {self.xe}]) {self.be})"

	def interp(self, env, db):
		new_env = env.copy()
		new_env[self.var.val] = self.xe.interp(env, db)
		return self.be.interp(new_env, db)

	def optimize(self):
		xe = self.xe.optimize()
		be  =  self.be.optimize()
		return LET(self.var, xe, be)


class VAR(Expr):
	def __init__(self, var):
		self.val = var
		self.str = f"{self.val}"

	def interp(self, env, db):
		try:
			return env[self.val]
		except:
			print("Variable not bound exception")
			raise

	def is_leaf(self):
		return True

	def is_var(self):
		return True

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = f"{self.num}"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def interp(self, env, db):
		return self.num

class READ(Expr):
	_db_cnt = RAND

	def __init__(self):
		self.str = "(read)"

	def is_leaf(self):
		return True

	def interp(self, env, db):
		global READ_COUNT
		if db:
			self.num = READ._db_cnt
			READ._db_cnt = READ._db_cnt - 1
		else:
			self.num = int(input("Input an integer: ",))
		READ_COUNT = READ_COUNT + 1
		return self.num

	def is_var(self):
		return True

class NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {self.expr})"

	def interp(self, env, db):
		return 0 - self.expr.interp(env, db)

	def optimize(self):
		expr = self.expr.optimize()

		if expr.is_num():
			return NUM(-expr.num)
		elif type(expr) == NEG:
			return expr.expr
		return NEG(expr)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {self.lhs} {self.rhs})"

	def interp(self, env, db):
		return self.lhs.interp(env, db) + self.rhs.interp(env, db)

	def optimize(self):
		lhs = self.lhs.optimize()
		rhs = self.rhs.optimize()

		if lhs.is_num() and rhs.is_num():
			return NUM(lhs.num + rhs.num)
		elif lhs.is_num() and not rhs.is_leaf():
			if type(rhs) == ADD:
				if rhs.lhs.is_num():
					return ADD(
						NUM(lhs.num + rhs.lhs.num),
						rhs.rhs
					)
				elif rhs.rhs.is_num():
					return ADD(
						NUM(lhs.num + rhs.rhs.num),
						rhs.lhs
					)
		elif rhs.is_num() and not lhs.is_leaf():
			if type(lhs) == ADD:
				if lhs.lhs.is_num():
					return ADD(
						NUM(rhs.num + lhs.lhs.num),
						lhs.rhs
					)
				elif lhs.rhs.is_num():
					return ADD(
						NUM(rhs.num + lhs.rhs.num),
						lhs.lhs
					)
		elif type(rhs) ==  ADD and type(lhs) == ADD:
			if rhs.lhs.is_num() and lhs.rhs.is_num() and \
			rhs.rhs.is_var() and lhs.lhs.is_var():
				return ADD(
						NUM(rhs.lhs.num +  lhs.rhs.num),
						ADD(rhs.rhs, lhs.lhs)
					)
			elif rhs.lhs.is_num() and lhs.lhs.is_num() and \
			rhs.rhs.is_var() and lhs.rhs.is_var():
				return ADD(
						NUM(rhs.lhs.num +  lhs.lhs.num),
						ADD(rhs.rhs, lhs.rhs)
					)
			elif rhs.rhs.is_num() and lhs.rhs.is_num() and \
			rhs.lhs.is_var() and lhs.lhs.is_var():
				return ADD(
						NUM(rhs.rhs.num +  lhs.rhs.num),
						ADD(rhs.lhs, lhs.lhs)
					)
			elif rhs.rhs.is_num() and lhs.lhs.is_num() and \
			rhs.lhs.is_var() and lhs.rhs.is_var():
				return ADD(
						NUM(rhs.rhs.num +  lhs.lhs.num),
						ADD(rhs.lhs, lhs.rhs)
					)

		return ADD(lhs, rhs)

class P:
	def __init__(self, e):
		self.expr = e
		self.str = f"(program () {e})"

	def show(self):
		print(self.str)

	def interp(self, db=False, reset=False):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.expr.interp({}, db)
		return ans

	def optimize(self):
		return P(self.expr.optimize())

	def __eq__(self, rhs):
		return self.show() == rhs.show()

def gen(f, n):
	return P(f(n))

def rand_r1(n, vs=[]):
	if n == 0:
		i = choice([0,1,2])
		if i == 0 and vs:
			return choice(vs)
		elif i == 1:
			return READ()
		else:
			return NUM(choice(range(-256, 256)))
	j = choice([0,1,2])
	if j == 0:
		return NEG(rand_r1(n-1, vs))
	elif j == 1:
		return ADD(rand_r1(n-1, vs), rand_r1(n-1, vs))
	else:
		x_prime = VAR(choice(string.ascii_letters))
		vs_prime = vs + [x_prime]
		return LET(x_prime, rand_r1(n-1, vs), rand_r1(n-1, vs_prime))

