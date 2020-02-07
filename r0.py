from random import choice
# e := num | (read) | (-  e) | (+ e e)
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

	def interp(self, debug):
		pass

	def optimize(self):
		return self

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = str(num)

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def interp(self, debug):
		return self.num

class READ(Expr):
	debug_counter = 42

	def __init__(self):
		self.str = "(read)"

	def is_leaf(self):
		return True

	def interp(self, debug):
		if debug:
			self.num = READ.debug_counter
			READ.debug_counter = READ.debug_counter - 1
		else:
			self.num = int(input())
		return self.num

class NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {e})"

	def interp(self, debug):
		return 0 - self.expr.interp(debug)

	def optimize(self):
		expr = self.expr.optimize()

		if expr.is_num():
			return NUM(-expr.num)
		return NEG(expr)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {e1} {e2})"

	def interp(self, debug):
		return self.lhs.interp(debug) + self.rhs.interp(debug)

	def optimize(self):
		lhs = self.lhs.optimize()
		rhs = self.rhs.optimize()

		if lhs.is_num() and rhs.is_num():
			return NUM(lhs.num + rhs.num)
		return ADD(lhs, rhs)

class P:
	def __init__(self, e):
		self.expr = e
		self.str = f"(program {e})"

	def show(self):
		print(self.str)

	def interp(self, debug=False):
		return self.expr.interp(debug)

	def optimize(self):
		return P(self.expr.optimize())

def gen(f, n):
	return P(f(n))

def exp_r0(n):
	if n == 0:
		return NUM(1)
	return ADD(exp_r0(n-1), exp_r0(n-1))

def rand_r0(n):
	if n == 0:
		return \
			NUM(choice(range(-256, 256))) if choice([0, 1]) \
			else READ()
	return \
		NEG(rand_r0(n-1)) if choice([0, 1]) \
		else ADD(rand_r0(n-1), rand_r0(n-1))

def rand_r0_no_read(n):
	if n == 0:
		return NUM(choice(range(-256, 256)))
	return \
		NEG(rand_r0_no_read(n-1)) if choice([0, 1]) \
		else ADD(rand_r0_no_read(n-1), rand_r0_no_read(n-1))
