import sys
import argparse

class Pikto2Py:

	tab_string = "    "

	commands = {
		# empty space
		"_" : (0, None),

		# actions
		"." : (1, "pass"),

		"pit0" : (1, "pitcher = 0"),
		"pit+1" : (1, "pitcher += 1"),
		"pit-1" : (1, "pitcher = max(pitcher - 1, 0)"),
		"mem0" : (1, "memory = 0"),
		"mem+p" : (1, "memory += pitcher"),
		"mem-p" : (1, "memory = max(memory - pitcher, 0)"),
		"fl0+" : (1, "fl0 = True"),
		"fl0-" : (1, "fl0 = False"),
		"fl1+" : (1, "fl1 = True"),
		"fl1-" : (1, "fl1 = False"),

		"rfwd" : (1, "mr.step_forward()"),
		"rleft" : (1, "mr.turn_left()"),
		"rright" : (1, "mr.turn_right()"),
		"rfix" : (1, "mr.fix_cell()"),

		# for Tyagun
		"rtow" : (1, "mr.tow()"),

		# for Iskun
		"rmup": (1, "mr.step_up()"),
		"rmright": (1, "mr.step_right()"),
		"rmdown": (1, "mr.step_down()"),
		"rmleft": (1, "mr.step_left()"),

		# subroutines
		"@" : (3, "proc_main()"),
		"A" : (3, "proc_A()"),
		"B" : (3, "proc_B()"),
		"C" : (3, "proc_C()"),
		"D" : (3, "proc_D()"),

		# fixed repeaters
		"(0)" : (2, 0),
		"(1)" : (2, 1),
		"(2)" : (2, 2),
		"(3)" : (2, 3),
		"(4)" : (2, 4),
		"(5)" : (2, 5),
		"(6)" : (2, 6),

		# dynamic repeaters, vars only
		"(pit)" : (4, "pitcher"),
		"(mem)" : (4, "memory"),

		# if conditionals
		"<pit>" : (5, "(pitcher > 0)"),
		"<!pit>" : (5, "(pitcher <= 0)"),
		"<mem>" : (5, "(memory > 0)"),
		"<!mem>" : (5, "(memory <= 0)"),
		"<memeq>" : (5, "(memory == pitcher)"),
		"<memne>" : (5, "(memory != pitcher)"),
		"<memlt>" : (5, "(memory < pitcher)"),
		"<memle>" : (5, "(memory <= pitcher)"),
		"<memgt>" : (5, "(memory > pitcher)"),
		"<memge>" : (5, "(memory >= pitcher)"),
		"<fl0>" : (5, "fl0"),
		"<!fl0>" : (5, "not fl0"),
		"<fl1>" : (5, "fl1"),
		"<!fl1>" : (5, "not fl1"),

		"<rclear>" : (5, "mr.path_clear()"),
		"<!rclear>" : (5, " not mr.path_clear()"),

		# for Dvigun
		"<rfwd>" : (5, "mr.can_step_forward()"),
		"<!rfwd>" : (5, "not mr.can_step_forward()"),

		"<rcnor>" : (5, "mr.cell_normal()"),
		"<!rcnor>" : (5, "not mr.cell_normal()"),
		"<rcbro>" : (5, "mr.cell_broken()"),
		"<!rcbro>" : (5, "not mr.cell_broken()"),
		"<rcfix>" : (5, "mr.cell_fixed()"),
		"<!rcfix>" : (5, "not mr.cell_fixed()"),

		# for Iskun
		"<rmup>": (5, "mr.path_clear_up()"),
		"<rmright>": (5, "mr.path_clear_right()"),
		"<rmdown>": (5, "mr.path_clear_down()"),
		"<rmleft>": (5, "mr.path_clear_left()"),
		"<!rmup>": (5, "not mr.path_clear_up()"),
		"<!rmright>": (5, "not mr.path_clear_right()"),
		"<!rmdown>": (5, "not mr.path_clear_down()"),
		"<!rmleft>": (5, "not mr.path_clear_left()"),

		# while conditionals
		"[pit]" : (6, "(pitcher > 0)"),
		"[!pit]" : (6, "(pitcher <= 0)"),
		"[mem]" : (6, "(memory > 0)"),
		"[!mem]" : (6, "(memory <= 0)"),
		"[memeq]" : (6, "(memory == pitcher)"),
		"[memne]" : (6, "(memory != pitcher)"),
		"[memlt]" : (6, "(memory < pitcher)"),
		"[memle]" : (6, "(memory <= pitcher)"),
		"[memgt]" : (6, "(memory > pitcher)"),
		"[memge]" : (6, "(memory >= pitcher)"),
		"[fl0]" : (6, "fl0"),
		"[!fl0]" : (6, "not fl0"),
		"[fl1]" : (6, "fl1"),
		"[!fl1]" : (6, "not fl1"),

		"[rclear]" : (6, "mr.path_clear()"),
		"[!rclear]" : (6, "not mr.path_clear()"),

		# for Dvigun
		"[rfwd]" : (6, "mr.can_step_forward()"),
		"[!rfwd]" : (6, "not mr.can_step_forward()"),

		"[rcnor]" : (6, "mr.cell_normal()"),
		"[!rcnor]" : (6, "not mr.cell_normal()"),
		"[rcbro]" : (6, "mr.cell_broken()"),
		"[!rcbro]" : (6, "not mr.cell_broken()"),
		"[rcfix]" : (6, "mr.cell_fixed()"),
		"[!rcfix]" : (6, "not mr.cell_fixed()"),

		# for Iskun
		"[rmup]": (6, "mr.path_clear_up()"),
		"[rmright]": (6, "mr.path_clear_right()"),
		"[rmdown]": (6, "mr.path_clear_down()"),
		"[rmleft]": (6, "mr.path_clear_left()"),
		"[!rmup]": (6, "not mr.path_clear_up()"),
		"[!rmright]": (6, "not mr.path_clear_right()"),
		"[!rmdown]": (6, "not mr.path_clear_down()"),
		"[!rmleft]": (6, "not mr.path_clear_left()"),

	}

	def __init__(self):
		pass


	#Divides program text for sections
	@classmethod
	def precompile_program(cls, lines):
		cmds = cls.commands
		res = [None] * 5
		for i in range(5):
			res[i] = list()

		main_section = 0
		cur_section = 0
		cur_skip = True

		for l in lines:
			lw = l.rstrip().split()
			while lw and (lw[-1] == "_"):
				lw.pop()
			ls = len(lw)

			if ls == 0:
				cur_skip = True
				continue

			if cur_skip and (ls == 1) and (lw[0] in cmds) and (cmds[lw[0]][0] == 3):
				# selecting another section
				cur_section = ord(lw[0][0]) - ord('@')
				print("Section " + str(cur_section) + " selected.", file=sys.stderr)
				if main_section == 0:
					main_section = cur_section
				continue
			cur_skip = False
			res[cur_section].append(lw)
		if (not res[0]) and (main_section > 0):
			res[0].append([chr(ord('@') + main_section)])
		return res

	@classmethod
	def compile_section(cls, lines, fo):
		cmds = cls.commands
		stack = []
		stack.append((-1, 1))

		for l in lines:
			qb = False
			ls = len(l)
			for i in range(ls):
				ci = l[i]
				if not ci in cmds:
					print("Unknown symbol", ci, file=sys.stderr)
					ci = "."
				cci = cmds[ci]
				if cci[0] == 0:
					continue
				if not qb:
					while stack[-1][0] >= i:
						stack.pop()
						assert stack
					qb = True

				print(cls.tab_string * stack[-1][1], end='', file = fo)

				if cci[0] == 1 or cci[0] == 3:
					print(cci[1], file = fo)

				elif cci[0] == 2: # fixed repeaters
					print("for _ in range(" + str(cci[1]) + "):", file = fo)
					stack.append((i, stack[-1][1] + 1))

				elif cci[0] == 4: # dynamic repeaters (pitcher and memory)
					print("for _ in range(" + cci[1] + "):", file = fo)
					stack.append((i, stack[-1][1] + 1))

				elif cci[0] == 5: # if conditionals
					print("if "+ cci[1] + ":", file = fo)
					stack.append((i, stack[-1][1] + 1))

				elif cci[0] == 6: # while conditionals
					print("while "+ cci[1] + ":", file = fo)
					stack.append((i, stack[-1][1] + 1))

			pass # for i in range(ls)
		pass # for l in lines

	@classmethod
	def compile_program(cls, lines, fo):
		codes = cls.precompile_program(lines)
		cn = len(codes)
		print("import moscow_robots as mrs\n", file = fo)

		for i in range(cn):
			sname = cls.commands[chr(ord('@') + i)][1]
			print("def " + sname + ":", file = fo)
			cls.compile_section(codes[i], fo)
			print(cls.tab_string + "pass\n", file = fo)

		print('with mrs.GameVertun("a.json") as mr:', file = fo)
		print(cls.tab_string + "proc_main()\n", file = fo)
		fo.flush()

	@classmethod
	def compile_file(cls, fname):
		ext = ".pikto"
		if not fname.endswith(ext):
			print("File", fname, "does not end with", ext, "skipping.", file = sys.stderr)
			return
		oname = fname[:-len(ext)] + ".py"
		lines = []
		try:
			fi = open(fname, 'rt')
			lines = fi.readlines()
			fi.close()
		except OSError as err:
			print(err, file = sys.stderr)
			return

		try:
			fo = open(oname, 'wt')
			cls.compile_program(lines, fo)
			fo.close()
		except OSError as err:
			print(err, file = sys.stderr)
			return

	@classmethod
	def compile_stdin(cls):
		lines = sys.stdin.readlines()
		cls.compile_program(lines, sys.stdout)

	@staticmethod
	def main():
		parser = argparse.ArgumentParser()
		parser.add_argument('rest', nargs = '*')
		args = parser.parse_args()

		if not args.rest:
			print("No arguments provided, compiling from stdin", file = sys.stderr)
			compile_stdin()
		else:
			for fn in args.rest:
				Pikto2Py.compile_file(fn)

if __name__ == '__main__':
	Pikto2Py.main()

# vim: set noet:
