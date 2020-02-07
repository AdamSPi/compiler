# e := num | (read) | (-  e) | (+ e e)
# p := (program any e)
class Expr():
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

class EX_NUM(Expr):
	def __init__(self, num):
		self.str = str(num)

class EX_READ(Expr):
	def __init__(self):
		self.str = "(read)"

class EX_NEG(Expr):
	def __init__(self, e):
		self.str = f"(- {e})"

class EX_ADD(Expr):
	def __init__(self, e1, e2):
		self.str = f"(+ {e1} {e2})"

class P():
	def __init__(self, e):
		self.str = f"(program {e})"

	def print(self):
		print(self.str)