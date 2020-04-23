from rand import RAND
from flags import MAC_OS

import networkx as nx

class xARG:
	def __init__(self):
		pass

	def __repr__(self):
		return self.str

	def assign(self, σ):
		return self

	def w(self):
		return set()

	def r(self):
		return set()


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

	def interp_d(self, ms=0, db=0, inp=0):
		return self.num

class register(xARG):
	def __init__(self, name):
		self.name = name
		self.str = f"%{self.name}"

	def interp_a(self, ms, db, inp):
		return ms[self]

	def interp_d(self, ms=0, db=0, inp=0):
		return self

	def w(self):
		if self in caller_sav_reg:
			return set([self])
		return set()

	def r(self):
		if self in caller_sav_reg:
			return set([self])
		return set()

class DREF(xARG):
	def __init__(self, reg, offset=0):
		self.reg = reg
		self.offset = offset
		self.str = f"{self.offset}({self.reg})" if offset != 0 else f"({self.reg})"

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

	def interp_d(self, ms=0, db=0, inp=0):
		return self.name

	def assign(self, σ):
		return σ[self.name]

	def w(self):
		return set([self.name])

	def r(self):
		return set([self.name])



# x86_64 register set
rsp = register("rsp")
rbp = register("rbp")
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

caller_sav_reg = [
	rax, rdx, rcx, rsi,
	rdi, r8, r9, r10, r11
]

regs = [
	rax, rbx, rcx, rdx, rsi, rdi,
	r8, r9, r10, r11, r12, r13, r14, r15
]

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

	def W(self):
		return set()

	def R(self):
		return set()

	def build_intf_edges(self, live_vars):
		return []

	def build_mov_edges(self):
		return []

class xADD(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"addq {self.src}, {self.dest}"

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

	def W(self):
		return self.dest.w()

	def R(self):
		return self.src.r() | self.dest.r()

	def build_intf_edges(self, live_vars):
		if type(self.dest) == DREF:
			return []
		intf_vars = []
		for v in live_vars:
			if v == self.dest.interp_d():
				continue
			intf_vars += [(self.dest.interp_d(), v)]
		return intf_vars


class xSUB(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"subq {self.src}, {self.dest}"

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

	def W(self):
		return self.dest.w()

	def R(self):
		return self.src.r() | self.dest.r()

	def build_intf_edges(self, live_vars):
		if type(self.dest) == DREF:
			return []
		intf_vars = []
		for v in live_vars:
			if v == self.dest.interp_d():
				continue
			intf_vars += [(self.dest.interp_d(), v)]
		return intf_vars


class MOV(INSTR):
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		self.str = f"movq {self.src}, {self.dest}"

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
		if type(self.src) == type(self.dest) and self.src == self.dest:
			return []
		return [self]

	def W(self):
		return self.dest.w()

	def R(self):
		return self.src.r()

	def build_intf_edges(self, live_vars):
		if type(self.dest) == DREF:
			return []
		intf_vars = []
		for v in live_vars:
			if v in [self.dest.interp_d(), self.src.interp_d()]:
				continue
			intf_vars += [(self.dest.interp_d(), v)]
		return intf_vars

	def build_mov_edges(self):
		if type(self.dest) == DREF or \
		   type(self.src) == xNUM:
			return []
		return [(self.src.interp_d(), self.dest.interp_d())]

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

	def W(self):
		return self.src.w()

	def R(self):
		return self.src.r()

	def build_intf_edges(self, live_vars):
		if type(self.src) == DREF:
			return []
		intf_vars = []
		for v in live_vars:
			if v == self.src.interp_d():
				continue
			intf_vars += [(self.src.interp_d(), v)]
		return intf_vars

class CALL(INSTR):
	_db_cnt = RAND
	_rd_cnt = 0

	def __init__(self, label):
		self.label = label if not MAC_OS else '_'+label
		self.str = f"callq {self.label}"

	def interp_e(self, ms, db, inp):
		if self.label == "read_int" or self.label == "_read_int":
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

	def build_intf_edges(self, live_vars):
		intf_vars = []
		for r in caller_sav_reg:
			for v in live_vars:
				intf_vars += [(r, v)]
		return intf_vars

class JMP(INSTR):
	def __init__(self, label):
		self.label = label if not MAC_OS else '_'+label
		self.str = f"jmp {self.label}"

	def interp_e(self, ms, db, inp):
		label = self.label[1:] if MAC_OS else self.label
		return ms[label].interp(ms, db, inp)

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

	def W(self):
		return self.src.w()

	def build_intf_edges(self, live_vars):
		if type(self.dest) == DREF:
			return []
		intf_vars = []
		for v in live_vars:
			if v == self.src.interp_d():
				continue
			intf_vars += [(self.src.interp_d(), v)]
		return intf_vars



class BLCK:
	def __init__(self, instr):
		# a list of INSTR objects
		self.instr = instr

	def interp(self, ms, db, inp, info={}):
		live_vars = set()
		for k in range(len(self.instr)):
			ms = self.instr[k].interp_e(ms, db, inp)
			if info:
				live_inf = info['liveness']
				dead_vars = live_vars - live_inf[k]
				for var in dead_vars:
					del ms[var]
		return ms

	def assign(self, σ):
		ni = []
		for ins in self.instr:
			ni += ins.assign(σ)
		return BLCK(ni)

	def patch(self):
		ni = []
		for ins in self.instr:
			ni += ins.patch()
		return BLCK(ni)

	def pprint(self):
		for ins in self.instr:
			print(ins)

	def to_str(self):
		s = ""
		for ins in self.instr:
			s += ins.str + "\n"
		return s

	def uncover_live(self):
		liveness = {}
		liv_vars = set()
		for k in reversed(range(len(self.instr))):
			if k == len(self.instr)-1:
				liveness[k] = liv_vars
			else:
				instr = self.instr[k+1]
				liv_vars = (liv_vars - instr.W()) | instr.R() 
				liveness[k] = liv_vars
		return liveness

	# def liv_befor(self, k):
	# 	instr = self.instr[k]
	# 	return (self.liv_after(k) - instr.W()) | instr.R()

	# def liv_after(self, k):
	# 	return set() if k == len(self.instr)-1 else self.liv_befor(k+1)

	def build_intf_graph(self, info):
		g = nx.Graph()
		g.add_nodes_from(regs)
		g.add_nodes_from(info['locals'])

		for k in range(len(self.instr)):
			live_vars = info['liveness'][k]
			g.add_edges_from(self.instr[k].build_intf_edges(live_vars))
		return nx.to_dict_of_lists(g)

	def build_mov_graph(self, info):
		g = nx.Graph()
		g.add_nodes_from(regs)
		g.add_nodes_from(info['locals'])

		for k in range(len(self.instr)):
			g.add_edges_from(self.instr[k].build_mov_edges())
		return nx.to_dict_of_lists(g)


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

	def interp(self, db=False, reset=False, inp=0, gc=False):
		# ms := (reg -> num) x (addr(num) -> num) x
		#       (var -> num) x (label(str) -> block)
		global RAND
		if reset:
			CALL._db_cnt = RAND
		return  self.ms["start"].interp(self.ms, db, inp, self.info) if gc else \
				self.ms["start"].interp(self.ms, db, inp)

	def assign_homes(self):
		n = len(self.info['locals'])
		vc = (n if n%2==0 else n+1)

		if 'allocs' in self.info:
			σ = self.info['allocs'].copy()
		else:
			σ = {}

		for i in range(n):
			σ[self.info['locals'][i]] = DREF(rbp, -8*(i+1))
		body_blck = self.ms['start'].assign(σ)

		start_blck = BLCK(
			[
				PUSH(rbp),
				MOV(rsp, rbp),
				xSUB(xNUM(vc*8), rsp),
				JMP('body')
			]
		)
		end_blck = BLCK(
			[
				xADD(xNUM(vc*8), rsp),
				POP(rbp),
				xRET()
			]
		)
		new_ms = {
			'start': start_blck,
			'end': end_blck,
			'body': body_blck
		}
		return X(self.info, new_ms)

	def patch_instr(self):
		new_ms = self.ms.copy()
		body_blck = new_ms['body'].patch()
		new_ms['body'] = body_blck
		return X(self.info, new_ms)

	def main_gen(self):
		main_blck = BLCK(
			[
				PUSH(rbp),
				MOV(rsp, rbp),
				CALL('start'),
				MOV(rax, rdi),
				CALL('print_int'),
				POP(rbp),
				xRET()
			]
		)
		new_ms = self.ms.copy()
		new_ms['main'] = main_blck
		return X(self.info, new_ms)

	def uncover_live(self):
		live_set  = self.ms['start'].uncover_live()
		new_inf = {**self.info,  **{'liveness':  live_set}}
		return X(new_inf, self.ms)

	def intf_graph(self):
		intf_map = self.ms['start'].build_intf_graph(self.info)
		# new_inf = {**self.info, **{'interference': intf_map}}
		return intf_map

	def mov_graph(self):
		mov_map = self.ms['start'].build_mov_graph(self.info)
		# new_inf = {**self.info, **{'interference': intf_map}}
		return mov_map

	def allocate_regs(self, mv=0):
		i_graph = self.intf_graph()
		mov_graph = self.mov_graph()

		def get_adj_color(v, s):
			sat = set()
			if v not in s:
				return sat
			for u in s[v]:
				if u in color_graph:
					sat |= set([color_graph[u]])
			return sat

		def get_color_w_mv(v):
			sat = get_adj_color(v, i_graph)
			m = get_adj_color(v, mov_graph)
			look_first = m - sat
			return min(look_first) if look_first else \
				   min(aval_colors) if aval_colors else []


		w = [(i, len(i_graph[i])) for i in i_graph.keys() if i_graph[i]]
		# sort w based on saturation
		w = sorted(w, key=lambda x: x[1])
		color_graph = {}
		v_allocs = {}
		for r in range(len(regs)):
			# give regs colors
			color_graph[regs[r]] = r
		# color the graph
		while w:
			v, n = w.pop()
			if type(v) == register:
				continue
			aval_colors = [c for c in range(len(regs))]
			for u in i_graph[v]:
				if u in color_graph and color_graph[u] in aval_colors:
					aval_colors.remove(color_graph[u])
			# if move-biasing enabled
			color_graph[v] = get_color_w_mv(v) if mv else \
							 min(aval_colors) if aval_colors else []
			# if a reg was assigned
			if color_graph[v] != []: 
				v_allocs[v] = regs[color_graph[v]]
				# remove this var from locals, any left will be allocated stack space
				if v in self.info['locals']:
					self.info['locals'].remove(v)
		new_inf = {**self.info, **{'allocs': v_allocs}}
		return X(new_inf, self.ms)

	def assign_regs(self):
		n = len(self.info['locals'])
		vc = (n if n%2==0 else n+1)

		σ = self.info['allocs'].copy()

		for i in range(n):
			σ[self.info['locals'][i]] = DREF(rbp, -8*(i+1))
		body_blck = self.ms['start'].assign(σ)

		start_blck = BLCK(
			[
				PUSH(rbp),
				MOV(rsp, rbp),
				xSUB(xNUM(vc*8), rsp),
				JMP('body')
			]
		)
		end_blck = BLCK(
			[
				xADD(xNUM(vc*8), rsp),
				POP(rbp),
				xRET()
			]
		)
		new_ms = {
			'start': start_blck,
			'end': end_blck,
			'body': body_blck
		}
		return X(self.info, new_ms)

	def pprint(self):
		print('.data')
		print('.text')
		lmain = '_main' if MAC_OS else 'main'
		print(f'.globl {lmain}')
		for k in ['start', 'body', 'end', 'main']:
			if k in self.ms:
				l = k if not MAC_OS else ('_' + k)
				print(f'\n{l}:')
				self.ms[k].pprint()
