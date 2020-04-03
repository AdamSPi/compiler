from rand import RAND

class xARG:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def assign(self, σ):
		return self


class xNUM(xARG):
	def __init__(self, num):
		self.num = num
		self.str = f"${self.num}"

	def __add__(self, op):
		if type(op) == int:
			return xNUM(self.num + op)
		return xNUM(self.num + op.num)

	def __sub__(self, op):
		if type(op) == int:
			return xNUM(self.num - op)
		return xNUM(self.num - op.num)

	def __eq__(self, op):
		if type(op) == int:
			return self.num == op
		return self.num == op.num 

	def __neg__(self):
		return xNUM(-self.num)

	def interp_a(self, ms, db, inp):
		return self

	def interp_d(self, ms, db, inp):
		return self.num

class register(xARG):
	def __init__(self, name):
		self.name = name
		self.str = f"%{self.name}"

	def interp_a(self, ms, db, inp):
		return ms[self]

	def interp_d(self, ms, db, inp):
		return self

class DREF(xARG):
	def __init__(self, reg, offset=0):
		self.reg = reg
		self.offset = offset
		self.str = f"{self.reg}({self.offset})" if offset > 0 else f"({self.reg})"

	def interp_a(self, ms, db, inp):
		val = ms[self.reg] + self.offset
		return ms[val.num]

	def interp_d(self, ms, db, inp):
		val = ms[self.reg] + self.offset
		return val.num

class xVAR(xARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"

	def interp_a(self, ms, db, inp):
		return ms[self.name]

	def interp_d(self, ms, db, inp):
		return self.name

	def assign(self, σ):
		return σ[self.name]



# x86_64 register set
rsp = register("rsi")
rbp = register("rbi")
rax = register("rax")
rbx = register("rbx")
rcx = register("rcx")
rdx = register("rdx")
rsi = register("rsi")
rdi = register("rdi")
r8  = register("r8")
r9  = register("r9")
r10 = register("r10")
r11 = register("r11")
r12 = register("r12")
r13 = register("r13")
r14 = register("r14")
r15 = register("r15")


class INSTR:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp_e(self, ms, db, inp):
		pass

	def assign(self, σ):
		return [self]

	def patch(self):
		return [self]

class xADD(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"addq {self.src} {self.dest}"

	def interp_e(self, ms, db, inp):
		val =  self.dest.interp_d(ms, db, inp)
		ms[val] = self.src.interp_a(ms, db, inp) + ms[val]
		return ms

	def assign(self, σ):
		return [xADD(self.src.assign(σ), self.dest.assign(σ))]

	def patch(self):
		tmp_reg = rax
		if type(self.src) == DREF and type(self.dest) == DREF:
			return [\
				MOV(self.src, tmp_reg),
				xADD(tmp_reg, self.dest)
			]
		return [self]


class xSUB(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"subq {self.src} {self.dest}"

	def interp_e(self, ms, db, inp):
		val =  self.dest.interp_d(ms, db, inp)
		ms[val] = ms[val] - self.src.interp_a(ms, db, inp)
		return ms

	def assign(self, σ):
		return [xSUB(self.src.assign(σ), self.dest.assign(σ))]

	def patch(self):
		tmp_reg = rax
		if type(self.src) == DREF and type(self.dest) == DREF:
			return [\
				MOV(self.src, tmp_reg),
				xSUB(tmp_reg, self.dest)
			]
		return [self]


class MOV(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"movq {self.src} {self.dest}"

	def interp_e(self, ms, db, inp):
		val = self.dest.interp_d(ms, db, inp)
		ms[val] = self.src.interp_a(ms, db, inp)
		return ms

	def assign(self, σ):
		return [MOV(self.src.assign(σ), self.dest.assign(σ))]

	def patch(self):
		tmp_reg = rax
		if type(self.src) == DREF and type(self.dest) == DREF:
			return [\
				MOV(self.src, tmp_reg),
				MOV(tmp_reg, self.dest)
			]
		return [self]

class xRET(INSTR):
	def __init__(self):
		self.str = "retq"

	def interp_e(self, ms, db, inp):
		print(ms[rax])
		return ms

class xNEG(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"negq {self.src}"

	def interp_e(self, ms, db, inp):
		val = self.src.interp_d(ms, db, inp)
		ms[val] = - self.src.interp_a(ms, db, inp)
		return ms

	def assign(self, σ):
		return [xNEG(self.src.assign(σ))]

class CALL(INSTR):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self, label):
		self.label = label
		self.str = f"callq {self.label}"

	def interp_e(self, ms, db, inp):
		if self.label == "_read_int":
			if db:
				if inp:
					ms[rax] = xNUM(inp)
				else:
					ms[rax] = xNUM(CALL._db_cnt)
					CALL._db_cnt -= 1
			else:
				ms[rax] = xNUM(int(input("Input an integer: ",)))
			CALL._rd_cnt += 1
			return ms

class JMP(INSTR):
	def __init__(self, label):
		self.label = label
		self.str = f"jmp {self.label}"

	def interp_e(self, ms, db, inp):
		return ms[self.label].interp(ms, db, inp)

class PUSH(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"pushq {self.src}"

	def interp_e(self, ms, db, inp):
		ms[rsp] = ms[rsp] - xNUM(8)
		val = DREF(rsp).interp_d(ms, db, inp)
		ms[val]  = self.src.interp_a(ms, db, inp)
		return ms

	def assign(self, σ):
		return [PUSH(self.src.assign(σ))]

class POP(INSTR):
	def __init__(self, src):
		self.src = src 
		self.str = f"popq {self.src}"

	def interp_e(self, ms, db, inp):
		val = self.src.interp_d(ms, db, inp)
		ms[val] = DREF(rsp).interp_a(ms, db, inp)
		ms[rsp] = ms[rsp] + xNUM(8)
		return ms

	def assign(self, σ):
		return [POP(self.src.assign(σ))]



class BLCK:
	def __init__(self, info, instr):
		self.info = info
		# a list of INSTR objects
		self.instr = instr

	def interp(self, ms, db, inp):
		for ins in self.instr:
			ms = ins.interp_e(ms, db, inp)
		return ms

	def assign(self, info, σ):
		ni = []
		for ins in self.instr:
			ni += ins.assign(σ)
		return BLCK(info, ni)

	def patch(self, info):
		ni = []
		for ins in self.instr:
			ni += ins.patch()
		return BLCK(info, ni)

	def pprint(self):
		for ins in self.instr:
			print(ins)

init_ms = {
	rsp: xNUM(0),
	rbp: xNUM(0),
	rax: xNUM(0),
	rbx: xNUM(0),
	rcx: xNUM(0),
	rdx: xNUM(0),
	rsi: xNUM(0),
	rdi: xNUM(0),
	r8 : xNUM(0),
	r9 : xNUM(0),
	r10: xNUM(0),
	r11: xNUM(0),
	r12: xNUM(0),
	r13: xNUM(0),
	r14: xNUM(0),
	r15: xNUM(0),
}

class X:
	def __init__(self, info, ms):
		self.info = info
		# a dict of labels to blocks
		self.ms = {**init_ms, **ms}

	def interp(self, db=False, reset=False, inp=0):
		# ms := (reg -> num) x (addr(num) -> num) x
		#       (var -> num) x (label(str) -> block)
		global RAND
		if reset:
			CALL._db_cnt = RAND
		return  self.ms["_main"].interp(self.ms, db, inp)

	def assign_homes(self):
		n = len(self.info['locals'])
		vc = (n if n%2==0 else n+1) * 8

		σ = {}
		for i in range(1,n+1):
			σ[self.info['locals'][i-1]] = DREF(rsp, 8*i)
		new_main = self.ms['_main'].assign({}, σ)

		begin_blck = BLCK(
			{},
			[
				PUSH(rbp),
				MOV(rsp, rbp),
				xSUB(xNUM(vc), rsp),
				JMP('_begin')
			]
		)
		end_blck = BLCK(
			{},
			[
				xADD(xNUM(vc), rsp),
				POP(rbp),
				xRET()
			]
		)
		new_ms = {
			'_main': begin_blck,
			'_end': end_blck,
			'_begin': new_main
		}
		return X(self.info, new_ms)

	def patch_instr(self):
		new_ms = self.ms.copy()
		new_main = new_ms['_begin'].patch({})
		new_ms['_begin'] = new_main
		return X(self.info, new_ms)

	def pprint(self):
		print('.section    __TEXT,__text')
		print('.globl _main')
		for k in (self.ms.keys() - init_ms.keys()):
			print(f'{k}:')
			self.ms[k].pprint()
