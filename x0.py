


class ARG:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

class NUM(ARG):
	def __init__(self, num):
		self.num = num
		self.str = f"${self.num}"

class REG(ARG):
	def __init__(self, rn):
		self.rn = rn
		self.str = f"%{self.rn}"

class REF(ARG):
	def __init__(self, rn, offset):
		self.rn = rn
		self.offset = offset
		self.str = f"%{self.rn}({self.offset})"

class VAR(ARG):
	def __init__(self, n):
		self.name = n
		self.str = f"{self.name}"



class INSTR:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

class ADD(INSTR):
	def __init__(self, arg1, arg2):
		self.arg1 = arg1
		self.arg2 = arg2
		self.str = f"addq {self.arg1} {self.arg2}"

class SUB(INSTR):
	def __init__(self, arg1, arg2):
		self.arg1 = arg1
		self.arg2 = arg2
		self.str = f"subq {self.arg1} {self.arg2}"

class MOV(INSTR):
	def __init__(self, arg1, arg2):
		self.arg1 = arg1
		self.arg2 = arg2
		self.str = f"movq {self.arg1} {self.arg2}"

class RET(INSTR):
	def __init__(self):
		self.str = "retq"

class NEG(INSTR):
	def __init__(self, arg1):
		self.arg1 = arg1
		self.str = f"negq {self.arg1}"

class CALL(INSTR):
	def __init__(self, label):
		self.label = label
		self.str = f"callq {self.label.name}"

class JMP(INSTR):
	def __init__(self, label):
		self.label = label
		self.str = f"jmp {self.label.name}"

class PUSH(INSTR):
	def __init__(self, arg1):
		self.arg1 = arg1
		self.str = f"pushq {self.arg1}"

class POP(INSTR):
	def __init__(self, arg1):
		self.arg1 = arg1
		self.str = f"popq {self.arg1}"



class LABEL:
	def __init__(self, name):
		self.name = name



class BLCK:
	def __init__(self, info, instr):
		self.info = info
		# a list of INSTR objects
		self.instr = instr



class P:
	def __init__(self):
		self.info = {}
		self.map = {}
