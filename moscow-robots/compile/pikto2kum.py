import sys


commands = {
	# empty space
	"_" : (0, None),

	# actions
	"." : (1, ";"),

	"pit0" : (1, "кувшин := 0"),
	"pit+1" : (1, "кувшин := кувшин + 1"),
	"pit-1" : (1, "кувшин := imax(кувшин - 1, 0)"),
	"mem0" : (1, "память := 0"),
	"mem+p" : (1, "память := память + кувшин"),
	"mem-p" : (1, "память := imax(память - кувшин, 0)"),
	"fl0+" : (1, "флаг0 := да"),
	"fl0-" : (1, "флаг0 := нет"),
	"fl1+" : (1, "флаг1 := да"),
	"fl1-" : (1, "флаг1 := нет"),

	"rfwd" : (1, "вперед"),
	"rleft" : (1, "налево"),
	"rright" : (1, "направо"),
	"rfix" : (1, "закрасить"),
	"rtow" : (1, "тащить"), # for Tower

	# subroutines
	"@" : (3, "main"),
	"A" : (3, "A"),
	"B" : (3, "B"),
	"C" : (3, "C"),
	"D" : (3, "D"),

	# fixed repeaters
	"(0)" : (2, 0),
	"(1)" : (2, 1),
	"(2)" : (2, 2),
	"(3)" : (2, 3),
	"(4)" : (2, 4),
	"(5)" : (2, 5),
	"(6)" : (2, 6),

	# dynamic repeaters, vars only
	"(pit)" : (4, "кувшин"),
	"(mem)" : (4, "память"),

	# if conditionals
	"<pit>" : (5, "(кувшин > 0)"),
	"<!pit>" : (5, "(кувшин <= 0)"),
	"<mem>" : (5, "(память > 0)"),
	"<!mem>" : (5, "(память <= 0)"),
	"<memeq>" : (5, "(память = кувшин)"),
	"<memne>" : (5, "(память <> кувшин)"),
	"<memlt>" : (5, "(память < кувшин)"),
	"<memle>" : (5, "(память <= кувшин)"),
	"<memgt>" : (5, "(память > кувшин)"),
	"<memge>" : (5, "(память >= кувшин)"),
	"<fl0>" : (5, "флаг0"),
	"<!fl0>" : (5, "не флаг0"),
	"<fl1>" : (5, "флаг1"),
	"<!fl1>" : (5, "не флаг1"),

	"<rclear>" : (5, "впереди свободно"),
	"<!rclear>" : (5, "не впереди свободно"),
	"<rfwd>" : (5, "можно шагнуть"), #for Mover
	"<!rfwd>" : (5, "можно не шагнуть"), #for Mover

	"<rcnor>" : (5, "клетка голубая"),
	"<!rcnor>" : (5, "клетка не голубая"),
	"<rcbro>" : (5, "клетка серая"),
	"<!rcbro>" : (5, "клетка не серая"),
	"<rcfix>" : (5, "клетка синяя"),
	"<!rcfix>" : (5, "клетка не синяя"),

	# while conditionals
	"[pit]" : (6, "(кувшин > 0)"),
	"[!pit]" : (6, "(кувшин <= 0)"),
	"[mem]" : (6, "(память > 0)"),
	"[!mem]" : (6, "(память <= 0)"),
	"[memeq]" : (6, "(память = кувшин)"),
	"[memne]" : (6, "(память <> кувшин)"),
	"[memlt]" : (6, "(память < кувшин)"),
	"[memle]" : (6, "(память <= кувшин)"),
	"[memgt]" : (6, "(память > кувшин)"),
	"[memge]" : (6, "(память >= кувшин)"),
	"[fl0]" : (6, "флаг0"),
	"[!fl0]" : (6, "не флаг0"),
	"[fl1]" : (6, "флаг1"),
	"[!fl1]" : (6, "не флаг1"),

	"[rclear]" : (6, "впереди свободно"),
	"[!rclear]" : (6, "не впереди свободно"),
	"[rfwd]" : (6, "можно шагнуть"), #for Mover
	"[!rfwd]" : (6, "можно не шагнуть"), #for Mover

	"[rcnor]" : (6, "клетка голубая"),
	"[!rcnor]" : (6, "клетка не голубая"),
	"[rcbro]" : (6, "клетка серая"),
	"[!rcbro]" : (6, "клетка не серая"),
	"[rcfix]" : (6, "клетка синяя"),
	"[!rcfix]" : (6, "клетка не синяя"),
}

tab_string = "    "

def compile_section(lines):
	stack = []
	stack.append((-1, 1, "кон"))

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
					print(tab_string * (stack[-1][1] - 1) + stack[-1][2])
					stack.pop()
					assert stack
				qb = True

			print(tab_string * stack[-1][1], end='');

			if cci[0] == 1 or cci[0] == 3:
				print(cci[1])

			elif cci[0] == 2: # fixed repeaters
				print("нц " + str(cci[1]) + " раз")
				stack.append((i, stack[-1][1] + 1, "кц"))

			elif cci[0] == 4: # dynamic repeaters (pitcher and memory)
				print("нц " + str(cci[1]) + " раз")
				stack.append((i, stack[-1][1] + 1, "кц"))

			elif cci[0] == 5: # if conditionals
				print("если "+ cci[1] + " то")
				stack.append((i, stack[-1][1] + 1, "все"))

			elif cci[0] == 6: # while conditionals
				print("нц пока "+ cci[1])
				stack.append((i, stack[-1][1] + 1, "кц"))

		pass # for i in range(ls)
	pass # for l in lines

	while stack:
		print(tab_string * (stack[-1][1] - 1) + stack[-1][2])
		stack.pop()

def precompile_program():
	uses = [False] * 5
	uses[0] = True
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
			uses[cur_section] = True
			print("Section " + str(cur_section) + " selected.", file=sys.stderr);
			if main_section == 0:
				main_section = cur_section
			continue
		cur_skip = False
		res[cur_section].append(lw)

		for w in lw:
			if (w in commands) and (commands[w][0] == 3):
				cur_section = ord(w[0]) - ord('@')
				uses[cur_section] = True

	if (not res[0]) and (main_section > 0):
		res[0].append([chr(ord('@') + main_section)])
		uses[main_section] = True
	return res, uses


def main():
	codes, uses = precompile_program()
	cn = len(codes)
	print("использовать Вертун")
	print()
	print("цел кувшин = 0, память = 0")
	print("лог флаг0 = нет, флаг1 = нет")
	print()

	for i in range(cn):
		if codes[i] or uses[i]:
			sname = commands[chr(ord('@') + i)][1]
			print("алг " + sname)
			print("нач")
			compile_section(codes[i])
			print()

main()

