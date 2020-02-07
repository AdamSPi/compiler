from random import choice

RAND = choice([0,100])
READ_COUNT = 0

# e := num | (read) | (-  e) | (+ e e)
# p := (program any e)
class Expr:
	def __init__(self):
		self.args = []
		pass

	def __repr__(self):
		return self.str

	def is_num(self):
		return False

	def is_leaf(self):
		return False

	def interp(self, db):
		pass

	def optimize(self):
		return self

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = f"NUM({self.num})"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def interp(self, db):
		return self.num

class READ(Expr):
	_db_cnt = RAND

	def __init__(self):
		self.str = "READ()"

	def is_leaf(self):
		return True

	def interp(self, db):
		global READ_COUNT
		if db:
			self.num = READ._db_cnt
			READ._db_cnt = READ._db_cnt - 1
		else:
			self.num = int(input())
		READ_COUNT = READ_COUNT + 1
		return self.num

class NEG(Expr):
	def __init__(self, e):
		self.args = [e]
		self.str = f"NEG({self.args[0]})"

	def interp(self, db):
		return 0 - self.args[0].interp(db)

	def optimize(self):
		arg = self.args[0].optimize()

		if arg.is_num():
			return NUM(-arg.num)
		elif type(arg) == NEG:
			return arg.args[0]
		return NEG(arg)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.args = [e1, e2]
		self.str = f"ADD({self.args[0]}, {self.args[1]})"

	def interp(self, db):
		return self.args[0].interp(db) + self.args[1].interp(db)

	def optimize(self):
		argl = self.args[0].optimize()
		argr = self.args[1].optimize()

		if argl.is_num() and argr.is_num():
			return NUM(argl.num + argr.num)
		elif argl.is_num() and not argr.is_leaf():
			if len(argr.args) > 1:
				if argr.args[0].is_num():
					return ADD(
						NUM(argl.num + argr.args[0].num),
						argr.args[1]
					)
				elif argr.args[1].is_num():
					return ADD(
						NUM(argl.num + argr.args[1].num),
						argr.args[0]
					)
		elif argr.is_num() and not argl.is_leaf():
			if len(argl.args) > 1:
				if argl.args[0].is_num():
					return ADD(
						NUM(argr.num + argl.args[0].num),
						argl.args[1]
					)
				elif argl.args[1].is_num():
					return ADD(
						NUM(argr.num + argl.args[1].num),
						argl.args[0]
					)

		return ADD(argl, argr)

class P:
	def __init__(self, e):
		self.args = [e]
		self.str = f"P({e})"

	def show(self):
		print(self.str)

	def interp(self, db=False, reset=False):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.args[0].interp(db)
		return ans

	def optimize(self):
		return P(self.args[0].optimize())

	def __eq__(self, rhs):
		return self.show() == rhs.show()

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
