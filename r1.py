from random import choice
from string import ascii_letters

RAND = choice(range(100))

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

	def interp(self, env, db, inp):
		pass

	def is_var(self):
		return False

	def opt(self, env):
		return self

	def is_unused(self, var):
		pass

class LET(Expr):
	def __init__(self, var, xe, be):
		self.var = var
		self.xe = xe
		self.be = be
		self.str = f"LET({self.var}, {self.xe}, {self.be})"

	def interp(self, env, db, inp):
		new_env = env.copy()
		new_env[self.var.val] = self.xe.interp(env, db, inp)
		return self.be.interp(new_env, db, inp)

	def opt(self, env):
		b_env = {key:val for key, val in env.items() if key != self.var.val}
		be = self.be.opt(b_env)
		if be.is_unused(self.var):
			return be
		xe = self.xe.opt(env)
		if xe.is_num():
			new_env = env.copy()
			new_env[self.var.val] = xe
			return self.be.opt(new_env)
		else:
			return LET(self.var, xe, be)

	def is_unused(self, var):
		return self.xe.is_unused(var) and self.be.is_unused(var)



class VAR(Expr):
	def __init__(self, var):
		self.val = var
		self.str = f"VAR('{self.val}')"

	def interp(self, env, db, inp):
		return env[self.val]

	def is_leaf(self):
		return True

	def is_var(self):
		return True

	def opt(self, env):
		try:
			return env[self.val]
		except KeyError:
			return self

	def is_unused(self, var):
		return not self.val == var.val

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = f"NUM({self.num})"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def interp(self, env, db, inp):
		return self.num

	def is_unused(self, var):
		return True

class READ(Expr):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self):
		self.str = "READ()"

	def is_leaf(self):
		return True

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

	def is_var(self):
		return True

	def is_unused(self, var):
		return True

class NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"NEG({self.expr})"

	def interp(self, env, db, inp):
		return 0 - self.expr.interp(env, db, inp)

	def opt(self, env):
		expr = self.expr.opt(env)

		if expr.is_num():
			return NUM(-expr.num)
		elif type(expr) == NEG:
			return expr.expr
		return NEG(expr)

	def is_unused(self, var):
		return self.expr.is_unused(var)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"ADD({self.lhs}, {self.rhs})"

	def interp(self, env, db, inp):
		return self.lhs.interp(env, db, inp) + self.rhs.interp(env, db, inp)

	def opt(self, env):
		lhs = self.lhs.opt(env)
		rhs = self.rhs.opt(env)

		if lhs.is_num() and rhs.is_num():
			return NUM(lhs.num + rhs.num)
		elif type(lhs) == NEG and type(rhs) == NEG:
			return NEG(ADD(lhs.expr, rhs.expr))
		elif lhs.is_num() and type(rhs) == ADD:
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
		elif rhs.is_num() and type(lhs) == ADD:
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

	def is_unused(self, var):
		return self.lhs.is_unused(var) and self.rhs.is_unused(var)

class P:
	def __init__(self, e):
		self.expr = e
		self.str = f"P({e})"

	def show(self):
		print(self.str)

	def interp(self, db=False, reset=False, inp=0):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.expr.interp({}, db, inp)
		return ans

	def opt(self):
		return P(self.expr.opt({}))

	def __eq__(self, rhs):
		return self.show() == rhs.show()

def gen(f, n):
	return P(f(n))

def rand_r1(n, vs=[]):
	if n == 0:
		if choice([0,1]) and vs:
			return choice(vs)
		else:
			return NUM(choice(range(-256, 256))) if choice([0,1]) else READ()
	j = choice([0,1,2])
	if j == 0:
		return NEG(rand_r1(n-1, vs))
	elif j == 1:
		return \
			ADD(rand_r1(n-1, vs), rand_r1(n-1, vs))
	else:
		x_prime = VAR(choice(ascii_letters))
		vs_prime = vs + [x_prime]
		return \
			LET(x_prime, rand_r1(n-1, vs), rand_r1(n-1, vs_prime))

def rand_r1_no_read(n, vs=[]):
	if n == 0:
		if choice([0,1]) and vs:
			return choice(vs)
		else:
			return NUM(choice(range(-256, 256)))
	j = choice([0,1,2])
	if j == 0:
		return NEG(rand_r1_no_read(n-1, vs))
	elif j == 1:
		return \
			ADD(rand_r1_no_read(n-1, vs), rand_r1_no_read(n-1, vs))
	else:
		x_prime = VAR(choice(ascii_letters))
		vs_prime = vs + [x_prime]
		return \
			LET(x_prime, rand_r1_no_read(n-1, vs), rand_r1_no_read(n-1, vs_prime))