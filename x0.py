from rand import RAND

class xARG:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, ms, db, inp):
		return self

class xNUM(xARG):
	def __init__(self, num):
		self.num = num
		self.str = f"${self.num}"

	def __add__(self, op):
		return xNUM(self.num + op.num)

	def __sub__(self, op):
		return xNUM(self.num - op.num)

	def __eq__(self, op):
		return self.num == op.num

	def __neg__(self):
		return xNUM(-self.num)

class register(xARG):
	def __init__(self, name):
		self.name = name
		self.str = f"%{self.name}"

class DREF(xARG):
	def __init__(self, reg, offset=0):
		self.reg = reg
		self.offset = offset
		self.str = f"{self.reg}({self.offset})" if offset > 0 else f"({self.reg})"

	def interp(self, ms, db, inp):
		val = ms[self.reg] + xNUM(self.offset)
		return ms.getdefault(val, xNUM(0))

class xVAR(xARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"


# x86_64 register set
rsp = register("rsi")
rbp = register("rbi")
rax = register("rax")
rbx = register("rbx")
rcx = register("rcx")
rdx = register("rdx")
rsi = register("rsi")
rdi = register("rdi")
r8 = register("r8")
r9 = register("r9")
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

	def interp(self, ms, db, inp):
		pass

class xADD(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"addq {self.src} {self.dest}"

	def interp(self, ms, db, inp):
		val =  self.dest.interp(ms, db, inp)
		if type(self.src) == xNUM and type(self.dest) != xNUM:
			 ms[val] = self.src + ms[val]
		else:
			ms[val] = ms[self.src] + ms[val]
		return ms

class xSUB(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"subq {self.src} {self.dest}"

	def interp(self, ms, db, inp):
		val =  self.dest.interp(ms, db, inp)
		if type(self.src) == xNUM and type(self.dest) != xNUM:
			 ms[val] = ms[val] - self.src
		else:
			ms[val] = ms[val] - ms[self.src]
		return ms

class MOV(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"movq {self.src} {self.dest}"

	def interp(self, ms, db, inp):
		ms[self.dest.interp(ms, db, inp)] = self.src.interp(ms, db, inp)
		return ms

class xRET(INSTR):
	def __init__(self):
		self.str = "retq"

	def interp(self, ms, db, inp):
		print(ms[rax])
		return ms

class xNEG(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"negq {self.src}"

	def interp(self, ms, db, inp):
		ms[self.src] = -ms[self.src]
		return ms

class CALL(INSTR):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self, label):
		self.label = label
		self.str = f"callq {self.label}"

	def interp(self, ms, db, inp):
		if self.label == "read_int":
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

	def interp(self, ms, db, inp):
		return ms[self.label].interp(ms, db, inp)

class PUSH(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"pushq {self.src}"

	def interp(self, ms, db, inp):
		ms[rsp] = ms[rsp] - 8
		ms[DREF(rsp).interp(ms, db, inp)]  = ms[self.src]
		return ms

class POP(INSTR):
	def __init__(self, src):
		self.dest = dest 
		self.str = f"popq {self.dest}"

	def interp(self, ms, db, inp):
		ms[self.dest]  = ms[DREF(rsp).interp(ms, db, inp)]
		ms[rsp] = ms[rsp] + 8
		return ms



class BLCK:
	def __init__(self, info, instr):
		self.info = info
		# a list of INSTR objects
		self.instr = instr

	def interp(self, ms, db, inp):
		if not self.instr:
			pass
		for ins in self.instr:
			ms = ins.interp(ms, db, inp)
		return ms

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
		# ms := (reg -> num) x (num(addr) -> num) x
		#       (var -> num) x (label -> block)
		global RAND
		if reset:
			CALL._db_cnt = RAND
		return  self.ms["_main"].interp(self.ms, db, inp)

	def print(self):
		print('.section    __TEXT,__text')
		print('.globl _main')
		for k, v in self.ms:
			if k in init_ms: continue
			print(f'{k}:')
			self.ms[k].pprint()
