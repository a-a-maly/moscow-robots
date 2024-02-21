import sys


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
	"rtow" : (1, "mr.tow()"), # for Tower

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
	"<rfwd>" : (5, "mr.can_step_forward()"), #for Mover
	"<!rfwd>" : (5, "not mr.can_step_forward()"), #for Mover

	"<rcnor>" : (5, "mr.cell_normal()"),
	"<!rcnor>" : (5, "not mr.cell_normal()"),
	"<rcbro>" : (5, "mr.cell_broken()"),
	"<!rcbro>" : (5, "not mr.cell_broken()"),
	"<rcfix>" : (5, "mr.cell_fixed()"),
	"<!rcfix>" : (5, "not mr.cell_fixed()"),

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
	"[rfwd]" : (6, "mr.can_step_forward()"), #for Mover
	"[!rfwd]" : (6, "not mr.can_step_forward()"), #for Mover

	"[rcnor]" : (6, "mr.cell_normal()"),
	"[!rcnor]" : (6, "not mr.cell_normal()"),
	"[rcbro]" : (6, "mr.cell_broken()"),
	"[!rcbro]" : (6, "not mr.cell_broken()"),
	"[rcfix]" : (6, "mr.cell_fixed()"),
	"[!rcfix]" : (6, "not mr.cell_fixed()"),
}

tab_string = "    "

def compile_section(lines):
	stack = []
	stack.append((-1, 1))

	for l in lines:
		qb = False
		ls = len(l)
		for i in range(ls):
			ci = l[i]
			if not ci in commands:
				print("Unknown symbol", i, ord(ci), file=sys.stderr)
				ci = "."
			cci = commands[ci]
			if cci[0] == 0:
				continue
			if not qb:
				while stack[-1][0] >= i:
					stack.pop()
					assert stack
				qb = True

			print(tab_string * stack[-1][1], end='');

			if cci[0] == 1 or cci[0] == 3:
				print(cci[1])

			elif cci[0] == 2: # fixed repeaters
				print("for _ in range(" + str(cci[1]) + "):")
				stack.append((i, stack[-1][1] + 1))

			elif cci[0] == 4: # dynamic repeaters (pitcher and memory)
				print("for _ in range(" + cci[1] + "):")
				stack.append((i, stack[-1][1] + 1))

			elif cci[0] == 5: # if conditionals
				print("if "+ cci[1] + ":")
				stack.append((i, stack[-1][1] + 1))

			elif cci[0] == 6: # while conditionals
				print("while "+ cci[1] + ":")
				stack.append((i, stack[-1][1] + 1))

		pass # for i in range(ls)
	pass # for l in lines


def precompile_program():
	res = [None] * 5
	for i in range(5):
		res[i] = list()

	main_section = 0
	cur_section = 0
	cur_skip = True

	for l in sys.stdin:
		lw = l.rstrip().split()
		while lw and (lw[-1] == "_"):
			lw.pop()
		ls = len(lw)

		if ls == 0:
			cur_skip = True
			continue

		if cur_skip and (ls == 1) and (lw[0] in commands) and (commands[lw[0]][0] == 3):
			# selecting another section
			cur_section = ord(lw[0][0]) - ord('@')
			print("Section " + str(i) + " selected.", file=sys.stderr);
			if main_section == 0:
				main_section = cur_section
			continue
		cur_skip = False
		res[cur_section].append(lw)
	if (not res[0]) and (main_section > 0):
		res[0].append([chr(ord('@') + main_section)])
	return res


def main():
	codes = precompile_program()
	cn = len(codes)
	print("import MoscowRobots as mr")
	print()
	print("pitcher = 0")
	print("memory = 0")
	print("fl0 = False")
	print("fl1 = False")
	print()

	for i in range(cn):
		sname = commands[chr(ord('@') + i)][1]
		print("def " + sname + ":")
#		if i == 0:
#			print(tab_string + "(pitcher, memory) = (0, 0)")
#			print(tab_string + "(fl0, fl1) = (False, False)")
		compile_section(codes[i])
		print("    pass\n")
	print("proc_main()")


main()
