
class ARG:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def interp(self, ms):
		return self

class NUM(ARG):
	def __init__(self, num):
		self.num = num
		self.str = f"${self.num}"

	def __add__(self, op):
		return NUM(self.num + op.num)

	def __sub__(self, op):
		return NUM(self.num - op.num)

	def __neg__(self):
		return NUM(-self.num)

class register(ARG):
	def __init__(self, name):
		self.name = name
		self.str = f"%{self.name}"

class DREF(ARG):
	def __init__(self, reg, offset):
		self.reg = reg
		self.offset = offset
		self.str = f"{self.reg}({self.offset})"

	def interp(self, ms):
		return ms[self.reg] + NUM(self.offset)

class VAR(ARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"


# x86_64 register set
rsi = register("rsi")
rbi = register("rbi")
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

	def interp(self, ms):
		pass

class ADD(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"addq {self.src} {self.dest}"

	def interp(self, ms):
		ms[self.dst] = ms[self.src] + ms[self.dst]
		return ms

class SUB(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"subq {self.src} {self.dest}"

	def interp(self, ms):
		ms[self.dst] = ms[self.src] - ms[self.dst]
		return ms

class MOV(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"movq {self.src} {self.dest}"

	def interp(self, ms):
		ms[self.dst] = ms[self.src]
		return ms

class RET(INSTR):
	def __init__(self):
		self.str = "retq"

	def interp(self, ms):
		print(ms[rax])
		return ms

class NEG(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"negq {self.src}"

	def interp(self, ms):
		ms[self.src] = -ms[self.src]
		return ms

class CALL(INSTR):
	def __init__(self, label):
		self.label = label
		self.str = f"callq {self.label.name}"

	def interp(ms):
		if self.label == 'read_int':
			ms[rax] = NUM(int(input("Input an integer: ",)))

class JMP(INSTR):
	def __init__(self, label):
		self.label = label
		self.str = f"jmp {self.label.name}"

	def interp(self, ms):
		return ms[self.label].interp(ms)

class PUSH(INSTR):
	def __init__(self, src):
		self.src = src
		self.str = f"pushq {self.src}"

	def interp(self, ms):
		ms[rsp] = ms[rsp] - 8
		ms[DREF(rsp, 0).interp(ms)]  = ms[self.src]
		return ms

class POP(INSTR):
	def __init__(self, src):
		self.dest = dest 
		self.str = f"popq {self.dest}"

	def interp(self, ms):
		ms[self.dest]  = ms[DREF(rsp, 0).interp(ms)]
		ms[rsp] = ms[rsp] + 8
		return ms




class LABEL:
	def __init__(self, name):
		self.name = name

class BLCK:
	def __init__(self, info, instr):
		self.info = info
		# a list of INSTR objects
		self.instr = instr

	def interp(self, ms):
		if not self.instr:
			pass
		for ins in self.instr:
			ms = ins.interp(ms)
		return ms




class P:
	def __init__(self):
		self.info = {}
		# a dict of labels to blocks
		self.map = {}

	def interp(self, ms):
		# ms := (reg -> num) x (num(addr) -> num) x
		#       (var -> num) x (label -> block)
		return  ms[LABEL('main')].interp(ms)
