# e := num | (read) | (-  e) | (+ e e)
# p := (program any e)
class Expr():
	def __init__(self):
		pass

	def __repr__(self):
		return self.v

class EX_NUM(Expr):
	def __init__(self, num):
		self.v = num

class EX_READ(Expr):
	def __init__(self):
		self.v = "(read)"

class EX_NEG(Expr):
	def __init__(self, e):
		self.v = f"(- {e})"

class EX_ADD(Expr):
	def __init__(self, e1, e2):
		self.v = f"(+ {e1} {e2})"