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
		return self.pp

	def is_num(self):
		return False

	def is_leaf(self):
		return False

	def interp(self, env, db, inp):
		pass

	def is_var(self):
		return False

	def is_simp(self, env):
		return False

	def opt(self, env):
		return self

	def uniqueify(self, env):
		return self

	def is_unused(self, var):
		pass

class LET(Expr):
	def __init__(self, var, xe, be):
		self.var = var
		self.xe = xe
		self.be = be
		self.str = f"(let ([{self.var} {self.xe}]) {self.be})"
		self.pp = f"LET({self.var}, {self.xe}, {self.be})"

	def interp(self, env, db, inp):
		env_n = env.copy()
		env_n[self.var.val] = self.xe.interp(env, db, inp)
		return self.be.interp(env_n, db, inp)

	def opt(self, env):
		xe = self.xe.opt(env)
		syms = env.copy()
		syms[self.var.val] = xe
		be = self.be.opt(syms)
		if be.is_unused(self.var):
			print(f"Warning: unused variable {self.var.val}")
			return be
		elif xe.is_simp(syms):
			syms[self.var.val] = xe
			return self.be.opt(syms)
		else:
			return LET(self.var, xe, be)

	def uniqueify(self, env):
		env_p = env.copy()
		env_p[self.var.val] = env_p.setdefault(self.var.val, 0) + 1
		new_var = VAR(self.var.val + str(env_p[self.var.val]))
		return LET(new_var, self.xe.uniqueify(env), self.be.uniqueify(env_p))

	def is_unused(self, var):
		return self.xe.is_unused(var) and self.be.is_unused(var)



class VAR(Expr):
	def __init__(self, var):
		self.val = var
		self.str = f"{self.val}"
		self.pp = f"VAR('{self.val}')"

	def interp(self, env, db, inp):
		try:
			return env[self.val]
		except KeyError:
			print(f'Undefined var {self.val}')
			raise SystemExit

	def is_leaf(self):
		return True

	def is_var(self):
		return True

	def is_simp(self, env):
		return True

	def opt(self, env):
		try:
			val = env[self.val]
			return val if val.is_simp(env) else self
		except KeyError:
			print(f'Undefined var {self.val}')
			raise SystemExit

	def uniqueify(self, env):
		return VAR(self.val + str(env[self.val]))

	def is_unused(self, var):
		return not self.val == var.val

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = f"{self.num}"
		self.pp = f"NUM({self.num})"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def is_simp(self, env):
		return True

	def interp(self, env, db, inp):
		return self.num

	def is_unused(self, var):
		return True

class READ(Expr):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self):
		self.str = "(read)"
		self.pp = "READ()"

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
		self.str = f"(- {self.expr})"
		self.pp = f"NEG({self.expr})"

	def interp(self, env, db, inp):
		return 0 - self.expr.interp(env, db, inp)

	def opt(self, env):
		expr = self.expr.opt(env)

		if expr.is_num():
			return NUM(-expr.num)
		elif type(expr) == NEG:
			return expr.expr
		return NEG(expr)

	def uniqueify(self, env):
		return NEG(self.expr.uniqueify(env))

	def is_unused(self, var):
		return self.expr.is_unused(var)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {self.lhs} {self.rhs})"
		self.pp = f"ADD({self.lhs}, {self.rhs})"

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

	def uniqueify(self, env):
		return ADD(self.lhs.uniqueify(env), self.rhs.uniqueify(env))

	def is_unused(self, var):
		return self.lhs.is_unused(var) and self.rhs.is_unused(var)

class P:
	def __init__(self, e):
		self.expr = e
		self.str = f"(program () {e})"
		self.pp = f"P({e})"

	def show(self):
		print(self.pp)

	def interp(self, db=False, reset=False, inp=0):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.expr.interp({}, db, inp)
		return ans

	def opt(self):
		return P(self.expr.uniqueify({}).opt({}))

	def uniqueify(self):
		return P(self.expr.uniqueify({}))

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