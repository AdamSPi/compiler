# e := num | (read) | (-  e) | (+ e e)
# p := (program any e)
class Expr:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def is_leaf(self):
		return False

	def interp(self, debug):
		pass

class EX_NUM(Expr):
	def __init__(self, num):
		self.num = num
		self.str = str(num)

	def is_leaf(self):
		return True

	def interp(self, debug):
		return self.num

class EX_READ(Expr):
	def __init__(self):
		self.str = f"(read)"
		self.debug_counter = 42

	def is_leaf(self):
		return True

	def interp(self, debug):
		if debug:
			self.num = self.debug_counter
			self.debug_counter = self.debug_counter - 1
		else:
			self.num = int(input())
		return self.num

class EX_NEG(Expr):
	def __init__(self, e):
		self.expr = e
		self.str = f"(- {e})"

	def interp(self, debug):
		return 0 - self.expr.interp(debug)

class EX_ADD(Expr):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.str = f"(+ {e1} {e2})"

	def interp(self, debug):
		return self.lhs.interp(debug) + self.rhs.interp(debug)

class P:
	def __init__(self, e):
		self.expr = e
		self.str = f"(program {e})"

	def print(self):
		print(self.str)

	def interp(self, debug=False):
		return self.expr.interp(debug)