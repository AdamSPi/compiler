from random import choice
from string import ascii_letters
from rand import RAND
from c0 import *

# e := num | (read) | (-  e) | (+ e e)
#    | var | let var := xe in be
# p := (program any e)

rco_cnt = -1

def get_unq_var():
	global rco_cnt
	rco_cnt += 1
	return 'tmp.' + str(rco_cnt)

class TY():
	pass

class S64(TY):
	pass

class BOOL(TY):
	pass

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

	def rcoify(self, σ):
		pass

	def expcon_e(self):
		pass

	def expcon_a(self):
		pass

	def expcon_c(self):
		pass

	def is_unused(self, var):
		pass



class CMP(Expr, BOOL):
	def __init__(self, op, e1, e2):
		self.op = op # must be CMP
		self.e1 = e1 # must be NUM
		self.e2 = e2 # must be NUM
		self.pp = f"({e1} {op} {e2})"
		self.str = f"CMP({op}, {e1}, {e2})"

	def interp(self, env, db, inp):
		lhs = self.e1.interp(env, db, inp)
		rhs = self.e2.interp(env, db, inp)
		return self.op.interp(lhs, rhs)

	def Γ(self, γ):
		if self.e1.Γ(γ) != S64 or self.e2.Γ(γ) != S64:
			print('TypeError: expected s64')
			raise TypeError
		return BOOL


class eq(CMP):
	def __init__(self):
		self.pp = "=="
		self.str = "eq()"

	def interp(self, e1, e2):
		return e1.num == e2.num

class lt(CMP):
	def __init__(self):
		self.pp = "<"
		self.str = "lt()"

	def interp(self, e1, e2):
		return e1.num < e2.num

class lte(CMP):
	def __init__(self):
		self.pp = "<="
		self.str = "lte()"

	def interp(self, e1, e2):
		return e1.num <= e2.num

class gte(CMP):
	def __init__(self):
		self.pp = ">="
		self.str = "gte()"

	def interp(self, e1, e2):
		return e1.num >= e2.num

class gt(CMP):
	def __init__(self):
		self.pp = ">"
		self.str = "gt()"

	def interp(self, e1, e2):
		return e1.num > e2.num


class IF(Expr):
	def __init__(self, c, t, f):
		self.cond = c
		self.t = t
		self.f = f
		self.pp = f"(if {c} {t} {f})"
		self.str = f"IF({c}, {t}, {f})"

	def interp(self, env, db, inp):
		if self.cond.interp(env, db, inp):
			return self.t.interp(env, db, inp)
		return self.f.interp(env, db, inp)

	def Γ(self, γ):
		if self.cond.Γ(γ) != BOOL:
			print('TypeError: expected bool')
			raise TypeError
		type_t = self.t.Γ(γ)
		type_f = self.f.Γ(γ)
		if type_t != type_f:
			print(f'TypeError: expected {type_t}')
			raise TypeError
		return type_t

class TRUE(Expr, BOOL):
	def __init__(self):
		self.pp = "(true)"
		self.str = "TRUE()"

	def interp(self, env, db, inp):
		return self

	def Γ(self, γ):
		return BOOL

	def __bool__(self):
		return True

class FALSE(Expr, BOOL):
	def __init__(self):
		self.pp = "(false)"
		self.str = "FALSE()"

	def interp(self, env, db, inp):
		return self

	def Γ(self, γ):
		return BOOL

	def __bool__(self):
		return False

class NOT(Expr, BOOL):
	def __init__(self, b):
		self.bool = e
		self.pp = f"(not {self.bool})"
		self.str = f"NOT({self.bool})"

	def interp(self, env, db, inp):
		if self.bool.interp(env, db, inp):
			return TRUE()
		return FALSE()

	def Γ(self, γ):
		b = self.bool.Γ(γ)
		if b != BOOL:
			print('TypeError: expected bool')
			raise TypeError
		return BOOL

class AND(Expr, BOOL):
	def __init__(self, e1, e2):
		return IF(e1, e2, FALSE())


class OR(Expr, BOOL):
	def __init__(self, e1, e2):
		return IF(e1, TRUE(), e2)



class SUB(Expr):
	def __init__(self, e1, e2):
		return ADD(e2, NEG(e1))

class LET(Expr):
	def __init__(self, var, xe, be):
		self.var = var
		self.xe = xe
		self.be = be
		self.pp = f"\n(let ([{self.var} {self.xe}]) {self.be})"
		self.str = f"LET({self.var.str}, {self.xe.str}, {self.be.str})"

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
		new_var = VAR(self.var.val + '.' + str(env_p[self.var.val]))
		return LET(new_var, self.xe.uniqueify(env), self.be.uniqueify(env_p))

	def rcoify(self, σ):
		nvxe, epx = self.xe.rcoify(σ)
		σp  = {**σ, **{self.var.val: epx}}
		nvbe, epb = self.be.rcoify(σp)
		nvp = {**nvxe,  **nvbe}
		return (nvp, epb)

	def expcon_e(self):
		return SEQ(
				STMT(self.var.expcon_a(), self.xe.expcon_c()),
				self.be.expcon_e()
			)

	def is_unused(self, var):
		return self.xe.is_unused(var) and self.be.is_unused(var)

	def Γ(self, γ):
		type_xe = self.xe.Γ(γ)
		type_be = self.be.Γ(γ)
		γ[self.var.val] = type_xe
		return type_be


class VAR(Expr):
	def __init__(self, var):
		self.val = var
		self.pp = f"{self.val}"
		self.str = f"VAR('{self.val}')"

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
		return VAR(self.val + '.' + str(env[self.val]))

	def rcoify(self, σ):
		return ({}, σ[self.val] if self.val in σ else self)

	def expcon_a(self):
		return cVAR(self.val)

	def expcon_e(self):
		return RET(self.expcon_a())

	def is_unused(self, var):
		return not self.val == var.val

	def Γ(self, γ):
		return γ[self.val]

class NUM(Expr, S64):
	def __init__(self, num):
		self.num = num
		self.pp = f"{self.num}"
		self.str = f"NUM({self.num})"

	def is_num(self):
		return True

	def is_leaf(self):
		return True

	def is_simp(self, env):
		return True

	def interp(self, env, db, inp):
		return self.num

	def rcoify(self, σ):
		return ({}, self)

	def expcon_a(self):
		return cNUM(self.num)

	def expcon_e(self):
		return RET(self.expcon_a())

	def is_unused(self, var):
		return True

	def Γ(self, γ):
		return S64

class READ(Expr, S64):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self):
		self.pp = "(read)"
		self.str = "READ()"

	def is_leaf(self):
		return True

	def interp(self, env, db, inp):
		if db:
			if inp:
				# running opt could cut read calls
				# which could raise off test results
				# this flag make read always return inp
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

	def rcoify(self, σ):
		new_var = VAR(get_unq_var()) 
		nv = {new_var.val: READ()}
		return (nv, new_var)

	def expcon_c(self):
		return cREAD()

	def is_unused(self, var):
		return True

	def Γ(self, γ):
		return S64

class NEG(Expr, S64):
	def __init__(self, e):
		self.expr = e
		self.pp = f"(- {self.expr})"
		self.str = f"NEG({self.expr.str})"

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

	def rcoify(self, σ):
		nvp, ep = self.expr.rcoify(σ)
		new_var = VAR(get_unq_var())
		nv = {new_var.val: NEG(ep)}
		return ({**nvp, **nv}, new_var)

	def expcon_c(self):
		return cNEG(self.expr.expcon_a())

	def is_unused(self, var):
		return self.expr.is_unused(var)

	def Γ(self, γ):
		type_e = self.expr.Γ(γ)
		if type_e != S64:
			print('TypeError: expected s64')
			raise TypeError
		return S64

class ADD(Expr, S64):
	def __init__(self, e1, e2):
		self.lhs, self.rhs = e1, e2
		self.pp = f"(+ {self.lhs} {self.rhs})"
		self.str = f"ADD({self.lhs.str}, {self.rhs.str})"

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

	def rcoify(self, σ):
		nvl, epl = self.lhs.rcoify(σ)
		nvr, epr = self.rhs.rcoify(σ)
		new_var = VAR(get_unq_var())
		nvp  = {**nvl,  **nvr}
		nv = {new_var.val: ADD(epl, epr)}
		return ({**nvp, **nv}, new_var)

	def expcon_c(self):
		return cADD(self.lhs.expcon_a(), self.rhs.expcon_a())

	def is_unused(self, var):
		return self.lhs.is_unused(var) and self.rhs.is_unused(var)

	def Γ(self, γ):
		type_l = self.lhs.Γ(γ)
		type_r = self.rhs.Γ(γ)
		if type_r != S64 or type_l != S64:
			print('TypeError: expected s64')
			raise TypeError
		return S64


class P:
	def __init__(self, e):
		self.expr = e
		self.pp = f"(program () {e}\n)"
		self.str = f"P({e.str})"

	def pprint(self):
		print(self.pp)

	def interp(self, db=False, reset=False, inp=0):
		global RAND
		if reset:
			READ._db_cnt = RAND
		ans = self.expr.interp({}, db, inp)
		return ans

	def opt(self):
		# running unqify before opt simplifies the opt code
		# while retaining optimal output
		return P(self.expr.uniqueify({}).opt({}))

	def uniqueify(self):
		return P(self.expr.uniqueify({}))

	def rcoify(self):
		if is_rco_form(self.expr):
			return P(self.expr)
		global rco_cnt
		rco_cnt = -1
		def LETify(env):
			if not env:
				# empty new variable list so already rco-ed
				return e
			# py3.7+ keys are stored in order added
			k = next(iter(env))
			if len(env) == 1:
				return LET(VAR(k), env[k], VAR(k))
			return LET(VAR(k), env.pop(k), LETify(env))
		nv, e = self.expr.rcoify({})
		return P(LETify(nv))

	def expcon(self):
		return C({'locals': []}, {'body': self.expr.expcon_e()})

	def to_c(self, opt=0):
		return self.opt().rcoify().expcon() if opt else \
			   self.uniqueify().rcoify().expcon()

	def to_x(self, opt=0):
		return self.to_c(opt).uncover_locs().select()

	def to_asm(self, opt=0):
		return self.to_x(opt).assign_homes().patch_instr().main_gen()

	def to_asm_w_reg_alloc(self, opt=0, mv=0):
		return self.to_x(opt).uncover_live().allocate_regs(mv).assign_regs().patch_instr().main_gen()

	def __eq__(self, rhs):
		return self.show() == rhs.show()

def gen(f, n):
	return P(f(n))

def rand_r2(n, vs=[]):
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

def is_rco_form(e):
	if type(e) in (VAR, NUM):
		return True
	elif type(e) == LET:
		return is_rco_form(e.be) and is_rco_form_c(e.xe)
	return False

def is_rco_form_c(c):
	if  type(c) in (READ, NEG, ADD):
		if type(c) == NEG:
			return is_rco_form_a(c.expr)
		elif type(c) == ADD:
			return is_rco_form_a(c.lhs) and is_rco_form_a(c.rhs)
		return True
	return False

def is_rco_form_a(a):
	if type(a) in (NUM, VAR):
		return True
	return False
