import itertools

from tpconf import tps, dictionary, alpha, letter_to_tp

def ints_to_quads(ints):
	return (list(itertools.combinations(ints, 5))
	 + list(itertools.combinations(ints, 4))
	 + list(itertools.combinations(ints, 3))
	 # + list(itertools.combinations(ints, 2))
	 # + list(itertools.combinations(ints, 1))
	)

# this is all the 12 choose 4 comboes of tp rolls
# + the other lengths, still called quads
quads = ints_to_quads(list(range(len(tps))))

# all the words that can be made from a quad
# by considering all permutations
def words(quad):
	ret = []
	for order in itertools.permutations(quad):
		quad_tps = [tps[i] for i in order]
		for word in itertools.product(*quad_tps):
			word = ''.join(word)
			if word in dictionary:
				# print(word)
				ret.append(word)
			elif word[-1] in "?!" and word[:-1] in dictionary:
				ret.append(word)
			# elif word[0] in "#" and word[1:] in dictionary:
			# 	ret.append(word)
	return set(ret)

# by trying to spell each word
def words2(quad):
	def canspell(suffix, tps_left):
		if suffix == "":
			return True
		for next_tp in tps_left & letter_to_tp[suffix[0]]:
			if canspell(suffix[1:], tps_left - set([next_tp])):
				return True
		return False

	return set([w for w in dictionary if all(c in alpha for c in w) and canspell(w, set(quad))])

# mapping from quad to the words they can spell
quadwords = {}
for quad in quads:
	quadwords[quad] = words(quad)

# all the possible words
allwords = set.union(*list(quadwords.values()))

def out_wordlist(words):
	if not words:
		print("error: nothing found", file=sys.stderr)
	print("\n".join(words))
	# print(len(words))

def out_tp(tp):
	# todo print words in right order
	for t in tp:
		print(tps[t])
	print()

def get_remaining_words(used_words):
	all_ = set(quadwords)
	possible = set()

	# list of quad options for each word
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
		new_tps = sorted(set(range(12)) - used_tps)
		possible = set.union(
			possible,
			set(ints_to_quads(new_tps))
		)

		# if we found them all early abort
		if len(possible) == len(all_):
			break

	return set.union(*list(words for quad, words in quadwords.items() if quad in possible))

def how_to_make(used_words):
	# list of quad options for each word
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
		for quad in used_quads:
			out_tp(quad)

		return

	print("error, cant make those words")


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
	how_to_make([A,B,C])

