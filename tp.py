import itertools
from collections import defaultdict

from tpconf import tps, dictionary, alpha, letter_to_tp, all_tps

# return set of frozensets
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return set(frozenset(x) for x in
    	itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

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
def words2():
	# mapping from word to what quads spell it
	# use sets because multiple ways to spell a word from a quad
	wordquads = defaultdict(set)
	# quad to words it spells
	quadwords = defaultdict(set)


	# same but with bitset
	iletter_to_tp = {}
	for k in alpha:
		iletter_to_tp[k] = 0
		for i, tp in enumerate(tps):
			if k in tp:
				iletter_to_tp[k] |= 1 << i

	bits_to_quads = {}
	for i in range(1 << len(tps)):
		toadd = list()
		j = i
		while j > 0:
			ffs = (j & (-j)).bit_length() - 1
			j -= j & (-j)
			toadd.append(ffs)
		bits_to_quads[i] = frozenset(toadd)


	iall_tps = (1 << len(tps)) - 1
	def canspell(word, suffix, tps_left):
		if suffix == "":
			used_tps = iall_tps & (~tps_left)
			# assert(len(used_tps) == len(word))
			wordquads[word].add(bits_to_quads[used_tps])
			quadwords[bits_to_quads[used_tps]].add(word)
			return
		# mask to only tps with next letter
		next_tps = tps_left & iletter_to_tp[suffix[0]]
		# foreach set bit
		while next_tps > 0:
			next_bit = next_tps & (-next_tps)
			next_tps -= next_bit
			canspell(word, suffix[1:], tps_left - next_bit)

	for word in dictionary:
		canspell(word, word, iall_tps)

	return wordquads, quadwords

# print(len(quads)) # 1507

# mapping from quad to the words they can spell
# quadwords = {}
# for quad in quads:
# 	quadwords[quad] = words(quad)

wordquads, quadwords = words2()

# all the possible words
allwords = set.union(*list(quadwords.values()))
# print(len(allwords)) # 15367

def out_wordlist(words):
	if not words:
		print("error: nothing found", file=sys.stderr)
	print("\n".join(words))
	# print(len(words))

def out_tp(tp, word):
	tp = set(tp)
	def howspell(suffix, tps_used):
		if suffix == "":
			assert(len(tps_used) == len(word))
			return tps_used
		for next_tp in (tp - set(tps_used)) & letter_to_tp[suffix[0]]:
			r = howspell(suffix[1:], tps_used + [next_tp])
			if r:
				return r
		return False
	spell = howspell(word, [])
	for l in spell:
		print(tps[l])
	print()

def get_remaining_words(used_words):
	possible_quads = set()
	possible_tps = set()
	len_used_words = len("".join(used_words))

	# list of quad options for each word
	used = [
		wordquads[word]
		for word in used_words
	]
	# print(used)

	#
	# for every way to make the words from quads
	for used_quads in itertools.product(*used):
		used_tps = set.union(*[set(u) for u in used_quads])
		if len(used_tps) != len_used_words:
			# skip if we have re-used some tp
			continue
		# Add this iterations unused quads
		unused_tps = frozenset(all_tps - used_tps)

		possible_quads.add(unused_tps)
		possible_tps |= unused_tps

		# if we found them all early abort
		if len(possible_tps) == len(all_tps):
			break
	all_possible_quads = set.union(*[powerset(pq) for pq in possible_quads])
	# print(possible_quads)
	# print(all_possible_quads)

	return set.union(*[quadwords[quad] for quad in all_possible_quads])

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
		for quad, word in zip(used_quads, used_words):
			out_tp(quad, word)

		return

	print("error, cant make those words")

# how_to_make(["lexicography"])

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

