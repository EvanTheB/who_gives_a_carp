import itertools

tps = [
	"xqr",
	"obk",
	"#hw",
	"y&t",
	"hsi",
	"ayg",
	"dcf",
	"mez",
	"l?p",
	"auv",
	"!nr",
	"pej",
]

dictionary = set(
	open("/usr/share/dict/words.pre-dictionaries-common").read().split("\n")
)

dictionary = set.union(dictionary, [
	"evan",
	"lulu",
])

# this is all the 12 choose 4 comboes of tp rolls
quads = list(itertools.combinations(list(range(12)), 4))

def words(quad):
	ret = []
	for order in itertools.permutations(quad):
		quad_tps = [tps[i] for i in order]
		for word in itertools.product(*quad_tps):
			word = ''.join(word)
			if word in dictionary:
				# print(word)
				ret.append(word)
	return set(ret)

# mapping from 4 tps to words they spell
quadwords = {}
for quad in quads:
	quadwords[quad] = words(quad)

allwords = set.union(*list(quadwords.values()))

# mapping from a quad to the other unused quads
quadtoquads = {}
for quad in quads:
	quadtoquads[quad] = list(itertools.combinations(set(range(12)) - set(quad), 4))

# print(len(allwords)) # 1727
# for less_one in itertools.combinations(list(quadwords.values()), len(quadwords) - 1):
# 	# these are all at or slightly under 1727, not many missing words
# 	print(len(set.union(*less_one)))
# exit(1)

def out_wordlist(words):
	print("\n".join(words))
	print(len(words))

def out_tp(tp):
	# todo print words in right order
	for t in tp:
		print(tps[t])
	print()

def get_remaining_words(used_words):
	all_ = set(quadwords)
	possible = set()

	# list of possible quads for each word
	used = [
		[quad for quad, words in quadwords.items() if word in words]
		for word in used_words
	]
	# print(used)

	# for every way to make the words from quads
	for used_quads in itertools.product(*used):
		used_tps = set.union(*[set(u) for u in used_quads])
		if len(used_tps) != len("".join(used_words)):
			# skip if we have re-used some tp
			continue
		# Add this iterations unused quads
		new_tps = set(range(12)) - used_tps
		possible = set.union(
			possible,
			set(itertools.combinations(new_tps, 4))
		)

		# if we found them all early abort
		if len(possible) == len(all_):
			break

	# print(possible)

	return set.union(*list(words for quad, words in quadwords.items() if quad in possible))

import sys
# phrases are A B C
if len(sys.argv) == 1:
	# print all As
	out_wordlist(allwords)

elif len(sys.argv) == 2:
	# print all Bs
	A = sys.argv[1]
	words = get_remaining_words([A])
	out_wordlist(words)

elif len(sys.argv) == 3:
	A = sys.argv[1]
	B = sys.argv[2]
	words = get_remaining_words([A, B])
	out_wordlist(words)

elif len(sys.argv) == 4:
	# print how to
	A = sys.argv[1]
	B = sys.argv[2]
	C = sys.argv[3]

	As = [quad for quad,words in quadwords.items() if A in words]
	Bs = [quad for quad,words in quadwords.items() if B in words]
	Cs = [quad for quad,words in quadwords.items() if C in words]
	# for every way to make "A B C"
	for A, B, C in itertools.product(As, Bs, Cs):
		if A == B or B == C or A == C:
			continue
		out_tp(A)
		out_tp(B)
		out_tp(C)
		break

