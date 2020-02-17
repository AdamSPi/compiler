from random import choice

RAND = choice([0,100])
READ_COUNT = 0

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

	def interp(self, db):
		pass

	def opt(self):
		return self

class NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = f"{self.num}"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def interp(self, db):
		return self.num

class READ(Expr):
	_db_cnt = RAND

	def __init__(self):
		self.str = "(read)"

	def is_leaf(self):
		return True

	def interp(self, db):
		global READ_COUNT
		if db:
			self.num = READ._db_cnt
			READ._db_cnt = READ._db_cnt - 1
		else:
			self.num = int(input("Input an integer: ",))
		READ_COUNT = READ_COUNT + 1
		return self.num

class NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {self.expr})"

	def interp(self, db):
		return 0 - self.expr.interp(db)

	def opt(self):
		expr = self.expr.opt()

		if expr.is_num():
			return NUM(-expr.num)
		elif type(expr) == NEG:
			return expr.expr
		return NEG(expr)

class ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {self.lhs} {self.rhs})"

	def interp(self, db):
		return self.lhs.interp(db) + self.rhs.interp(db)

	def opt(self):
		lhs = self.lhs.opt()
		rhs = self.rhs.opt()

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
			type(rhs.rhs) == READ and type(lhs.lhs) == READ:
				return ADD(
						NUM(rhs.lhs.num +  lhs.rhs.num),
						ADD(rhs.rhs, lhs.lhs)
					)
			elif rhs.lhs.is_num() and lhs.lhs.is_num() and \
			type(rhs.rhs) == READ and type(lhs.rhs) == READ:
				return ADD(
						NUM(rhs.lhs.num +  lhs.lhs.num),
						ADD(rhs.rhs, lhs.rhs)
					)
			elif rhs.rhs.is_num() and lhs.rhs.is_num() and \
			type(rhs.lhs) == READ and type(lhs.lhs) == READ:
				return ADD(
						NUM(rhs.rhs.num +  lhs.rhs.num),
						ADD(rhs.lhs, lhs.lhs)
					)
			elif rhs.rhs.is_num() and lhs.lhs.is_num() and \
			type(rhs.lhs) == READ and type(lhs.rhs) == READ:
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
		ans = self.expr.interp(db)
		return ans

	def opt(self):
		return P(self.expr.opt())

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
